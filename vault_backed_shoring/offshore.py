import math
import numpy as np
import pandas as pd
import streamlit as st

from .base import calc_block_cap
    # block_cap = calc_block_cap(xhv_mcap, xhv_supply, static_parameters['block_cap_mult']) # TODO: will this break all tests?

OFFSHORE_ACC_THRESH = 0.0001

# TODO: add st.cache
#  function working out the amount of collateral required for offshores
# def specific_offshore(xhv_qty, xhv_mcap, block_cap, slippage_mult):
def specific_offshore(
    xhv_price,
    xhv_qty,
    xusd_qty,
    xhv_supply,
    xassets_mcap,

    xhv_mcap,
    # block_cap,
    slippage_mult,
    is_healthy,
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
        Error Message               object
        dtype: object

    '''
    errs = [nan, 'offshore amount greater than block limit',
       'incorrect offshore amount', 'not enough collateral available'],
    assert(xhv_qty >= st.session_state['static_parameters']['min_shore_amount'])
    # assert(enuff unlocked)
    # ensure offshore amount is not greater than block cap
    block_cap = math.sqrt(xhv_mcap * st.session_state['static_parameters']['block_cap_mult'])
    assert(block_cap >= xhv_qty)


    # st.session_state['static_parameters']['mcap_ratio_mult'] # mcapRatioMultiplier
    # current_vbs
    
    mcap_ratio = xassets_mcap / xhv_mcap
    new_mcap_ratio = ((xhv_qty * xhv_price) + xassets_mcap) / ((xhv_supply - xhv_qty) * xhv_price)

    if mcap_ratio <= 0:
    # mcap_ratio_increase = ()
        increase_ratio = new_mcap_ratio
        current_vbs = 0
    else:
        increase_ratio = abs((new_mcap_ratio / mcap_ratio) -1) # TODO: did the author use the right formula here?
        mcap_vbs = math.exp((mcap_ratio + math.sqrt(mcap_ratio)) * 2) - 0.5 if is_healthy else \
                math.sqrt(mcap_ratio) * st.session_state['static_parameters']['mcap_ratio_mult']
        current_vbs = mcap_vbs

    slippage_vbs = math.sqrt(increase_ratio) * slippage_mult
    total_vbs = max(current_vbs + slippage_vbs, st.session_state['static_parameters']['min_vbs'])
    total_collateral = math.floor((xhv_qty * total_vbs) + xhv_qty)
    return total_collateral

    return {
        'Shore Type': 'Offshore Specific',
        'XHV (vault)': 'TODO',
        'XHV to offshore': 'TODO',
        'xUSD (vault)': 'TODO',
        'xUSD to onshore': 'TODO',
        'XHV Supply': 'TODO',
        'XHV Price': 'TODO',
        'XHV Mcap': 'TODO',
        'xAssets Mcap': 'TODO',
        'Mcap Ratio': 'TODO',
        'Spread Ratio': 'TODO',
        'Mcap VBS': 'TODO',
        'Spread VBS': 'TODO',
        'Slippage VBS': 'TODO',
        'Total VBS': 'TODO',
        'Max Offshore XHV': 'TODO',
        'Max Onshore xUSD': 'TODO',
        'Collateral Needed (XHV)': 'TODO',
        'Error Message': 'TODO',
    }



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
