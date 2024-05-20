import pytest
from exceptions import *
from datastructure.cfg import *
from algorithm.eliminate_useless_symbol import *


def test_basic() -> None:
    cfg = CFG(
        N={"S", "A", "B", "C", "D", "E", "F", "G"},
        T={"a"},
        P={
            (("S",), ("A", "B")),
            (("A",), ("a",)),
            (("B",), ("C",)),
            (("C",), ("D",)),
            (("D",), ("a",)),
            (("E",), ("F",)),
            (("F",), ("G",)),
            (("G",), ("E",)),
        },
        S="S",
    )
    new_cfg: CFG = eliminate_useless_symbol(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A", "B", "C", "D"},
        T={"a"},
        P={
            (("S",), ("A", "B")),
            (("A",), ("a",)),
            (("B",), ("C",)),
            (("C",), ("D",)),
            (("D",), ("a",)),
        },
        S="S",
    )

    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_unreachable_symbols() -> None:
    cfg = CFG(
        N={"S", "A", "B", "C", "E"},
        T={"a", "b"},
        P={
            (("S",), ("A", "B")),
            (("A",), ("a",)),
            (("B",), ("b",)),
            (("C",), ()),
        },
        S="S",
    )
    new_cfg: CFG = eliminate_useless_symbol(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={
            (("S",), ("A", "B")),
            (("A",), ("a",)),
            (("B",), ("b",)),
        },
        S="S",
    )

    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_unproductive_symbols() -> None:
    cfg = CFG(
        N={"S", "A", "B", "C"},
        T={"a", "b"},
        P={
            (("S",), ("A", "B")),
            (("A",), ("a",)),
            (("B",), ("b",)),
            (("C",), ("C",)),
            (("C",), ("a", "C", "B")),
        },
        S="S",
    )
    new_cfg: CFG = eliminate_useless_symbol(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={
            (("S",), ("A", "B")),
            (("A",), ("a",)),
            (("B",), ("b",)),
        },
        S="S",
    )

    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_no_useless_symbols() -> None:
    cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={
            (("S",), ("A", "B")),
            (("A",), ("a",)),
            (("B",), ("b",)),
        },
        S="S",
    )
    new_cfg: CFG = eliminate_useless_symbol(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={
            (("S",), ("A", "B")),
            (("A",), ("a",)),
            (("B",), ("b",)),
        },
        S="S",
    )

    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_single_production() -> None:
    cfg = CFG(
        N={"S"},
        T={"a"},
        P={(("S",), ("a",))},
        S="S",
    )
    new_cfg: CFG = eliminate_useless_symbol(cfg=cfg)
    expected_cfg = CFG(
        N={"S"},
        T={"a"},
        P={(("S",), ("a",))},
        S="S",
    )

    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_no_productions() -> None:
    cfg = CFG(
        N={"S"},
        T={"a"},
        P=set(),
        S="S",
    )
    with pytest.raises(expected_exception=CFGEmptyError):
        eliminate_useless_symbol(cfg=cfg)
