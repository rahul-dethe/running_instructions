#!/bin/bash

#SBATCH --job-name=ashish_par18
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48
#SBATCH --exclusive
#SBATCH --partition=cpu
#SBATCH --time=96:00:00
#SBATCH --output=%j.out
#SBATCH --error=%j.err

source /scratch/d.rahul/miniconda3/bin/activate
conda activate seth_ann_mpi
cd $SLURM_SUBMIT_DIR
mpirun -np 24 python3 exe_v3.py 18site_pah_S.in

