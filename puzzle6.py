import sys
from collections import defaultdict


# center of mass
COM = 'COM'


def build_tree_directed(vertices):
    # build a tree, represented as an adjacency list
    tree = defaultdict(list)
    for v in vertices:
        orbitee, orbiter = v
        tree[orbitee].append(orbiter)
        # ensure `orbiter` is in tree for later logic
        if orbiter not in tree:
            tree[orbiter] = list()
    # sanity check
    assert COM in tree
    return tree


def build_tree_undirected(vertices):
    tree = defaultdict(set)
    for v1, v2 in vertices:
        # don't worry about direction now
        tree[v1].add(v2)
        tree[v2].add(v1)
    return tree


def part1(vertices):
    tree = build_tree_directed(vertices)

    def count_orbits_from_node(node, depth):
        ''' Return number of orbits from node `node` and onwards '''
        # COM has no direct orbit, all others have 1
        n_direct_orbits = 1 if node != COM else 0
        # COM and orbitees have no indirect orbits, all others
        # have `depth-1` indirect orbits
        n_indirect_orbits = max(depth-1, 0)
        # count orbits from here
        orbitees = tree[node]
        n_orbits_from_here = \
            sum(count_orbits_from_node(orbitee, depth+1)
                for orbitee in orbitees)
        return (n_direct_orbits +
                n_indirect_orbits +
                n_orbits_from_here)

    # count direct and indirect orbits, starting from COM
    return count_orbits_from_node(COM, 0)


def part2(vertices):
    tree = build_tree_undirected(vertices)

    # find path from YOU to SAN
    YOU, SAN = 'YOU', 'SAN'
    neighbors = tree[YOU]
    # initalize steps taken for each neighbor as 0
    _steps = (0 for n in neighbors)
    to_visit = zip(neighbors, _steps)
    # so far we've seen ourselves
    seen = {YOU}
    # traverse DFS
    while to_visit:
        current, steps = to_visit.pop()
        seen.add(current)
        if SAN in tree[current]:
            # we found him!
            return steps
        # otherwise visit all our neighbors
        for neighbor in tree[current]:
            if neighbor in seen:
                # don't revisit ourselves
                continue
            to_visit.append((neighbor, steps+1))
    raise RuntimeError('santa not found!')


def main():
    infile = "data/6.txt"
    with open(infile, "r") as f:
        pairs = [l.strip() for l in f.readlines()]
    # convert to list of vertice pairs
    vertices = [pair.split(")") for pair in pairs]
    # solve
    print part1(vertices)
    print part2(vertices)


if __name__ == '__main__':
    main()
