[Mesh]
  type = GeneratedMesh
  dim = 1
  nx = 80
  xmax = 160
  ny = 1
  ymax = 2
  uniform_refine = 3
[]


[GlobalParams]
  profile = TANH
  enable_jit = false
  enable_ad_cache = false
[]

[Variables]
  [w_Ni]
  []
  [w_Cr]
  []
  [eta0] #represents the metal phase
  []
  [phi]
  []
[]

[AuxVariables]
  [E_x]
    order = CONSTANT
    family = MONOMIAL
  []
[]

[Kernels]
  [DT_eta0]
    type = TimeDerivative
    variable = eta0
  []
  [ACInt_eta0]
    type = ACInterface
    kappa_name = kappa
    variable = eta0
  []
  [ACBulkF]
    type = KKSACBulkF
    variable = eta0
    fa_name = omega_melt
    fb_name = omega_metal
    w = ${fparse 6 * 1.493e7 / 2}#4.479e7
    h_name = h_metal
    mob_name = L
    args = 'w_Ni w_Cr'
  []

  #Ni CH equation
  [ChiDt_w_Ni]
    type = SusceptibilityTimeDerivative
    args = 'eta0 w_Cr'
    f_name = chi_Ni
    variable = w_Ni
  []
  [MatDif_w_Ni]
    type = MatDiffusion
    diffusivity = M_Ni
    variable = w_Ni
    args = 'eta0 w_Cr'
  []
  [Coupled_w_Ni_eta0]
    type = CoupledSwitchingTimeDerivative
    Fj_names = 'del_c_Ni'
    args = 'eta0 w_Cr'
    hj_names = 'h_metal'
    v = eta0
    variable = w_Ni
  []
  #Cr CH equation
  [ChiDt_w_Cr]
    type = SusceptibilityTimeDerivative
    args = 'eta0 w_Ni'
    f_name = chi_Cr
    variable = w_Cr
  []
  [MatDif_w_Cr]
    type = MatDiffusion
    diffusivity = M_Cr
    variable = w_Cr
    args = 'eta0 w_Ni'
  []
  [Coupled_w_Cr_eta0]
    type = CoupledSwitchingTimeDerivative
    Fj_names = 'del_c_Cr'
    args = 'eta0 w_Ni'
    hj_names = 'h_metal'
    v = eta0
    variable = w_Cr
  []

  ###Electrochemistry Kernels
  #calculating phi
  [elec_chem_Ni]
    type = MatDiffusion
    variable = phi
    v = w_Ni
    diffusivity = 'chem_flux_Ni'
  []
  [elec_chem_Cr]
    type = MatDiffusion
    variable = phi
    v = w_Cr
    diffusivity = 'chem_flux_Cr'
  []
  [elec_phi]
    type = MatDiffusion
    variable = phi
    diffusivity = 'elec_flux'
  []

  # ##electro_diffusion
  [elec_diffusion_Ni]
    type = MatDiffusion
    variable = w_Ni
    v = phi
    diffusivity = elec_M_Ni
  []
  [elec_diffusion_Cr]
    type = MatDiffusion
    variable = w_Cr
    v = phi
    diffusivity = elec_M_Cr
  []
[]

[AuxKernels]
  [elec_field]
    type = VariableGradientComponent
    variable = 'E_x'
    component = 'x'
    gradient_variable = phi
  []
[]

[ICs]
  [eta0_metal_inital]
    type = SmoothCircleIC
    variable = 'eta0'
    x1 = 0
    y1 = 0
    radius = 150
    invalue = '1'
    outvalue = '0.0'
    int_width = 2
  []

  # #Ni INITIAL CONDITIONS -> 5% Cr
  [w_Ni_global_inital]
    type = SmoothCircleIC
    variable = 'w_Ni'
    x1 = 0
    y1 = 0
    radius = 150
    invalue = -0.4667  #Ni-20Cr
    outvalue = -0.45065 #Same chemical potential as Ni-5Cr alloy
    int_width = 2.0
  []
  [w_Cr]
    type = SmoothCircleIC
    variable = 'w_Cr'
    x1 = 0
    y1 = 0
    radius = 150
    invalue = -0.56093  #Ni-5Cr
    outvalue = -0.9699 #Ni2+ concentration is 25e-6
    int_width = 2.0
  []
[]

[BCs]
  [left_electrode_phi]
    type = DirichletBC
    variable = phi
    value = 0.0
    boundary = 'left'
  []
  [w_Ni_right]
    type = DirichletBC
    variable = w_Ni
    value = -0.45065
    boundary = 'right'
  []
  [w_Cr_right]
    type = FunctionDirichletBC
    variable = w_Cr
    function = '-0.9699'
    boundary = 'right'
  []
[]

[Materials]

  [constants]
    type = GenericConstantMaterial
    prop_names = 'gamma    gr_energy_sigma  interface_energy_sigma    interface_thickness_l  Va          pi           del_int   Na                xc  GB_width'
    prop_values = '1.5     6.803e6          1.493e7                   2.0                    1.1087e-11  3.141592653  0.025       6.02214076e23   0.0 5e-4'
  []
  [energy_constants]
    type = GenericConstantMaterial
    prop_names = 'kB            R      T     n  F             k_metal  k_melt   HF_H2  E0_F   E_F' #E0_F is electrode potential in Baes, E_F is pontential in the experimental salt
    prop_values = '8.6173324e-5 8.314  973   2  96485.33212   1.0     1.0      1e-9   2.871  3.3607'
  []

  [L]
    type = ParsedMaterial
    f_name = 'L'
    material_property_names = 'n F kB T Va interface_thickness_l pi del_int'
    constant_names = 'i0   m          D    J_to_eV    m3_to_um3 R'
    constant_expressions = '5.7 58.693e-3  8900 6.242e+18  1e18      8.314' #SI units
    function = '((del_int*i0*(m/D)^2)/(pi*n*F*R*T*interface_thickness_l*1e-6) )*(m3_to_um3/J_to_eV)' #/Va to normalize L for grand potential in eV/atom rather than eV/um3
    outputs = exodus
  []

  [E0_Ni_metal]
    type = ParsedMaterial
    material_property_names = 'T F'
    function = '(-5179.159 + 117.854*T - 22.096*T*log(T) - (4.8407e-3)*T^2)/F'
    f_name = 'E0_Ni_metal'
    outputs = exodus
  []
  [G_xs]
    type = ParsedMaterial
    f_name = 'Gxs'
    material_property_names = 'T F'
    constant_names = 'H_xs S_xs'
    constant_expressions = '-1.56448695e+04 -1.56011217'
    function = 'H_xs - S_xs*T'
    outputs = exodus
  []
  [E0_Va_metal]
    type = ParsedMaterial
    material_property_names = 'T kB'
    constant_names = 'H0_f S0_f'
    constant_expressions = '1.56 3.3'
    function = 'H0_f - S0_f*kB*T'
    f_name = 'E0_Va_metal'
    outputs = exodus
  []
  [E0_Cr_metal]
    type = ParsedMaterial
    material_property_names = 'T F Gxs'
    function = '(-1572.94 + 157.643*T - 26.908*T*log(T) + 1.89435e-3*T^2 - 1.47721e-6*T^3 + 139250/T '
               '+ Gxs)/F'
    f_name = 'E0_Cr_metal'
    outputs = exodus
  []

  [E0_Ni_melt]
    type = ParsedMaterial
    f_name = 'E0_Ni_melt'
    constant_names = 'E0_NiF2'
    constant_expressions = '0.473'
    material_property_names = 'E0_Ni_metal kB T n HF_H2 E0_F E_F'
    function = 'E0_Ni_metal + n*(E0_NiF2 + (E_F-E0_F))'
    outputs = exodus
  []
  [E0_Cr_Cr]
    type = ParsedMaterial
    f_name = 'E0_Cr_Cr'
    material_property_names = 'T F'
    function = '(-8856.94 + 157.48*T - 26.908*T*log(T) + 1.89435e-3*T^2 - 1.47721e-6*T^3 + '
               '139250/T)/F'
  []
  [E0_Cr_melt]
    type = ParsedMaterial
    f_name = 'E0_Cr_melt'
    constant_names = 'E0_CrF2'
    constant_expressions = '-0.39'
    material_property_names = 'E0_Cr_Cr kB T n HF_H2 E0_F E_F'
    function = 'E0_Cr_Cr + n*(E0_CrF2 +  (E_F-E0_F))'
    outputs = exodus
  []
  [E0_Va_melt]
    type = GenericConstantMaterial
    prop_names = 'E0_Va_melt'
    prop_values = '0.0'
  []

  #PARAMETERS
  [kappa] #assume that three interfaces having the same interfacial energy and thickness
    type = ParsedMaterial
    f_name = kappa
    material_property_names = 'interface_energy_sigma interface_thickness_l'
    function = '3*interface_energy_sigma*interface_thickness_l/4'
  []
  [m]
    type = ParsedMaterial
    f_name = mu
    material_property_names = 'interface_energy_sigma interface_thickness_l'
    function = '6*interface_energy_sigma/interface_thickness_l'
  []

  #DOUBLE WELL eta
  [g]
    type = DerivativeParsedMaterial
    f_name = 'g'
    args = 'eta0'
    material_property_names = 'gamma'
    function = '(eta0^4/4-eta0^2/2)+((1-eta0)^4/4-(1-eta0)^2/2)+(gamma*eta0^2*(1-eta0)^2)+1/4'
  []

  [h_metal]
    type = DerivativeParsedMaterial
    f_name = 'h_metal'
    args = 'eta0'
    material_property_names = 'pi del_int'
    function = '0.5*(1+tanh(2*pi*(eta0-0.5)/del_int ))'
    outputs = 'exodus'
    output_properties = 'h_metal'
    derivative_order = 4
  []

  [c_Ni_metal]
    type = DerivativeParsedMaterial
    f_name = "c_Ni_metal"
    args = 'w_Ni w_Cr'
    material_property_names = 'kB T k_metal E0_Ni_metal E0_Va_metal  E0_Cr_metal'
    function = 'exp( (w_Ni - (E0_Ni_metal - E0_Va_metal))/kB/T/k_metal )/( 1 + exp( (w_Ni - '
               '(E0_Ni_metal - E0_Va_metal))/kB/T/k_metal ) + exp( (w_Cr - (E0_Cr_metal - '
               'E0_Va_metal))/kB/T/k_metal ))'
    outputs = 'exodus'
    output_properties = 'c_Ni_metal'
  []
  [c_Ni_melt]
    type = DerivativeParsedMaterial
    f_name = "c_Ni_melt"
    args = 'w_Ni w_Cr'
    material_property_names = 'kB T k_melt E0_Ni_melt E0_Va_melt E0_Cr_melt'
    function = 'exp( (w_Ni - (E0_Ni_melt) - k_melt*kB*T)/kB/T/k_melt )'
    outputs = 'exodus'
    output_properties = 'c_Ni_melt'
  []
  [c_Cr_metal]
    type = DerivativeParsedMaterial
    f_name = "c_Cr_metal"
    args = 'w_Ni w_Cr'
    material_property_names = 'kB T k_metal E0_Ni_metal E0_Cr_metal E0_Va_metal'
    function = 'exp( (w_Cr - (E0_Cr_metal - E0_Va_metal))/kB/T/k_metal )/( 1 + exp( (w_Ni - '
               '(E0_Ni_metal - E0_Va_metal))/kB/T/k_metal ) + exp( (w_Cr - (E0_Cr_metal - '
               'E0_Va_metal))/kB/T/k_metal ))'
    outputs = 'exodus'
    output_properties = 'c_Cr_metal'

  []
  [c_Cr_melt]
    type = DerivativeParsedMaterial
    f_name = "c_Cr_melt"
    args = 'w_Ni w_Cr'
    material_property_names = 'kB T k_melt E0_Ni_melt E0_Va_melt E0_Cr_melt'
    function = 'exp( (w_Cr - (E0_Cr_melt - E0_Va_melt) - k_melt*kB*T)/kB/T/k_melt )'
    outputs = 'exodus'
    output_properties = 'c_Cr_melt'

  []
  #Calculate global concentrations using switching FUNCTIONS
  [c_Ni]
    type = DerivativeParsedMaterial
    f_name = 'c_Ni'
    material_property_names = 'c_Ni_metal c_Ni_melt h_metal h_melt'
    function = 'c_Ni_metal*h_metal + c_Ni_melt*(1-h_metal)'
    outputs = 'exodus'
    output_properties = 'c_Ni'
  []
  [c_Cr]
    type = DerivativeParsedMaterial
    f_name = 'c_Cr'
    material_property_names = 'c_Cr_metal c_Cr_melt h_metal h_melt'
    function = 'c_Cr_metal*h_metal + c_Cr_melt*(1-h_metal)'
    outputs = 'exodus'
    output_properties = 'c_Cr'
  []
  [c_Va]
    type = DerivativeParsedMaterial
    f_name = 'c_Va'
    material_property_names = 'c_Ni c_Cr h_metal'
    function = '(1-c_Ni-c_Cr)'
    outputs = exodus
  []
  [del_c_Ni]
    type = DerivativeParsedMaterial
    f_name = 'del_c_Ni'
    args = 'w_Ni w_Cr eta0'
    material_property_names = 'kB T k_metal E0_Ni_metal E0_Va_metal  E0_Cr_metal k_melt E0_Ni_melt '
                              'E0_Va_melt E0_Cr_melt Va'
    function = '(exp( (w_Ni - (E0_Ni_metal - E0_Va_metal))/kB/T/k_metal )/( 1 + exp( (w_Ni - '
               '(E0_Ni_metal - E0_Va_metal))/kB/T/k_metal ) + exp( (w_Cr - (E0_Cr_metal - '
               'E0_Va_metal))/kB/T/k_metal ))
     - exp( (w_Ni - (E0_Ni_melt-E0_Va_melt) - '
               'k_melt*kB*T )/kB/T/k_melt ) )'
  []
  [del_c_Cr]
    type = DerivativeParsedMaterial
    f_name = 'del_c_Cr'
    args = 'w_Ni w_Cr eta0'
    material_property_names = 'kB T k_metal E0_Ni_metal E0_Cr_metal E0_Va_metal k_melt E0_Ni_melt '
                              'E0_Va_melt E0_Cr_melt Va'
    function = '(exp( (w_Cr - (E0_Cr_metal - E0_Va_metal))/kB/T/k_metal )/( 1 + exp( (w_Ni - '
               '(E0_Ni_metal - E0_Va_metal))/kB/T/k_metal ) + exp( (w_Cr - (E0_Cr_metal - '
               'E0_Va_metal))/kB/T/k_metal ))
     - exp( (w_Cr - (E0_Cr_melt-E0_Va_melt)  - '
               'k_melt*kB*T)/kB/T/k_melt ) )'
  []
  #Derivative terms of free energy
  [omega_metal]
    type = DerivativeParsedMaterial
    f_name = 'omega_metal'
    args = 'eta0 w_Ni w_Cr'
    material_property_names = 'kB T k_metal E0_Ni_metal E0_Va_metal  E0_Cr_metal Va'
    function = '(E0_Va_metal - kB*T*k_metal*log( 1 + exp( (w_Ni - (E0_Ni_metal - '
               'E0_Va_metal))/kB/T/k_metal ) + exp( (w_Cr - (E0_Cr_metal - '
               'E0_Va_metal))/kB/T/k_metal ) ) )/Va'
    outputs = exodus
    derivative_order = 2
  []
  [omega_melt]
    type = DerivativeParsedMaterial
    f_name = 'omega_melt'
    args = 'eta0 w_Ni w_Cr'
    material_property_names = 'kB T k_melt E0_Ni_melt E0_Va_melt E0_Cr_melt Va'
    function = '(E0_Va_melt - kB*T*k_melt*(exp( (w_Ni - (E0_Ni_melt - E0_Va_melt) - '
               'k_melt*kB*T)/kB/T/k_melt ) + exp( (w_Cr - (E0_Cr_melt - E0_Va_melt) - '
               'k_melt*kB*T)/kB/T/k_melt ) ) )/Va'
    outputs = exodus
    derivative_order = 2
  []
  [omega_chem]
    type = DerivativeParsedMaterial
    f_name = omega_chem
    args = 'eta0'
    material_property_names = 'h_metal omega_metal omega_melt Va'
    function = 'h_metal*Va*(omega_metal-omega_melt)'
    outputs = 'exodus'
  []
  [hart_factor]
    type = ParsedMaterial
    f_name = 'f'
    constant_names = 'd q'
    constant_expressions = '4.64 1'
    function = 'q/d'
    outputs = exodus
  []
  [susceptibility_Ni]
    type = DerivativeParsedMaterial
    f_name = 'chi_Ni'
    args = 'eta0 w_Ni w_Cr'
    material_property_names = 'c_Ni_metal(w_Ni,w_Cr) c_Ni_melt(w_Ni,w_Cr) h_metal '
                              'chi_Ni_metal:=D[c_Ni_metal,w_Ni] chi_Ni_melt:=D[c_Ni_melt,w_Ni]'
    function = 'chi_Ni_metal*h_metal + chi_Ni_melt*(1-h_metal)'
    outputs = exodus
  []
  [D_Ni_V]
    type = ParsedMaterial
    f_name = 'D_Ni_V'
    material_property_names = 'T R c_Va'
    constant_names = 'D0_Ni_V       E0_Ni_V     cal_to_J' ##https://aip.scitation.org/doi/pdf/10.1063/1.1703047
    constant_expressions = '1.9e8         66800       4.184'
    function = 'D0_Ni_V*exp(-E0_Ni_V*cal_to_J/R/T)*(c_Va/2.254e-7)'
    outputs = exodus
  []
  [D_Ni_GB]
    type = ParsedMaterial
    f_name = 'D_Ni_GB'
    material_property_names = 'T R GB_width c_Va'
    constant_names = 'D0_Ni_GB      E0_Ni_GB     cal_to_J' ##https://aip.scitation.org/doi/pdf/10.1063/1.1703047
    constant_expressions = '0.07e8        27400        4.184'
    function = 'D0_Ni_GB*exp(-E0_Ni_GB*cal_to_J/R/T)*GB_width*(c_Va/2.254e-7)'
    outputs = exodus
  []
  [D_Ni]
    type = ParsedMaterial
    f_name = D_Ni
    args = 'eta0 w_Ni w_Cr'
    material_property_names = 'f D_Ni_V D_Ni_GB h_metal'
    function = '( (1-f)*D_Ni_V + f*D_Ni_GB)*h_metal  + 500*(1-h_metal) '
    outputs = 'exodus'
  []

  [mobility_Ni]
    type = DerivativeParsedMaterial
    f_name = M_Ni
    args = 'eta0 w_Ni w_Cr'
    material_property_names = 'chi_Ni D_Ni'
    function = 'D_Ni*chi_Ni'
    outputs = 'exodus'
    derivative_order = 2
  []

  [susceptibility_Cr]
    type = DerivativeParsedMaterial
    f_name = 'chi_Cr'
    args = 'eta0 w_Ni w_Cr'
    material_property_names = 'c_Cr_metal(w_Ni,w_Cr) c_Cr_melt(w_Ni,w_Cr) h_metal '
                              'chi_Cr_metal:=D[c_Cr_metal,w_Cr] chi_Cr_melt:=D[c_Cr_melt,w_Cr]'
    function = 'chi_Cr_metal*h_metal + chi_Cr_melt*(1-h_metal)'
    outputs = exodus
  []
  [cross_susceptibility_Cr]
    type = DerivativeParsedMaterial
    f_name = 'cross_chi_Cr'
    args = 'w_Ni w_Cr eta0'
    material_property_names = 'c_Cr_metal c_Cr_melt  cross_Cr_metal:=D[c_Cr_metal,w_Ni] '
                              'cross_Cr_melt:=D[c_Cr_melt,w_Ni] h_metal'
    function = 'h_metal*cross_Cr_metal + (1-h_metal)*cross_Cr_melt'
    outputs = 'exodus'
  []

  [D_Cr_V]
    type = ParsedMaterial
    f_name = D_Cr_V
    material_property_names = 'R T F E0_Ni_metal E0_Va_metal xc c_Va'
    constant_names = 'D0      D1        E0        E1'
    constant_expressions = '5.353e3 0.0199e3  7.8886e7  0.0285e7'
    function = '(exp(-(84702800778885824000*xc + 306299812110263875)/(8927089524736*T))*exp((5885692387260437*xc)/1099511627776)*exp(699261826406127/35184372088832))*(c_Va/2.254e-7)'
    outputs = exodus
  []
  [D_Cr_GB]
    type = ParsedMaterial
    f_name = D_Cr_GB
    material_property_names = 'R T F E0_Ni_metal E0_Va_metal xc c_Va'
    constant_names = 'D2       D3        E2        E3'
    constant_expressions = '1.2211e4 0.0017e4  1.9883e8  0.002e8'
    function = '(exp((209787039506469*xc)/17179869184)*exp(2393065153853383/140737488355328)*exp(-(85'
               '3955374395308288000*xc + 841876566076058375)/(35708358098944*T)))*(c_Va/2.254e-7)'
    outputs = exodus
  []
  [D_Cr]
    type = ParsedMaterial
    f_name = D_Cr
    args = 'eta0 w_Ni w_Cr'
    material_property_names = 'f D_Cr_V D_Cr_GB h_metal'
    function = '  ( (1-f)*D_Cr_V + f*D_Cr_GB)*h_metal  + 500*(1-h_metal)' #'( ( (1-f)*D_Cr_V + f*D_Cr_GB )*h_metal  + 500*(1-h_metal) )'

    outputs = 'exodus'
  []
  [mobility_Cr]
    type = DerivativeParsedMaterial
    f_name = M_Cr
    args = 'eta0 w_Ni w_Cr'
    material_property_names = 'chi_Cr D_Cr'
    function = 'D_Cr*chi_Cr'
    outputs = 'exodus'
    derivative_order = 2
  []
  [M_H]
    type = DerivativeParsedMaterial
    args = 'w_Ni eta0'
    f_name = 'M_H'
    material_property_names = 'h_metal kB T k_melt R E0_F E_F'

    function = 'c_H:= exp(-(E_F-E0_F)/kB/T);(1e-7*h_metal + 1000*(1-h_metal) )*c_H/kB/T/k_melt'
    outputs = 'exodus'
    output_properties = 'M_H'
  []
  [M_e]
    type = DerivativeParsedMaterial
    args = 'w_Ni eta0'
    f_name = 'M_e'
    material_property_names = 'h_metal kB T k_metal Va'
    function = '( (48709375000)*h_metal + 1e-12*(1-h_metal) )/kB/T/k_metal'
    outputs = 'exodus'
    output_properties = 'M_e'
  []
  #Computing phi
  [flux_Ni]
    type = DerivativeParsedMaterial
    args = 'eta0 w_Ni phi'
    f_name = 'chem_flux_Ni'
    material_property_names = 'z_Ni z_F M_Ni M_F h_metal'
    function = '(1-h_metal)*M_Ni*2'
  []
  [flux_Cr]
    type = DerivativeParsedMaterial
    args = 'eta0 w_Cr phi'
    f_name = 'chem_flux_Cr'
    material_property_names = 'z_Ni z_F M_Cr M_F h_metal'
    function = '(1-h_metal)*M_Cr*2'
    outputs = 'exodus'
    output_properties = 'chem_flux_Cr'
  []
  [grad_phi_coeff]
    type = DerivativeParsedMaterial
    f_name = 'elec_flux'
    args = 'eta0 w_Ni phi'
    material_property_names = 'z_Ni z_F M_Ni M_Cr M_H M_e h_metal'
    function = '(1-h_metal)*(4*M_Ni + 4*M_Cr + M_H) + (h_metal)*M_e'
    output_properties = 'elec_flux'
    outputs = exodus
  []
  #electro_diffusion
  [elec_M_Ni]
    type = DerivativeParsedMaterial
    f_name = 'elec_M_Ni'
    args = 'w_Ni eta0 phi'
    material_property_names = 'h_metal M_Ni'
    function = '(1-h_metal)*M_Ni*2'
  []
  [elec_M_Cr]
    type = DerivativeParsedMaterial
    f_name = 'elec_M_Cr'
    args = 'w_Cr eta0 phi'
    material_property_names = 'h_metal M_Cr'
    function = '(1-h_metal)*M_Cr*2'
  []

  #Postprocessor materials
  [metal_thickness]
    type = ParsedMaterial
    f_name = 'metal_thickness'
    args = 'eta0'
    function = 'if(eta0>0.5,1,0)'
  []
  [Cr_mass]
    type = ParsedMaterial
    f_name = 'Cr_mass'
    material_property_names = 'c_Cr h_metal metal_thickness Va Na'
    function = '(h_metal*c_Cr/Va)*51.99*1e8*1000/Na' #g/um3 -> 1e12 g/cm3, Mass loss/Area => g/um2 -> 1e8 g/cm2, *1000 -> mg/cm2
  []
  [Ni_mass]
    type = ParsedMaterial
    f_name = 'Ni_mass'
    material_property_names = 'c_Ni h_metal metal_thickness Va Na'
    function = '(h_metal*c_Ni/Va)*58.69*1e8*1000/Na' #g/um3 -> 1e12 g/cm3, Mass loss/Area => g/um2 -> 1e8 g/cm2, *1000 -> mg/cm2
  []
  [total_mass]
    type = ParsedMaterial
    f_name = 'total_mass'
    material_property_names = 'c_Cr_metal c_Ni_metal h_metal metal_thickness Va Na'
    function = '(h_metal/Va)*(c_Cr_metal*51.99 +c_Ni_metal*58.69)*1e8*1000/Na' #g/um3 -> 1e12 g/cm3, Mass loss/Area => g/um2 -> 1e8 g/cm2, *1000 -> mg/cm2
  []

  [elec_conductivity]
    type = ParsedMaterial
    f_name = 'sigma_e'
    material_property_names = 'M_e'
    function = '1.43e7*1e6*1e3/1e4' #1.43e7 S/m, *1e6 because electric field is in um, 1e3 to convert A->mA, 1e4 converts /m2 to /cm2
  []
[]

[Executioner]
  type = Transient
  solve_type = PJFNK #NEWTON
  scheme = bdf2
  petsc_options_iname = '-pc_type -pc_factor_mat_solver_package'
  petsc_options_value = 'lu superlu_dist'
  l_max_its = 30
  l_tol = 1e-4
  # nl_rel_tol = 1e-8
  # nl_abs_tol = 1e-20
  nl_rel_tol = 1e-12
  nl_abs_tol = 1e-12
  dtmin = 1e-7
  automatic_scaling = true
  compute_scaling_once = false
  dtmax = 1e4 #1000#3600 #5000 #500.0
  end_time = 3.6e6 #8.6e6 #8.6e4 = 1 day
  [TimeStepper]
    type = IterationAdaptiveDT
    dt = 1e-4
    iteration_window = 2
    optimal_iterations = 9
    growth_factor = 1.1
    cutback_factor = 0.8
  []
  # [Adaptivity]
  #   max_h_level = 2
  #   refine_fraction = 0.9
  #   coarsen_fraction = 0.05
  # []

  # num_steps = 1
[]

[Postprocessors]
  [elapsed]
    type = PerfGraphData
    section_name = "Root"
    data_type = total
  []
  [metal_thickness]
    type = ElementIntegralMaterialProperty
    mat_prop = 'h_metal'
  []
  [Cr_metal_mass_total]
    type = ElementIntegralMaterialProperty
    mat_prop = 'Cr_mass'
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [dM_Cr_metal]
    type = ChangeOverTimePostprocessor
    postprocessor = Cr_metal_mass_total
    execute_on = 'INITIAL TIMESTEP_END'
    change_with_respect_to_initial = true
  []
  [Ni_metal_mass_total]
    type = ElementIntegralMaterialProperty
    mat_prop = 'Ni_mass'
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [total_alloy_mass]
    type = ElementIntegralMaterialProperty
    mat_prop = 'total_mass'
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [total_Ni]
    type = ElementIntegralMaterialProperty
    mat_prop = 'c_Ni'
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [total_Cr]
    type = ElementIntegralMaterialProperty
    mat_prop = 'c_Cr'
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [corrosion_current] ##Gives current in A/um^2. To convert to mA/cm^2, multiply value by 10^11
    type = SideFluxAverage
    variable = phi
    diffusivity = 'sigma_e'
    boundary = left
  []
[]

[Outputs]
  exodus = true
  perf_graph = true
  csv = true
  file_base = '1D/Ni20Cr_hart'
[]
