import math
import streamlit as st

def shore(
    shore_type,
    xhv_price,
    xhv_qty,
    xusd_qty,
    xhv_supply,
    xassets_mcap,

    static_parameters,#=st.session_state['static_parameters'],
):
    
    # Universal Calculations
    xhv_mcap = xhv_price * xhv_supply
    assert(xhv_mcap > 0)
    block_cap    = math.sqrt(xhv_mcap * static_parameters['block_cap_mult']) # TODO: confirm this is the same for all shoring
    mcap_ratio   = abs(xassets_mcap / xhv_mcap) # abs for sanity
    is_healthy   = mcap_ratio < static_parameters['state_mcap_ratio']
    spread_ratio = max(1 - mcap_ratio, 0)

    # page 10 of PDF v4
    mcap_vbs = math.exp((mcap_ratio + math.sqrt(mcap_ratio)) * 2) - 0.5 if is_healthy else \
               math.sqrt(mcap_ratio) * static_parameters['mcap_ratio_mult']

    spread_vbs = math.exp(1 + math.sqrt(spread_ratio)) + mcap_vbs + 1.5

    # TODOing: mcap_ratio_increase
    # LOGIC SPLITS HERE
    slippage_mult = static_parameters['slippage_mult_good'] if is_healthy else \
                    static_parameters['slippage_mult_bad']
    if   shore_type == "Onshore":
        pass
    elif shore_type == "Offshore":
        # spec_off = specific_offshore(
        #     xhv_price,
        #     xhv_qty,
        #     xusd_qty,
        #     xhv_supply,
        #     xassets_mcap,

        #     xhv_mcap,
        #     # block_cap,
        #     slippage_mult,
        #     is_healthy,
        # )
        # max_off = max_offshore(
        #     xhv_price,
        #     xhv_qty,
        #     xusd_qty,
        #     xhv_supply,
        #     xassets_mcap,

        #     xhv_mcap,
        #     # block_cap,
        #     slippage_mult,
        #     is_healthy,
        # )
        # return {
        #     "specific_offshore": spec_off,
        #     "max_offshore": max_off
        #     }
        pass

    # TODO LOGIC SPLITS HERE
    new_mcap_ratio = ((xhv_qty * xhv_price) + xassets_mcap) / ((xhv_supply - xhv_qty) * xhv_price)
    # mcap_ratio_increase = (new_mcap_ratio - mcap_ratio) / mcap_ratio
    mcap_ratio_increase = (new_mcap_ratio / mcap_ratio) - 1
    slippage_vbs = math.sqrt(mcap_ratio_increase) * slippage_mult

    # total_vbs = 

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
        "XHV Price": xhv_price,
        "XHV Mcap": xhv_mcap,
        "xAssets Mcap": xassets_mcap,
        "Mcap Ratio": round(mcap_ratio, 4),
        "Spread Ratio": round(spread_ratio, 4),
        "Mcap VBS": round(mcap_vbs, 4),
        "Spread VBS": round(spread_vbs, 4),
        "Slippage VBS": round(slippage_vbs, 4), # TODO: fix!
        "Total VBS": "TODO",
        "Max Offshore xUSD": "TODO",
        "Max Offshore XHV": "TODO",
        "Max Onshore xUSD": "TODO",
        "Max Onshore XHV": "TODO",
        'Collateral Needed (XHV)': "TODO",
        'Error Message': "TODO",
        # f"Max {shore_type} xUSD": "heyyoo",
        # f"Max {shore_type} XHV": "heyyoo",
        "Elapsed days": "TODO",#(len(st.session_state['simulation_list']) + 1) * 21,
        }
    # sim = {
    #     "Shore Type": shore_type,
    #     "XHV (vault)": xhv_qty,
    #     "xUSD (vault)": xusd_qty,
    #     "XHV Supply": xhv_supply,
    #     "XHV Price ($)": xhv_price,
    #     "XHV Mcap ($)": xhv_mcap,
    #     "xAssets Mcap ($)": xassets_mcap,
    #     "Mcap Ratio": mcap_ratio,
    #     "Spread Ratio": spread_ratio,
    #     "Mcap VBS": mcap_vbs,
    #     "Spread VBS": spread_vbs,
    #     "Slippage VBS": "TODO",
    #     "Total VBS": "TODO",
    #     "Max Offshore xUSD": "TODO",
    #     "Max Offshore XHV": "TODO",
    #     "Max Onshore xUSD": "TODO",
    #     "Max Onshore XHV": "TODO",
    #     # f"Max {shore_type} xUSD": "heyyoo",
    #     # f"Max {shore_type} XHV": "heyyoo",
    #     "Elapsed days": "TODO",#(len(st.session_state['simulation_list']) + 1) * 21,
    #     }
    return sim

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
    and it will calculate the required collateral.'''
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



def max_offshore(
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

if __name__ == "__main__":
    import pandas as pd

    static_parameters = dict(
        min_vbs = 1,
        min_shore_amount = 1,
        block_cap_mult   = 2500,
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

    def test_row(row):
        return shore( # TODO: <--------------------------------- test row
            shore_type=row['Shore Type'],
            xhv_price=row['XHV Price'],#.astype(float),
            xhv_qty=row['XHV (vault)'],#.astype(float),
            xusd_qty=row['xUSD (vault)'],#.astype(float),
            xhv_supply=row['XHV Supply'],#.astype(float),
            xassets_mcap=row['xAssets Mcap'],#.astype(float),

            static_parameters=static_parameters,
        )

    def test_df(df):
        # return df.apply(lambda x: [*test_row(x)], axis=1)
        # return df.transform(test_row, axis=1)
        return [test_row(row) for index, row in df.iterrows()]

    def run_test(test_file, verbose=False, show_all=False):
        df = pd.read_csv(test_file, sep='\t')
        df['XHV Mcap'] = df['XHV Mcap'].astype(int)
        # print(df.head())
        
        results_df = pd.DataFrame(test_df(df))
        results_df['XHV Mcap'] = results_df['XHV Mcap'].astype(int)
        # print(results_df.head())

        # print(df.equals(results_df))
        same_df = df == results_df[df.columns]
        diff_df = df != results_df[df.columns]
        # correct_cols = [ col == True for col in diff_df.all() ]
        # print(correct_cols)

        if verbose:
            if show_all:
                print(same_df)
                print(df)
                print(results_df)
            elif not same_df.all().all():
                # print(diff_df)
                print(df[diff_df].dropna(axis=1, how='all'))
                print(results_df[diff_df].dropna(axis=1, how='all'))

            print("Column: Passed")
            print(same_df.all())
        else:
            print("Passed" if same_df.all().all() else "Failed")
        
    def run_tests(files, show_all=False):
        for test_file in files:
            print(test_file)
            run_test(test_file) # TODO add verbose and stuff

    run_tests(['tests/Simulation_1.csv', 'tests/Simulation_2.csv', 'tests/Simulation_3.csv'], False)