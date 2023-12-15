def recursive_sort_dict(input_dict):
    sorted_dict = {}
    
    for key, value in sorted(input_dict.items()):
        if isinstance(value, dict):
            sorted_dict[key] = recursive_sort_dict(value)
        else:
            sorted_dict[key] = value

    return sorted_dict


my_dict = {'b': 2, 'a': 1, 'd': {'c': 3, 'a': 1}, 'c': 3}

sorted_dict = recursive_sort_dict(my_dict)

# Display the sorted dictionary
print("Original Dictionary:", my_dict)
print("Sorted Dictionary:", sorted_dict)