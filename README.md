# DFT Calculations for CO2 Reduction on Cu(211)

This repository contains the computational framework and atomic structure files for investigating the **CO2 Reduction Reaction (CO2RR)** on the **Cu(211)** stepped surface using Density Functional Theory (DFT).

## Project Overview
The research focuses on modeling the electrochemical environment at the Cu(211) interface, a surface known for high catalytic activity due to its step sites. This repository showcases structural modeling across various potential states and the automation scripts used to manage complex electrochemical DFT workflows with **VASP** (Vienna Ab-initio Simulation Package).

*   **Target System**: Cu(211) surface.
*   **Key Focus**: Surface charge effects, potential-dependent modeling, and solvation effects.
*   **Methodology**: Periodic DFT calculations utilizing dipole corrections and explicit/implicit solvation models.

## Repository Structure
The repository is organized to demonstrate systematic control over simulation parameters, including slab thickness and potential states (represented by charge variations):
```text
.
├── adsorbates/          # Structural models for reaction intermediates
│   └── CHOH_slab_sol/   # Example: Solvated CHOH on Cu(211)
│       ├── Slab_20/     # 20 angstrom slab thickness variations
│       └── dense_sol/   # Potential-dependent models (m10, p10, neutral)
├── scripts/             # Python & ASE scripts for structural manipulation
├── shell_script/        # HPC automation and job distribution for KISTI Nurion
├── slab/                # Clean Cu(211) surface models
└── README.md

## Key features in scripts folder
These tools were developed to streamline the simulation setup and ensure the physical accuracy of the electrochemical models:

Symmetric Slab Generator(symmetric.py): Automatically constructs symmetric slab models to eliminate artificial dipole moments and ensure computational stability in surface calculations.

Neutral Electron Counter (get_nelect.py): A utility to precisely calculate valence electron counts for charged or solvated systems, ensuring the NELECT parameter in the INCAR file is correctly assigned.

HPC Job Automation: Shell scripts designed for batch processing, job distribution, and directory synchronization on SLURM-based clusters (e.g., Nurion).

## Data Availability 
As this research is currently under preparation for publication, this repository serves as a methodological showcase rather than a full data release.

Included: Custom Python/Shell scripts, initial structures (POSCAR), and optimized geometries (CONTCAR) for various states.

Excluded: Raw output files (OUTCAR), convergence parameters (INCAR, KPOINTS), and charge density files (CHGCAR).

Note: The provided CONTCAR files demonstrate the structural stability and convergence of the models. For full energy datasets or collaboration inquiries, please contact me directly.

## Contact
Byungmin Chun

Graduate Student, Department of Chemistry

Korea University

Email: bmchun722@korea.ac.kr

GitHub: @bmchun722
