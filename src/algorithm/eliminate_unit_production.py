from exceptions import *
from datastructure.cfg import *

__all__: list[str] = ["eliminate_unit_production"]


def eliminate_unit_production(cfg: CFG) -> CFG:
    return CFG(N=set(), T=set(), P=set(), S="S")
