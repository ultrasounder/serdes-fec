import numpy as np

def rlgc_gamma(f, R0, L, G0, C, length, tand=None):
    """Calculate the propogateion constant and characteristic impedance of a lossy transmission line
    f : array of frequencies in [HZ]
    R0: series resistance coefficinet so that R(f) = R0 * sqrt(f) [ohm/sqrt(Hz)]
    L : series inductance [H/m]
    G0: shunt conductance coefficient so that G(f) = G0 * f [S/Hz]
    C: shunt capacitance [F/m]
    length : line length [m]
    tand : loss tangent of the dielectric; if given, overrides G0 via G = w*C*tand
    
    returns (alpha_Np_per_m, beta_rad_per_m)
    
    """
    
    w = 2 * np * np.pi * f
    R = R0 * np.sqrt(f) # Skin effect resistance
    G = (w * C * tand) if tand is not None else (G0 * f) # Dielectic ~ f
    Zser = R + 1j * w * L
    Ysh = G + 1j * w * C
    gamma = np.sqrt(Zser * Ysh)
    return np.real(gamma), np.imag(gamma)


    
    