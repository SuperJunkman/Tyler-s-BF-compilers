#BrainF*ck class-based interpereter w/ methods for each command
#By Tyler Marion
#Runs the benchmark test below (268,435,497 commands) in 614 seconds (10 minutes)
#++++++++[->-[->-[->-[-]<]<]<]


from sys import exit
from time import time

class bf_interpreter:
    MEM_SIZE = 1000
    mem = [0 for i in range(MEM_SIZE)]
    mem_ptr: int = 0
    ins_ptr: int = 0
    inp_ptr: int = 0
    out: str = ""

    #finds and catalogues the beginning and end of every scope
    def scope_scan(self):
        self.scopes: dict = {}
        unbounded: list[int] = []

        #TODO add error handler for unclosed scope and unexpected closure
        for i, j in enumerate(self.ins):
            if j == '[': unbounded += [i]
            if j == ']': 
                #assigns 2 KV pairs where a : b and b : a
                #a is value of j, and b is the popped value from unbound
                self.scopes[i] = unbounded.pop()
                self.scopes[self.scopes[i]] = i

    def __init__(self, instructions: str, input: str = ''):
        self.ins = ''.join(filter((lambda x : x in '+-><[],.'),instructions))
        self.inp = input
        self.scope_scan()

    #command '+'
    def increment(self):
        self.mem[self.mem_ptr] = (self.mem[self.mem_ptr] + 1) % 256

    #command '-'
    def decrement(self):
        self.mem[self.mem_ptr] = (self.mem[self.mem_ptr] - 1) % 256

    #command '>'
    def shift_right(self):
        self.mem_ptr = (self.mem_ptr + 1) % self.MEM_SIZE

    #command '<'
    def shift_left(self):
        self.mem_ptr = (self.mem_ptr - 1) % self.MEM_SIZE

    #command '['
    def open_scope(self):
        if not bool(self.mem[self.mem_ptr]): self.ins_ptr = self.scopes[self.ins_ptr]

    #command ']'
    def close_scope(self):
        if bool(self.mem[self.mem_ptr]): self.ins_ptr = self.scopes[self.ins_ptr]

    #command ','
    def read(self):
        self.mem[self.mem_ptr] = 0 if self.inp_ptr >= len(self.inp) else ord(self.inp[self.inp_ptr])
        self.inp_ptr += 1

    #command '.'
    def write(self):
        self.out += chr(self.mem[self.mem_ptr])

    def run(self):
        command_num: int = 0
        start = time()


        while(self.ins_ptr < len(self.ins)):

            
            #list of commands
            {
                '+':self.increment,
                '-':self.decrement,
                '>':self.shift_right,
                '<':self.shift_left,
                '[':self.open_scope,
                ']':self.close_scope,
                ',':self.read,
                '.':self.write
            }[self.ins[self.ins_ptr]]()

            command_num += 1
            self.ins_ptr += 1
        
        print(self.out)
        print(f'Commands executed: {command_num}')
        end = time()
        print(f'finished in {end - start} seconds')


bf_exec = bf_interpreter('''++++++++[->-[->-[->-[-]<]<]<]''')
bf_exec.run()
