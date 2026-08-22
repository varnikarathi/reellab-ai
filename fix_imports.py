import sys
import re

file_path = sys.argv[1]

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix imports in reelsController
content = content.replace("import type { Request, Response } from 'express';",
                          "import type { Request, Response } from 'express';\nimport fs from 'node:fs';\nimport path from 'node:path';")

content = content.replace("import fs from 'node:fs';\nimport path from 'node:path';\n\n/** GET /api/v1/reels/:id/stream */", "/** GET /api/v1/reels/:id/stream */")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Patched controller imports')
