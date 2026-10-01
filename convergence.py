import numpy as np
import matplotlib.pyplot as plt
from narrow_beam import linear_mu, simulate_narrow

rng = np.random.default_rng(seed=1)
material = "lead"
x = 5.0                      # slab thickness in cm
mu = linear_mu(material)
T = np.exp(-mu * x)          # exact Beer-Lambert answer

Ns = np.logspace(2, 6, 9).astype(int)   # 100 up to 1,000,000 photons
trials = 20                             # repeat each N to measure the scatter

rms_errors = []
for N in Ns:
    results = np.array([simulate_narrow(mu, x, N, rng) for _ in range(trials)])
    rms = np.sqrt(np.mean((results - T) ** 2))
    rms_errors.append(rms)
    print(f"N = {N:>8d}   RMS error = {rms:.2e}")
rms_errors = np.array(rms_errors)

# Fit a straight line on log-log axes; the slope should be about -0.5
slope, intercept = np.polyfit(np.log10(Ns), np.log10(rms_errors), 1)
print(f"Fitted slope: {slope:.3f} (expected -0.5)")

expected = np.sqrt(T * (1 - T) / Ns)
plt.loglog(Ns, rms_errors, "o", label="Measured RMS error (20 runs each)")
plt.loglog(Ns, expected, label=r"Theory: $\sqrt{T(1-T)/N}$")
plt.xlabel("Number of photons N")
plt.ylabel
plt.savefig("figures/convergence.png", dpi=150)
plt.show()