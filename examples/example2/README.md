# FlowEcalc Example 2: Ecalc Integration with Dynamic Well Constraints

This example demonstrates how to integrate the Ecalc economic simulator into an OPM reservoir simulation using PyAction, while also programmatically modifying well constraints during the simulation.

## 📌 Overview

This PyAction-based integration accomplishes two main goals:

1. **Production-Economics Coupling**: Periodically exports production metrics from the reservoir simulator and evaluates them using Ecalc.
2. **Dynamic Simulation Control**: Changes gas injection constraints at specific report steps to simulate operational adjustments.

This workflow helps quantify the economic impacts of operational decisions in real time as part of a reservoir simulation loop.

## 🔄 Code Flow Explanation

### 1. **Initialization (First-Time Setup)**

- Logs the start of setup using `opm_embedded.OpmLog`.
- Initializes:
  - A dictionary to track production state over time.
  - File paths for:
    - Ecalc YAML model.
    - Time series CSV for Ecalc input.
    - Ecalc output folder.
- Defines:
  - A list of production keywords to monitor: `FOPR`, `FWIR`, `FGIR`, `FWPR`.
  - Report steps (every 10 steps in 120 total) when Ecalc should be triggered.

### 2. **Well Constraint Updates**

- The function `update_well_injection_constrain(well_name, value, reportstep)` injects a `WCONINJE` keyword to modify the gas injection rate of a specified well (`INJ` in this case).
- In this example:
  - At step 5: Gas injection is stopped.
  - At step 10: High gas injection (500,000).
  - At step 15: Low gas injection (10).

### 3. **Collecting Production Data**

- Every report step:
  - Extracts the current simulation time from the schedule.
  - Checks if that date is already recorded. If not:
    - Appends it to the state.
    - Appends values for each production keyword if present in `current_summary_state`.

### 4. **Running Ecalc**

- At selected report steps (every 10):
  - Writes the accumulated production metrics to `production_data.csv`.
  - Calls Ecalc using `subprocess.run(...)`, passing:
    - YAML model path.
    - Output directory and filename prefix.
  - Logs Ecalc's stdout and stderr outputs for inspection.
