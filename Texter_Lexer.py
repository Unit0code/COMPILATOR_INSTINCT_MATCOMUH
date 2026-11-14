### Sacar esto del proyecto

from Lexer import Lexer
from Errors import LexicalError

with open("uruk.ins", encoding="utf-8") as f:
    code = f.read()

try:
    tokens = Lexer(code).to_tokenize()
    for t in tokens:
        print(t)
    print(f"\nTotal: {len(tokens)} tokens")
except LexicalError as e:
    print(f"Error: {e}")