# Task 4.1
# Open file `data/unsorted_names.txt` in data folder. Sort the names and
# write them to a new file called `sorted_names.txt`. Each name should
# start with a new line as in the following example:

with open("data/unsorted_names.txt", "r") as file_unsorted:
    with open("data/sorted_names.txt", "w") as file_sorted:
        file_sorted.writelines(sorted(file_unsorted.readlines()))