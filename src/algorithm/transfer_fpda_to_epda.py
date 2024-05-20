from datastructure.pda import *

__all__: list[str] = ["transfer_fpda_to_epda"]


def transfer_fpda_to_epda(fpda: PDA) -> PDA:
    return PDA(Q=set(), T=set(), Gamma=set(), delta={}, q0="q0", Z0="Z", F=set())
