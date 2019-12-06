def load_weights():
    with open("data/1.txt", "rb") as f:
        return [int(w) for w in f.readlines()]


def calc_fuel(weight):
    return weight//3 - 2


def total_fuel(weight):
    fuel = calc_fuel(weight)
    if fuel <= 0:
        return 0
    return fuel + total_fuel(fuel)


def part1():
    return sum(calc_fuel(w) for w in load_weights())


def part2():
    return sum(total_fuel(w) for w in load_weights())


def main():
    print part1()
    print part2()


if __name__ == '__main__':
    main()
