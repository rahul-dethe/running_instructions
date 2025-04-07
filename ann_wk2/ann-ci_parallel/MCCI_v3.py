import numpy as np
from bitstring import BitArray
import random
import math
import os
from newGeneration_v3 import makeNewGeneration, makeNewMlGeneration
from newConvergence_v3 import checkConvergence, checkFinalConv, makeFitGeneration, convInitializer, update, updateDeterminatList
from spinCalculator import spinCalculator, stateFinder
from setup_v3 import readInput
from mpi4py import MPI
import time

subroutine = MPI.COMM_WORLD
size = subroutine.Get_size()
rank = subroutine.Get_rank()

model, nSite, subSpace, nStates, s2Target, maxItr, startSpinTargetItr, energyTola, spinTola, beta, jVal, det, Ms, posibleDet, bondOrder, outputfile, restart, saveBasis, multi = readInput()

os.environ["OMP_NUM_THREADS"] = multi  # export OMP_NUM_THREADS=x
os.environ["MKL_NUM_THREADS"] = multi  # export MKL_NUM_THREADS=x

if model == 'HB':
    from HeisenHam_v1 import Hamiltonian
if model == 'GM':
    from GhoshMajumHam import Hamiltonian

mlStart = 4
mlPerSpace = 3
spaceIncrease = subSpace

dataFile = outputfile + ".TrainData_subSpace.csv"

def performMCCI():
    convReach = False
    subBasis = []
    if rank == 0:
        if restart:
            with open(saveBasis, "r") as fsaveB:
                for i in range(subSpace):
                    line = fsaveB.readline()
                    det0 = BitArray(bin=line.strip())
                    subBasis.append(det0)
        else:
            for i in range(len(det)):
                det0 = det[i]
                random.shuffle(det0)
                subBasis.append(det0)
                if Ms[0] == 0:
                    subBasis.append(~det0)
                    detCopy0 = BitArray()

            for i in range(len(det)):
                while len(subBasis) < int(subSpace * (i + 1) / len(det)):
                    detCopy0 = subBasis[i * 2].copy()
                    random.shuffle(detCopy0)
                    if detCopy0 not in list(subBasis):
                        subBasis.append(detCopy0)
                        if Ms[0] == 0 and ~detCopy0 not in list(subBasis):
                            subBasis.append(~detCopy0)
    subBasis = subroutine.bcast(subBasis, root=0)

    # Compute initial Hamiltonian matrix and reduce to root
    sh = Hamiltonian(subBasis)
    if rank == 0:
        subHam = np.zeros((len(subBasis), len(subBasis)), dtype=float)
    else:
        subHam = None
    subroutine.Reduce(sh, subHam, op=MPI.SUM, root=0)

    lenSB = len(subBasis)
    ciCoefL = []
    energyL = []
    if rank == 0:
        energyL, vecsL = np.linalg.eigh(subHam)
        for ix in range(nStates):
            for jx in range(lenSB):
                ciCoefL.append(vecsL[jx][ix])

    energyL = subroutine.bcast(energyL, root=0)
    ciCoefL = subroutine.bcast(ciCoefL, root=0)
    energy = np.array(energyL)
    ciCoef = np.array(ciCoefL)

    energyMin = energy[0]
    ciCoefMin = ciCoef[0:lenSB]

    s2ValMin = 100
    targetState, s2ValDiff, energyChange = ([],) * 3
    targetState, s2ValList, s2ValDiff, energyChange, spinChange = convInitializer()

    allDetCi = {}
    kValue = [0, 0]  # to check if space size increased or not
    for i in range(maxItr):
        k = max(0, math.floor((i - mlStart - 3) / mlPerSpace))
        newSize = k * spaceIncrease + subSpace

        kValue[0] = kValue[1]
        kValue[1] = k
        kDiff = kValue[1] - kValue[0]

        # Create new generation
        newGen = []
        lenNewGen = 0
        if rank == 0:
            if i <= mlStart:
                newGen, lenNewGen = makeNewGeneration(subBasis)
            if i == mlStart + 1:
                with open(outputfile, "a") as fout:
                    fout.write("\nStarting Active-Learning Protocol\n")
            if i > mlStart:
                newGen, lenNewGen, allDetCi = makeNewMlGeneration(subBasis, dataFile, newSize, allDetCi, k)

        newGen = subroutine.bcast(newGen, root=0)
        lenNewGen = subroutine.bcast(lenNewGen, root=0)
        allDetCi = subroutine.bcast(allDetCi, root=0)

        # Compute new generation Hamiltonian and reduce to root
        ng = Hamiltonian(newGen)
        if rank == 0:
            newGenHam = np.zeros((lenNewGen, lenNewGen), dtype=float)
        else:
            newGenHam = None
        subroutine.Reduce(ng, newGenHam, op=MPI.SUM, root=0)

        ciCoefL = []
        energyL = []
        if rank == 0:
            energyL, vecsL = np.linalg.eigh(newGenHam)
            for ix in range(nStates):
                for jx in range(lenNewGen):
                    ciCoefL.append(vecsL[jx][ix])

        energyL = subroutine.bcast(energyL, root=0)
        ciCoefL = subroutine.bcast(ciCoefL, root=0)
        energy = np.array(energyL)
        ciCoef = np.array(ciCoefL)

        s2ValList = spinCalculator(newGen, energy[0:nStates], ciCoef, lenNewGen, convReach)

        if i < startSpinTargetItr:
            targetState[1] = 0
            s2ValDiff = [10, 10]
        elif i == startSpinTargetItr:
            targetState[1], s2ValDiff[1] = stateFinder(s2ValList, s2Target)
            if rank == 0:
                with open(outputfile, "a") as fout:
                    fout.write(f"\nStarting Optimization W.R.T Spin, Target State Spin Value -> {s2Target}\n\n")
            energyMin = energy[targetState[1]]
            s2ValDiff[0] = s2ValDiff[1]
        else:
            targetState[1], s2ValDiff[1] = stateFinder(s2ValList, s2Target)

        ciCoefNew = ciCoef[(lenNewGen) * targetState[1]:(lenNewGen) * (targetState[1] + 1)]
        energyNew = energy[targetState[1]]
        s2ValNew = s2ValList[targetState[1]]
        Eith = energyMin

        if rank == 0:
            allDetCi = updateDeterminatList(allDetCi, newGen, ciCoefNew, dataFile, kDiff)
        allDetCi = subroutine.bcast(allDetCi, root=0)

        subBasis, energyMin, ciCoefMin, s2ValDiff, s2ValMin, energyUpdate = checkConvergence(
            energyMin, energyNew, ciCoefMin, ciCoefNew, s2ValMin, s2ValNew, targetState, newGen, s2ValDiff, i, newSize
        )

        energyChange, spinChange, convReach = checkFinalConv(energyChange, spinChange, Eith, energyMin, s2ValDiff[0], convReach)

        energyUpdate = subroutine.bcast(energyUpdate, root=0)
        if energyUpdate:
            energyFinal, ciFinal, basisFinal = update(energy[0:nStates], ciCoef, newGen, len(newGen))

        if convReach or i == maxItr - 1:
            if convReach and rank == 0:
                with open(outputfile, "a") as fout:
                    fout.write("\nIteration Converged.\n")
            elif rank == 0:
                with open(outputfile, "a") as fout:
                    fout.write("\nReached Max Iteration Number.\n")
            convReach = True
            spinCalculator(basisFinal, energyFinal, ciFinal, len(basisFinal), convReach)
            break

    if rank == 0:
        bF, cF = makeFitGeneration(basisFinal, ciFinal[:len(basisFinal)], len(basisFinal))
        with open(f"{outputfile}.basis", "w") as fbasis:
            for element in bF:
                fbasis.write(element.bin + '\n')
        with open(f"{outputfile}.ci", "w") as fci:
            for element in cF:
                fci.write(str(round(float(element), 6)) + '\n')

# Note: The original code had a commented-out call to performMCCI(), but it's typically called from exe_v3.py
