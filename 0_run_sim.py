from rtllauncher import *
import os
import argparse

def main():
        launcher = RTLlauncher()

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

        rtl_test=args.rtl_test
        rtl_dir=args.rtl_dir

        ###########################################################################################
        # Run RTLSIM
        ###########################################################################################

        server=launcher.select_server()
        print(server)
        launcher.run_rtlsim(server, rtl_dir, rtl_test)
        launcher.check_rtlsim_done(rtl_dir, rtl_test)

if __name__ == "__main__":
        main()
