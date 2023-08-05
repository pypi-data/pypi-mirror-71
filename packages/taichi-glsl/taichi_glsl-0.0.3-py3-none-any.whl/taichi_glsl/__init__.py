'''
Manipulate Taichi with GLSL-alike helper functions.
'''

import taichi as ti
import numpy as np
import math

from .version import version as __version__
print(f'[TaiGLSL] version {__version__}')

from .hack import *
from .glsl import *
from .array import *
from .linalg import *
from .transform import *
from .rand import *
