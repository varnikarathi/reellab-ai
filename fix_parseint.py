import sys

file_path = sys.argv[1]

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("const start = parseInt(parts[0], 10);",
                          "const start = parseInt(parts[0] || '0', 10);")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Fixed parseInt')
