import subprocess

script_dir="/user/seojikim/work/scripts"
default_server='fdn13'
COMPLETE_LOG_NOT_FOUND='[ERR] Complete Log is not found! Seemd RTLSIM done abnormally.'

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
                    print(COMPLETE_LOG_NOT_FOUND)
                    exit() 
                pass

        def check_rtlsim_result(self):
                pass

def run_command(cmd):
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable='/bin/tcsh')
        return popen
