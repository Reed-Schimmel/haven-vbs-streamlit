import math
import streamlit as st

def shore(
    shore_type,
    xhv_price,
    xhv_qty,
    xusd_qty,
    xhv_supply,
    xassets_mcap
):
    
    # Universal Calculations
    xhv_mcap = xhv_price * xhv_supply
    assert(xhv_mcap > 0)
    block_cap    = math.sqrt(xhv_mcap * st.session_state['static_parameters']['block_cap_mult']) # TODO: confirm this is the same for all shoring
    mcap_ratio   = min(xassets_mcap / xhv_mcap, 0)
    is_healthy   = mcap_ratio < st.session_state['static_parameters']['state_mcap_ratio']
    spread_ratio = 1 - mcap_ratio

    # page 10 of PDF v4
    mcap_vbs = math.exp((mcap_ratio + math.sqrt(mcap_ratio)) * 2) - 0.5 if is_healthy else \
               math.sqrt(mcap_ratio) * st.session_state['static_parameters']['mcap_ratio_mult']

    # TODO: make spread_vbs work
    spread_vbs = "FIX"#math.exp(1 + math.sqrt(spread_ratio)) + mcap_vbs + 1.5

    # TODOing: mcap_ratio_increase
    # LOGIC SPLITS HERE
    slippage_mult = st.session_state['static_parameters']['slippage_mult_good'] if is_healthy else \
                    st.session_state['static_parameters']['slippage_mult_bad']
    if   shore_type == "Onshore":
        pass
    elif shore_type == "Offshore":
        pass

    # TODO LOGIC SPLITS HERE
    new_mcap_ratio = ((xhv_qty * xhv_price) + xassets_mcap) / ((xhv_supply - xhv_qty) * xhv_price)
    mcap_ratio_increase = (new_mcap_ratio - mcap_ratio) / mcap_ratio
    # slippage_vbs = math.sqrt(mcap_ratio_increase) * slippage_mult

    # TODO: send `sim` to functions
    # TODO: update sim with returned values

    # if   sim["Shore Type"] == "Onshore":
    #     pass
    # elif sim["Shore Type"] == "Offshore":
    #     pass

    # sim[f"Max {shore_type} xUSD"] = "Heyyoo"
    # sim[f"Max {shore_type} XHV"] = "Heyyoo"

    # if shore_type == "Onshore":
    #     sim["Max Onshore xUSD"] = "TODO"
    #     sim["Max Onshore XHV"] = "TODO"

    # Simulation Values
    sim = {
        "Shore Type": shore_type,
        "XHV (vault)": xhv_qty,
        "xUSD (vault)": xusd_qty,
        "XHV Supply": xhv_supply,
        "XHV Price ($)": xhv_price,
        "XHV Mcap ($)": xhv_mcap,
        "xAssets Mcap ($)": xassets_mcap,
        "Mcap Ratio": mcap_ratio,
        "Spread Ratio": spread_ratio,
        "Mcap VBS": mcap_vbs,
        "Spread VBS": spread_vbs,
        "Slippage VBS": "TODO",
        "Total VBS": "TODO",
        "Max Offshore xUSD": "TODO",
        "Max Offshore XHV": "TODO",
        "Max Onshore xUSD": "TODO",
        "Max Onshore XHV": "TODO",
        # f"Max {shore_type} xUSD": "heyyoo",
        # f"Max {shore_type} XHV": "heyyoo",
        "Elapsed days": (len(st.session_state['simulation_list']) + 1) * 21,
        }

    return sim

def specific_offshore(xhv_qty, xhv_mcap, block_cap, slippage_mult):
    '''The “specific” functions are intended for when someone enters an amount in the vault,
    and it will calculate the required collateral.'''
    assert(xhv_qty >= st.session_state['static_parameters']['min_shore_amount'])
    # assert(enuff unlocked)

    # current_vbs
    # TODO: <-------------------------------------------------------------------- I was here
    new_mcap_ratio = ((xhv_qty * xhv_price) + xassets_mcap) / ((xhv_supply - xhv_qty) * xhv_price)
    # mcap_ratio_increase = ()
    increase_ratio = new_mcap_ratio # TODOing: <-------------------------------------------------------------------- I was here
    slippage_vbs = math.sqrt(increase_ratio) * slippage_mult
    total_vbs = max(current_vbs + slippage_vbs, st.session_state['static_parameters']['min_vbs'])
    total_collateral = math.floor((xhv_qty * total_vbs) + xhv_qty)
    return total_collateral



def max_offshore():
    '''The “max” functions are intended for when the user wants to offshore or onshore the
    maximum amount possible. This will allow us to introduce a “Max” button in the vault,
    which will save users a lot of time trying to guess what that maximum value might be.'''
    pass

def specific_onshore():
    '''The “specific” functions are intended for when someone enters an amount in the vault,
    and it will calculate the required collateral.'''
    pass

def max_onshore():
    pass