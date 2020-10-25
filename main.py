
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


if __name__ == '__main__':
    print(task_1())
