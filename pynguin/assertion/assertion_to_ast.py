#  This file is part of Pynguin.
#
#  SPDX-FileCopyrightText: 2019–2020 Pynguin Contributors
#
#  SPDX-License-Identifier: LGPL-3.0-or-later
#
"""Provides an assertion visitor to transform assertions to AST."""
import ast
from typing import Any, List

import pynguin.assertion.assertionvisitor as av
import pynguin.assertion.noneassertion as na
import pynguin.assertion.primitiveassertion as pa
import pynguin.testcase.variable.variablereference as vr
import pynguin.utils.ast_util as au
from pynguin.utils.namingscope import NamingScope


class AssertionToAstVisitor(av.AssertionVisitor):
    """An assertion visitor that transforms assertions into AST nodes."""

    def __init__(self, variable_names: NamingScope):
        """Create a new assertion visitor.

        Args:
            variable_names: the naming scope that is used to resolve the names
                            of the variables used in the assertions.
        """
        self._variable_names = variable_names
        self._nodes: List[ast.stmt] = []

    @property
    def nodes(self) -> List[ast.stmt]:
        """Provides the ast nodes generated by this visitor.

        Returns:
            the ast nodes generated by this visitor.
        """
        return self._nodes

    def visit_primitive_assertion(self, assertion: pa.PrimitiveAssertion) -> None:
        """
        Creates an assertion of form "assert var0 == value" or assert var0 is False,
        if the value is a bool.

        Args:
            assertion: the assertion that is visited.

        """
        if isinstance(assertion.value, bool):
            self._nodes.append(
                self._create_assert(assertion.source, ast.Is(), assertion.value)
            )
        else:
            self._nodes.append(
                self._create_assert(assertion.source, ast.Eq(), assertion.value)
            )

    def visit_none_assertion(self, assertion: na.NoneAssertion) -> None:
        """
        Creates an assertion of form "assert var0 is None" or "assert var0 is not None".

        Args:
            assertion: the assertion that is visited.
        """
        if assertion.value:
            self._nodes.append(self._create_assert(assertion.source, ast.Is(), None))
        else:
            self._nodes.append(self._create_assert(assertion.source, ast.IsNot(), None))

    def _create_assert(
        self, var: vr.VariableReference, operator: ast.cmpop, value: Any
    ) -> ast.Assert:
        return ast.Assert(
            test=ast.Compare(
                left=au.create_var_name(self._variable_names, var, load=True),
                ops=[operator],
                comparators=[ast.Constant(value=value, kind=None)],
            ),
            msg=None,
        )
