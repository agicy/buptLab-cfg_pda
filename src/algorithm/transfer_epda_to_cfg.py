from datastructure.cfg import *
from datastructure.pda import *

__all__: list[str] = ["transfer_epda_to_cfg"]


def transfer_epda_to_cfg(epda: PDA) -> CFG:
    return CFG(N=set(), T=set(), P=set(), S="S")
