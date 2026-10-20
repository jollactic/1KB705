"""Linear-equilibrium absorption and dry-bed hydraulic screening."""
import numpy as np


def stage_count(gas_flow, solvent_flow, gas_in, gas_out, liquid_in=0.0,
                slope=1.5, max_stages=300):
    """Mole-ratio basis, solute-free flow rates. Full final ideal stage.

    Returns (count, staircase_array), stepped from column top to bottom.
    """
    if min(gas_flow, solvent_flow, slope) <= 0 or liquid_in < 0:
        raise ValueError('Require positive flows/slope and nonnegative liquid inlet.')
    if not gas_in > gas_out > slope*liquid_in:
        raise ValueError('Require Yin > Yout > m Xin for absorption.')
    minimum = gas_flow*(gas_in-gas_out)/(gas_in/slope-liquid_in)
    if solvent_flow <= minimum:
        raise ValueError('Solvent flow must exceed the pinch minimum.')
    y = gas_out
    points = [(liquid_in, y)]
    for n in range(1, max_stages+1):
        x = y/slope
        points.append((x, y))
        next_y = gas_out+solvent_flow/gas_flow*(x-liquid_in)
        points.append((x, next_y))
        if next_y >= gas_in:
            return n, np.array(points)
        if next_y <= y+1e-12:
            raise ValueError('Pinch or non-progressing staircase.')
        y = next_y
    raise ValueError('Stage cap reached; increase solvent flow or inspect the model.')


def ergun_gradient(superficial_velocity, void_fraction, particle_diameter,
                   density=1.2, viscosity=1.8e-5):
    """Dry-bed pressure gradient in Pa/m. SI units; not a wet-packing model.

    150 mu (1-e)^2 u/(e^3 dp^2) + 1.75 rho (1-e) u^2/(e^3 dp).
    The supplied equivalent diameter is illustrative; no flooding prediction.
    """
    if not 0 < void_fraction < 1 or min(particle_diameter, density, viscosity) <= 0:
        raise ValueError('Require 0 < void fraction < 1 and positive properties.')
    if superficial_velocity < 0:
        raise ValueError('Superficial velocity must be nonnegative.')
    e, dp, u = void_fraction, particle_diameter, superficial_velocity
    return 150*viscosity*(1-e)**2*u/(e**3*dp**2)+1.75*density*(1-e)*u**2/(e**3*dp)
