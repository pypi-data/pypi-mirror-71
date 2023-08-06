# cfdpost

CFD post procedures.

## # post

    Frequently used CFD post procedures.

### [ post_foil_cfl3d ]

    post_foil_cfl3d(path, j0, j1, nHi=40, fname='feature2d.txt')

    Read in CFL3D foil result and extract flow features.
        path:       folder that contains the output files
        j0:         j index of the lower surface TE
        j1:         j index of the upper surface TE
        nHi:        maximum number of mesh points in k direction for boundary layer
        fname:      output file name. If None, then no output
        tecplot:    if True, then convert cfl3d.prt to surface.dat

    Single C-block cfl3d.prt index
        i : 1 - 1   symmetry plane
        j : 1 - nj  far field of lower surface TE to far field of upper surface TE
        k : 1 - nk  surface to far field

### [ feature_xfoil ]

    feature_xfoil(cst_u, cst_l, t, Minf, Re, AoA, n_crit=0.1, fname='feature-xfoil.txt')

    Evaluate by xfoil and extract features. 
        cst-u, cst-l:   list of upper/lower CST coefficients of the airfoil.
        t:              airfoil thickness or None
        Minf:           free stream Mach number for wall Mach number calculation
        Re, AoA (deg):  flight condition (s), float or list, for Xfoil
        n_crit:         critical amplification ratio for transition in xfoil
        fname:  output file name. If None, then no output

    Dependencies:
        cst_modeling    pip install cst-modeling3d
        xfoil           pip install xfoil

    XFoil:
        Re:     Reynolds number in case the simulation is for a viscous flow. 
                In case not informed, the code will assume inviscid.
        Minf:   Mach number in case the simulation has to take in account compressibility 
                effects through the Prandtl-Glauert correlation. If not informed, 
                the code will not use the correction. For logical reasons, if Mach 
                is informed, a Reynolds number different from zero must also be informed.

### [ feature_TSFoil ]

    Evaluate by TSFOIL2 and extract features.
        cst-u, cst-l:   list of upper/lower CST coefficients of the airfoil
        t:      airfoil thickness or None
        Minf, Re, AoA (deg): flight condition (s), float or list
        fname:  output file name. If None, then no output

    Dependencies:
        cst_modeling    pip install cst-modeling3d
        pyTSFoil        pip install pyTSFoil

## # cfdresult

    Read in CFD results.

### cfl3d

    Read in CFL3D results.

## # feature2d

    Extract 2D flow features.

### FeatureSec

    Extract flow features of airfoils or wing sections.

### FeatureXfoil

    Extract features from Xfoil (low speed) results.

### FeatureTSFoil

    Extract features from pyTSFoil (transonic speed) results.
