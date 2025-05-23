#!/bin/bash
#SBATCH --job-name=sites18
#SBATCH --nodes=1
#SBATCH --partition=cpu
#SBATCH --time=48:00:00
#SBATCH --output=%j.out
#SBATCH --error=%j.err

module load MSCC/ann-ci
cd $SLURM_SUBMIT_DIR
exe.py 18site_pah_S.in
