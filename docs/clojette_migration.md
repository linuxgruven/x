# Glosure → Clojette Migration Plan

## Status: PLANNING

**Date:** 2026-03-24
**Note from Clojette author:** There are known crashes being fixed. Minification can introduce issues — build from `src/` files if problems arise.

---

## Why Migrate?

### Pros of Clojette over Glosure

- **Macros** — Full `defmacro` + quasiquote (`\``, `~`, `~@`) + `gensym`. Users can extend the language itself. Glosure has basic macros but Clojette's are far more capable.
- **Threading macros** — `->` and `->>` turn deeply nested interop calls from unreadable to clean:
  ```clojure
  ;; Glosure:  (dot (dot (dot (get_shell) 'host_computer') 'File' path) 'get_content')
  ;; Clojette: (-> (get_shell) (.host_computer) (.File path) (.get_content))
  ```
- **Error handling** — `try/catch/throw` with stack traces. Glosure has none — errors propagate via `Error.set` from the x shell.
- **Namespaces** — `ns` + cross-namespace `tools/helper` syntax. Glosure is flat global scope.
- **Cleaner interop** — `.method obj args` dot-prefix syntax vs Glosure's verbose `(dot obj 'method' args)`.
- **Richer stdlib** — 50+ functions (map, filter, reduce, every?, some?, flatten, take, drop, etc.) vs Glosure's minimal set.
- **Standard Clojure syntax** — Double-quoted strings, `[vectors]`, `{maps}`, `:keywords`. Easier for anyone who knows Clojure.
- **loop/recur** — Proper tail-call-safe looping. Glosure uses `(loop body condition)` which is just a while.
- **Better docs** — 911-line language reference vs a short README.
- **Closures with lexical scoping** — `let` bindings, proper `fn` closures with environment chains.
- **Control flow** — `cond`, `when`, `unless`, `and`/`or` short-circuit, `while` macro.

### Cons / Risks

- **Clojette is young** — Author warns of known crashes still being fixed. We're adopting early.
- **Minification / x build obfuscation** — Two separate problems here:
  1. **Clojette's own minifier** — Author says their minified `all.gs` can introduce bugs. Solution: build from their `src/` files instead.
  2. **x's build system** — x uses aggressive obfuscation during build: variable renaming to Unicode chars (Ј, ڔ, Ё, etc.), comment stripping, whitespace collapsing, quote doubling. This will mangle Clojette's internals — function names like `eval`, `parse`, `globalEnv`, `makeEnv`, `lispError` will all get renamed. Clojette's code references these by name internally and should survive renaming IF the compiler is consistent (same name → same replacement everywhere). But any string-based lookups like `globalEnv.locals["macros"]` or `op["classID"]` use string keys that WON'T be renamed, so those should be safe. The real risk is if the compiler breaks on Clojette's coding patterns (e.g., deeply nested closures, the `@` dereference patterns, or the `__runtimeTag__` function-as-identity trick). **Needs live testing after build.**
- **Larger codebase** — Clojette is 5 files (~1500+ lines of GreyScript) + 2 `.clj` stdlib files vs Glosure's single ~700 line file. More `import_code` budget used.
- **GPL v3 license** — Glosure is MIT. Clojette is GPLv3 with a linking exception. The exception should cover our use case (importing/linking) but worth noting.
- **No `x` command dispatcher** — Glosure has `(x 'cmd')` baked into the evaluator. Clojette has no equivalent — we need to build it.
- **No `glosure` keyword** — Glosure can create native GreyScript funcRefs via `(glosure (args) body)` for passing callbacks to GreyHack APIs. Clojette has no equivalent — `fn` creates Clojette closures, not funcRefs.
- **Breaking change for scripts** — All existing `.src` scripts in `testing/REPL/` use Glosure syntax and need rewriting.
- **Different falsy semantics** — Clojette inherits MiniScript's falsy (0, "", false, null are falsy). Same as Glosure in practice, but differs from standard Clojure where only `false`/`nil` are falsy.
- **No `exec` keyword** — Glosure's `(exec 'string')` evaluates a string as code. Clojette has `eval` + `parse` as separate functions, so equivalent is `(eval (parse "string"))`.

---

## Gotchas

### 1. The `x` Command Dispatcher — CRITICAL

Glosure has a special form `x` baked into the evaluator:
```clojure
;; Glosure: get a reference to an x shell command
((x 'scan') obj target-ip)
```
This looks up `Obj.commands[name]` and returns a `{classID:"native", ref:@fn}` wrapper. Clojette has **nothing like this**. We need to either:

- **Option A:** Add an `x` special form to Clojette's `eval` function (invasive — modifies upstream code)
- **Option B:** Register a native `x` function in the interop layer that does the lookup (cleaner — keeps Clojette stock)
- **Option C:** Register every command individually into the Clojette env (explosion of bindings)

**Recommendation:** Option B. Register `x` as a native function that takes a command name and returns the funcRef. But there's a subtlety — Glosure's native dispatch uses `nref(argv)` passing a list, while Clojette's native call convention uses positional args. We need to verify how Clojette calls funcRefs.

### 2. Native funcRef Calling Convention

Glosure's `classID:"native"` objects are called with `nref(argv)` — the entire argument list as a single list parameter. The x shell commands (`Command.scan`, `Command.ls`, etc.) take `(Obj, argv)` — an object context and an argv list.

Clojette calls funcRefs with positional args: `fn(args[0], args[1], ...)` up to 5. So the `x` bridge function needs to wrap each command to accept positional Clojette args and repack them to `command(Obj, [args])`.

### 3. The `glosure` Keyword (GreyScript funcRef creation)

Glosure's `(glosure (x) (* x x))` creates an actual GreyScript `funcRef` — needed when passing callbacks to native GreyHack APIs that expect real functions (like `.sort(key)`). Clojette's `(fn ...)` creates internal closure maps, not funcRefs.

Clojette does NOT have an equivalent. **This is a gap.** Workaround: expose a `make-native` helper that wraps a Clojette fn into a funcRef via the same glosure-style arity dispatch pattern.

### 4. String Quoting — ALL Scripts Break

Glosure uses single-quoted strings: `'hello'`
Clojette uses double-quoted strings: `"hello"`

Every existing script (`meta_remote.src`, `meta_local.src`) needs full string literal conversion. This is mechanical but tedious.

### 5. `begin` → `do`

Glosure uses `(begin expr1 expr2 ...)` for sequencing.
Clojette uses `(do expr1 expr2 ...)`.

All multi-expression bodies in existing scripts use `begin`.

### 6. `defun` → `defn`

Glosure STL macro: `(defun name (args) body)`
Clojette macro: `(defn name [args] body1 body2 ...)`

Note the `[vector]` syntax for params in Clojette vs `(list)` in Glosure.

### 7. `array` / `dict` → `[vectors]` / `{maps}` or `hash-map`

Glosure: `(array 1 2 3)` and `(dict 'k' 'v')`
Clojette: `[1 2 3]` and `(hash-map "k" "v")` — though `(array ...)` does work in Clojette (it's a special form).

### 8. `dot` → `.method` Syntax

Glosure: `(dot obj 'method' arg1 arg2)`
Clojette: `(.method obj arg1 arg2)`

The method name moves from a string argument to a dot-prefixed symbol. This changes every interop call.

### 9. `at` / `set` → `get` / `assoc`

Glosure: `(at obj 'key')` and `(set obj 'key' value)`
Clojette: `(get obj "key")` and `(assoc obj "key" value)` — but `assoc` returns a NEW map, doesn't mutate. For mutation, would need a native helper or `set!`.

**This is a semantic difference.** Glosure's `(set obj 'key' value)` mutates in place. Clojette's `assoc` is functional. The meta scripts use `(set shell 0 result)` to mutate a list — this pattern needs a replacement (native `set!` or a mutable helper).

### 10. `==` / `!=` → `=` / `not=`

Glosure: `(== a b)`, `(!= a b)`
Clojette: `(= a b)`, `(not= a b)`

### 11. `foreach` → No Direct Equivalent

Glosure: `(foreach key value collection body)` — iterates with both key and value.
Clojette: `(map ...)` or `(loop ... (recur ...))` — no built-in foreach with index access.

We'd need a `doseq`-style macro or use `(loop [i 0] ... (recur (inc i)))`.

### 12. `|` / `&` Boolean Operators → `or` / `and`

Glosure: `(| cond1 cond2)`, `(& cond1 cond2)`
Clojette: `(or cond1 cond2)`, `(and cond1 cond2)`

### 13. `to_int` Not in Clojette

Glosure exposes `to_int` from GreyScript. Clojette has `val` (native). May need to register `to_int` as a native or alias `val`.

### 14. `import_code` Budget

Clojette is 5 `.gs` files + 2 `.clj` files. Currently Glosure is 1 file imported via `import_code`. The Clojette files will need to be concatenated or imported sequentially. GreyHack has a hard limit on total `import_code` size — need to verify we have budget.

### 15. Clojette's `import` Uses `get_shell.host_computer`

Clojette's `(import "/path/file.clj")` in `clojette-core.gs` calls `get_shell.host_computer` directly — not through Obj or session context. This means it always reads from the LOCAL machine, even during a proxy/SSH session. For our use case this is probably fine (stdlib is local), but worth knowing.

### 16. Error Propagation Mismatch

Glosure errors use x shell's `Error.set()` which prints and returns an Error object that the x shell understands. Clojette errors use `lispError()` returning `{classID:"error", __tag__:@__runtimeTag__, message:msg}` — a different error type. The REPL wrapper needs to handle Clojette errors and optionally bridge them to `Error.set` for x shell compatibility.

### 17. `_` Result Binding

Both Glosure and Clojette REPL bind last result to `_`. Glosure does this via `env.__local["_"]=@result`. Our wrapper needs to replicate this in the Clojette env.

### 18. REPL Prompt

Glosure uses `Gui.replPrompt` (x shell's styled prompt). Clojette's built-in REPL uses `user_input("Clojette> ")`. We need to write our own REPL loop using `Gui.replPrompt` instead of using Clojette's built-in `repl()`.

### 19. x Build Obfuscation — CRITICAL

The x build system does aggressive variable renaming (to Unicode chars like Ј, ڔ, Ё) + comment stripping + whitespace collapsing + quote doubling (`"` → `""`). This is separate from Clojette's own minifier.

**What should survive:**
- String keys in maps (`"classID"`, `"error"`, `"fn"`, `"args"`, `"body"`, `"env"`, `"__tag__"`) — these are string literals, not variable names. The obfuscator won't touch them.
- Clojette's internal variable names (`globalEnv`, `makeEnv`, `eval`, `parse`, etc.) — IF the compiler consistently renames all occurrences of the same variable to the same Unicode replacement. Since Glosure already survives the build, this pattern works.
- `@` dereference operators — syntactic, not name-based.

**What could break:**
- **`__runtimeTag__`** — This is a function used as an identity tag. Its NAME doesn't matter (it's compared by reference via `@`), but the variable holding it needs consistent renaming. Should be fine if compiler is consistent.
- **Quote doubling in embedded `.clj` strings** — If macros.clj + stdlib.clj content is embedded as a GreyScript string literal (like Glosure's `stl` string), the build's quote doubling will turn `"` inside Clojette code strings into `""`. Since Clojette uses `"` for string literals (unlike Glosure which uses `'`), ALL string literals inside embedded `.clj` code will be corrupted by the build. **This is the biggest risk.**
- **Deeply nested closures** — Clojette uses a LOT of closures (the stdlib is 500+ lines of nested functions). If the obfuscator has scope-tracking bugs, these could get mangled.
- **`eval` and `parse` as variable names** — These shadow GreyScript builtins. The obfuscator needs to handle this correctly. Glosure doesn't shadow `eval` (it uses `Glosure.eval`), so this is a new pattern for the build.

**Mitigation for the quote-doubling problem:**
- Option 1: Store `.clj` stdlib on the filesystem and load at runtime via `(import)` — avoids embedding in GreyScript strings entirely.
- Option 2: Use single-quote delimiters in the embedded string and have Clojette convert them. Ugly.
- Option 3: Escape the embedded string content to use a different delimiter pattern that survives build.
- **Best option:** Runtime loading from `/lib/clojette/macros.clj` and `/lib/clojette/stdlib.clj` — this is what Clojette's own `clojette-repl.gs` already does.

---

## Architecture Decision: How to Embed Clojette

### Option A: Concatenate All Clojette src/ Files into One .src

Combine `clojette-env.gs` + `clojette-stdlib.gs` + `clojette-core.gs` + `clojette-interop.gs` into a single `src/libs/clojette.src`, then append our x-shell bridge code. Strip the Clojette REPL (`clojette-repl.gs`) — we write our own.

**Pros:** Single `import_code`, mirrors current Glosure structure, easy to manage.
**Cons:** Large file. Updates from upstream require re-merging.

### Option B: Multiple import_code Calls

Keep Clojette files separate, import each one in sequence in `main.src`.

**Pros:** Cleaner separation, easier upstream updates.
**Cons:** Uses more `import_code` slots, more file management in GreyHack.

### Option C: Build from src/ into single file at dev time

Use a build script to concatenate Clojette src/ files + our bridge into one `.src` file. Keep originals in a `vendor/` folder for reference.

**Pros:** Best of both worlds — clean dev, single import at runtime.
**Cons:** Extra build step.

**Recommendation:** Option A for now (single concatenated file). We can restructure later.

---

## Files to Modify

| File | Change |
|------|--------|
| `src/libs/glosure.src` | **Replace** with Clojette sources + x bridge |
| `src/command/commands/repl.src` | Rewrite to init Clojette env + run REPL |
| `main.src` line 201 | Update `import_code` path |
| `man/repl.src` | Rewrite man page for Clojette syntax |
| `testing/REPL/meta_remote.src` | Convert from Glosure → Clojette syntax |
| `testing/REPL/meta_local.src` | Convert from Glosure → Clojette syntax |
| `testing/REPL/README.md` | Update for Clojette |
| `testing/REPL/Tutorial.md` | Replace with Clojette tutorial (or link to DOCS.md) |
| `testing/REPL/x_repl_guide.md` | Rewrite for Clojette syntax + x bridge |
| `docs/glosure_bugfixes.md` | Archive or update |

---

## Implementation Order

1. **Build clojette.src** — Concatenate Clojette src/ files (env, stdlib, core, interop) into single file. Strip license duplication. Strip built-in REPL.
2. **Write x bridge** — Append to clojette.src: register `Obj`, commands map, exploit helpers, `x` command dispatcher, mutable `set-at!` helper as Clojette natives.
3. **Write REPL wrapper** — New `Clojette.run()` entry point matching Glosure's signature `(Obj, commands, file, scriptArgs, opts)`. Uses `Gui.replPrompt`. Handles `-e`, `-i`, `-p` flags. Binds `_` after each eval.
4. **Boot stdlib** — Load `macros.clj` + `stdlib.clj` content at startup (embed as strings or use import).
5. **Update repl.src** — Point to new `Clojette.run()`.
6. **Update main.src** — Change import path.
7. **Test basic REPL** — Arithmetic, string ops, interop calls, `x` commands.
8. **Convert meta scripts** — Rewrite `meta_remote.src` and `meta_local.src` in Clojette syntax.
9. **Update docs** — Man page, guides, README.
10. **Regression test** — Run meta scripts against live targets, verify exploit flow end-to-end.

---

## Syntax Conversion Cheat Sheet

| Glosure | Clojette | Notes |
|---------|----------|-------|
| `'hello'` | `"hello"` | String literals |
| `(begin ...)` | `(do ...)` | Sequencing |
| `(defun name (args) body)` | `(defn name [args] body)` | Named functions |
| `(lambda (args) body)` | `(fn [args] body)` | Anonymous functions |
| `(array 1 2 3)` | `[1 2 3]` | List/vector literals |
| `(dict 'k' v)` | `(hash-map "k" v)` | Map literals |
| `(dot obj 'method' arg)` | `(.method obj arg)` | Method calls |
| `(at obj 'key')` | `(get obj "key")` | Property access |
| `(set obj 'key' val)` | `(set-at! obj "key" val)` | Mutation (custom) |
| `(x 'cmd')` | `(x "cmd")` | x dispatch (custom) |
| `(== a b)` | `(= a b)` | Equality |
| `(!= a b)` | `(not= a b)` | Inequality |
| `(\| a b)` | `(or a b)` | Boolean OR |
| `(& a b)` | `(and a b)` | Boolean AND |
| `(! a)` | `(not a)` | Boolean NOT |
| `(foreach k v coll body)` | `(doseq ...)` or loop | Iteration (custom macro needed) |
| `(defmacro n (a) (s) body)` | `(defmacro n [a] body)` | Macro definition |
| `(exec 'code')` | `(eval (parse "code"))` | Eval string as code |
| `(context)` | N/A | Get local env (no equivalent) |
| `(glosure (args) body)` | `(make-native (fn [args] body))` | Native funcRef (custom) |

---

## Open Questions

1. **import_code budget** — Do we have room for the larger Clojette codebase? Need to check current total.
2. **`glosure` keyword replacement** — How often do meta scripts need native funcRefs? If rarely, we can defer `make-native`.
3. **Clojette crash bugs** — Author says some exist. Should we pin to a specific commit or track main?
4. **Stdlib loading** — Embed macros.clj + stdlib.clj as GreyScript strings (like Glosure's `stl`)? Or read from filesystem at runtime? **The build's quote-doubling strongly favors runtime loading from filesystem** — embedding as strings will corrupt all `"` inside Clojette code.
5. **Backward compat** — Do we keep Glosure available as a fallback during transition? (e.g. `repl --glosure`)
6. **Build testing** — Need to do a test build early (before converting scripts) to verify Clojette survives x's obfuscation pipeline intact. If it doesn't, we may need to negotiate exclusion rules with the build system, or restructure Clojette's code to avoid the problematic patterns.
7. **`eval`/`parse` shadowing** — Clojette defines `eval` and `parse` as top-level variables that shadow GreyScript builtins. Does x's compiler handle this correctly? Glosure namespaces everything under `Glosure.eval` / `Glosure.reader` so this wasn't an issue before.
