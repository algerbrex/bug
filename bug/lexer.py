from collections import namedtuple
from enum import Enum
from .error import error, ILLEGAL_CHAR

Token = namedtuple('Token', 'value tok_type line column')

class TokenType(Enum):
    IDENTIFIER = 1
    TYPE       = 2
    INTEGER    = 3
    EQUAL      = 4
    NEWLINE    = 5
    END        = 6

class Lexer:

    WHITESPACE = (' ', '\t')
    TYPES = ('int',)
    OPERATORS = {
        '=': TokenType.EQUAL
    }

    def __init__(self, buffer: str) -> None:
        self._buffer = buffer
        self._buffer_len = len(buffer)

        if not self._buffer.endswith('\n'):
            self._buffer += '\n'
            self._buffer_len = len(self._buffer)

        self._pos: int = 0
        self._line_no: int = 1
        self._col_no: int = 1

    def next_token(self) -> Token:
        if self._pos == self._buffer_len:
            return Token('', TokenType.END, self._line_no, self._col_no)

        curr_char = self._buffer[self._pos]

        while curr_char in self.WHITESPACE:
            self._pos += 1
            self._col_no += 1

            if self._pos == self._buffer_len:
                return Token('', TokenType.END, self._line_no, self._col_no)

            curr_char = self._buffer[self._pos]

        if curr_char.isalpha():
            token = self._lex_identifier()
        elif curr_char.isdigit():
            token = self._lex_digit()
        elif curr_char in self.OPERATORS:
            token = self._lex_operator()
        elif curr_char == '\n':
            token = self._lex_newline()
        else:
            error(ILLEGAL_CHAR.format(curr_char), self._line_no, self._col_no)
        
        return token

    def _lex_identifier(self) -> Token:
        value = self._buffer[self._pos]
        while value.isalnum():
            self._pos += 1

            if self._pos >= self._buffer_len:
                break

            self._col_no +=1
            value += self._buffer[self._pos]

        value = value[:-1]
        tok_type = TokenType.IDENTIFIER

        if value in self.TYPES:
            tok_type = TokenType.TYPE

        return Token(value, tok_type, self._line_no, self._col_no - len(value))

    def _lex_digit(self) -> Token:
        value = self._buffer[self._pos]
        while value.isdigit():
            self._pos += 1

            if self._pos >= self._buffer_len:
                break

            self._col_no +=1
            value += self._buffer[self._pos]

        value = value[:-1]
        return Token(value, TokenType.INTEGER, self._line_no, self._col_no - len(value))

    def _lex_operator(self) -> Token:
        value = self._buffer[self._pos]
        self._pos += 1
        self._col_no +=1
        return Token(value, self.OPERATORS[value], self._line_no, self._col_no - 1)

    def _lex_newline(self) -> Token:
        self._pos += 1
        self._line_no += 1

        curr_col_no = self._col_no
        self._col_no = 1
        return Token('\n', TokenType.NEWLINE, self._line_no - 1, curr_col_no)
