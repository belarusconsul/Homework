### Task 1.6
### Write a program which makes a pretty print of a part of the multiplication table.


def print_mult_table(a, b, c, d):
    print(end="\t\t")
    for i in range(c, d + 1):
        print(i, end="\t\t")
    print(end="\n\n")
    for j in range(a, b + 1):
        print(j, end="\t\t")
        for k in range(c, d + 1):
            print(j * k, end="\t\t")
        print(end="\n\n")


# =============================================================================
# print_mult_table(2, 4, 3, 7)
# =============================================================================
