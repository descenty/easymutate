import ast
from typing import Iterable
from easymutate.mutators.mutator import Mutator
from ast import AST, BinOp, NodeTransformer


class MathMutator(Mutator):
    class BinOpTransformer(NodeTransformer):
        def __init__(self, operation) -> None:
            self.operation = operation
            super().__init__()

        def visit_BinOp(self, node: BinOp) -> BinOp | None:
            node.op = self.operation
            return node

    operations = [ast.Add(), ast.Sub(), ast.Mult(), ast.Div()]

    @classmethod
    def generate(cls, tree: AST) -> Iterable[AST]:
        for operation in cls.operations:
            yield cls.BinOpTransformer(operation).visit(tree)
