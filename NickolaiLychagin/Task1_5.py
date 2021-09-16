### Task 1.5
### Write a Python program to print all unique values of all dictionaries in a list.


def get_unique_values(input_list):
    unique_set = set()
    for each_dict in input_list:
        unique_set.update(list(each_dict.values()))
    print(unique_set)


# =============================================================================
# test_list = [{"V":"S001"}, {"V": "S002"}, {"VI": "S001"}, {"VI": "S005"}, {"VII":"S005"}, {"V":"S009"},{"VIII":"S007"}]
# get_unique_values(test_list)
# =============================================================================
