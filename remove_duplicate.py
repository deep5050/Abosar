# Open the input file in read mode
with open("onnoalo", "r") as file:

    # Read all lines into a list
    lines = file.readlines()

# Remove duplicates while preserving order
unique_lines = []
for line in lines:
    if line not in unique_lines:
        unique_lines.append(line)

# Open the output file in write mode
with open("output_file.txt", "w") as file:

    # Write the unique lines to the output file
    for line in unique_lines:
        file.write(line)
