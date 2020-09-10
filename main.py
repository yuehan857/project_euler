import math
import numpy as np
import pandas as pd

# ********************** 100_arranged_probability **********************

def find_arr(start):
    N = math.floor(start)
    n = math.floor(0.7 * N)
    t1 = 0
    t2 = 0
    while 2 * n * (n - 1) != N * (N - 1):
        if 2 * n * (n - 1) < N * (N - 1):
            n = n + 1
            t1 = t1 + 1
        else:
            N = N + 1
            t2 = t2 + 1

    t = t1 + t2

    print("iterate", t1, "+", t2, "=", t, "times")

    return N, n

def find_arr2(start):
    N = 21
    n = 15
    t = 0
    while N < start:
        N_temp = N
        n_temp = n
        N = 4 * n_temp + 3 * N_temp - 3
        n = 3 * n_temp + 2 * N_temp - 2
        t = t + 1

    print("iterate", t, "times")

    return N, n

print(find_arr(1e2))
print(find_arr(1e4))
print(find_arr(1e6))

print(find_arr2(1e2))
print(find_arr2(1e4))
print(find_arr2(1e6))

print(find_arr2(1e12))

# reference: https://www.mathblog.dk/project-euler-100-blue-discs-two-blue/





# ********************** 54_poker_hands **********************

hands = pd.read_csv('p054_poker.txt', header = None)
card_num = range(0, 9)
hands = pd.concat([hands[0].str.split(' ', expand=True)], axis = 1, names = card_num)

# arrange card

def rep_jqka(val):
    letters = ["T", "J", "Q", "K", "A"]
    v = 9
    for j in letters:
        v = v + 1
        while j in val:
            val[val.index(j)] = v

    return val

def arrang_card(cards, a_b):
    if a_b == "a":
        start = 0
    elif a_b == "b":
        start = 5

    val = []
    suit = []
    for i in range(start, start + 5):
        temp = cards[i].str.split('').tolist()
        val.append(temp[0][1])
        suit.append(temp[0][2])

    val = sorted(list(map(int, rep_jqka(val))))

    return val, suit

arrang_card(hands[0:1], "a")

# find pattern

def check_pairs(val):
    pairs = []
    for i in range(2, 15):
        if val.count(i) == 2:
            pairs.append(i)

    return sorted(pairs)

def check_three(val):
    three = 0
    for i in range(2, 15):
        if val.count(i) == 3:
            three = i

    return three

def check_four(val):
    four = 0
    for i in range(2, 15):
        if val.count(i) == 4:
            four = i

    return four

def check_straight(val):
    straight = 0
    check = len(check_pairs(val)) == 0 and check_three(val) == 0 and check_four(val) == 0
    if check:
        if val[-1] - val[0] == 4:
            straight = val[-1]

    return straight

def check_flush(suit):
    flush = 0
    if len(set(suit)) == 1:
        flush = 1

    return flush

def find_pattern(val, suit):
    pairs = check_pairs(val)
    three = check_three(val)
    four = check_four(val)
    straight = check_straight(val)
    flush = check_flush(suit)

    if straight and flush:
        pattern = 1
    elif four:
        pattern = 2
    elif len(pairs) == 1 and three:
        pattern = 3
    elif flush:
        pattern = 4
    elif straight:
        pattern = 5
    elif three:
        pattern = 6
    elif len(pairs) == 2:
        pattern = 7
    elif len(pairs) == 1:
        pattern = 8
    else:
        pattern = 9

    cache = [pairs, three, four, straight, flush]

    return cache, pattern

# compare: pattern > value

def high(a, b, a2=0, b2=0, a3=0, b3=0):
    if a > b:
        r = 1
    elif a < b:
        r = 0
    elif a2 > b2:
        r = 1
    elif a2 < b2:
        r = 0
    elif a3 > b3:
        r = 1
    else:
        r = 0

    return r

def compare_high(a, b, p, v_a, v_b):
    if p == 1:
        r = high(a[3], b[3])
    elif p == 2:
        r = high(a[2], b[2])
    elif p == 3:
        r = high(a[1], b[1], a[0][0], b[0][0])
    elif p == 4:
        r = high(max(v_a), max(v_b))
    elif p == 5:
        r = high(a[3], b[3])
    elif p == 6:
        r = high(a[1], b[1])
    elif p == 7:
        a3 = list(set(v_a))
        a3.remove(a[0][1])
        a3.remove(a[0][0])
        b3 = list(set(v_b))
        b3.remove(b[0][1])
        b3.remove(b[0][0])
        r = high(a[0][1], b[0][1], a[0][0], b[0][0], a3, b3)
    elif p == 8:
        a2 = list(set(v_a))
        a2.remove(a[0][0])
        b2 = list(set(v_b))
        b2.remove(b[0][0])
        r = high(a[0][0], b[0][0], max(a2), max(b2))
    elif p == 9:
        r = high(max(v_a), max(v_b))

    return r

def compare(val_a, suit_a, val_b, suit_b):
    cache_a, pattern_a = find_pattern(val_a, suit_a)
    cache_b, pattern_b = find_pattern(val_b, suit_b)
    if pattern_a < pattern_b:
        result = 1
    elif pattern_a > pattern_b:
        result = 0
    else:
        result = compare_high(cache_a, cache_b, pattern_a, val_a, val_b)

    return result, cache_a, cache_b, pattern_a, pattern_b

# do a loop for 1000 hands

def main(hands):
    a_win = 0
    for i in range(0, len(hands)):
        val_a, suit_a = arrang_card(hands[i:(i + 1)], "a")
        val_b, suit_b = arrang_card(hands[i:(i + 1)], "b")
        a_win = a_win + compare(val_a, suit_a, val_b, suit_b)[0]

    return a_win

print(main(hands))

# reference：https://blog.dreamshire.com/project-euler-54-solution/





# ********************** 85_counting_rectangles **********************

def counting_rect(n, m):
    rect = np.zeros([n, m])
    for i in range(0, n):
        for j in range(0, m):
            rect[i, j] = (n - i) * (m - j)

    return np.sum(rect)

near_2e6 = []

L = 2000
k = 1
while k <= L:
    l = 1
    while counting_rect(k, l) < 2e6:
        l = l + 1
    near_2e6.append([k, l - 1, counting_rect(k, l - 1)])
    near_2e6.append([k, l , counting_rect(k, l)])
    L = l
    k = k + 1

near_2e6 = pd.DataFrame(near_2e6).astype(int)

diff = abs(near_2e6[2] - 2e6)
min_idx = diff.argmin(axis = 0)
near_2e6[min_idx:min_idx + 1]

# reference:https://www.mathblog.dk/project-euler-85-rectangles-rectangular-grid/