def specific_offshore(
    offshore_qty,

    min_shore_amount,
    block_cap_mult,
    mcap_ratio_mult,
    slippage_mult_good,
    slippage_mult_bad,
    
    
    ):
    '''The “specific” functions are intended for when someone enters an amount in the vault,
    and it will calculate the required collateral.'''
    assert(offshore_qty >= min_shore_amount)

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