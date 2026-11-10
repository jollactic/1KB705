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


def compare_designs(resistance=.0006, price=.10, years=10, hours=4000):
    """Synthetic same-service comparison: recuperator followed by electric trim heat.

    Target 1 kg/s water at 55°C. Ideal trim heater efficiency 1; no export credit
    for excess heat. Installed exchanger cost €4000 + €700 per m². No hydraulic,
    heater-capital, maintenance, discounting or cleaning cost. Values are teaching inputs.
    """
    if min(resistance,price,years,hours) < 0:
        raise ValueError('Resistance, price, horizon and hours must be nonnegative.')
    U = 1/(1/650+resistance)
    rows = []
    target = 4180*40
    # Preserve exact base-design areas so rounding does not create a false target failure.
    clean_area = target/(650*lmtd(30,85-target/4560-15))
    for area in [clean_area,clean_area*(1+650*.0006),14.0]:
        hot,cold,recovery = outlets(U*area,4560,4180,85,15)
        trim = max(0.,target-recovery)
        installed = 4000+700*area
        annual_kwh = trim/1000*hours
        rows.append(dict(area=area,hot=hot,cold=cold,recovery_kw=recovery/1000,
                         trim_kw=trim/1000,annual_kwh=annual_kwh,
                         installed=installed,total=installed+annual_kwh*price*years))
    return rows
