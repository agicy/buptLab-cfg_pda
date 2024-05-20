from exceptions import *
from datastructure.cfg import *

__all__: list[str] = ["eliminate_useless_symbol"]


def eliminate_useless_symbol(cfg: CFG) -> CFG:
    return CFG(N=set(), T=set(), P=set(), S="S")
