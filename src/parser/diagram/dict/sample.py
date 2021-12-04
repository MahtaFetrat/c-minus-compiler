from src.parser.utils import SymbolType

transition_diagram = [
    {
        "name": "1",
        "predict_set": {"*", "if", "$"},
        "follow_set": {"$"},
        "states": [{"id": 1, "start": True, "end": False}],
        "transitions": [
            {
                "stare_src_id": 1,
                "state_dst_id": 2,
                "type": SymbolType.NON_TERMINAL,
                "name": 2,
            }
        ],
    },
    {
        "name": "2",
        "predict_set": {"else", "+"},
        "follow_set": {"+"},
        "states": [{"id": 1, "start": True, "end": False}],
        "transitions": [
            {
                "stare_src_id": 1,
                "state_dst_id": 2,
                "type": SymbolType.TERMINAL,
                "terminal": "endif",
            }
        ],
    },
    {
        "name": "3",
        "predict_set": {"else", "+"},
        "follow_set": {"+"},
        "states": [{"id": 1, "start": True, "end": False}],
        "transitions": [
            {
                "stare_src_id": 1,
                "state_dst_id": 2,
                "type": SymbolType.EPSILON,
                "predict": {"+"},
            }
        ],
    },
]
