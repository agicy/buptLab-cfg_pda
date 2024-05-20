from exceptions import *
from datastructure.cfg import *

__all__: list[str] = ["eliminate_useless_symbol"]


def _is_left_contained(
    cfg: CFG, production: production_t, symbols: set[nonterminal_t]
) -> bool:
    left, _ = production
    return all(symbol not in cfg.N or symbol in symbols for symbol in left)


def _is_right_contained(
    cfg: CFG, production: production_t, symbols: set[nonterminal_t]
) -> bool:
    _, right = production
    return all(symbol not in cfg.N or symbol in symbols for symbol in right)


def _get_reachable(cfg: CFG, symbols: set[nonterminal_t]) -> set[nonterminal_t]:
    return {
        symbol
        for production in cfg.P
        if _is_left_contained(cfg=cfg, production=production, symbols=symbols)
        for _, right in [production]
        for symbol in right
        if symbol in cfg.N
    }


def _get_reachable_nonterminal(
    cfg: CFG,
) -> set[nonterminal_t]:
    current_set: set[nonterminal_t] = {cfg.S}
    next_set: set[nonterminal_t] = (
        _get_reachable(cfg=cfg, symbols=current_set) | current_set
    )
    while current_set != next_set:
        current_set = next_set
        next_set = _get_reachable(cfg=cfg, symbols=current_set) | current_set
    return current_set


def _get_productive(cfg: CFG, symbols: set[nonterminal_t]) -> set[nonterminal_t]:
    return {
        symbol
        for production in cfg.P
        if _is_right_contained(cfg=cfg, production=production, symbols=symbols)
        for left, _ in [production]
        for symbol in left
        if symbol in cfg.N
    }


def _get_productive_nonterminal(
    cfg: CFG,
) -> set[nonterminal_t]:
    current_set: set[nonterminal_t] = set()
    next_set: set[nonterminal_t] = (
        _get_productive(cfg=cfg, symbols=current_set) | current_set
    )
    while current_set != next_set:
        current_set = next_set
        next_set = _get_productive(cfg=cfg, symbols=current_set) | current_set
    return current_set


def _reduce_grammar_by_nonterminal(cfg: CFG, nonterminals: set[nonterminal_t]) -> CFG:
    new_productions: set[production_t] = {
        production
        for production in cfg.P
        if all(
            symbol in cfg.T or symbol in nonterminals
            for part in production
            for symbol in part
        )
    }

    new_terminals: set[terminal_t] = {
        symbol
        for production in new_productions
        for part in production
        for symbol in part
        if symbol not in nonterminals
    }
    new_nonterminals: set[nonterminal_t] = nonterminals
    new_start = cfg.S
    return CFG(N=new_nonterminals, T=new_terminals, P=new_productions, S=new_start)


def eliminate_useless_symbol(cfg: CFG) -> CFG:
    if not cfg.is_valid():
        raise CFGInvalid("Invalid CFG.")
    nonterminals: set[nonterminal_t] = _get_productive_nonterminal(cfg=cfg)
    if cfg.S not in nonterminals:
        raise CFGEmptyError("CFG is empty.")
    cfg = _reduce_grammar_by_nonterminal(cfg=cfg, nonterminals=nonterminals)
    nonterminals: set[nonterminal_t] = _get_reachable_nonterminal(cfg=cfg)
    if cfg.S not in nonterminals:
        raise CFGEmptyError("CFG is empty.")
    cfg = _reduce_grammar_by_nonterminal(cfg=cfg, nonterminals=nonterminals)
    return cfg
