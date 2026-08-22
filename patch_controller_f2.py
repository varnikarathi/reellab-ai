import sys
import re

file_path = sys.argv[1]

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix getReelById
content = re.sub(
    r"const reel = await Reel\.findOne\(\{ reelId: req\.params\.id \}\);\s*if \(!reel\) \{\s*throw ApiError\.notFound\('Reel', req\.params\.id\);\s*\}",
    "const reel = await getReel(req.params.id);",
    content
)

# Ensure getReel is imported
if "getReel" not in content[:content.find("export ")]:
    content = content.replace("import { analyzeReel, registerUpload } from '../services/reelService';",
                              "import { analyzeReel, registerUpload, getReel } from '../services/reelService';")

# Add getReelStream for Feature 2
get_reel_stream = '''
import fs from 'node:fs';
import path from 'node:path';

/** GET /api/v1/reels/:id/stream */
export async function getReelStream(req: Request, res: Response): Promise<void> {
  const reel = await getReel(req.params.id);
  
  const videoPath = path.resolve(reel.storagePath);
  
  // Security check: ensure path is within uploads directory
  const uploadDir = path.resolve(process.cwd(), 'uploads');
  if (!videoPath.startsWith(uploadDir)) {
      throw new ApiError('FORBIDDEN', 'Invalid file path');
  }

  if (!fs.existsSync(videoPath)) {
    throw ApiError.notFound('VideoFile', reel.id);
  }

  const stat = fs.statSync(videoPath);
  const fileSize = stat.size;
  const range = req.headers.range;

  if (range) {
    const parts = range.replace(/bytes=/, '').split('-');
    const start = parseInt(parts[0], 10);
    const end = parts[1] ? parseInt(parts[1], 10) : fileSize - 1;

    if (start >= fileSize || end >= fileSize) {
      res.status(416).header('Content-Range', ytes */).send();
      return;
    }

    const chunksize = end - start + 1;
    const file = fs.createReadStream(videoPath, { start, end });
    const head = {
      'Content-Range': ytes -/,
      'Accept-Ranges': 'bytes',
      'Content-Length': chunksize,
      'Content-Type': 'video/mp4',
    };

    res.writeHead(206, head);
    file.pipe(res);
  } else {
    const head = {
      'Content-Length': fileSize,
      'Content-Type': 'video/mp4',
    };
    res.writeHead(200, head);
    fs.createReadStream(videoPath).pipe(res);
  }
}
'''

content += get_reel_stream

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Patched {file_path}')
