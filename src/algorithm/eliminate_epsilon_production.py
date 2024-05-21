from exceptions import *
from datastructure.cfg import *

__all__: list[str] = ["eliminate_epsilon_production"]


def _is_right_nullable(
    cfg: CFG, production: production_t, nullable_symbols: set[nonterminal_t]
) -> bool:
    _, right = production
    return all(symbol in nullable_symbols for symbol in right)


def _get_nullable(
    cfg: CFG, nullable_nonterminals: set[nonterminal_t]
) -> set[nonterminal_t]:
    return {
        symbol
        for production in cfg.P
        if _is_right_nullable(
            cfg=cfg, production=production, nullable_symbols=nullable_nonterminals
        )
        for left, _ in [production]
        for symbol in left
        if symbol in cfg.N
    }


def _get_nullable_nonterminal(cfg: CFG) -> set[nonterminal_t]:
    current_set: set[nonterminal_t] = set()
    next_set: set[nonterminal_t] = current_set | _get_nullable(
        cfg=cfg, nullable_nonterminals=current_set
    )
    while current_set != next_set:
        current_set = next_set
        next_set = current_set | _get_nullable(
            cfg=cfg, nullable_nonterminals=current_set
        )
    return current_set


def eliminate_epsilon_production(cfg: CFG) -> CFG:
    if not cfg.is_valid():
        raise CFGInvalid("Invalid CFG.")
    nullable_nonterminals: set[nonterminal_t] = _get_nullable_nonterminal(cfg)
    new_productions: set[production_t] = set()
    for left_hand, right_hand in cfg.P:
        if not right_hand:
            continue
        nullable_indices: list[int] = [
            i for i, symbol in enumerate(right_hand) if symbol in nullable_nonterminals
        ]
        for i in range(0, 2 ** len(nullable_indices)):
            new_right_hand = list(right_hand)
            for j, index in enumerate(nullable_indices):
                if not (i & (1 << j)):
                    new_right_hand[index] = ""
            filtered_right_hand = tuple(
                symbol for symbol in new_right_hand if symbol is not ""
            )
            if filtered_right_hand:
                new_productions.add((left_hand, filtered_right_hand))
    if cfg.S in nullable_nonterminals and any(cfg.S in right for _, right in cfg.P):
        new_start: nonterminal_t = cfg.S + "'"
        new_nonterminals: set[nonterminal_t] = cfg.N | {new_start}
        new_productions.add(((new_start,), (cfg.S,)))
        new_productions.add(((new_start,), ()))
    else:
        new_nonterminals = cfg.N
        if cfg.S in nullable_nonterminals:
            new_productions.add(((cfg.S,), ()))
        new_start = cfg.S
    return CFG(N=new_nonterminals, T=cfg.T, P=new_productions, S=new_start)
