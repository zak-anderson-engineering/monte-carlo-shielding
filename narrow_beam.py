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


rng = np.random.default_rng(seed=42)
N = 100_000
thicknesses = np.linspace(0, 10, 21)   # cm

Path("figures").mkdir(exist_ok=True)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

for material in MATERIALS:
    mu = linear_mu(material)
    rho = MATERIALS[material]["density"]
    sim = np.array([simulate_narrow(mu, x, N, rng) for x in thicknesses])
    err = np.sqrt(sim * (1 - sim) / N)
    theory = np.exp(-mu * thicknesses)
    print(f"{material}: mu = {mu:.4f} cm^-1, mean free path = {1/mu:.2f} cm")

    # Left: transmission vs physical thickness
    line, = ax1.plot(thicknesses, theory, label=material)
    ax1.errorbar(thicknesses, sim, yerr=err, fmt="o", markersize=3, color=line.get_color())

    # Right: transmission vs mass thickness (thickness x density)
    mass_thickness = thicknesses * rho
    ax2.plot(mass_thickness, theory, color=line.get_color(), label=material)
    ax2.errorbar(mass_thickness, sim, yerr=err, fmt="o", markersize=3, color=line.get_color())

ax1.set_xlabel("Thickness (cm)")
ax1.set_title("Per cm: lead wins easily")
ax2.set_xlabel("Mass thickness (g/cm$^2$)")
ax2.set_title("Per gram: almost identical (Compton-dominated)")
for ax in (ax1, ax2):
    ax.set_yscale("log")
    ax.set_ylabel("Transmitted fraction")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
fig.suptitle("Narrow-beam transmission at 1.25 MeV: Monte Carlo (points) vs Beer-Lambert (lines)")
fig.tight_layout()
fig.savefig("figures/narrow_beam_all.png", dpi=150)
plt.show()