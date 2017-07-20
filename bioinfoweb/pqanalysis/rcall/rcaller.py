""" R caller is used as a helper 
to call R scripts using Python """

import os
import subprocess
import shlex

from subprocess import Popen, PIPE, STDOUT
from django.conf import settings

class R_Caller():

    def __init__(self, user_name, stats_option, assay_type, data_dir, analysis_id, graph, output_dir="./",):

        self.user_name = user_name
        self.stats_option = stats_option
        self.assay = assay_type
        self.data_dir = data_dir
        self.output_dir = output_dir + analysis_id + ".html"
        self.analysis_id = analysis_id
        self.graph_type = graph

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.markdown_file = os.path.join(base_dir, 'pqresults', 'rscripts', 'PQReportCompiler5.Rmd')

    def set_defaults(self):
        """ Sets the default settings if none is specified """

        base_dir = os.path.dirname(os.path.abspath(__file__))

        settings = {
            'paraflu':{'worklist_file': os.path.join(base_dir, 'defaults', 'paraflu','worklist', 'worklist.id.csv'),
                       'limits_file': os.path.join(base_dir, 'defaults', 'paraflu', 'limits', 'assay.limits.csv')
                      }
        }

        if self.assay == 'Paraflu':
            self.worklist_file = settings['paraflu']['worklist_file']
            self.limits_file = settings['paraflu']['limits_file']
        else:
            pass

    def execute(self, default=True, *args, **kwargs):

        """ Execute is used as the main entrance point of the 
        program. Execute takes care of the main logic. If default settings
        are used, it will directly call r markdown script, else it will
        use user inputs

        Args:
            defaults - to switch defaults on/off (bool)
            *args - None
            **kwargs - 
              
                (0) user_name
                (1) data_dir
                (2) stats_option
                (3) assay_type
                (4) wrk_list
                (5) limits_list
                (6) lof
                (7) analysis_id
                (8) graph_type
        Returns:
            If run was executed. (bool)
        """

        logs = None

        if default:
            if self.assay == 'Paraflu':
                logs = self.__call_r_markdown(self.markdown_file,
                                              self.output_dir,
                                              self.user_name,
                                              self.data_dir,
                                              self.stats_option,
                                              'Paraflu', 
                                              self.worklist_file, 
                                              self.limits_file,
                                              self.analysis_id,
                                              self.graph_type)
        else:
            try:
                markdown_arg = self.markdown_file
                data_arg = kwargs.get('data_dir')
                user_arg = kwargs.get('user_name')
                stat_arg = kwargs.get('stats_option')
                assay_arg = kwargs.get('assay_type')
                work_arg = kwargs.get('wrk_list')
                limit_arg = kwargs.get('limits_list')
                analysis_id = kwargs.get('analysis_id')
                graphing_type = kwargs.get('graphing_type', 'time')
                ignoreflag_arg = kwargs.get('ignoreflags_options')

                logs = self.__call_r_markdown(markdown_arg, 
                                              self.output_dir, 
                                              user_arg, 
                                              data_arg, 
                                              stat_arg, 
                                              assay_arg, 
                                              work_arg, 
                                              limit_arg, 
                                              analysis_id, 
                                              graphing_type, 
                                              ignoreflag_arg)

            except KeyError:
                print("MISSING ARGUMENTS")

        return logs

    def __call_r_markdown(self, markdown_file, output_dir, user_name, data_dir, 
                        stat_type, assay_type, worklist_file, limits_file, 
                        analysis_id, graphing_type, ignore_flags):
        
        """ call_r_markdown is a method used for executing the
        R markdown script PQReportCompiler.Rmd. The PQReportCompiler
        takes a directory of 'Panther PCR' files, combines them,
        then runs an analysis on them and outputs a .html file 

        Args:
            markdown_dir - the file where the *.Rmd file is located.
            output_dir - the directory to output the file
            user_name - name of the runner
            data_dir - the data directory where the PCR data is located.
            stat_type - the stats filter for viewing
            assay_type - the assay type analyzed (paraflu, flu, etc)
            worklist_file - the file containing the naming schema
            limits_file - the file containing the PQ ranges
            ignore_flags - ignore flags from Panther instrument
            analysis_id - the unique tag to group this run
            graphing_type - FVF, time, instrument (changes view of graph)
        Returns:
            None
        Outputs:
            R markdown file
        """

        COMMAND = "Rscript"
        PARAM = "-e"
        RMD_FILE = markdown_file
        OUTPUT_DIR = output_dir
        USR_NAME = user_name
        DATA_DIR = data_dir
        STAT_TYPE = stat_type
        AS_TYPE = assay_type
        WRKLIST = worklist_file
        LIM_FILE = limits_file
        ANA_ID = analysis_id
        GRPH_TYPE = graphing_type
        IGN_FLAG = ignore_flags

        # FOR WINDOWS
        if settings.OPERATING_SYSTEM == "Windows":
          RMD_FILE = RMD_FILE.replace("\\","/")
          OUTPUT_DIR = OUTPUT_DIR.replace("\\","/")
          DATA_DIR = DATA_DIR.replace("\\","/")
          WRKLIST = WRKLIST.replace("\\","/")
          LIM_FILE = LIM_FILE.replace("\\","/")



        FINAL_CMD = "\"rmarkdown::render(input='%s', output_file='%s', params=list(name='%s',"\
                                                                                  "directory='%s',"\
                                                                                  "stats.filter='%s',"\
                                                                                  "assay='%s',"\
                                                                                  "worklist.id='%s',"\
                                                                                  "limits='%s',"\
                                                                                  "analysis.id='%s',"\
                                                                                  "graphing='%s'," \
                                                                                  "ignore.flags=%s"\
                                                                                  "))\"" % (RMD_FILE, OUTPUT_DIR, USR_NAME,
                                                                                            DATA_DIR, STAT_TYPE, AS_TYPE,
                                                                                            WRKLIST, LIM_FILE,
                                                                                            ANA_ID, GRPH_TYPE, IGN_FLAG)

        execute_cmd = [COMMAND, PARAM, FINAL_CMD]
        execute_to_str = " ".join(execute_cmd)
        print(execute_to_str)

        # // LATER FIX -- WHY DOESN'T CENTOS NOT LIKE SHLEX.SPLIT??
        args=execute_to_str
        
        # args = shlex.split(execute_to_str)

        logs = subprocess.Popen(args, stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)

        # run_completed = True
        #
        # while True:
        #
        #     line = logs.stdout.readline()
        #     print(">>> ", line)
        #
        #     if "Execution halted" in line:
        #         print("IT BROKE!!!!!!!!!")
        #         run_completed = False
        #         break
        #
        #     if line == '':
        #         break

        return logs

if __name__ == '__main__':

    """ STANDALONE SCRIPT RUNNER """


    r = R_Caller("bob", "none", 'Paraflu', os.path.join(os.getcwd(), 'data'), "test", "instrument")
    r.set_defaults()
    r.execute()
