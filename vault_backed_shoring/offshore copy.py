import math
import numpy as np
import pandas as pd
import streamlit as st

from .base import calc_block_cap

OFFSHORE_ACC_THRESH = 0.0001

# TODO: add st.cache
#  function working out the amount of collateral required for offshores
# def specific_offshore(xhv_qty, xhv_mcap, block_cap, slippage_mult):
def specific_offshore(
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
    '''The “specific” functions are intended for when someone enters an amount in the vault,
    and it will calculate the required collateral.
    
    test_df:
        Shore Type                  object
        XHV (vault)                float64
        XHV to offshore            float64
        xUSD (vault)               float64
        xUSD to onshore            float64
        XHV Supply                 float64
        XHV Price                  float64
        XHV Mcap                   float64
        xAssets Mcap               float64
        Mcap Ratio                 float64
        Spread Ratio               float64
        Mcap VBS                   float64
        Spread VBS                 float64
        Slippage VBS               float64
        Total VBS                  float64
        Max Offshore XHV           float64
        Max Onshore xUSD           float64
        Collateral Needed (XHV)    float64
        TODO FIX Error Message               object: [np.nan | 'incorrect offshore amount' | 'not enough xUSD available to onshore' | 'not enough collateral available']
        dtype: object

    '''
    xhv_mcap = xhv_price * xhv_supply
    # amount_to_onshore_xhv = xusd_to_onshore / xhv_price # TODO: remove

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


    # if (not ignore_errors) and amount_to_onshore_xhv > xusd_vault:
    #     results['Error Message'] = 'not enough xUSD available to onshore'
    #     return results
    if (not ignore_errors) and xhv_to_offshore < static_parameters['min_shore_amount']:
        results['Error Message'] = 'incorrect offshore amount' # -1
        return results
    if (not ignore_errors) and xhv_vault < static_parameters['min_shore_amount']:
        results['Error Message'] = 'not enough unlocked XHV available' # -2
        return results

    # assert(xhv_mcap > 0) # TODO: enable? prolly no cuz it crashes exec

    # validation – ensure onshore amount is not greater than block cap
    # block_cap = math.sqrt(xhv_mcap * static_parameters['block_cap_mult']) # TODO: confirm this is the same for all shoring
    # block cap v2
    block_cap = calc_block_cap(xhv_mcap, xhv_supply, static_parameters['block_cap_mult']) # TODO: will this break all tests?
    if (not ignore_errors) and xhv_to_offshore > block_cap:
        # Error code -3, no message
        return results


    mcap_ratio   = (xassets_mcap / xhv_mcap) # cannot be < 0
    spread_ratio = max(1 - mcap_ratio, 0)
    mcap_ratio = max(mcap_ratio, 0)
    is_healthy   = mcap_ratio <= static_parameters['state_mcap_ratio'] # TODO: problem here?

    # # page 10 of PDF v4
    # TODO: problem here?
    # called "currentVBS" in pseudocode
    mcap_vbs = (math.exp( (mcap_ratio + math.sqrt(mcap_ratio)) * 2) - 0.5) if is_healthy else \
               (math.sqrt(mcap_ratio) * static_parameters['mcap_ratio_mult'])

    spread_vbs = math.exp(1 + math.sqrt(spread_ratio)) + mcap_vbs + 1.5
    if spread_vbs > mcap_vbs:
        mcap_vbs = spread_vbs

    # calculate spread ratio increase
    new_spread_ratio = 1 - ( (xassets_mcap - xusd_to_onshore) / ((xhv_supply + amount_to_onshore_xhv) * xhv_price) )
    if spread_ratio == 0:
        #  prevent div by 0
        increase_spread_ratio = new_spread_ratio - 1
    else:
        increase_spread_ratio = (new_spread_ratio / spread_ratio) - 1
    # TODO: THE COMMENT DOESN'T LINE UP WITH THIS LOGIC. WARNING!!!!
    # if the increase is negative, change it to positive due to square root performed on it
    increase_spread_ratio = max(increase_spread_ratio, 0)
    # increase_spread_ratio = abs(increase_spread_ratio)



    # slippage_mult = static_parameters['slippage_mult_good'] if is_healthy else \
    #                 static_parameters['slippage_mult_bad']
    # slippage_vbs = math.sqrt(increase_spread_ratio) * slippage_mult
    
    # TODO: why aren't we asking about the health??? ASK xKleinroy
    slippage_vbs = math.sqrt(increase_spread_ratio) * static_parameters['slippage_mult_good']

    # set min or max VBS if the calculated VBS is out of bounds
    total_vbs = max(mcap_vbs + slippage_vbs, static_parameters['min_vbs'])

    # total amount of unlocked XHV needed for the onshore specified (includes onshore amount)
    total_collateral = amount_to_onshore_xhv * total_vbs
    if (not ignore_errors) and total_collateral > (xhv_vault * total_vbs):
        results['Error Message'] = 'not enough collateral available' # -4
        return results

    # print(err_msg)
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
        'Mcap Ratio': mcap_ratio, # line 10 of the csv is wack yo TODO: fix??
        'Spread Ratio': spread_ratio,
        'Mcap VBS': mcap_vbs, # TODO: problem here?
        'Spread VBS': spread_vbs,
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

    results = {
        'Shore Type': 'Offshore',
        'XHV (vault)': xhv_vault,
        # 'XHV to offshore': xhv_to_offshore,
        'xUSD (vault)': xusd_vault,
        # 'xUSD to onshore': xusd_to_onshore,
        'XHV Supply': xhv_supply,
        'XHV Price': xhv_price,
        'XHV Mcap': xhv_mcap,
        'xAssets Mcap': xassets_mcap,
        'Mcap Ratio': 0,
        'Spread Ratio': 0,
        'Mcap VBS': 0,
        'Spread VBS': 0,
        'Slippage VBS': 0,
        'Total VBS': 0,
        'Max Offshore XHV': 0,
        'Max Onshore xUSD': 0,
        'Max Onshore XHV': 0,
        'Collateral Needed (XHV)': "TODO",
        'Error Message': "TODO",#np.nan,
    }

    return results
