import math
import numpy as np
import pandas as pd
import streamlit as st

from . import max_offshore, specific_offshore, max_onshore, specific_onshore
# from vault_backed_shoring import max_offshore, specific_offshore, max_onshore, specific_onshore


# TODO: add st.cache
def shore(
    shore_type,
    amount_to_shore,
    xhv_price,
    xhv_vault,
    xusd_vault,
    xhv_supply,
    xassets_mcap,

    static_parameters,#=st.session_state['static_parameters'],
    ):
    '''
    (On/Off)Shore Simulation.

    Entry point for calculating VBS.

    Returns dictionary of inputs and outputs.

    :param shore_type: (str) valid inputs are "Onshore" and "Offshore".
    :param xhv_price: (float) XHV Price.
    :param xhv_qty: (float) Amount of unlocked XHV in vault.
    :param xusd_qty: (float) Amount of unlocked xUSD in vault.
    :param xhv_supply: (float) Number of XHV in circulation.
    :param xassets_mcap: (float) Market cap of all assets (in USD).
    :param static_parameters: (dict) VBS rule values for current proposal.
        min_vbs = 1,
        min_shore_amount = 1,
        block_cap_mult   = 3000,
        mcap_ratio_mult  = 40,
        
        # For changing the condition for "good" and "bad" protocol state
        state_mcap_ratio = 0.9,
        slippage_mult_good = 3,
        slippage_mult_bad  = 10,

        locktime_offshore = 21,
        locktime_onshore  = 21,
        conversion_fee_offshore = 1.5,
        conversion_fee_onshore  = 1.5,
    :return: (dict) TODO write me
        "Shore Type": 
        "XHV (vault)": 
        "xUSD (vault)":
        "XHV Supply": 
        "XHV Price": 
        "XHV Mcap": 
        "xAssets Mcap": 
        "Mcap Ratio": 
        "Spread Ratio": 
        "Mcap VBS": 
        "Spread VBS": 
        "Slippage VBS":
        "Total VBS": 
        "Max Offshore xUSD": 
        "Max Offshore XHV": 
        "Max Onshore xUSD": 
        "Max Onshore XHV": 
        'Collateral Needed (XHV)':
        'Error Message':
        "Elapsed days":
    '''
    assert(shore_type == "Onshore" or shore_type == "Offshore")

    # Universal Calculations
    xhv_mcap = xhv_price * xhv_supply
    # assert(xhv_mcap > 0)

    if shore_type == "Onshore":
        if amount_to_shore == "max":
            results = max_onshore(xhv_vault, xusd_vault, xhv_price, xhv_supply, xassets_mcap, static_parameters)
        else:
            xhv_to_offshore = 0
            xusd_to_onshore = amount_to_shore
            results = specific_onshore(xhv_vault, xhv_to_offshore, xusd_vault, xusd_to_onshore, xhv_price, xhv_supply, xassets_mcap, static_parameters)
    elif shore_type == "Offshore":
        if amount_to_shore == "max":
            results = max_offshore(xhv_vault, xusd_vault, xhv_price, xhv_supply, xassets_mcap, static_parameters)
        else:
            xhv_to_offshore = amount_to_shore
            xusd_to_onshore = 0
            results = specific_offshore(xhv_vault, xhv_to_offshore, xusd_vault, xusd_to_onshore, xhv_price, xhv_supply, xassets_mcap, static_parameters)
    # Simulation Values
    sim = {
        "Shore Type": results['Shore Type'],#shore_type,
        "XHV (vault)": xhv_vault,
        "xUSD (vault)": xusd_vault,
        "XHV Supply": xhv_supply,
        "XHV Price": xhv_price,
        "XHV Mcap": xhv_mcap,
        "xAssets Mcap": xassets_mcap,
        # "Mcap Ratio": round(mcap_ratio, 4),
        # "Spread Ratio": round(spread_ratio, 4),
        # "Mcap VBS": round(mcap_vbs, 4),
        # "Spread VBS": round(spread_vbs, 4),
        # "Slippage VBS": round(slippage_vbs, 4), # TODO: fix!
        "Total VBS": results['Total VBS'], # TODO: confirm with Roy
        # "Max Offshore xUSD": "TODO",
        "Max Offshore XHV": results['Max Offshore XHV'],
        "Max Onshore xUSD": results['Max Onshore xUSD'],
        # "Max Onshore XHV": "TODO",
        'Collateral Needed (XHV)': results['Collateral Needed (XHV)'],
        'Error Message': results['Error Message'],
        # f"Max {shore_type} xUSD": "heyyoo",
        # f"Max {shore_type} XHV": "heyyoo",
        # "Elapsed days": "TODO",#(len(st.session_state['simulation_list']) + 1) * 21,
        }

    return sim#.update(results)