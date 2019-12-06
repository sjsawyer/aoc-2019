import sys


def gen_passwords(lo, hi):
    max_len = len(str(hi))
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    passwds = []

    def _gen_passwds(start_idx, current, n_remaining, have_double):
        if n_remaining == 0:
            if not have_double:
                # not valid
                return
            if lo <= current <= hi:
                # we found one
                passwds.append(current)
            return
        # only loop over numbers whose index in `choices` is greater than
        # or equal to `start_idx` to keep increasing order
        for idx in range(start_idx, len(choices)):
            choice = choices[idx]
            # temporarily store prev value of have_double
            prev_have_double = have_double
            if current > 0:
                # check if `choice` is same as our last chosen digit
                have_double |= (current % 10 == choice)
            # "append" choice to our current number
            current = current*10 + choice
            _gen_passwds(idx, current, n_remaining-1, have_double)
            # backtrack
            current /= 10
            have_double = prev_have_double

    n_remaining = max_len
    have_double = False
    current = 0
    start_idx = 0
    # generate all passwds of length max_len
    _gen_passwds(start_idx, current, n_remaining, have_double)
    return passwds



def gen_passwords_strict(lo, hi):
    max_len = len(str(hi))
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    passwds = []

    def _gen_passwds(start_idx, current, n_remaining,
                     double_idxs, triple_idxs):
        if n_remaining == 0:
            if not double_idxs:
                # not valid
                return
            if not lo <= int(''.join(map(str, current))) <= hi:
                return
            # make sure double not part of triple
            doubs = set(double_idxs)
            trips = set(triple_idxs)
            for idx in trips:
                for _idx in range(idx-2, idx+1):
                    if _idx in doubs:
                        doubs.remove(_idx)
            if doubs:
                # we found one
                passwds.append(current[:])
            return
        # only loop over numbers whose index in `choices` is greater than
        # or equal to `start_idx` to keep increasing order
        curr_idx = len(current) + 1
        for idx in range(start_idx, len(choices)):
            choice = choices[idx]
            double, triple = False, False
            # check if we have a double
            if current and choice == current[-1]:
                double_idxs.append(curr_idx)
                double = True
                # check if we have a triple
                if len(current) > 1 and current[-2] == choice:
                    triple_idxs.append(curr_idx)
                    triple = True
            current.append(choice)
            _gen_passwds(idx, current, n_remaining-1,
                         double_idxs, triple_idxs)
            # backtrack
            current.pop()
            if double:
                double_idxs.pop()
            if triple:
                triple_idxs.pop()

    n_remaining = max_len
    current = []
    start_idx = 0
    double_idxs = []
    triple_idxs = []
    # generate all passwds of length max_len
    _gen_passwds(start_idx, current, n_remaining,
                 double_idxs, triple_idxs)
    return passwds



def solve(lo, hi):
    passwords = gen_passwords_strict(lo, hi)
    print "total:", len(passwords)
    print "sample:", passwords[1:10000:250]
    print "test:", 123456 not in passwords


def main():
    input = sys.argv[-1]
    lo, hi = map(int, input.split('-'))
    solve(lo, hi)
    


if __name__ == '__main__':
    main()
