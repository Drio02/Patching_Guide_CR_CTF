# Patcher's Guide & CheatSheet — Attack/Defense CTF

> Quick reference for patching vulnerable services during an Attack/Defense game.
> Per-vulnerability deep dives and `vulnerable` / `parche` sample pairs live in [`vulns/`](vulns/).
> This guide is the "one page you keep open during the game".

**Contents**

1. [The patching loop (A/D workflow)](#1-the-patching-loop-ad-workflow)
2. [Triage: what to patch first](#2-triage-what-to-patch-first)
3. [Lessons from a real scan (opengrep, 5 services)](#3-lessons-from-a-real-scan-opengrep-5-services)
4. [SQL Injection](#4-sql-injection)
5. [NoSQL Injection](#5-nosql-injection)
6. [Path Traversal / LFI](#6-path-traversal--lfi)
7. [Command Injection](#7-command-injection)
8. [SSTI (Server-Side Template Injection)](#8-ssti-server-side-template-injection)
9. [Insecure Deserialization](#9-insecure-deserialization)
10. [IDOR & Missing Authentication](#10-idor--missing-authentication)
11. [Sessions, Secrets & JWT](#11-sessions-secrets--jwt)
12. [Weak Randomness](#12-weak-randomness)
13. [Crypto bugs (signatures, MACs, hashes)](#13-crypto-bugs-signatures-macs-hashes)
14. [XSS](#14-xss)
15. [SSRF](#15-ssrf)
16. [XXE](#16-xxe)
17. [C / memory-safety bugs](#17-c--memory-safety-bugs)
18. [PHP-specific traps](#18-php-specific-traps)
19. [Container / infra quick fixes](#19-container--infra-quick-fixes)
20. [CheatSheet: grep → fix](#20-cheatsheet-grep--fix)
21. [Patching pitfalls (how teams lose SLA)](#21-patching-pitfalls-how-teams-lose-sla)

---

## 1. The patching loop (A/D workflow)

Every tick you are scored on **attack + defense + SLA**. An exploit that is "fixed" by breaking the
checker costs more than the flag you saved. The loop:

1. **Snapshot first.** `git init && git add -A && git commit -m baseline` (or `cp -a service service.bak`)
   *before* touching anything. You need a one-command rollback.
2. **Find.** Scan (opengrep/semgrep, `grep` patterns from [section 20](#20-cheatsheet-grep--fix)),
   read the routes and handlers, and **watch incoming traffic** (tcpdump/Tulip/packmate): other teams' exploits
   show you the vulns you missed.
3. **Patch minimally.** Change the smallest thing that kills the bug. Don't refactor, don't change the
   storage format, response format, ports, or status codes the checker relies on.
4. **Rebuild & restart.** `docker compose up -d --build <svc>` and confirm the container is healthy
   (`docker compose ps`, `docker compose logs -f <svc>`).
5. **Verify both sides.**
   - Run the exploit against yourself → it must fail.
   - Run the normal feature (register, login, store, retrieve) → it must still work.
6. **Commit the patch** with a message naming the vuln, so you can revert one patch without losing the others.
7. **Monitor.** Watch the scoreboard SLA status for the next ticks. A drop to "mumble"/"down" right after
   a deploy means rollback first, debug later.

> **Rule of thumb:** patch the *sink* (query, file open, exec, deserialize) instead of filtering the input
> with a blacklist. Blacklists are what the other teams' second exploit bypasses.

---

## 2. Triage: what to patch first

Sort by **impact on flags**, not by CVSS:

| Priority | Impact class | Typical bugs | Why first |
|---|---|---|---|
| 1 | `rce` | command injection, deserialization, SSTI, memory corruption | Takes all flags, may persist, can wipe your service |
| 2 | `flag-leak` | SQLi, path traversal, IDOR, unauthenticated "admin/backdoor/export" route | Direct flag read, usually scripted by every team in minutes |
| 3 | `auth-bypass` | hardcoded session secret, forgeable JWT, weak RNG tokens, broken signature verify | Log in as the flag-holding user |
| 4 | `session-theft` | XSS (only if there is a bot/admin that visits pages) | Needs a victim; often not exploitable in A/D |
| 5 | `integrity` / `dos` | chmod 777, DoS, remote `ADD` in Dockerfile | Rarely costs flags; fix after the game-critical ones |

Also triage **false positives** fast. A scanner flag on `Math.random()` in a frontend animation is noise,
while the same call generating a session token is critical. Look at *what the value is used for*.

---

## 3. Lessons from a real scan (opengrep, 5 services)

Results of an opengrep scan of five A/D services (`bambinotes`, `fastvuln`, `fireworx`, `stldoctor`,
`stonksexchange`), with the patch for each true positive. These are the patterns to expect in the game.

| Service | Lang | Finding (rule) | Location | Impact | Patch | See |
|---|---|---|---|---|---|---|
| fastvuln | Python (FastAPI) | Sensitive route without auth (`/backdoor?username=`) | `main.py:161` | flag-leak | Delete the route, or add an auth dependency + owner check | [§10](#10-idor--missing-authentication) |
| fireworx | Python (aiohttp) | IDOR: only checks `"username" in session`, then shows the private key of *any* user | `src/app.py:385` | flag-leak | Compare the session user with the requested user | [§10](#10-idor--missing-authentication) |
| fireworx | Python | Signature oracle: error response leaks the expected signature | `src/app.py:349` | auth-bypass | Return a generic error; never echo the computed value | [§13](#13-crypto-bugs-signatures-macs-hashes) |
| fireworx | Python | DSA static nonce `k = H(self.y)` | `src/crypto.py:59` | auth-bypass (key recovery) | Random `k` per signature (`secrets`) or RFC 6979 | [§13](#13-crypto-bugs-signatures-macs-hashes) |
| fireworx | Python | DSA verify without `0 < r,s < q` range check | `src/crypto.py:85` | auth-bypass (any sig verifies) | Reject out-of-range `r`, `s` before inverting | [§13](#13-crypto-bugs-signatures-macs-hashes) |
| fireworx | Python | `random` for private key / nonces / PoW prefix | `src/crypto.py:51,92`, `src/app.py:249` | auth-bypass | `secrets.randbelow`, `secrets.token_bytes` | [§12](#12-weak-randomness) |
| fireworx | JS (frontend) | `innerHTML = xhr.responseText` | `src/static/content.js:52,102,135` | session-theft | `textContent` | [§14](#14-xss) |
| fireworx | JS (frontend) | `Math.random()` | `src/static/firework.js:26` | — | **False positive**: animation only | [§12](#12-weak-randomness) |
| fireworx | Python | MD5 | `src/app.py:423` | — | Likely **false positive** if it is a proof-of-work check; only fix if used for passwords/MACs | [§13](#13-crypto-bugs-signatures-macs-hashes) |
| fireworx | Docker | `chmod 777 data .venv` | `Dockerfile:18` | integrity | `chown` to the app user, `750` | [§19](#19-container--infra-quick-fixes) |
| stldoctor | C | `sprintf("%02x", signed char)` → sign extension writes 8 chars, overflow into globals (e.g. `loggedin`) | `src/util.c:59` | rce / auth-bypass | Cast to `(unsigned char)`, use `snprintf` with remaining size | [§17](#17-c--memory-safety-bugs) |
| stldoctor | C | `strncmp(prefix, str, strlen(prefix))` → empty input matches | `src/util.c:139` | auth-bypass | Compare full lengths, then constant-time compare | [§17](#17-c--memory-safety-bugs) |
| stldoctor | C | `char c = fgetc(f)` compared to `EOF` → byte `0xff` ends the string early | `src/util.c:82` | auth-bypass | `int c` | [§17](#17-c--memory-safety-bugs) |
| stldoctor | C | `srand(time(NULL))` / `rand()` for IDs | `src/main.c:202`, `src/util.c:57` | auth-bypass | `getrandom()` (but check whether the output must be reproducible, see §12) | [§12](#12-weak-randomness) |
| stldoctor | C | `malloc(n * size)` / `realloc` without overflow check | `src/stlfile.c:21,30`, `cleaner/main.c:112,125` | rce (low confidence) | `calloc` / `reallocarray` | [§17](#17-c--memory-safety-bugs) |
| stonksexchange | JS (Express) | Hardcoded `express-session` secret `'keyboard cat'` | `app.js:23` | auth-bypass | Random secret from env/file | [§11](#11-sessions-secrets--jwt) |
| stonksexchange | JS (Express + Mongo) | NoSQLi: `findOne({username: req.body.username})` | `routes/index.js:63,85` | auth-bypass | `String()` cast / type check | [§5](#5-nosql-injection) |
| bambinotes | binary only | No source: needs reversing | — | — | Binary patching (out of scope here) | — |

**Takeaways**

- Every service shipped with **at least one auth-bypass**. Hardcoded secrets and missing owner checks are
  the cheapest flags in the game: patch them in the first minutes.
- Custom crypto (fireworx) hides **several independent bugs in one file**. Patch all of them; teams will
  switch exploits as soon as one is closed.
- C services (stldoctor) hide auth bypasses in **memory bugs next to an auth flag**. Look at which globals
  sit right after a buffer.
- Scanner noise is real (frontend `Math.random`, PoW MD5, Dockerfile `ADD`). Triage by *use*, not by rule.

---

## 4. SQL Injection

**Fix:** parameterized queries / prepared statements. Never build SQL with `+`, f-strings,
`.format()`, `%`, template literals, or `sprintf`.

```python
# Python — sqlite3 (placeholder ?), psycopg / mysqlclient / pymysql (placeholder %s)
cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pw))
cur.execute("SELECT * FROM users WHERE username = %s", (user,))      # NOT  "... = '%s'" % user
# SQLAlchemy
db.session.execute(text("SELECT * FROM notes WHERE id = :id"), {"id": note_id})
```

```php
// PHP — PDO
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->execute([$user, $pw]);
// PHP — mysqli
$stmt = $mysqli->prepare("SELECT * FROM users WHERE username = ?");
$stmt->bind_param("s", $user);
$stmt->execute();
```

```js
// Node — mysql2 / sqlite3: ?    pg: $1, $2
const [rows] = await conn.execute("SELECT * FROM users WHERE username = ?", [user]);
db.get("SELECT * FROM users WHERE username = ?", [user], cb);
await pool.query("SELECT * FROM users WHERE username = $1", [user]);
```

```java
// Java — JDBC
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE username = ?");
ps.setString(1, user);
ResultSet rs = ps.executeQuery();
```

```go
// Go — database/sql (MySQL/SQLite: ?, Postgres: $1)
row := db.QueryRow("SELECT id FROM users WHERE username = ?", user)
// NOT fmt.Sprintf("... WHERE username = '%s'", user)
```

```csharp
// C# — ADO.NET
var cmd = new SqlCommand("SELECT * FROM users WHERE username = @u", conn);
cmd.Parameters.AddWithValue("@u", user);
```

```ruby
# Ruby — ActiveRecord / Sequel
User.where(username: user)                 # hash form
User.where("username = ?", user)           # NOT "username = '#{user}'"
DB["SELECT * FROM users WHERE username = ?", user]
```

```c
// C — sqlite3
sqlite3_stmt *st;
sqlite3_prepare_v2(db, "SELECT * FROM users WHERE username = ?", -1, &st, NULL);
sqlite3_bind_text(st, 1, user, -1, SQLITE_TRANSIENT);
while (sqlite3_step(st) == SQLITE_ROW) { /* ... */ }
sqlite3_finalize(st);
```

**Things placeholders can't protect:**

| Case | Fix |
|---|---|
| Table / column names, `ORDER BY`, `ASC/DESC` | Allowlist: `col = {"name","date"}.get(x, "date")`, `dir = "DESC" if x == "desc" else "ASC"` |
| `LIMIT` / `OFFSET` | Cast to `int` |
| `LIKE` patterns | Bind the value, escape `%` and `_` if wildcards must not be user-controlled |
| `IN (...)` lists | Generate `?,?,?` with the right count and bind each value |

**Quick emergency fix** when the query is too tangled to rewrite: cast numeric IDs (`int(x)`) or reject
anything outside `^[A-Za-z0-9_]{1,64}$` *at the sink*. It's a stop-gap: replace with placeholders when you have time.

---

## 5. NoSQL Injection

Express (`qs`) and JSON bodies turn `password[$ne]=x` into `{password: {$ne: "x"}}`.

```js
// Node / Mongo — force strings
const username = String(req.body.username);
const password = String(req.body.password);
const user = await db.collection("users").findOne({ username });
// or reject non-strings
if (typeof req.body.username !== "string") return res.status(400).end();
// or globally (package already in the image? don't add deps mid-game unless you have to)
app.use(require("express-mongo-sanitize")());
```

```python
# Python / pymongo — same idea
username = request.json.get("username")
if not isinstance(username, str):
    abort(400)
users.find_one({"username": username})
```

```php
// PHP / MongoDB — ?user[$ne]=x arrives as an array
if (!is_string($_POST['user'])) { http_response_code(400); exit; }
```

Also kill `$where`, `$function`, and `mapReduce` with user input (server-side JavaScript → RCE/DoS).

---

## 6. Path Traversal / LFI

**Fix:** resolve the canonical path and check it is *inside* the base directory, or accept only a plain
filename (no separators) from an allowlist. Decode first, check last.

```python
# Python
from pathlib import Path
BASE = Path("/srv/files").resolve()
target = (BASE / name).resolve()                 # resolves .. and symlinks
if not target.is_relative_to(BASE):              # Python 3.9+
    abort(403)
# Flask: prefer send_from_directory(BASE, name), which uses safe_join internally
```

```js
// Node
const BASE = path.resolve("/srv/files");
const target = path.resolve(BASE, req.query.name);
if (!target.startsWith(BASE + path.sep)) return res.sendStatus(403);
// symlinks: use fs.realpathSync(target) before the check if the file exists
// Express: res.sendFile(name, { root: BASE }) rejects ".." for you
```

```php
// PHP 8
$base = realpath('/var/www/uploads');
$real = realpath($base . '/' . $_GET['file']);
if ($real === false || !str_starts_with($real, $base . DIRECTORY_SEPARATOR)) {
    http_response_code(403); exit;
}
// LFI: never include/require user input. Use a map: $pages = ['home' => 'home.php']; include $pages[$p] ?? 'home.php';
```

```java
// Java
Path base = Paths.get("/srv/files").toRealPath();
Path target = base.resolve(name).normalize();
if (!target.startsWith(base)) throw new SecurityException("traversal");   // Path.startsWith is per-component
```

```go
// Go
if !filepath.IsLocal(name) {                     // Go 1.20+: rejects "..", absolute paths, empty names
    http.Error(w, "forbidden", http.StatusForbidden); return
}
f, err := os.Open(filepath.Join(baseDir, name))
// Go 1.24+: root, _ := os.OpenRoot(baseDir); f, err := root.Open(name)  // also blocks symlink escapes
```

```csharp
// C#
var baseDir = Path.GetFullPath("/srv/files") + Path.DirectorySeparatorChar;
var full = Path.GetFullPath(Path.Combine(baseDir, name));   // Combine returns `name` if it is absolute
if (!full.StartsWith(baseDir, StringComparison.Ordinal)) return Forbid();
```

```ruby
# Ruby
base = File.expand_path("/srv/files")
full = File.expand_path(name, base)
halt 403 unless full.start_with?(base + File::SEPARATOR)
```

```c
// C
char path[PATH_MAX], real[PATH_MAX];
if (snprintf(path, sizeof path, "%s/%s", BASE, name) >= (int)sizeof path) return deny();
if (!realpath(path, real) || strncmp(real, BASE "/", strlen(BASE "/")) != 0) return deny();
// simplest for note/file stores: allow only [A-Za-z0-9_-] in `name`
```

**Common broken fixes:** `name.replace("../", "")` (`....//` survives), `startsWith(base)` without the
trailing separator (`/srv/files_evil`), checking *before* URL-decoding, and `os.path.join(base, "/etc/passwd")`
(an absolute 2nd arg discards `base` in Python, Node `path.join` doesn't, `path.resolve` does).

---

## 7. Command Injection

**Fix:** don't use a shell. Pass an argument array. Prefer a library call over a subprocess at all
(e.g. `socket` instead of `ping`). Watch for **argument injection** too: a value starting with `-`.

```python
# Python
subprocess.run(["ping", "-c", "1", "--", host], shell=False, timeout=5, check=False)
# if a shell is unavoidable: shlex.quote(host)
```

```php
// PHP
$out = shell_exec('ping -c 1 ' . escapeshellarg($host));
// better: validate first
if (!filter_var($host, FILTER_VALIDATE_IP)) exit;
```

```js
// Node — execFile/spawn don't use a shell; exec does
execFile("ping", ["-c", "1", "--", host], { timeout: 5000 }, cb);
```

```java
// Java
new ProcessBuilder("ping", "-c", "1", "--", host).start();   // NOT Runtime.exec("sh -c ...")
```

```go
// Go — exec.Command never uses a shell, unless you call "sh", "-c"
exec.Command("ping", "-c", "1", "--", host).Run()
```

```csharp
// C#
var psi = new ProcessStartInfo("ping");
psi.ArgumentList.Add("-c"); psi.ArgumentList.Add("1"); psi.ArgumentList.Add(host);
```

```ruby
# Ruby — multi-arg form skips the shell; backticks / %x / single-string system don't
system("ping", "-c", "1", "--", host)
```

```c
// C — replace system()/popen() with fork + execve/execvp
char *argv[] = {"ping", "-c", "1", "--", host, NULL};
execvp("ping", argv);
```

Validate the shape too (`ipaddress.ip_address(host)`, `^[a-z0-9.-]+$`) and reject leading `-`.
Not every tool understands `--`.

---

## 8. SSTI (Server-Side Template Injection)

**Fix:** user input is *data* passed to a fixed template, never the template itself.

```python
# Python / Flask / Jinja2
return render_template_string("Hello " + name)               # vulnerable
return render_template_string("Hello {{ name }}", name=name)  # fixed
# if users really must write templates:
from jinja2.sandbox import SandboxedEnvironment
SandboxedEnvironment().from_string(tpl).render(...)
```

```js
// Node — ejs / pug / handlebars / nunjucks
ejs.render(req.body.template, data);           // vulnerable
res.render("profile", { name: req.body.name }); // fixed (fixed template file)
```

```java
// Java — Freemarker / Velocity / Thymeleaf
// never new Template("t", new StringReader(userInput), cfg)
cfg.setNewBuiltinClassResolver(TemplateClassResolver.ALLOWS_NOTHING_RESOLVER); // Freemarker: blocks ?new
```

```go
// Go — text/template with user-controlled template text can call exported methods
tmpl := template.Must(template.New("t").Parse("Hello {{.}}"))   // fixed template
tmpl.Execute(w, name)                                           // html/template for HTML
```

```php
// PHP — Twig
$twig->createTemplate($userInput)->render();            // vulnerable
$twig->render('hello.twig', ['name' => $userInput]);   // fixed
```

---

## 9. Insecure Deserialization

**Fix:** use a data-only format (JSON). If the format must stay (existing data!), restrict classes.

| Language | Dangerous | Fix |
|---|---|---|
| Python | `pickle.loads`, `yaml.load(x)`, `yaml.unsafe_load`, `jsonpickle.decode`, `shelve` | `json.loads`, `yaml.safe_load` |
| PHP | `unserialize($user)` | `json_decode`, or `unserialize($x, ['allowed_classes' => false])` |
| Java | `ObjectInputStream.readObject`, XStream, Jackson default typing | JSON DTOs, `ObjectInputFilter` allowlist, disable `enableDefaultTyping` |
| Node | `node-serialize` / `serialize-javascript` + `eval`, `funcster` | `JSON.parse` |
| Ruby | `Marshal.load`, `YAML.load` (Psych < 4), `Oj.load` (object mode) | `JSON.parse`, `YAML.safe_load` |
| .NET | `BinaryFormatter`, `NetDataContractSerializer`, `TypeNameHandling.All` | `System.Text.Json`, `TypeNameHandling.None` |

```python
# Signed cookies that carry pickles (e.g. custom session): the HMAC key is the only protection.
# If that key is hardcoded (every team has the source) → RCE. Rotate the key (§11) AND switch to json.
```

```java
// Java 9+ — global allowlist filter
ObjectInputFilter f = ObjectInputFilter.Config.createFilter("com.example.model.*;java.lang.*;!*");
ois.setObjectInputFilter(f);
```

---

## 10. IDOR & Missing Authentication

**Fix:** every handler that returns user data must (1) require a logged-in user and (2) check that the
object belongs to *that* user. Take the identity from the **session**, never from a parameter.

```python
# Python / Flask — owner in the WHERE clause
@app.get("/note/<int:note_id>")
@login_required
def note(note_id):
    row = db.execute("SELECT * FROM notes WHERE id = ? AND owner_id = ?",
                     (note_id, session["user_id"])).fetchone()
    if row is None:
        abort(404)
```

```python
# Python / FastAPI — finding from fastvuln: GET /backdoor?username=...
# Best: delete the route (check traffic logs first that the checker never calls it).
@app.get("/backdoor", response_model=UserProfile)
def get_backdoor(username: str, current: User = Depends(get_current_user)):
    if current.username != username:
        raise HTTPException(status_code=403)
    ...
```

```python
# Python / aiohttp — finding from fireworx: `if "username" in session:` → any logged-in user
session = await get_session(request)
if session.get("username") == requested_username:   # owner check, not just "is logged in"
    data += privkey.dict().items()
else:
    data += privkey.pubkey().dict().items()
```

```js
// Node / Express
app.get("/note/:id", requireLogin, async (req, res) => {
  const note = await Note.findOne({ _id: req.params.id, owner: req.session.userId });
  if (!note) return res.sendStatus(404);
  res.json(note);
});
```

```go
// Go
userID := sessionUserID(r)                       // from the session, not r.URL.Query()
row := db.QueryRow("SELECT body FROM notes WHERE id = ? AND owner = ?", id, userID)
```

```php
// PHP
$stmt = $pdo->prepare("SELECT * FROM notes WHERE id = ? AND owner = ?");
$stmt->execute([$_GET['id'], $_SESSION['user_id']]);
```

**Where to look:** routes named `admin`, `flag`, `debug`, `backdoor`, `export`, `profile`, `api/users/<id>`,
list endpoints (`/notes` returning everyone's notes), search endpoints, and "share" links with
sequential or guessable IDs (swap them for `secrets.token_urlsafe(16)`).

---

## 11. Sessions, Secrets & JWT

Every team has your source code, so **any hardcoded secret is public**.

```python
# Python / Flask — persist a random key so all workers and restarts share it
import os, secrets, pathlib
key_file = pathlib.Path("/data/secret_key")          # a volume, writable by the app
if not key_file.exists():
    key_file.write_text(secrets.token_hex(32))
app.secret_key = key_file.read_text()
# os.urandom(32) per process breaks sessions with several gunicorn workers → checker fails
```

```js
// Node / Express — finding from stonksexchange: secret: 'keyboard cat'
app.use(session({
  secret: process.env.SESSION_SECRET || require("crypto").randomBytes(32).toString("hex"),
  resave: false,
  saveUninitialized: false,
}));
// set SESSION_SECRET in docker-compose (or a .env file) so restarts don't log everyone out
```

```php
// PHP — custom HMAC cookies: replace the constant with a random key from a file outside the webroot
$key = trim(file_get_contents('/data/hmac.key'));
hash_equals(hash_hmac('sha256', $data, $key), $sig);   // constant-time compare
```

**JWT:**

```python
# PyJWT — pin the algorithm; never verify=False / options={"verify_signature": False}
jwt.decode(token, SECRET, algorithms=["HS256"])
```

```js
// jsonwebtoken — jwt.decode() does NOT verify
jwt.verify(token, SECRET, { algorithms: ["HS256"] });
```

```java
// jjwt
Jwts.parser().verifyWith(key).build().parseSignedClaims(token);   // not parseUnsecuredClaims
```

| JWT bug | Fix |
|---|---|
| `alg: none` accepted | Pin `algorithms=[...]` |
| RS256 → HS256 confusion (public key used as HMAC secret) | Pin the algorithm; separate key objects per alg |
| Hardcoded / weak secret (`secret`, `changeme`) | Random 32+ byte secret from env/file |
| `kid` / `jku` header used to load a key from a path/URL | Ignore it or allowlist |
| `decode` instead of `verify` | Use the verifying function |

---

## 12. Weak Randomness

If the value is a **token, session ID, password, reset code, note ID, filename, key, or nonce**, use a CSPRNG.

| Language | Weak | Secure |
|---|---|---|
| Python | `random.*`, `numpy.random` | `secrets.token_hex(16)`, `secrets.token_urlsafe(16)`, `secrets.randbelow(n)`, `secrets.token_bytes(16)` |
| Node | `Math.random()` | `crypto.randomBytes(16)`, `crypto.randomUUID()`, `crypto.randomInt(n)` |
| Browser JS | `Math.random()` | `crypto.getRandomValues(new Uint8Array(16))` |
| Java | `java.util.Random`, `Math.random()` | `java.security.SecureRandom` |
| Go | `math/rand` | `crypto/rand` (`rand.Read(b)`, `rand.Text()` in Go 1.24+) |
| PHP | `rand()`, `mt_rand()`, `uniqid()` | `random_bytes(16)`, `random_int(a, b)`, `bin2hex(random_bytes(16))` |
| Ruby | `rand`, `Random.new` | `SecureRandom.hex(16)` |
| C# | `System.Random` | `RandomNumberGenerator.GetBytes(16)` |
| C | `rand()`, `srand(time(NULL))` | `getrandom()` (Linux), `/dev/urandom` |

```python
# Python — fireworx: DSA private key and nonces from `random`
x = secrets.randbelow(q - 1) + 1          # was random.randint(1, q - 1)
nonce = int.from_bytes(secrets.token_bytes(16), "big")   # was random.randbytes(16)
session["pow_prefix"] = secrets.token_hex(3)[:5]
```

```c
// C — stldoctor: srand(time(NULL)); id = rand() ...
#include <sys/random.h>
unsigned int r;
if (getrandom(&r, sizeof r, 0) != sizeof r) abort();
```

> **A/D trap:** if the PRNG output is *persisted and re-derived later* (e.g. `srand(seed)` to rebuild an
> XOR keystream that decodes stored data), swapping the RNG breaks existing flags and the checker.
> In that case fix the *exploitable* part (overflow, predictable seed source) and keep the derivation
> deterministic, or migrate the data.

---

## 13. Crypto bugs (signatures, MACs, hashes)

Hand-rolled crypto in A/D services usually hides several bugs at once. Check each one:

```python
# DSA/ECDSA sign — static/deterministic nonce (fireworx: k = H(self.y))
# Two signatures with the same k → k → private key x.
k = secrets.randbelow(q - 1) + 1      # fresh per signature (or RFC 6979: k derived from x AND H(m))

# DSA/ECDSA verify — missing range check (fireworx): r=1, s=0 makes inverse() return 0 → v = 1 = r
def verify(self, m, r, s):
    if not (0 < r < self.q and 0 < s < self.q):
        return False
    w = inverse(s, self.q)
    ...
```

```python
# Signature / MAC oracle (fireworx): error path sends the expected value back
return web.Response(status=400, text=f"bad signature, expected {expected}")   # vulnerable
return web.Response(status=400, text="bad signature")                          # fixed

# Constant-time comparison
hmac.compare_digest(given, expected)
```

| Bug | Fix |
|---|---|
| Comparing secrets with `==` / `strcmp` / `memcmp` | `hmac.compare_digest`, `crypto.timingSafeEqual`, `MessageDigest.isEqual`, `subtle.ConstantTimeCompare`, `hash_equals`, `CRYPTO_memcmp` |
| `MAC = H(key ‖ msg)` with MD5/SHA1/SHA256 (length extension) | `hmac.new(key, msg, sha256)` |
| AES-ECB (block cut-and-paste, e.g. `role=admin` blocks) | AES-GCM with random 12-byte nonce |
| AES-CBC without MAC (padding oracle, bit flipping) | AES-GCM, or encrypt-then-MAC |
| Static IV / nonce reuse in CTR/GCM | Random nonce per message |
| RSA with small `e` and no padding, shared modulus, tiny primes | Use a library with OAEP/PSS; regenerate keys |
| Passwords hashed with MD5/SHA1/unsalted SHA256 | bcrypt/argon2, **but only if you can migrate existing users** (see §21) |
| MD5 in a proof-of-work / cache key / checksum | Not a vuln. Leave it |

---

## 14. XSS

Only worth patching early if the game has a **bot that visits pages** (admin viewer, report feature).
Otherwise it's low priority.

```js
// Frontend — fireworx: log.innerHTML = xhr.responseText
log.textContent = xhr.responseText;
log.textContent = "Generation failed:\n" + data;
// need HTML? DOMPurify.sanitize(html)
```

| Stack | Escaped by default | Bypass to look for |
|---|---|---|
| Jinja2 / Flask | yes (`.html` templates) | `\|safe`, `Markup()`, `{% autoescape false %}`, `render_template_string` with `.txt` |
| Express + EJS | `<%= %>` yes | `<%- %>` |
| Handlebars | `{{ }}` yes | `{{{ }}}` |
| React | yes | `dangerouslySetInnerHTML` |
| Vue | yes | `v-html` |
| PHP | no | `echo $x` → `echo htmlspecialchars($x, ENT_QUOTES, 'UTF-8')` |
| Go | `html/template` yes | `text/template` used for HTML, `template.HTML(x)` |

Defense in depth: `Content-Security-Policy: default-src 'self'`, `HttpOnly` + `SameSite=Lax` cookies.

---

## 15. SSRF

```python
# Python — allowlist by scheme + resolved IP; disable redirects
import ipaddress, socket
from urllib.parse import urlparse
u = urlparse(url)
if u.scheme not in ("http", "https") or not u.hostname:
    abort(400)
for info in socket.getaddrinfo(u.hostname, u.port or 80):
    ip = ipaddress.ip_address(info[4][0])
    if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
        abort(403)
requests.get(url, allow_redirects=False, timeout=5)
```

```js
// Node — same idea: resolve, check, then request with redirects disabled
const { address } = await dns.promises.lookup(new URL(url).hostname);
if (ipaddr.parse(address).range() !== "unicast") return res.sendStatus(403);
```

Typical A/D target: an internal admin endpoint or the DB on `127.0.0.1`. If the feature only ever needs
one host, **hardcode it** and drop the user-supplied URL.

---

## 16. XXE

```python
# Python
import defusedxml.ElementTree as ET      # drop-in for xml.etree
ET.fromstring(data)
# lxml
etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
```

```java
// Java
DocumentBuilderFactory f = DocumentBuilderFactory.newInstance();
f.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
f.setXIncludeAware(false);
f.setExpandEntityReferences(false);
```

```php
// PHP 8: external entities off by default. Don't pass LIBXML_NOENT / LIBXML_DTDLOAD
$doc->loadXML($xml);                      // NOT loadXML($xml, LIBXML_NOENT)
```

```csharp
// .NET
var settings = new XmlReaderSettings { DtdProcessing = DtdProcessing.Prohibit, XmlResolver = null };
```

---

## 17. C / memory-safety bugs

| Bug | Vulnerable | Fixed |
|---|---|---|
| Unbounded copy | `strcpy(d, s)`, `strcat`, `sprintf`, `gets` | `snprintf(d, sizeof d, "%s", s)`, `strncat(d, s, sizeof d - strlen(d) - 1)`, `fgets(b, sizeof b, stdin)` |
| Format string | `printf(user)` | `printf("%s", user)` |
| Signed char in `%x` (stldoctor) | `sprintf(bp, "%02x", c)` → `ffffff80` | `snprintf(bp, end - bp, "%02x", (unsigned char)c)` |
| `char` vs `EOF` (stldoctor) | `char c; while ((c = fgetc(f)) != EOF)` | `int c;` |
| Length from attacker (stldoctor) | `strncmp(a, b, strlen(a))` → empty `a` matches | check `strlen(a) == strlen(b)` first, then constant-time compare |
| Size overflow (stldoctor) | `malloc(n * sizeof(T))`, `realloc(p, n * sizeof(T))` | `calloc(n, sizeof(T))`, `reallocarray(p, n, sizeof(T))` |
| Off-by-one | `buf[len] = 0` with `len == sizeof buf` | `if (len >= sizeof buf) len = sizeof buf - 1;` |
| Signed length | `int len = read_len(); if (len > MAX) …; memcpy(d, s, len)` with `len < 0` | `size_t` / check `len < 0` |
| Use-after-free | `free(p);` then use | `free(p); p = NULL;` |
| Stack read | `read(fd, buf, 0x200)` into `char buf[0x100]` | `read(fd, buf, sizeof buf)` |

```c
// stldoctor util.c — hex-encode without overflow
char *bp = out, *end = out + outsz;
for (size_t i = 0; i < n; i++) {
    int w = snprintf(bp, end - bp, "%02x", (unsigned char)(str[i % len] ^ key[i]));
    if (w < 0 || w >= end - bp) break;
    bp += w;
}

// stldoctor util.c — prefix/password compare
size_t pl = strlen(prefix);
if (pl == 0 || strlen(str) < pl) return 0;   // or require strlen(str) == pl for exact matches
return CRYPTO_memcmp(prefix, str, pl) == 0;  // or a hand-written constant-time loop
```

**How to look:** find the auth state (`loggedin`, `is_admin`, `user_id`) and check which buffers sit next to
it in `.bss`/the stack (`nm -n binary`, a struct definition). An overflow of a few bytes into that flag
is the classic A/D C bug. Rebuild with `-fstack-protector-strong -D_FORTIFY_SOURCE=2 -O2` as defense in depth,
but only if the Dockerfile already builds from source.

---

## 18. PHP-specific traps

| Trap | Vulnerable | Fixed |
|---|---|---|
| Loose comparison | `if ($hash == $_GET['h'])` (`"0e123" == "0e456"` is true) | `hash_equals($hash, $_GET['h'])` / `===` |
| `strcmp` with arrays | `if (strcmp($_GET['p'], $pw) == 0)` (`p[]=` returns `NULL` → `== 0`) | `is_string()` check + `hash_equals` |
| `in_array` / `array_search` | `in_array($x, $allowed)` | `in_array($x, $allowed, true)` |
| `extract($_GET)` / `parse_str($q)` without target | overwrites `$is_admin` | remove; read keys explicitly |
| `include $_GET['page']` | LFI / RFI / `php://filter` | map from allowlist (§6) |
| `preg_replace` with `/e` (old PHP) | code exec | `preg_replace_callback` |
| `assert($user)`, `eval`, `create_function` | code exec | remove |
| File upload by extension only | `shell.php.jpg`, `.phtml`, `.htaccess` | random filename + fixed extension, store outside webroot, deny PHP exec in upload dir |
| `unserialize($_COOKIE[...])` | object injection | `json_decode` (§9) |

---

## 19. Container / infra quick fixes

| Finding | Fix | Game priority |
|---|---|---|
| `chmod 777` on code/data (fireworx) | `chown -R app:app data && chmod 750 data` | Medium: matters once another service on the box is popped |
| Service runs as root | `USER app` in Dockerfile | Medium |
| DB / Redis / admin port exposed on `0.0.0.0` | Bind to the internal docker network only; remove the `ports:` mapping | **High** (direct flag read) |
| Default DB credentials (`root:root`, `postgres:postgres`) | Change them in compose **and** app config at the same time | **High** |
| Debug mode on (`FLASK_DEBUG=1`, Werkzeug console, `app.run(debug=True)`) | Turn it off. The Werkzeug debugger is RCE | **High** |
| `ADD https://...` / `curl \| sh` in Dockerfile | Pin a checksum. Not exploitable by other teams | Low |

---

## 20. CheatSheet: grep → fix

Run from the service root. `rg` = ripgrep (falls back to `grep -rnE`).

```bash
# SQLi: string-built queries
rg -n --pcre2 '(execute|query|raw|prepare)\s*\(\s*(f["'\'']|["'\''].*["'\'']\s*(\+|%|\.format))'
rg -n 'sprintf\(.*(SELECT|INSERT|UPDATE|DELETE)' -i
rg -n '\$\{.*\}.*(SELECT|WHERE)|(SELECT|WHERE).*\$\{' -i            # JS template literals
# NoSQLi
rg -n 'find(One)?\(\{[^}]*req\.(body|query|params)'
rg -n '\$where'
# Path traversal / LFI
rg -n '(open|readFile|sendFile|send_file|file_get_contents|include|require|fopen|os\.Open|File\.read)\s*\(.*(req|request|params|args|GET|POST|query|name)'
# Command injection
rg -n 'os\.system|subprocess.*shell=True|popen|child_process|exec\(|execSync|shell_exec|passthru|system\(|`.*\$\{|Runtime\.getRuntime|"sh", "-c"'
# SSTI
rg -n 'render_template_string|Template\(|from_string|ejs\.render|createTemplate|template\.New\(.*\)\.Parse\(.*(req|r\.)'
# Deserialization
rg -n 'pickle\.loads?|yaml\.load\(|unserialize\(|ObjectInputStream|Marshal\.load|BinaryFormatter|node-serialize|jsonpickle'
# Auth / IDOR: sensitive routes, presence-only session checks
rg -n -i '(route|get|post|app\.\w+)\(.*(admin|flag|debug|backdoor|export|internal|profile)'
rg -n 'in session|session\.get\(|req\.session\.\w+\s*\)'
# Hardcoded secrets
rg -n -i '(secret|secret_key|jwt|hmac|password|api_key)\s*[:=]\s*["'\''][^"'\'']{3,}'
rg -n "keyboard cat|changeme|supersecret|s3cr3t"
# JWT misuse
rg -n 'jwt\.decode|verify_signature.*False|algorithms.*none|parseUnsecured' -i
# Weak randomness
rg -n 'random\.(randint|choice|choices|random|randbytes|getrandbits)|Math\.random|mt_rand|\brand\(|srand\(|math/rand|new Random\('
# Crypto
rg -n -i 'md5|sha1|AES\.MODE_ECB|ECB|iv\s*=\s*b?["'\'']|nonce\s*=|k\s*=\s*H\('
rg -n '==\s*(sig|signature|mac|hmac|token|hash)|strcmp\(.*(pass|token|hash)' -i
# C memory
rg -n '\b(strcpy|strcat|sprintf|vsprintf|gets|scanf\("%s")\b'
rg -n 'printf\(\s*[a-z_]+\s*\)'                                       # format string
rg -n 'malloc\([^)]*\*|realloc\([^)]*\*'
rg -n '\b(fgetc|getc|getchar)\('                                     # then check the variable is int, not char
# XSS
rg -n 'innerHTML|outerHTML|document\.write|\|\s*safe|<%-|\{\{\{|dangerouslySetInnerHTML|v-html'
# SSRF / XXE
rg -n 'requests\.(get|post)\(|urlopen|axios\(|fetch\(|http\.Get\(|curl_exec|file_get_contents\(\$'
rg -n 'XMLParser|DocumentBuilderFactory|LIBXML_NOENT|resolve_entities|etree\.parse'
```

**One-line fixes**

| Vuln | Python | Node | PHP | Java | Go | C |
|---|---|---|---|---|---|---|
| SQLi | `cur.execute(q, (x,))` | `db.execute(q, [x])` | `$pdo->prepare(q)->execute([$x])` | `PreparedStatement` | `db.Query(q, x)` | `sqlite3_bind_text` |
| NoSQLi | `isinstance(x, str)` | `String(x)` | `is_string($x)` | typed DTO | typed struct | — |
| Path traversal | `resolve()` + `is_relative_to` | `path.resolve` + `startsWith(base+sep)` | `realpath` + `str_starts_with` | `normalize()` + `startsWith` | `filepath.IsLocal` / `os.OpenRoot` | `realpath` + prefix |
| Cmd injection | `subprocess.run([..])` | `execFile(cmd, [..])` | `escapeshellarg` | `ProcessBuilder(list)` | `exec.Command(a, b)` | `execvp` |
| SSTI | `render_template(..., x=x)` | `res.render(view, {x})` | `$twig->render(file, [..])` | no user templates | fixed `Parse` | — |
| Deserialization | `json.loads` / `yaml.safe_load` | `JSON.parse` | `json_decode` | `ObjectInputFilter` | `encoding/json` | — |
| IDOR | `WHERE id=? AND owner=?` | `{_id, owner: req.session.userId}` | `AND owner = ?` | same | same | same |
| Secrets | `secrets.token_hex(32)` from file | `crypto.randomBytes(32)` from env | `random_bytes(32)` from file | `SecureRandom` | `crypto/rand` | `getrandom` |
| Compare | `hmac.compare_digest` | `crypto.timingSafeEqual` | `hash_equals` | `MessageDigest.isEqual` | `subtle.ConstantTimeCompare` | `CRYPTO_memcmp` |
| Random | `secrets` | `crypto.randomBytes` | `random_bytes` | `SecureRandom` | `crypto/rand` | `getrandom` |
| XSS | autoescape on, no `\|safe` | `textContent` | `htmlspecialchars` | encode on output | `html/template` | — |

---

## 21. Patching pitfalls (how teams lose SLA)

- **Changing storage format.** Hashing passwords that were stored in plaintext, or renaming a column,
  makes every existing user (and the checker's previously stored flags) unreadable. Patch the *access path*,
  not the data.
- **Rotating secrets that the checker relies on.** A new session secret logs everyone out: usually fine.
  A new signing key for tokens the checker issued last round breaks flag retrieval. Rotate at a round
  boundary, and persist the new value so restarts don't rotate it again.
- **Blocking by IP or User-Agent.** The checker often comes from the same network as attackers, and
  many games forbid it. Patch the bug instead.
- **Over-strict validation.** A regex `^[a-z]+$` on usernames breaks a checker that registers `user_8f3a1`.
  Check what the checker sends (traffic capture) before tightening.
- **Changing responses.** Different status codes, extra fields, or new error text can make the checker
  mark the service as "mumble". Keep the success path byte-identical.
- **Adding dependencies mid-game.** `pip install` / `npm install` in a rebuilt image may fail offline.
  Prefer standard-library fixes (`secrets`, `hmac`, `crypto`, `pathlib`).
- **Patching only the first exploit.** When one hole closes, attackers move to the next one in the
  same service. After a patch, re-read the whole file and re-run the scanner.
- **Forgetting the restart.** The fix in the source does nothing until the container is rebuilt.
  Many teams "patch" for an hour without redeploying.
- **No rollback.** Always commit before and after each patch (§1).
- **Deleting a feature the checker uses.** Deleting a backdoor route is fine. Deleting `/export`
  because it leaks data is not, if the checker downloads its flag from there. Add the auth check instead.

---

### References

- Per-vulnerability notes in this repo: [`vulns/`](vulns/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) (to test your own patches)
