# Licensed under MIT license - see LICENSE.rst

# Affiliated packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._astropy_init import *
# ----------------------------------------------------------------------------

# For egg_info test builds to pass, put package imports here.
if not _ASTROPY_SETUP_:
    from stingray.lightcurve import *
    from stingray.utils import *
    from stingray.powerspectrum import *
    from stingray.crossspectrum import *
    from stingray import *
    from stingray.exceptions import *
    from stingray.covariancespectrum import *
    from stingray.crosscorrelation import *
    from stingray.stats import *
    from stingray.bispectrum import *
    from stingray.varenergyspectrum import *
