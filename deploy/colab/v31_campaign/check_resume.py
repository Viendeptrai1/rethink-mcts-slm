"""Before resuming from a partial archive: list completed problems whose selected.py would trip the
frozen code's resume check (read_text() turns CRLF into LF, so the hash no longer matches).
usage: python3 check_resume.py <partial.tar.gz>  -> prints run/problem ids to drop, one per line."""
import io, json, sys, tarfile
sys.path.insert(0, '/Users/kotori/Documents/TLCN/src')
from rethink_mcts.domain.candidate import ProgramCandidate as P

tf = tarfile.open(sys.argv[1])
files = {m.name: m for m in tf.getmembers() if m.isfile()}
for name, m in files.items():
    if not name.endswith('/completed.json'):
        continue
    rec = json.load(tf.extractfile(m))
    sel = name.rsplit('/', 1)[0] + '/selected.py'
    if not rec.get('code_hash') or sel not in files:
        continue
    text = io.TextIOWrapper(tf.extractfile(files[sel]), encoding='utf-8').read()  # universal newlines, like read_text()
    if P.compute_hash(text) != rec['code_hash']:
        print(name.rsplit('/', 1)[0])
