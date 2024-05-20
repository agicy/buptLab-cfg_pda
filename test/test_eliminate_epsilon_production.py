from datastructure.cfg import *
from algorithm.eliminate_epsilon_production import *
from datastructure.cfg import CFG


def test_empty_production() -> None:
    cfg = CFG(N={"S"}, T=set(), P={(("S",), ())}, S="S")
    new_cfg: CFG = eliminate_epsilon_production(cfg=cfg)
    expected_cfg = CFG(
        N={"S"},
        T=set(),
        P={(("S",), ())},
        S="S",
    )
    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_single_nonterminal() -> None:
    cfg = CFG(N={"S", "A"}, T=set(), P={(("S",), ("A",)), (("A",), ())}, S="S")
    new_cfg: CFG = eliminate_epsilon_production(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A"},
        T=set(),
        P={(("S",), ()), (("S",), ("A",))},
        S="S",
    )
    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_multiple_nonterminals() -> None:
    cfg = CFG(
        N={"S", "A", "B"},
        T=set(),
        P={(("S",), ("A", "B")), (("A",), ()), (("B",), ())},
        S="S",
    )
    new_cfg: CFG = eliminate_epsilon_production(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A", "B"},
        T=set(),
        P={(("S",), ()), (("S",), ("A",)), (("S",), ("B",)), (("S",), ("A", "B"))},
        S="S",
    )
    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_direct_empty_production() -> None:
    cfg = CFG(
        N={"S", "A"},
        T={"a"},
        P={(("S",), ("A",)), (("A",), ()), (("S",), ("a",))},
        S="S",
    )
    new_cfg: CFG = eliminate_epsilon_production(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A"},
        T={"a"},
        P={(("S",), ()), (("S",), ("A",)), (("S",), ("a",))},
        S="S",
    )
    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_indirect_empty_production() -> None:
    cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={
            (("S",), ("A", "B")),
            (("A",), ("a",)),
            (("B",), ("b",)),
            (("A",), ()),
            (("B",), ()),
        },
        S="S",
    )
    new_cfg: CFG = eliminate_epsilon_production(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={
            (("S",), ()),
            (("S",), ("A", "B")),
            (("S",), ("A",)),
            (("S",), ("B",)),
            (("A",), ("a",)),
            (("B",), ("b",)),
        },
        S="S",
    )
    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_multiple_productions() -> None:
    cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={
            (("S",), ("A", "B")),
            (("A",), ("a",)),
            (("A",), ()),
            (("B",), ("b",)),
            (("B",), ("a",)),
            (("B",), ()),
        },
        S="S",
    )
    new_cfg: CFG = eliminate_epsilon_production(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={
            (("S",), ()),
            (("S",), ("A", "B")),
            (("S",), ("A",)),
            (("S",), ("B",)),
            (("A",), ("a",)),
            (("B",), ("b",)),
            (("B",), ("a",)),
        },
        S="S",
    )
    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_complex_cfg() -> None:
    cfg = CFG(
        N={"S", "A", "B", "C"},
        T={"a", "b", "c"},
        P={
            (("S",), ("A", "B")),
            (("A",), ("a", "B")),
            (("A",), ("A",)),
            (("B",), ("b", "C")),
            (("B",), ()),
            (("C",), ("c",)),
            (("C",), ()),
        },
        S="S",
    )
    new_cfg: CFG = eliminate_epsilon_production(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A", "B", "C"},
        T={"a", "b", "c"},
        P={
            (("S",), ("A", "B")),
            (("S",), ("A",)),
            (("A",), ("a", "B")),
            (("A",), ("a",)),
            (("A",), ("A",)),
            (("B",), ("b", "C")),
            (("B",), ("b",)),
            (("C",), ("c",)),
        },
        S="S",
    )
    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_no_new_start_symbol() -> None:
    cfg = CFG(
        N={"S", "A"},
        T={"a"},
        P={(("S",), ("A",)), (("A",), ()), (("S",), ("a",))},
        S="S",
    )
    new_cfg: CFG = eliminate_epsilon_production(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A"},
        T={"a"},
        P={
            (("S",), ()),
            (("S",), ("A",)),
            (("S",), ("a",)),
        },
        S="S",
    )
    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_new_start_symbol() -> None:
    cfg = CFG(
        N={"S", "A"},
        T={"a"},
        P={(("S",), ("A",)), (("A",), ()), (("S",), ("a",)), (("A",), ("S",))},
        S="S",
    )
    new_cfg: CFG = eliminate_epsilon_production(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A", "S'"},
        T={"a"},
        P={
            (("S'",), ("S",)),
            (("S'",), ()),
            (("S",), ("A",)),
            (("S",), ("a",)),
            (("A",), ("S",)),
        },
        S="S'",
    )
    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_no_empty_production() -> None:
    cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={(("S",), ("A", "B")), (("A",), ("a",)), (("B",), ("b",))},
        S="S",
    )
    new_cfg: CFG = eliminate_epsilon_production(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={(("S",), ("A", "B")), (("A",), ("a",)), (("B",), ("b",))},
        S="S",
    )
    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S
