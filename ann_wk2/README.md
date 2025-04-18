# Guide to Running ANN-CI on NSM Systems

## ⚠️ Important Note
**Do not run MSCC applications on login nodes!**

---

##  Step 1: Login to the NSM System
If you already have a user account in any of the NSM systems, please use your existing credentials to log in.
If you do not have access to any NSM system and wish to create an account, please contact **mscc-support@cdac.in**.

---

##  Step 2: Create input and bond Order file or download the sample input files available in this Github repository.

## 🔧 Setup of Input File (for system 14 nsites)
User needs to configure the input file based on system in considerations. There is no restriction on the name of input file but the extension should be ".in"
In the input file, arguments are given in `"P,Q,R"` format, where:

- **P** is the keyword
- **Q, R** are values associated with the keyword

The setup section is defined between `***startSetup***` and `***endSetup***`.
```
***startSetup***                  # First line of the input setup file
model,HB                          # Hamiltonian model, HB for Heisenberg Hamiltonian model
nSite,14                          # Number of the sites in the system. Here, 14 sites
subSpace,200                      # Initial size of the sub-Hilbert space; starting with 200 configurations
nStates,10                        # Number of states on which spin states are calculated
Ms,1,0                            # Z component of spin: 1st = number of values, 2nd = value (e.g., 0)
s2Target,0                        # Spin value of target states: 0 = singlet, 2 = triplet
maxItr,10                         # Maximum number of iterations
startSpinTargetItr,5              # Iteration from which spin targeting starts (minimum is 5)
energyTola, 0.0005                # Energy convergence threshold
spinTola,0.05                     # Spin convergence threshold
jValue,1                          # Coupling constant
beta,38.61                        # kT value for Boltzmann probability distribution
bondOrder,bondOrder-chain14.dat   # Bond order file (contains node connection info)
restart,False                     # Restart status; use "True" to resume from previous state
***endSetup***                    # Last line of the setup file 
```

📌 **Bond Order File (14 nsites)**:
```
1       2
2       3
3       4
4       5
5       6
6       7
7       8
8       9
9       10
10      11
11      12
12      13
13      14
```


##  Step 3: Running the application: There are two modes in which you can run **Interactive Mode** and **Non-Interactive Mode**.

### A) Running in 'Interactive Mode'
Execute the commands in the given sequence:

```bash
Command 1) sinfo  # To see partition names
```
![sinfo_label](https://github.com/user-attachments/assets/a8e063f6-1628-4cbb-bdf0-f040e53c0dd6)

```
Command 2) salloc -N 1 -p <partition-name> --exclusive  # To assign a node
Command 3) squeue --me                                  # To see the assigned node name
Command 4) ssh <node-name>                              # To log in to the assigned node
```
![salloc, squeue, ssh_label](https://github.com/user-attachments/assets/5b47c8f6-c512-4250-84e2-f333edd2bc76)


After logging into the assigned node, we have to load the Application
```bash
Command 5) module avail | grep -i mscc                 # List all MSCC applications
Command 6) module load MSCC/ann-ci                     # Load ann-ci
```
![ml av, module load](https://github.com/user-attachments/assets/10b226df-1f10-4a50-8728-89b06626eac8)

Command to run the Application
```bash
exe.py <your_input_file>
```
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

---

### 🔹 B) Running an Application in 'Non-Interactive Mode'
Create a file `job.sh`
This is a SLURM batch script used to submit a job to a computing cluster. It automates the job setup, runs your application, and handles input/output.

```bash
#!/bin/bash
#SBATCH --job-name=sys14  # This sets the name of your job
#SBATCH --nodes=1         # Requesting compute node
#SBATCH --exclusive       # Reserves the entire node for your job only
#SBATCH --partition=cpu   # Specifies the partition
#SBATCH --time=48:00:00   # Sets the maximum time limit
#SBATCH --output=%j.out   # Output file
#SBATCH --error=%j.err    # Error file in case of failure

module load MSCC/ann-ci   # Loads the software module required to run your application
cd $SLURM_SUBMIT_DIR      # Changes to the directory where you submitted the job from
exe.py <your_input_file>  # Runs your main application
```
![sbatch script](https://github.com/user-attachments/assets/541dc399-db92-4def-870e-191de06d6b18)

> 📌 **Note:** The names of partitions, modules, and other settings may be different on each NSM HPC cluster.  
> You should manually check your cluster’s documentation to confirm the correct names and update the script accordingly.

---

## 🚀 Step 3: Execute the SLURM Script

Once your `job.sh` file is ready, you can submit your job to the cluster using the command below:

```bash
sbatch job.sh
```
This tells the SLURM scheduler to run your job according to the instructions you mentioned in the script.  
If everything is set up correctly, SLURM will assign resources and begin processing your job in the background. 

![sbatch with squeue](https://github.com/user-attachments/assets/ca2cb65b-b993-468c-a59f-53084726d9ba)

## Output Files
![ann_output](https://github.com/user-attachments/assets/48e011a7-b559-4d27-b7f3-14e33fa28b9a)


---

✅ Following these steps ensures proper execution of ANN-CI on any NSM systems. 🚀

