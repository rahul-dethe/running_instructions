import math
import numpy as np
import time
import sys
import os
from mpi4py import MPI
from setup_v3 import readInput
from MCCI_v3 import performMCCI  # Import the function, not a class

def main():
    # Initialize MPI
    subroutine = MPI.COMM_WORLD
    size = subroutine.Get_size()
    rank = subroutine.Get_rank()

    start_time = time.time()

    try:
        # Read input parameters
        (model, nSite, subSpace, nStates, s2Target, maxItr,
         startSpinTargetItr, energyTola, spinTola, beta, jVal,
         det, Ms, posibleDet, bondOrder, outputfile,
         restart, saveBasis, multi) = readInput()

        # Print header information
        if rank == 0:
            print_header(outputfile)
            print_system_info(outputfile, posibleDet, Ms)

            # Check subspace size
            if subSpace > (sum(posibleDet) * 0.8):
                error_msg = ("\nSub-Space size is more than 80% of total determinants "
                           "space. Make Sub-Space size smaller and run it again.\n")
                print(error_msg)
                with open(outputfile, "a") as fout:
                    fout.write(error_msg)
                sys.exit(1)

        # Synchronize all processes
        subroutine.Barrier()

        # Run MCCI calculation directly
        performMCCI()  # Call the function directly

        # Print completion information
        if rank == 0:
            execution_time = time.time() - start_time
            completion_msg = f"\nTotal Time Taken in MCCI Calculation: {execution_time:.2f} seconds\n"
            with open(outputfile, "a") as fout:
                fout.write(completion_msg)

    except Exception as e:
        if rank == 0:
            error_msg = f"\nError occurred during execution: {str(e)}\n"
            print(error_msg)
            with open(outputfile, "a") as fout:
                fout.write(error_msg)
        sys.exit(1)

def print_header(outputfile):
    """Print ASCII art header to output file"""
    header = """
    A    L           M   M   CCCC   CCCC   II
   A A   L           MM MM  C      C       II
  AAAAA  L     ###   M M M C      C        II
  A   A  L           M   M  C      C       II
  A   A  LLLLL       M   M   CCCC   CCCC   II
    """
    with open(outputfile, "a") as fout:
        fout.write(header + "\n")

def print_system_info(outputfile, posibleDet, Ms):
    """Print system information to output file"""
    total_det = sum(posibleDet)
    info = f"\nTotal Possible Determinants: {total_det}\n"
    info += "Breakup [Ms, No of Determinants]:"

    for i, (ms, det) in enumerate(zip(Ms, posibleDet)):
        info += f" [{ms}, {det}]"
        if i + 1 == len(Ms):
            info += "\n\n"

    with open(outputfile, "a") as fout:
        fout.write(info)

if __name__ == "__main__":
    main()
