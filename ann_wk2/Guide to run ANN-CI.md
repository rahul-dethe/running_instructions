Guide to run ANN-CI

---------------------------------------------------
exe.py < Input.in> 


Step 1: Load the application
module load MSCC/ann-ci

Step 2: Create input and bond order files (keep both files in same place)

Step 3: Create a slurm script.

#!/bin/bash
#SBATCH --job-name=sys14
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --partition=cpu
#SBATCH --time=48:00:00
#SBATCH --output=%j.out
#SBATCH --error=%j.err

module load MSCC/ann-ci
cd $SLURM_SUBMIT_DIR
exe.py <your_inputfile>  

Step 4: Execute the slurm script to start the job.
Command: sbatch script.sh
