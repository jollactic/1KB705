"""Constant-property, ideal countercurrent heat-exchanger utilities."""
import numpy as np


def lmtd(delta1, delta2):
    """Positive terminal differences in K; continuous at equal differences."""
    if min(delta1, delta2) <= 0:
        raise ValueError('Both terminal temperature differences must be positive.')
    if np.isclose(delta1, delta2, rtol=1e-8):
        return (delta1+delta2)/2
    return (delta1-delta2)/np.log(delta1/delta2)


def countercurrent_effectiveness(ntu, capacity_ratio):
    """epsilon=(1-exp[-NTU(1-Cr)])/(1-Cr*exp[-NTU(1-Cr)]).

    For Cr=1 the limit is NTU/(1+NTU). NTU >= 0 and 0 <= Cr <= 1.
    """
    if ntu < 0 or not 0 <= capacity_ratio <= 1:
        raise ValueError('Require NTU >= 0 and 0 <= Cr <= 1.')
    if np.isclose(capacity_ratio, 1, rtol=0, atol=1e-10):
        return ntu/(1+ntu)
    numerator = -np.expm1(-ntu*(1-capacity_ratio))
    return numerator/(1-capacity_ratio+capacity_ratio*numerator)


def outlets(ua, hot_capacity, cold_capacity, hot_in, cold_in):
    """Return hot outlet, cold outlet (°C or K), duty (W). Capacities in W/K."""
    if ua < 0 or min(hot_capacity, cold_capacity) <= 0 or hot_in < cold_in:
        raise ValueError('Require UA >= 0, positive capacities, and hot_in >= cold_in.')
    cmin, cmax = min(hot_capacity, cold_capacity), max(hot_capacity, cold_capacity)
    eps = countercurrent_effectiveness(ua/cmin, cmin/cmax)
    duty = eps*cmin*(hot_in-cold_in)
    return hot_in-duty/hot_capacity, cold_in+duty/cold_capacity, duty
