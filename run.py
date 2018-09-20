import os, argparse
from subprocess import call

# directory where the TXL rule files are located
TXL_RULES_DIR = "./txl/rules/"

def run_all_examples(in_dir):

    # set output directory (inside current src directory)
    out_dir = in_dir + "out/"

    # clear out out directory
    call("rm -rf " + out_dir + "*", shell=True)

    # iterate through all files in the examples
    for example_filename in os.listdir(in_dir):

        if (os.path.splitext(example_filename)[-1] != ".java"):
            continue

        # get current filename root for class name
        example_filename_root = os.path.splitext(example_filename)[0]
        curr_out_dir = out_dir + example_filename_root

        # make directory using the example program's root name
        call(["mkdir", curr_out_dir])

        # iterate through all TXL rules present
        for txl_filename in os.listdir(TXL_RULES_DIR):

            # get the pattern name from the TXL rule file name
            txl_filename_basic = os.path.splitext(txl_filename)[0].replace("Finder", "").replace("Pattern", "")

            call(["mkdir", curr_out_dir + "/" + txl_filename_basic])

            # run the current rule against the current example
            call(["txl", "-q", os.path.join(in_dir, example_filename), "-o", os.path.join(curr_out_dir, txl_filename_basic + "/" + example_filename) , os.path.join(TXL_RULES_DIR, txl_filename)])

    # clear all additional outputs automatically generated by the TXL rule originally written
    call("rm TransformedFor*.java", shell=True)

if __name__== "__main__":

    # set default directory for example src directory
    examples_dir = "./examples/"

    # set up command-line arguments
    parser = argparse.ArgumentParser(description="ConDesignPatterns: Static concurrency design pattern detection and annotation in Java using TXL. This script will run given example programs against all TXL rules present.")
    # parser.add_argument("-o", action="store_true")
    parser.add_argument("-i", metavar="INPUT PATH", help="Path to the input examples programs (default: ./examples/)", default=examples_dir)
    args = parser.parse_args()

    run_all_examples(args.i)