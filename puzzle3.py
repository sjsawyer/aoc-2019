import sys


def get_points(moves):
    ''' Find all points traced by `moves` '''
    points = set()
    current = [0, 0]
    for move in moves:
        direction, distance = move[0], int(move[1:])
        if direction == 'R':
            for _ in range(distance):
                current[1] += 1
                points.add(tuple(current))
        elif direction == 'L':
            for _ in range(distance):
                current[1] -= 1
                points.add(tuple(current))
        elif direction == 'U':
            for _ in range(distance):
                current[0] += 1
                points.add(tuple(current))
        elif direction == 'D':
            for _ in range(distance):
                current[0] -= 1
                points.add(tuple(current))
        else:
            raise RuntimeError("unknown direction")
    return points


def solve(l1, l2):
    points1 = get_points(l1)
    points2 = get_points(l2)
    # get all intersection points
    points = points1.intersection(points2)
    return sum(min(points, key=lambda t: abs(t[0]) + abs(t[1])))



def get_points2(moves):
    ''' Find all points traced by `moves` '''
    points = set()
    current = [0, 0]
    step_map = {}
    steps = 0
    for move in moves:
        direction, distance = move[0], int(move[1:])
        if direction == 'R':
            for _ in range(distance):
                current[1] += 1
                point = tuple(current)
                points.add(point)
                steps += 1
                # Keep track of number of steps
                if point not in step_map:
                    step_map[point] = steps
        elif direction == 'L':
            for _ in range(distance):
                current[1] -= 1
                point = tuple(current)
                points.add(point)
                steps += 1
                # Keep track of number of steps
                if point not in step_map:
                    step_map[point] = steps
        elif direction == 'U':
            for _ in range(distance):
                current[0] += 1
                point = tuple(current)
                points.add(point)
                steps += 1
                # Keep track of number of steps
                if point not in step_map:
                    step_map[point] = steps
        elif direction == 'D':
            for _ in range(distance):
                current[0] -= 1
                point = tuple(current)
                points.add(point)
                steps += 1
                # Keep track of number of steps
                if point not in step_map:
                    step_map[point] = steps
        else:
            raise RuntimeError("unknown direction")

    return points, step_map


def solve2(l1, l2):
    points1, steps1 = get_points2(l1)
    points2, steps2 = get_points2(l2)
    # get all intersection points
    points = points1.intersection(points2)
    # get intersection point with smallest number of steps
    min_steps = float('inf')
    for point in points:
        min_steps = min(min_steps,
                        steps1[point] + steps2[point])
    return min_steps


def main():
    input1, input2 = sys.argv[-2:]
    input1 = input1.split(',')
    input2 = input2.split(',')
    print solve2(input1, input2)

    


if __name__ == '__main__':
    main()
