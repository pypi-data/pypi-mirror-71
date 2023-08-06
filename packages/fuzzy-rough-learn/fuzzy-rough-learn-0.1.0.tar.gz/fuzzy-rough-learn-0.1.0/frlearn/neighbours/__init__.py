"""
The :mod:`frlearn.neighbours` subpackage implements nearest neighbour algorithms.
"""

from .classifiers import FuzzyRoughEnsemble, FRNN, FRONEC, FROVOCO
from .neighbour_search import BallTree, KDTree, NNSearch
from .preprocessors import FRFS, FRPS
