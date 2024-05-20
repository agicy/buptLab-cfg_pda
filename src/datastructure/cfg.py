from exceptions import *

__all__: list[str] = ["CFG", "symbol_t", "nonterminal_t", "terminal_t", "production_t"]

nonterminal_t = str
terminal_t = str
symbol_t = nonterminal_t | terminal_t
production_t = tuple[tuple[symbol_t, ...], tuple[symbol_t, ...]]


class CFG:
    def __init__(
        self,
        N: set[nonterminal_t],
        T: set[terminal_t],
        P: set[production_t],
        S: nonterminal_t,
    ) -> None:
        self.N: set[nonterminal_t] = N
        self.T: set[terminal_t] = T
        self.P: set[production_t] = P
        self.S: nonterminal_t = S

    def is_valid(self) -> bool:
        if self.N & self.T:
            return False
        if self.S not in self.N:
            return False
        for left_hand, right_hand in self.P:
            if len(left_hand) != 1:
                return False
            for left_element in left_hand:
                if left_element not in self.N:
                    return False
            for right_element in right_hand:
                if right_element not in self.N | self.T | {""}:
                    return False
        return True

    def to_string(self) -> str:
        if not self.is_valid():
            raise CFGInvalid("Invalid CFG.")
        nonterminals: str = "{ " + ", ".join(sorted(self.N)) + " }"
        terminals: str = "{ " + ", ".join(sorted(self.T)) + " }"
        productions: set[str] = {
            nonterminal
            + " -> "
            + " | ".join(
                sorted(
                    {
                        (
                            " ".join([symbol for symbol in right_hand])
                            if right_hand
                            else "ε"
                        )
                        for left_hand, right_hand in self.P
                        if left_hand == (nonterminal,)
                    }
                )
            )
            for nonterminal in self.N
        }
        start: str = self.S
        return "\n".join(
            [
                "N = " + nonterminals,
                "T = " + terminals,
                "P:\n" + "\n".join(sorted(productions)),
                "S = " + start,
            ]
        )
