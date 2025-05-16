#!/bin/bash
#SBATCH --job-name=sites20
#SBATCH --nodes=1
#SBATCH --partition=cpu
#SBATCH --time=48:00:00
#SBATCH --output=%j.out
#SBATCH --error=%j.err

module load MSCC/ann-ci
cd $SLURM_SUBMIT_DIR
exe.py 20site_lc_S.in
