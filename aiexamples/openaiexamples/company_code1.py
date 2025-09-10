# a function to take a string and return a permutation of the string
def PermuteString(s):
    if len(s) == 0:
        return ['']
    PREVLIST = permute_string(s[1:len(s)])
    next_list = []
    for i in range(0,len(PREVLIST)):
        for j in range(0,len(s)):
            new_str = PREVLIST[i][0:j]+s[0]+PREVLIST[i][j:len(s)-1]
            if new_str not in next_list:
                next_list.append(new_str)
    return next_list

