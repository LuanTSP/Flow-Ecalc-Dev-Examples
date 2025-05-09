# FlowEcalc Example 1: Basic Ecalc Integration

This example shows how to integrate an OPM simulation with the Ecalc economic simulator using a PyAction script. It collects production metrics from the simulation, saves them as a time series, and triggers Ecalc runs at regular intervals.

## 📌 Overview

The purpose of this example is to:

- Monitor selected production data during the simulation (e.g., FOPR, FWIR, FGIR, FWPR).
- Automatically export production metrics to a `.csv` file.
- Trigger Ecalc simulations at specified report steps (e.g., every 10 steps).
- Log relevant outputs for review and debugging.

This setup enables a tight feedback loop between reservoir simulation and economic evaluation, helping assess the financial impact of production profiles as the model evolves.

## 🔄 Code Flow Explanation

The PyAction script follows this flow:

### 1. **Initial Setup (Executed Once)**

- Logs the start of the setup phase.
- Creates a `state` dictionary to store time-series data.
- Sets paths to:
  - The Ecalc YAML model (`yaml_model_path`)
  - The CSV output file for time-series (`timeseries_path`)
  - The Ecalc output folder (`ecalc_output`)
- Defines:
  - Supported production keywords to track (`keywords`)
  - Report steps that will trigger Ecalc (`ecalc_reportsteps`)
- Flags `setup_done = True` to prevent reinitialization.

### 2. **Each Report Step**

- Gets the current simulation date from the schedule.
- Checks if the current date is already in the state:
  - If not, appends the current date.
  - Then, for each production keyword, appends the current value to the state.

### 3. **Triggering Ecalc**

- If the current report step is one of the predefined steps (every 10 steps in this example):
  - Writes the full `state` dictionary to `production_data.csv`.
  - Runs Ecalc using the `subprocess` module:
    - Executes `ecalc run` with the YAML model and production data.
    - Saves results in the specified `ecalc_output` folder.
    - Logs output and any errors to both stdout and OPM's log.
