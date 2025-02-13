def fibonacci_upto_100():
    a, b = 0, 1
    while a <= 100:
        print(a, end=' ')
        a, b = b, a + b

fibonacci_upto_100()
