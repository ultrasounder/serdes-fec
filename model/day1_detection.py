import numpy as np, matplotlib.pyplot as plt
from scipy.stats import norm

def ml_thresholds(levels, priors=None):
    """Given a set of levels, return the ML decision thresholds. If priors are given, use them for MAP."""
    levels = np.sort(np.asarray(levels, float))
    mids = (levels[:-1] + levels[1:]) / 2 #ML midpoints
    if priors is None:
        return mids
    
    #MAP correction for adjacent pair (equal-variance Gaussian assumption):
    # threshold = midpoint + (sigma^2 / (Li+1 - Li)) * ln(P(Li)/P(Li+1))
    return mids # extend with prior shift in the excercise
def decide(y, levels, thresholds):
    """slice y into nearest symbol using thresholds"""
    idx = np.searchsorted(thresholds, y)
    return np.asarray(levels)[np.clip(idx, 0, len(levels)-1)]
# --demo: NRZ, show ML=MAP under equal priors--
A, sigma = 1.0, 0.3
levels = np.array([-A, A])
thr = ml_thresholds(levels)
print(f"ML thresholds = {thr}")  # -> [0.0]

# visualize the two likelihood Gaussians + threshold
y = np.linspace(-3, 3, 500)
plt.figure(figsize=(7, 4))
plt.plot(y, norm.pdf(y, -A, sigma), label="p(y|x=-1)")
plt.plot(y, norm.pdf(y, A, sigma), label="p(y|x=1)")
for t in thr: plt.axvline(t, color='k', ls='--', label=f"threshold={t}")
plt.fill_between(y, norm.pdf(y, -A, sigma), where=(y>0), alpha=0.2, color='r', label="P(error | x=-1)")
plt.xlabel("y"); plt.ylabel("likelihood");plt.legend(); plt.grid(alpha=0.3)
plt.title("ML decision threshold for NRZ (equal priors)")
plt.tight_layout(); plt.savefig("day1_detection.png", dpi=120); plt.show()


# --prove MAP shifts threshold when priors are skewed ---
def map_threshold_nrz(A, sigma, p_plus):
    """Closed form: threshold = (sigma^2 / (2A)) * ln((1-p_plus)/p_plus)"""
    return (sigma**2 / (2*A)) * np.log((1-p_plus)/p_plus)

for p in [0.5, 0.7, 0.9]:
    print(f"p(+)= {p}: MAP threshold = {map_threshold_nrz(A, sigma, p):.3f}")
    