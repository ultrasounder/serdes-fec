
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def rlgc_gamma(f, R0, L, C, length, tand):
    w = 2 * np.pi * f
    R = R0 * np.sqrt(f)          # skin effect ~ sqrt(f)
    G = w * C * tand             # dielectric ~ f
    gamma = np.sqrt((R + 1j*w*L) * (G + 1j*w*C))
    return np.real(gamma), np.imag(gamma)

f = np.logspace(7, 10.3, 400)
L, C, R0, tand, length = 350e-9, 140e-12, 0.05, 0.02, 0.30
alpha, beta = rlgc_gamma(f, R0, L, C, length, tand)

w = 2*np.pi*f
a_cond = np.real(np.sqrt((R0*np.sqrt(f)) * (1j*w*C)))
a_diel = np.real(np.sqrt((1j*w*L) * (w*C*tand)))

fig, ax = plt.subplots(1, 2, figsize=(11,4))
ax[0].loglog(f/1e9, alpha, 'k', label='total α')
ax[0].loglog(f/1e9, a_cond, '--', label='conductor ∝√f')
ax[0].loglog(f/1e9, a_diel, ':',  label='dielectric ∝f')
ax[0].set(xlabel='GHz', ylabel='α [Np/m]'); ax[0].legend(); ax[0].grid(True, which='both', alpha=.3)
ax[1].loglog(f/1e9, beta, 'b'); ax[1].set(xlabel='GHz', ylabel='β [rad/m]'); ax[1].grid(True, which='both', alpha=.3)
plt.tight_layout(); plt.savefig("day2_rlgc.png", dpi=120)

print(f"vp ~ {2*np.pi*14e9/np.interp(14e9,f,beta)/1e8:.2f} ×10^8 m/s")
print(f"14 GHz: conductor α={np.interp(14e9,f,a_cond):.2f}, dielectric α={np.interp(14e9,f,a_diel):.2f} Np/m")
