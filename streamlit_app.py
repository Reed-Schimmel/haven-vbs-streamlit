import pandas as pd
import streamlit as st

from vault_backed_shoring.vbs import shore


APP_VERSION = "0.0.4" # TODO: grab this from setup.py or whatever https://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
PROPOSAL_VERSION = 4
# TESTING = True

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

# State Initialization
if 'simulation_list' not in st.session_state:
    st.session_state['simulation_list'] = []
if 'static_parameters' not in st.session_state:
    # st.session_state['static_parameters'] = {}
    st.session_state['static_parameters'] = dict(
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
    )

# with st.sidebar:
#     show_tests = st.checkbox("Show tests", False)
    # with st.expander("Static Parameters", expanded=False):
    #     st.caption('The default values are set to the latest official proposal. Adjusting these is only for hypothetical VBS rules. These changes must be made before the first simulation.')
    #     st.session_state['static_parameters'] = dict(
    #         min_vbs = st.number_input('Minimum VBS', value=1),
    #         min_shore_amount = st.number_input('Minimum amount of XHV that can be on/offshored', value=1),
    #         block_cap_mult   = st.number_input('Multiplier which calculates the amount one can on/offshore inside a single block', value=3000),
    #         mcap_ratio_mult  = st.number_input('Multiplier for working out the mcap VBS', value=40),
            
    #         # For changing the condition for "good" and "bad" protocol state
    #         state_mcap_ratio = st.number_input(
    #             label='Protocol state threshold',
    #             help='mcap ratio < this == bad state. mcap ratio >= this == good state.',
    #             value=0.9),
    #         slippage_mult_good = st.number_input('During a good state, mcap ratio < "Protocol state threshold", we apply a lower multiplier', value=3),
    #         slippage_mult_bad  = st.number_input('During a bad state, mcap ratio >= "Protocol state threshold", we apply a higher multiplier', value=10),

    #         locktime_offshore = st.number_input('Offshore lock time (days)', value=21, min_value=0, step=1),
    #         locktime_onshore  = st.number_input('Onshore lock time (days)',  value=21, min_value=0, step=1),
    #         conversion_fee_offshore = st.number_input('Offshore conversion fee (%)', value=1.5, min_value=0.0, step=0.1),
    #         conversion_fee_onshore  = st.number_input('Onshore conversion fee (%)',  value=1.5, min_value=0.0, step=0.1),
    #     )

st.title("VBS Simulator")
st.caption(f"Proposal Version {PROPOSAL_VERSION} | Simulator Version {APP_VERSION}")
st.markdown('---')

# Simulation inputs
shore_type   = st.radio("Shore Type", ["Onshore", "Offshore"])
xhv_price    = st.number_input("XHV Price", min_value=0.00001, value=0.5, step=0.10)
xhv_vault    = st.number_input("Amount of unlocked XHV in vault", min_value=0.0, step=10000.0)
xusd_vault   = st.number_input("Amount of unlocked xUSD in vault", min_value=0.0, step=10000.0)
xhv_supply   = st.number_input("Number of XHV in circulation", min_value=xhv_vault, value=2.8*10E6, max_value=10E12, step=10000.0)
xassets_mcap = st.number_input("Market cap of all assets (in USD)", min_value=0.01, value=1.6*10E6, max_value=10E12, step=10000.0)

# button to add simulation
if st.button(label="Add simulation to table"):
    sim = shore(
        shore_type,
        xhv_price,
        xhv_vault,
        xusd_vault,
        xhv_supply,
        xassets_mcap,
        static_parameters=st.session_state['static_parameters'],
    )
    st.session_state['simulation_list'].append(sim)

if st.session_state['simulation_list'] != []:
    # columns = st.session_state['simulation_list'][0].keys()
    # show_cols = st.multiselect("Show Columns", columns, default=columns)
    # st.write(show_cols)

    # sim_list = [dict(filter(lambda x: x in show_cols, sim)) for sim in st.session_state['simulation_list']]
    # st.write(sim_list)
    # st.table(sim_list)

    st.table(st.session_state['simulation_list'])

    if st.button(label="Reset"):
        st.session_state['simulation_list'] = []
        st.experimental_rerun()