"""
Manacher's algorithm is used to find the longest palindromic
substring in a given string in O(n) time.
e.g. 'eabcbadf' -> 'abcba'
"""


def manacher_palindromic(s: str) -> str:
    s = '|' + '|'.join(s) + '|'
    p = [0] * len(s)
    r = 0
    c = 0
    i = 1
    for i in range(len(s)):
        j = 2 * c - i
        if i < c + p[c]:
            if j - p[j] > c - p[c]:
                # case 1
                p[i] = p[j]
                l = -1
            else:
                # case 2
                p[i] = c + p[c] - i
                l = 2 * i - r
        else:
            # case 3
            r = i
            l = i
        while l >= 0 and r < len(s) and s[r] == s[l]:
            p[i] += 1
            r += 1
            l -= 1
        if i + p[i] > c + p[c]:
            c = i
    m = max(p)
    c = p.index(m)
    return s[c - m + 1:c + m].replace('|', '')


if __name__ == '__main__':
    a = manacher_palindromic('cabbaded')
    print(a)
