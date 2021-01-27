import re


def task_1() -> str:
    """Find PI to the Nth Digit - Enter a number and have the program generate PI up to that many decimal places.
    Keep a limit to how far the program will go."""
    from math import pi
    limit = 1000
    dec = 2
    try:
        dec = int(input("Enter number of decimal places as positive integer"))
    except ValueError:
        print("This is not an integer!")
    if dec > limit or dec < 0:
        print("Wrong value. Positive integers lesser than: {limit}, using default value: {d}".format(limit=limit, d=dec))

    return str(round(pi, dec))


def task_2() -> str:
    """Find e to the Nth Digit - Just like the previous problem, but with e instead of PI. Enter a number and have the
    program generate e up to that many decimal places. Keep a limit to how far the program will go."""
    from math import e

    limit = 1000
    dec = 2
    try:
        dec = int(input("Enter number of decimal places as positive integer"))
    except ValueError:
        print("This is not an integer!")
    if dec > limit or dec < 0:
        print("Wrong value. Positive integers lesser than: {limit}, using default value: {d}".format(limit=limit, d=dec))

    return str(round(e, dec))


def task_3(number: int) -> tuple:
    u"""Fibonacci Sequence - Enter a number and have the program generate the Fibonacci sequence
    to that number or to the Nth number."""
    try:
        number = int(number)
    except ValueError:
        return tuple()
    seq = [1, 1]
    for i in range(2, number):
        seq.append(seq[i - 1] + seq[i - 2])
    return tuple(seq)


def task_4(number: int) -> list:
    u"""Prime Factorization - Have the user enter a number and find all Prime Factors (if there are any)
        and display them."""
    results = []
    digit = 2
    try:
        number = int(number)
    except ValueError:
        return results

    while digit * digit <= number:
        while number % digit == 0:
            results.append(digit)
            number = number / digit
        digit += 1
    return results


def task_5():
    u"""Next Prime Number - Have the program find prime numbers until the user chooses to stop asking for
        the next one."""
    def is_prime(number) -> bool:
        d = 3
        if number % 2 == 0:
            return False
        while d * d <= number:
            if number % d == 0:
                return False
            d += 2
        return True

    stop = False
    skip = 0
    number = 3
    run = str(input("To stop program type 'stop'. To skip some number, type 'skip x', where x is an int."))

    while not stop:
        try:
            if "skip" in run:
                skip = int(re.split(" ", run)[-1])
                run = ""
                print("Skipping: {}".format(skip))

            if int(skip) > 0:
                skip -= 1
                number += 2
                continue
        except ValueError:
            print("eee")
            continue

        if run == "stop":
            raise SystemExit

        if is_prime(number):
            print(number)
        number += 2
        run = str(input("To stop program type 'stop'. To skip some number, type 'skip x', where x is an int."))


def task_6(w, h):
    u"""Find Cost of Tile to Cover W x H Floor - Calculate the total cost of tile it would take to cover
        a floor plan of width and height, using a cost entered by the user."""
    try:
        w = float(w)
        h = float(h)
    except ValueError:
        return
    cost = float(input("Enter a cost."))
    return cost * w * h


def task_7(loan, rate):
    u"""Mortgage Calculator - Calculate the monthly payments of a fixed term mortgage over given Nth terms at a given
    interest rate. Also figure out how long it will take the user to pay back the loan. For added complexity,
    add an option for users to select the compounding interval (Monthly, Weekly, Daily, Continually).
    """
    assert 0.00 < rate < 1.00
    assert loan > 0.0
    # Ive got no idea how mortgage are calculated :P
    payment = loan * (1 + rate)
    n = int(input("How many months?"))
    interval = str(input("What interval type you are interested in? Accepted: m, w, d, c"))
    res = None
    if interval == "m":
        res = "monthly"
        payment /= n
    elif interval == "w":
        res = "weekly"
        payment /= (4 * n)
    elif interval == "d":
        res = "daily"
        payment /= (30 * n)
    elif interval == "c":
        res = "continually"
        c = float(input("Give the interval in hours"))
        payment /= (30 * c * n)
    print("Your {} payments are: {:.2f}".format(res, payment))


# Classic Algorithms
import matplotlib.pyplot as plt


def collatz_conjecture(number: int):
    u"""Collatz Conjecture - Start with a number n > 1. Find the number of steps it takes to reach one using
    the following process: If n is even, divide it by 2. If n is odd, multiply it by 3 and add 1."""
    def collatz(n):
        return n / 2 if n % 2 == 0 else 3 * n + 1

    results = [number]
    for i in range(1000):
        n = collatz(results[-1])
        results.append(n)
        if n == 1:
            break

    print("Steps: {}".format(len(results)))
    plt.figure()
    plt.plot(results, "*-")
    plt.show()


def merge_sort(seq):
    if len(seq) > 1:
        mid = len(seq)//2
        left = seq[:mid]
        right = seq[mid:]

        merge_sort(left)
        merge_sort(right)

        i, j, k = 0, 0, 0
        while len(left) > i and len(right) > j:
            if left[i] < right[j]:
                seq[k] = left[i]
                i += 1
            else:
                seq[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            seq[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            seq[k] = right[j]
            j += 1
            k += 1


def bubble_sort(seq):
    i = 0
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, len(seq)):
            if seq[i] < seq[i - 1]:
                seq[i], seq[i - 1] = seq[i - 1], seq[i]
                swapped = True
            i += 1


class Text:
    u"""Text related problems."""

    @staticmethod
    def task_1():
        u"""Fizz Buzz - Write a program that prints the numbers from 1 to 100. But for multiples of three print
        “Fizz” instead of the number and for the multiples of five print “Buzz”. For numbers which are multiples of
        both three and five print “FizzBuzz”.
        """
        for i in range(1, 101):
            if i % 3 == 0 and i % 5 != 0:
                print("Fizz")
            elif i % 3 != 0 and i % 5 == 0:
                print("buzz")
            elif i % (3 * 5) == 0:
                print("FizzBuzz")
            else:
                print(i)

    @staticmethod
    def task_2():
        u"""Reverse a String - Enter a string and the program will reverse it and print it out."""
        return input("Please, provide a string\n")[::-1]


if __name__ == '__main__':
    print(Text.task_2())
