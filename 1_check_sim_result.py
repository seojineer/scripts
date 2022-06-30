from rtllauncher import *
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
        # Check RTLSIM result
        ###########################################################################################

        log_orig=open(rtl_dir + '/' + rtl_test + '/orig_sim.log').read()
        log_new=open(rtl_dir + '/' + rtl_test + '/sim.log').read()
        launcher.check_rtlsim_result(log_orig, log_new);

if __name__ == "__main__":
        main()
    pass

if __name__ == "__main__":
    main()
