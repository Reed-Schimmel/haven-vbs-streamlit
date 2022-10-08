import math

import pandas as pd
import streamlit as st

from vbs import shore#, specific_offshore, specific_onshore, max_offshore, max_onshore


APP_VERSION = "0.0.2"
PROPOSAL_VERSION = 4


st.set_page_config(
    page_title="VBS Simulator",
    page_icon="https://raw.githubusercontent.com/haven-protocol-org/brand-assets/master/Branding%20Kit/png/white/rounded.png",
    layout='wide',
    initial_sidebar_state="collapsed",
    menu_items={
    'Get Help': 'https://discord.com/channels/536838513182638090/570818940553527296',
    'Report a bug': "https://github.com/Reed-Schimmel/haven-vbs-streamlit/issues",
    'About': f"[Haven Protocol](https://havenprotocol.org/). Version {APP_VERSION}"#"[GitHub](https://github.com/Reed-Schimmel/haven-vbs-streamlit)"#\n-[Haven Protocol](https://havenprotocol.org/)"
    })

st.title("VBS Simulator")
st.caption(f"Proposal Version {PROPOSAL_VERSION} | Simulator Version {APP_VERSION}")
# st.caption(f"Simulator Version {APP_VERSION}")


# State Initialization
if 'simulation_list' not in st.session_state:
    st.session_state['simulation_list'] = []

with st.sidebar:
    with st.expander("Static Parameters", expanded=False):
        st.caption('The default values are set to the latest official proposal. Adjusting these is only for hypothetical VBS rules. These changes must be made before the first simulation.')
        min_vbs = st.number_input('Minimum VBS', value=1)
        min_shore_amount = st.number_input('Minimum amount of XHV that can be on/offshored', value=1)
        block_cap_mult   = st.number_input('Multiplier which calculates the amount one can on/offshore inside a single block', value=2500)
        mcap_ratio_mult  = st.number_input('Multiplier for working out the mcap VBS', value=40)
        
        # For changing the condition for "good" and "bad" protocol state
        state_mcap_ratio = st.number_input(
            label='Protocol state threshold',
            help='mcap ratio < this == bad state. mcap ratio >= this == good state.',
            value=0.9)
        slippage_mult_good = st.number_input(f'During a good state, mcap ratio < {state_mcap_ratio}, we apply a lower multiplier', value=3)
        slippage_mult_bad  = st.number_input(f'During a bad state, mcap ratio >= {state_mcap_ratio}, we apply a higher multiplier', value=10)

        locktime_offshore = st.number_input('Offshore lock time (days)', value=21, min_value=0, step=1)
        locktime_onshore  = st.number_input('Onshore lock time (days)',  value=21, min_value=0, step=1)
        conversion_fee_offshore = st.number_input('Offshore conversion fee (%)', value=1.5, min_value=0.0, step=0.1)
        conversion_fee_onshore  = st.number_input('Onshore conversion fee (%)',  value=1.5, min_value=0.0, step=0.1)

st.markdown('---')

shore_type   = st.radio("Shore Type", ["Onshore", "Offshore"])
xhv_price    = st.number_input("XHV Price", min_value=0.00001, value=0.5, step=0.10)
xhv_qty      = st.number_input("Amount of unlocked XHV in vault", min_value=0.0, step=10000.0)
xusd_qty     = st.number_input("Amount of unlocked xUSD in vault", min_value=0.0, step=10000.0)
xhv_supply   = st.number_input("Number of XHV in circulation", min_value=xhv_qty, value=2.8*10E6, max_value=10E12, step=10000.0)
xassets_mcap = st.number_input("Market cap of all assets (in USD)", min_value=0.01, value=1.6*10E6, max_value=10E12, step=10000.0)

# Calculations
xhv_mcap     = xhv_price * xhv_supply
mcap_ratio   = xassets_mcap / xhv_mcap
is_healthy   = mcap_ratio < state_mcap_ratio
spread_ratio = 1 - mcap_ratio

# page 10 of PDF v4
mcap_vbs = math.exp((mcap_ratio + math.sqrt(mcap_ratio)) * 2) - 0.5 if is_healthy else \
           math.sqrt(mcap_ratio) * mcap_ratio_mult

# TODO: make spread_vbs work
spread_vbs = "FIX"#math.exp(1 + math.sqrt(spread_ratio)) + mcap_vbs + 1.5

# TODO: mcap_ratio_increase
slippage_mult = slippage_mult_good if is_healthy else slippage_mult_bad
# slippage_vbs = math.sqrt(mcap_ratio_increase) * slippage_mult

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

# TODO: send `sim` to functions
# TODO: update sim with returned values

# sim[f"Max {shore_type} xUSD"] = "Heyyoo"
# sim[f"Max {shore_type} XHV"] = "Heyyoo"

# if shore_type == "Onshore":
#     sim["Max Onshore xUSD"] = "TODO"
#     sim["Max Onshore XHV"] = "TODO"

# button to add simulation
if st.button(label="Add simulation to table"):
    st.session_state['simulation_list'].append(sim)

st.table(st.session_state['simulation_list'])
