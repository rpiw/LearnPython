
def task_1() -> str:
    """Find PI to the Nth Digit - Enter a number and have the program generate PI up to that many decimal places.
    Keep a limit to how far the program will go."""
    from math import pi
    limit = 1000

    try:
        dec = int(input("Enter number of decimal places as positive integer"))
    except ValueError:
        print("This is not an integer!")
    if dec > limit or dec < 0:
        dec = 2
        print("Wrong value. Positive integers lesser than: {limit}, using default value: {d}".format(limit=limit, d=dec))

    return str(round(pi, dec))


def task_2() -> str:
    """Find e to the Nth Digit - Just like the previous problem, but with e instead of PI. Enter a number and have the
    program generate e up to that many decimal places. Keep a limit to how far the program will go."""
    from math import e

    limit = 1000
    try:
        dec = int(input("Enter number of decimal places as positive integer"))
    except ValueError:
        print("This is not an integer!")
    if dec > limit or dec < 0:
        dec = 2
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


if __name__ == '__main__':
    import unittest
    import test_main
    suite = unittest.TestLoader().loadTestsFromModule(test_main)
    unittest.TextTestRunner(verbosity=2).run(suite)
