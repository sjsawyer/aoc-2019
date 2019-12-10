import sys


def counts(lst):
    c = {}
    for n in lst:
        c[n] = c.get(n, 0) + 1
    return c



def load_image():
    with open('data/8.txt', 'r') as f:
        content = f.read().strip()
    return [int(c) for c in content]


def display_image(img_array):
    # make easier for reading
    for l in range(len(img_array)):
        for m in range(len(img_array[0])):
            img_array[l][m] = '*' if img_array[l][m] == 1 else ' '
    for r in img_array:
        print ' '.join(r)


def part1(img):
    w, h = 25, 6
    layers = [img[i*w*h:(i+1)*w*h] for i in range(len(img)/(w*h))]
    min_zeros, min_layer, min_counts = sys.maxint, None, None
    for layer in layers:
        c = counts(layer)
        n_zeros = c[0]
        if n_zeros < min_zeros:
            min_zeros, min_layer, min_counts = n_zeros, layer, c
    return min_counts[1]*min_counts[2]


def part2(img):
    # 0 black, 1 white, 2 transparent
    w, h = 25, 6
    unseen = set(
        (i, j)
        for i in range(w)
        for j in range(h)
    )
    # we will populate the final image
    final_img = [[None for _ in range(w)]
                 for _ in range(h)]
    layers = [img[i*w*h:(i+1)*w*h] for i in range(len(img)/(w*h))]
    for layer in layers:
        if not unseen:
            # we've seen all pixels, early exit
            break
        # iterate over all points left to populate, first converting to list
        # to avoid iterating over a mutating data structure
        for (i, j) in list(unseen):
            # map coordinate (w, h) = (i, j) to its corresponding
            # index in the 1d array and check for transparency (2)
            if layer[j*w + i] != 2:
                # first non transparent pixel
                final_img[j][i] = layer[j*w + i]
                unseen.remove((i, j))
    display_image(final_img)


def main():
    img = load_image()
    print part1(img)
    part2(img)


if __name__ == '__main__':
    main()
