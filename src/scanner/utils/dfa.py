from functools import reduce
from operator import concat
from typing import Any, Dict

from src.scanner.utils.creator import *

__all__ = list(map(lambda x: x(), [
    BaseCreator, NUMCreator,
    KEYIDCreator, STARCreator,
    SYMBOLCreator, EQUALCreator,
    COMMENTCreator, WHITESPACECreator
]))

DFA_DICT: Dict[str, Any] = {
    'states': reduce(concat, [x.states for x in __all__]),
    'transitions': reduce(concat, [x.transitions for x in __all__])
}
