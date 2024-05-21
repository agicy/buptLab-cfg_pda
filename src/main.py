from algorithm.eliminate_epsilon_production import *
from algorithm.eliminate_unit_production import *
from algorithm.eliminate_useless_symbol import *
from algorithm.transfer_fpda_to_epda import *
from algorithm.transfer_epda_to_cfg import *
from datastructure.cfg import *
from datastructure.pda import *
from exceptions import *
import os
import re


def _read_symbol_set(input: str) -> set[str]:
    if input.count("{") != 1 or input.count("}") != 1:
        raise InputSetInvalid("Invalid Set Input")
    try:
        input = input.split(sep="{")[1].split(sep="}")[0]
    except Exception as _:
        raise InputSetInvalid("Invalid Set Input")
    inputs: list[str] = list(filter(None, input.split(",")))
    for item in inputs:
        if " " in item.strip():
            raise InputSetInvalid("Invalid Input with space in symbol name")
    return {item.strip() for item in inputs}


def _cfg_input() -> CFG:
    print("please input your CFG")
    print("N = ", end="")
    nonterminals: set[nonterminal_t] = _read_symbol_set(input=input())
    if not nonterminals:
        raise InputCFGInvalid("The non-terminal symbol set are empty")
    print("T = ", end="")
    terminals: set[terminal_t] = _read_symbol_set(input=input())
    if nonterminals & terminals:
        raise InputCFGInvalid("The terminal and non-terminal symbols are repeated")

    print(
        "P: (input one empty line to end, use -> to separate the left and right sides)"
    )

    productions: set[production_t] = set()
    while True:
        input_line: str = input()
        if input_line == "":
            break
        production: list[str] = input_line.split(sep="->")
        if len(production) != 2:
            raise InputCFGInvalid("Production is contains multiple '->'")
        left = tuple(filter(None, production[0].split(sep=" ")))
        for right_input in production[1].split(sep="|"):
            right = tuple(filter(None, right_input.split(sep=" ")))
            productions.add((left, right))

    print("S: ", end="")
    start: str = input()
    if start not in nonterminals:
        raise InputCFGInvalid("S is not in N")
    cfg = CFG(N=nonterminals, T=terminals, P=productions, S=start)
    if not cfg.is_valid():
        raise InputCFGInvalid("Input CFG is invalid")
    return cfg


def _read_immediate_state(
    Q: set[state_t], T: set[character_t], Gamma: set[stack_symbol_t], input: str
) -> tuple[state_t, character_t, stack_symbol_t]:
    if input.count("(") != 1 or input.count(")") != 1:
        raise InputSetInvalid("Invalid State Input")
    try:
        input = input.split(sep="(")[1].split(sep=")")[0]
    except Exception as _:
        raise InputSetInvalid("Invalid State Input")

    if input.count(",") != 2:
        raise InputSetInvalid("Invalid transition definition")
    inputs = input.split(",")
    immediate_state: tuple[state_t, character_t, stack_symbol_t] = (
        inputs[0].strip(),
        inputs[1].strip(),
        inputs[2].strip(),
    )
    if immediate_state[0] not in Q:
        raise InputSetInvalid("Invalid transition definition")
    if immediate_state[1] and immediate_state[1] not in T:
        raise InputSetInvalid("Invalid transition definition")
    if immediate_state[2] and immediate_state[2] not in Gamma:
        raise InputSetInvalid("Invalid transition definition")
    return immediate_state


def _read_transition_set(
    Q: set[state_t], Gamma: set[stack_symbol_t], input: str
) -> set[tuple[state_t, tuple[stack_symbol_t, ...]]]:
    if input.count("{") != 1 or input.count("}") != 1:
        raise InputSetInvalid("Invalid Set Input")
    try:
        input = input.split(sep="{")[1].split(sep="}")[0]
    except Exception as _:
        raise InputSetInvalid("Invalid Set Input")

    brackets = str()
    for character in input:
        if character == "(" or character == ")":
            brackets: str = brackets + character
    if (
        len(brackets) % 2 == 1
        or "((" in brackets
        or "))" in brackets
        or (brackets and brackets[0] == ")")
        or (brackets and brackets[-1] == "(")
    ):
        raise InputSetInvalid("Invalid brackets")

    pattern = r"\(([^)]+)\)"

    matches: list[str] = re.findall(pattern=pattern, string=input)

    result: set[tuple[state_t, tuple[stack_symbol_t, ...]]] = set()
    for transition in matches:
        content: list[str] = transition.split(sep=",")
        if len(content) != 2:
            raise InputSetInvalid("Invalid transition definition")
        state: state_t = content[0]
        stack_symbols = tuple(filter(None, content[1].split(sep=" ")))
        result.add((state, stack_symbols))
    return result


def _pda_input() -> PDA:
    print("please input your PDA")
    print("Q = ", end="")
    Q: set[state_t] = _read_symbol_set(input=input())
    if not Q:
        raise InputPDAInvalid("The state set are empty")
    print("T = ", end="")
    T: set[character_t] = _read_symbol_set(input=input())

    print("Gamma = ", end="")
    Gamma: set[stack_symbol_t] = _read_symbol_set(input=input())

    print("delta: (input one empty line to end, use (?,?,?) -> {(?,?),...} format)")

    delta: dict[
        tuple[state_t, character_t, stack_symbol_t],
        set[tuple[state_t, tuple[stack_symbol_t, ...]]],
    ] = {}
    while True:
        input_line: str = input()
        if input_line == "":
            break
        transitions: list[str] = input_line.split(sep="->")
        if len(transitions) != 2:
            raise InputPDAInvalid("Transition is contains multiple '->'")
        immediate_state: tuple[state_t, character_t, stack_symbol_t] = (
            _read_immediate_state(Q=Q, T=T, Gamma=Gamma, input=transitions[0])
        )
        next_states: set[tuple[state_t, tuple[stack_symbol_t, ...]]] = (
            _read_transition_set(Q=Q, Gamma=Gamma, input=transitions[1])
        )
        if immediate_state in delta.keys():
            raise InputPDAInvalid("repeated transition definition")
        delta[immediate_state] = next_states

    print("q0 = ", end="")
    q0: state_t = input()
    if q0 not in Q:
        raise InputPDAInvalid("q0 is not in Q")
    print("Z0 = ", end="")
    Z0: stack_symbol_t = input()
    if Z0 not in Gamma:
        raise InputPDAInvalid("Z0 is not in Gamma")

    print("F = ", end="")
    F: set[state_t] = _read_symbol_set(input=input())
    if not F.issubset(Q):
        raise InputPDAInvalid("F is not a subset of Q")

    pda = PDA(Q=Q, T=T, Gamma=Gamma, delta=delta, q0=q0, Z0=Z0, F=F)
    if not pda.is_valid():
        raise InputPDAInvalid("Input PDA is invalid")

    return pda


def _simplify_cfg(cfg: CFG) -> CFG:
    return eliminate_useless_symbol(
        cfg=eliminate_unit_production(cfg=eliminate_epsilon_production(cfg=cfg))
    )


def _solve() -> None:
    print("please input an number to choose the functionality you want to use.")
    print("1. input a CFG to simplify")
    print("2. input a PDA to convert to CFG")
    print("(input any other thing to exit)")
    input_content: str = input()
    if input_content == "1":
        while True:
            try:
                cfg: CFG = _cfg_input()
                break
            except Exception as e:
                print(e)
                print("Please check you input format and retry!")
        try:
            cfg = _simplify_cfg(cfg=cfg)
        except Exception as e:
            print(e)
        print("#=======================")
        print("Here is the result.")
        print(cfg.to_string())
    if input_content == "2":
        while True:
            try:
                pda: PDA = _pda_input()
                break
            except Exception as e:
                print(e)
                print("Please check you input format and retry!")
        if not pda.is_epda():
            pda = transfer_fpda_to_epda(fpda=pda)
        cfg = transfer_epda_to_cfg(epda=pda)
        try:
            cfg = _simplify_cfg(cfg=cfg)
            print("#=======================")
            print("Here is the result.")
            print(cfg.to_string())
        except Exception as e:
            print(e)
    return


if __name__ == "__main__":
    _solve()
    os.system("pause")
