import numpy as np
import pandas as pd
import streamlit as st

from vault_backed_shoring.vbs import shore


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

APP_VERSION = "0.3.2" # TODO: grab this from setup.py or whatever https://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
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

# --------------- BODY ---------------
st.title("VBS Simulator")
st.caption(f"Proposal Version {PROPOSAL_VERSION} | Simulator Version {APP_VERSION}")
st.markdown('---')

### Simulation inputs
# Market Conditions
st.markdown('#### Market Conditions')
xhv_price    = st.number_input("XHV Price (USD)", min_value=0.00001, value=0.5, step=0.10)
xhv_supply   = st.number_input("Number of XHV in circulation", min_value=1.0, value=2.8*10E6, max_value=10E12, step=10000.0)
xassets_mcap = st.number_input("Market cap of all assets (USD)", min_value=0.01, value=1.6*10E6, max_value=10E12, step=10000.0)

# Vault Conditions
st.markdown('#### Vault Conditions')
xhv_vault    = st.number_input("Unlocked XHV", min_value=0.0, step=10000.0)
xusd_vault   = st.number_input("Unlocked xUSD", min_value=0.0, step=10000.0)

# Amount to shore
st.markdown('#### Shoring Conditions')
shore_type   = st.radio("Shore Type", ["Onshore", "Offshore"])
shore_unit = "XHV" if shore_type == "Offshore" else "xUSD"
is_max = st.checkbox(f"{shore_type} maximum {shore_unit}", value=True, disabled=False)
if not is_max:
    max_qty = xhv_vault if shore_type == "Offshore" else xusd_vault
    amount_to_shore = st.number_input(
        label=f"Amount of {shore_unit} to {shore_type.lower()}", 
        min_value=0.0, max_value=max_qty,
        step=float(max(int(0.1 * max_qty), 1)),
    )

col1a, col2a = st.columns([1,3], gap="small")
# button to add simulation
with col1a:
    if st.button(label="Add simulation to table"):
        sim = shore(
            shore_type=shore_type,
            amount_to_shore="max" if is_max else amount_to_shore,
            xhv_price=xhv_price,
            xhv_vault=xhv_vault,
            xusd_vault=xusd_vault,
            xhv_supply=xhv_supply,
            xassets_mcap=xassets_mcap,
            static_parameters=st.session_state['static_parameters'],
        )
        sim[f"{shore_unit} to {shore_type.lower()}"] = np.nan if is_max else amount_to_shore

        st.session_state['simulation_list'].append(sim)

if st.session_state['simulation_list'] != []:
    # st.table(st.session_state['simulation_list'])
    df = pd.DataFrame(st.session_state['simulation_list'])
    df_cols = df.columns.to_list()
    with col2a:
        with st.expander("Enabled Columns"):
            selected_cols = st.multiselect(label="Columns", options=df_cols, default=df_cols, label_visibility="collapsed")
    st.dataframe(df[selected_cols])

    col1b, col2b, col3b = st.columns([3, 4, 1], gap="small")
    with col1b:
        # https://docs.streamlit.io/library/api-reference/widgets/st.download_button
        st.download_button(
            label="Download table as CSV",
            data=convert_df(df),
            file_name='VBS_simulations.csv',
            mime='text/csv',
        )
    with col3b:
        if st.button(label="Reset"):
            st.session_state['simulation_list'] = []
            st.experimental_rerun()


### FOOTER
# https://spongebob.fandom.com/wiki/Can_You_Spare_a_Dime%3F#Production
st.markdown('''
---
##### Donations:\n
*VBS Simulator* is developed* and maintained by the volunteer efforts of [Reed Schimmel](https://github.com/Reed-Schimmel).\n
- Haven: hvxyCn1Umq3PuQ7pWzixJnFtZNeDTfy8tQE3DjKLZ8pt8gvcqP9A3UCi6PizS2d19dZkdNMVzsPxhLoYSkLdDQLd8Xqbrrn3PX
- Monero: 87L9AVmqrPATUCJnHrJkPBZGM27qN5BxY7uwDJQ6XSCw4VRtYFY5Lpw2Rt9ZxU5nFiev9hvyP4pbD8RD4EMQh9d9H9LNaUA

\* In collaboration with **Community Manager
Contributor [xKleinroy](https://havenprotocol.org/team/)**, who generously provided pseudocode and quality assurance.
''')