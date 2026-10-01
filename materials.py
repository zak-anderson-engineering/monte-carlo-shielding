# Mass attenuation coefficients at 1.25 MeV, in cm^2/g
# Source: NIST XCOM (physics.nist.gov/PhysRefData/Xcom)

MATERIALS = {
    "lead": {
        "density": 11.35,       # g/cm^3
        "coherent": 1.930e-3,
        "incoherent": 4.476e-2,
        "photoelectric": 1.168e-2,
        "pair": 3.781e-4,       # nuclear + electron field
        "total": 5.875e-2,      # with coherent
    },
}