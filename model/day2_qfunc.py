import numpy as np, matplotlib.pyplot as plt, scipy.signal as sig
from scipy.special import erfc

def q(x):
    return 0.5*erfc(x/np.sqrt(2))

def ber_nrz(snr_db):
    """Given SNR in dB, return the BER for NRZ (2-PAM)"""
    snr = 10**(snr_db/10)
    return q(np.sqrt(snr))

def ber_pam4(snr_db):
    """Given SNR in dB, return the BER for 4-PAM (Gray coded)"""
    snr = 10**(snr_db/10)
    return (0.75)*q(np.sqrt(snr/3))

snr = np.linspace(0, 25, 100)
plt.figure(figsize=(7, 4))
plt.semilogy(snr, [ber_nrz(s) for s in snr], label="NRZ")
plt.semilogy(snr, [ber_pam4(s) for s in snr], label="4 PAM")
plt.axhline(1e-12, color='g', ls=":", label="1e-12 target")
plt.axhline(2.4e-4, color='r', ls=':', label="KP4 pre-FEC threshold")
plt.xlabel("SNR (dB, A/N ratio)"); plt.ylim(1e-15, 1); plt.legend(); plt.grid(alpha=0.3, which='both')
plt.title("BER vs SNR"); plt.ylim(1e-15, 1); plt.tight_layout(); plt.savefig("day2_qfunc.png", dpi=120); plt.show()

#the catastrophic-collapse demonstration: 4-PAM has a much higher slope than NRZ, so if you are just above the threshold, you are in trouble
from scipy.optimize import brentq
snr_nrz = brentq(lambda s: ber_nrz(s)-1e-12, 1, 30)
snr_pam4 = brentq(lambda s: ber_pam4(s)-1e-12, 1, 30)
print(f"\n@BER=1e-12, NRZ SNR={snr_nrz:.2f} dB, 4-PAM SNR={snr_pam4:.2f} dB")
print(f"PAM4 penalty = {snr_pam4-snr_nrz:.2f} dB\n")
s = 16
print(f"@16dB: NRZ={ber_nrz(16):.2e}  PAM4={ber_pam4(16):.2e}")
# CORRECT: PAM4 BER must be LARGER (worse) than NRZ
# e.g. NRZ~7e-11, PAM4~1e-2
