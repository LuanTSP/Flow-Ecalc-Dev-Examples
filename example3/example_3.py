# This script integrates an OPM reservoir simulation with periodic calls to 
# the economic simulator (Ecalc). It tracks specific production metrics across report steps, 
# stores them in a timeseries CSV, and triggers Ecalc runs at user-defined intervals.
# 
# Main Features:
# - Initializes necessary paths, state dictionary, and configuration on first run.
# - Collects production data (e.g., FOPR, FWIR, FGIR, FWPR) during simulation steps.
# - Avoids duplicate time entries and appends only new data.
# - Every N report steps (e.g., every 10 steps), the script:
#   - Saves the accumulated timeseries data to a CSV.
#   - Calls the external Ecalc process with appropriate arguments.
#   - Logs outputs and errors for traceability.
# 
# Intended Use:
# To be run inside a PyAction script context in OPM simulations, where the simulation engine 
# can periodically evaluate production economics during runtime.


import opm_embedded as opm_embedded
import pandas as pd
import subprocess
from api.api import WellConInje

# CURRENT SUMMARY, REPORT STEP and SCHEDULE
current_summary_state = opm_embedded.current_summary_state
current_report_step = opm_embedded.current_report_step
current_schedule = opm_embedded.current_schedule


# SETUP
if not "setup_done" in locals():
  opm_embedded.OpmLog.info("STARTING PYACTION SETUP...")

  # CREATE STATE
  state = dict()

  # PATH CONFIG
  yaml_model_path = "/home/luantsp/Documentos/Projetos/FlowEcalc/examples/example3/simple_model_example/modified_simple_model_example.yml"
  timeseries_path = "/home/luantsp/Documentos/Projetos/FlowEcalc/examples/example3/simple_model_example/production_data.csv"
  ecalc_output = "/home/luantsp/Documentos/Projetos/FlowEcalc/examples/example3/ecalc_output"

  # SUPPORTED KEYWORDS
  keywords = ["FOPR", "FWIR", "FGIR", "FWPR"]

  # REPORT STEPS THAT ECALC SHOULD RUN
  ecalc_reportsteps = [x for x in range(120) if (x + 1) % 10 == 0]

  # CREATE WellConInje class
  inj_cntl = WellConInje()

  # FINISH SETUP
  setup_done = True
  opm_embedded.OpmLog.info("PYACTION SETUP DONE")


# DEFINE WELL UPDATE FUNCTIONS
# def update_well_injection_constrain(well_name: str, value: float, reportstep: int):
#   if (current_report_step == reportstep):
#     kw = f"""
#     WCONINJE
#     -- Item #:1	 2	 3	 4	5      6  7
#         '{well_name}'	'GAS'	'OPEN'	'RATE'	{value} 1* 9014 /
#     /
#     """
#     current_schedule.insert_keywords(kw)


if (current_report_step in ecalc_reportsteps):
  inj_cntl.update("INJ", "GAS", "OPEN", "RATE", "50000", "1*", 9014, "1*", "1*")


# UPDATE STATE EVERY REPORTSTEP
if "DATES" not in state:
    state["DATES"] = []


# only add state if not duplicate DATES exists
time = current_schedule.reportsteps[current_report_step]
if not time in state["DATES"]:
    state["DATES"].append(time)

    # add other state columns
    for kw in keywords:
        if kw in current_summary_state:
            if kw not in state:
                state[kw] = []
            state[kw].append(current_summary_state[kw])


# RUN ECALC FOR SELECTED REPORT STEPS
if (current_report_step in ecalc_reportsteps):
  # SAVE STATE AS TIMESERIES TO BE USED BY ECALC
  pd.DataFrame(state).to_csv(timeseries_path, index=None)
  
  # RUN ECALC AND OUTPUT TO TERMINAL
  opm_embedded.OpmLog.info("\n" + "="*60)
  opm_embedded.OpmLog.info(f"Running Ecalc simulation for reportstep {current_report_step}...")
  output = subprocess.run(
    f"ecalc run {yaml_model_path} --output-folder={ecalc_output} --name-prefix=model_timestep_{current_report_step}", 
    shell=True, 
    text=True,
    capture_output=True
  )
  
  print(output.stdout)
  print(output.stderr)

  opm_embedded.OpmLog.info("="*60)



