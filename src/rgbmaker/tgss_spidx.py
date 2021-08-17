from astropy.io import fits
import numpy as np

def find_spidx(spidx_file,c, r):
    """bash:
    >>> find_spidx('spidxcat_v1.1b.fits', c)
    >>> [212.52272467 212.43975207 212.47209909 212.46530053 212.39858977
        212.40165324],[-3.11523434 -3.03256748 -3.07505213 -3.0517433  -2.9848956  -2.96384673], 
        [-0.842 -0.488 -0.872 -0.308 -0.615 -0.471]

    Parameters:
    ----------
        spidx_file  : spidx fits file (approx 111 MB) with Fitsrec type table in hdul[1]
        c           : Astropy SkyCoord type RA, DEC (astropy unit - degrees)
        radius (r)  : Astropy unit in degree for the sky angular size.
        

    Returns:
    --------
        xi, yi, spidx : RA(unitless), DEC(unitless) and corrosponding Spectral Index values
                        that can be plotted on plot using wcs.world_to_pixel()

    TODO: add capability/parameter to change radius (epsilon)
    """

    # ------- 
    spidx_hdul = fits.open(spidx_file)
    t = spidx_hdul[1].data
    
    # ------- 
    ra, dec =c.ra.deg, c.dec.deg
    epsilon = r.value # expected r in astropy unit degree
    print(f'spidx search is roughly within {epsilon*60} arcmin')
    i_spidx = np.where( np.abs(t.DEC-dec) < epsilon )
    true_spidx = np.where( np.abs(t.RA[i_spidx]-ra) < epsilon )
    xi,yi,spidx = t.RA[i_spidx][true_spidx], t.DEC[i_spidx][true_spidx], np.round(np.double(t.Spidx[i_spidx][true_spidx]),3)
    if (not hasattr(spidx, '__len__')) and (not isinstance(spidx, str)) :
        spidx = [spidx]
        xi = [xi]
        yi = [yi]
    return xi, yi, spidx
    