import numpy as np
import matplotlib.pyplot as plt
from materials import MATERIALS


def simulate_broad(material, thickness, n_photons, rng):
    """Fraction of photons transmitted when scattering is included.

    Simplified model: scattering is isotropic and the photon keeps its
    energy (real Compton scattering is forward-peaked and loses energy).
    """
    m = MATERIALS[material]
    mu = m["total"] * m["density"]
    p_scatter = (m["coherent"] + m["incoherent"]) / m["total"]

    transmitted = 0
    for _ in range(n_photons):
        z = 0.0            # depth into the slab (cm)
        cos_theta = 1.0    # direction: 1 = straight in, -1 = straight back
        while True:
            s = -np.log(1 - rng.random()) / mu
            z += s * cos_theta
            if z >= thickness:
                transmitted += 1          # got through the back face
                break
            if z < 0:
                break                     # escaped back out the front
            if rng.random() < p_scatter:
                cos_theta = 2 * rng.random() - 1   # isotropic new direction
            else:
                break                     # absorbed
    return transmitted / n_photons


if __name__ == "__main__":
    rng = np.random.default_rng(seed=7)
    N = 20_000
    mfps = np.arange(0, 6.5, 0.5)     # thickness in mean free paths (mu * x)

    for material in MATERIALS:
        m = MATERIALS[material]
        mu = m["total"] * m["density"]
        T_narrow = np.exp(-mfps)
        T_broad = np.array([simulate_broad(material, n / mu, N, rng) for n in mfps])
        B = T_broad / T_narrow
        B_err = np.sqrt(T_broad * (1 - T_broad) / N) / T_narrow

        print(f"\n{material} (scatter probability {(m['coherent'] + m['incoherent']) / m['total']:.2f})")
        for n, b in zip(mfps, B):
            print(f"  {n:.1f} mfp   B = {b:.2f}")

        plt.errorbar(mfps, B, yerr=B_err, fmt="o-", markersize=4, label=material)

    plt.xlabel("Thickness (mean free paths, $\\mu x$)")
    plt.ylabel("Buildup factor B")
    plt.title("Buildup factor at 1.25 MeV (simplified isotropic scattering)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("figures/buildup.png", dpi=150)
    plt.show()