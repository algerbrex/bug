from typing import Union
from .lexer import Lexer, Token, TokenType
from .ast import Program, Assignment, Identifier, Integer, Stmt, Expression, Types
from .error import error, PARSING_ERROR, UNDEFINED_IDENT, DEFINED_IDENT

class Scope:
    def __init__(self, parent: 'Scope'):
        self._parent = parent
        self._variables: dict[str, Identifier] = {}

    def lookup(self, name: str) -> Union[Identifier, None]:
        curr_scope = self

        while curr_scope is not None:
            ident = curr_scope._variables.get(name)

            if ident is not None:
                return ident

            curr_scope = self._parent

        return None

    def define(self, name: str, ident: Identifier) -> None:
        self._variables[name] = ident


class Parser:
    def __init__(self, buffer: str) -> None:
        self._lexer = Lexer(buffer)
        self._curr_token: Token = None
        self._curr_scope = Scope(None)

    def parse(self) -> Program:
        return self._parse_program()

    def _parse_program(self) -> Program:
        stmts: list['Stmt'] = []

        self._consume()
        while self._curr_token.tok_type != TokenType.END:
            if self._curr_token.tok_type == TokenType.NEWLINE:
                self._consume()
                continue

            stmt = self._parse_stmt()
            stmts.append(stmt)

        return Program(stmts)

    def _parse_stmt(self) -> Stmt:
        return self._parse_assignment()

    def _parse_assignment(self) -> Assignment:
        type_tok = self._check_then_consume(TokenType.TYPE)
        ident_tok = self._check_then_consume(TokenType.IDENTIFIER)

        ident = self._curr_scope.lookup(ident_tok.value)
        if ident is not None:
            self._error(
                DEFINED_IDENT.format(ident_tok.value),
                ident_tok,
            )


        self._check_then_consume('=')
        expr = self._parse_expression()

        ident = Identifier(ident_tok, Types[type_tok.value.upper()])
        self._curr_scope.define(ident_tok.value, ident)
        
        assignment = Assignment(type_tok, ident, expr)
        self._check_then_consume('\n')
        return assignment

    def _parse_expression(self) -> Expression:
        expr: Expression = None
        if self._curr_token.tok_type == TokenType.INTEGER:
            expr = Integer(self._curr_token)
        elif self._curr_token.tok_type == TokenType.IDENTIFIER:
            expr = self._curr_scope.lookup(self._curr_token.value)
            if expr is None:
                self._error(
                    UNDEFINED_IDENT.format(self._curr_token.value)
                )
        else:
            self._error(PARSING_ERROR)

        self._consume()
        return expr
            

    def _check_then_consume(self, should_be: Union[TokenType, 'str']) -> Token:
        if self._curr_token.tok_type != should_be and self._curr_token.value != should_be:
            self._error(PARSING_ERROR)

        curr_token = self._curr_token
        self._consume()
        return curr_token

    def _consume(self) -> None:
        self._curr_token = self._lexer.next_token()

    def _error(self, msg: str, tok: Union[Token, None]=None):
        tok = self._curr_token if tok is None else tok
        error(msg, tok.line, tok.column)
