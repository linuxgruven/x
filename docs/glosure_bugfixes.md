# Glosure Bug Fixes

## 1. `get_shell` Name Conflict

**File:** `src/libs/glosure.src`

**Problem:** The general map had `"get_shell":@get_shell` which exposed the GreyHack built-in `get_shell(user, password)` directly. A wrapper `_glosure_get_shell` calling `Exploit.getShell(sh)` was also present, both using the same key — the built-in overwrote the wrapper.

**Fix:** Renamed the wrapper to `_glosure_exploit_shell` exposed as `"exploit_shell"` in the general map. The built-in `get_shell` was removed from the map entirely. Scripts now call `(exploit_shell sh)`.

---

## 2. `_glosure_get_file` Passing Wrong Meta

**File:** `src/libs/glosure.src`

**Problem:** `_glosure_get_file` was called with a MetaLib object (`tlib`) as its second argument and passed it directly as the `meta` parameter to `Exploit.getFile`. `FileObject.run` reads `meta.public_ip` and `meta.local_ip` for the session prompt — on a MetaLib object these are null/wrong, producing:

```
•[FILE]•[P]••[guest~Router@:MetaxploitLib] [/home/guest]
```

**Root cause chain:**
- `MetaLib` has no `public_ip` or `local_ip` properties (documented API: `lib_name`, `version`, `is_patched`, `overflow`, `debug_tools` only)
- Passing it as `meta` caused `meta.local_ip` to stringify as `"MetaxploitLib"` and `meta.public_ip` to be empty

**Fix:** Wrapper now takes explicit `local_ip` and `public_ip` string arguments and builds the meta map explicitly:

```greyscript
_glosure_get_file=function(fileObj,local_ip,public_ip)
  return Exploit.getFile(fileObj,{"public_ip":public_ip,"local_ip":local_ip})
end function
```

---

## 3. `local_ip` / `public_ip` Not in General Map

**File:** `src/libs/glosure.src`

**Problem:** The GreyHack built-in functions `local_ip(router)` and `public_ip(router)` were not exposed in the Glosure general map. Scripts couldn't call `(local_ip router)` — the symbol was unresolved.

**Fix:** Added both to the general map:

```greyscript
"local_ip":@local_ip,"public_ip":@public_ip,
```

---

## 4. `dot` Operator Can't Access Router Properties

**File:** `src/libs/glosure.src`

**Problem:** The `dot` special form always calls the resolved value as a function (`method()`). Router properties like `local_ip` and `public_ip` are getter properties — calling them as `()` returns null.

Attempting `(dot router 'local_ip')` returned empty string instead of the LAN IP.

**Workaround:** Use the free-function forms `(local_ip router)` and `(public_ip router)` (now in the general map) instead of `dot` for router IP access.

**Note:** `dot` works for methods that take no args and are called via `()`, but not for properties that are direct values or built-in getters.

---

## 5. `try-port` File Branch — Wrong LAN IP for Direct Exploits

**File:** `testing/REPL/meta_remote.src`

**Problem:** `exploit-direct` passes the public IP as both `ip` and `wan_ip` to `try-port`. When a file result is obtained, `ip` (the public IP) was being passed as `local_ip` to `get_file` — producing an invalid session.

**Fix:** Detect the direct exploit case (`ip == wan_ip`) and resolve the router's actual LAN IP:

```clojure
(def flan (if (== ip wan_ip) (local_ip (get_router wan_ip)) ip))
(get_file result flan wan_ip)
```

This mirrors how `Exploit.extract` works — it stores `local_ip(r)` for port 0 (router kernel) and `get_lan_ip(p)` for LAN device ports.

---

## 6. `-e` Flag Type Causing Split-Arg Issues in `repl`

**File:** `src/command/commands/repl.src`

**Problem:** `-e` was a `"store"` type argument, so the game shell's space-splitting caused `repl -e "(+ 1 2)"` to be parsed as `-e` = `"(+ 1 2)"` only if quoted. Without quotes, the expression was split and only the first token was captured.

**Fix:** Changed `-e` to `"flag"` type and joined all `argv.rest` tokens as the expression:

```greyscript
if argv.e then
  opts["eval"]=join(argv.rest," ")
  file=null
  scriptArgs=[]
end if
```

---

## 7. `try-port` Returning File/Computer Results to `exploit_shell`

**File:** `testing/REPL/meta_remote.src`

**Problem:** `try-port` returned the raw result for all exploit types. The caller passed all non-null returns to `exploit_shell`, which failed on file/computer objects.

**Fix:** `file` and `computer` branches handle their result in-place and return `null`. Only `shell` type propagates a return value back to the caller.

---

## 8. `$` Path Expansion Using `string.replace` Broken

**File:** `src/libs/glosure.src`

**Problem:** `repl $/test` silently failed to find the file. `string.replace("$", home)` treats `$` as a regex end-of-string anchor in GreyScript, so it appended the home path to the end of the string instead of substituting `$`:

```
$/test  →  $/test/home/tux   (wrong)
```

**Fix:** Changed both the file path and `-p` prefix expansion to use `[0]=="$"` slice:

```greyscript
// Before (broken):
if indexOf(file,"$")!=null then file=file.replace("$",path(Obj.user.home))

// After (correct):
if file[0]=="$" then file=path(Obj.user.home)+file[1:]
```
