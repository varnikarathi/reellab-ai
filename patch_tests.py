import sys

file_path = sys.argv[1]

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

streaming_tests = '''
  describe('GET /api/v1/reels/:id/stream', () => {
    it('returns 404 for missing reel', async () => {
      const res = await request(app).get('/api/v1/reels/nonexistent/stream');
      expect(res.status).toBe(404);
    });
  });
'''

if "describe('GET /api/v1/reels/:id/stream'" not in content:
    # Just append basic tests at the end inside the main describe block if possible, 
    # but since it's hard to parse without AST, let's just use regex to insert before the last '});'
    last_brace_idx = content.rfind('});')
    if last_brace_idx != -1:
        content = content[:last_brace_idx] + streaming_tests + content[last_brace_idx:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        print("Added streaming tests")
