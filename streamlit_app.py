import pandas as pd
import streamlit as st

st.title("VBS Playground")

with st.expander("Static Parameters"):
    min_vbs = st.number_input('Minimum VBS', value=1)
    min_shore_amount = st.number_input('Minimum amount of XHV that can be on/offshored', value=1)
    block_cap_mult = st.number_input('Multiplier which calculates the amount one can on/offshore inside a single block', value=2500)
    mcap_ratio_mult = st.number_input('Multiplier for working out the mcap VBS', value=40)
    slippage_mult_good = st.number_input('During a good state, mcap ratio < 0.1, we apply a lower multiplier', value=3)
    slippage_mult_bad = st.number_input('During a bad state, mcap ratio >= 0.1, we apply a higher multiplier', value=10)
st.markdown('---')
shore_type = st.radio("Shore Type", ["Onshore", "Offshore"])
xhv_price = st.number_input("XHV Price", min_value=0.00001, value=0.5)
xhv_qty = st.number_input("Amount of unlocked XHV in vault", min_value=0.0)#, value=100, step=1000)
xusd_qty = st.number_input("Amount of unlocked xUSD in vault", min_value=0.0)#, value=18000000, step=10000)
xhv_supply = st.number_input("Number of XHV in circulation", min_value=xhv_qty, value=28*10E6, max_value=10E12)#, step=10000)
xassets_mcap = st.number_input("Market cap of all assets (in USD)", min_value=0.01, value=16*10E6, max_value=10E12)#, step=10000)
# st.write(28*10E6)