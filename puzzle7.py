from collections import deque


def load_opcode():
    with open("data/7.txt", "rb") as f:
        return [int(x) for x in f.read().split(',')]


def val(num, param, opcode):
    if param == 0:
        return opcode[num]
    if param == 1:
        return num
    else:
        raise ValueError("invalid param {}".format(param))


def run(opcode, input_generator):
    i = 0
    output = []
    while opcode[i] != 99:
        op = opcode[i] % 100
        params = (opcode[i]/100) % 10, (opcode[i]/1000) % 10, (opcode[i]/10000) % 10
        # sanity check
        assert op in {1, 2, 3, 4, 5, 6, 7, 8}
        assert all(p in {0, 1} for p in params)

        if op == 1:
            # we add
            res = sum(val(opcode[i+j+1], params[j], opcode)
                      for j in range(2))
            position = opcode[i+3]
            opcode[position] = res
            i += 4
            continue
        if op == 2:
            # we multiply
            res = reduce(lambda x, y: x*y,
                         (val(opcode[i+j+1], params[j], opcode)
                          for j in range(2)))
            position = opcode[i+3]
            opcode[position] = res
            i += 4
            continue
        if op == 3:
            # read input
            input = input_generator.next()
            position = opcode[i+1]
            opcode[position] = input
            i += 2
            continue
        if op == 4:
            # output
            out = val(opcode[i+1], params[0], opcode)
            output.append(out)
            i += 2
            continue
        if op == 5:
            # jump if true
            if val(opcode[i+1], params[0], opcode) != 0:
                i = val(opcode[i+2], params[1], opcode)
            else:
                i += 3
            continue
        if op == 6:
            # jump if false
            if val(opcode[i+1], params[0], opcode) == 0:
                i = val(opcode[i+2], params[1], opcode)
            else:
                i += 3
            continue
        if op == 7:
            # less than
            value = 1 if (val(opcode[i+1], params[0], opcode) <
                          val(opcode[i+2], params[1], opcode)) \
                      else 0
            #position = val(opcode[i+3], params[2], opcode)
            position = opcode[i+3]
            opcode[position] = value
            i += 4
            continue
        if op == 8:
            # equal
            value = 1 if (val(opcode[i+1], params[0], opcode) ==
                          val(opcode[i+2], params[1], opcode)) \
                      else 0
            #position = val(opcode[i+3], params[2], opcode)
            position = opcode[i+3]
            opcode[position] = value
            i += 4
            continue
    return output


def all_permutations(elements):
    perms = []

    def _all_permutations(current, remaining):
        if not remaining:
            perms.append(current[:])
        else:
            for _ in range(len(remaining)):
                current.append(remaining.popleft())
                _all_permutations(current, remaining)
                remaining.append(current.pop())

    _all_permutations([], deque(elements))
    return perms


def part1(opcode):
    choices = [0, 1, 2, 3, 4]
    max_thrust = -float('inf')
    for phases in all_permutations(choices):
        input = 0
        for phase in phases:
            input_generator = iter((phase, input))
            res = run(opcode[:], input_generator)
            # should have returned a list of one thing
            assert len(res) == 1
            output = res[0]
            # set return value as next input
            input = output
        max_thrust = max(max_thrust, output)
    print "max_thrust:", max_thrust


def part2(opcode):
    choices = [5, 6, 7, 8, 9]
    max_thrust = -float('inf')
    for phases in all_permutations(choices):
    #for phases in [[9, 8, 7, 6, 5]]:
        input = 0
        phase_idx = 0
        while True:
            phase = phases[phase_idx]
            input_generator = iter((phase, input))
            
            res = run(opcode, input_generator)
            # should have returned a list of one thing
            assert len(res) == 1
            output = res[0]
            # set return value as next input
            input = output
            # cycle through phases
            phase_idx = (phase_idx + 1) % len(phases)

        max_thrust = max(max_thrust, output)
    print "max_thrust:", max_thrust


def main():
    opcode = load_opcode()
    #part1(opcode)
    opcode=[3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
            27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    part2(opcode)


if __name__ == '__main__':
    main()
