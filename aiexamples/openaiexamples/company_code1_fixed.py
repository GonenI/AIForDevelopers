# @@@@@@ a function to take a string and return a permutation of the string
def permute_string(s):
    if len(s) == 0:
        return ['']
    prev_list = permute_string(s[1:len(s)])
    next_list = []
    for i in range(0,len(prev_list)):
        for j in range(0,len(s)):
            new_str = prev_list[i][0:j]+s[0]+prev_list[i][j:len(s)-1]
            if new_str not in next_list:
                next_list.append(new_str)
    return next_list