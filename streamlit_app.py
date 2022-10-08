import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="VBS Simulator",
    page_icon="https://raw.githubusercontent.com/haven-protocol-org/brand-assets/master/Branding%20Kit/png/white/rounded.png",
    layout='wide',
    initial_sidebar_state="collapsed",
    menu_items={
    'Get Help': 'https://discord.com/channels/536838513182638090/570818940553527296',
    'Report a bug': "https://github.com/Reed-Schimmel/haven-vbs-streamlit/issues",
    'About': "[Haven Protocol](https://havenprotocol.org/)"#"[GitHub](https://github.com/Reed-Schimmel/haven-vbs-streamlit)"#\n-[Haven Protocol](https://havenprotocol.org/)"
    })

# State Initialization
if 'simulation_list' not in st.session_state:
    st.session_state['simulation_list'] = []


st.title("VBS Simulator")

with st.expander("Static Parameters", expanded=False):
    min_vbs = st.number_input('Minimum VBS', value=1)
    min_shore_amount = st.number_input('Minimum amount of XHV that can be on/offshored', value=1)
    block_cap_mult = st.number_input('Multiplier which calculates the amount one can on/offshore inside a single block', value=2500)
    mcap_ratio_mult = st.number_input('Multiplier for working out the mcap VBS', value=40)
    slippage_mult_good = st.number_input('During a good state, mcap ratio < 0.1, we apply a lower multiplier', value=3)
    slippage_mult_bad = st.number_input('During a bad state, mcap ratio >= 0.1, we apply a higher multiplier', value=10)

st.markdown('---')

shore_type = st.radio("Shore Type", ["Onshore", "Offshore"])
xhv_price = st.number_input("XHV Price", min_value=0.00001, value=0.5)
xhv_qty = st.number_input("Amount of unlocked XHV in vault", min_value=0.0, step=10000.0)
xusd_qty = st.number_input("Amount of unlocked xUSD in vault", min_value=0.0, step=10000.0)
xhv_supply = st.number_input("Number of XHV in circulation", min_value=xhv_qty, value=2.8*10E6, max_value=10E12, step=10000.0)
xassets_mcap = st.number_input("Market cap of all assets (in USD)", min_value=0.01, value=1.6*10E6, max_value=10E12, step=10000.0)

# button to add simulation
if st.button(label="Add simulation to table"):
    st.session_state['simulation_list'].append({
        "Shore Type": shore_type,
        "XHV (vault)": xhv_qty,
        "xUSD (vault)": xusd_qty,
        "XHV Supply": xhv_supply,
        "XHV Price": xhv_price,
        "XHV Mcap": xhv_price * xhv_supply,
        "xAssets Mcap": xassets_mcap,
        "Mcap Ratio": "TODO",
        "Spread Ratio": "TODO",
        "Mcap VBS": "TODO",
        "Spread VBS": "TODO",
        "Slippage VBS": "TODO",
        "Total VBS": "TODO",
        "Max Onshore xUSD": "TODO",
        "Max Onshore XHV": "TODO",
        "Elapsed days": "TODO",
        })

st.table(st.session_state['simulation_list'])