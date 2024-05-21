from datastructure.pda import *

__all__: list[str] = ["transfer_fpda_to_epda"]


def transfer_fpda_to_epda(fpda: PDA) -> PDA:

    epda_q0 = fpda.q0 + "'"
    epda_Z0 = fpda.Z0 + "'"
    epda_qf = fpda.q0 + "''"

    epda_Q = fpda.Q | {epda_q0, epda_qf}
    epda_T = fpda.T
    epda_Gamma = fpda.Gamma | {epda_Z0}
    epda_delta = fpda.delta
    epda_F = set[state_t]()

    epda_delta[(epda_q0, "", epda_Z0)] = {(fpda.q0, (fpda.Z0, epda_Z0))}
    for Z in epda_Gamma:
        for f in fpda.F:
            if (f, "", Z) not in epda_delta:
                epda_delta[(f, "", Z)] = set()
            epda_delta[(f, "", Z)].add((epda_qf, ()))
        epda_delta[(epda_qf, "", Z)] = {(epda_qf, ())}

    return PDA(
        Q=epda_Q,
        T=epda_T,
        Gamma=epda_Gamma,
        delta=epda_delta,
        q0=epda_q0,
        Z0=epda_Z0,
        F=epda_F,
    )
