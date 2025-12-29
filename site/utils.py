def add_indentation_to_every_line(s: str, indentation_length: int) -> str:
    """
        Util to keep indentation in the generated code
    """
    return '\n'.join([' '*indentation_length + line for line in s.split('\n')])
