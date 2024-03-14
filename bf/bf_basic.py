#My first attempt at a BF interpereter. Executes each command using a match statement
#By Tyler Marion
#Timeout logic has been temporarily removed, will likely be re-implemented in the future
#Currently no handler for broken scopes
#Runs the benchmark test below (268,435,497 commands) in 202 seconds (>3 minutes)
#++++++++[->-[->-[->-[-]<]<]<]

from time import time
def bf(ins: str, inp: str = "") -> str:
    BUF_SIZE = 1000
    mem: list[int] = [0 for i in range(BUF_SIZE)]
    ptr, ins_ptr, inp_ptr = 0,0,0
    out: str = ""
    loop_stack: list[int] = []
    starttime = time()
    commands = 0
    while(ins_ptr < len(ins)):
        match(ins[ins_ptr]):
            case '<': ptr -= (1 if ptr > 0 else -BUF_SIZE)
            case '>': ptr += (1 if ptr < BUF_SIZE else -BUF_SIZE)
            case '+': mem[ptr] += (1 if ptr < 256 else -256)
            case '-': mem[ptr] -= (1 if mem[ptr] > 0 else -256)
            case '[':
                if bool(mem[ptr]): loop_stack += [ins_ptr]
                else:
                    scope = 1
                    while(scope > 0):
                        ins_ptr += 1
                        if ins[ins_ptr] == '[': scope += 1
                        elif ins[ins_ptr] == ']': scope -= 1
            case ']': 
                if mem[ptr] == 0: loop_stack.pop()
                else: ins_ptr = loop_stack[-1]
            case ',': 
                mem[ptr] = 0 if inp_ptr >= len(inp) else ord(inp[inp_ptr])
                inp_ptr += 1
            case '.': out += chr(mem[ptr])
        ins_ptr += 1
        commands += 1
    return out

ins = '''++++++++[->-[->-[->-[-]<]<]<]'''
start = time()
print(bf(ins))
print(f'Finished in {time() - start} seconds')
