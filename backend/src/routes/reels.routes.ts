import { Router } from 'express';

import { postAnalyzeReel, postUploadReel, getReelById } from '../controllers/reelsController';
import { uploadReel } from '../middleware/upload';
import { asyncHandler } from '../utils/asyncHandler';

const router = Router();

router.post('/upload', uploadReel, asyncHandler(postUploadReel));
router.post('/analyze', asyncHandler(postAnalyzeReel));

router.get('/:id', asyncHandler(getReelById));

export default router;
