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
            break

        if is_prime(number):
            print(number)
        number += 2
        run = str(input("To stop program type 'stop'. To skip some number, type 'skip x', where x is an int."))


if __name__ == '__main__':
    import unittest
    import test_main
    suite = unittest.TestLoader().loadTestsFromModule(test_main)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    task_5()
