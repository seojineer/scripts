import subprocess

script_dir="/user/seojikim/work/scripts"
default_server='fdn13'
ERR_LOG_COMPLETE_LOG_NOT_FOUND='[ERR] Complete Log is not found! Seemd RTLSIM done abnormally.'
FAIL_LOG_RTLSIM_RESULT='[FAIL] RTLSIM sim.log is not same as original log. Failed RTLSIM test!'

class RTLlauncher:
        def __init__(self):
                pass

        def select_server(self):

                ###########################################################################################
                # Check FDN memory of server 
                ###########################################################################################

                server_list=[line.strip() for line in open(script_dir+'/server.lst')]
                for server in server_list:
                    cmd='ssh ' + server + ' free -g | grep Mem | tr -d \"Mem:\"'
                    p=run_command(cmd)
                    (stdoutdata, stderrdata) = p.communicate()
                    free_mem=map(int, stdoutdata.decode('utf8').split())[2]
                    #print(free_mem)

                    if free_mem > 50:
                        return server
                pass

        def run_rtlsim(self, fdn_server, rtl_dir, rtl_test):

                ###########################################################################################
                # Run RTLSIM on fdn_server
                # fdn_server: fdn server name (ex. fdn55, fdn14, ...)
                # rtl_dir: rtl directory path (ex. /user/seojikim/work/trunk/rtl/chip/sim/pt_host/vcpu)
                # rtl_test: rtl directory name (ex. dp000-lnkmgr, sp000-lnkmgr, ...)
                ###########################################################################################

                print('#'*100)
                print('Run RTLSIM - ' + rtl_test)

				# using run_sim_cmd.py script
                cmd='ssh ' + fdn_server + ' python ' + script_dir + '/run_sim_cmd.py --rtl_dir ' + rtl_dir + ' --rtl_test ' + rtl_test
                print(cmd)
                p=run_command(cmd)

                # log capture for jenkins
                while True:
                    output=p.stdout.readline()
                    if p.poll() is not None:
                        break
                    if output:
                        print(output.strip())
                rc=p.poll()

        def check_rtlsim_done(self, rtl_dir, rtl_test):

                ###########################################################################################
                # Check complete message from sim.log file
                # rtl_dir: rtl directory path (ex. /user/seojikim/work/trunk/rtl/chip/sim/pt_host/vcpu)
                # rtl_test: rtl directory name (ex. dp000-lnkmgr, sp000-lnkmgr, ...)
                ###########################################################################################

                print('#'*100)
                print('Check complete log from sim.log file...')
                cmd='ssh '+ default_server + ' \'grep -r \"Simulation complete\" ' + rtl_dir + '/' + rtl_test + '/sim.log\''
                p=run_command(cmd)
                p.communicate()

                if p.returncode is not 0:
                    print(ERR_LOG_COMPLETE_LOG_NOT_FOUND)
                    exit(1)
                pass

        def log_preprocess(self, log):

                ###########################################################################################
                # Remove unnececerry log
                ###########################################################################################

                logs=list()

                for line in log.split('\n'):
                    if len(line.split())<5:
                        continue
                    elif line.split()[4].startswith('(') and line.split()[4].endswith('):'):
                        processed_line=' '.join(line.split()[1:-1])
                        #print(processed_line)
                        logs.append(processed_line)

                return logs

        def check_rtlsim_result(self, log_orig, log_new):

                ###########################################################################################
                # Compare original and new log
                # log_orig: original rtlsim log data
                # log_new: new rtlsim log data
                ###########################################################################################

                processed_orig=self.log_preprocess(log_orig)
                processed_new=self.log_preprocess(log_new)
                tc_res=True

                for line_orig, line_new in zip(processed_orig, processed_new):
                    res=(line_orig==line_new) 
                    if res is not True:
                        tc_res=False
                
                    print('-'*100)
                    print('[ Original log ] : ' + line_orig)
                    print('[    New log   ] : ' + line_new)
                    print('[  Log Compare ] : ' + str(res))
            
                if tc_res is not True:
                    print(FAIL_LOG_RTLSIM_RESULT)
                    exit(1)


def run_command(cmd):
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable='/bin/tcsh')
        return popen
