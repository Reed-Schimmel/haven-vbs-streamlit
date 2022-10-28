import math

# v2
def calc_block_cap(xhv_mcap, xhv_supply, block_cap_mult=3000, block_cap_exp=0.42, supply_pct=0.005):
    return ((xhv_mcap * block_cap_mult) ** block_cap_exp) + (xhv_supply * supply_pct)