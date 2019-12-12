"""
Copyright 2017 Steven Diamond

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from cvxpy.atoms.affine.affine_atom import AffAtom
import cvxpy.lin_ops.lin_utils as lu
import operator as op


class UnaryOperator(AffAtom):
    """
    Base class for expressions involving unary operators.
    """

    def __init__(self, expr):
        super(UnaryOperator, self).__init__(expr)

    def name(self):
        return self.OP_NAME + self.args[0].name()

    # Applies the unary operator to the value.
    def numeric(self, values):
        return self.OP_FUNC(values[0])


class NegExpression(UnaryOperator):
    OP_NAME = "-"
    OP_FUNC = op.neg

    def size_from_args(self):
        """Returns the (row, col) size of the expression.
        """
        return self.args[0].size

    def sign_from_args(self):
        """Returns sign (is positive, is negative) of the expression.
        """
        return (self.args[0].is_negative(), self.args[0].is_positive())

    def is_incr(self, idx):
        """Is the composition non-decreasing in argument idx?
        """
        return False

    def is_decr(self, idx):
        """Is the composition non-increasing in argument idx?
        """
        return True

    @staticmethod
    def graph_implementation(arg_objs, size, data=None):
        """Negate the affine objective.

        Parameters
        ----------
        arg_objs : list
            LinExpr for each argument.
        size : tuple
            The size of the resulting expression.
        data :
            Additional data required by the atom.

        Returns
        -------
        tuple
            (LinOp for objective, list of constraints)
        """
        return (lu.neg_expr(arg_objs[0]), [])