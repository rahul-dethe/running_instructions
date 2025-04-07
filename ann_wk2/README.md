# Guide to Running ANN-CI on NSM Systems

## ⚠️ Important Note
**Do not run any this or any other MSCC application on login nodes!**

---

##  Step 1: Log in to the NSM System
If you don’t have access, please contact **mscc-support@cdac.in**.

![image](https://github.com/user-attachments/assets/2952413b-ae62-4814-840b-2918a0b57e0b)


---

##  Step 2: Running the Application
There are two ways to run an application: **Interactive Mode** and **Non-Interactive Mode**.

### 🔹 A) Running in 'Interactive Mode'
Execute the commands in the given sequence:

```bash
sinfo  # To see partition names
```
![Screenshot 2025-04-07 115335](https://github.com/user-attachments/assets/2e667b4f-b3cd-4c9a-87df-f8e196f3bf9a)
```
salloc -N 1 -p <partition-name> --exclusive  # To assign a node
squeue --me  # To see the assigned node name
ssh <node-name>  # To log in to the assigned node
```





After logging into the assigned node, follow these steps:

#### 1️⃣ Load the Application
```bash
module load MSCC/ann-ci
```

#### 2️⃣ Create the Input and Bond Order Files
Both files should be in the same directory.

📌 **Example Input File (16 nsites)**:
```
***startSetup***
model,HB
nSite,16
subSpace,500
nStates,10
Ms,1,0
s2Target,0
maxItr,50
startSpinTargetItr,5
energyTola,0.01
spinTola,0.1
jValue,1
beta,38.61
bondOrder,bondOrder-lc16.dat
restart,False
***endSetup***
```

📌 **Example Bond Order File (16 nsites)**:
```
1   2
2   3
3   4
4   5
5   6
6   7
7   8
8   9
9   10
10  11
11  12
12  13
13  14
14  15
15  16
```

#### 3️⃣ Run the Application
```bash
exe.py <your_input_file>
```

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

