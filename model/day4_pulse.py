import numpy as np, matplotlib.pyplot as plt, scipy.signal as sig
from sys import path; path.append("../model")
from channel import s4p_to_pulse
import skrf as rf
"""Getting the actual pulse response from a .s4p file or a synthetic model"""
baud = 10e9 # baud rate
sps = 32 # samples per symbol
pulse = s4p_to_pulse("model/peters_01_0605_B12_thru.s4p", baud, sps)  # Example values, replace with actual parameters
"""Cursor extraction: find the peak, then find the first zero crossing after the peak"""
main_idx = np.argmax(pulse)
def tap(k):
    i = main_idx + k* sps # k-th UI after the main peak
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

n = rf.Network("model/peters_01_0605_B12_thru.s4p")
n.renumber([0,1,2,3], [0,2,1,3]); n.se2gmm(p=2)
f = n.f; sdd21 = n.s[:,1,0]
i5 = np.argmin(np.abs(f-5e9))
print(f"IL @5GHz = {20*np.log10(abs(sdd21[i5])):.1f} dB")