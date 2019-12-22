import math


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


def part1(field):
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



def compute_angle(v, vd, hd):
    # recall v is (vertical, horizontal)
    v = map(float, v)
    if v[1] == 0:
        return 0 if not vd else math.pi
    if v[0] == 0:
        return math.pi/2 if hd else 3*math.pi/2
    if vd and hd:
        return math.pi/2 - math.atan(v[0]/v[1])
    if not vd and hd:
        return math.pi/2 + math.atan(v[0]/v[1])
    if not vd and not hd:
        return 3*math.pi/2 - math.atan(v[0]/v[1])
    if vd and not hd:
        return 3*math.pi/2 + math.atan(v[0]/v[1])


def part2(field, station):
    astroids = {}
    for astroid in gridpoints(field):
        import pdb; pdb.set_trace()
        if astroid == station:
            continue
        # Tag all astroids with the following information:
        # - distance from station
        # - (y, x) vector direction (simplified)
        # - right of station (bool)
        # - down of station (bool)
        dist = ((astroid[0] - station[0])**2 +
                (astroid[1] - station[1])**2) ** 0.5

        # calculate the vector pointing from station to astroid
        v = astroid[0]-station[0], astroid[1]-station[1]
        # magnitude^2 (don't require actual distance)
        d = v[0]**2 + v[1]**2
        # directions
        vd, hd = v[0] >= 0, v[1] >= 0
        # reduce v to lowest form
        v = abs(v[0]), abs(v[1])
        gcd = compute_gcd(v[0], v[1])
        v = v[0]/gcd, v[1]/gcd
        # get angle used by laser
        angle = compute_angle(v, vd, hd)
        # add to map
        print
        print (v, vd, hd)
        print (angle, d, astroid)
        if (v, vd, hd) not in astroids:
            astroids[(v, vd, hd)] = []
        astroids[(v, vd, hd)].append((angle, d, astroid))

    # now sort by angle
    # (1=value of .items(), 0=first thing in list, 0=angle)
    astroids = sorted(astroids.items(),
                      key=lambda t: t[1][0][0])
    import pdb; pdb.set_trace()
    # sort each sublist by decreasing distance so we can
    # cleanly pop()
    for astroid in astroids:
        astroid[-1].sort(key=lambda t: -t[1])

    # now we spin and shoot astroids
    i, count = 0, 0
    while count != 200:
        j = i % len(astroids)
        # shoot!
        astroid = astroids[j][1].pop()
        #print astroid
        if not astroids[j][1]:
            # no more astroids here
            del astroids[j]
            # don't increase i here! we will just continue from
            # where we left off
        else:
            i += 1
        count += 1

    print "last astroid:", astroid
    return astroid[-1]


def main():
    field = load_field('data/10.txt')
    #field = [['#', '.', '#'],
    #         ['.', '#', '#'],
    #         ['#', '.', '#']]
    n_seen, (i, j) = part1(field)
    print n_seen, (i, j)
    twohundredthastroid = part2(field, (i, j))
    print twohundredthastroid[1]*100 + twohundredthastroid[0]
    


if __name__ == '__main__':
    main()
