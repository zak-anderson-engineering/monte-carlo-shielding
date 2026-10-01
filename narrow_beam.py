import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from materials import MATERIALS


def linear_mu(material):
    """Linear attenuation coefficient mu in cm^-1 (mass coefficient x density)."""
    m = MATERIALS[material]
    return m["total"] * m["density"]


def simulate_narrow(mu, thickness, n_photons, rng):
    """Fraction of photons that cross a slab without interacting at all."""
    # Each photon travels a random distance s = -ln(U)/mu before its first interaction.
    # 1 - rng.random() gives numbers in (0, 1], so we never take log(0).
    distances = -np.log(1 - rng.random(n_photons)) / mu
    transmitted = np.sum(distances > thickness)
    return transmitted / n_photons


rng = np.random.default_rng(seed=42)   # fixed seed so results are reproducible
material = "lead"
mu = linear_mu(material)
N = 100_000
thicknesses = np.linspace(0, 10, 21)   # 0 to 10 cm in 0.5 cm steps

sim = np.array([simulate_narrow(mu, x, N, rng) for x in thicknesses])
err = np.sqrt(sim * (1 - sim) / N)     # binomial standard error
theory = np.exp(-mu * thicknesses)     # Beer-Lambert

print(f"{material}: mu = {mu:.4f} cm^-1, mean free path = {1/mu:.3f} cm")
for x, s, t in zip(thicknesses, sim, theory):
    print(f"x = {x:4.1f} cm   sim = {s:.5f}   theory = {t:.5f}")

Path("figures").mkdir(exist_ok=True)
plt.errorbar(thicknesses, sim, yerr=err, fmt="o", markersize=4, label="Monte Carlo")
plt.plot(thicknesses, theory, label="Beer-Lambert")
plt.yscale("log")
plt.xlabel("Lead thickness (cm)")
plt.ylabel("Transmitted fraction")
plt.title(f"Narrow-beam transmission through {material}, 1.25 MeV")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.savefig(f"figures/narrow_beam_{material}.png", dpi=150)
plt.show()
