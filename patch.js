const fs = require('fs');
const controllerPath = 'backend/src/controllers/reelsController.ts';
let controller = fs.readFileSync(controllerPath, 'utf8');

if (!controller.includes('getReelById')) {
  controller = controller.replace(`import { ApiError } from '../utils/ApiError';`, `import { ApiError } from '../utils/ApiError';\nimport { Reel } from '../models/Reel';`);
  controller += `\n\n/** \`GET /api/v1/reels/:id\` */\nexport async function getReelById(req: Request, res: Response): Promise<void> {\n  const reel = await Reel.findOne({ reelId: req.params.id });\n  if (!reel) {\n    throw ApiError.notFound('Reel', req.params.id);\n  }\n  sendData(req, res, { data: reel, mock: false }, 200);\n}\n`;
  fs.writeFileSync(controllerPath, controller);
}

const routesPath = 'backend/src/routes/reels.routes.ts';
let routes = fs.readFileSync(routesPath, 'utf8');
if (!routes.includes('getReelById')) {
  routes = routes.replace(`import { postAnalyzeReel, postUploadReel } from '../controllers/reelsController';`, `import { postAnalyzeReel, postUploadReel, getReelById } from '../controllers/reelsController';`);
  routes = routes.replace(`export default router;`, `router.get('/:id', asyncHandler(getReelById));\n\nexport default router;`);
  fs.writeFileSync(routesPath, routes);
}
console.log('GET feature added');
