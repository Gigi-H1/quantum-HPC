#!/bin/bash

# Copy/paste this job script into a text file and submit with the command:
#    sbatch thefilename
# job standard output will go to the file slurm-%j.out (where %j is the job ID)

#SBATCH --time=00:15:00   # walltime limit (HH:MM:SS)
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=8   # 8 processor core(s) per node 
#SBATCH --mem=16G   # maximum memory per node
#SBATCH --gres=gpu:v100:2   # request 1 NVIDIA V100 GPU
#SBATCH --partition=scavenger    # gpu node(s)
#SBATCH --job-name="job"
#SBATCH --mail-user=gharrabil@iastate.edu   # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE

# Load necessary modules
module load miniconda3
conda create cuda-quantum2
module load  cuda/11.8.89-oequqoy 
pip install qiskit-aer-gpu
module load py-matplotlib/3.8.3-py310-fp2sij3
# Set environment variables
export CUDA_VISIBLE_DEVICES=0

# Run the Python script


python four-bw-statevec-v1.py --csv four-statevec-v1.csv
