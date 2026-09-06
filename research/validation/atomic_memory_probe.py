"""Isolated executable storage-contract model; not the Kivi application.

Run with Python's standard library. Every case uses a fresh in-memory SQLite DB.
The only filesystem write is the results JSON next to this script.
Interleavings are injected sequentially; real threads/processes are not tested.
"""

from contextlib import contextmanager
from hashlib import sha256
import json
from pathlib import Path
import sqlite3
import sys


class StaleWork(Exception):
    pass


class IdempotencyConflict(Exception):
    pass


class InjectedFailure(Exception):
    pass


SCHEMA = """
CREATE TABLE users (
  user_id TEXT PRIMARY KEY, knowledge_rev INTEGER NOT NULL DEFAULT 0,
  index_rev INTEGER NOT NULL DEFAULT 0, publication_seq INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE sources (
  user_id TEXT NOT NULL, source_id TEXT NOT NULL, revision INTEGER NOT NULL,
  state TEXT NOT NULL CHECK(state IN ('held','ready','suppressed')),
  request_id TEXT NOT NULL, raw_text TEXT NOT NULL,
  PRIMARY KEY(user_id,source_id), FOREIGN KEY(user_id) REFERENCES users(user_id)
);
CREATE TABLE documents (
  row_id INTEGER PRIMARY KEY, user_id TEXT NOT NULL, source_id TEXT NOT NULL,
  source_revision INTEGER NOT NULL, projection_revision INTEGER NOT NULL,
  text TEXT NOT NULL, UNIQUE(user_id,source_id),
  FOREIGN KEY(user_id,source_id) REFERENCES sources(user_id,source_id)
);
CREATE TABLE exclusions (
  user_id TEXT NOT NULL, source_id TEXT NOT NULL, start INTEGER NOT NULL,
  end INTEGER NOT NULL CHECK(end > start),
  FOREIGN KEY(user_id,source_id) REFERENCES sources(user_id,source_id)
);
CREATE TABLE memories (
  row_id INTEGER PRIMARY KEY, user_id TEXT NOT NULL, memory_id TEXT NOT NULL,
  source_id TEXT NOT NULL, source_revision INTEGER NOT NULL,
  value TEXT NOT NULL, state TEXT NOT NULL DEFAULT 'active',
  UNIQUE(user_id,memory_id),
  FOREIGN KEY(user_id,source_id) REFERENCES sources(user_id,source_id)
);
CREATE TABLE evidence (
  user_id TEXT NOT NULL, memory_id TEXT NOT NULL, source_id TEXT NOT NULL,
  source_revision INTEGER NOT NULL, start INTEGER NOT NULL, end INTEGER NOT NULL,
  FOREIGN KEY(user_id,memory_id) REFERENCES memories(user_id,memory_id),
  FOREIGN KEY(user_id,source_id) REFERENCES sources(user_id,source_id)
);
CREATE TABLE jobs (
  user_id TEXT NOT NULL, job_key TEXT NOT NULL, payload_hash TEXT NOT NULL,
  state TEXT NOT NULL, result_id TEXT, PRIMARY KEY(user_id,job_key),
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);
CREATE TABLE vectors (
  user_id TEXT NOT NULL, source_id TEXT NOT NULL, source_revision INTEGER NOT NULL,
  projection_revision INTEGER NOT NULL, encoder TEXT NOT NULL, value BLOB NOT NULL,
  PRIMARY KEY(user_id,source_id,encoder),
  FOREIGN KEY(user_id,source_id) REFERENCES sources(user_id,source_id)
);
CREATE TABLE query_cache (
  user_id TEXT NOT NULL, query_key TEXT NOT NULL, knowledge_rev INTEGER NOT NULL,
  body TEXT NOT NULL, PRIMARY KEY(user_id,query_key),
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);
CREATE TABLE responses (
  user_id TEXT NOT NULL, request_id TEXT NOT NULL, payload_hash TEXT NOT NULL,
  source_id TEXT NOT NULL, sequence INTEGER NOT NULL, body TEXT,
  state TEXT NOT NULL, PRIMARY KEY(user_id,request_id),
  FOREIGN KEY(user_id,source_id) REFERENCES sources(user_id,source_id)
);
CREATE VIRTUAL TABLE source_fts USING fts5(text,content='documents',content_rowid='row_id');
CREATE TRIGGER documents_ai AFTER INSERT ON documents BEGIN
  INSERT INTO source_fts(rowid,text) VALUES(new.row_id,new.text);
END;
CREATE TRIGGER documents_au AFTER UPDATE ON documents BEGIN
  INSERT INTO source_fts(source_fts,rowid,text) VALUES('delete',old.row_id,old.text);
  INSERT INTO source_fts(rowid,text) VALUES(new.row_id,new.text);
END;
CREATE TRIGGER documents_ad AFTER DELETE ON documents BEGIN
  INSERT INTO source_fts(source_fts,rowid,text) VALUES('delete',old.row_id,old.text);
END;
CREATE VIRTUAL TABLE memory_fts USING fts5(value,content='memories',content_rowid='row_id');
CREATE TRIGGER memories_ai AFTER INSERT ON memories BEGIN
  INSERT INTO memory_fts(rowid,value) VALUES(new.row_id,new.value);
END;
CREATE TRIGGER memories_au AFTER UPDATE ON memories BEGIN
  INSERT INTO memory_fts(memory_fts,rowid,value) VALUES('delete',old.row_id,old.value);
  INSERT INTO memory_fts(rowid,value) VALUES(new.row_id,new.value);
END;
"""


@contextmanager
def transaction(db):
    db.execute('BEGIN IMMEDIATE')
    try:
        yield
        db.execute('COMMIT')
    except BaseException:
        db.execute('ROLLBACK')
        raise


@contextmanager
def fresh_db():
    db = sqlite3.connect(':memory:', isolation_level=None)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    db.executescript(SCHEMA)
    db.executemany('INSERT INTO users(user_id) VALUES(?)', [('alice',), ('bob',)])
    try:
        yield db
    finally:
        db.close()


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def scalar(db, sql, args=()):
    return db.execute(sql, args).fetchone()[0]


def source(db, user='alice', sid='s1'):
    return db.execute('SELECT * FROM sources WHERE user_id=? AND source_id=?', (user, sid)).fetchone()


def snapshot(db, user='alice', sid='s1'):
    row = source(db, user, sid)
    doc = db.execute('SELECT * FROM documents WHERE user_id=? AND source_id=?', (user, sid)).fetchone()
    return {
        'knowledge_rev': scalar(db, 'SELECT knowledge_rev FROM users WHERE user_id=?', (user,)),
        'source_revision': row['revision'],
        'projection_revision': doc['projection_revision'] if doc else None,
    }


def require_current(db, expected, user='alice', sid='s1'):
    if source(db, user, sid)['state'] != 'ready' or snapshot(db, user, sid) != expected:
        raise StaleWork('expected source, projection and knowledge versions no longer match')


def add_source(db, text='I like tea.', state='ready', user='alice', sid='s1', request='r1'):
    with transaction(db):
        db.execute('INSERT INTO sources VALUES(?,?,1,?,?,?)', (user, sid, state, request, text))
        if state == 'ready':
            db.execute('INSERT INTO documents(user_id,source_id,source_revision,projection_revision,text) VALUES(?,?,1,1,?)', (user, sid, text))
            db.execute('UPDATE users SET knowledge_rev=knowledge_rev+1 WHERE user_id=?', (user,))


def projected_source_text(db, user='alice', sid='s1'):
    """Apply exclusions even when no searchable document has been created yet."""
    chars = list(source(db, user, sid)['raw_text'])
    for excluded in db.execute('SELECT start,end FROM exclusions WHERE user_id=? AND source_id=?', (user, sid)):
        chars[excluded['start']:excluded['end']] = ' ' * (excluded['end'] - excluded['start'])
    return ''.join(chars)


def private_current_input(db, request, user='alice', sid='s1'):
    row = source(db, user, sid)
    if row['state'] == 'held' and row['request_id'] == request:
        return projected_source_text(db, user, sid)
    return None


def fallback(db, user='alice'):
    # All shared retrieval uses eligible projections, never raw sources.
    return [r[0] for r in db.execute('''SELECT d.text FROM documents d JOIN sources s
        ON (d.user_id=s.user_id AND d.source_id=s.source_id)
        WHERE d.user_id=? AND s.state='ready' AND d.source_revision=s.revision''', (user,))]


def lexical(db, word, user='alice'):
    return [r[0] for r in db.execute('''SELECT d.text FROM source_fts
        JOIN documents d ON d.row_id=source_fts.rowid
        JOIN sources s ON (d.user_id=s.user_id AND d.source_id=s.source_id)
        WHERE source_fts MATCH ? AND d.user_id=? AND s.state='ready'
          AND d.source_revision=s.revision''', (word, user))]


def resolve_held(db, user='alice', sid='s1', rebase_expected=None, seen_text=None):
    with transaction(db):
        row = source(db, user, sid)
        if row['state'] != 'held':
            raise ValueError('only a held input can be released')
        before = snapshot(db, user, sid)
        permitted_text = projected_source_text(db, user, sid)
        if rebase_expected is not None:
            # Caller is trusted coordinator code in this toy model, not model output.
            if before != rebase_expected or permitted_text != seen_text:
                raise StaleWork('promotion can rebase only its own unchanged, already-seen input')
        db.execute("UPDATE sources SET state='ready' WHERE user_id=? AND source_id=?", (user, sid))
        db.execute('INSERT INTO documents(user_id,source_id,source_revision,projection_revision,text) VALUES(?,?,?,1,?)', (user, sid, row['revision'], permitted_text))
        db.execute('UPDATE users SET knowledge_rev=knowledge_rev+1 WHERE user_id=?', (user,))
        return {'before': before, 'after': snapshot(db, user, sid), 'promoted_digest': digest(permitted_text)}


def admit(db, expected, key='extract:s1:1:v1', payload=None, fail=False, user='alice', sid='s1'):
    payload = payload or {'value': 'Likes tea', 'quote': 'I like tea.'}
    fingerprint = digest(payload)
    with transaction(db):
        prior = db.execute('SELECT * FROM jobs WHERE user_id=? AND job_key=?', (user, key)).fetchone()
        if prior:
            if prior['payload_hash'] != fingerprint:
                raise IdempotencyConflict('same operation key with different payload')
            return prior['result_id']
        require_current(db, expected, user, sid)
        raw = source(db, user, sid)['raw_text']
        start = raw.index(payload['quote'])
        end = start + len(payload['quote'])
        overlap = scalar(db, 'SELECT count(*) FROM exclusions WHERE user_id=? AND source_id=? AND start<? AND end>?', (user, sid, end, start))
        if overlap:
            raise StaleWork('evidence span is excluded')
        memory_id = 'm-' + key
        db.execute('INSERT INTO memories(user_id,memory_id,source_id,source_revision,value) VALUES(?,?,?,?,?)', (user, memory_id, sid, expected['source_revision'], payload['value']))
        db.execute('INSERT INTO evidence VALUES(?,?,?,?,?,?)', (user, memory_id, sid, expected['source_revision'], start, end))
        db.execute("INSERT INTO jobs VALUES(?,?,?,'succeeded',?)", (user, key, fingerprint, memory_id))
        db.execute('UPDATE users SET knowledge_rev=knowledge_rev+1 WHERE user_id=?', (user,))
        if fail:
            raise InjectedFailure('failure after memory/evidence/FTS/job writes, before commit')
        return memory_id


def forget_span(db, start, end, user='alice', sid='s1'):
    with transaction(db):
        row = source(db, user, sid)
        if not 0 <= start < end <= len(row['raw_text']):
            raise ValueError('invalid original Unicode-code-point span')
        db.execute('INSERT INTO exclusions VALUES(?,?,?,?)', (user, sid, start, end))
        db.execute('UPDATE documents SET text=?,projection_revision=projection_revision+1 WHERE user_id=? AND source_id=?', (projected_source_text(db, user, sid), user, sid))
        db.execute('''UPDATE memories SET value='',state='suppressed' WHERE user_id=? AND memory_id IN
            (SELECT memory_id FROM evidence WHERE user_id=? AND source_id=? AND start<? AND end>?)''', (user, user, sid, end, start))
        db.execute('DELETE FROM vectors WHERE user_id=? AND source_id=?', (user, sid))
        db.execute('DELETE FROM query_cache WHERE user_id=?', (user,))
        # Conservative dependency invalidation: this toy model supports one source per response.
        db.execute("UPDATE responses SET body=NULL,state='suppressed' WHERE user_id=? AND source_id=?", (user, sid))
        db.execute('UPDATE users SET knowledge_rev=knowledge_rev+1,index_rev=index_rev+1,publication_seq=publication_seq+1 WHERE user_id=?', (user,))


def save_vector(db, expected, user='alice', sid='s1'):
    with transaction(db):
        require_current(db, expected, user, sid)
        # Synthetic bytes: no model or semantic quality is exercised.
        db.execute('INSERT INTO vectors VALUES(?,?,?,?,?,?)', (user, sid, expected['source_revision'], expected['projection_revision'], 'fake-v1', b'vector'))
        db.execute('UPDATE users SET index_rev=index_rev+1 WHERE user_id=?', (user,))


def cached(db, key, user='alice'):
    row = db.execute('''SELECT q.body FROM query_cache q JOIN users u ON q.user_id=u.user_id
        WHERE q.user_id=? AND q.query_key=? AND q.knowledge_rev=u.knowledge_rev''', (user, key)).fetchone()
    return row[0] if row else None


def publish(db, expected, request='answer1', body='You like tea.', fail=False, user='alice', sid='s1'):
    fingerprint = digest({'source_id': sid, 'body': body})
    with transaction(db):
        prior = db.execute('SELECT * FROM responses WHERE user_id=? AND request_id=?', (user, request)).fetchone()
        if prior:
            if prior['payload_hash'] != fingerprint:
                raise IdempotencyConflict('request replay differs from accepted response')
            # A replay is a response lookup, not permission to restore purged content.
            return prior['body'] if prior['state'] == 'accepted' else None
        require_current(db, expected, user, sid)
        db.execute('UPDATE users SET publication_seq=publication_seq+1 WHERE user_id=?', (user,))
        sequence = scalar(db, 'SELECT publication_seq FROM users WHERE user_id=?', (user,))
        db.execute("INSERT INTO responses VALUES(?,?,?,?,?,?,'accepted')", (user, request, fingerprint, sid, sequence, body))
        if fail:
            raise InjectedFailure('failure after saved response/sequence, before commit')
        return body


def must_raise(error_type, operation):
    try:
        operation()
    except error_type:
        return
    raise AssertionError('expected ' + error_type.__name__)


def case_atomic_admission():
    with fresh_db() as db:
        add_source(db)
        original = snapshot(db)
        must_raise(InjectedFailure, lambda: admit(db, original, fail=True))
        for table in ('memories', 'evidence', 'jobs'):
            assert scalar(db, 'SELECT count(*) FROM ' + table) == 0
        assert scalar(db, "SELECT count(*) FROM memory_fts WHERE memory_fts MATCH 'tea'") == 0
        assert snapshot(db) == original
        admit(db, original)
        assert scalar(db, "SELECT count(*) FROM memory_fts WHERE memory_fts MATCH 'tea'") == 1
    return {'checks': 'memory/evidence/FTS/job/revision roll back together; successful retry commits once'}


def case_idempotency():
    with fresh_db() as db:
        add_source(db)
        original = snapshot(db)
        result = admit(db, original)
        assert admit(db, original) == result
        assert scalar(db, 'SELECT count(*) FROM memories') == 1
        must_raise(IdempotencyConflict, lambda: admit(db, original, payload={'value': 'Other', 'quote': 'I like tea.'}))
        assert scalar(db, 'SELECT count(*) FROM evidence') == 1
    return {'checks': 'same key/same payload replays; changed payload conflicts without new effects'}


def case_user_scope():
    with fresh_db() as db:
        add_source(db)
        must_raise(sqlite3.IntegrityError, lambda: db.execute("INSERT INTO memories(user_id,memory_id,source_id,source_revision,value) VALUES('bob','m1','s1',1,'wrong owner')"))
        admit(db, snapshot(db))
        assert lexical(db, 'tea', 'bob') == [] and fallback(db, 'bob') == []
        assert scalar(db, 'SELECT count(*) FROM memories WHERE user_id=?', ('bob',)) == 0
    return {'checks': 'composite ownership FK rejects cross-user source link; retrieval independently scopes by user'}


def case_stale_admission():
    observed = []
    for change in ('source_revision', 'control_generation'):
        with fresh_db() as db:
            add_source(db)
            old = snapshot(db)
            with transaction(db):
                if change == 'source_revision':
                    db.execute('UPDATE sources SET revision=revision+1')
                else:
                    db.execute('UPDATE users SET knowledge_rev=knowledge_rev+1 WHERE user_id=?', ('alice',))
            must_raise(StaleWork, lambda: admit(db, old))
            assert scalar(db, 'SELECT count(*) FROM memories') == 0
            assert scalar(db, 'SELECT count(*) FROM jobs') == 0
            observed.append(change)
    return {'rejected_before_write': observed}


def case_held_input():
    with fresh_db() as db:
        add_source(db, state='held')
        assert private_current_input(db, 'r1') == 'I like tea.'
        assert private_current_input(db, 'other-run') is None
        assert lexical(db, 'tea') == [] and fallback(db) == []
        must_raise(StaleWork, lambda: admit(db, snapshot(db)))
        naive_raw_fallback_leaks = 'tea' in source(db)['raw_text']
        assert naive_raw_fallback_leaks
        resolve_held(db)
        assert lexical(db, 'tea') == ['I like tea.']
    return {'checks': 'held input visible only to its current run; unavailable to shared retrieval/extraction until resolution', 'negative_control_raw_table_bypass_exposes_held_text': True}


def case_forget_projection():
    raw = 'I like tea. मुझे किताबें पसंद हैं. My private code is orchid.'
    with fresh_db() as db:
        add_source(db, raw)
        admit(db, snapshot(db), payload={'value': 'Code orchid', 'quote': 'My private code is orchid.'})
        assert lexical(db, 'orchid')
        forget_span(db, raw.index('My private'), len(raw))
        assert lexical(db, 'orchid') == []
        assert scalar(db, "SELECT count(*) FROM memory_fts WHERE memory_fts MATCH 'orchid'") == 0
        assert all('orchid' not in text for text in fallback(db))
        assert lexical(db, 'tea')
        assert 'orchid' in source(db)['raw_text']  # Suppression, not claimed physical erasure.
        assert len(fallback(db)[0]) == len(raw)
    return {'checks': 'excluded original span absent from source FTS, memory FTS and full-source fallback; surviving text remains searchable', 'negative_control_raw_table_bypass_resurrects_forgotten_text': True, 'offset_unit': 'Unicode code points'}


def case_stale_vector_cache():
    with fresh_db() as db:
        add_source(db)
        old = snapshot(db)
        old_mirror = {'snapshot': old, 'text': source(db)['raw_text']}
        forget_span(db, 0, len('I like tea.'))
        must_raise(StaleWork, lambda: save_vector(db, old))
        # Inject an obsolete cache row, emulating a cache writer that skipped fencing.
        db.execute('INSERT INTO query_cache VALUES(?,?,?,?)', ('alice', 'q1', old['knowledge_rev'], 'I like tea.'))
        assert cached(db, 'q1') is None
        assert old_mirror['snapshot'] != snapshot(db)
        assert scalar(db, 'SELECT count(*) FROM vectors') == 0
    return {'checks': 'late vector commit rejected; obsolete cache and RAM mirror fail revision eligibility despite retained bytes'}


def case_stale_publication():
    with fresh_db() as db:
        add_source(db)
        old = snapshot(db)
        forget_span(db, 0, len('I like tea.'))
        sequence = scalar(db, "SELECT publication_seq FROM users WHERE user_id='alice'")
        must_raise(StaleWork, lambda: publish(db, old))
        assert scalar(db, 'SELECT count(*) FROM responses') == 0
        assert scalar(db, "SELECT publication_seq FROM users WHERE user_id='alice'") == sequence
        # Negative control in a savepoint: unchecked persistence admits obsolete body.
        db.execute('SAVEPOINT naive')
        db.execute("INSERT INTO responses VALUES('alice','naive','hash','s1',99,'You like tea.','accepted')")
        assert scalar(db, "SELECT body FROM responses WHERE request_id='naive'") == 'You like tea.'
        db.execute('ROLLBACK TO naive')
        db.execute('RELEASE naive')
    return {'checks': 'stale generation rejected before response/sequence writes', 'negative_control_unchecked_publication_writes_stale_response': True}


def case_response_replay():
    with fresh_db() as db:
        add_source(db)
        old = snapshot(db)
        assert publish(db, old) == 'You like tea.'
        assert publish(db, old) == 'You like tea.'
        assert scalar(db, 'SELECT count(*) FROM responses') == 1
        must_raise(IdempotencyConflict, lambda: publish(db, old, body='Different response'))
        forget_span(db, 0, len('I like tea.'))
        assert publish(db, old) is None
        assert scalar(db, "SELECT body FROM responses WHERE request_id='answer1'") is None
        assert scalar(db, 'SELECT count(*) FROM responses') == 1
    return {'checks': 'idempotent reply replays once; different payload conflicts; replay after forget respects purged body'}


def case_readiness_and_publication_atomicity():
    with fresh_db() as db:
        add_source(db)
        old = snapshot(db)
        assert scalar(db, 'SELECT count(*) FROM vectors') == 0 and lexical(db, 'tea')
        assert fallback(db) == ['I like tea.']
        must_raise(InjectedFailure, lambda: publish(db, old, fail=True))
        assert scalar(db, 'SELECT count(*) FROM responses') == 0
        assert scalar(db, "SELECT publication_seq FROM users WHERE user_id='alice'") == 0
        save_vector(db, old)
        assert scalar(db, 'SELECT count(*) FROM vectors') == 1
        assert scalar(db, "SELECT index_rev FROM users WHERE user_id='alice'") == 1
    return {'checks': 'lexical/fallback work while dense coverage is pending; publication body/sequence roll back together; vector readiness changes atomically'}


def case_forget_before_held_release():
    raw = 'I like tea. Do not remember the nickname orchid.'
    with fresh_db() as db:
        add_source(db, raw, state='held')
        start = raw.index('orchid')
        assert scalar(db, 'SELECT count(*) FROM documents') == 0
        forget_span(db, start, start + len('orchid'))
        private_after_control = private_current_input(db, 'r1')
        resolve_held(db)
        leaks = []
        if 'orchid' in (private_after_control or ''):
            leaks.append('private_current_input')
        if lexical(db, 'orchid'):
            leaks.append('source_fts')
        if any('orchid' in text for text in fallback(db)):
            leaks.append('full_source_fallback')
        assert not leaks, 'excluded span reappeared through ' + ', '.join(leaks)
        assert lexical(db, 'tea')
        assert 'orchid' in source(db)['raw_text']
    return {'checks': 'forget while current source is held survives private re-read and later publication to source FTS/fallback; allowed text remains searchable'}


def case_own_promotion_rebase():
    with fresh_db() as db:
        add_source(db, state='held')
        captured = snapshot(db)
        seen = private_current_input(db, 'r1')
        receipt = resolve_held(db, rebase_expected=captured, seen_text=seen)
        assert receipt['before'] == captured
        assert receipt['after']['knowledge_rev'] == captured['knowledge_rev'] + 1
        assert receipt['promoted_digest'] == digest(seen)
        assert publish(db, receipt['after']) == 'You like tea.'

    with fresh_db() as db:
        add_source(db, state='held')
        captured = snapshot(db)
        seen = private_current_input(db, 'r1')
        add_source(db, 'I prefer trains.', sid='unrelated', request='r2')
        must_raise(StaleWork, lambda: resolve_held(db, rebase_expected=captured, seen_text=seen))
        assert source(db)['state'] == 'held'
        assert scalar(db, "SELECT count(*) FROM documents WHERE source_id='s1'") == 0

    with fresh_db() as db:
        add_source(db, state='held')
        captured = snapshot(db)
        receipt = resolve_held(db, rebase_expected=captured, seen_text=private_current_input(db, 'r1'))
        add_source(db, 'I prefer trains.', sid='unrelated', request='r2')
        must_raise(StaleWork, lambda: publish(db, receipt['after']))
        assert scalar(db, 'SELECT count(*) FROM responses') == 0

    with fresh_db() as db:
        add_source(db, state='held')
        original_seen = private_current_input(db, 'r1')
        forget_span(db, 0, len(original_seen))
        # Even a fresh counter cannot bless a previously seen, now-excluded body.
        fresh_counter = snapshot(db)
        must_raise(StaleWork, lambda: resolve_held(db, rebase_expected=fresh_counter, seen_text=original_seen))
        assert source(db)['state'] == 'held'
    return {'checks': 'sole unchanged current-input promotion rebases through a code-issued receipt; unrelated changes before or after promotion and changed projections reject', 'scope': 'trusted in-process coordinator; sequential interleavings; no model authority or real concurrency tested'}


CASES = [
    ('atomic_admission_rollback', case_atomic_admission),
    ('operation_idempotency', case_idempotency),
    ('cross_user_scope', case_user_scope),
    ('stale_extraction_fencing', case_stale_admission),
    ('held_input_visibility', case_held_input),
    ('forgotten_span_projection', case_forget_projection),
    ('stale_vector_cache_and_mirror', case_stale_vector_cache),
    ('stale_publication_rejection', case_stale_publication),
    ('response_replay_after_forget', case_response_replay),
    ('partial_index_and_atomic_publication', case_readiness_and_publication_atomicity),
    ('forget_before_held_source_release', case_forget_before_held_release),
    ('own_source_promotion_rebase', case_own_promotion_rebase),
]


def main():
    results = []
    for name, case in CASES:
        try:
            results.append({'case': name, 'status': 'passed', **case()})
        except Exception as exc:
            results.append({'case': name, 'status': 'failed', 'error': type(exc).__name__ + ': ' + str(exc)})
    passed = sum(r['status'] == 'passed' for r in results)
    report = {
        'experiment': 'Isolated proposed storage contracts; not product implementation or benchmark',
        'python_version': sys.version.split()[0], 'sqlite_version': sqlite3.sqlite_version,
        'database_mode': 'fresh in-memory databases; foreign_keys=ON; actual FTS5 external-content triggers',
        'passed': passed, 'total': len(results), 'cases': results,
        'limits': [
            'No LLM extraction, entailment, natural-language control detection or answer quality tested.',
            'No actual threads/processes, disk crash, WAL, network delivery, MCP or provider retries tested.',
            'Sequential injected interleavings model stale work; they do not prove concurrent correctness.',
            'One-source response dependency model and conservative response invalidation only.',
            'Synthetic vector bytes; no semantic retrieval, embedding computation or performance measurement.',
            'No physical erasure, backups, provider retention, arbitrary paraphrase forgetting or alias/graph cleanup tested.',
            'The proposed Kivi product is not implemented by this script and may differ from this executable model.',
        ],
    }
    output = Path(__file__).resolve().with_name('atomic_memory_results.json')
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8',newline='\n')
    print(json.dumps({'passed': passed, 'total': len(results), 'python': report['python_version'], 'sqlite': report['sqlite_version'], 'results_file': str(output)}, ensure_ascii=False))
    for result in results:
        if result['status'] == 'failed':
            print(json.dumps(result))
    return 0 if passed == len(results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
