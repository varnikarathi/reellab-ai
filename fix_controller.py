import sys

file_path = sys.argv[1]

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the getReelStream function that got corrupted by PowerShell variable expansion
# We will just replace the entire getReelStream function

start_idx = content.find("/** `GET /api/v1/reels/:id/stream` */")

if start_idx != -1:
    content = content[:start_idx]

get_reel_stream = """/** `GET /api/v1/reels/:id/stream` */
export async function getReelStream(req: Request, res: Response): Promise<void> {
  const reel = await getReel(req.params.id);
  
  const videoPath = path.resolve(reel.storagePath);
  
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
      res.status(416).header('Content-Range', `bytes */${fileSize}`).send();
      return;
    }

    const chunksize = end - start + 1;
    const file = fs.createReadStream(videoPath, { start, end });
    const head = {
      'Content-Range': `bytes ${start}-${end}/${fileSize}`,
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
"""

content += get_reel_stream

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Fixed {file_path}')
