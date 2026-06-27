from pathlib import Path
import numpy as np



def rlgc_gamma(f, R0, L, C, tand, f0=1e9):
    """Gamma = α + jβ for a lossy transmission line. Returns tuple of (α, β) in Np/m and rad/m"""
    w = 2 * np.pi * f
    R = R0 * np.sqrt(f/f0)          # skin effect ~ sqrt(f)
    G = w * C * tand             # dielectric ~ f
    # gamma = np.sqrt((R + 1j*w*L) * (G + 1j*w*C))
    # return np.real(gamma), np.imag(gamma)
    return np.sqrt((R + 1j*w*L) * (G + 1j*w*C))

def insertion_loss_db(gamma, length):
    """IL as positive dB. Accepts complex gamma or real alpha array"""
    alpha = np.real(gamma) if np.iscomplexobj(gamma) else np.asanyarray(gamma)
    return 8.686 * alpha * length     # = -20*log10(exp(-alpha*length))
def loss_components_db_per_m(f, R0, L, C, tand, f0=1e9):
    """Split total loss into conductor vs dielectric components. Returns tuple of (conductor, dielectric) in dB/m"""
    Z0 = np.sqrt(L/C)
    a_c = (R0*np.sqrt(f/f0))/(2*Z0)      # Np/m
    a_d = (2*np.pi*f*C*tand)*Z0/2        # Np/m
    return 8.686 * a_c, 8.686 * a_d
