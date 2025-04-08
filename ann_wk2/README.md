# Guide to Running ANN-CI on NSM Systems

## ⚠️ Important Note
**Do not run MSCC applications on login nodes!**

---

##  Step 1: Log in to the NSM System
If you do not have access to any NSM system and would like to create an account, please contact **mscc-support@cdac.in**.



---

##  Step 2: Running the Application
There are two ways to run an application: **Interactive Mode** and **Non-Interactive Mode**.

### 🔹 A) Running in 'Interactive Mode'
Execute the commands in the given sequence:

```bash
sinfo  # To see partition names
```
![sinfo_label](https://github.com/user-attachments/assets/a8e063f6-1628-4cbb-bdf0-f040e53c0dd6)

```
salloc -N 1 -p <partition-name> --exclusive  # To assign a node
squeue --me                                  # To see the assigned node name
ssh <node-name>                              # To log in to the assigned node
```
![salloc, squeue, ssh_label](https://github.com/user-attachments/assets/5b47c8f6-c512-4250-84e2-f333edd2bc76)




After logging into the assigned node, follow these steps:

#### 1️⃣ Load the Application
```bash
module avail | grep -i mscc #List all MSCC applications
module load MSCC/ann-ci     #Load ann-ci
```
![ml av, module load](https://github.com/user-attachments/assets/10b226df-1f10-4a50-8728-89b06626eac8)


#### 2️⃣ Create the Input and Bond Order Files
Both files should be in the same directory.

📌 **Example Input File (14 nsites)**:
```
***startSetup***
model,HB
nSite,14
subSpace,200
nStates,10
Ms,1,0
s2Target,0
maxItr,10
startSpinTargetItr,5
energyTola, 0.0005
spinTola,0.05
jValue,1
beta,38.61
bondOrder,bondOrder-chain14.dat
restart,False
***endSetup***
```

📌 **Example Bond Order File (14 nsites)**:
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

#### 3️⃣ Run the Application
```bash
exe.py <your_input_file>
```
## Output Files

A total of 10 output files are generated after successful calculations.
The main files are:

```
1)  input_file.in.out                     # Main output file, which contains information on subspace size, energy
2)  input_file.in.out.basis               # Configurations of final sub-Hilbert space
3)  input_file.in.out.ci                  # CI coefficient corresponding to configurations
4)  input_file.in.out.model.pth           # Final optimized ANN model
5)  input_file.in.out.error.dat           # Train and test error at each AL iteration
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
While on the **login node**, create a `.sh` file (SLURM script) and copy the lines below:

```bash
#!/bin/bash
#SBATCH --job-name=sys14  # Display name for your job
#SBATCH --nodes=1  # Number of nodes
#SBATCH --exclusive  # Assign a full node exclusively
#SBATCH --partition=cpu  # Partition name
#SBATCH --time=48:00:00  # Time allocation for the node
#SBATCH --output=%j.out  # Output file
#SBATCH --error=%j.err  # Error file in case of failure

module load MSCC/ann-ci  # Load the application
cd $SLURM_SUBMIT_DIR  # Change to the directory where input files are located
exe.py <your_input_file>  # Run the application
```

---

## 🚀 Step 3: Execute the SLURM Script
Run the following command to start the job:
```bash
sbatch script.sh
```

---

✅ Following these steps ensures proper execution of MSCC applications on NSM systems. 🚀

