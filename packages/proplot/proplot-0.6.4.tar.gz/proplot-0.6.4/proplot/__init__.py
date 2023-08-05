#!/usr/bin/env python3
"""
A python package for making beautiful, publication-quality graphics.
"""
# For now import everything into the top-level module namespace
# In the future we will not import the class names
import pkg_resources as _pkg
from .config import *  # noqa: F401 F403
from .internals import timers
with timers._benchmark('imports'):
    from .utils import *  # noqa: F401 F403
    from .crs import *  # noqa: F401 F403
    from .colors import *  # noqa: F401 F403
    from .ticker import *  # noqa: F401 F403
    from .scale import *  # noqa: F401 F403
    from .gridspec import *  # noqa: F401 F403
    from .constructor import *  # noqa: F401 F403
    from .axes import *  # noqa: F401 F403
    from .figure import *  # noqa: F401 F403
    from .ui import *  # noqa: F401 F403
    from .demos import *  # noqa: F401 F403

# SCM versioning
name = 'proplot'
try:
    version = __version__ = _pkg.get_distribution(__name__).version
except _pkg.DistributionNotFound:
    version = __version__ = 'unknown'
