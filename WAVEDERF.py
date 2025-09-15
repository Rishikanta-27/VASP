import numpy as np
from scipy.io import FortranFile

def wavederr_to_text(waveder='WAVEDER', outfile='WAVEDERF'):
    # Open the binary WAVEDER file
    f = FortranFile(waveder, 'r')
    
    # Read header
    nb_tot, nbands_cder, nkpts, ispin = f.read_record(dtype=np.int32)
    nodesn = f.read_record(dtype=np.float64)
    wplasmon = f.read_record(dtype=np.float64).reshape(3,3)
    
    print(f"Total bands: {nb_tot}, Bands in cder: {nbands_cder}, K-points: {nkpts}, Spins: {ispin}")
    
    # Read cder array
    cder = f.read_record(dtype=np.complex64)
    cder = cder.reshape(ispin, nkpts, nbands_cder, nb_tot, 3)
    
    # Write to plain-text file
    with open(outfile, 'w') as out:
        out.write(f"{ispin} {nkpts} {nbands_cder}\n")
        for s in range(ispin):
            for k in range(nkpts):
                for b1 in range(nbands_cder):
                    for b2 in range(nb_tot):
                        vals = cder[s, k, b1, b2, :]
                        out.write(f"{s+1} {k+1} {b1+1} {b2+1} ")
                        out.write(" ".join(f"{v.real:.6e} {v.imag:.6e}" for v in vals))
                        out.write("\n")
    
    print(f"Conversion complete. Plain-text file saved as {outfile}")

# Run it
wavederr_to_text('WAVEDER', 'WAVEDERF')
