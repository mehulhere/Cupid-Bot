import json

# Define the dictionary
my_dict = {
    42424242442424: [[], 4284824942942],
    637345182651514891: [[1, 2, 3, 4, 5], '556780158804033567', 0],
    556780158804033567: [[1, 2, 3, 4, 5], 637345182651514891]
}

# Convert the dictionary to a JSON string
json_str = json.dumps(my_dict)

# Write the JSON string to a file
with open('my_dict.json', 'w') as f:
    f.write(json_str)