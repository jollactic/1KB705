"""Authored answers used to fill the four separate instructor notebooks."""

SOLUTIONS = {}

SOLUTIONS['lab_01_flow'] = {
    'prediction': 'Prediction: reducing pipe diameter will increase friction losses strongly, '
                  'while reducing pump speed will reduce both available head and operating flow. '
                  'The elevation rise remains fixed even when pipe losses are reduced.',
    'warmup': (
        'A smaller pipe increases velocity and especially the pipe-friction term. '
        'Increasing flow from 3 to 4 L/s further increases both friction and fitting losses. '
        'The printed contributions identify which term changes most; elevation is unchanged.',
        '''
        print("D / m   Q / L/s   pipe loss / m   fitting loss / m   total / m")
        for warm_D, warm_q in [(0.065, .003), (.050, .003), (.050, .004)]:
            warm_v = 4*warm_q/(np.pi*warm_D**2)
            warm_f = float(h.friction_factor(998*warm_v*warm_D/.001, 4.5e-5/warm_D))
            warm_pipe = warm_f*120/warm_D*warm_v**2/(2*9.81)
            warm_fittings = 8*warm_v**2/(2*9.81)
            print(f"{warm_D:.3f}   {warm_q*1000:.1f}       {warm_pipe:.3f}           {warm_fittings:.3f}            {12+warm_pipe+warm_fittings:.3f}")
        '''),
    'tasks': [(
        '''
        trial_q = .003
        velocity = 4*trial_q/(np.pi*diameter**2)
        reynolds = rho*velocity*diameter/mu
        # Independent evaluation of the stated Haaland correlation.
        darcy_f = (-1.8*np.log10((roughness/diameter/3.7)**1.11 + 6.9/reynolds))**-2
        pipe_loss = darcy_f*length/diameter*velocity**2/(2*g)
        fitting_loss = K*velocity**2/(2*g)
        hand_head = rise + pipe_loss + fitting_loss
        reference_head = float(h.system_head(trial_q, diameter, length, rise, roughness, K, rho, mu))
        assert np.isclose(hand_head, reference_head)
        print(f"v = {velocity:.6f} m/s; Re = {reynolds:.1f}; f_D = {darcy_f:.6f}")
        print(f"Pipe = {pipe_loss:.6f} m; fittings = {fitting_loss:.6f} m; total = {hand_head:.6f} m")
        print(f"Equivalent pressure rise = {rho*g*hand_head/1000:.3f} kPa")
        print(f"Helper mismatch = {hand_head-reference_head:.3e} m; zero-flow limit = {rise:.1f} m")
        ''',
        r'''Between the large open tank surfaces, pressures are equal and velocities
are negligible. Bernoulli therefore reduces to $H_p=z_2-z_1+h_f+h_K$.
The Darcy–Weisbach expression supplies $h_f=f_D(L/D)v^2/(2g)$ and the
fittings supply $h_K=\Sigma K\,v^2/(2g)$. At 3 L/s the required head is
14.0484 m, including 12 m of elevation. Head measures energy per unit weight
in metres; pressure is force per area, and the equivalent pressure is $\rho gH$.
The helper agrees with the independently evaluated correlation. As flow tends
to zero the fitting loss vanishes as $Q^2$, and the laminar pipe loss vanishes
as $Q$ because $f=64/Re$. Hence the head tends to 12 m, without evaluating
the singular friction factor at zero Reynolds number.'''), (
        '''
        def bisect_root(function, low, high, tolerance=1e-6, max_iterations=200):
            f_low, f_high = function(low), function(high)
            if f_low == 0:
                return low
            if f_high == 0:
                return high
            if not np.isfinite([f_low, f_high]).all() or f_low*f_high > 0:
                raise ValueError("A finite sign-changing bracket is required")
            for iteration in range(max_iterations):
                mid = (low+high)/2
                f_mid = function(mid)
                if not np.isfinite(f_mid):
                    raise ValueError("Nonfinite residual")
                if abs(f_mid) < tolerance:
                    return mid
                if f_low*f_mid < 0:
                    high = mid
                else:
                    low, f_low = mid, f_mid
            raise ValueError("Bisection did not converge")

        def operating_point(D, speed=1.0, eps=roughness, eta=efficiency):
            if not 0 < eta <= 1:
                raise ValueError("Efficiency must lie in (0, 1]")
            def residual(q):
                return float(h.pump_head(q, H0, a, speed) -
                             h.system_head(q, D, length, rise, eps, K, rho, mu))
            # Lower end remains turbulent for every D in this exercise.
            low, high = .001, speed*np.sqrt(H0/a)
            flow = bisect_root(residual, low, high)
            head = float(h.pump_head(flow, H0, a, speed))
            shaft = rho*g*flow*head/eta
            assert abs(residual(flow)) < .001
            return flow, head, shaft, shaft/flow/3.6e6  # m³/s, m, W, kWh/m³

        base_q, base_h, base_power, base_specific = operating_point(diameter)
        assert base_q >= .003
        print(f"Operating flow = {base_q*1000:.6f} L/s; head = {base_h:.6f} m")
        print(f"Shaft power = {base_power:.3f} W; annual energy = {base_power/1000*4000:.2f} kWh")
        print(f"Specific energy = {base_specific:.6f} kWh/m³")
        plt.figure(figsize=(7, 4))
        plt.plot(Q*1000, system, label="System")
        plt.plot(Q*1000, h.pump_head(Q, H0, a), label="Pump")
        plt.scatter([base_q*1000], [base_h], color="black", label="Operating point")
        plt.xlabel("Flow / L s$^{-1}$"); plt.ylabel("Head / m"); plt.legend(); plt.grid(); plt.show()
        ''',
        '''The curves intersect at 4.03456 L/s and 15.5835 m, exceeding the
3 L/s requirement. Shaft power is about 879.35 W and annual electricity use
is 3517.4 kWh at 4000 hours. The bracket is checked separately for every
case. The residual tolerance is stricter than the required 0.001 m; a small
head mismatch establishes numerical convergence, not physical model accuracy.'''), (
        '''
        designs = []
        print("D / m  speed   flow / L/s  shaft / W  kWh/m³     >=3 L/s")
        for D in [.050, .065, .080]:
            for speed in [.8, 1.0, 1.1]:
                flow, head, power, specific = operating_point(D, speed)
                designs.append((D, speed, flow, head, power, specific))
                print(f"{D:.3f}   {speed:.1f}     {flow*1000:8.4f}   {power:8.2f}  {specific:.6f}   {flow >= .003}")
        feasible_designs = [row for row in designs if row[2] >= .003]
        selected = min(feasible_designs, key=lambda row: row[5])
        chosen_D, chosen_speed = selected[:2]
        print(f"Lowest specific-energy feasible candidate: D={chosen_D:.3f} m, speed={chosen_speed:.1f}")
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))
        for D in [.050, .065, .080]:
            rows = np.array([row for row in designs if row[0] == D])
            axes[0].plot(rows[:, 1], rows[:, 2]*1000, 'o-', label=f"D={D:.3f} m")
            axes[1].plot(rows[:, 1], rows[:, 5], 'o-', label=f"D={D:.3f} m")
        axes[0].axhline(3, color='black', linestyle=':', label='Required flow')
        axes[0].set_ylabel("Operating flow / L s$^{-1}$")
        axes[1].set_ylabel("Specific energy / kWh m$^{-3}$")
        for axis in axes:
            axis.set_xlabel("Speed ratio / dimensionless"); axis.legend(); axis.grid()
        plt.tight_layout(); plt.show()
        ''',
        '''The 80 mm pipe at speed ratio 1.0 is the lowest specific-energy
candidate meeting the nominal minimum flow. Larger pipes reduce hydraulic
losses; all three 0.8-speed candidates fall below 3 L/s. A smaller total
power can also mean that less water is being delivered, so power alone is an
unfair basis for comparing different throughputs. Specific energy normalizes
by delivered volume. Capital cost, control requirements and an actual efficiency
curve are absent, so this is an energy-based selection among nine candidates,
not a global economic optimum.'''), (
        '''
        roughness_values = np.unique(np.r_[np.linspace(1e-6, 2e-4, 25), roughness])
        eta_values = np.unique(np.r_[np.linspace(.55, .80, 25), efficiency])
        rough_results = np.array([operating_point(chosen_D, chosen_speed, eps=value)
                                  for value in roughness_values])
        eta_results = np.array([operating_point(chosen_D, chosen_speed, eta=value)
                                for value in eta_values])
        fig, axes = plt.subplots(1, 3, figsize=(13, 4))
        axes[0].plot(roughness_values*1e6, rough_results[:, 0]*1000)
        axes[0].axhline(3, color='black', linestyle=':')
        axes[0].set(xlabel="Roughness / µm", ylabel="Operating flow / L s$^{-1}$")
        axes[1].plot(roughness_values*1e6, rough_results[:, 3])
        axes[1].set(xlabel="Roughness / µm", ylabel="Specific energy / kWh m$^{-3}$")
        axes[2].plot(eta_values, eta_results[:, 3])
        axes[2].set(xlabel="Efficiency / dimensionless", ylabel="Specific energy / kWh m$^{-3}$")
        for axis in axes:
            axis.grid()
        plt.tight_layout(); plt.show()
        rough_change = (rough_results[:, 3].max()/rough_results[:, 3].min()-1)*100
        eta_change = (eta_results[:, 3].max()/eta_results[:, 3].min()-1)*100
        print(f"Specific-energy span: roughness {rough_change:.2f}%; efficiency {eta_change:.2f}% (max/min - 1)")
        print(f"Minimum flow across roughness sweep: {rough_results[:,0].min()*1000:.4f} L/s")
        assert np.allclose(eta_results[:, 0], eta_results[0, 0])
        # Check all designs at worst roughness before declaring a robust candidate.
        robust = [row for row in designs if operating_point(row[0], row[1], eps=2e-4)[0] >= .003]
        robust_choice = min(robust, key=lambda row: row[5])
        print(f"Robust to stated roughness range: D={robust_choice[0]:.3f} m, speed={robust_choice[1]:.1f}")
        ''',
        '''Efficiency has the larger effect on specific energy over the stated
ranges. In this simplified model efficiency changes shaft power but not the
head-curve intersection. Roughness affects both flow and head and must also
be checked against minimum throughput. The 80 mm, full-speed candidate remains
above 3 L/s across this range. Real selection requires a measured pump curve,
efficiency versus flow, NPSH available and required, suction losses, liquid
temperature, allowable operating range, and piping costs.''')],
    'recommendation': '''I recommend the 80 mm pipe with the illustrative pump at
speed ratio 1.0 for the stated transfer duty. Among the nine candidates, it meets
the minimum delivery of 3 L/s and gives the lowest electricity per unit volume
at the assumed efficiency. This is a conditional selection based on operating
energy; installation cost could justify a different pipe diameter. The labelled
flowsheet shows the two open tanks, pump and connecting pipe, and the energy
balance is applied between the two free surfaces.

The original 65 mm, full-speed case delivers 4.03456 L/s at 15.5835 m head.
Its shaft power is 879.35 W, corresponding to 3517.4 kWh for 4000 operating
hours per year. The numerical residual is below 0.001 m. Independently adding
the elevation, straight-pipe and fitting contributions reproduces the helper
calculation, providing a separate check on units and the friction convention.
All friction factors used here are Darcy factors.

The comparison shows why pipe diameter and speed must be checked together.
A larger diameter reduces dynamic losses, but at speed ratio 0.8 even the
80 mm pipe falls below 3 L/s. Comparing shaft power alone would mix energy
performance with delivered throughput, so the recommendation also uses kWh per
cubic metre and explicitly checks minimum flow. A requirement for exactly
3 L/s would call for a separate controlled-flow calculation.

The selected candidate continues to meet the flow requirement across the
specified roughness range. Over the stated uncertainty ranges, efficiency has
a larger influence on specific electricity use than roughness. However,
efficiency has been treated as independent of flow and speed; a real pump
can behave differently. Static elevation head remains necessary even with a
frictionless pipe, placing a lower bound on the hydraulic energy demand.

Before procurement, obtain manufacturer head and efficiency curves at the
intended speeds, verify suction conditions and NPSH margin, and confirm actual
pipe lengths, fittings and surface elevations. Add capital and maintenance
costs, flow control requirements, and permitted operating limits. These checks
could change the final equipment choice even though the simplified energy
comparison is internally consistent.''',
    'extension': (
        'Two identical parallel pumps each deliver Q_total/2 at the common head, '
        'so H_parallel(Q_total) = H_single(Q_total/2). The system loss rises with '
        'total flow, making the combined operating flow less than twice the single-pump flow.',
        '''
        parallel_q = bisect_root(
            lambda q: float(h.pump_head(q/2, H0, a) -
                            h.system_head(q, diameter, length, rise, roughness, K, rho, mu)),
            .001, 2*np.sqrt(H0/a))
        print(f"Single-pump flow: {base_q*1000:.4f} L/s")
        print(f"Two parallel pumps: {parallel_q*1000:.4f} L/s; twice single: {2*base_q*1000:.4f} L/s")
        assert base_q < parallel_q < 2*base_q
        plt.figure(figsize=(7,4))
        ext_q = np.linspace(.001, .010, 200)
        plt.plot(ext_q*1000, h.system_head(ext_q, diameter, length, rise, roughness, K, rho, mu), label="System")
        plt.plot(ext_q*1000, h.pump_head(ext_q, H0, a), label="Single pump")
        plt.plot(ext_q*1000, h.pump_head(ext_q/2, H0, a), label="Two pumps in parallel")
        plt.ylim(0, 60); plt.xlabel("Total flow / L s$^{-1}$"); plt.ylabel("Head / m")
        plt.legend(); plt.grid(); plt.show()
        ''')
}

SOLUTIONS['lab_02_heat'] = {
    'prediction': 'Prediction: fouling increases thermal resistance and reduces recovered heat '
                  'for a fixed area. More cold flow can recover more heat while producing a lower outlet temperature.',
    'warmup': (
        'Raising the cold outlet target increases both duty and required area. A '
        '75 °C target exceeds the 70 °C hot inlet and gives a negative terminal '
        'driving force, so it is infeasible for this passive exchanger.',
        '''
        for warm_target in [35., 45., 75.]:
            warm_duty = ex_Cc*(warm_target-ex_Tci)
            warm_hot_out = ex_Thi-warm_duty/ex_Ch
            warm_deltas = (ex_Thi-warm_target, warm_hot_out-ex_Tci)
            if min(warm_deltas) <= 0:
                print(f"Target {warm_target:.0f} °C: infeasible; terminal differences = {warm_deltas}")
            else:
                warm_area = warm_duty/(ex_U*h.lmtd(*warm_deltas))
                print(f"Target {warm_target:.0f} °C: duty {warm_duty/1000:.2f} kW, area {warm_area:.3f} m²")
        '''),
    'tasks': [(
        '''
        cold_duty = mc*cpc*(Tco_target-Tci)
        independent_hot_out = Thi-cold_duty/(mh*cph)
        dt1, dt2 = Thi-Tco_target, independent_hot_out-Tci
        independent_lmtd = (dt1-dt2)/np.log(dt1/dt2)
        independent_area = cold_duty/(U_clean*independent_lmtd)
        qmax = min(Ch, Cc)*(Thi-Tci)
        effectiveness = cold_duty/qmax
        energy_residual = Ch*(Thi-independent_hot_out)-cold_duty
        assert np.isclose(independent_area, area)
        assert abs(energy_residual) < 1e-8
        print(f"Duty = {cold_duty/1000:.3f} kW; hot outlet = {independent_hot_out:.4f} °C")
        print(f"Area = {independent_area:.5f} m²; Qmax = {qmax/1000:.3f} kW; effectiveness = {effectiveness:.6f}")
        print(f"Balance residual = {energy_residual:.3e} W; terminal differences = {dt1:.3f}, {dt2:.3f} K")
        plt.figure(figsize=(7,4))
        plt.plot([0,1], [Thi, independent_hot_out], 'o-', label='Hot stream →')
        plt.plot([0,1], [Tco_target, Tci], 'o-', label='Cold stream ←')
        plt.xticks([0,1], ['Hot inlet / cold outlet', 'Hot outlet / cold inlet'])
        plt.ylabel('Temperature / °C'); plt.title('Terminal temperatures — schematic connections only')
        plt.legend(); plt.grid(); plt.show()
        ''',
        r'''For each stream, enthalpy change is $\dot m c_p\Delta T$.
Neglecting external loss gives $C_h(T_{h,in}-T_{h,out})=C_c(T_{c,out}-T_{c,in})$.
The duty is 167.2 kW, compared with a maximum of 292.6 kW, giving an
effectiveness of 0.57143. The LMTD is based on two positive terminal
differences, 30 K and 33.3333 K. The cold outlet at 55 °C is warmer than
the hot outlet at 48.3333 °C because they are at opposite ends. Locally,
the hot stream is still warmer than the adjacent cold stream. Straight
segments in the figure are schematic, not a computed temperature profile.'''), (
        '''
        def effectiveness_own(ntu, cr):
            if ntu < 0 or not 0 <= cr <= 1:
                raise ValueError("Require NTU >= 0 and 0 <= Cr <= 1")
            if abs(1-cr) < 1e-10:
                return ntu/(1+ntu)
            numerator = -np.expm1(-ntu*(1-cr))
            return numerator/((1-cr)+cr*numerator)

        def predict_outlets(UA, hot_capacity=Ch, cold_capacity=Cc):
            cmin, cmax = min(hot_capacity, cold_capacity), max(hot_capacity, cold_capacity)
            eps = effectiveness_own(UA/cmin, cmin/cmax)
            q = eps*cmin*(Thi-Tci)
            return Thi-q/hot_capacity, Tci+q/cold_capacity, q

        ntu, cr = U_clean*area/min(Ch,Cc), min(Ch,Cc)/max(Ch,Cc)
        recovered_hot, recovered_cold, recovered_duty = predict_outlets(U_clean*area)
        assert np.allclose([recovered_hot, recovered_cold, recovered_duty], [Tho,Tco_target,duty])
        assert np.isclose(effectiveness_own(2,1), 2/3)
        assert np.isclose(effectiveness_own(1e-9,.5), 1e-9, rtol=1e-6, atol=1e-15)
        assert np.isclose(effectiveness_own(100,.5), 1)
        assert np.isclose(effectiveness_own(0,.5), 0)
        for test_ntu in [0, 1e-9, 1, 100]:
            for test_cr in [.5, 1.0]:
                assert np.isclose(effectiveness_own(test_ntu,test_cr), h.countercurrent_effectiveness(test_ntu,test_cr))
        print(f"NTU = {ntu:.6f}; Cr = {cr:.6f}; hot outlet = {recovered_hot:.4f} °C; cold outlet = {recovered_cold:.4f} °C")
        print("Zero, small/large NTU, equal-capacity and helper comparisons passed")
        ''',
        '''The independently coded effectiveness method reproduces both target
outlets and the LMTD duty. At zero NTU there is no heat transfer; for small
NTU effectiveness approaches NTU, and for very large NTU it approaches one.
At equal capacity rates the general expression has the indeterminate form
0/0. Using its analytical limit, NTU/(1+NTU), avoids division by zero and
preserves continuity. `expm1` improves accuracy when the exponential argument
is very small.'''), (
        '''
        resistance = np.unique(np.r_[np.linspace(0,.001,60), .0006])
        fouled_U = 1/(1/U_clean+resistance)
        fixed_area_results = np.array([h.outlets(u*area, Ch, Cc, Thi, Tci) for u in fouled_U])
        design_R = .0006
        design_U = 1/(1/U_clean+design_R)
        fouled_sized_area = duty/(design_U*delta_lm)
        at_design = h.outlets(design_U*area, Ch,Cc,Thi,Tci)
        enlarged_design = h.outlets(design_U*fouled_sized_area, Ch,Cc,Thi,Tci)
        enlarged_clean = h.outlets(U_clean*fouled_sized_area, Ch,Cc,Thi,Tci)
        assert np.isclose(enlarged_design[1],55)
        print(f"At design fouling: U={design_U:.3f} W/(m² K)")
        print(f"Clean-sized area={area:.4f} m²: Tco={at_design[1]:.4f} °C, duty={at_design[2]/1000:.3f} kW")
        print(f"Fouling-sized area={fouled_sized_area:.4f} m²: Tco={enlarged_design[1]:.4f} °C")
        print(f"When clean, enlarged unit gives Tco={enlarged_clean[1]:.4f} °C: allow for control")
        fig, axes = plt.subplots(1,2,figsize=(11,4))
        axes[0].plot(resistance*1e4, fixed_area_results[:,2]/1000)
        axes[0].set_ylabel('Recovered duty / kW')
        axes[1].plot(resistance*1e4, fixed_area_results[:,1])
        axes[1].axhline(55,color='black',linestyle=':', label='Target'); axes[1].legend()
        axes[1].set_ylabel('Cold outlet / °C')
        for axis in axes:
            axis.set_xlabel('Added resistance / (10$^{-4}$ m² K W$^{-1}$)'); axis.grid()
        plt.tight_layout(); plt.show()
        ''',
        '''The fixed clean-sized area cannot retain the original duty after U
decreases. At the specified fouling resistance its cold outlet falls to about
49.01 °C. Meeting the original 55 °C target at that resistance requires
approximately 11.30 m², 39% more area. A fouling-sized exchanger transfers
more than the target duty when clean, so a bypass or flow/temperature control
would be needed if 55 °C is a strict target rather than a minimum.'''), (
        '''
        cold_flows = np.unique(np.r_[np.linspace(.5,1.8,60),mc])
        # Chosen design: fouling-sized area, operated at design fouling resistance.
        flow_results = np.array([h.outlets(design_U*fouled_sized_area,Ch,value*cpc,Thi,Tci)
                                 for value in cold_flows])
        fig, axes = plt.subplots(1,2,figsize=(11,4))
        axes[0].plot(cold_flows,flow_results[:,1]); axes[0].set_ylabel('Cold outlet / °C')
        axes[1].plot(cold_flows,flow_results[:,2]/1000); axes[1].set_ylabel('Recovered duty / kW')
        for axis in axes:
            axis.set_xlabel('Cold mass flow / kg s$^{-1}$'); axis.grid()
        plt.tight_layout(); plt.show()
        for index in [0,-1]:
            print(f"mc={cold_flows[index]:.2f} kg/s: Tco={flow_results[index,1]:.3f} °C, duty={flow_results[index,2]/1000:.3f} kW")
        assert np.allclose(Ch*(Thi-flow_results[:,0]), cold_flows*cpc*(flow_results[:,1]-Tci))
        ''',
        '''At fixed installed area and assumed U, increasing cold flow raises
total recovered duty while reducing its temperature rise. This can improve
heat recovery yet miss the outlet-temperature requirement. In real equipment
U changes with velocity and convection coefficients, and pressure drop also
changes. The missing hydraulic design includes channel or tube geometry,
Reynolds numbers, pressure losses and pumping power. The sweep isolates a
thermal effect and does not establish a permissible operating envelope.''')],
    'recommendation': '''I recommend an ideal countercurrent exchanger with about
11.30 m² of heat-transfer area if the 55 °C cold-outlet requirement must be
met at an added fouling resistance of 0.0006 m² K/W. This recommendation
uses the stated constant heat capacities and the assumed clean coefficient of
650 W/(m² K). It is a thermal area estimate, pending hydraulic and mechanical
design. The system diagram identifies the opposite flow directions and the
four terminal temperatures used in the balances.

At the specified flows, the target duty is 167.2 kW. Conservation of energy
then gives a hot outlet of 48.3333 °C. The two terminal driving forces are
positive, and the required duty is only 57.14% of the thermodynamic maximum.
These checks establish feasibility within the ideal model. The cold outlet
being warmer than the hot outlet does not violate heat-transfer direction:
the outlets are at opposite ends of the countercurrent exchanger.

A clean-only design needs 8.13059 m². The independently implemented
effectiveness–NTU method reproduces the LMTD result, including both outlet
temperatures, and passes checks at zero NTU, large NTU and equal capacity
rates. With the clean-sized area held fixed, the design fouling resistance
reduces the cold outlet to about 49.01 °C. Adding area instead restores the
target. The enlarged unit will recover more heat when clean, so temperature
control or bypass provision should accompany the area allowance.

The cold-flow sweep shows that maximum heat recovery and maximum outlet
temperature are different objectives. Increasing cold flow can increase total
duty while lowering its outlet temperature. Operation should therefore be
judged against both process heat demand and the required temperature level,
not against recovered kilowatts alone.

Before purchase, confirm physical properties over the temperature range,
fouling behaviour, cleaning intervals, allowable pressure drops and actual
heat-transfer geometry. Flow-dependent convection coefficients and pumping
power are absent from this model, and a real multipass exchanger may need
an LMTD correction. Collect calibrated inlet/outlet temperatures and both
mass flows during operation to verify the energy balance and estimate UA.
Use those measurements to revise the fouling allowance and maintenance
schedule rather than treating the assumed resistance as a measured fact.''',
    'extension': (
        r'''With external heat loss, $Q_h=C_h(T_{h,in}-T_{h,out})$,
$Q_c=C_c(T_{c,out}-T_{c,in})$ and $Q_{loss}=Q_h-Q_c$.
The synthetic illustration below loses 5 kW from the hot stream to the room
upstream of the active exchanger. This explicit location assumption lets us
reuse the two-stream model. A single cold outlet cannot distinguish reduced
UA from heat loss. Measure all four temperatures and both flows, with
uncertainties; ambient/surface temperatures and insulation data help locate loss.
Real distributed loss would require an additional spatial energy balance.''',
        '''
        illustrative_loss = 5000.0  # W, synthetic upstream hot-side heat leak
        hot_at_exchanger = Thi-illustrative_loss/Ch
        loss_hot_out, loss_cold_out, cold_gain = h.outlets(
            design_U*fouled_sized_area,Ch,Cc,hot_at_exchanger,Tci)
        hot_release = Ch*(Thi-loss_hot_out)
        inferred_loss = hot_release-Cc*(loss_cold_out-Tci)
        print(f"Hot enthalpy decrease: {hot_release/1000:.3f} kW")
        print(f"Cold enthalpy increase: {cold_gain/1000:.3f} kW")
        print(f"Imbalance inferred as ambient loss: {inferred_loss/1000:.3f} kW")
        assert np.isclose(inferred_loss,illustrative_loss)
        ''')
}

SOLUTIONS['lab_03_distillation'] = {
    'prediction': 'Prediction: increasing reflux moves the operating lines toward the '
                  'diagonal and reduces ideal stages, while increasing vapour circulation. '
                  'Higher distillate purity is likely to increase separation effort.',
    'warmup': (
        'At R = 5 the operating line is closer to the diagonal and the liquid '
        'composition falls further per step. Below the feed, the stripping line '
        'must replace the rectifying line because the feed changes liquid flow.',
        '''
        print("R   step    x         next y")
        for warm_R in [3.,5.]:
            warm_rect,warm_strip = h.operating_lines(.5,.9,.1,warm_R)
            warm_y = .9
            for warm_n in range(1,3):
                warm_x = float(h.inverse_equilibrium(warm_y))
                warm_y = float(warm_rect(warm_x) if warm_x >= .5 else warm_strip(warm_x))
                print(f"{warm_R:.0f}    {warm_n}     {warm_x:.6f}  {warm_y:.6f}")
        '''),
    'tasks': [(
        '''
        D = F*(zF-xB)/(xD-xB)
        B = F-D
        total_residual = F-D-B
        component_residual = F*zF-D*xD-B*xB
        y_feed_star = float(h.equilibrium(zF,alpha))
        pinch_slope = (xD-y_feed_star)/(xD-zF)
        Rmin = pinch_slope/(1-pinch_slope)
        assert np.isclose(total_residual,0)
        assert np.isclose(component_residual,0)
        assert np.isclose(Rmin,h.minimum_reflux(zF,xD,alpha))
        print(f"D={D:.6f}; B={B:.6f} kmol/h")
        print(f"Total residual={total_residual:.3e} kmol/h; light-component residual={component_residual:.3e} kmol/h")
        print(f"Feed equilibrium y*={y_feed_star:.6f}; pinch slope={pinch_slope:.6f}; Rmin={Rmin:.6f}")
        plt.figure(figsize=(6,5))
        plt.plot(x,h.equilibrium(x,alpha),label='Equilibrium')
        plt.plot(x,x,color='grey',label='Diagonal')
        pinch_x = np.linspace(zF,xD,100)
        plt.plot(pinch_x,pinch_slope*pinch_x+xD/(Rmin+1),label='Pinched rectifying line')
        plt.scatter([zF,xD],[y_feed_star,xD],color='black')
        plt.axvline(zF,color='grey',linestyle=':',label='q=1 feed line')
        plt.xlabel('Liquid mole fraction x'); plt.ylabel('Vapour mole fraction y')
        plt.legend(); plt.grid(); plt.show()
        ''',
        r'''The total and light-component balances give D = 44.4444 and
B = 55.5556 kmol/h. For q = 1 the feed pinch is at the intersection of the
vertical feed line and equilibrium curve. The line from that point to
$(x_D,x_D)$ has slope $R_{min}/(R_{min}+1)$, giving Rmin = 1.35209.
At that reflux the operating and equilibrium curves meet at the feed pinch:
steps become arbitrarily small there, requiring infinitely many stages in
the ideal model. A finite stage count therefore requires R > Rmin.'''), (
        '''
        def distillation_steps(z, xd, xb, reflux, volatility=2.4, limit=300, inverse=None):
            if not 0 < xb < z < xd < 1 or volatility <= 1:
                raise ValueError("Invalid composition order or relative volatility")
            if inverse is None:
                if reflux <= h.minimum_reflux(z,xd,volatility):
                    raise ValueError("Reflux at or below minimum")
                inverse = lambda y: float(h.inverse_equilibrium(y,volatility))
            elif reflux < 0:
                raise ValueError("Negative reflux")
            # Lines derived here independently of the helper's stage counter.
            def rectifying(x_value):
                return reflux/(reflux+1)*x_value+xd/(reflux+1)
            feed_y = rectifying(z)
            strip_slope = (feed_y-xb)/(z-xb)
            def stripping(x_value):
                return strip_slope*(x_value-xb)+xb
            previous_x, y_value = xd, xd
            staircase, contacts = [(xd,xd)], []
            for n in range(1,limit+1):
                x_value = float(inverse(y_value))
                if not 0 <= x_value < previous_x-1e-12:
                    raise ValueError("Pinch, non-progress or composition outside physical bounds")
                staircase.append((x_value,y_value))
                section = 'rectifying' if x_value >= z else 'stripping'
                contacts.append((n,x_value,y_value,section))
                if x_value <= xb:
                    return n,np.array(staircase),contacts
                y_value = rectifying(x_value) if x_value >= z else stripping(x_value)
                if not 0 <= y_value <= 1:
                    raise ValueError("Operating line outside physical composition bounds")
                staircase.append((x_value,y_value))
                previous_x = x_value
            raise ValueError("Stage cap reached")

        N_ideal, staircase, contacts = distillation_steps(zF,xD,xB,R,alpha)
        assert N_ideal == h.stage_count(zF,xD,xB,R,alpha)[0]
        feed_switch = next(row[0] for row in contacts if row[3]=='stripping')
        print(f"Full ideal stages (partial reboiler included): {N_ideal}")
        print(f"Operating-line switch after equilibrium contact {feed_switch}")
        print("First three hand-checkable horizontal/vertical steps:")
        print("n     liquid x     entering y    following line")
        for n,liquid,vapour,section in contacts[:3]:
            print(f"{n}     {liquid:.6f}     {vapour:.6f}    {section}")
        fig,axes = plt.subplots(1,2,figsize=(12,5))
        for axis in axes:
            axis.plot(x,h.equilibrium(x,alpha),label='Equilibrium')
            axis.plot(x,x,color='grey',label='Diagonal')
            axis.plot(x[x>=zF],rect(x[x>=zF]),label='Rectifying')
            axis.plot(x[x<=zF],strip(x[x<=zF]),label='Stripping')
            axis.axvline(zF,color='grey',linestyle=':')
            axis.set(xlabel='Liquid mole fraction x',ylabel='Vapour mole fraction y')
            axis.grid()
        # First three explicit steps can be checked from the printed coordinates.
        axes[0].plot(staircase[:7,0],staircase[:7,1],'o-',color='black',label='First three steps')
        axes[0].set_title('Graphical check'); axes[0].legend()
        axes[1].plot(staircase[:,0],staircase[:,1],'o-',color='black',label='Full staircase')
        axes[1].set_title('Complete numerical solution'); axes[1].legend()
        plt.tight_layout(); plt.show()
        # Explicit rejection check at the limiting reflux.
        try:
            distillation_steps(zF,xD,xB,Rmin,alpha)
        except ValueError as error:
            print('Expected infeasible case:',error)
        else:
            raise AssertionError('Minimum reflux should be rejected')
        ''',
        '''The independent loop agrees with the helper at 11 full ideal stages.
The first three printed pairs can be reproduced by substituting y into the
inverse equilibrium relation and x into the rectifying line. When liquid x
first falls below zF, the next vertical move uses the stripping line. The last
horizontal step reaches or passes xB and is counted in full, so this is a
conservative integer result. The equilibrium partial reboiler is included;
the total condenser is excluded. The operating-line switch identifies the
feed region in this discrete construction, rather than a fully optimized
feed-tray location for a real column.'''), (
        '''
        ratios = np.linspace(1.1,3.0,60)
        sweep = []
        for ratio in ratios:
            candidate_R = ratio*Rmin
            try:
                stages = distillation_steps(zF,xD,xB,candidate_R,alpha)[0]
            except ValueError as error:
                print(f"R/Rmin={ratio:.3f}: infeasible or unresolved: {error}")
                stages = np.nan
            sweep.append((stages,(candidate_R+1)*D))
        sweep = np.array(sweep)
        fig,axes = plt.subplots(1,2,figsize=(11,4))
        axes[0].step(ratios,sweep[:,0],where='mid'); axes[0].set_ylabel('Full ideal stages / count')
        axes[1].plot(ratios,sweep[:,1]); axes[1].set_ylabel('Vapour load V / kmol h$^{-1}$')
        for axis in axes:
            axis.set_xlabel('R / Rmin'); axis.grid()
        plt.tight_layout(); plt.show()
        print("xD     D/kmol h-1   B/kmol h-1   Rmin      R      stages    V/kmol h-1")
        purity_results = []
        for candidate_xD in [.90,.95,.98]:
            candidate_D = F*(zF-xB)/(candidate_xD-xB)
            candidate_B = F-candidate_D
            candidate_min = h.minimum_reflux(zF,candidate_xD,alpha)
            candidate_R = 1.5*candidate_min
            candidate_N = distillation_steps(zF,candidate_xD,xB,candidate_R,alpha)[0]
            candidate_V = (candidate_R+1)*candidate_D
            purity_results.append((candidate_xD,candidate_D,candidate_B,candidate_min,candidate_R,candidate_N,candidate_V))
            assert np.isclose(candidate_D*candidate_xD+candidate_B*xB,F*zF)
            print(f"{candidate_xD:.2f}    {candidate_D:8.3f}      {candidate_B:8.3f}    {candidate_min:.4f}   {candidate_R:.4f}    {candidate_N:3d}      {candidate_V:8.3f}")
        ''',
        '''Higher reflux reduces required stages, with diminishing gains, while
the vapour-load proxy rises. Increasing xD at fixed R/Rmin requires both a
new balance and a new reflux: the distillate flow changes, so V cannot be
compared by holding D fixed. The table shows the integer stage response and
the vapour-load change. V is only a circulation proxy. Converting it into
utility duty requires latent heats and an energy balance; a monetary optimum
also needs column diameter, heat-transfer areas, utility prices and capital costs.'''), (
        '''
        ideal_trays = N_ideal-1
        tray_results = []
        print("Overall efficiency   installed trays   active height / m")
        for overall in [.50,.65,.80]:
            actual = int(np.ceil(ideal_trays/overall))
            active_height = .45*actual
            tray_results.append((overall,actual,active_height))
            print(f"{overall:.2f}                  {actual:2d}                {active_height:.2f}")
        assert N_ideal == 11 and tray_results[1][1] == 16
        ''',
        '''Ten ideal trays remain after subtracting the reboiler. At overall
efficiencies 0.50, 0.65 and 0.80 the estimates are 20, 16 and 13 installed
trays, with active heights 9.00, 7.20 and 5.85 m under the given convention.
Overall efficiency relates the total ideal-tray requirement to the actual
tray count. Murphree efficiency compares the composition change on an
individual tray with its equilibrium limit and cannot be substituted without
a tray-by-tray model. These active heights omit disengagement spaces, sumps,
feed and draw-off allowances, supports and the separate reboiler/condenser.''')],
    'recommendation': '''For the hypothetical binary mixture, I recommend carrying
forward the base reflux ratio of 2.5 as a provisional design case. It is above
the calculated minimum reflux ratio of 1.35209 and gives 11 full ideal stages
under the stated stepping convention. This is a reasonable case for further
design comparison, rather than a demonstrated economic optimum. The system
diagram identifies the feed, total condenser, reflux return, distillate and
partial reboiler, making the different balance boundaries explicit.

The overall and light-component balances give 44.4444 kmol/h of distillate
and 55.5556 kmol/h of bottoms. Both residuals are negligible numerically.
The independently implemented staircase agrees with the helper result, and
the first three horizontal and vertical moves are printed for hand checking.
The feed-line intersection determines the operating-line switch. The last
equilibrium contact is counted in full even when it overshoots the specified
bottoms composition, so the reported integer stage count is conservative.

The 11 ideal stages include the equilibrium partial reboiler and exclude the
total condenser. Subtracting the reboiler leaves ten ideal trays. Assuming an
overall tray efficiency of 0.65 gives 16 installed trays and an active-height
estimate of 7.2 m at 0.45 m spacing. This is not the full vessel height;
additional spaces and mechanical allowances are required. Changing efficiency
from 0.50 to 0.80 changes the estimate from 20 to 13 trays, showing that
efficiency information materially affects the equipment size.

The reflux sweep demonstrates a tradeoff: more reflux reduces stages while
increasing vapour circulation. Purity changes also alter distillate flow and
minimum reflux, so all balances must be recalculated. Vapour flow alone does
not measure actual energy cost or identify the cheapest design.

Before applying the design to a real mixture, obtain validated vapour–liquid
equilibrium data at the operating pressure and check for azeotropes. Confirm
feed thermal condition, latent heats and constant-molar-overflow validity.
Hydraulic sizing, tray efficiency, pressure drop, flooding margin, condenser
and reboiler duties, utility conditions and equipment costs remain necessary.
These data could change both the selected reflux ratio and the preferred
number of installed trays.''',
    'extension': (
        'No instructor equilibrium dataset is supplied in the lab. To make the '
        'method executable, the example below uses a clearly labelled synthetic '
        'table sampled from the existing constant-alpha model. Linear inverse '
        'interpolation is monotone and requires no additional dependency. This '
        'checks the data-driven workflow, not a real-mixture prediction. Replace '
        'the table with validated instructor data before drawing physical conclusions.',
        '''
        table_x = np.linspace(0,1,31)
        table_y = h.equilibrium(table_x,alpha)  # synthetic, not measured VLE
        assert np.all(np.diff(table_x)>0) and np.all(np.diff(table_y)>0)
        def table_inverse(y_value):
            if not table_y[0] <= y_value <= table_y[-1]:
                raise ValueError("Requested composition outside VLE table")
            return float(np.interp(y_value,table_y,table_x))
        tabulated_N,tabulated_steps,_ = distillation_steps(zF,xD,xB,R,alpha,inverse=table_inverse)
        print(f"Analytical VLE: {N_ideal} full stages; synthetic tabulated VLE: {tabulated_N}")
        print("For real data, recompute pinch/minimum reflux and check progress with the new equilibrium curve.")
        plt.figure(figsize=(6,5))
        plt.plot(table_x,table_y,'o',label='Synthetic VLE samples')
        plt.plot(staircase[:,0],staircase[:,1],label='Analytical staircase')
        plt.plot(tabulated_steps[:,0],tabulated_steps[:,1],'--',label='Interpolated staircase')
        plt.xlabel('Liquid mole fraction x'); plt.ylabel('Vapour mole fraction y')
        plt.legend(); plt.grid(); plt.show()
        ''')
}

SOLUTIONS['lab_04_absorption'] = {
    'prediction': 'Prediction: increasing solvent flow reduces the ideal-stage requirement, '
                  'but increases solvent handling. A larger equilibrium slope makes absorption '
                  'less favourable and increases the minimum solvent requirement.',
    'warmup': (
        'The higher solvent rate gives a larger rise in Y per contact when stepping '
        'from top to bottom. Both small cases reach Yin = 0.03 within three full '
        'contacts, although their intermediate compositions differ.',
        '''
        for warm_L in [300.,400.]:
            warm_min = 100*(.03-.002)/(.03/1.5)
            assert warm_L > warm_min
            warm_y, warm_n = .002, 0
            while warm_y < .03:
                if warm_n >= 300:
                    raise ValueError('Small-example stage cap')
                warm_x = warm_y/1.5
                warm_next = .002+warm_L/100*warm_x
                if warm_next <= warm_y:
                    raise ValueError('Non-progressing stage')
                warm_n += 1
                print(f"Ls={warm_L:.0f}, contact={warm_n}, X={warm_x:.6f}, next Y={warm_next:.6f}")
                warm_y = warm_next
        '''),
    'tasks': [(
        '''
        yin_fraction, yout_fraction = Yin/(1+Yin), Yout/(1+Yout)
        xout_ratio = Xin+Gs/Ls*(Yin-Yout)
        xout_fraction = xout_ratio/(1+xout_ratio)
        removed = Gs*(Yin-Yout)
        liquid_gain = Ls*(xout_ratio-Xin)
        gas_reduction_percent = (Yin-Yout)/Yin*100
        top_force = Yout-m*Xin
        bottom_force = Yin-m*xout_ratio
        derived_Lmin = Gs*(Yin-Yout)/(Yin/m-Xin)
        assert np.isclose(removed,liquid_gain)
        assert np.isclose(derived_Lmin,Lmin)
        assert min(top_force,bottom_force)>0
        print(f"Gas inlet mole fraction={yin_fraction:.6f}; outlet={yout_fraction:.6f}")
        print(f"Solvent outlet X={xout_ratio:.6f}; x={xout_fraction:.6f}")
        print(f"Solute removed={removed:.6f} kmol/h ({gas_reduction_percent:.1f}% of entering solute)")
        print(f"Solute-balance residual={removed-liquid_gain:.3e} kmol/h")
        print(f"Top driving force={top_force:.6f}; bottom={bottom_force:.6f}; Lmin={derived_Lmin:.3f} kmol/h")
        plt.figure(figsize=(6,5))
        plt.plot(X,m*X,label='Equilibrium')
        plt.plot(X,Yout+Ls/Gs*(X-Xin),label='Selected operating line')
        plt.plot(X,Yout+Lmin/Gs*(X-Xin),'--',label='Bottom-pinch operating line')
        plt.scatter([Xin,xout_ratio],[Yout,Yin],color='black',label='Actual end compositions')
        plt.xlabel('Liquid mole ratio X'); plt.ylabel('Gas mole ratio Y')
        plt.legend(); plt.grid(); plt.show()
        ''',
        r'''On a solute-free basis the entering and leaving solute flows are
$G_sY_{in}$ and $G_sY_{out}$. The solvent gains exactly their difference,
2.7 kmol/h, or 90% of the incoming solute. The actual gas mole fractions
are about 0.029126 and 0.002991, so percentage removal must use solute
flows rather than subtracting these fractions at assumed equal total flows.
The solvent outlet is X = 0.0133333, or x = 0.0131579. At the bottom
pinch, $X_{out}=Y_{in}/m$; substitution in the balance gives Lmin =
135 kmol/h. The selected 202.5 kmol/h exceeds it and gives positive
end driving forces of 0.003 at the top and 0.010 at the bottom.'''), (
        '''
        def absorption_steps(gas,liquid,gas_in,gas_out,liquid_in=0.,eq_slope=1.5,limit=300):
            if min(gas,liquid,eq_slope)<=0 or liquid_in<0:
                raise ValueError('Invalid flow, slope or solvent composition')
            if not gas_in>gas_out>eq_slope*liquid_in:
                raise ValueError('Infeasible absorption direction')
            minimum = gas*(gas_in-gas_out)/(gas_in/eq_slope-liquid_in)
            if liquid<=minimum:
                raise ValueError('Solvent flow at or below minimum')
            y_value = gas_out
            steps = [(liquid_in,y_value)]
            for n in range(1,limit+1):
                x_value = y_value/eq_slope
                steps.append((x_value,y_value))
                next_y = gas_out+liquid/gas*(x_value-liquid_in)
                steps.append((x_value,next_y))
                if next_y>=gas_in:
                    return n,np.array(steps)
                if next_y<=y_value+1e-12:
                    raise ValueError('Pinch or non-progressing stage')
                y_value = next_y
            raise ValueError('Stage cap reached')

        N_abs,abs_steps = absorption_steps(Gs,Ls,Yin,Yout,Xin,m)
        assert N_abs==h.stage_count(Gs,Ls,Yin,Yout,Xin,m)[0]
        # Independent fresh-solvent geometric-series check.
        absorption_factor = Ls/(m*Gs)
        analytic_n = next(n for n in range(1,301)
                          if Yout*sum(absorption_factor**k for k in range(n+1))>=Yin)
        assert analytic_n==N_abs
        print(f'Full ideal contacts={N_abs}; absorption factor={absorption_factor:.4f}')
        solvent_ratios = np.linspace(1.05,2.5,60)
        abs_counts = [absorption_steps(Gs,r*Lmin,Yin,Yout,Xin,m)[0] for r in solvent_ratios]
        fig,axes = plt.subplots(1,2,figsize=(12,5))
        axes[0].plot(X,m*X,label='Equilibrium')
        axes[0].plot(X,Yout+Ls/Gs*(X-Xin),label='Operating line')
        axes[0].plot(abs_steps[:,0],abs_steps[:,1],'o-',label='Staircase')
        axes[0].axhline(Yin,color='grey',linestyle=':',label='Gas inlet')
        axes[0].set(xlabel='Liquid mole ratio X',ylabel='Gas mole ratio Y'); axes[0].legend()
        axes[1].step(solvent_ratios,abs_counts,where='mid')
        axes[1].set(xlabel='Ls / Lmin',ylabel='Full ideal contacts / count')
        for axis in axes:
            axis.grid()
        plt.tight_layout(); plt.show()
        try:
            absorption_steps(Gs,Lmin,Yin,Yout,Xin,m)
        except ValueError as error:
            print('Expected pinch rejection:',error)
        else:
            raise AssertionError('Minimum solvent rate should be rejected')
        ''',
        r'''The independent recurrence, helper and fresh-solvent series all give
five full contacts. The final vertical move can overshoot Yin; retaining the
whole contact follows the conservative integer convention. At low solvent
rates near Lmin, the driving force is small and many contacts are needed.
Increasing solvent rate reduces contacts but raises solvent handling and
possibly regeneration costs. The staircase is an equilibrium model, not a
hydraulic or mass-transfer-rate calculation.'''), (
        '''
        installed_trays = int(np.ceil(N_abs/.60))
        tray_height = installed_trays*.45
        hetp_values = np.linspace(.6,1.2,25)
        packed_heights = N_abs*hetp_values
        cross_section, gas_volume = 1.,.8
        superficial_velocity = gas_volume/cross_section
        dry_gradient = h.ergun_gradient(superficial_velocity,.70,.025,1.2,1.8e-5)
        dry_pressure_drop = dry_gradient*packed_heights
        print(f'Tray option: {installed_trays} trays, active height={tray_height:.2f} m')
        print(f'Packing option: active height={packed_heights.min():.2f}–{packed_heights.max():.2f} m')
        print(f'Superficial gas velocity={superficial_velocity:.3f} m/s')
        print(f'Dry Ergun gradient={dry_gradient:.6f} Pa/m; dry drop={dry_pressure_drop.min():.2f}–{dry_pressure_drop.max():.2f} Pa')
        assert np.isclose(h.ergun_gradient(0,.70,.025),0)
        fig,axes = plt.subplots(1,2,figsize=(11,4))
        axes[0].plot(hetp_values,packed_heights,label='Packing')
        axes[0].axhline(tray_height,linestyle=':',color='black',label='Tray active height'); axes[0].legend()
        axes[0].set(xlabel='Assumed HETP / m',ylabel='Active height / m')
        axes[1].plot(packed_heights,dry_pressure_drop)
        axes[1].set(xlabel='Packed height / m',ylabel='Illustrative dry pressure drop / Pa')
        for axis in axes:
            axis.grid()
        plt.tight_layout(); plt.show()
        ''',
        '''The tray option gives nine trays and 4.05 m active height. The
packing option gives 3–6 m using an independent HETP assumption; tray
efficiency is not applied to packing. The supplied 1 m² area gives 0.8 m/s
superficial gas velocity and about 47.93 Pa/m in the dry Ergun model,
or 144–288 Pa across the active packed height. These pressure drops exclude
distributors and other internals. Treating irrigated industrial packing as
dry equivalent particles omits liquid holdup and packing geometry effects,
so the result is an illustration, not an operating pressure-drop prediction.'''), (
        '''
        robustness = []
        print('m       Lmin/kmol h-1   Ls/Lmin   full contacts   status')
        for candidate_m in [.8*m,m,1.2*m]:
            candidate_min = Gs*(Yin-Yout)/(Yin/candidate_m-Xin)
            if Ls<=candidate_min:
                robustness.append((candidate_m,candidate_min,np.nan))
                print(f'{candidate_m:.3f}   {candidate_min:10.3f}    {Ls/candidate_min:.3f}       --       infeasible')
                continue
            candidate_N = absorption_steps(Gs,Ls,Yin,Yout,Xin,candidate_m)[0]
            robustness.append((candidate_m,candidate_min,candidate_N))
            print(f'{candidate_m:.3f}   {candidate_min:10.3f}    {Ls/candidate_min:.3f}       {candidate_N:2d}       feasible')
        # Also show that the same fixed-flow calculation rejects a true infeasible case.
        infeasible_m = 2.5
        infeasible_min = Gs*(Yin-Yout)/(Yin/infeasible_m-Xin)
        assert Ls<=infeasible_min
        print(f'Illustrative infeasible check: m={infeasible_m}, Lmin={infeasible_min:.2f} > Ls={Ls:.2f}')
        robust_array = np.array(robustness)
        plt.figure(figsize=(6,4))
        plt.plot(robust_array[:,0],robust_array[:,2],'o-')
        plt.xlabel('Equilibrium slope m / dimensionless'); plt.ylabel('Full ideal contacts / count')
        plt.grid(); plt.show()
        ''',
        '''All three requested ±20% cases remain feasible at fixed solvent flow,
but the stage requirement increases as equilibrium becomes less favourable.
Recomputing Lmin is necessary even when Ls is unchanged. A sufficiently
large slope would make the same solvent rate infeasible, as the extra check
demonstrates. Dry Ergun has no liquid-loading variable or flooding criterion;
it cannot predict liquid holdup, wet pressure drop or flooding. Obtain vendor
wet pressure-drop/capacity curves, packing-specific HETP or transfer data,
liquid properties and loads, surface tension, distribution limits and a
recommended flooding margin before designing a real packed absorber.''')],
    'recommendation': '''I recommend retaining the base solvent rate of
202.5 kmol/h for preliminary comparison of absorber internals. It is
1.5 times the minimum rate of 135 kmol/h and achieves the specified
90% solute removal with five full ideal contacts in the assumed linear,
isothermal equilibrium model. The diagram shows gas entering from below
and lean solvent entering from above; the balance uses solute-free carrier
and solvent flow rates rather than total mixture flows.

The removed solute is 2.7 kmol/h, matching the calculated liquid gain.
The rich-solvent outlet ratio is 0.0133333, equivalent to a mole fraction
of 0.0131579. Both terminal driving forces are positive. The independently
implemented recurrence agrees with the helper and with the fresh-solvent
geometric-series result. The last stage is counted in full even when its
step overshoots the specified gas-inlet ratio, consistent with the lab's
integer counting rule.

For the tray option, an overall efficiency of 0.60 gives nine installed
trays and 4.05 m active height using the stated spacing. For the packing
option, an assumed HETP of 0.6–1.2 m gives 3–6 m active height. These
are alternative equipment models; tray efficiency should not be applied
on top of HETP. The information supplied does not justify choosing one
internals type on economic or hydraulic grounds.

The dry-bed calculation gives about 47.93 Pa/m at 0.8 m/s superficial
gas velocity. It demonstrates how geometry and gas flow enter an Ergun
screening calculation, but cannot establish wet operating pressure drop
or flooding margin. Liquid loading, holdup, distributor performance and
actual packing geometry are absent.

The equilibrium-slope sensitivity remains feasible across the requested
range, although the contact requirement changes. Increasing solvent flow
could reduce contacts, but it would also raise circulation and possible
regeneration demand. Before fixing height or diameter, obtain validated
equilibrium data at operating conditions and assess heat effects. Obtain
vendor capacity and wet pressure-drop correlations, packing-specific
mass-transfer performance or HETP, and tray-efficiency data if trays remain
an option. A complete design must also include distributors, disengagement
space, hydraulic margins and solvent handling. The present results support
a preliminary comparison rather than an equipment specification.''',
    'extension': (
        r'''For an overall gas-phase transfer-unit model on the same solute-free
basis, $N_{OG}=\int_{Yout}^{Yin}dY/(Y-Y^*(X(Y)))$, where
$X(Y)=X_{in}+(G_s/L_s)(Y-Yout)$ and $Y^*=mX$.
The integral depends on the same equilibrium/operating lines but does not
equal the number of ideal stages. A continuous model gives $Z=H_{OG}N_{OG}$.
With a coefficient defined by $d\dot n_A=K_Y a(Y-Y^*)dV$,
$H_{OG}=G'_s/(K_Y a)$ using consistent time/area/volume units.
Additional data are gas and liquid film coefficients or an overall coefficient,
effective wetted interfacial area, phase properties and loading dependence.
The HOG below is illustrative, not inferred from HETP or the equilibrium curve.''',
        '''
        gas_ratios = np.linspace(Yout,Yin,10001)
        liquid_ratios = Xin+Gs/Ls*(gas_ratios-Yout)
        transfer_force = gas_ratios-m*liquid_ratios
        assert np.all(transfer_force>0)
        integrate = getattr(np,'trapezoid',None)
        if integrate is None:
            integrate = np.trapz
        NOG = integrate(1/transfer_force,gas_ratios)
        illustrative_HOG = .8  # m; synthetic transfer-unit height, not HETP
        transfer_height = illustrative_HOG*NOG
        print(f'Overall gas transfer units NOG={NOG:.6f}; assumed HOG={illustrative_HOG:.2f} m')
        print(f'Illustrative rate-model height={transfer_height:.4f} m; ideal contacts={N_abs}')
        # Independent analytical integral for the linear force aY+b.
        force_slope = 1-m*Gs/Ls
        if abs(force_slope)>1e-12:
            analytic_NOG = np.log(transfer_force[-1]/transfer_force[0])/force_slope
        else:
            analytic_NOG = (Yin-Yout)/transfer_force[0]
        assert np.isclose(NOG,analytic_NOG,rtol=1e-7)
        ''')
}
