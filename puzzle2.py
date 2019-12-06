def load_opcode():
    with open("data/2.txt", "rb") as f:
        return [int(x) for x in f.read().split(',')]


def restore_gravity(opcode, x, y):
    opcode[1] = x
    opcode[2] = y
    return opcode


ops = {
    1: lambda x, y: x+y,
    2: lambda x, y: x*y,
}


def part1(opcode, x, y):
    opcode = restore_gravity(opcode, x, y)
    i = 0
    while opcode[i] != 99:
        # check valid operator code
        assert opcode[i] in ops
        func = ops[opcode[i]]
        # next two values are indexes of the values
        nums = opcode[opcode[i+1]], opcode[opcode[i+2]]
        res = func(*nums)
        # insert into new position
        pos = opcode[i+3]
        opcode[pos] = res
        i += 4
    return opcode[0]


def find_noun_verb(opcode, target, lo, hi):
    for noun in range(lo, hi+1):
        for verb in range(lo, hi+1):
            res = part1(opcode[:], noun, verb)
            if res == target:
                return noun, verb


def main():
    opcode = load_opcode()
    noun, verb = find_noun_verb(opcode, 19690720, 0, 99)
    print noun, verb



if __name__ == '__main__':
    main()
