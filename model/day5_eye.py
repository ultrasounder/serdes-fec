import numpy as np, matplotlib.pyplot as plt
from sys import path; path.append("../model")
from channel import s4p_to_pulse

baud, sps = 10e9, 32
CH = "peters_01_0605_B12_thru.s4p" #your -14dB channel; or None
#CH = None
pulse = s4p_to_pulse(CH, baud, sps)

# -- build RX waveform: convolve random NRZ symbols with the pulse reposne ---

def rx_waveform(pulse, sps, n_sym=4000, seed=0):
    rng = np.random.default_rng(seed)
    syms = rng.choice([-1.0, 1.0], n_sym) #NRZ
    up = np.zeros(n_sym*sps); up[::sps] = syms #Upsample: impulse train
    return np.convolve(up, pulse), syms

rx, syms = rx_waveform(pulse, sps)

# -- fold into an eye (2 UI wide) ---
def eye_matrix(rx, sps, n_ui=2, skip=200):
    seg = n_ui*sps
    start = skip*sps
    usable = rx[start:] #everything after warmup
    n = len(usable) // seg #whole segments only
    usable = usable[:n*seg] #trim the remainder (the +12)
    return usable.reshape(n, seg)
eye = eye_matrix(rx, sps)

# -- eye height/width at center phase

def eye_height_aligned(rx, syms, pulse, sps, skip=200):
    delay=np.argmax(pulse)
    idx = skip + np.arange(len(syms) - skip - 10)
    samp = rx[delay + idx*sps]
    s = syms[idx]
    ones = samp[s > 0]
    zeros = samp[s < 0]
    #worst-case opening: lowest "1" minus highest "0"
    eye_h = ones.min() - zeros.max()
    #also useful: separation of the *means* (clean, outlier-robust)
    eye_mean = ones.mean() - zeros.mean()
    return eye_h, eye_mean, ones, zeros

eye_h, eye_mean, ones, zeros = eye_height_aligned(rx, syms, pulse, sps)
plt.title(f"Eye @10GBd (worst-case h={eye_h:.3f}, mean-sep={eye_mean:.3f})")
plt.tight_layout();plt.savefig("day5_eye.png", dpi=120); plt.show()


# plot
t = np.linspace(0, 2, eye.shape[1])
plt.figure(figsize=(6, 4))
for row in eye[:400]:
    plt.plot(t, row, 'b', lw=0.3, alpha=0.3)
plt.axvline(1.0, color='k', ls=':');
plt.axhline(0, color='k', ls=':')
plt.xlabel("Time (UI)");
plt.ylabel("Amplitude")
plt.title(f"Eye @10GBd, unequalized (height={eye_h:.3f})")
plt.tight_layout();
plt.savefig("day5_eye.png", dpi=120);
plt.show()

from scipy.special import erfc
def q(x):
    return 0.5*erfc(x/np.sqrt(2))
sigma = 0.05 # RX Noise RMS start here and we will sweep
ber = q((eye_h/2)/sigma) if eye_h > 0 else 0.5
print(f"sigma={sigma}: eye_h={eye_h:.3f} -> BER ~ {ber:.2e}")



    

