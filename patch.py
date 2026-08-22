import sys
import re

file_path = sys.argv[1]

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# For reelService.ts
if 'reelService.ts' in file_path:
    # Add imports
    imports_to_add = "import { isDbConnected } from '../config/db';\nimport { Reel as ReelModel } from '../models/Reel';\n\n"
    content = imports_to_add + content
    
    # Replace getReel function
    old_get_reel = '''export function getReel(reelId: string): Reel {
  const reel = memoryStore.get<Reel>(COLLECTIONS.reels, reelId);
  if (!reel) throw ApiError.notFound('Reel', reelId);
  return reel;
}'''
    new_get_reel = '''export async function getReel(reelId: string): Promise<Reel> {
  if (isDbConnected()) {
    const doc = await ReelModel.findOne({ reelId });
    if (doc) {
      return {
        id: doc.reelId,
        filename: doc.filename,
        storagePath: doc.storagePath,
        sizeBytes: doc.sizeBytes,
        durationSeconds: doc.durationSeconds,
        uploadedAt: doc.createdAt ? doc.createdAt.toISOString() : new Date().toISOString(),
        status: doc.status as Reel['status'],
      };
    }
  }

  const reel = memoryStore.get<Reel>(COLLECTIONS.reels, reelId);
  if (!reel) throw ApiError.notFound('Reel', reelId);
  return reel;
}'''
    content = content.replace(old_get_reel, new_get_reel)
    
    # Also need to update analyzeReel to await getReel
    content = content.replace('reel = getReel(input.reelId);', 'reel = await getReel(input.reelId);')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Patched {file_path}')
