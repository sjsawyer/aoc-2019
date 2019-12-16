
def load_field(infile):
    with open(infile, 'r') as f:
        field = [list(l.strip()) for l in f.readlines()]
    return field


def compute_gcd(x, y): 
    while(y): 
        x, y = y, x % y 
    return x 


def gridpoints(field):
    width, height = len(field), len(field[0])
    for i in range(height):
        for j in range(width):
            if field[i][j] == '#':
                yield (i, j)


def part1():
    field = load_field('data/10.txt')
    #field = [['#', '.', '#'],
    #         ['.', '#', '#'],
    #         ['#', '.', '#']]
    visible = [[0 for _ in range(len(field[0]))]
               for _ in field]
    for astroid1 in gridpoints(field):
        # find which astroids (i, j) can see
        seen = set()
        for astroid2 in gridpoints(field):
            if astroid1 == astroid2:
                # this is us
                continue
            # calculate the vector pointing from 1 to 2
            v = astroid2[0]-astroid1[0], astroid2[1]-astroid1[1]
            # directions
            hd, wd = v[0] >= 0, v[1] >= 0
            # reduce v to lowest form
            v = abs(v[0]), abs(v[1])
            gcd = compute_gcd(v[0], v[1])
            v = v[0]/gcd, v[1]/gcd
            seen.add((v, hd, wd))
        visible[astroid1[0]][astroid1[1]] = len(seen)
    #for row in field:
    #    print ' '.join(row)
    #for row in visible:
    #    print row
    best_score, best_i, best_j = 0, None, None
    width, height = len(field), len(field[0])
    for i in range(height):
        for j in range(width):
            if visible[i][j] > best_score:
                best_score = visible[i][j]
                best_i, best_j = i, j
    return best_score, (best_i, best_j)


def main():
    print part1()
    


if __name__ == '__main__':
    main()
