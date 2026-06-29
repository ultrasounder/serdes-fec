import numpy as np, matplotlib.pyplot as plt, scipy.signal as sig
from sys import path; path.append("../model")
from channel import rlgc_gamma, insertion_loss_db, loss_components_db_per_m

"""Link parameters(match Day 3, loss-tangent form)"""
R0, L, C, tand = 17.27, 250e-9, 100e-12, 0.02
length = 0.30 
baud = 10e9
sps = 32
UI = 1/baud

"""build a dense one-sided H(f) on an FFT grid"""

N = 8192 # freq points(one-sided)
fs = baud*sps # sample rate
f = np.linspace(0, fs/2, N) # one-sided freq vector
f[0] = f[1]/10 # avoid DC singularity
gamma = rlgc_gamma(f, R0, L, C, tand)
H = np.exp(-gamma*length) # one-sided H(f)

"""--- one UI rectangular input, then channel filter ----"""
"""impulse-style: take channel impulse response via irfft"""
h = np.fft.irfft(H, n=2*(N-1)) # channel impulse response
h = h/np.max(np.abs(h)) # normalize to unity peak

"""pulse response = response to a single UI-wide rectangle -----"""
rect = np.ones(sps) 
pulse = np.convolve(h, rect)[:4000] # truncate to 4000 samples
pulse = pulse/np.max(np.abs(pulse)) # normalize to unity peak

"""Cursor extraction: find the peak, then find the first zero crossing after the peak"""
main_idx = np.argmax(pulse)
def tap(k):
    i = main_idx + k*sps # k-th UI after the main peak
    return pulse[i] if 0 <=i  < len(pulse) else 0.0
pre = [tap(-k) for k in range(1, 4)] # 3 pre-cursors
post = [tap(k) for k in range(1, 9)] # 8 post-cursors
main = tap(0) # main cursor
isi = (sum(abs(x) for x in pre) + sum(abs(x) for x in post))/abs(main) # ISI = sum of all pre/post cursors divided by main cursor

print(f"main cursor = {main:.3f}")
print(f"pre-cursors = {[f'{x:.3f}' for x in pre]}")
print(f"post-cursors = {[f'{x:.3f}' for x in post]}")
print(f"ISI = {isi:.3f}")

t = np.arange(len(pulse)) / sps # time vector in seconds

plt.figure(figsize=(7, 4))
plt.plot(t, pulse, lw=1)
plt.stem([(main_idx+k*sps)/sps for k in range(-3, 9)], [tap(k) for k in range(-3, 9)], linefmt='r-', markerfmt='ro', basefmt= ' ')
plt.xlabel("Time (UI)"); plt.ylabel("Normalized pulse"); plt.grid(alpha=0.3)
plt.title(f"pulse response (ISI ratio={isi:.2f})")
plt.tight_layout(); plt.savefig("day4_pulse.png", dpi=120); plt.show()
