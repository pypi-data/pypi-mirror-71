"""Flatbread Library
=================

The Flatbread Library provides a collection of modules for presenting data.
"""

from flatbread.utils import log
from flatbread.utils import sanity
from flatbread.utils import readout
from flatbread.core import aggregation
from flatbread.core import aggregation as agg
from flatbread.core import assign
from flatbread.core import load
from flatbread.core import select
from flatbread.core import copy
from flatbread.core import drop
from flatbread.core.axes import columns
from flatbread.core.axes import columns as cols
from flatbread.core.axes import index
from flatbread.core.axes import index as idx
from flatbread.core.axes import index as rows
from flatbread import present
from flatbread.present.format import formatter
from flatbread.present.trendline import TrendLine

__version__ = '0.0.7'
__license__ = 'GPLv3+'
__author__  = 'L.C. Vriend'
__email__   = 'vanboefer@gmail.com'
__credits__ = ['L.C. Vriend']


@log.entry
def init(df, **kwargs):
    return df
