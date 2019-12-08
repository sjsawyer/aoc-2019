def load_opcode():
    with open("data/5.txt", "rb") as f:
        return [int(x) for x in f.read().split(',')]


def get_input():
    #return 5
    return 5


def val(num, param, opcode):
    if param == 0:
        return opcode[num]
    if param == 1:
        return num
    else:
        raise ValueError("invalid param {}".format(param))


def run(opcode):
    #opcode = restore_gravity(opcode, x, y)
    i = 0
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
            input = get_input()
            position = opcode[i+1]
            opcode[position] = input
            i += 2
            continue
        if op == 4:
            # output
            print val(opcode[i+1], params[0], opcode)
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


def main():
    opcode = load_opcode()
    run(opcode)


if __name__ == '__main__':
    main()
