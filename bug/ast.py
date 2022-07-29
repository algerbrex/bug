from enum import Enum
from collections import namedtuple
from typing import Union
from .lexer import Token
from .error import error, MISMATCHED_TYPES

PROGRAM_TEMPLATE = """
int main() {{ 
{} 
}}
"""


Type = namedtuple('Type', 'base_type c_name')


class Types(Enum):
    U8          = Type('untyped_int', 'unsigned char')
    U16         = Type('untyped_int', 'unsigned short')
    U32         = Type('untyped_int', 'unsigned long')
    U64         = Type('untyped_int', 'unsigned long long')
    I8          = Type('untyped_int', 'signed char')
    I16         = Type('untyped_int', 'signed short')
    I32         = Type('untyped_int', 'signed long')
    I64         = Type('untyped_int', 'signed long long')
    UNTYPED_INT = Type('', '')


def _types_match(first_type: Types, second_type: Types) -> bool:
    untyped_type = None
    concrete_type = None

    if first_type in (Types.UNTYPED_INT,):
        untyped_type = first_type
    elif second_type in (Types.UNTYPED_INT,):
        untyped_type = second_type

    if first_type not in (Types.UNTYPED_INT,):
        concrete_type = first_type
    elif second_type not in (Types.UNTYPED_INT,):
        concrete_type = second_type

    if untyped_type is None:
        return first_type == second_type
    elif untyped_type == Types.UNTYPED_INT and concrete_type.value.base_type == 'untyped_int':
        return True
    
    return False

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
        if not _types_match(expr_type, self._assignment_type):
            error(
                MISMATCHED_TYPES.format(expr_type.name.lower(), self._assignment_type.name.lower()),
                self._type_tok.line,
                self._type_tok.column
            )
        
    def gen_code(self) -> str:
        self.resolve_type()
        return '{} {} = {};'.format(
            # Make sure to use the type of the assignment here, since the type
            # of the expression may be an unconcrete type, like untyped int.
            self._assignment_type.value.c_name, 
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

    def resolve_type(self):
        return Types.UNTYPED_INT
        
    def gen_code(self) -> str:
        return self._int_tok.value
