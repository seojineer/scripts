import os
import argparse
from rtllauncher import run_command

work_dir="/user/seojikim/work/trunk"
RTLSIM_ERR_LOG='[ERR] Failed to run RTLSIM. Exit code is not 0.'

def main():
        ###########################################################################################
        # Argument parser
        ###########################################################################################

        parser = argparse.ArgumentParser()
        parser.add_argument("--rtl_test",
                                                        help="RTL test directory name",
                                                        dest="rtl_test",
                                                        required=True)
        parser.add_argument("--rtl_dir",
                                                        help="RTL test directory path",
                                                        dest="rtl_dir",
                                                        required=True)
        args, _ = parser.parse_known_args()

        print(args.rtl_test)
        rtl_test=args.rtl_test
        rtl_dir=args.rtl_dir

        ###########################################################################################
        # Run RTLSIM
        ###########################################################################################

        # run rtlsim directly
        os.chdir(work_dir)
        cmd='source SourceME; cd ' + rtl_dir + '/' + rtl_test + '; make fw; make host; make done; make'
        p=run_command(cmd)

        # log capture for jenkins
        while True:
            output=p.stdout.readline()
            if p.poll() is not None:
                break
            if output:
                print(output.strip())
        rc=p.poll()

        if p.returncode is not 0:
            print(RTLSIM_ERR_LOG)
            exit() 

        pass

if __name__ == "__main__":
        main()
