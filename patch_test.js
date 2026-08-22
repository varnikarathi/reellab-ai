const fs = require('fs');
const testPath = 'backend/tests/routes.test.ts';
let tests = fs.readFileSync(testPath, 'utf8');

if (!tests.includes('import { Reel }')) {
  tests = tests.replace(`import request from 'supertest';`, `import request from 'supertest';\nimport { Reel } from '../src/models/Reel';`);
}

if (!tests.includes('jest.spyOn(Reel, \'findOne\')')) {
  tests = tests.replace(`it('retrieves a reel by id', async () => {`, `it('retrieves a reel by id', async () => {\n    jest.spyOn(Reel, 'findOne').mockResolvedValueOnce(null);`);
  fs.writeFileSync(testPath, tests);
}
console.log('GET test patched with mock');
