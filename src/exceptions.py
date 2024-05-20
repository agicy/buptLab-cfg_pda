__all__: list[str] = [
    "CFGEmptyError",
    "CFGInvalid",
    "InputCFGInvalid",
    "InputPDAInvalid",
    "InputSetInvalid",
]


class CFGEmptyError(Exception):
    pass


class CFGInvalid(Exception):
    pass


class InputCFGInvalid(Exception):
    pass


class InputPDAInvalid(Exception):
    pass


class InputSetInvalid(Exception):
    pass
