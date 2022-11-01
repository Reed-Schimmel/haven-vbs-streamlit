import math

# v2
def calc_block_cap(xhv_mcap, xhv_supply, block_cap_mult=3000, block_cap_exp=0.42, supply_pct=0.005):
    return ((xhv_mcap * block_cap_mult) ** block_cap_exp) + (xhv_supply * supply_pct)

def calc_current_vbs(mcap_ratio, mcap_ratio_mult, thresh=0.9): # TODO: should it be < or <= thresh?
    return (math.exp((mcap_ratio + math.sqrt(mcap_ratio)) * 2) - 0.5) if mcap_ratio < thresh else \
           (math.sqrt(mcap_ratio) * mcap_ratio_mult)