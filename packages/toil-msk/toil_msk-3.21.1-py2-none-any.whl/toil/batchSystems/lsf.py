# Copyright (C) 2013 by Thomas Keane (tk2@sanger.ac.uk)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from __future__ import absolute_import
from __future__ import division
from builtins import str
from builtins import range
from past.utils import old_div
import logging
import math
from toil import subprocess
import os
import traceback
import json
import re
from random import randint

from dateutil.parser import parse
from dateutil.tz import tzlocal
from datetime import datetime

from toil.batchSystems import MemoryString
from toil.batchSystems.abstractGridEngineBatchSystem import \
        AbstractGridEngineBatchSystem
from toil.batchSystems.lsfHelper import (parse_memory_resource,
                                         parse_memory_limit,
                                         per_core_reservation)

logger = logging.getLogger(__name__)


class LSFBatchSystem(AbstractGridEngineBatchSystem):

    class Worker(AbstractGridEngineBatchSystem.Worker):
        """LSF specific AbstractGridEngineWorker methods."""

        def getRunningJobIDs(self):
            times = {}
            with self.runningJobsLock:
                currentjobs = dict((str(self.batchJobIDs[x][0]), x) for x in
                                   self.runningJobs)
            process = subprocess.Popen(
                    ["bjobs","-json","-o", "jobid stat start_time"],
                    stdout=subprocess.PIPE)
            stdout, _ = process.communicate()

            output = stdout.decode('utf-8')
            bjobs_records = self.parseBjobs(output)
            if bjobs_records:
                for single_item in bjobs_records:
                    if single_item['STAT'] == 'RUN' and single_item['JOBID'] in currentjobs:
                        jobstart = parse(single_item['START_TIME'], default=datetime.now(tzlocal()))
                        times[currentjobs[single_item['JOBID']]] = datetime.now(tzlocal()) \
                        - jobstart
            return times



        def killJob(self, jobID):
            subprocess.check_call(['bkill', self.getBatchSystemID(jobID)])

        def prepareSubmission(self, cpu, memory, jobID, command):
            return self.prepareBsub(cpu, memory, jobID) + [command]

        def parseBjobs(self,bjobs_output_str):
            bjobs_dict = None
            bjobs_records = None
            # Handle Cannot connect to LSF. Please wait ... type messages
            dict_start = bjobs_output_str.find('{')
            dict_end = bjobs_output_str.rfind('}')
            if dict_start != -1 and dict_end != -1:
                bjobs_output = bjobs_output_str[dict_start:(dict_end+1)]
                try:
                    bjobs_dict = json.loads(bjobs_output)
                except json.decoder.JSONDecodeError:
                    logger.error("Could not parse bjobs output: {}".format(bjobs_output_str))
                if 'RECORDS' in bjobs_dict:
                    bjobs_records = bjobs_dict['RECORDS']
            if bjobs_records == None:
                logger.error("Could not find bjobs output json in: {}".format(bjobs_output_str))

            return bjobs_records


        def submitJob(self, subLine):
            combinedEnv = self.boss.environment
            combinedEnv.update(os.environ)
            process = subprocess.Popen(subLine, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       env=combinedEnv)
            output = process.stdout.read().decode('utf-8')
            logger.debug("BSUB: " + output)
            result_str = re.search('Job <(.*)> is submitted', output)

            if result_str:
                result = int(result_str.group(1))
                logger.debug("Got the job id: {}".format(result))
            else:
                logger.error("Could not submit job\nReason: {}".format(output))
                temp_id = randint(10000000, 99999999)
                result = "NOT_SUBMITTED_{}".format(temp_id)
            return result

        def getJobExitCode(self, lsfJobID):
            # the task is set as part of the job ID if using getBatchSystemID()
            if "NOT_SUBMITTED" in lsfJobID:
                logger.error("bjobs detected job failed to submit")
                return 1
            job, task = (lsfJobID, None)
            if '.' in lsfJobID:
                job, task = lsfJobID.split('.', 1)

            # first try bjobs to find out job state
            args = ["bjobs", "-json", "-o",
                    "user exit_code stat exit_reason pend_reason", str(job)]
            logger.debug("Checking job exit code for job via bjobs: "
                         "{}".format(job))
            process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            output = process.stdout.read().decode('utf-8')
            bjobs_records = self.parseBjobs(output)
            if bjobs_records:
                process_output = bjobs_records[0]
                if 'STAT' in process_output:
                    process_status = process_output['STAT']
                    if process_status == 'DONE':
                        logger.debug(
                            "bjobs detected job completed for job: {}".format(job))
                        return 0
                    if process_status == 'PEND':
                        pending_info = ""
                        if 'PEND_REASON' in process_output:
                            if process_output['PEND_REASON']:
                                pending_info = "\n" + \
                                    process_output['PEND_REASON']
                        logger.debug(
                            "bjobs detected job pending with: {}\nfor job: {}".format(pending_info, job))
                        return None
                    if process_status == 'EXIT':
                        exit_code = 1
                        exit_reason = ""
                        if 'EXIT_CODE' in process_output:
                            exit_code_str = process_output['EXIT_CODE']
                            if exit_code_str:
                                exit_code = int(exit_code_str)
                        if 'EXIT_REASON' in process_output:
                            exit_reason = process_output['EXIT_REASON']
                        exit_info = ""
                        if exit_code:
                            exit_info = "\nexit code: {}".format(exit_code)
                        if exit_reason:
                            exit_info += "\nexit reason: {}".format(exit_reason)
                        logger.error(
                            "bjobs detected job failed with: {}\nfor job: {}".format(exit_info, job))
                        return exit_code
                    if process_status == 'RUN':
                        logger.debug(
                            "bjobs detected job started but not completed for job: {}".format(job))
                        return None
                    if process_status in {'PSUSP', 'USUSP', 'SSUSP'}:
                        logger.debug(
                            "bjobs detected job suspended for job: {}".format(job))
                        return None

            # if not found in bjobs, then try bacct (slower than bjobs)
            logger.debug("bjobs failed to detect job - trying bacct: "
                         "{}".format(job))

            args = ["bacct", "-l", str(job)]
            process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            output = process.stdout.read().decode('utf-8')
            process_output = output.split('\n')
            for line in process_output:
                if line.find("Completed <done>") > -1 or line.find("<DONE>") > -1:
                    logger.debug("Detected job completed for job: "
                                 "{}".format(job))
                    return 0
                elif line.find("Completed <exit>") > -1 or line.find("<EXIT>") > -1:
                    logger.error("Detected job failed for job: "
                                 "{}".format(job))
                    return 1
            logger.debug("Can't determine exit code for job or job still "
                         "running: {}".format(job))
            return None

        """
        Implementation-specific helper methods
        """
        def prepareBsub(self, cpu, mem, jobID):
            """
            Make a bsub commandline to execute.

            params:
              cpu: number of cores needed
              mem: number of bytes of memory needed
              jobID: ID number of the job
            """
            if mem:
                if per_core_reservation():
                    mem = float(mem)/1024**3/math.ceil(cpu)
                    mem_resource = parse_memory_resource(mem)
                    mem_limit = parse_memory_limit(mem)
                else:
                    mem = old_div(float(mem), 1024**3)
                    mem_resource = parse_memory_resource(mem)
                    mem_limit = parse_memory_limit(mem)

                bsubMem = ['-R', 'select[mem > {m}] '
                           'rusage[mem={m}]'.format(m=mem_resource),
                           '-M', str(mem_limit)]
            else:
                bsubMem = []
            bsubCpu = [] if cpu is None else ['-n', str(math.ceil(cpu))]
            bsubline = ["bsub", "-cwd", ".", "-J", "toil_job_{}".format(jobID)]
            bsubline.extend(bsubMem)
            bsubline.extend(bsubCpu)
            stdoutfile = self.boss.formatStdOutErrPath(jobID, 'lsf', '%J', 'std_output')
            stderrfile = self.boss.formatStdOutErrPath(jobID, 'lsf', '%J', 'std_error')
            bsubline.extend(['-o', stdoutfile, '-e', stderrfile])
            lsfArgs = os.getenv('TOIL_LSF_ARGS')
            if lsfArgs:
                bsubline.extend(lsfArgs.split())
            return bsubline

    def getWaitDuration(self):
        """We give LSF a second to catch its breath (in seconds)"""
        return 20

    @classmethod
    def obtainSystemConstants(cls):
        p = subprocess.Popen(["lshosts"], stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        line = p.stdout.readline().decode('utf-8')
        items = line.strip().split()
        num_columns = len(items)
        cpu_index = None
        mem_index = None
        for i in range(num_columns):
                if items[i] == 'ncpus':
                        cpu_index = i
                elif items[i] == 'maxmem':
                        mem_index = i

        if cpu_index is None or mem_index is None:
                RuntimeError("lshosts command does not return ncpus or maxmem "
                             "columns")

        # p.stdout.readline().decode('utf-8')

        maxCPU = 0
        maxMEM = MemoryString("0")
        for line in p.stdout:
            split_items = line.strip().split()
            items = [item.decode('utf-8') for item in split_items if isinstance(item, bytes)]
            if len(items) < num_columns:
                RuntimeError("lshosts output has a varying number of "
                             "columns")
            if items[cpu_index] != '-' and int(items[cpu_index]) > int(maxCPU):
                maxCPU = items[cpu_index]
            if (items[mem_index] != '-' and
                MemoryString(items[mem_index]) > maxMEM):
                maxMEM = MemoryString(items[mem_index])

        if maxCPU is 0 or maxMEM is 0:
                RuntimeError("lshosts returns null ncpus or maxmem info")
        logger.debug("Got the maxMEM: {}".format(maxMEM))
        logger.debug("Got the maxCPU: {}".format(maxCPU))

        return maxCPU, maxMEM
