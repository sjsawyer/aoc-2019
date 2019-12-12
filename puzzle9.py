def load_program():
    with open("data/9.txt", "rb") as f:
        return [int(x) for x in f.read().split(',')]


class Memory():
    def __init__(self, memory):
        self.memory = list(memory)

    def __len__(self):
        return len(self.memory)

    def __getitem__(self, idx):
        if idx < 0:
            raise ValueError("Cannot access negative memory! {}".format(idx))
        if idx >= len(self):
            print "Warning: Accessing OOB memory"
            return 0
        return self.memory[idx]

    def __setitem__(self, idx, num):
        if idx < 0:
            raise ValueError("Cannot set negative memory! {}".format(idx))
        if idx >= len(self):
            print "Warning: Setting OOB memory. Extending..."
            self.memory.extend([0 for _ in range(idx-len(self)+1)])
        self.memory[idx] = num


def test_memory():
    mem = Memory([0, 1, 2, 3, 4])
    assert mem[2] == 2
    assert mem[100] == 0
    mem[10] = 10
    assert mem[10] == 10


class IntcodeComputer:
    def __init__(self, program, input=None):
        self.program = Memory(program)
        self.ptr = 0
        self.rel_base = 0
        self.input = input or iter(())
        self.output = []

    def eval_position(self, original_position, param):
        '''
        Return the POSITION of what we want to read from/write to, after
        evaluating the parameter mode

        eval_position(i+2, 0) -> program[i+2]
        eval_position(i+2, 1) -> i+2
        eval_position(i+2, 2) -> program[i+2]+rel_base
        '''
        if param == 0:
            # position mode
            return self.program[original_position]
        elif param == 1:
            # immediate mode
            return original_position
        elif param == 2:
            return self.program[original_position] + self.rel_base
        else:
            raise ValueError("Invalid parameter %d" % param)

    def eval(self, num, param):
        if param == 0:
            # position mode
            return self.program[num]
        elif param == 1:
            # immediate mode
            return num
        elif param == 2:
            # relative mode
            return self.program[num + self.rel_base]
        else:
            raise ValueError("invalid param {}".format(param))

    def parse_op(self):
        op = self.program[self.ptr] % 100
        params = ((self.program[self.ptr]/100) % 10,
                  (self.program[self.ptr]/1000) % 10,
                  (self.program[self.ptr]/10000) % 10)
        # sanity check
        assert op in {1, 2, 3, 4, 5, 6, 7, 8, 9, 99}
        assert all(p in {0, 1, 2} for p in params)
        return op, params

    def execute_next_instruction(self):
        op, params = self.parse_op()
        # for convenience:
        program, ptr = self.program, self.ptr

        if op == 1:
            # we add
            res = sum(self.eval(program[ptr+j+1], params[j])
                      for j in range(2))
            #position = program[ptr+3]
            position = self.eval_position(ptr+3, params[2])
            program[position] = res
            self.ptr += 4
        elif op == 2:
            # we multiply
            res = reduce(lambda x, y: x*y,
                         (self.eval(program[ptr+j+1], params[j])
                          for j in range(2)))
            #position = program[ptr+3]
            position = self.eval_position(ptr+3, params[2])
            program[position] = res
            self.ptr += 4
        elif op == 3:
            # read input
            try:
                input = self.input.next()
            except StopIteration:
                print "No input remaining, returning..."
                raise
            position = self.eval_position(ptr+1, params[0])
            program[position] = input
            self.ptr += 2
        elif op == 4:
            # output
            out = self.eval(program[ptr+1], params[0])
            self.output.append(out)
            self.ptr += 2
        elif op == 5:
            # jump if true
            if self.eval(program[ptr+1], params[0]) != 0:
                self.ptr = self.eval(program[ptr+2], params[1])
            else:
                self.ptr += 3
        elif op == 6:
            # jump if false
            if self.eval(program[ptr+1], params[0]) == 0:
                self.ptr = self.eval(program[ptr+2], params[1])
            else:
                self.ptr += 3
        elif op == 7:
            # less than
            value = 1 if (self.eval(program[ptr+1], params[0]) <
                          self.eval(program[ptr+2], params[1])) \
                      else 0
            #position = program[ptr+3]
            position = self.eval_position(ptr+3, params[2])
            program[position] = value
            self.ptr += 4
        if op == 8:
            # equal
            value = 1 if (self.eval(program[ptr+1], params[0]) ==
                          self.eval(program[ptr+2], params[1])) \
                      else 0
            #position = program[ptr+3]
            position = self.eval_position(ptr+3, params[2])
            program[position] = value
            self.ptr += 4
        if op == 9:
            # adjust the relative base
            self.rel_base += self.eval(program[ptr+1], params[0])
            self.ptr += 2
        if op == 99:
            print "HALT"
            raise StopIteration

    def run(self):
        halt = False
        while not halt:
            try:
                self.execute_next_instruction()
            except StopIteration:
                print "Program Terminated"
                return self.output
            except Exception:
                print "Unhandled exception!"
                raise


def tests():
    for program, output in [
            ([109, -1, 4, 1, 99] , -1),
            ([109, -1, 104, 1, 99] , 1),
            ([109, -1, 204, 1, 99] , 109),
            ([109, 1, 9, 2, 204, -6, 99] , 204),
            ([109, 1, 109, 9, 204, -6, 99] , 204),
            ([109, 1, 209, -1, 204, -106, 99] , 204),
            ([109, 1, 3, 3, 204, 2, 99] , 1),
            ([109, 1, 203, 2, 204, 2, 99] , 1),]:
        input_generator = iter((1,))
        comp = IntcodeComputer(program, input_generator)
        out = comp.run()
        assert out == [output]


def part1(program):
    input_generator = iter((1,))
    comp = IntcodeComputer(program, input_generator)
    out = comp.run()
    print out

def part2(program):
    input_generator = iter((2,))
    comp = IntcodeComputer(program, input_generator)
    out = comp.run()
    print out


def main():
    program = load_program()
    tests()
    test_memory()
    part1(program)
    part2(program)


if __name__ == '__main__':
    main()
