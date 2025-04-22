# Guide to Running ANN-CI on NSM Systems

---

##  Step 1: Login to the NSM System
- If you have a user account, please use your existing credentials to log in.  
- If you do not have access to any NSM system and wish to create an account, please contact [mscc-support@cdac.in](mailto:mscc-support@cdac.in).


## ⚠️ Important Note: **Do not run any MSCC application on login nodes!**
---

##  Step 2: Prepare your input and bond Order file or download the sample input files available in this Github repository.
For more details regarding creation of input and bond Order file please refer this repository: https://github.com/dghoshlab/AL-MCCI


##  Step 3: Run the application 
There are two modes in which you can run the application **Interactive Mode** and **Non-Interactive Mode**.

### A) Interactive Mode
In this process we manually allocate a node and then run the applicaion in that node.
Execute the commands in the given sequence:

```bash
Command 1) salloc -N 1                                  # To assign a node
Command 2) squeue --me                                  # To see the assigned node name
Command 3) ssh <node-name>                              # To log in to the assigned node
```
![salloc](https://github.com/user-attachments/assets/f2fba0bc-9167-4e27-ba08-ea474a0aa739)

After logging into the assigned node, we have to load the Application
```bash
Command 4) module avail | grep -i mscc                 # List all MSCC applications
Command 5) module load MSCC/ann-ci                     # Load ann-ci
```
![choose ann-ci](https://github.com/user-attachments/assets/baa3c322-20b5-488c-9c68-cfcb178345d2)

Command to run the Application
```bash
exe.py <your_input_file>                               # To run the application
```
![running the application](https://github.com/user-attachments/assets/9a37669c-4eb3-4067-a080-f1886e5dddac)

### B) Non-Interactive Mode
Create a file `job.sh`
This is a script used to submit a job to a computing cluster. It automates the job setup, runs your application, and handles input/output.

```bash
#!/bin/bash
#SBATCH --job-name=sys10       # This sets the name of your job
#SBATCH --nodes=1              # Requesting compute node
#SBATCH --partition=standard   # Specifies the partition
#SBATCH --time=48:00:00        # Sets the maximum time limit
#SBATCH --output=%j.out        # Output file
#SBATCH --error=%j.err         # Error file in case of failure

module load MSCC/ann-ci        # Kindly check the module name and replace the command accordingly
cd $SLURM_SUBMIT_DIR           # Changes to the directory where you submitted the job from
exe.py <input_file>            # Runs your main application

```
![running the application](https://github.com/user-attachments/assets/95bec1f7-429f-4313-8aeb-c29e3ef06428)



## Output Files

A total of 10 output files are generated after successful calculations.
The main files are:

```
1)  input_file.in.out                        # Main output file, which contains information on subspace size, energy
2)  input_file.in.out.basis                  # Configurations of final sub-Hilbert space
3)  input_file.in.out.ci                     # CI coefficient corresponding to configurations
4)  input_file.in.out.model.pth              # Final optimized ANN model
5)  input_file.in.out.error.dat              # Train and test error at each AL iteration
6)  input_file.in.out.TrainData_subSpace.csv # Train data set generated during calculation
```

These files are essential for system analysis. In addition, there are four more files:

```
7)  input_file.in.out.predictData.csv
8)  input_file.in.out.accVsPreTest.dat
9)  input_file.in.out.accVsPreTrain.dat
10) input_file.in.out.enrich.csv
```

These are scratch files generated during calculations.
It is recommended to delete these files to keep the directory clean.

## Step 3: Execute the Script file

Once your `job.sh` file is ready, run the script using the command below:

```bash
sbatch job.sh             # Executing the batch script
```
This tells the SLURM scheduler to run your job according to the instructions you mentioned in the script.  
If everything is set up correctly, SLURM will assign resources and begin processing your job in the background. 

![sbatch job sh](https://github.com/user-attachments/assets/6e1a50e3-64d6-4816-b042-fb2a06b195c4)


## Output Files
![ann_output](https://github.com/user-attachments/assets/48e011a7-b559-4d27-b7f3-14e33fa28b9a)



---
Please refer to the tutorial video for more detailed running instructions: https://youtu.be/R2KRXly2RBo?si=Wd9UUfS0lKd2Ayfy
---


> 📌 **Note:** The names of partitions, modules, and other settings may be different on each NSM HPC cluster.  
> Please check your cluster’s documentation to confirm the correct names and update the script accordingly.

---
