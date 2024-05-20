from datastructure.pda import PDA
from datastructure.cfg import CFG
from algorithm.transfer_epda_to_cfg import transfer_epda_to_cfg
from algorithm.transfer_fpda_to_epda import transfer_fpda_to_epda


def test_pda_to_cfg() -> None:
    pda = PDA(
        Q={"q0", "q1"},
        T={"a", "b"},
        Gamma={"Z0", "A"},
        delta={
            ("q0", "a", "Z0"): {("q0", ("A", "Z0"))},
            ("q0", "a", "A"): {("q0", ("A", "A"))},
            ("q0", "b", "A"): {("q1", ())},
            ("q1", "b", "A"): {("q1", ())},
            ("q1", "", "A"): {("q1", ())},
            ("q1", "", "Z0"): {("q1", ())},
        },
        q0="q0",
        Z0="Z0",
        F=set(),
    )

    target_cfg = CFG(
        N={
            "S",
            "q0_Z0_q0",
            "q0_Z0_q1",
            "q1_Z0_q0",
            "q1_Z0_q1",
            "q0_A_q0",
            "q0_A_q1",
            "q1_A_q0",
            "q1_A_q1",
        },
        T={"a", "b"},
        P={
            (("S",), ("q0_Z0_q0",)),
            (("S",), ("q0_Z0_q1",)),
            (("q0_Z0_q0",), ("a", "q0_A_q0", "q0_Z0_q0")),
            (("q0_Z0_q0",), ("a", "q0_A_q1", "q1_Z0_q0")),
            (("q0_Z0_q1",), ("a", "q0_A_q0", "q0_Z0_q1")),
            (("q0_Z0_q1",), ("a", "q0_A_q1", "q1_Z0_q1")),
            (("q0_A_q0",), ("a", "q0_A_q0", "q0_A_q0")),
            (("q0_A_q0",), ("a", "q0_A_q1", "q1_A_q0")),
            (("q0_A_q1",), ("a", "q0_A_q0", "q0_A_q1")),
            (("q0_A_q1",), ("a", "q0_A_q1", "q1_A_q1")),
            (("q0_A_q1",), ("b",)),
            (("q1_Z0_q1",), ()),
            (("q1_A_q1",), ()),
            (("q1_A_q1",), ("b",)),
        },
        S="S",
    )

    epda: PDA = pda if pda.is_epda() else transfer_fpda_to_epda(pda)
    assert epda.is_valid() and epda.is_epda()
    cfg: CFG = transfer_epda_to_cfg(epda)
    print(cfg.to_string())
    assert cfg.is_valid()
    assert cfg.N == target_cfg.N
    assert cfg.T == target_cfg.T
    assert cfg.P == target_cfg.P
    assert cfg.S == target_cfg.S
