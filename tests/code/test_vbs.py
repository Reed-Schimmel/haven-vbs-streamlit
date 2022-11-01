import math
import beavis
import pandas as pd
import numpy as np

from vault_backed_shoring.vbs import max_onshore, specific_onshore

static_parameters = dict( # TODO: move to config
    min_vbs = 1,
    min_shore_amount = 1, # min onshore amount
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

# # round_to(dfs, decimals=)

# def test_row(row):
#     return shore(
#         shore_type=row['Shore Type'],
#         xhv_price=row['XHV Price'],#.astype(float),
#         xhv_qty=row['XHV (vault)'],#.astype(float),
#         xusd_qty=row['xUSD (vault)'],#.astype(float),
#         xhv_supply=row['XHV Supply'],#.astype(float),
#         xassets_mcap=row['xAssets Mcap'],#.astype(float),

#         static_parameters=static_parameters,
#     )

# def test_df(df, test_func):
#     # return df.apply(lambda x: [*test_row(x)], axis=1)
#     # return df.transform(test_row, axis=1)
#     return [test_func(row) for index, row in df.iterrows()]

# def compare_df(ref, test, name):
#     # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.compare.html

#     # float_cols = ref.columns[ref.dtypes == float].to_list()
#     # for col in float_cols:
#     #     test[col] = test[col] - ref[col]

#     print(ref.compare(
#         other=test,
#         result_names=(name, 'results_df'),
#         )
#     )

# def run_test(test_file, verbose=False, show_all=False):
#     df = pd.read_csv(test_file, sep='\t')
#     df['XHV Mcap'] = df['XHV Mcap'].astype(int)
#     # print(df.head())
    
#     results_df = pd.DataFrame(test_df(df))
#     results_df['XHV Mcap'] = results_df['XHV Mcap'].astype(int)
#     # print(results_df.head())

#     compare_df(df, results_df[df.columns], test_file)
#     return

#     # print(df.equals(results_df))
#     same_df = df == results_df[df.columns]
#     diff_df = df != results_df[df.columns]
#     # correct_cols = [ col == True for col in diff_df.all() ]
#     # print(correct_cols)

#     if verbose:
#         if show_all:
#             print(same_df)
#             print(df)
#             print(results_df)
#         elif not same_df.all().all():
#             # print(diff_df)
#             print(df[diff_df].dropna(axis=1, how='all'))
#             print(results_df[diff_df].dropna(axis=1, how='all'))

#         print("Column: Passed")
#         print(same_df.all())
#     else:
#         print("Passed" if same_df.all().all() else "Failed")
    
# def run_tests(files, show_all=False):
#     for test_file in files:
#         print(test_file)
#         run_test(test_file) # TODO add verbose and stuff


# def fix_prec(df, cols, decimals=3):
#     mult = (10 ** decimals)
#     for col in cols:
#         df[col] = (df[col] * mult).astype(int).astype(float) / mult

#     return df

# def test_spec_onshore(test_file):
#     df = pd.read_csv(test_file, sep='\t')#.iloc[:12]#.reset_index()

#     def test_spec_row(row):
#         return specific_onshore(
#             xhv_vault=row['XHV (vault)'],
#             xhv_to_offshore=row['XHV to offshore'],
#             xusd_vault=row['xUSD (vault)'],
#             xusd_to_onshore=row['xUSD to onshore'],
#             xhv_price=row['XHV Price'],
#             xhv_supply=row['XHV Supply'],
#             xassets_mcap=row['xAssets Mcap'],

#             static_parameters=static_parameters,
#         )
#     results_df = pd.DataFrame(test_df(df, test_spec_row))
#     results_df = results_df.astype(df.dtypes.to_dict())

#     # compare_df(df, results_df, 'truth')

#     drop_test_cols = [
#         # 'Max Offshore XHV','Max Onshore xUSD',
#         # 'Error Message', # missing ~5%
#         # 'Mcap Ratio',
#         # 'Spread Ratio',
#         # 'Mcap VBS',
#         # 'Spread VBS',
#         # 'Slippage VBS',
#         # 'Total VBS', # missing ~5%
#         # 'Collateral Needed (XHV)', # missing ~5%
#     ]

#     # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.testing.assert_frame_equal.html
#     return pd.testing.assert_frame_equal(
#         left=df.drop(drop_test_cols, axis=1),
#         right=results_df.drop(drop_test_cols, axis=1),
#         check_dtype=False,
#         check_exact=False,
#         # rtol=1e-1,
#         atol=0.1,#1e-3,
#     )
    


#     # compare_df(df, results_df, 'truth')
#     # same_df = df == results_df[df.columns]
#     # ---------------------------------------------------------
#     float_cols = df.columns[df.dtypes == float]#.to_list()
#     # diff_df = (df[float_cols] - results_df[float_cols]).abs()
#     diff_df = np.round((df[float_cols] - results_df[float_cols]).abs(), decimals=2) # TODO: maybe should be 3?

#     # print(diff_df)#['Spread Ratio'])
#     # print("Column: Passed")
#     passed = (diff_df == 0.0).all()
#     # print(passed)
#     # passed_cols = passed[passed].to_dict().keys()
#     # print(passed)


#     # print("Failed")
#     failed = passed[passed == False] | True #(diff_df != 0.0).any()
#     # print(failed)
#     failed_cols = failed[failed].to_dict().keys()
#     # print(failed_cols)
#     # print(diff_df[failed_cols].sum())
#     # print(df[failed_cols].sum())
#     print(df[failed_cols].sum().compare(diff_df[failed_cols].sum(), result_names=('df.sum()', 'diff_df.sum()')))

#     # print(passed_cols[passed_cols])
#     # print(passed_cols[passed_cols].to_dict().keys())
#     # print(df[passed_cols[passed_cols].to_dict().keys()])


#     # failed_cols = passed_cols[passed_cols == False] | True#(diff_df != 0.0).any()
#     # print(df[failed_cols[failed_cols == True]])
#     # print(failed_cols[failed_cols == True])
#     # # print(df.columns)
#     # print(passed_cols[passed_cols == False] | True)
#     # # print(df[(passed_cols[passed_cols == False] | True)])
#     # compare_df(df[failed_cols], results_df[failed_cols], 'truth')
    

#     # print((float_cols))

#     # print(df[float_cols] - results_df[float_cols])

#     # for col in float_cols:
#     #     print(col, all(np.allclose(df[col], results_df[col], rtol=0.01)))
#     # ---------------------------------------------------------

#     # https://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.isclose.html

#     # print("Column: Passed")
#     # print(same_df.all())

# # run_tests(['tests/Simulation_1.csv', 'tests/Simulation_2.csv', 'tests/Simulation_3.csv'], False)
# # run_test('tests/Simulation_1.csv')
# # print('test_spec_onshore')
# # test_spec_onshore('tests/Specific_Onshores.csv')


# def test_max_onshore(test_file):
#     df = pd.read_csv(test_file, sep='\t')#.iloc[:12]#.reset_index()

#     def test_spec_row(row): # TODO: me to max
#         return max_onshore(
#             xhv_vault=row['XHV (vault)'],
#             # xhv_to_offshore=row['XHV to offshore'],
#             xusd_vault=row['xUSD (vault)'],
#             # xusd_to_onshore=row['xUSD to onshore'],
#             xhv_price=row['XHV Price'],
#             xhv_supply=row['XHV Supply'],
#             xassets_mcap=row['xAssets Mcap'],

#             static_parameters=static_parameters,
#         )
#     results_df = pd.DataFrame(test_df(df, test_spec_row))[df.columns] # TODO: maybe remove df.columns after fixes
#     results_df = results_df.astype(df.dtypes.to_dict())

#     # compare_df(df, results_df, 'truth')

#     drop_test_cols = [
#         # 'Max Offshore XHV','Max Onshore xUSD',
#         # 'Error Message', # missing ~5%
#         # 'Mcap Ratio',
#         # 'Spread Ratio',
#         # 'Mcap VBS',
#         # 'Spread VBS',
#         # 'Slippage VBS',
#         # 'Total VBS', # missing ~5%
#         # 'Collateral Needed (XHV)', # missing ~5%
#     ]

#     # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.testing.assert_frame_equal.html
#     return pd.testing.assert_frame_equal(
#         left=df.drop(drop_test_cols, axis=1),
#         right=results_df.drop(drop_test_cols, axis=1),
#         check_dtype=False,
#         check_exact=False,
#         # rtol=1e-1,
#         atol=0.1,#1e-3,
#     )

# print('test_max_onshore')
# test_max_onshore('tests/Simulation_1.csv')
def test_max_onshore():
    # print(max_onshore)
    # print(pd.read_csv('tests/Simulation_1.csv', sep='\t'))#.iloc[:12]#.reset_index()

    assert True


# # Simulation inputs
# shore_type   = st.radio("Shore Type", ["Onshore", "Offshore"])
# xhv_price    = st.number_input("XHV Price", min_value=0.00001, value=0.5, step=0.10)
# xhv_qty      = st.number_input("Amount of unlocked XHV in vault", min_value=0.0, step=10000.0)
# xusd_qty     = st.number_input("Amount of unlocked xUSD in vault", min_value=0.0, step=10000.0)
# xhv_supply   = st.number_input("Number of XHV in circulation", min_value=xhv_qty, value=2.8*10E6, max_value=10E12, step=10000.0)
# xassets_mcap = st.number_input("Market cap of all assets (in USD)", min_value=0.01, value=1.6*10E6, max_value=10E12, step=10000.0)

        # 'Shore Type': 'Onshore Specific',
        # 'XHV (vault)': xhv_vault,
        # 'XHV to offshore': xhv_to_offshore,
        # 'xUSD (vault)': xusd_vault,
        # 'xUSD to onshore': xusd_to_onshore,
        # 'XHV Supply': xhv_supply,
        # 'XHV Price': xhv_price,
        # 'XHV Mcap': xhv_mcap,
        # 'xAssets Mcap': xassets_mcap,
        # 'Mcap Ratio': 0, # line 10 of the csv is wack yo TODO: fix??
        # 'Spread Ratio': 0,
        # 'Mcap VBS': 0, 
        # 'Spread VBS': 0,
        # 'Slippage VBS': 0,
        # 'Total VBS': 0,
        # 'Max Offshore XHV': 0,
        # 'Max Onshore xUSD': 0,
        # 'Collateral Needed (XHV)': 0,
        # 'Error Message': np.nan,

# def base_test(test_file):
#     df = pd.read_csv(test_file, sep='\t')
#     # assert True
#     #             xhv_vault=row['XHV (vault)'],
#     #             # xhv_to_offshore=row['XHV to offshore'],
#     #             xusd_vault=row['xUSD (vault)'],
#     #             # xusd_to_onshore=row['xUSD to onshore'],
#     #             xhv_price=row['XHV Price'],
#     #             xhv_supply=row['XHV Supply'],
#     #             xassets_mcap=row['xAssets Mcap'],

def base_spec_onshore_test(df, column, rel_tol=1e-9, abs_tol=0):
    input_cols = ['XHV (vault)', 'XHV to offshore', 'xUSD (vault)', 'xUSD to onshore', 'XHV Price', 'XHV Supply', 'xAssets Mcap']
    test_cols = input_cols + [column]

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
    
    # results_list = [test_spec_row(row) for index, row in df.iterrows()]

    # results_df = pd.DataFrame(results_list)

    # beavis.assert_approx_pd_equality(df[test_cols], results_df[test_cols], abs_tol, check_dtype=False)

    for index, row in df.iterrows():
        truth = row[column]

        result = specific_onshore(
                xhv_vault=row['XHV (vault)'],
                xhv_to_offshore=row['XHV to offshore'],
                xusd_vault=row['xUSD (vault)'],
                xusd_to_onshore=row['xUSD to onshore'],
                xhv_price=row['XHV Price'],
                xhv_supply=row['XHV Supply'],
                xassets_mcap=row['xAssets Mcap'],

                static_parameters=static_parameters,
            )

        beavis.assert_approx_pd_equality(
            df.iloc[index:index+1][test_cols],
            pd.DataFrame([result])[test_cols],
            abs_tol, check_dtype=False, check_index=False)

        # assert np.round(truth, decimals=round_to) == np.round(result[column], decimals=round_to)
        # assert math.isclose(truth, result[column], rel_tol=rel_tol, abs_tol=abs_tol)

def test_spec_onshore_xhv_mcap():
    round_to = 4
    test_file = 'tests/Specific_Onshores.csv'
    df = pd.read_csv(test_file, sep='\t')
    base_spec_onshore_test(df, 'XHV Mcap', abs_tol=0.0001)

def test_spec_onshore_mcap_ratio():
    round_to = 4
    test_file = 'tests/Specific_Onshores.csv'
    df = pd.read_csv(test_file, sep='\t')
    base_spec_onshore_test(df, 'Mcap Ratio', abs_tol=0.005)



# https://github.com/MrPowers/beavis/blob/main/beavis/testing.py#L70


# Pytests with DataFrames
# https://levelup.gitconnected.com/advanced-pytest-techniques-i-learned-while-contributing-to-pandas-7ba1465b65eb
# https://towardsdatascience.com/getting-started-unit-testing-with-pytest-9cba6d366d61