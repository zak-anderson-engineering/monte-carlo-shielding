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
    "iron": {
        "density": 7.874,       # g/cm^3
        "coherent": 2.808e-4,
        "incoherent": 5.292e-2,
        "photoelectric": 2.256e-4,
        "pair": 7.031e-5,       # nuclear + electron field
        "total": 5.350e-2,      # with coherent
    },
        "concrete": {
        "density": 2.3,         # g/cm^3, NIST ordinary concrete
        "coherent": 7.093e-5,
        "incoherent": 5.796e-2,
        "photoelectric": 1.516e-5,
        "pair": 2.633e-5,       # nuclear + electron field
        "total": 5.807e-2,      # with coherent
    },
}