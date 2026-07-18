# Function Audit Report
**Date:** 2026-05-22  
**Scope:** All `.src` files under `src/`, `exploits/`, `utilities/`, `Bash/`, `scanner/`  
**Tool:** `audit_functions.py` (static analysis)

---

## Summary

| Metric | Count |
|--------|-------|
| Source files scanned | 279 |
| Total function definitions | 2,311 |
| Confirmed dead functions | ~40–60 (see notes on false positives) |
| Confirmed duplicate logic | 5–8 cases |

> **Important:** Static analysis finds functions never referenced by their *full qualified name*.  
> Many false positives exist because GreyScript calls functions via:
> - `self.method()` — inheritance/delegation (Bash._lex, RshellCommon.*, etc.)
> - `instance.method()` — e.g. `_p.addArgument()` for ArgumentParser
> - `globals.G_agent.method()` — AI module merge pattern
> - `globals.funcName()` — global function wrappers
> - `Obj.New` + instance calls — e.g. `s=Solver.New; s.solve()`
> - String dispatch — `Command.X` (99 functions, all fine)

---

## SECTION 1: CONFIRMED DEAD CODE

These were verified by checking no indirect call patterns exist.

### 1.1 — `src/libs/disk.src` — ~~5 dead helper functions~~ FALSE POSITIVE

All 5 helpers are called via `self.*` from `Disk.list`:
- `self.analyzeFileSystem(Obj,startPath)` — L279
- `self.sortBySize(results,...)` — L353
- `self.sortByName(results,...)` — L356
- `self._quicksort(...)` — called from sortBySize/sortByName
- `self.displayResults(results,maxDisplay,true)` — L405

Phase 2 self.* fix correctly identifies all as alive (call_count=1).

---

### 1.2 — `src/libs/date.src` — ~~Entire module dead~~ FALSE POSITIVE

All `Date.*` functions are called via `self.*` within `date.src`. `Date.calculate0day` is also called externally from `partial_objects.src` L420 (the 0day command). Phase 2 self.* fix correctly identifies all as alive.

---

### 1.3 — `src/compression/safe_map.src` — ~~11 of 13 methods unused~~ RESOLVED

`lzw.src` now uses inline `char(1)`-prefixed dict keys instead of SafeMap. `SafeMap` has zero callers — the entire file can be deleted.

**Recommendation:** Delete `src/compression/safe_map.src`.

---

### 1.4 — `src/libs/crack.src` — `Crack.sha256` dead (note: lowercase)

- `Crack.SHA256` (uppercase, L1349) — ✅ used, it's the user command  
- `Crack.sha256` (lowercase, L1338) — ❌ dead, a hash-lookup cracker function with 0 callers

**Recommendation:** Verify intent — either wire `Crack.sha256` into a cracking flow or remove it.

---

### 1.5 — Dead IO helpers

| Function | File | Line | Notes |
|----------|------|------|-------|
| ~~`Io.checkRW`~~ | — | — | **FALSE POSITIVE** — called 7× via `self.checkRW(f)` inside io.src |
| ~~`Io._fileOpInteractive`~~ | — | — | **FALSE POSITIVE** — called via `self._fileOpInteractive()` at L350, L354 |
| ~~`Io._fileOp`~~ | — | — | **FALSE POSITIVE** — called via `self._fileOp()` at L2204, L2205 |
| `Io.string` | `src/libs/io.src` | 29 | Formats r/w booleans, never called |
| `Io.findAny` | `src/libs/io.src` | 1969 | Recursive file search, no callers |
| `Io.uploadLog` | `src/libs/io.src` | 2260 | No callers |
| `Io.downloadLog` | `src/libs/io.src` | 2283 | No callers |

---

### 1.6 — `src/compression/encoder.src` — `Encoder.divide` dead

`Encoder.divide` (L32) has no callers. The `Encoder.toInt` and `Encoder.encode` are used.

---

### 1.7 — `src/man/man_loader.src` — `Man.header` dead

`Man.header` (L74) defined but never called.

---

### 1.8 — `src/network/net.src` — Dead standalone helpers

| Function | Line | Notes |
|----------|------|-------|
| ~~`initInfo`~~ | 842 | Removed |
| ~~`Net.firewallAccess`~~ | — | **FALSE POSITIVE** — called via `self.firewallAccess(...)` at L2381 inside net.src |
| ~~`Net.getRouter`~~ | 2397 | Removed |
| ~~`Net.addSession`~~ | — | **FALSE POSITIVE** — called via `self.addSession(...)` at L2523 inside net.src |

---

### 1.9 — `src/libs/log.src` — Dead log helpers

| Function | Line |
|----------|------|
| `Log.logFallback` | 18 |
| ~~`Log.logLastResort`~~ | 164 | **FALSE POSITIVE** — called via `self.logLastResort(...)` in `logX`, `logC`, `logT`, `log`, `fileLog` |
| ~~`Log.fileTransLog`~~ | 237 | **FALSE POSITIVE** — called via `self.fileTransLog(Obj)` in `transLog` |

---

### 1.10 — `src/libs/math.src` — Dead math utilities

| Function | Line | Notes |
|----------|------|-------|
| ~~`Math.levenshtein`~~ | — | Removed |
| `Math.max` | 40 | Duplicate of built-in `max()`? |
| `Math.min` | 49 | Duplicate of built-in `min()`? |
| `Math.exp` | 147 | No callers |

---

### 1.11 — `src/type_ext/globals.src` — Dead session cleaners

These are called via `globals.rmSession(...)` — but the STANDALONE token `rmSession` is never called.  
**This is a confirmed false positive** — they ARE used. See False Positives section.

---

### 1.12 — New confirmed dead (verified May 2026)

All verified with `grep` — zero callers anywhere.

| Function | File | Line | Notes |
|----------|------|------|-------|
| ~~`Boot.initDecoy`~~ | — | **FALSE POSITIVE** — called from `main.src:391` bootstrap (`params[1]=="decoy"`) |
| ~~`Boot.crack`~~ | — | **FALSE POSITIVE** — called from `main.src:382,385` bootstrap (`params[1]=="pass"`/`"shell"`) |
| ~~`Config._toggle`~~ | `src/system/config.src` | 131 | **FALSE POSITIVE** — called via `self._toggle(...)` in 15 wrapper functions |
| ~~`Gui.prompt`~~ | `src/system/gui.src` | 218 | **FALSE POSITIVE** — called via `self.prompt(...)` in `choiceAlpha`, `choiceHybrid`, `yesNo`, `yesNoNon` |
| ~~`Heist.corrupt`~~ | `src/libs/heist.src` | 33 | **FALSE POSITIVE** — called via `self.corrupt(...)` in `doWait` |
| `Farm.decipher` | `src/libs/farm.src` | 308 | No callers |
| `Farm.dictionary` | `src/libs/farm.src` | 333 | No callers |
| `Proxy.createMapConf` | `src/libs/proxy.src` | 269 | No callers |
| `ShellObject.packCrypto` | `src/objects/shell_object.src` | 83 | Wrapper around `Builder.packCrypto`; all callers use `Builder.packCrypto` directly |
| `viewFile` | `src/libs/attack_dig.src` | 682 | Standalone local function, zero references |

---

## SECTION 2: CONFIRMED DUPLICATE LOGIC

### 2.1 — `AgentCore` vs `AgentPlanning` — 5 duplicated methods

When `Command.ai` initializes the agent, it merges ALL agent modules into `G_agent`:
```
for key in indexes(AgentCore); globals.G_agent[key]=AgentCore[key]; end for
for key in indexes(AgentPlanning); globals.G_agent[key]=AgentPlanning[key]; end for
```
Because `AgentPlanning` is loaded **after** `AgentCore`, its version **overwrites** AgentCore's for these 5 functions:

| Shared Method | AgentCore location | AgentPlanning location |
|---------------|-------------------|----------------------|
| `_askUser` | `agent_util.src:190` | `agent_planning.src:116` |
| `_expandSubnet` | `agent_util.src:132` | `agent_planning.src:12` |
| `_extractIps` | `agent_util.src:74` | `agent_planning.src:45` |
| `_isPrivateIp` | `agent_util.src:116` | `agent_planning.src:91` |
| `_promptUser` | `agent_util.src:181` | `agent_planning.src:107` |

**Impact:** The `AgentCore` versions of these 5 functions are silently dead — they get overwritten on load.  
**Recommendation:** Pick one canonical location for each; remove the other.

---

### 2.2 — `AgentCommandKnowledge.getSemanticFlags` vs `AgentCommandRegistry.getSemanticFlags`

Both are dead (never called via full name), but they exist in parallel in two different agent knowledge files.  
Verify whether these should be unified.

---

### 2.3 — ~~`Disk.analyzeFileSystem` vs `Disk.list`~~ FALSE POSITIVE

`Disk.list` calls `self.analyzeFileSystem(Obj,startPath)` — the function is wired in. Not a duplicate concern.

---

### 2.4 — `Crack.sha256` vs `Crypt.SHA256`

- `Crypt.SHA256(x)` — the pure crypto implementation (used in `Crack.SHA256` and elsewhere)
- `Crack.sha256(h)` — takes a hash and tries to crack it by iterating a dictionary and comparing to `Crypt.SHA256(p)`. It appears to be an abandoned cracking helper superseded by `Crack.rainbow`/`Crack.findPassword`.

These are NOT the same function, but `Crack.sha256` looks like dead cracking logic.

---

## SECTION 3: FALSE POSITIVES (NOT actually dead)

The raw audit flagged **443** functions as dead. Most are false positives:

| Pattern | Example | Why false positive |
|---------|---------|-------------------|
| AI agent module merge | `AgentPlanning.*`, `AgentCore.*` (60+70 fns) | Merged into `G_agent`, called via `globals.G_agent.method()` |
| `self.method()` calls | `RshellCommon.*`, `Bash._lex`, `Bash._hasChain`, `Io._fileOp`, `Io._fileOpInteractive`, `Session.*`, `Share.rename` | Called via `self.` from within the same object |
| Instance method calls | `ArgumentParser.addArgument`, `Parser.parse` | Called as `_p.addArgument()`, `_parser.parse()` |
| `globals.funcName()` | `rmSession`, `rmByKey`, `killallSessions` | Called as `globals.rmSession()` |
| `Obj.New` + instance | `Solver.*` (31 fns) | Created via `s=Solver.New`, called as `s.solve()` |
| Type extensions | `list.each`, `list.map`, `map.each`, `number.toHex` | Called as native type methods: `myList.each()` |
| Command dispatch | `Command.psLock`, `Command.trim`, etc. (99 fns) | Registered as string-keyed dispatch entries |
| Polymorphic `.run()` | `MainObject.run`, `FTPShellObject.run`, etc. | Called via `Obj.run(...)` on different instance types |

---

## SECTION 4: WORTH REVIEWING (low-confidence dead)

These were flagged dead and may or may not be used via `self.*`:

| File | Functions | Count |
|------|-----------|-------|
| `src/libs/exploit.src` | `setFlag`, `clearFlag`, `hasFlag`, `packExploit`, `checksum`, bloom filter (`_bloomHashes`,`addToBloom`,`checkBloom`), `_getTree/_setTree/_loadTree`, `_tryLocalShell`, `returnShell` | 14 |
| `src/libs/exploit_scan.src` | `getNewFile`, `getNewFolder`, `checkUpdate`, `known`, `update`, `chooseLocal`, `change`, `runInput` | 8 |
| `src/libs/missions.src` | `extractBold`, `_ensureCache`, `getObject`, `getPasswd`, `init` (Mission + Mail + Inbox) | 9 |
| `src/libs/partial_objects.src` | `_formatPatchLine`, `getMetalib`, `checkDatabase`, `writeLog`, `checkip`, `_chooseCredential`, `_lookupService` | 7 |
| `src/system/system.src` | `_buildTerminalSrc`, `_readCredentials`, `_transferFiles`, `_changeRootPassword`, `_encryptedConnect`, `_compileBinary`, `_setupEncryption`, `_changeEncryption`, `_promptCredentials`, `restoreBoot`, `restoreEtc`, `restoreSystem`, `createDBDat`, `createLDBDat`, `interWeb` | 15 |
| `src/system/bash_lexer.src` | All 19 `Bash._lex*` functions | 19 (likely called via `self.*`) |

---

## SECTION 5: LARGE DEAD BLOCKS (flagged but likely false positives)

These entire files/objects were flagged as dead but are actually called via indirect patterns:

| Object | Functions | Actual call pattern |
|--------|-----------|---------------------|
| `RshellCommon` | 26 | Called via `self.*` from `Rshell`/`RshellLite` |
| `AgentExecution` | 4 | Merged into `G_agent`, called indirectly |
| `AgentLearning` | 6 | Merged into `G_agent`, called indirectly |
| `AgentParser` | 3 | Merged into `G_agent`, called indirectly |
| `Solver` | 31 | Called via `s=Solver.New; s.method()` |

---

## Quick-Win Cleanup Checklist

- [ ] Delete `src/compression/safe_map.src` (lzw.src no longer uses SafeMap — zero callers)
- [ ] Remove `Crack.sha256` (lowercase, L1338) from `crack.src`
- [ ] Remove `Io.string`, `Io.findAny`, `Io.uploadLog`, `Io.downloadLog` from `io.src`
- [ ] Remove `Encoder.divide` from `encoder.src`
- [x] Remove `Man.header` from `man_loader.src`
- [x] Remove `Log.logFallback` from `log.src` (~~`logLastResort`~~ and ~~`fileTransLog`~~ are `self.*` false positives)
- [x] Remove `Math.levenshtein`, `Math.max`, `Math.min`, `Math.exp` from `math.src`  
- [x] Remove dead `Net.*` helpers: ~~`initInfo`~~, ~~`Net.getRouter`~~ (`Net.firewallAccess` and `Net.addSession` are used via `self.*`)
- [x] ~~Remove `Config._toggle` from `config.src`~~ — FALSE POSITIVE (`self._toggle`)
- [x] ~~Remove `Gui.prompt` from `gui.src`~~ — FALSE POSITIVE (`self.prompt`)
- [x] ~~Remove `Heist.corrupt` from `heist.src`~~ — FALSE POSITIVE (`self.corrupt`)
- [ ] Remove `Farm.decipher`, `Farm.dictionary` from `farm.src`
- [ ] Remove `Proxy.createMapConf` from `proxy.src`
- [ ] Remove `ShellObject.packCrypto` from `shell_object.src` (callers use `Builder.packCrypto` directly)
- [ ] Remove `viewFile` from `attack_dig.src` (L682)
- [x] Consolidate `AgentCore` vs `AgentPlanning` duplicates (5 shared methods) — removed from `agent_util.src`; `promptOnSlow` guard ported into `AgentPlanning._expandSubnet`
- [ ] Verify & consolidate `Exploit.setFlag/clearFlag/hasFlag/packExploit` — bloom filter utilities unused?
