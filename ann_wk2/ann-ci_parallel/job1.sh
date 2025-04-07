#!/bin/bash

#SBATCH --job-name=20_ashish
#SBATCH --nodes=1
#SBATCH --ntasks=48
#SBATCH --exclusive
#SBATCH --partition=cpu
#SBATCH --time=96:00:00
#SBATCH --output=%j.out
#SBATCH --error=%j.err

# Load Conda environment
source /scratch/d.rahul/miniconda3/bin/activate
conda activate seth_ann_mpi

# Ensure working directory is submission directory
cd $SLURM_SUBMIT_DIR

# Run MPI job with 24 processes
mpirun -np 24 python3 exe_v3.py 20site_lc_S.in
