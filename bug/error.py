class CompilingException(Exception):
    pass

ILLEGAL_CHAR = "'{}' is an illegal character"
MISMATCHED_TYPES = "mistmatched types '{}' and '{}'"
PARSING_ERROR = "invalid syntax"
UNDEFINED_IDENT = "undefined identifier '{}'"
DEFINED_IDENT = "'{}' was already defined."

def error(msg: str, line_no: int, col_no: int) -> None:
    raise CompilingException(f"error at line {line_no}, column {col_no}: {msg}")