import sys


def is_double(num_list, strict=False):
    if strict:
        # A double cannot be, e.g., 777
        for i in range(len(num_list)-1):
            if num_list[i] == num_list[i+1]:
                # found a pair, is it valid?
                if i > 0:
                    # check preceding digit
                    if num_list[i-1] == num_list[i]:
                        continue
                if i == len(num_list)-2:
                    # last two digits
                    return True
                if num_list[i+1] == num_list[i+2]:
                    continue
                return True
        return False
    else:
        # A double can be, e.g., 777
        return any(num_list[i] == num_list[i+1]
                   for i in range(len(num_list)-1))


#def is_double_strict(num_list):
#    double_idxs = [i for i in range(len(num_list)-1)
#                   if num_list[i] == num_list[i+1]]
#    triple_idxs = [i for i in range(len(num_list)-2)
#                   if num_list[i] == num_list[i+1] == num_list[i+2]]
#    for di in double_idxs:
#        for ti in triple_idxs:




def increasing(num_list):
    return all(num_list[i] <= num_list[i+1]
               for i in range(len(num_list)-1))

#def gen_doubles(lo, hi):
#    lo_list, hi_list = list(str(lo)), list(str(hi))
#    lo_len, hi_len = len(lo_list), len(hi_list)
#    min_num, max_num = int('1' + '0'*(lo_len-1)), \
#                       int('9'*hi_len)



def solve(lo, hi):
    num_passwords = 0
    for num in range(lo, hi+1):
        num_list = list(str(num))
        if is_double(num_list, strict=False) and increasing(num_list):
            num_passwords += 1
    return num_passwords


def main():
    input = sys.argv[-1]
    lo, hi = map(int, input.split('-'))
    print solve(lo, hi)
    


if __name__ == '__main__':
    main()
