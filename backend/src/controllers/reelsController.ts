import type { Request, Response } from 'express';
import fs from 'node:fs';
import path from 'node:path';

import { analyzeReel, registerUpload, getReel } from '../services/reelService';
import { ApiError } from '../utils/ApiError';
import { sendData } from '../utils/respond';

/** `POST /api/v1/reels/upload` */
export async function postUploadReel(req: Request, res: Response): Promise<void> {
  if (!req.file) {
    throw new ApiError('UPLOAD_FAILED', "No file received. Send a multipart field named 'reel'.");
  }

  const reel = registerUpload(req.file);
  sendData(req, res, { data: reel, mock: false }, 201);
}

/** `POST /api/v1/reels/analyze` */
export async function postAnalyzeReel(req: Request, res: Response): Promise<void> {
  const body = (req.body ?? {}) as { reelId?: string; videoPath?: string };
  const resolved = await analyzeReel(body, req.requestId);
  sendData(req, res, resolved, 200);
}

/** `GET /api/v1/reels/:id` */
export async function getReelById(req: Request, res: Response): Promise<void> {
  const reelId = req.params.id as string;
  const reel = await getReel(reelId);
  sendData(req, res, { data: reel, mock: false }, 200);
}

/** `GET /api/v1/reels/:id/stream` */
export async function getReelStream(req: Request, res: Response): Promise<void> {
  const reelId = req.params.id as string;
  const reel = await getReel(reelId);
  
  const videoPath = path.resolve(reel.storagePath);
  
  const uploadDir = path.resolve(process.cwd(), 'uploads');
  if (!videoPath.startsWith(uploadDir)) {
      throw ApiError.validation('Invalid file path');
  }

  if (!fs.existsSync(videoPath)) {
    throw ApiError.notFound('VideoFile', reel.id);
  }

  const stat = fs.statSync(videoPath);
  const fileSize = stat.size;
  const range = req.headers.range as string | undefined;

  if (range) {
    const parts = range.replace(/bytes=/, '').split('-');
    const start = parseInt(parts[0] || '0', 10);
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
