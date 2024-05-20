from datastructure.cfg import *
from datastructure.pda import *
import itertools

__all__: list[str] = ["transfer_epda_to_cfg"]


def _eliminate_none(input: tuple[symbol_t, ...]) -> tuple[symbol_t, ...]:
    return tuple(filter(None, input))


def transfer_epda_to_cfg(epda: PDA) -> CFG:
    assert epda.is_epda(), "The input PDA is not an empty-accepted PDA."

    Q: set[state_t] = epda.Q
    T: set[character_t] = epda.T
    T_star: set[character_t] = T | {""}
    delta: dict[tuple[state_t, character_t, stack_symbol_t], delta_image_t] = epda.delta
    q0 = epda.q0
    Z0 = epda.Z0

    cfg_S = "S"
    cfg_N: set[nonterminal_t] = set(cfg_S)
    cfg_T: set[character_t] = T
    cfg_P: set[production_t] = set()

    que: list[tuple[state_t, stack_symbol_t, state_t]] = []
    vis: set[tuple[state_t, stack_symbol_t, state_t]] = set()

    for q in Q:
        cfg_N.add(f"{q0}_{Z0}_{q}")
        cfg_P.add((("S",), (f"{q0}_{Z0}_{q}",)))
        que.append((q0, Z0, q))

    while len(que):
        q, A, p = que.pop()

        if (q, A, p) in vis:
            continue
        vis.add((q, A, p))

        for a in T_star:
            if (q, a, A) not in delta:
                continue
            for q1, B in delta[q, a, A]:
                m: int = len(B)
                left_hand: tuple[symbol_t, ...] = (f"{q}_{A}_{p}",)
                right_hand_prefix: tuple[symbol_t] = (a,)
                if m > 1:
                    states: set[state_t] = Q
                    all_combinations = itertools.product(states, repeat=m - 1)
                    for combination in all_combinations:
                        pre: state_t = q1
                        nonterminals: tuple[nonterminal_t, ...] = tuple()
                        for i in range(m - 1):
                            if (pre, B[i], combination[i]) not in vis:
                                que.append((pre, B[i], combination[i]))
                            nonterminals += (f"{pre}_{B[i]}_{combination[i]}",)
                            pre = combination[i]
                        if (pre, B[m - 1], p) not in vis:
                            que.append((pre, B[m - 1], p))
                        nonterminals += (f"{pre}_{B[m-1]}_{p}",)
                        cfg_N.update(nonterminals)
                        cfg_P.add(
                            (
                                left_hand,
                                _eliminate_none(input=right_hand_prefix + nonterminals),
                            )
                        )
                elif m == 1:
                    if (q1, B[0], p) not in vis:
                        que.append((q1, B[0], p))
                    cfg_P.add(
                        (
                            left_hand,
                            _eliminate_none(
                                input=right_hand_prefix + (f"{q1}_{B[0]}_{p}",)
                            ),
                        )
                    )
                elif m == 0 and q1 == p:
                    cfg_P.add((left_hand, _eliminate_none(input=right_hand_prefix)))

    return CFG(N=cfg_N, T=cfg_T, P=cfg_P, S=cfg_S)
