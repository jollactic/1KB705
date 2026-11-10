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


# Synthetic reference-speed performance data. These are not manufacturer limits.
H0, CURVE_A = 40.0, 1.5e6
RUNOUT_FLOW = np.sqrt(H0/CURVE_A)
_reference_q = np.linspace(0, RUNOUT_FLOW, 20001)
_reference_eta = 998*9.81*_reference_q*(H0-CURVE_A*_reference_q**2)/(900+40000*_reference_q)
BEP_FLOW = float(_reference_q[np.argmax(_reference_eta)])


def performance(flow, speed=1.0, motor_efficiency=.90, drive_efficiency=.96):
    """One pump: SI head, hydraulic/shaft/electrical power, efficiency and range.

    Reference shaft input P_ref(q)=900+40000q W; q=Q/s (m³/s).
    Affinity scaling: H=s² H_ref(Q/s), P_shaft=s³ P_ref(Q/s).
    Efficiency is derived, not independently fitted. Intended only for water
    of density 998 kg/m³. Assumed operating band: 0.65–1.35 Q_BEP at speed s.
    Nonzero shutoff input is illustrative, not permission to operate at shutoff.
    """
    q = np.asarray(flow,dtype=float)
    if speed <= 0 or not 0 < motor_efficiency <= 1 or not 0 < drive_efficiency <= 1:
        raise ValueError('Require positive speed and motor/drive efficiencies in (0,1].')
    reference_flow = q/speed
    if np.any(~np.isfinite(q)) or np.any(q < 0) or np.any(reference_flow > RUNOUT_FLOW*(1+1e-12)):
        raise ValueError('Flow outside the nonnegative-head synthetic curve domain.')
    head = np.maximum(0.,pump_head(q,H0,CURVE_A,speed))
    hydraulic = 998*9.81*q*head
    shaft = speed**3*(900+40000*reference_flow)
    eta = hydraulic/shaft
    ratio = reference_flow/BEP_FLOW
    recommended = (ratio >= .65) & (ratio <= 1.35)
    return dict(head=head, hydraulic=hydraulic, shaft=shaft,
                electrical=shaft/(motor_efficiency*drive_efficiency),
                efficiency=eta, bep_ratio=ratio, recommended=recommended)


def arrangement_head(total_flow, speed=1., arrangement='single'):
    """Ideal identical pumps: series adds heads, parallel adds flows at equal head."""
    series, parallel = arrangement_counts(arrangement)
    return series*pump_head(np.asarray(total_flow)/parallel,H0,CURVE_A,speed)


def arrangement_counts(arrangement):
    if arrangement not in ('single','series','parallel'):
        raise ValueError('Choose single, series or parallel.')
    return {'single':(1,1),'series':(2,1),'parallel':(1,2)}[arrangement]


def design_at_flow(flow, diameter, rise=12., arrangement='single', roughness=4.5e-5,
                   motor_efficiency=.90, drive_efficiency=.96, hours=4000):
    """Match a fixed total flow by speed adjustment. No throttling or bypass.

    Both pumps in a pair run at the same speed; no interconnecting pipe losses.
    Feasible means speed 0.6–1.1 AND each pump within assumed BEP operating band.
    NPSH, motor rating and pressure ratings remain unverified.
    """
    if hours < 0:
        raise ValueError('Hours must be nonnegative.')
    series, parallel = arrangement_counts(arrangement)
    head = float(system_head(flow,diameter,120.,rise,roughness,8.))
    if head <= 0:
        raise ValueError('This exercise requires positive system head.')
    pump_flow = flow/parallel
    speed = np.sqrt((head/series+CURVE_A*pump_flow**2)/H0)
    point = performance(pump_flow,speed,motor_efficiency,drive_efficiency)
    total_shaft = series*parallel*float(point['shaft'])
    total_electrical = series*parallel*float(point['electrical'])
    speed_ok = .6 <= speed <= 1.1
    range_ok = bool(point['recommended'])
    return dict(flow=flow,head=head,speed=speed,pump_flow=pump_flow,
                efficiency=float(point['efficiency']),shaft=total_shaft,
                electrical=total_electrical,annual_kwh=total_electrical/1000*hours,
                specific_kwh=total_electrical/flow/3.6e6,
                feasible=speed_ok and range_ok,speed_ok=speed_ok,range_ok=range_ok,
                bep_ratio=float(point['bep_ratio']),arrangement=arrangement)


def free_operating_point(diameter=.065, speed=1., rise=12., arrangement='single'):
    """Bisection of the uncontrolled head intersection; supplied student utility."""
    _, parallel = arrangement_counts(arrangement)
    low, high = .001, parallel*speed*RUNOUT_FLOW
    def residual(q):
        return float(arrangement_head(q,speed,arrangement)-system_head(q,diameter,120,rise,4.5e-5,8))
    if residual(low)*residual(high) >= 0:
        raise ValueError('No turbulent-flow root in the supplied bracket.')
    for _ in range(100):
        mid = (low+high)/2
        value = residual(mid)
        if abs(value) < 1e-8:
            return mid
        if value > 0:
            low = mid
        else:
            high = mid
    raise ValueError('Operating-point search did not converge.')


def plot_performance(speed=1., operating_flow=None):
    """Three aligned axes avoid confusing scales while showing coupled curves."""
    import matplotlib.pyplot as plt
    q = np.linspace(0,speed*RUNOUT_FLOW,300)
    point = performance(q,speed)
    fig,axes = plt.subplots(3,1,figsize=(9,9),sharex=True)
    axes[0].plot(q*1000,point['head'],color='royalblue',label='Pump head')
    axes[0].set_ylabel('Head / m')
    axes[1].plot(q*1000,point['efficiency']*100,color='green',label='Pump efficiency')
    axes[1].set_ylabel('Efficiency / %')
    axes[2].plot(q*1000,point['shaft']/1000,color='firebrick',label='Shaft input')
    axes[2].plot(q*1000,point['electrical']/1000,'--',color='purple',label='Electrical input')
    axes[2].set_ylabel('Power / kW'); axes[2].set_xlabel('Flow per pump / L s$^{-1}$')
    for axis in axes:
        axis.axvspan(.65*BEP_FLOW*speed*1000,1.35*BEP_FLOW*speed*1000,
                     alpha=.12,color='green',label='Assumed operating band')
        axis.axvline(BEP_FLOW*speed*1000,color='green',linestyle=':',label='BEP')
        if operating_flow is not None:
            axis.axvline(operating_flow*1000,color='black',linestyle='--',label='Operating flow')
        axis.grid(); axis.legend(loc='best',fontsize=8)
    fig.suptitle(f'Synthetic pump performance at speed ratio {speed:.3f} — not manufacturer data')
    fig.tight_layout()
    return fig


def plot_arrangements():
    """Conceptual connections: arrow direction is flow, not a valve specification."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyArrowPatch
    fig,axes = plt.subplots(1,3,figsize=(12,3))
    for axis,name in zip(axes,['Single','Series: same flow, add heads','Parallel: same head, add flows']):
        axis.set(xlim=(0,6),ylim=(0,3),aspect='equal',title=name)
        axis.axis('off')
    def pump(axis,x,y):
        axis.add_patch(Circle((x,y),.32,fc='white',ec='navy',lw=2))
        axis.text(x,y,'P',ha='center',va='center')
    def arrow(axis,start,end):
        axis.add_patch(FancyArrowPatch(start,end,arrowstyle='->',mutation_scale=12,color='steelblue',lw=2))
    pump(axes[0],3,1.5); arrow(axes[0],(.3,1.5),(2.65,1.5)); arrow(axes[0],(3.35,1.5),(5.7,1.5))
    for x in [2,4]:
        pump(axes[1],x,1.5)
    for a,b in [(.3,1.65),(2.35,3.65),(4.35,5.7)]:
        arrow(axes[1],(a,1.5),(b,1.5))
    for y in [.7,2.3]:
        pump(axes[2],3,y)
        axes[2].plot([1.2,1.2,2.65],[1.5,y,y],color='steelblue',lw=2)
        axes[2].plot([3.35,4.8,4.8],[y,y,1.5],color='steelblue',lw=2)
        arrow(axes[2],(1.4,y),(2.6,y)); arrow(axes[2],(3.4,y),(4.6,y))
    arrow(axes[2],(.3,1.5),(1.2,1.5)); arrow(axes[2],(4.8,1.5),(5.7,1.5))
    fig.suptitle('Idealized connections — interconnecting losses and valves omitted')
    fig.tight_layout()
    return fig
