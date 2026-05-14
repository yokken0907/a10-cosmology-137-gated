with open('a10_2f_ef.yaml', 'r') as f:
    lines = f.readlines()

with open('a10_2f_ef.yaml', 'w') as f:
    for line in lines:
        if "drop: true" not in line:
            f.write(line)
