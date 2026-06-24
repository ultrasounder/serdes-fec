import model.rlgc
import numpy as np, matplotlib.pyplot as plt

f = np.logspace(7, 10.3, 400) # 10 MHz .. 20 GHz

# representative values for a lossy transmission line
L, C = 350e-9, 140e-12     #H/m, F/m -> Z0=sqrt(L/C)~50, vp~0.5c
R0 = 0.05 # ohm/sqrt(Hz)
tand = 0.02 # loss tangent of the dielectric
length = 0.30 # 30cm

alpha, beta = model.rlgc.rlgc_gamma(f, R0, L, 0.0, C, length, tand=tand)

#split the two loss mechanisms by recomputing each alone
w = 2*np.pi*f
a_cond = np.real(np.sqrt((R0*np.sqrt(f)) * (1j*w*C)))
a_diel = np.real(np.sqrt((1j*w*L) * (w*C*tand)))

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].loglog(f/1e9, alpha, 'k', label='total alpha')
ax[0].loglog(f/1e9, a_cond, '--', label='conductor alphasqrt(f)')
ax[0].loglog(f/1e9, a_diel, ':', label='dielectric alpha~f')
ax[0].set(xlabel='GHz', ylabel='α [Np/m]'); ax[0].legend(); ax[0].grid(True, which='both', alpha=.3)
ax[1].loglog(f/1e9, beta, 'b'); ax[1].set(xlabel='GHz', ylabel='β [rad/m]'); ax[1].grid(True, which='both', alpha=.3)
plt.tight_layout(); plt.savefig('notebooks/day2_rlgc.png', dpi=120)
print(f"vp ~ {2*np.pi*14e9/np.interp(14e9,f,beta)/1e8:.2f} ×10^8 m/s")
