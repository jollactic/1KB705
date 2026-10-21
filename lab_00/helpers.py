"""Basic nonreacting balances. Units are stated in each function."""
import numpy as np


def mix_streams(flow_a, fraction_a, flow_b, fraction_b=0.):
    """Steady mixing: flows use the same mass/time unit; fractions are kg/kg."""
    if min(flow_a,flow_b)<0 or flow_a+flow_b<=0:
        raise ValueError('Require nonnegative inlet flows and positive total flow.')
    if not 0<=fraction_a<=1 or not 0<=fraction_b<=1:
        raise ValueError('Mass fractions must be between zero and one.')
    total = flow_a+flow_b
    solute = flow_a*fraction_a+flow_b*fraction_b
    return total,solute/total


def evaporate(feed,fraction_in,fraction_product):
    """Steady mass balance only: nonvolatile solute, pure-water vapour, no losses.

    All flows have the same mass/time unit. No evaporation-energy model is implied.
    """
    if feed<=0 or not 0<fraction_in<=fraction_product<=1:
        raise ValueError('Require positive feed and 0 < feed fraction <= product fraction <= 1.')
    product=feed*fraction_in/fraction_product
    return product,feed-product


def heating_duty(mass_flow,heat_capacity,temp_in,temp_out):
    """Heat added in W: kg/s, J/(kg K), °C or K temperatures. No phase change."""
    if mass_flow<=0 or heat_capacity<=0:
        raise ValueError('Require positive mass flow and heat capacity.')
    return mass_flow*heat_capacity*(temp_out-temp_in)


def mixing_temperature(flow_a,temp_a,flow_b,temp_b):
    """Adiabatic mixing of the same liquid with equal constant cp; no phase change."""
    if min(flow_a,flow_b)<0 or flow_a+flow_b<=0:
        raise ValueError('Require nonnegative flows and positive total flow.')
    return (flow_a*temp_a+flow_b*temp_b)/(flow_a+flow_b)


def tank_inventory(initial_mass,inflow,outflow,time_seconds):
    """Mass in kg before emptying/overflow; flows kg/s, time s, no level control.

    No tank capacity is assumed. Caller must impose any upper capacity limit.
    """
    times=np.asarray(time_seconds,dtype=float)
    if min(initial_mass,inflow,outflow)<0 or np.any(times<0):
        raise ValueError('Require nonnegative masses, flows and times.')
    mass=initial_mass+(inflow-outflow)*times
    if np.any(mass<0):
        raise ValueError('Tank would empty; the constant-outflow model no longer applies.')
    return mass
