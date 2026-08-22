import sys

file_path = sys.argv[1]

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("import { postAnalyzeReel, postUploadReel, getReelById } from '../controllers/reelsController';",
                          "import { postAnalyzeReel, postUploadReel, getReelById, getReelStream } from '../controllers/reelsController';")

content = content.replace("router.get('/:id', asyncHandler(getReelById));",
                          "router.get('/:id', asyncHandler(getReelById));\nrouter.get('/:id/stream', asyncHandler(getReelStream));")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Patched routes')
