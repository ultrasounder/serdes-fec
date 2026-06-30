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
def _pulse_from_model(baud: float, sps: int) -> np.ndarray:
    """Day-3 synthetic channel -> pulse. Just your existing inline code, named."""
    R0, L, C, tand = 17.27, 250e-9, 100e-12, 0.02
    length = 0.30
    """build a dense one-sided H(f) on an FFT grid"""
    N, fs = 8192, baud*sps
    f = np.linspace(0, fs/2, N); f[0] = f[1]
    gamma = rlgc_gamma(f, R0, L, C, tand)
    """--- one UI rectangular input, then channel filter ----"""
    """impulse-style: take channel impulse response via irfft"""
    H = np.exp(-gamma*length)
    h = np.fft.irfft(H, n=2*(N-1)); h /= np.max(np.abs(h))
    pulse = np.convolve(h, np.ones(sps))[:4000]
    return pulse / np.max(pulse)

def s4p_to_pulse(path: str | None, baud: float, sps: int) -> np.ndarray:
    """The contract. None -> synthetic; a path -> real .s4p."""
    if path is None:
        return _pulse_from_model(baud, sps)
    import skrf as rf
    ntwk = rf.Network(path)
    ntwk.renumber([0,1,2,3], [0,2,1,3]); ntwk.se2gmm(p=2)
    sdd21, f = ntwk.s[:,1,0], ntwk.f
    N, fs = 4096, baud*sps
    fg = np.linspace(0, fs/2, N)
    H = np.interp(fg, f, sdd21, left=sdd21[0], right=0)
    h = np.fft.irfft(H, n=2*(N-1))
    pulse = np.convolve(h, np.ones(sps))
    return pulse / np.max(np.abs(pulse))