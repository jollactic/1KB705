"""SI-unit teaching utilities. Friction factors are Darcy factors."""
import numpy as np


def friction_factor(reynolds, relative_roughness):
    """64/Re below 2300; Haaland above 4000. Reject transition."""
    re = np.asarray(reynolds, dtype=float)
    if np.any(re <= 0) or relative_roughness < 0:
        raise ValueError('Require Re > 0 and nonnegative relative roughness.')
    if np.any((re >= 2300) & (re < 4000)):
        raise ValueError('Transition flow requires a separate model (2300 <= Re < 4000).')
    return np.where(re < 2300, 64/re,
                    (-1.8*np.log10((relative_roughness/3.7)**1.11 + 6.9/re))**-2)


def system_head(flow, diameter, length, rise, roughness, loss_coefficient,
                density=998.0, viscosity=1e-3):
    """Head in m for positive volumetric flow in m³/s, including static rise."""
    q = np.asarray(flow, dtype=float)
    if np.any(q <= 0) or min(diameter, density, viscosity) <= 0:
        raise ValueError('Require positive flow, diameter, density and viscosity.')
    if min(length, roughness, loss_coefficient) < 0:
        raise ValueError('Length, roughness and loss coefficient must be nonnegative.')
    velocity = 4*q/(np.pi*diameter**2)
    re = density*velocity*diameter/viscosity
    f = friction_factor(re, roughness/diameter)
    return rise+(f*length/diameter+loss_coefficient)*velocity**2/(2*9.81)


def pump_head(flow, shutoff_head=40.0, curve_coefficient=1.5e6, speed_ratio=1.0):
    """Illustrative affinity-scaled curve, H=s² H0-a Q²; not a pump catalogue."""
    if min(shutoff_head, curve_coefficient, speed_ratio) <= 0:
        raise ValueError('Pump parameters must be positive.')
    if np.any(np.asarray(flow) < 0):
        raise ValueError('Flow must be nonnegative.')
    return speed_ratio**2*shutoff_head-curve_coefficient*np.asarray(flow)**2
