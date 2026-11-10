"""Hypothetical constant-volatility binary; q=1, total condenser."""
import numpy as np


def equilibrium(x, alpha=2.4):
    """Equilibrium vapour mole fraction from liquid mole fraction."""
    x = np.asarray(x)
    if alpha <= 1 or np.any((x < 0) | (x > 1)):
        raise ValueError('Require alpha > 1 and 0 <= x <= 1.')
    return alpha*x/(1+(alpha-1)*x)


def inverse_equilibrium(y, alpha=2.4):
    """Inverse of equilibrium, with the same composition bounds."""
    y = np.asarray(y)
    if alpha <= 1 or np.any((y < 0) | (y > 1)):
        raise ValueError('Require alpha > 1 and 0 <= y <= 1.')
    return y/(alpha-(alpha-1)*y)


def operating_lines(z_feed, x_distillate, x_bottoms, reflux):
    """Return rectifying and stripping callables for saturated-liquid feed."""
    if not 0 < x_bottoms < z_feed < x_distillate < 1 or reflux < 0:
        raise ValueError('Require 0 < xB < zF < xD < 1 and R >= 0.')
    def rect(x):
        return reflux/(reflux+1)*x+x_distillate/(reflux+1)
    intersection_y = rect(z_feed)
    slope = (intersection_y-x_bottoms)/(z_feed-x_bottoms)
    def strip(x):
        return slope*(x-x_bottoms)+x_bottoms
    return rect, strip


def minimum_reflux(z_feed, x_distillate, alpha=2.4):
    """Feed-pinch minimum for the prescribed q=1, constant-alpha model."""
    if not 0 < z_feed < x_distillate < 1:
        raise ValueError('Require 0 < zF < xD < 1.')
    slope = (x_distillate-float(equilibrium(z_feed, alpha)))/(x_distillate-z_feed)
    return max(0.0, slope/(1-slope))


def stage_count(z_feed, x_distillate, x_bottoms, reflux, alpha=2.4, max_stages=300):
    """Full integer equilibrium stages, including partial reboiler, no condenser.

    Returns (count, staircase_array). Last stage is rounded up, not interpolated.
    """
    rect, strip = operating_lines(z_feed, x_distillate, x_bottoms, reflux)
    if reflux <= minimum_reflux(z_feed, x_distillate, alpha):
        raise ValueError('Reflux must exceed minimum reflux.')
    old_x, y = x_distillate, x_distillate
    points = [(old_x, y)]
    for n in range(1, max_stages+1):
        x = float(inverse_equilibrium(y, alpha))
        if x >= old_x-1e-12:
            raise ValueError('Pinch or non-progressing staircase.')
        points.append((x, y))
        if x <= x_bottoms:
            return n, np.array(points)
        y = float(rect(x) if x >= z_feed else strip(x))
        points.append((x, y))
        old_x = x
    raise ValueError('Stage cap reached; increase reflux or inspect the model.')


def compare_designs(feed=100.,efficiency=.65,heat_price=.03,years=10,hours=4000):
    """Same separation; synthetic active-height/vapour limits and cost comparison.

    Specs zF=.45,xD=.95,xB=.05, alpha=2.4, q=1. Max active height 8 m,
    max V=190 kmol/h. QR=V*lambda/3600 kW with assumed equal latent heats
    lambda=30000 kJ/kmol and negligible sensible changes. Approximate duty model,
    not measured mixture data. Installed cost €50000+3000*Ntrays+250*V;
    no cooling cost, hydraulic sizing, maintenance or discounting.
    """
    if feed <= 0 or not 0 < efficiency <= 1 or min(heat_price,years,hours)<0:
        raise ValueError('Require positive feed, efficiency in (0,1], nonnegative costs/time.')
    D = feed*(.45-.05)/(.95-.05)
    minimum = minimum_reflux(.45,.95)
    rows = []
    for multiple in [1.1,1.5,1.8,2.0,2.2,3.0]:
        R = multiple*minimum
        N,_ = stage_count(.45,.95,.05,R)
        trays = int(np.ceil((N-1)/efficiency))
        height = trays*.45
        V = (R+1)*D
        duty_kw = V*30000/3600
        capital = 50000+3000*trays+250*V
        rows.append(dict(multiple=multiple,R=R,stages=N,trays=trays,height=height,V=V,
                         duty_kw=duty_kw,capital=capital,
                         total=capital+duty_kw*heat_price*hours*years,
                         feasible=height<=8 and V<=190))
    return rows
