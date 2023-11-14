# File to test quick snippets
with open('./text_input.txt') as f:
    input_string=''.join(line for line in f)
print(input_string)