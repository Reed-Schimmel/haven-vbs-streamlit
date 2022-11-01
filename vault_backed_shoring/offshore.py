import math
import numpy as np
import pandas as pd
import streamlit as st

from .base import calc_block_cap, calc_current_vbs, calc_slippage_vbs

OFFSHORE_ACC_THRESH = 0.0001

# TODO: add st.cache
#  function working out the amount of collateral required for offshores
# def specific_offshore(xhv_qty, xhv_mcap, block_cap, slippage_mult):
def specific_offshore( # TODO: restore docstring
    xhv_vault,
    xhv_to_offshore,
    xusd_vault,
    xusd_to_onshore,
    xhv_price,
    xhv_supply,
    xassets_mcap,

    static_parameters,#=st.session_state['static_parameters'],
    ignore_errors=False,
    ):

    xhv_mcap = xhv_price * xhv_supply
    
    results = {
        'Shore Type': 'Offshore Specific',
        'XHV (vault)': xhv_vault,
        'XHV to offshore': xhv_to_offshore,
        'xUSD (vault)': xusd_vault,
        'xUSD to onshore': xusd_to_onshore,
        'XHV Supply': xhv_supply,
        'XHV Price': xhv_price,
        'XHV Mcap': xhv_mcap,
        'xAssets Mcap': xassets_mcap,
        'Mcap Ratio': 0, # line 10 of the csv is wack yo TODO: fix??
        'Spread Ratio': 0,
        'Mcap VBS': 0, 
        'Spread VBS': 0,
        'Slippage VBS': 0,
        'Total VBS': 0,
        'Max Offshore XHV': 0,
        'Max Onshore xUSD': 0,
        'Collateral Needed (XHV)': 0,
        'Error Message': np.nan,
    }

    if (not ignore_errors) and xhv_to_offshore < static_parameters['min_shore_amount']:
        results['Error Message'] = 'incorrect offshore amount' # -1
        return results
    if (not ignore_errors) and xhv_vault < static_parameters['min_shore_amount']:
        results['Error Message'] = 'not enough unlocked XHV available' # -2
        return results

    block_cap = calc_block_cap(xhv_mcap, xhv_supply, static_parameters['block_cap_mult'])
    if (not ignore_errors) and xhv_to_offshore > block_cap:
        results['Error Message'] = 'offshore amount greater than block limit' # -3
        # Error code -3, no message in ref code but this code includes it
        return results

    mcap_ratio   = (xassets_mcap / xhv_mcap) # cannot be < 0
    new_mcap_ratio = ((xhv_to_offshore * xhv_price) + xassets_mcap ) / ((xhv_supply - xhv_to_offshore) * xhv_price)
    if mcap_ratio <= 0:
        increase_ratio = new_mcap_ratio
        current_vbs = 0
    else:
        increase_ratio = (new_mcap_ratio / mcap_ratio) - 1
        current_vbs = calc_current_vbs(mcap_ratio, static_parameters['mcap_ratio_mult'])
    increase_ratio = abs(increase_ratio)

    slippage_mult = static_parameters['slippage_mult_good'] if mcap_ratio < 0.1 else static_parameters['slippage_mult_bad']
    slippage_vbs = calc_slippage_vbs(increase_ratio, slippage_mult)

    # set min or max VBS if the calculated VBS is out of bounds
    total_vbs = max(current_vbs + slippage_vbs, static_parameters['min_vbs'])
    
    # total amount of unlocked XHV needed for the offshore specified (includes offshore amount)
    total_collateral = math.floor((xhv_to_offshore * total_vbs) + xhv_to_offshore)
    if (not ignore_errors) and (total_collateral > xhv_vault):
        results['Error Message'] = 'not enough collateral available' # -4
        return results
    
    results.update({
        # 'Shore Type': 'Onshore Specific',
        # 'XHV (vault)': xhv_vault,
        # 'XHV to offshore': xhv_to_offshore,
        # 'xUSD (vault)': xusd_vault,
        # 'xUSD to onshore': xusd_to_onshore,
        # 'XHV Supply': xhv_supply,
        # 'XHV Price': xhv_price,
        # 'XHV Mcap': xhv_mcap,
        # 'xAssets Mcap': xassets_mcap,
        # 'Mcap Ratio': mcap_ratio, # line 10 of the csv is wack yo TODO: fix??
        # 'Spread Ratio': spread_ratio,
        # 'Mcap VBS': mcap_vbs, # TODO: problem here?
        # 'Spread VBS': spread_vbs,
        'Slippage VBS': slippage_vbs,
        'Total VBS': total_vbs,
        # 'Max Offshore XHV': -1,
        # 'Max Onshore xUSD': -1,
        'Collateral Needed (XHV)': total_collateral,
        # 'Error Message': err_msg,
    })
    return results

def max_offshore(
    xhv_price,
    xhv_vault,
    xusd_vault,
    xhv_supply,
    xassets_mcap,
    ):
    '''The “max” functions are intended for when the user wants to offshore or onshore the
    maximum amount possible. This will allow us to introduce a “Max” button in the vault,
    which will save users a lot of time trying to guess what that maximum value might be.'''

    xhv_mcap = xhv_price * xhv_supply

    init_results = specific_offshore(
        xhv_vault,
        xhv_vault,
        xusd_vault,
        0,
        xhv_price,
        xhv_supply,
        xassets_mcap,
        static_parameters)

    if init_results['Error Message'] != np.nan:
        return init_results # was an error
        # TODO: ing I was here <--------------------------

    

    # return results
