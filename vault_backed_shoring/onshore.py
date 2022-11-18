import math
import numpy as np
import pandas as pd
import streamlit as st

from .base import calc_block_cap

ONSHORE_ACC_THRESH = 0.0005

# TODO: add st.cache
# function working out the amount of collateral required for onshores
def specific_onshore(
    xhv_vault,
    xhv_to_offshore,
    xusd_vault,
    xusd_to_onshore,
    xhv_price,
    xhv_supply,
    xassets_mcap,

    static_parameters,#=st.session_state['static_parameters'],
    ignore_errors=False,
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
        Error Message               object: [np.nan | 'incorrect onshore amount' | 'not enough xUSD available to onshore' | 'not enough collateral available']
        dtype: object

    '''
    xhv_mcap = xhv_price * xhv_supply
    amount_to_onshore_xhv = xusd_to_onshore / xhv_price

    results = {
        'Shore Type': 'Onshore Specific',
        'XHV (vault)': xhv_vault,
        'XHV to offshore': xhv_to_offshore,
        'xUSD (vault)': xusd_vault,
        'xUSD to onshore': xusd_to_onshore,
        'XHV Supply': xhv_supply,
        'XHV Price': xhv_price,
        'XHV Mcap': xhv_mcap,
        'xAssets Mcap': xassets_mcap,
        'Mcap Ratio': 0, # line 10 of the csv is wack yo TODO: fix??
        'Spread Ratio': 0,
        'Mcap VBS': 0, 
        'Spread VBS': 0,
        'Slippage VBS': 0,
        'Total VBS': 0,
        'Max Offshore XHV': np.nan,
        'Max Onshore xUSD': np.nan,
        'Collateral Needed (XHV)': 0,
        'Error Message': np.nan,
    }


    if (not ignore_errors) and xusd_to_onshore > xusd_vault:
        results['Error Message'] = 'not enough xUSD available to onshore'
        return results
    if (not ignore_errors) and amount_to_onshore_xhv < static_parameters['min_shore_amount']:
        results['Error Message'] = 'incorrect onshore amount'
        return results
    if (not ignore_errors) and xhv_vault < static_parameters['min_shore_amount']:
        results['Error Message'] = 'not enough collateral available'
        return results

    # assert(xhv_mcap > 0) # TODO: enable? prolly no cuz it crashes exec

    # validation – ensure onshore amount is not greater than block cap
    # block_cap = math.sqrt(xhv_mcap * static_parameters['block_cap_mult']) # TODO: confirm this is the same for all shoring
    # block cap v2
    block_cap = calc_block_cap(xhv_mcap, xhv_supply, static_parameters['block_cap_mult']) # TODO: will this break all tests?
    if (not ignore_errors) and amount_to_onshore_xhv > block_cap:
        # Error code -4, no message
        return results


    mcap_ratio   = (xassets_mcap / xhv_mcap) # cannot be < 0
    spread_ratio = max(1 - mcap_ratio, 0)
    mcap_ratio = max(mcap_ratio, 0)
    is_healthy   = mcap_ratio <= static_parameters['state_mcap_ratio'] # TODO: problem here?

    # # page 10 of PDF v4
    # TODO: problem here?
    # called "currentVBS" in pseudocode
    mcap_vbs = (math.exp( (mcap_ratio + math.sqrt(mcap_ratio)) * 2) - 0.5) if is_healthy else \
               (math.sqrt(mcap_ratio) * static_parameters['mcap_ratio_mult'])

    spread_vbs = math.exp(1 + math.sqrt(spread_ratio)) + mcap_vbs + 1.5
    if spread_vbs > mcap_vbs:
        mcap_vbs = spread_vbs

    # calculate spread ratio increase
    new_spread_ratio = 1 - ( (xassets_mcap - xusd_to_onshore) / ((xhv_supply + amount_to_onshore_xhv) * xhv_price) )
    if spread_ratio == 0:
        #  prevent div by 0
        increase_spread_ratio = new_spread_ratio - 1
    else:
        increase_spread_ratio = (new_spread_ratio / spread_ratio) - 1
    # TODO: THE COMMENT DOESN'T LINE UP WITH THIS LOGIC. WARNING!!!!
    # if the increase is negative, change it to positive due to square root performed on it
    increase_spread_ratio = max(increase_spread_ratio, 0)
    # increase_spread_ratio = abs(increase_spread_ratio)



    # slippage_mult = static_parameters['slippage_mult_good'] if is_healthy else \
    #                 static_parameters['slippage_mult_bad']
    # slippage_vbs = math.sqrt(increase_spread_ratio) * slippage_mult
    
    # TODO: why aren't we asking about the health??? ASK xKleinroy
    slippage_vbs = math.sqrt(increase_spread_ratio) * static_parameters['slippage_mult_good']

    # set min or max VBS if the calculated VBS is out of bounds
    total_vbs = max(mcap_vbs + slippage_vbs, static_parameters['min_vbs'])

    # total amount of unlocked XHV needed for the onshore specified (includes onshore amount)
    total_collateral = amount_to_onshore_xhv * total_vbs
    if (not ignore_errors) and total_collateral > (xhv_vault * total_vbs):
        results['Error Message'] = 'not enough collateral available'
        return results

    # print(err_msg)
    results.update({
        # 'Shore Type': 'Onshore Specific',
        # 'XHV (vault)': xhv_vault,
        # 'XHV to offshore': xhv_to_offshore,
        # 'xUSD (vault)': xusd_vault,
        # 'xUSD to onshore': xusd_to_onshore,
        # 'XHV Supply': xhv_supply,
        # 'XHV Price': xhv_price,
        # 'XHV Mcap': xhv_mcap,
        # 'xAssets Mcap': xassets_mcap,
        'Mcap Ratio': mcap_ratio, # line 10 of the csv is wack yo TODO: fix??
        'Spread Ratio': spread_ratio,
        'Mcap VBS': mcap_vbs, # TODO: problem here?
        'Spread VBS': spread_vbs,
        'Slippage VBS': slippage_vbs,
        'Total VBS': total_vbs,
        # 'Max Offshore XHV': -1,
        # 'Max Onshore xUSD': -1,
        'Collateral Needed (XHV)': total_collateral,
        # 'Error Message': err_msg,
    })
    return results

# function working out the maximum amount of xUSD that can be onshored
def max_onshore(
    xhv_vault, # Unlocked
    # xhv_to_offshore,
    xusd_vault, # Unlocked
    # xusd_to_onshore,
    xhv_price,
    xhv_supply,
    xassets_mcap,

    static_parameters,
    ):
    '''function working out the maximum amount of xUSD that can be onshored.

    This function is harder to calculate for three reasons:
        1. Introduction of Spread Ratio.
        2. Working with two currencies, XHV and xUSD.
        3. When trying to work out the maximum amount of xUSD that we can onshore, we have to consider both,
        the amounts of unlocked xUSD and XHV in the vault and the corresponding VBS.
    
    test_df: TODO: fix this below to match da right stuff
        Shore Type                  object: "Onshore" | "Offshore"
        XHV (vault)                float64
        xUSD (vault)               float64
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
        dtype: object

    '''

    xhv_mcap = xhv_price * xhv_supply

    results = {
        'Shore Type': 'Onshore Max',
        'XHV (vault)': xhv_vault,
        # 'XHV to offshore': xhv_to_offshore,
        'xUSD (vault)': xusd_vault,
        # 'xUSD to onshore': xusd_to_onshore,
        'XHV Supply': xhv_supply,
        'XHV Price': xhv_price,
        'XHV Mcap': xhv_mcap,
        'xAssets Mcap': xassets_mcap,
        'Mcap Ratio': 0,
        'Spread Ratio': 0,
        'Mcap VBS': 0,
        'Spread VBS': 0,
        'Slippage VBS': 0,
        'Total VBS': 0,
        'Max Offshore XHV': 0,
        'Max Onshore xUSD': 0,
        'Max Onshore XHV': 0,
        'Collateral Needed (XHV)': 0,
        'Error Message': np.nan,
    }

    # return results # TODO: confirm tests workin
    if xhv_vault < static_parameters['min_shore_amount']:
        results['Error Message'] = 'not enough unlocked funds to onshore' # -1
        return results
    if xusd_vault / xhv_price < static_parameters['min_shore_amount']:
        results['Error Message'] = 'not enough unlocked funds to onshore' # -1
        return results

    # Call the specific_onshore() function get the amount
    # of collateral needed based on the amount of unlocked xUSD available
    # by passing “true” in the function, it will ignore some error messages in the calling
    # function, which will need to be verified in this function

    xhv_to_offshore = 0
    xusd_to_onshore = xusd_vault
    spec_results = specific_onshore(xhv_vault, xhv_to_offshore, xusd_vault, xusd_to_onshore, xhv_price, xhv_supply, xassets_mcap, static_parameters, ignore_errors=True)
    total_collateral = spec_results['Collateral Needed (XHV)']

    if total_collateral < static_parameters['min_shore_amount']:
        results['Error Message'] = 'incorrect onshore amount' # -2
        return results

    if total_collateral <= xhv_vault:
        # we have enough collateral to onshore all the unlocked xUSD
        # TODO: REALLY confirm this
        results['Collateral Needed (XHV)'] = xusd_vault # TODO: pg 7, confirm that unlockedXUSD should be returned as "Collateral Needed"

    # From this point on, we have to work out the amount of xUSD that can be onshored based
    # on the amount of available unlocked XHV.
    # calculate the VBS in order to get the onshore amount from the unlocked XHV
    # get all other parameters required for calculating the VBS
    # TODO: this makes me think the prev todos something idk
    mcap_ratio   = (xassets_mcap / xhv_mcap) # cannot be < 0
    spread_ratio = max(1 - mcap_ratio, 0)
    mcap_ratio = max(mcap_ratio, 0)
    is_healthy   = mcap_ratio <= static_parameters['state_mcap_ratio'] # TODO: problem here?

    # # page 10 of PDF v4
    # TODO: problem here?
    # called "currentVBS" in pseudocode
    mcap_vbs = (math.exp( (mcap_ratio + math.sqrt(mcap_ratio)) * 2) - 0.5) if is_healthy else \
               (math.sqrt(mcap_ratio) * static_parameters['mcap_ratio_mult'])

    spread_vbs = math.exp(1 + math.sqrt(spread_ratio)) + mcap_vbs + 1.5
    if spread_vbs > mcap_vbs:
        mcap_vbs = spread_vbs

    # calculate the onshore amount using the Max Onshore Collateral defined earlier in the paper
    temp_xhv_to_onshore = xhv_vault / mcap_vbs
    temp_xusd_to_onshore = temp_xhv_to_onshore * xhv_price

    onshore_acc = 1
    onshore_pct = 0 # % value of calculated collateral vs available XHV
    temp_collateral = 0
    collateral_diff = 0 # a % difference between first and calculated collateral
    additional_onshore = 0 # amount to be added to existing shore
    less_onshore = 0 # amount to be subtracted from the existing onshore 

    # create a while loop to run until a condition of 0.0005 (0.05%) accuracy has been met
    while(onshore_acc > ONSHORE_ACC_THRESH):
        # call the specificOnshore() function in order to return the actual collateral
        # needed, from which we can work out the accuracy. We then add or subtract a %
        # to the current onshore amount until the desired accuracy is met.
        temp_results = specific_onshore(
            xhv_vault,
            xhv_to_offshore,
            xusd_vault,
            temp_xusd_to_onshore, # xusd_to_onshore
            xhv_price,
            xhv_supply,
            xassets_mcap,
            static_parameters, ignore_errors=True)
        temp_collateral = temp_results['Collateral Needed (XHV)']
        if temp_collateral > xhv_vault:
            # collateral higher than amount of unlocked XHV, so we use the % difference
            # to subtract from the onshore amount
            onshore_pct = 1 - (xhv_vault / temp_collateral)
            less_onshore = temp_xusd_to_onshore * onshore_pct
            temp_xusd_to_onshore -= less_onshore
        else:
            onshore_acc = 1 - (temp_collateral / xhv_vault)
            if onshore_acc <= ONSHORE_ACC_THRESH:
                break # exit since onshore amount is within accepted acc
            
            # calc additional onshore amount
            additional_onshore = temp_xusd_to_onshore * onshore_acc
            # add additional onshore amount to existing amount
            temp_xusd_to_onshore += additional_onshore
        
    # this is the final max onshore amount
    # If the temp amount is greater than the unlocked xUSD in the vault,
    # set the final amount to the amount unlocked in the vault.
    final_xusd_to_onshore = min(temp_xusd_to_onshore, xusd_vault)
    if (final_xusd_to_onshore / xhv_price) < static_parameters['min_shore_amount']:
        results['Error Message'] = 'incorrect onshore amount' # -2
        return results
    if (final_xusd_to_onshore / xhv_price) < static_parameters['min_shore_amount']:
        results['Error Message'] = 'onshore amount greater than block limit' # -3
        return results

    # final_spec_results = specific_onshore(xhv_vault, xhv_to_offshore, xusd_vault, temp_xusd_to_onshore, xhv_price, xhv_supply, xassets_mcap, static_parameters, ignore_errors=True)
    final_spec_results = specific_onshore(xhv_vault, xhv_to_offshore, xusd_vault, final_xusd_to_onshore, xhv_price, xhv_supply, xassets_mcap, static_parameters, ignore_errors=True)
    total_collateral = final_spec_results['Collateral Needed (XHV)']
    results.update({
        'Max Onshore xUSD': final_xusd_to_onshore,#final_spec_results['Max Onshore xUSD'],#final_xusd_to_onshore,

        # 'Mcap Ratio': mcap_ratio, # line 10 of the csv is wack yo TODO: fix??
        # 'Spread Ratio': spread_ratio,
        # 'Mcap VBS': mcap_vbs, # TODO: problem here?
        # 'Spread VBS': spread_vbs,
        # 'Slippage VBS': slippage_vbs,
        'Total VBS': final_spec_results['Total VBS'], #total_vbs, # TODO: confirm with Roy
        # 'Max Offshore XHV': -1,
        'Collateral Needed (XHV)': total_collateral,
    })
    
    return results
