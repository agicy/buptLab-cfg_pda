import pytest
from exceptions import *
from datastructure.cfg import *


def test_is_valid_valid_cfg() -> None:
    cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={
            (("S",), ("A",)), 
            (("A",), ("a",)), 
            (("A",), ("B",)), 
            (("B",), ("b",))
        },
        S="S",
    )
    assert cfg.is_valid()


def test_is_valid_invalid_cfg() -> None:
    cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={
            (("S",), ("A",)),
            (("A",), ("C",)),
            (("B",), ("b",)),
        },
        S="S",
    )
    assert not cfg.is_valid()


def test_to_string_valid_cfg() -> None:
    cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={
            (("S",), ("A",)),
            (("S",), ("B", "A",), ),
            (("A",), ("a",)),
            (("A",), ("B",)),
            (("B",), ("b",)),
        },
        S="S",
    )
    expected_string: str = """\
N = { A, B, S }
T = { a, b }
P:
A -> B | a
B -> b
S -> A | B A
S = S\
"""
    assert cfg.to_string() == expected_string


def test_to_string_invalid_cfg() -> None:
    cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={
            (("S",), ("A",)), 
            (("A",), ("C",)), 
            (("B",), ("b",))},
        S="S",
    )
    with pytest.raises(expected_exception=CFGInvalid):
        cfg.to_string()
