#BF-to-Python compiler and executer
#By Tyler Marion
    
#-Uses exec() function to run the code from a string
#-Probably violates python zen in half a dozen different ways
#-My fastest interpereter
#-Currently only runs with 8-bit memory addresses
#-memory pointer is only programmed to wrap when going out of range
    
#-currently completes the below benchmark test (268,436,271 commands) in 24 seconds 
#-code: ++++++++[->-[->-[->-[-]<]<]<]>++++++++[<++++++++++>-]<[>+>+<<-]>-.>-----.
#-(code from https://github.com/rdebath/Brainfuck/blob/master/testing/Bench.b)

from time import time
from sys import exit

scope = 0
instructions = ''''''
ins = ''.join(filter((lambda x:x in '+-><[],.'), instructions))
inp = list('brainf*ck')
out: str = ''

code = '''MEM_SIZE = 1000
mem = [0 for i in range(MEM_SIZE)]
ptr = 0
'''

#lambda functions

#adds new line and however many indents are currently neccessary
new_line = lambda : '\n' + ('\t' * scope)

#reads next instruction, returns null i is the last index in ins
look_ahead = lambda i : ins[i + 1] if (i + 1) < len(ins) else '\0'

val_change = 0
ptr_change = 0

#compiler
for i, j in enumerate(ins):

    match(j):
        case '+': val_change += 1
        case '-': val_change -= 1
        case '>': ptr_change += 1
        case '<': ptr_change -= 1
        case '[':
            scope += 1
            code += f'while mem[ptr]:{new_line()}'
        case ']': 
            scope -= 1
            code += new_line()
        case ',': 
            code += f'mem[ptr] = ord(inp.pop(0)) if inp else 0{new_line()}'    
        case '.': code += f'out += chr(mem[ptr]){new_line()}'
    
    if look_ahead(i) not in '+-' and val_change:
        code += f'mem[ptr] = (mem[ptr] + {val_change}) % 256{new_line()}'
        val_change = 0

    if look_ahead(i) not in '><' and ptr_change:
        code += f'ptr = (ptr + {ptr_change}) % MEM_SIZE{new_line()}'
        ptr_change = 0

    if scope < 0 : 
        print(f'Error - unexpected \']\' at instruction index {i}')
        exit()

if scope > 0:
    print(f'Error - expected {scope} additional \']\'s')
    exit()

print(code)
start = time()
exec(code)

print(out)
print(f'Finished in {time() - start} seconds')
