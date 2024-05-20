__all__: list[str] = [
    "PDA",
    "state_t",
    "character_t",
    "stack_symbol_t",
    "delta_image_t",
]

state_t = str
character_t = str
stack_symbol_t = str
delta_image_t = set[tuple[state_t, tuple[stack_symbol_t, ...]]]


class PDA:
    def __init__(
        self,
        Q: set[state_t],
        T: set[character_t],
        Gamma: set[stack_symbol_t],
        delta: dict[tuple[state_t, character_t, stack_symbol_t], delta_image_t],
        q0: state_t,
        Z0: stack_symbol_t,
        F: set[state_t],
    ) -> None:
        self.Q: set[state_t] = Q
        self.T: set[character_t] = T
        self.Gamma: set[stack_symbol_t] = Gamma
        self.delta: dict[
            tuple[state_t, character_t, stack_symbol_t],
            set[tuple[state_t, tuple[stack_symbol_t, ...]]],
        ] = delta
        self.q0: state_t = q0
        self.Z0: stack_symbol_t = Z0
        self.F: set[state_t] = F

    def is_valid(self) -> bool:
        if self.q0 not in self.Q:
            return False
        if self.Z0 not in self.Gamma:
            return False
        if not self.F.issubset(self.Q):
            return False
        for (state, symbol, stack_symbol), transitions in self.delta.items():
            if state not in self.Q:
                return False
            if symbol and symbol not in self.T:
                return False
            if stack_symbol and stack_symbol not in self.Gamma:
                return False
            for next_state, stack_string in transitions:
                if next_state not in self.Q:
                    return False
                for symbol in stack_string:
                    if symbol and symbol not in self.Gamma:
                        return False
        return True

    def is_epda(self) -> bool:
        return not self.F
