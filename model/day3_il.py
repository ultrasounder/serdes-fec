import numpy as np, matplotlib.pyplot as plt, scipy.signal as sig
from sys import path; path.append("../model")
from channel import rlgc_gamma, insertion_loss_db, loss_components_db_per_m

# Representative 50-ohm FR-4 stripline, per meter
R0, L, C, tand = 17.27, 250e-9, 100e-12, 0.02 #Tuned: Crossover ~ 1GHz
length = 0.30 # 30 cm
f = np.logspace(7, 10.43, 400) # 10 MHz to 27 GHz
gamma = rlgc_gamma(f, R0, L, C, tand)
IL = insertion_loss_db(gamma, length)
print("shapes:", f.shape, gamma.shape, np.shape(IL))   # want (400,) (400,) (400,)
ac, ad = loss_components_db_per_m(f, R0, L, C, tand)

# Crossover: where conductor == dielectric
fx = f[np.argmin(np.abs(ac - ad))]
# read the two lossess at 14 GHz (The prediction point for the 28G PAM4 channel)
print(f"Crossover frequency: {fx/1e9:.2f} GHz")
print(f"f = 14 GHz: Conductor loss = {ac[np.argmin(np.abs(f-14e9))]:.2f} dB/m, Dielectric loss = {ad[np.argmin(np.abs(f-14e9))]:.2f} dB/m")
print(f"@14 GHz dielectric = {ad[np.argmin(np.abs(f-14e9))]*length:.2f} dB ({ad[np.argmin(np.abs(f-14e9))]:.2f} dB/m * {length:.2f} m)")
print(f"@14GHz total IL = {IL[np.argmin(np.abs(f-14e9))]:.2f} dB ({IL[np.argmin(np.abs(f-14e9))]/length:.2f} dB/m * {length:.2f} m)")

fig, ax = plt.subplots(figsize=(7, 4))
ax.semilogx(f/1e9, IL, 'k', lw=2, label="total IL (30 cm)")
ax.semilogx(f/1e9, ac*length, '--', label="conductor loss (30 cm)")
ax.semilogx(f/1e9, ad*length, '--', label="dielectric loss (30 cm)")
ax.axvline(fx/1e9, color='gray', ls=':'); ax.axvline(14, color='r', ls=':')
ax.annotate(f"crossover {fx/1e9:.1f} GHz", (fx/1e9, 1), rotation=90, va='bottom')
ax.set_xlabel("Frequency (GHz)"); ax.set_ylabel("Loss (dB)")
ax.legend(); ax.grid(True, which="both", alpha=0.3); ax.invert_yaxis(); ax.set_title("FR-4 Stripline Losses (30 cm)")
plt.tight_layout();plt.savefig("day3_il.png", dpi=120); plt.show()