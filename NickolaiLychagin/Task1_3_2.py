### Task 1.3
### Create a program that asks the user for a number and then prints out a list of all the divisors of that number.


def get_divisors():
    while True:
        input_string = input("Please enter a positive integer\n")
        try:
            number = int(input_string)
            break
        except:
            pass
    list_of_divisors = []
    for i in range(1, number + 1):
        if number % i == 0:
            list_of_divisors.append(i)
    print(list_of_divisors)


# =============================================================================
# get_divisors()
# =============================================================================
