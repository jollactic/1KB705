"""Supplied student analysis code; no written model answers.

Used by the design-focused notebook builder. Students run these cells as supplied.
"""

CALCULATIONS = {'lab_01_flow': ['\n'
                 '        trial_q = .003\n'
                 '        velocity = 4*trial_q/(np.pi*diameter**2)\n'
                 '        reynolds = rho*velocity*diameter/mu\n'
                 '        # Independent evaluation of the stated Haaland correlation.\n'
                 '        darcy_f = (-1.8*np.log10((roughness/diameter/3.7)**1.11 + 6.9/reynolds))**-2\n'
                 '        pipe_loss = darcy_f*length/diameter*velocity**2/(2*g)\n'
                 '        fitting_loss = K*velocity**2/(2*g)\n'
                 '        hand_head = rise + pipe_loss + fitting_loss\n'
                 '        reference_head = float(h.system_head(trial_q, diameter, length, rise, roughness, '
                 'K, rho, mu))\n'
                 '        assert np.isclose(hand_head, reference_head)\n'
                 '        print(f"v = {velocity:.6f} m/s; Re = {reynolds:.1f}; f_D = {darcy_f:.6f}")\n'
                 '        print(f"Pipe = {pipe_loss:.6f} m; fittings = {fitting_loss:.6f} m; total = '
                 '{hand_head:.6f} m")\n'
                 '        print(f"Equivalent pressure rise = {rho*g*hand_head/1000:.3f} kPa")\n'
                 '        print(f"Helper mismatch = {hand_head-reference_head:.3e} m; zero-flow limit = '
                 '{rise:.1f} m")\n'
                 '        ',
                 '\n'
                 '        def bisect_root(function, low, high, tolerance=1e-6, max_iterations=200):\n'
                 '            f_low, f_high = function(low), function(high)\n'
                 '            if f_low == 0:\n'
                 '                return low\n'
                 '            if f_high == 0:\n'
                 '                return high\n'
                 '            if not np.isfinite([f_low, f_high]).all() or f_low*f_high > 0:\n'
                 '                raise ValueError("A finite sign-changing bracket is required")\n'
                 '            for iteration in range(max_iterations):\n'
                 '                mid = (low+high)/2\n'
                 '                f_mid = function(mid)\n'
                 '                if not np.isfinite(f_mid):\n'
                 '                    raise ValueError("Nonfinite residual")\n'
                 '                if abs(f_mid) < tolerance:\n'
                 '                    return mid\n'
                 '                if f_low*f_mid < 0:\n'
                 '                    high = mid\n'
                 '                else:\n'
                 '                    low, f_low = mid, f_mid\n'
                 '            raise ValueError("Bisection did not converge")\n'
                 '\n'
                 '        def operating_point(D, speed=1.0, eps=roughness, eta=efficiency):\n'
                 '            if not 0 < eta <= 1:\n'
                 '                raise ValueError("Efficiency must lie in (0, 1]")\n'
                 '            def residual(q):\n'
                 '                return float(h.pump_head(q, H0, a, speed) -\n'
                 '                             h.system_head(q, D, length, rise, eps, K, rho, mu))\n'
                 '            # Lower end remains turbulent for every D in this exercise.\n'
                 '            low, high = .001, speed*np.sqrt(H0/a)\n'
                 '            flow = bisect_root(residual, low, high)\n'
                 '            head = float(h.pump_head(flow, H0, a, speed))\n'
                 '            shaft = rho*g*flow*head/eta\n'
                 '            assert abs(residual(flow)) < .001\n'
                 '            return flow, head, shaft, shaft/flow/3.6e6  # m³/s, m, W, kWh/m³\n'
                 '\n'
                 '        base_q, base_h, base_power, base_specific = operating_point(diameter)\n'
                 '        assert base_q >= .003\n'
                 '        print(f"Operating flow = {base_q*1000:.6f} L/s; head = {base_h:.6f} m")\n'
                 '        print(f"Shaft power = {base_power:.3f} W; annual energy = '
                 '{base_power/1000*4000:.2f} kWh")\n'
                 '        print(f"Specific energy = {base_specific:.6f} kWh/m³")\n'
                 '        plt.figure(figsize=(7, 4))\n'
                 '        plt.plot(Q*1000, system, label="System")\n'
                 '        plt.plot(Q*1000, h.pump_head(Q, H0, a), label="Pump")\n'
                 '        plt.scatter([base_q*1000], [base_h], color="black", label="Operating point")\n'
                 '        plt.xlabel("Flow / L s$^{-1}$"); plt.ylabel("Head / m"); plt.legend(); plt.grid(); '
                 'plt.show()\n'
                 '        ',
                 '\n'
                 '        designs = []\n'
                 '        print("D / m  speed   flow / L/s  shaft / W  kWh/m³     >=3 L/s")\n'
                 '        for D in [.050, .065, .080]:\n'
                 '            for speed in [.8, 1.0, 1.1]:\n'
                 '                flow, head, power, specific = operating_point(D, speed)\n'
                 '                designs.append((D, speed, flow, head, power, specific))\n'
                 '                print(f"{D:.3f}   {speed:.1f}     {flow*1000:8.4f}   {power:8.2f}  '
                 '{specific:.6f}   {flow >= .003}")\n'
                 '        feasible_designs = [row for row in designs if row[2] >= .003]\n'
                 '        selected = min(feasible_designs, key=lambda row: row[5])\n'
                 '        chosen_D, chosen_speed = selected[:2]\n'
                 '        print(f"Lowest specific-energy feasible candidate: D={chosen_D:.3f} m, '
                 'speed={chosen_speed:.1f}")\n'
                 '        fig, axes = plt.subplots(1, 2, figsize=(11, 4))\n'
                 '        for D in [.050, .065, .080]:\n'
                 '            rows = np.array([row for row in designs if row[0] == D])\n'
                 '            axes[0].plot(rows[:, 1], rows[:, 2]*1000, \'o-\', label=f"D={D:.3f} m")\n'
                 '            axes[1].plot(rows[:, 1], rows[:, 5], \'o-\', label=f"D={D:.3f} m")\n'
                 "        axes[0].axhline(3, color='black', linestyle=':', label='Required flow')\n"
                 '        axes[0].set_ylabel("Operating flow / L s$^{-1}$")\n'
                 '        axes[1].set_ylabel("Specific energy / kWh m$^{-3}$")\n'
                 '        for axis in axes:\n'
                 '            axis.set_xlabel("Speed ratio / dimensionless"); axis.legend(); axis.grid()\n'
                 '        plt.tight_layout(); plt.show()\n'
                 '        ',
                 '\n'
                 '        roughness_values = np.unique(np.r_[np.linspace(1e-6, 2e-4, 25), roughness])\n'
                 '        eta_values = np.unique(np.r_[np.linspace(.55, .80, 25), efficiency])\n'
                 '        rough_results = np.array([operating_point(chosen_D, chosen_speed, eps=value)\n'
                 '                                  for value in roughness_values])\n'
                 '        eta_results = np.array([operating_point(chosen_D, chosen_speed, eta=value)\n'
                 '                                for value in eta_values])\n'
                 '        fig, axes = plt.subplots(1, 3, figsize=(13, 4))\n'
                 '        axes[0].plot(roughness_values*1e6, rough_results[:, 0]*1000)\n'
                 "        axes[0].axhline(3, color='black', linestyle=':')\n"
                 '        axes[0].set(xlabel="Roughness / µm", ylabel="Operating flow / L s$^{-1}$")\n'
                 '        axes[1].plot(roughness_values*1e6, rough_results[:, 3])\n'
                 '        axes[1].set(xlabel="Roughness / µm", ylabel="Specific energy / kWh m$^{-3}$")\n'
                 '        axes[2].plot(eta_values, eta_results[:, 3])\n'
                 '        axes[2].set(xlabel="Efficiency / dimensionless", ylabel="Specific energy / kWh '
                 'm$^{-3}$")\n'
                 '        for axis in axes:\n'
                 '            axis.grid()\n'
                 '        plt.tight_layout(); plt.show()\n'
                 '        rough_change = (rough_results[:, 3].max()/rough_results[:, 3].min()-1)*100\n'
                 '        eta_change = (eta_results[:, 3].max()/eta_results[:, 3].min()-1)*100\n'
                 '        print(f"Specific-energy span: roughness {rough_change:.2f}%; efficiency '
                 '{eta_change:.2f}% (max/min - 1)")\n'
                 '        print(f"Minimum flow across roughness sweep: {rough_results[:,0].min()*1000:.4f} '
                 'L/s")\n'
                 '        assert np.allclose(eta_results[:, 0], eta_results[0, 0])\n'
                 '        # Check all designs at worst roughness before declaring a robust candidate.\n'
                 '        robust = [row for row in designs if operating_point(row[0], row[1], eps=2e-4)[0] '
                 '>= .003]\n'
                 '        robust_choice = min(robust, key=lambda row: row[5])\n'
                 '        print(f"Robust to stated roughness range: D={robust_choice[0]:.3f} m, '
                 'speed={robust_choice[1]:.1f}")\n'
                 '        '],
 'lab_02_heat': ['\n'
                 '        cold_duty = mc*cpc*(Tco_target-Tci)\n'
                 '        independent_hot_out = Thi-cold_duty/(mh*cph)\n'
                 '        dt1, dt2 = Thi-Tco_target, independent_hot_out-Tci\n'
                 '        independent_lmtd = (dt1-dt2)/np.log(dt1/dt2)\n'
                 '        independent_area = cold_duty/(U_clean*independent_lmtd)\n'
                 '        qmax = min(Ch, Cc)*(Thi-Tci)\n'
                 '        effectiveness = cold_duty/qmax\n'
                 '        energy_residual = Ch*(Thi-independent_hot_out)-cold_duty\n'
                 '        assert np.isclose(independent_area, area)\n'
                 '        assert abs(energy_residual) < 1e-8\n'
                 '        print(f"Duty = {cold_duty/1000:.3f} kW; hot outlet = {independent_hot_out:.4f} '
                 '°C")\n'
                 '        print(f"Area = {independent_area:.5f} m²; Qmax = {qmax/1000:.3f} kW; effectiveness '
                 '= {effectiveness:.6f}")\n'
                 '        print(f"Balance residual = {energy_residual:.3e} W; terminal differences = '
                 '{dt1:.3f}, {dt2:.3f} K")\n'
                 '        plt.figure(figsize=(7,4))\n'
                 "        plt.plot([0,1], [Thi, independent_hot_out], 'o-', label='Hot stream →')\n"
                 "        plt.plot([0,1], [Tco_target, Tci], 'o-', label='Cold stream ←')\n"
                 "        plt.xticks([0,1], ['Hot inlet / cold outlet', 'Hot outlet / cold inlet'])\n"
                 "        plt.ylabel('Temperature / °C'); plt.title('Terminal temperatures — schematic "
                 "connections only')\n"
                 '        plt.legend(); plt.grid(); plt.show()\n'
                 '        ',
                 '\n'
                 '        def effectiveness_own(ntu, cr):\n'
                 '            if ntu < 0 or not 0 <= cr <= 1:\n'
                 '                raise ValueError("Require NTU >= 0 and 0 <= Cr <= 1")\n'
                 '            if abs(1-cr) < 1e-10:\n'
                 '                return ntu/(1+ntu)\n'
                 '            numerator = -np.expm1(-ntu*(1-cr))\n'
                 '            return numerator/((1-cr)+cr*numerator)\n'
                 '\n'
                 '        def predict_outlets(UA, hot_capacity=Ch, cold_capacity=Cc):\n'
                 '            cmin, cmax = min(hot_capacity, cold_capacity), max(hot_capacity, '
                 'cold_capacity)\n'
                 '            eps = effectiveness_own(UA/cmin, cmin/cmax)\n'
                 '            q = eps*cmin*(Thi-Tci)\n'
                 '            return Thi-q/hot_capacity, Tci+q/cold_capacity, q\n'
                 '\n'
                 '        ntu, cr = U_clean*area/min(Ch,Cc), min(Ch,Cc)/max(Ch,Cc)\n'
                 '        recovered_hot, recovered_cold, recovered_duty = predict_outlets(U_clean*area)\n'
                 '        assert np.allclose([recovered_hot, recovered_cold, recovered_duty], '
                 '[Tho,Tco_target,duty])\n'
                 '        assert np.isclose(effectiveness_own(2,1), 2/3)\n'
                 '        assert np.isclose(effectiveness_own(1e-9,.5), 1e-9, rtol=1e-6, atol=1e-15)\n'
                 '        assert np.isclose(effectiveness_own(100,.5), 1)\n'
                 '        assert np.isclose(effectiveness_own(0,.5), 0)\n'
                 '        for test_ntu in [0, 1e-9, 1, 100]:\n'
                 '            for test_cr in [.5, 1.0]:\n'
                 '                assert np.isclose(effectiveness_own(test_ntu,test_cr), '
                 'h.countercurrent_effectiveness(test_ntu,test_cr))\n'
                 '        print(f"NTU = {ntu:.6f}; Cr = {cr:.6f}; hot outlet = {recovered_hot:.4f} °C; cold '
                 'outlet = {recovered_cold:.4f} °C")\n'
                 '        print("Zero, small/large NTU, equal-capacity and helper comparisons passed")\n'
                 '        ',
                 '\n'
                 '        resistance = np.unique(np.r_[np.linspace(0,.001,60), .0006])\n'
                 '        fouled_U = 1/(1/U_clean+resistance)\n'
                 '        fixed_area_results = np.array([h.outlets(u*area, Ch, Cc, Thi, Tci) for u in '
                 'fouled_U])\n'
                 '        design_R = .0006\n'
                 '        design_U = 1/(1/U_clean+design_R)\n'
                 '        fouled_sized_area = duty/(design_U*delta_lm)\n'
                 '        at_design = h.outlets(design_U*area, Ch,Cc,Thi,Tci)\n'
                 '        enlarged_design = h.outlets(design_U*fouled_sized_area, Ch,Cc,Thi,Tci)\n'
                 '        enlarged_clean = h.outlets(U_clean*fouled_sized_area, Ch,Cc,Thi,Tci)\n'
                 '        assert np.isclose(enlarged_design[1],55)\n'
                 '        print(f"At design fouling: U={design_U:.3f} W/(m² K)")\n'
                 '        print(f"Clean-sized area={area:.4f} m²: Tco={at_design[1]:.4f} °C, '
                 'duty={at_design[2]/1000:.3f} kW")\n'
                 '        print(f"Fouling-sized area={fouled_sized_area:.4f} m²: '
                 'Tco={enlarged_design[1]:.4f} °C")\n'
                 '        print(f"When clean, enlarged unit gives Tco={enlarged_clean[1]:.4f} °C: allow for '
                 'control")\n'
                 '        fig, axes = plt.subplots(1,2,figsize=(11,4))\n'
                 '        axes[0].plot(resistance*1e4, fixed_area_results[:,2]/1000)\n'
                 "        axes[0].set_ylabel('Recovered duty / kW')\n"
                 '        axes[1].plot(resistance*1e4, fixed_area_results[:,1])\n'
                 "        axes[1].axhline(55,color='black',linestyle=':', label='Target'); axes[1].legend()\n"
                 "        axes[1].set_ylabel('Cold outlet / °C')\n"
                 '        for axis in axes:\n'
                 "            axis.set_xlabel('Added resistance / (10$^{-4}$ m² K W$^{-1}$)'); axis.grid()\n"
                 '        plt.tight_layout(); plt.show()\n'
                 '        ',
                 '\n'
                 '        cold_flows = np.unique(np.r_[np.linspace(.5,1.8,60),mc])\n'
                 '        # Chosen design: fouling-sized area, operated at design fouling resistance.\n'
                 '        flow_results = '
                 'np.array([h.outlets(design_U*fouled_sized_area,Ch,value*cpc,Thi,Tci)\n'
                 '                                 for value in cold_flows])\n'
                 '        fig, axes = plt.subplots(1,2,figsize=(11,4))\n'
                 "        axes[0].plot(cold_flows,flow_results[:,1]); axes[0].set_ylabel('Cold outlet / "
                 "°C')\n"
                 "        axes[1].plot(cold_flows,flow_results[:,2]/1000); axes[1].set_ylabel('Recovered "
                 "duty / kW')\n"
                 '        for axis in axes:\n'
                 "            axis.set_xlabel('Cold mass flow / kg s$^{-1}$'); axis.grid()\n"
                 '        plt.tight_layout(); plt.show()\n'
                 '        for index in [0,-1]:\n'
                 '            print(f"mc={cold_flows[index]:.2f} kg/s: Tco={flow_results[index,1]:.3f} °C, '
                 'duty={flow_results[index,2]/1000:.3f} kW")\n'
                 '        assert np.allclose(Ch*(Thi-flow_results[:,0]), '
                 'cold_flows*cpc*(flow_results[:,1]-Tci))\n'
                 '        '],
 'lab_03_distillation': ['\n'
                         '        D = F*(zF-xB)/(xD-xB)\n'
                         '        B = F-D\n'
                         '        total_residual = F-D-B\n'
                         '        component_residual = F*zF-D*xD-B*xB\n'
                         '        y_feed_star = float(h.equilibrium(zF,alpha))\n'
                         '        pinch_slope = (xD-y_feed_star)/(xD-zF)\n'
                         '        Rmin = pinch_slope/(1-pinch_slope)\n'
                         '        assert np.isclose(total_residual,0)\n'
                         '        assert np.isclose(component_residual,0)\n'
                         '        assert np.isclose(Rmin,h.minimum_reflux(zF,xD,alpha))\n'
                         '        print(f"D={D:.6f}; B={B:.6f} kmol/h")\n'
                         '        print(f"Total residual={total_residual:.3e} kmol/h; light-component '
                         'residual={component_residual:.3e} kmol/h")\n'
                         '        print(f"Feed equilibrium y*={y_feed_star:.6f}; pinch '
                         'slope={pinch_slope:.6f}; Rmin={Rmin:.6f}")\n'
                         '        plt.figure(figsize=(6,5))\n'
                         "        plt.plot(x,h.equilibrium(x,alpha),label='Equilibrium')\n"
                         "        plt.plot(x,x,color='grey',label='Diagonal')\n"
                         '        pinch_x = np.linspace(zF,xD,100)\n'
                         "        plt.plot(pinch_x,pinch_slope*pinch_x+xD/(Rmin+1),label='Pinched rectifying "
                         "line')\n"
                         "        plt.scatter([zF,xD],[y_feed_star,xD],color='black')\n"
                         "        plt.axvline(zF,color='grey',linestyle=':',label='q=1 feed line')\n"
                         "        plt.xlabel('Liquid mole fraction x'); plt.ylabel('Vapour mole fraction "
                         "y')\n"
                         '        plt.legend(); plt.grid(); plt.show()\n'
                         '        ',
                         '\n'
                         '        def distillation_steps(z, xd, xb, reflux, volatility=2.4, limit=300, '
                         'inverse=None):\n'
                         '            if not 0 < xb < z < xd < 1 or volatility <= 1:\n'
                         '                raise ValueError("Invalid composition order or relative '
                         'volatility")\n'
                         '            if inverse is None:\n'
                         '                if reflux <= h.minimum_reflux(z,xd,volatility):\n'
                         '                    raise ValueError("Reflux at or below minimum")\n'
                         '                inverse = lambda y: float(h.inverse_equilibrium(y,volatility))\n'
                         '            elif reflux < 0:\n'
                         '                raise ValueError("Negative reflux")\n'
                         "            # Lines derived here independently of the helper's stage counter.\n"
                         '            def rectifying(x_value):\n'
                         '                return reflux/(reflux+1)*x_value+xd/(reflux+1)\n'
                         '            feed_y = rectifying(z)\n'
                         '            strip_slope = (feed_y-xb)/(z-xb)\n'
                         '            def stripping(x_value):\n'
                         '                return strip_slope*(x_value-xb)+xb\n'
                         '            previous_x, y_value = xd, xd\n'
                         '            staircase, contacts = [(xd,xd)], []\n'
                         '            for n in range(1,limit+1):\n'
                         '                x_value = float(inverse(y_value))\n'
                         '                if not 0 <= x_value < previous_x-1e-12:\n'
                         '                    raise ValueError("Pinch, non-progress or composition outside '
                         'physical bounds")\n'
                         '                staircase.append((x_value,y_value))\n'
                         "                section = 'rectifying' if x_value >= z else 'stripping'\n"
                         '                contacts.append((n,x_value,y_value,section))\n'
                         '                if x_value <= xb:\n'
                         '                    return n,np.array(staircase),contacts\n'
                         '                y_value = rectifying(x_value) if x_value >= z else '
                         'stripping(x_value)\n'
                         '                if not 0 <= y_value <= 1:\n'
                         '                    raise ValueError("Operating line outside physical composition '
                         'bounds")\n'
                         '                staircase.append((x_value,y_value))\n'
                         '                previous_x = x_value\n'
                         '            raise ValueError("Stage cap reached")\n'
                         '\n'
                         '        N_ideal, staircase, contacts = distillation_steps(zF,xD,xB,R,alpha)\n'
                         '        assert N_ideal == h.stage_count(zF,xD,xB,R,alpha)[0]\n'
                         "        feed_switch = next(row[0] for row in contacts if row[3]=='stripping')\n"
                         '        print(f"Full ideal stages (partial reboiler included): {N_ideal}")\n'
                         '        print(f"Operating-line switch after equilibrium contact {feed_switch}")\n'
                         '        print("First three hand-checkable horizontal/vertical steps:")\n'
                         '        print("n     liquid x     entering y    following line")\n'
                         '        for n,liquid,vapour,section in contacts[:3]:\n'
                         '            print(f"{n}     {liquid:.6f}     {vapour:.6f}    {section}")\n'
                         '        fig,axes = plt.subplots(1,2,figsize=(12,5))\n'
                         '        for axis in axes:\n'
                         "            axis.plot(x,h.equilibrium(x,alpha),label='Equilibrium')\n"
                         "            axis.plot(x,x,color='grey',label='Diagonal')\n"
                         "            axis.plot(x[x>=zF],rect(x[x>=zF]),label='Rectifying')\n"
                         "            axis.plot(x[x<=zF],strip(x[x<=zF]),label='Stripping')\n"
                         "            axis.axvline(zF,color='grey',linestyle=':')\n"
                         "            axis.set(xlabel='Liquid mole fraction x',ylabel='Vapour mole fraction "
                         "y')\n"
                         '            axis.grid()\n'
                         '        # First three explicit steps can be checked from the printed coordinates.\n'
                         '        '
                         "axes[0].plot(staircase[:7,0],staircase[:7,1],'o-',color='black',label='First three "
                         "steps')\n"
                         "        axes[0].set_title('Graphical check'); axes[0].legend()\n"
                         "        axes[1].plot(staircase[:,0],staircase[:,1],'o-',color='black',label='Full "
                         "staircase')\n"
                         "        axes[1].set_title('Complete numerical solution'); axes[1].legend()\n"
                         '        plt.tight_layout(); plt.show()\n'
                         '        # Explicit rejection check at the limiting reflux.\n'
                         '        try:\n'
                         '            distillation_steps(zF,xD,xB,Rmin,alpha)\n'
                         '        except ValueError as error:\n'
                         "            print('Expected infeasible case:',error)\n"
                         '        else:\n'
                         "            raise AssertionError('Minimum reflux should be rejected')\n"
                         '        ',
                         '\n'
                         '        ratios = np.linspace(1.1,3.0,60)\n'
                         '        sweep = []\n'
                         '        for ratio in ratios:\n'
                         '            candidate_R = ratio*Rmin\n'
                         '            try:\n'
                         '                stages = distillation_steps(zF,xD,xB,candidate_R,alpha)[0]\n'
                         '            except ValueError as error:\n'
                         '                print(f"R/Rmin={ratio:.3f}: infeasible or unresolved: {error}")\n'
                         '                stages = np.nan\n'
                         '            sweep.append((stages,(candidate_R+1)*D))\n'
                         '        sweep = np.array(sweep)\n'
                         '        fig,axes = plt.subplots(1,2,figsize=(11,4))\n'
                         "        axes[0].step(ratios,sweep[:,0],where='mid'); axes[0].set_ylabel('Full "
                         "ideal stages / count')\n"
                         "        axes[1].plot(ratios,sweep[:,1]); axes[1].set_ylabel('Vapour load V / kmol "
                         "h$^{-1}$')\n"
                         '        for axis in axes:\n'
                         "            axis.set_xlabel('R / Rmin'); axis.grid()\n"
                         '        plt.tight_layout(); plt.show()\n'
                         '        print("xD     D/kmol h-1   B/kmol h-1   Rmin      R      stages    V/kmol '
                         'h-1")\n'
                         '        purity_results = []\n'
                         '        for candidate_xD in [.90,.95,.98]:\n'
                         '            candidate_D = F*(zF-xB)/(candidate_xD-xB)\n'
                         '            candidate_B = F-candidate_D\n'
                         '            candidate_min = h.minimum_reflux(zF,candidate_xD,alpha)\n'
                         '            candidate_R = 1.5*candidate_min\n'
                         '            candidate_N = '
                         'distillation_steps(zF,candidate_xD,xB,candidate_R,alpha)[0]\n'
                         '            candidate_V = (candidate_R+1)*candidate_D\n'
                         '            '
                         'purity_results.append((candidate_xD,candidate_D,candidate_B,candidate_min,candidate_R,candidate_N,candidate_V))\n'
                         '            assert np.isclose(candidate_D*candidate_xD+candidate_B*xB,F*zF)\n'
                         '            print(f"{candidate_xD:.2f}    {candidate_D:8.3f}      '
                         '{candidate_B:8.3f}    {candidate_min:.4f}   {candidate_R:.4f}    '
                         '{candidate_N:3d}      {candidate_V:8.3f}")\n'
                         '        ',
                         '\n'
                         '        ideal_trays = N_ideal-1\n'
                         '        tray_results = []\n'
                         '        print("Overall efficiency   installed trays   active height / m")\n'
                         '        for overall in [.50,.65,.80]:\n'
                         '            actual = int(np.ceil(ideal_trays/overall))\n'
                         '            active_height = .45*actual\n'
                         '            tray_results.append((overall,actual,active_height))\n'
                         '            print(f"{overall:.2f}                  {actual:2d}                '
                         '{active_height:.2f}")\n'
                         '        assert N_ideal == 11 and tray_results[1][1] == 16\n'
                         '        '],
 'lab_04_absorption': ['\n'
                       '        yin_fraction, yout_fraction = Yin/(1+Yin), Yout/(1+Yout)\n'
                       '        xout_ratio = Xin+Gs/Ls*(Yin-Yout)\n'
                       '        xout_fraction = xout_ratio/(1+xout_ratio)\n'
                       '        removed = Gs*(Yin-Yout)\n'
                       '        liquid_gain = Ls*(xout_ratio-Xin)\n'
                       '        gas_reduction_percent = (Yin-Yout)/Yin*100\n'
                       '        top_force = Yout-m*Xin\n'
                       '        bottom_force = Yin-m*xout_ratio\n'
                       '        derived_Lmin = Gs*(Yin-Yout)/(Yin/m-Xin)\n'
                       '        assert np.isclose(removed,liquid_gain)\n'
                       '        assert np.isclose(derived_Lmin,Lmin)\n'
                       '        assert min(top_force,bottom_force)>0\n'
                       '        print(f"Gas inlet mole fraction={yin_fraction:.6f}; '
                       'outlet={yout_fraction:.6f}")\n'
                       '        print(f"Solvent outlet X={xout_ratio:.6f}; x={xout_fraction:.6f}")\n'
                       '        print(f"Solute removed={removed:.6f} kmol/h ({gas_reduction_percent:.1f}% of '
                       'entering solute)")\n'
                       '        print(f"Solute-balance residual={removed-liquid_gain:.3e} kmol/h")\n'
                       '        print(f"Top driving force={top_force:.6f}; bottom={bottom_force:.6f}; '
                       'Lmin={derived_Lmin:.3f} kmol/h")\n'
                       '        plt.figure(figsize=(6,5))\n'
                       "        plt.plot(X,m*X,label='Equilibrium')\n"
                       "        plt.plot(X,Yout+Ls/Gs*(X-Xin),label='Selected operating line')\n"
                       "        plt.plot(X,Yout+Lmin/Gs*(X-Xin),'--',label='Bottom-pinch operating line')\n"
                       "        plt.scatter([Xin,xout_ratio],[Yout,Yin],color='black',label='Actual end "
                       "compositions')\n"
                       "        plt.xlabel('Liquid mole ratio X'); plt.ylabel('Gas mole ratio Y')\n"
                       '        plt.legend(); plt.grid(); plt.show()\n'
                       '        ',
                       '\n'
                       '        def '
                       'absorption_steps(gas,liquid,gas_in,gas_out,liquid_in=0.,eq_slope=1.5,limit=300):\n'
                       '            if min(gas,liquid,eq_slope)<=0 or liquid_in<0:\n'
                       "                raise ValueError('Invalid flow, slope or solvent composition')\n"
                       '            if not gas_in>gas_out>eq_slope*liquid_in:\n'
                       "                raise ValueError('Infeasible absorption direction')\n"
                       '            minimum = gas*(gas_in-gas_out)/(gas_in/eq_slope-liquid_in)\n'
                       '            if liquid<=minimum:\n'
                       "                raise ValueError('Solvent flow at or below minimum')\n"
                       '            y_value = gas_out\n'
                       '            steps = [(liquid_in,y_value)]\n'
                       '            for n in range(1,limit+1):\n'
                       '                x_value = y_value/eq_slope\n'
                       '                steps.append((x_value,y_value))\n'
                       '                next_y = gas_out+liquid/gas*(x_value-liquid_in)\n'
                       '                steps.append((x_value,next_y))\n'
                       '                if next_y>=gas_in:\n'
                       '                    return n,np.array(steps)\n'
                       '                if next_y<=y_value+1e-12:\n'
                       "                    raise ValueError('Pinch or non-progressing stage')\n"
                       '                y_value = next_y\n'
                       "            raise ValueError('Stage cap reached')\n"
                       '\n'
                       '        N_abs,abs_steps = absorption_steps(Gs,Ls,Yin,Yout,Xin,m)\n'
                       '        assert N_abs==h.stage_count(Gs,Ls,Yin,Yout,Xin,m)[0]\n'
                       '        # Independent fresh-solvent geometric-series check.\n'
                       '        absorption_factor = Ls/(m*Gs)\n'
                       '        analytic_n = next(n for n in range(1,301)\n'
                       '                          if Yout*sum(absorption_factor**k for k in '
                       'range(n+1))>=Yin)\n'
                       '        assert analytic_n==N_abs\n'
                       "        print(f'Full ideal contacts={N_abs}; absorption "
                       "factor={absorption_factor:.4f}')\n"
                       '        solvent_ratios = np.linspace(1.05,2.5,60)\n'
                       '        abs_counts = [absorption_steps(Gs,r*Lmin,Yin,Yout,Xin,m)[0] for r in '
                       'solvent_ratios]\n'
                       '        fig,axes = plt.subplots(1,2,figsize=(12,5))\n'
                       "        axes[0].plot(X,m*X,label='Equilibrium')\n"
                       "        axes[0].plot(X,Yout+Ls/Gs*(X-Xin),label='Operating line')\n"
                       "        axes[0].plot(abs_steps[:,0],abs_steps[:,1],'o-',label='Staircase')\n"
                       "        axes[0].axhline(Yin,color='grey',linestyle=':',label='Gas inlet')\n"
                       "        axes[0].set(xlabel='Liquid mole ratio X',ylabel='Gas mole ratio Y'); "
                       'axes[0].legend()\n'
                       "        axes[1].step(solvent_ratios,abs_counts,where='mid')\n"
                       "        axes[1].set(xlabel='Ls / Lmin',ylabel='Full ideal contacts / count')\n"
                       '        for axis in axes:\n'
                       '            axis.grid()\n'
                       '        plt.tight_layout(); plt.show()\n'
                       '        try:\n'
                       '            absorption_steps(Gs,Lmin,Yin,Yout,Xin,m)\n'
                       '        except ValueError as error:\n'
                       "            print('Expected pinch rejection:',error)\n"
                       '        else:\n'
                       "            raise AssertionError('Minimum solvent rate should be rejected')\n"
                       '        ',
                       '\n'
                       '        installed_trays = int(np.ceil(N_abs/.60))\n'
                       '        tray_height = installed_trays*.45\n'
                       '        hetp_values = np.linspace(.6,1.2,25)\n'
                       '        packed_heights = N_abs*hetp_values\n'
                       '        cross_section, gas_volume = 1.,.8\n'
                       '        superficial_velocity = gas_volume/cross_section\n'
                       '        dry_gradient = h.ergun_gradient(superficial_velocity,.70,.025,1.2,1.8e-5)\n'
                       '        dry_pressure_drop = dry_gradient*packed_heights\n'
                       "        print(f'Tray option: {installed_trays} trays, active "
                       "height={tray_height:.2f} m')\n"
                       "        print(f'Packing option: active "
                       "height={packed_heights.min():.2f}–{packed_heights.max():.2f} m')\n"
                       "        print(f'Superficial gas velocity={superficial_velocity:.3f} m/s')\n"
                       "        print(f'Dry Ergun gradient={dry_gradient:.6f} Pa/m; dry "
                       "drop={dry_pressure_drop.min():.2f}–{dry_pressure_drop.max():.2f} Pa')\n"
                       '        assert np.isclose(h.ergun_gradient(0,.70,.025),0)\n'
                       '        fig,axes = plt.subplots(1,2,figsize=(11,4))\n'
                       "        axes[0].plot(hetp_values,packed_heights,label='Packing')\n"
                       "        axes[0].axhline(tray_height,linestyle=':',color='black',label='Tray active "
                       "height'); axes[0].legend()\n"
                       "        axes[0].set(xlabel='Assumed HETP / m',ylabel='Active height / m')\n"
                       '        axes[1].plot(packed_heights,dry_pressure_drop)\n'
                       "        axes[1].set(xlabel='Packed height / m',ylabel='Illustrative dry pressure "
                       "drop / Pa')\n"
                       '        for axis in axes:\n'
                       '            axis.grid()\n'
                       '        plt.tight_layout(); plt.show()\n'
                       '        ',
                       '\n'
                       '        robustness = []\n'
                       "        print('m       Lmin/kmol h-1   Ls/Lmin   full contacts   status')\n"
                       '        for candidate_m in [.8*m,m,1.2*m]:\n'
                       '            candidate_min = Gs*(Yin-Yout)/(Yin/candidate_m-Xin)\n'
                       '            if Ls<=candidate_min:\n'
                       '                robustness.append((candidate_m,candidate_min,np.nan))\n'
                       "                print(f'{candidate_m:.3f}   {candidate_min:10.3f}    "
                       "{Ls/candidate_min:.3f}       --       infeasible')\n"
                       '                continue\n'
                       '            candidate_N = absorption_steps(Gs,Ls,Yin,Yout,Xin,candidate_m)[0]\n'
                       '            robustness.append((candidate_m,candidate_min,candidate_N))\n'
                       "            print(f'{candidate_m:.3f}   {candidate_min:10.3f}    "
                       "{Ls/candidate_min:.3f}       {candidate_N:2d}       feasible')\n"
                       '        # Also show that the same fixed-flow calculation rejects a true infeasible '
                       'case.\n'
                       '        infeasible_m = 2.5\n'
                       '        infeasible_min = Gs*(Yin-Yout)/(Yin/infeasible_m-Xin)\n'
                       '        assert Ls<=infeasible_min\n'
                       "        print(f'Illustrative infeasible check: m={infeasible_m}, "
                       "Lmin={infeasible_min:.2f} > Ls={Ls:.2f}')\n"
                       '        robust_array = np.array(robustness)\n'
                       '        plt.figure(figsize=(6,4))\n'
                       "        plt.plot(robust_array[:,0],robust_array[:,2],'o-')\n"
                       "        plt.xlabel('Equilibrium slope m / dimensionless'); plt.ylabel('Full ideal "
                       "contacts / count')\n"
                       '        plt.grid(); plt.show()\n'
                       '        ']}
