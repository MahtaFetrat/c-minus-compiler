from functools import reduce
from operator import concat

from src.scanner.dfa.dict import *
#
# __all__ = list(map(lambda x: x(), [
#     InitialDict, NUMDFADict,
#     KEYIDDFADict, STARDFADict,
#     SYMBOLDFADict, EQUALDFADict,
#     COMMENTDFADict, WHITESPACEDFADict
# ]))
#
# DFA_DICT: Dict[str, Any] = {
#     'states': reduce(concat, [x.states for x in __all__]),
#     'transitions': reduce(concat, [x.transitions for x in __all__])
# }
