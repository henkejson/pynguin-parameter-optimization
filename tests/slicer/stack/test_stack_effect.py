#  This file is part of Pynguin.
#
#  SPDX-FileCopyrightText: 2019–2022 Pynguin Contributors
#
#  SPDX-License-Identifier: LGPL-3.0-or-later
#

import dis
from typing import List, Tuple

import pytest

import pynguin.slicer.stack.stack_effect as se
import pynguin.utils.opcodes as opcodes


@pytest.mark.parametrize(
    "op",
    [pytest.param(op) for op in range(90)],  # opcodes up to 90 take no argument
)
def test_argument_less_opcodes(op):
    """Test argument less opcode stack effects."""
    if op in opcodes.__dict__.values():
        pops, pushes = se.StackEffect.stack_effect(op, None)
        expected = dis.stack_effect(op)

        assert expected == (pushes - pops)


def _conditional_combinations() -> List[Tuple[int, int, bool]]:
    """Create a list of all combinations to call a conditional opcode's stack effect."""
    args = [0, 1]
    conditional_opcodes = range(90, 166)

    # (opcode, argument, jump)
    combinations: List[Tuple[int, int, bool]] = []
    for op in conditional_opcodes:
        for arg in args:
            combinations.append((op, arg, True))
            combinations.append((op, arg, False))
    return combinations


@pytest.mark.parametrize(
    "op, arg, jump",
    [pytest.param(op, arg, jump) for (op, arg, jump) in _conditional_combinations()],
)
def test_conditional_opcodes(op, arg, jump):
    """Test opcodes with arguments and jumps."""
    if op in opcodes.__dict__.values():
        pops, pushes = se.StackEffect.stack_effect(op, arg, jump=jump)
        expected = dis.stack_effect(op, arg, jump=jump)

        assert expected == (pushes - pops)


