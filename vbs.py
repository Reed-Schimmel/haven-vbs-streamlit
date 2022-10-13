import math
import numpy as np
import pandas as pd
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



def specific_onshore( # TODOing: this boi <---------------------------------------
    xhv_vault,
    xhv_to_offshore,
    xusd_vault,
    xusd_to_onshore,
    xhv_price,
    xhv_supply,
    xassets_mcap,

    static_parameters,#=st.session_state['static_parameters'],
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

    # # Universal Calculations
    xhv_mcap = xhv_price * xhv_supply
    assert(xhv_mcap > 0)
    # block_cap    = math.sqrt(xhv_mcap * static_parameters['block_cap_mult']) # TODO: confirm this is the same for all shoring
    mcap_ratio   = abs(xassets_mcap / xhv_mcap) # abs for sanity
    is_healthy   = mcap_ratio < static_parameters['state_mcap_ratio'] # TODO: problem here?
    spread_ratio = max(1 - mcap_ratio, 0)

    # # page 10 of PDF v4
    # TODO: problem here?
    mcap_vbs = math.exp((mcap_ratio + math.sqrt(mcap_ratio)) * 2) - 0.5 if is_healthy else \
               math.sqrt(mcap_ratio) * static_parameters['mcap_ratio_mult']

    # spread_vbs = math.exp(1 + math.sqrt(spread_ratio)) + mcap_vbs + 1.5

    # # TODOing: mcap_ratio_increase
    # # LOGIC SPLITS HERE
    # slippage_mult = static_parameters['slippage_mult_good'] if is_healthy else \
    #                 static_parameters['slippage_mult_bad']


    return {
        'Shore Type': 'Onshore Specific',
        'XHV (vault)': xhv_vault,
        'XHV to offshore': xhv_to_offshore,
        'xUSD (vault)': xusd_vault,
        'xUSD to onshore': xusd_to_onshore,
        'XHV Supply': xhv_supply,
        'XHV Price': xhv_price,
        'XHV Mcap': xhv_mcap,
        'xAssets Mcap': xassets_mcap,
        'Mcap Ratio': mcap_ratio,
        'Spread Ratio': spread_ratio,
        'Mcap VBS': mcap_vbs, # TODO: problem here?
        'Spread VBS': -1,
        'Slippage VBS': -1,
        'Total VBS': -1,
        'Max Offshore XHV': -1,
        'Max Onshore xUSD': -1,
        'Collateral Needed (XHV)': -1,
        'Error Message': 'TODO',
    }

def max_onshore():
    pass







### -------- TESTS -----------
if __name__ == "__main__":
    # import pandas as pd
    # pd.set_option('precision', 4)

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

    # round_to(dfs, decimals=)

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

    def test_df(df, test_func=test_row):
        # return df.apply(lambda x: [*test_row(x)], axis=1)
        # return df.transform(test_row, axis=1)
        return [test_func(row) for index, row in df.iterrows()]

    def compare_df(ref, test, name):
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.compare.html

        # float_cols = ref.columns[ref.dtypes == float].to_list()
        # for col in float_cols:
        #     test[col] = test[col] - ref[col]

        print(ref.compare(
            other=test,
            result_names=(name, 'results_df'),
            )
        )

    def run_test(test_file, verbose=False, show_all=False):
        df = pd.read_csv(test_file, sep='\t')
        df['XHV Mcap'] = df['XHV Mcap'].astype(int)
        # print(df.head())
        
        results_df = pd.DataFrame(test_df(df))
        results_df['XHV Mcap'] = results_df['XHV Mcap'].astype(int)
        # print(results_df.head())

        compare_df(df, results_df[df.columns], test_file)
        return

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


    def fix_prec(df, cols, decimals=3):
        mult = (10 ** decimals)
        for col in cols:
            df[col] = (df[col] * mult).astype(int).astype(float) / mult

        return df

    def test_spec_onshore(test_file): # TODOing: this boi <---------------------------------------
        # cols = ['Spread Ratio', 'Mcap Ratio']
        
        df = pd.read_csv(test_file, sep='\t')
        # df['XHV Mcap'] = df['XHV Mcap'].astype(int)
        # df = fix_prec(df, cols)

        

        # df['Spread Ratio'] = np.round(df['Spread Ratio'], decimals=4)


        def test_spec_row(row):
            return specific_onshore(
                xhv_vault=row['XHV (vault)'],
                xhv_to_offshore=row['XHV to offshore'],
                xusd_vault=row['xUSD (vault)'],
                xusd_to_onshore=row['xUSD to onshore'],
                xhv_price=row['XHV Price'],
                xhv_supply=row['XHV Supply'],
                xassets_mcap=row['xAssets Mcap'],

                static_parameters=static_parameters,
            )
        results_df = pd.DataFrame(test_df(df, test_spec_row))
        results_df = results_df.astype(df.dtypes.to_dict())
        # results_df['XHV Mcap'] = results_df['XHV Mcap'].astype(int)


        # df = fix_prec(df, cols)
        # results_df = fix_prec(results_df, cols)

        # results_df['Spread Ratio'] = (results_df['Spread Ratio'] * 10000).astype(int).astype(float) / 10000
        # results_df['Spread Ratio'] = np.round(results_df['Spread Ratio'], decimals=4) 
        # results_df['Spread Ratio'] = np.floor(results_df['Spread Ratio'])

        compare_df(df, results_df, 'truth')
        # same_df = df == results_df[df.columns]
        # ---------------------------------------------------------
        float_cols = df.columns[df.dtypes == float]#.to_list()
        # diff_df = (df[float_cols] - results_df[float_cols]).abs()
        diff_df = np.round((df[float_cols] - results_df[float_cols]).abs(), decimals=3)

        print(diff_df)#['Spread Ratio'])

        print((diff_df == 0.0).all())

        # print((float_cols))
        print("Column: Passed")

        # print(df[float_cols] - results_df[float_cols])

        # for col in float_cols:
        #     print(col, all(np.allclose(df[col], results_df[col], rtol=0.01)))
        # ---------------------------------------------------------

        # https://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.isclose.html

        # print("Column: Passed")
        # print(same_df.all())

    # run_tests(['tests/Simulation_1.csv', 'tests/Simulation_2.csv', 'tests/Simulation_3.csv'], False)
    # run_test('tests/Simulation_1.csv')
    test_spec_onshore('tests/Specific_Onshores.csv')