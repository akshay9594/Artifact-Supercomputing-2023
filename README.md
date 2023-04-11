# Artifact Description for the Evaluation of Subscripted Subscript Analysis
We have developed a new analysis technique for the automatic parallelization of subsripted
subscript loops. The technique analyzes loops that define and/or modify the subscript array
and determines array properties which is sufficient to parallelize a class of subscripted
subscripts. This repository mentions benchmark source codes used to evaluate two capabilites
of the technique - (a) determining monotonicity of arrays that store intermittent sequences
and (b) determining monotonicity of multi-dimensional subscript arrays. The technique has
been described in detail in our paper - "Recurrence Analysis for Automatic Parallelization
of Subscripted Subscripts" submitted to the Supercomputing 2023 conference. 

## Execution environment
The results described in the above submitted paper have been gathered on the following machine-
The execution times for both applications were recorded on a compute node with a 20-core Intel 
Xeon Gold 6230 processors in a dual socket configuration, with a processor base frequency of 
2.1 GHz, 27.5MB cache and we used upto 8GB of DDR4 memory. The application codes were compiled 
using GCC v4.8.5 with the -O3 optimization flag enabled on CentOS v7.4.1708 and we report 
the mean of 5 application runs. We observed an average run-to-run variation of 1.45% and we 
used one thread per core.

## Dependencies
### Software
 - GNU C Compiler (GCC) v4.8.5 and above
 - Python v3.8.0 and above
 - OpenMP v4.0 and above

### Hardware
 - Machine with Intel processors

## Obtaining the Codes
The codes to reproduce the results can be obtained by cloning this repository using the commands-
```
cd $HOME or cd ~
git clone (https://github.com/akshay9594/Artifact-Supercomputing-2023.git)
cd Artifact-Supercomputing-2023
```
This repository contains the benchmarks and codes listed below:

| Code  | Source | Original Source link | 
| ------------- | ------------- | ------------- |
| Amgmk-v1.0  | CORAL Benchmark Codes | (https://asc.llnl.gov/coral-benchmarks)
| UA-NPB-1.0.3  | NAS Parallel Benchmarks | (https://github.com/akshay9594/SNU_NPB-1.0.3)

## Directory Tree and Code Descriptions
The directory layout of this Artifact is as follows-

```bash
├── Artifact-Supercomputing-2023
│   ├── amgmk-v1.0
│   │   ├── Baselines
│   │   │   ├── Cetus-Output-WithoutSubSub
│   │   │   ├── Serial
│   │   └── Technique_Applied
│   ├── UA-NPB-1.0.3
│   │   ├── Baselines
│   │   │   ├── Cetus-Output-WithoutSubSub
│   │   │   ├── Serial
│   │   └── Technique_Applied
└── README.md
```
### Baseline and Optimized Codes
The experiments have two Baselines against which performance improvement is measured:
 - Serial Code
 - Cetus Parallelized code (without subscripted subscript analysis applied)

***The serial baseline codes have been placed in the "Serial" directory
and the Cetus parallelized codes (without subscripted subscript analysis applied) have 
been placed in the "Cetus-Output-WithoutSubSub" directory.***

***The Cetus parallelized code with subscripted subscript analysis (Optimized codes) 
applied has been placed in the "Technique_Applied" directory.***

### Compiling and Running the Codes
