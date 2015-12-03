from __future__ import print_function
from complexity import Mf
@Mf
def Loop1(n):
    s = 0
    for i in range(1, n + 1):
        for j in range(1, i * i + 1):
            s = s + 1
    return s

@Mf
def Loop2(n):
    s = 0
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            s = s + 1
    return s

@Mf
def Loop3(n):
    i = 0
    j = n
    while i <= j:
        i = i + 1
        j = j - 1
    return i

@Mf
def Loop4a(n):
    i = n
    while i > 0:
        i = (i - 1) / 2

@Mf
def Loop5(n):
    s = 1
    i = 1
    while i <= n:
        for j in range(1, i + 1):
            s = s + 1
        i = i * 2
    return s

@Mf
def Loop6(n):
    i = 1
    s = 1
    while i * i <= n:
        i = i + i
        s = s + 1
    return s

@Mf
def Loop7(n):
    s = 0
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            s = s + 1
    return s

@Mf
def Loop8(n):
    i = 0
    while i < n:
        j = i
        while j > 0:
            j = j / 2
        i = i + 1

@Mf
def nlogn(n):
    for i in range(n):
        j = 1
        while j < n:
            j += j

@Mf
def logn(n):
    j = 1
    while j < n:
        j += j

@Mf
def logsq(n):
    i = 1
    s = 0
    while i <= n:
        j = 1
        while j <= i:
            j = 2 * j
            s += 1
        i = 2 * i
    return s
    # Should be O(log(n)**2)

@Mf
def whilewhile(n):
    i = 1
    while i <= n:
        j = 1
        while j <= n:
            j = j + 1
        i = i + 1

@Mf
def arith(n):
    i = 37 * n
    s = 0
    while i < 53 * n:
        s += i
        i += 1
    return s

print(Loop1)
print(Loop2)
print(Loop3)
print(Loop4a)
print(Loop5)
print(Loop6)
print(Loop7)
print(Loop8)
print(nlogn)
print(logn)
print(logsq)
print(whilewhile)
print(arith)
