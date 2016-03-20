# Andrew Black
# March 19, 2016
# Context Free Grammar parser for Valve's VDF file format

import sys
import re

#
# Lexer
#
tokens = [
	'VALUE', 'SEPARATOR', 'LBRACKET', 'RBRACKET', 'QUOTE'
    ]

t_VALUE = r'[\w.,?`~!@#$%^&*()-+=<>/\\]+'
t_SEPARATOR = r'\s+'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'

def t_QUOTE(t):
	r'(?<!\\)"'
	pattern = r'(?<!)"'
	m = re.search(r'(?<!\\)"', t.lexer.lexdata[t.lexer.lexpos:])
	if m:
		text = t.lexer.lexdata[t.lexer.lexpos:(t.lexer.lexpos)+m.start()]
		t.lexer.lexpos = t.lexer.lexpos+m.start()+1
		t.value = text
		t.type = 'VALUE'
		return t
	raise Exception("Unbalanced quotes!")

t_ignore = '\f\v'

def t_error(t):
	print("Illegal character: ",t.value[0])
	t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

#
# Parser
#
def p_vdf(t):
	'''vdf : vdf SEPARATOR kvp
			| kvp'''
	if len(t) == 4:
		t[0] = t[1] + t[3]
	else:
		t[0] = t[1]

def p_kvp(t):
	'''kvp : VALUE SEPARATOR VALUE
			| VALUE SEPARATOR LBRACKET SEPARATOR vdf SEPARATOR RBRACKET'''
	if len(t) == 4:
		t[0] = [ (t[1], t[3]) ]
	else:
		t[0] = [ (t[1], t[5]) ]

# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()

# Parse data from stdin (will be replaced with an API)
result = parser.parse(sys.stdin.read().strip())
print(result)

print("PRETTY")
for v in result:
	print(v)
