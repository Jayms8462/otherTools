# Function to convert decimal number to hexadecimal string
def decimal_to_hex(decimal_num):
    return hex(decimal_num).upper()[2:]  # Convert to uppercase hex string without '0x' prefix

# Original data structure with decimal numbers
data = {
    
}

# Convert decimal numbers to hexadecimal format
hex_data = {}
for key, nums in data.items():
    hex_nums = [decimal_to_hex(num) for num in nums]
    hex_data[key] = hex_nums

# Print the hexadecimal representation
for key, hex_nums in hex_data.items():
    print(f"{key}: {hex_nums}")