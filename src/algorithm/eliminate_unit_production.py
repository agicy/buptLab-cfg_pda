from exceptions import *
from datastructure.cfg import *

__all__: list[str] = ["eliminate_unit_production"]


def _is_unit_production(cfg: CFG, production: production_t) -> bool:
    left, right = production
    is_left_unit: bool = len(left) == 1 and left[0] in cfg.N
    is_right_unit: bool = len(right) == 1 and right[0] in cfg.N
    return is_left_unit and is_right_unit


def _get_unit_reachable(
    unit_productions: set[production_t], symbols: set[nonterminal_t]
) -> set[nonterminal_t]:
    return {left[0] for left, right in unit_productions if right[0] in symbols}


def _get_unit_production_left_side(
    unit_productions: set[production_t], symbol: nonterminal_t
) -> set[nonterminal_t]:
    current_set: set[nonterminal_t] = {symbol}
    next_set: set[nonterminal_t] = current_set.union(
        _get_unit_reachable(unit_productions=unit_productions, symbols=current_set)
    )
    while current_set != next_set:
        current_set = next_set
        next_set = current_set | _get_unit_reachable(
            unit_productions=unit_productions, symbols=current_set
        )
    return current_set


def eliminate_unit_production(cfg: CFG) -> CFG:
    if not cfg.is_valid():
        raise CFGInvalid("Invalid CFG.")
    unit_productions: set[production_t] = {
        production
        for production in cfg.P
        if _is_unit_production(cfg=cfg, production=production)
    }
    new_productions: set[production_t] = set()
    for symbol in cfg.N:
        unit_reachable_symbols: set[nonterminal_t] = _get_unit_production_left_side(
            unit_productions=unit_productions, symbol=symbol
        )
        rights: set[tuple[symbol_t, ...]] = {
            right
            for left, right in cfg.P
            if left == (symbol,) and (len(right) != 1 or (right[0] in cfg.T))
        }
        for right in rights:
            for left_symbol in unit_reachable_symbols:
                new_productions.add(((left_symbol,), right))
    return CFG(N=cfg.N, T=cfg.T, P=new_productions, S=cfg.S)
