class WellConInje:
  
  def __init__(self, schedule):
    self.schedule = schedule
    self.template_kw = f"""
    -- WELL FLUID OPEN/ CNTL SURF RESV BHP THP VFP
    -- NAME TYPE SHUT MODE RATE RATE PRSES PRES TABLE
    WCONINJE
    """

  def update(self,
    well_name: str, fluid_type: str, open_shut: str,
    cntl_mode: str, surf_rate: str, resv_rate: str,
    bhp_prses: str, thp_pres: str, vfp_table: str
    ):
    complete_kw = self.template_kw + f"{well_name} {fluid_type} {open_shut} {cntl_mode} {surf_rate} {resv_rate} {bhp_prses} {thp_pres} {vfp_table}"
    self.schedule.insert_keywords(complete_kw)
