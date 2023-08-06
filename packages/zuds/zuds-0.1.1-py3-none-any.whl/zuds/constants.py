import numpy as np
from astropy import units as u
BIG_RMS = np.sqrt(50000.)
BKG_BOX_SIZE = 128
DETECT_NSIGMA = 1.5
DETECT_NPIX = 5
MJD_TO_JD = 2400000.5
MATCH_RADIUS_DEG = 0.0002777 * 2.0
N_PREV_SINGLE = 1
N_PREV_MULTI = 1
RB_ASSOC_MIN = 0.2
CUTOUT_SIZE = 63  # pix
APER_KEY = 'APCOR4'
APERTURE_RADIUS = 3 * u.pixel
GROUP_PROPERTIES = ['field', 'ccdid', 'qid', 'fid']
NTHREADS_PER_NODE = 64
CMAP_RANDOM_SEED = 8675309
RB_CUT = {1: 0.3,
          2: 0.3,
          3: 0.6}
BRAAI_MODEL = 'braai_d6_m9'
MASK_BORDER = 10  # pix
BKG_VAL = 150.  # counts

MASK_BITS = {
    'BIT00': 0,
    'BIT01': 1,
    'BIT02': 2,
    'BIT03': 3,
    'BIT04': 4,
    'BIT05': 5,
    'BIT06': 6,
    'BIT07': 7,
    'BIT08': 8,
    'BIT09': 9,
    'BIT10': 10,
    'BIT11': 11,
    'BIT12': 12,
    'BIT13': 13,
    'BIT14': 14,
    'BIT15': 15,
    'BIT16': 16
}

BAD_BITS = np.asarray([0, 2, 3, 4, 5, 7, 8, 9, 10, 16, 17])
BAD_SUM = int(np.sum(2 ** BAD_BITS))

MASK_COMMENTS = {
    'BIT00': 'AIRCRAFT/SATELLITE TRACK',
    'BIT01': 'CONTAINS SEXTRACTOR DETECTION',
    'BIT02': 'LOW RESPONSIVITY',
    'BIT03': 'HIGH RESPONSIVITY',
    'BIT04': 'NOISY',
    'BIT05': 'GHOST FROM BRIGHT SOURCE',
    'BIT06': 'RESERVED FOR FUTURE USE',
    'BIT07': 'PIXEL SPIKE (POSSIBLE RAD HIT)',
    'BIT08': 'SATURATED',
    'BIT09': 'DEAD (UNRESPONSIVE)',
    'BIT10': 'NAN (not a number)',
    'BIT11': 'CONTAINS PSF-EXTRACTED SOURCE POSITION',
    'BIT12': 'HALO FROM BRIGHT SOURCE',
    'BIT13': 'RESERVED FOR FUTURE USE',
    'BIT14': 'RESERVED FOR FUTURE USE',
    'BIT15': 'RESERVED FOR FUTURE USE',
    'BIT16': 'NON-DATA SECTION FROM SWARP ALIGNMENT'
}

REFERENCE_VERSION = 'zuds5'

ACTIVE_FIELDS = [631, 762, 763, 722, 676, 724, 677,
                 761, 678, 720, 721, 679, 863, 846, 823, 862,
                 845, 822, 793, 844, 759, 821, 719, 792, 758, 791]


SYSTEM_DEPENDENCIES = {
    'psql': (
        ['psql', '--version'],
        lambda v: v.split('\n')[-1].split()[2],
        '9.6',
    ),
    'sextractor (sex)': (
        ['sex', '--version'],
        lambda v: v.split()[2],
        '2.18.0'
    ),
    'swarp': (
        ['swarp', '--version'],
        lambda v: v.split()[2],
        '2.38.0'
    ),
    'hotpants': (
        ['hotpants'],
        lambda v: v.split('\n')[1].split()[-1],
        '5.1.11'
    )
}
