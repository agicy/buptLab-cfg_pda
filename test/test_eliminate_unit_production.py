import pytest
from exceptions import *
from datastructure.cfg import *
from algorithm.eliminate_unit_production import *


def test_basic() -> None:
    cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={(("S",), ("A",)), (("S",), ("a",)), (("A",), ("B",)), (("B",), ("b",))},
        S="S",
    )
    new_cfg: CFG = eliminate_unit_production(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={(("S",), ("b",)), (("S",), ("a",)), (("A",), ("b",)), (("B",), ("b",))},
        S="S",
    )
    print(new_cfg.P)
    print(expected_cfg.P)
    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_no_unit_productions() -> None:
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
    new_cfg: CFG = eliminate_unit_production(cfg=cfg)
    assert new_cfg.N == cfg.N
    assert new_cfg.T == cfg.T
    assert new_cfg.P == cfg.P
    assert new_cfg.S == cfg.S


def test_cyclic_unit_productions() -> None:
    cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={(("S",), ("A",)), (("A",), ("B",)), (("A",), ("a",)), (("B",), ("A",))},
        S="S",
    )
    new_cfg: CFG = eliminate_unit_production(cfg=cfg)
    expected_cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={(("S",), ("a",)), (("A",), ("a",)), (("B",), ("a",))},
        S="S",
    )
    assert new_cfg.N == expected_cfg.N
    assert new_cfg.T == expected_cfg.T
    assert new_cfg.P == expected_cfg.P
    assert new_cfg.S == expected_cfg.S


def test_invalid_CFG() -> None:
    cfg = CFG(
        N={"S", "A", "B"},
        T={"a", "b"},
        P={(("S",), ("a",)), (("S",), ("a",)), (("A",), ("B",)), (("B",), ("C",))},
        S="S",
    )
    with pytest.raises(expected_exception=CFGInvalid):
        eliminate_unit_production(cfg=cfg)
