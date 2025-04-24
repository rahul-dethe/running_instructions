#!/bin/bash
#SBATCH --job-name=sys10       # Set the job name
#SBATCH --nodes=1              # Request one compute node
#SBATCH --partition=standard   # Specify the partition/queue
#SBATCH --time=48:00:00        # Set maximum execution time
#SBATCH --output=%j.out        # File to save standard output
#SBATCH --error=%j.err         # File to save error messages

module load MSCC/ann-ci        # Load the ANN-CI module (verify module name if needed)
cd $SLURM_SUBMIT_DIR           # Navigate to the job submission directory
exe.py <input_file>            # Run the ANN-CI application (replace <input_file> accordingly)
