import sys

file_path = sys.argv[1]

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update import
content = content.replace("import { analyzeReel, registerUpload } from '../services/reelService';",
                          "import { analyzeReel, registerUpload, getReel } from '../services/reelService';")

# Update getReelById
old_get_reel_by_id = '''/** GET /api/v1/reels/:id */
export async function getReelById(req: Request, res: Response): Promise<void> {
  const reel = await Reel.findOne({ reelId: req.params.id });
  if (!reel) {
    throw ApiError.notFound('Reel', req.params.id);
  }
  sendData(req, res, { data: reel, mock: false }, 200);
}'''

new_get_reel_by_id = '''/** GET /api/v1/reels/:id */
export async function getReelById(req: Request, res: Response): Promise<void> {
  const reel = await getReel(req.params.id);
  sendData(req, res, { data: reel, mock: false }, 200);
}'''

content = content.replace(old_get_reel_by_id, new_get_reel_by_id)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Patched {file_path}')
