from enum import Enum
from typing import Union
from .lexer import Token
from .error import error, MISMATCHED_TYPES

PROGRAM_TEMPLATE = """
int main() {{ 
{} 
}}
"""

class Types(Enum):
    INT = 1
    ERR = 2

Expression = Union['Identifier', 'Integer']
Stmt = 'Assignment'

class Program:
    def __init__(self, stmts: "list['Stmt']") -> None:
        self._stmts = stmts

    def gen_code(self) -> str:
        program = ''
        for stmt in self._stmts:
            program += f'    {stmt.gen_code()}\n'
        return PROGRAM_TEMPLATE.format(program.rstrip('\n')).lstrip('\n')

class Assignment:
    def __init__(self, type_tok: Token, ident: 'Identifier', expression: 'Expression') -> None:
        self._type_tok = type_tok
        self._ident = ident
        self._assignment_type = Types[type_tok.value.upper()]
        self._expression = expression

    def resolve_type(self):
        expr_type = self._expression.resolve_type()
        if self._assignment_type != expr_type:
            error(
                MISMATCHED_TYPES.format(expr_type.name.lower(), self._assignment_type.name.lower()),
                self._type_tok.line,
                self._type_tok.column
            )
        
    def gen_code(self) -> str:
        self.resolve_type()
        return '{} {} = {};'.format(
            self._type_tok.value, 
            self._ident.gen_code(),
            self._expression.gen_code()
        )

class Identifier:
    def __init__(self, ident_tok: Token, ident_type: Types) -> None:
        self._ident_tok = ident_tok
        self._ident_type = ident_type

    def resolve_type(self):
        return self._ident_type
        
    def gen_code(self) -> str:
        return self._ident_tok.value

class Integer:
    def __init__(self, int_tok: Token) -> None:
        self._int_tok = int_tok
        self._expr_type = Types.INT

    def resolve_type(self):
        return self._expr_type
        
    def gen_code(self) -> str:
        return self._int_tok.value
