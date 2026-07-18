# Bash Engine Refactor Plan

## Overview

The bash engine works well but has grown organically to **5,691 lines** across 5 files with **37 command handlers** and **44 builtin functions**. The naming is inconsistent, the main dispatch file is 2,337 lines, and the scripting syntax is more verbose than it needs to be.

**Goal:** Clean, logical organization. Simpler syntax. Same functionality.

---

## Current State

### File Sizes
| File | Lines | Purpose |
|------|-------|---------|
| bash.src | 534 | Config, lists, variable mgmt, input prompts |
| bash_commands.src | 2,337 | Preprocessing, arithmetic, **37 command handlers** |
| bash_parser.src | 910 | Tokenizer, AST parser |
| bash_executor.src | 822 | Control flow, loops, conditionals |
| bash_builtins.src | 1,088 | 44 builtin function evaluators |
| **Total** | **5,691** | |

### Pain Points

1. **bash_commands.src is a monolith** — preprocessing, arithmetic, string concat, set_var processing (400+ lines), AND all 37 command handlers in one massive `_exec()` function
2. **Naming is ad-hoc** — `bash_get_ports` vs `ping_host` vs `port_open` vs `list_processes` vs `can_write`
3. **Dual command pattern is confusing** — `bash_scanner` (prints) vs `bash_get_ports` (returns data) are two separate commands for the same thing
4. **set_var can't capture commands with args** — `set_var(ports, bash_get_ports 1.2.3.4)` stores the literal string instead of executing. Only no-arg commands (`bash_random`, `bash_pwd`, `bash_whoami`, `bash_whatami`) work
5. **Verbose scripting syntax** — `bash_print`, `set_var(x, ...)`, `get_var(x)` is a lot of typing for simple operations
6. **Text-eating bugs** — `process()` matches builtin names anywhere in strings via `indexOf`, causing printTip/printNote text to get evaluated

---

## Phase 1: New Naming Convention

### Prefix System — LOCKED

| Prefix | Scope | Dispatch | Example |
|--------|-------|----------|---------|
| `_` | Bash core (high frequency) | Core table | `_print`, `_setvar`, `_sleep` |
| `_fs_` | File system operations | File table | `_fs_read`, `_fs_write`, `_fs_cd` |
| `_net_` | Network operations | Network table | `_net_ports`, `_net_ping`, `_net_devices` |
| `_sys_` | System operations | System table | `_sys_whoami`, `_sys_procs`, `_sys_kill` |
| `__` | x framework (attack tools) | x dispatch | `__exploit`, `__crack`, `__airmon` |

Routing:
```
if cmd starts with "__"    → x handler table
if cmd starts with "_net_" → network table
if cmd starts with "_sys_" → system table
if cmd starts with "_fs_"  → file table
if cmd starts with "_"     → core table
```
| `__` | x framework (attack tools, exploits) | `__exploit`, `__crack`, `__airmon` |

Two tiers. Simple. `_` is bash (a fully capable shell with networking), `__` is x (the attack framework that bash passes `Obj` to).

Bash handles: printing, variables, control flow, file I/O, networking, scanning, processes.
x handles: exploits, password cracking, aircrack, custom attack chains — things that need the full Obj context.

### Command Rename Map

#### Output (`_`)
| Current | New | Notes |
|---------|-----|-------|
| `bash_print` | `_print` | Queued output |
| `bash_print_now` | `_printnow` | Immediate output |

#### Variables (`_`)
| Current | New | Notes |
|---------|-----|-------|
| `set_var(name, val)` | `_setvar(name, val)` | |
| `get_var(name)` | `_getvar(name)` | Consider `$name` shorthand later |
| `push_var(list, val)` | `_push(list, val)` | |
| `pop_var(list)` | `_pop(list)` | |
| `pull_var(list, idx)` | `_pull(list, idx)` | |
| `len_var(list)` | `_len(list)` | |
| `in_var(list, val)` | `_in(list, val)` | |

#### Control (`_`)
| Current | New | Notes |
|---------|-----|-------|
| `sleep n` | `_sleep(n)` | |
| `exit` | `_exit` | |
| `bash_home` | `_home` | |

#### File System (`_` — core bash operations)
| Current | New | Notes |
|---------|-----|-------|
| `bash_read /path` | `_read(path)` | |
| `bash_view /path` | `_view(path)` | |
| `bash_write /path content` | `_write(path, content)` | |
| `bash_mkdir /path` | `_mkdir(path)` | |
| `bash_cd /path` | `_cd(path)` | |
| `bash_pwd` | `_pwd()` | |
| `bash_find /path pattern` | `_find(path, pattern)` | |

#### Network / Recon (`_` — bash shell networking)
| Current | New | Notes |
|---------|-----|-------|
| `bash_scanner` / `bash_get_ports` | `_ports(ip)` | Unified: prints or returns (see Phase 2) |
| `ping_host ip` | `_ping(ip)` | Returns 1/0 |
| `port_open ip port` | `_port(ip, port)` | Check single port |
| `bash_lan_devices` / `bash_get_lan_devices` | `_devices(ip)` | Unified |
| `bash_router_info` / `bash_get_router_info` | `_router(ip)` | Unified |
| `bash_device_ports` / `bash_get_device_ports` | `_devports(router, device)` | Unified |
| `bash_firewall_rules` / `bash_get_firewall_rules` | `_fwrules(ip)` | Unified |
| `bash_random` | `_random()` | Random router IP |

#### File Transfer (`_` — bash shell operations)
| Current | New | Notes |
|---------|-----|-------|
| `bash_put src dst` | `_put(src, dst)` | Upload to remote |
| `bash_get src dst` | `_get(src, dst)` | Download from remote |

#### System (`_` — bash shell system ops)
| Current | New | Notes |
|---------|-----|-------|
| `bash_whoami` | `_whoami()` | |
| `bash_whatami` | `_whatami()` | |
| `list_processes` | `_procs()` | |
| `kill_process pid` | `_kill(pid)` | |
| `can_write path` | `_canwrite(path)` | |
| `can_execute path` | `_canexec(path)` | |

#### x Framework (`__` — attack tools, needs Obj)
| Current | New | Notes |
|---------|-----|-------|
| (future) | `__exploit(ip, port, lib)` | Run exploit chain |
| (future) | `__crack(ip, port)` | Password cracking |
| (future) | `__airmon(bssid)` | Wireless monitoring |
| (future) | `__aireplay(bssid)` | Wireless replay |
| (future) | `__aircrack(path)` | Crack captured handshake |

**Note:** Most x functions currently print output and don't return values standalone.
BUT — **when piped, they DO return values** via `PIPE_MODE`. The pipe system already
sets `globals.G_pipe.PIPE_MODE=true` which tells commands to return data instead of printing.

The `_set` capture mechanism simply reuses `PIPE_MODE`:
```
// In _set processing — same mechanism as pipe:
globals.G_pipe.PIPE_MODE = true     // tell command to return, not print
result = _exec(Obj, cmd)
globals.G_pipe.PIPE_MODE = false    // restore
varValue = result
```

**Zero changes to x functions needed.** They already respect `PIPE_MODE`.
The `__` wrapper layer + `_set` capture = free.

---

## Phase 2: Unify Print vs Return (Boolean Pattern)

**The core insight:** Instead of having paired commands (`bash_scanner` prints, `bash_get_ports` returns), use **one command** that does both — **prints by default, returns when captured**.

This applies to ALL commands: `_` bash commands AND `__` x framework commands.

### Convention
- `_ports(ip)` — **prints** formatted output (default, standalone)
- `_setvar(p, _ports(ip))` — **returns** data (captured in `_setvar`)
- `__exploit(ip, port)` — **prints** exploit output (standalone)
- `_setvar(result, __exploit(ip, port))` — **returns** exploit result map (captured)

### How It Works in the Engine
Reuses the existing `PIPE_MODE` mechanism. When piped, commands already return
data instead of printing. `_set` just flips the same flag:

```
// In _setvar processing (set_var replacement):
// Detect command call, enable PIPE_MODE to capture return value
globals.G_pipe.PIPE_MODE = true
cmd = _prepareCommand(varValue, false, Obj)
result = _exec(Obj, cmd, false)
globals.G_pipe.PIPE_MODE = false
if result != null then varValue = result
```

No boolean parameter needed. No function rewrites. No `returnData` flag.
Commands already know how to return data — `PIPE_MODE` is the switch.

### This Solves Everything
- **Bash `_` commands** — `_setvar(p, _ports(ip))` flips PIPE_MODE, gets port list
- **x `__` commands** — `_setvar(shell, __exploit(ip, 22))` flips PIPE_MODE, gets shell object
- **Standalone calls** — PIPE_MODE stays off, commands print as usual
- **Piped calls** — pipe system already sets PIPE_MODE, works as before

This eliminates **5 duplicate command pairs**:
- `bash_scanner` / `bash_get_ports` → `_ports`
- `bash_lan_devices` / `bash_get_lan_devices` → `_devices`
- `bash_router_info` / `bash_get_router_info` → `_router`
- `bash_device_ports` / `bash_get_device_ports` → `_devports`
- `bash_firewall_rules` / `bash_get_firewall_rules` → `_fwrules`

### Engine Change for set_var + Command Capture
In set_var processing, after checking `_bashCmds` (exact match no-arg), add:

```
// Check if varValue matches "commandName arg1 arg2..." pattern
// Split by space, check if first token is a known command
if typeof(varValue)=="string" then
  tokens = split(varValue, " ")
  if len(tokens) >= 1 then
    cmdName = tokens[0]
    if cmdName is in known_returnable_commands then
      cmd = _prepareCommand(varValue, false, Obj)
      result = _exec(Obj, cmd, false)
      if result != null and result != false then
        varValue = result
      end if
    end if
  end if
end if
```

**Known returnable commands** (new list `_returnCmds`):
```
["_ports","_ping","_port","_devices","_router",
 "_devports","_fwrules","_random","_procs",
 "_whoami","_whatami","_canwrite","_canexec"]
```

---

## Phase 3: Split bash_commands.src

Break the 2,337-line monolith into logical modules:

### New File Layout
```
src/system/
├── bash.src              (~400)  Config, lists, variable mgmt
├── bash_parser.src       (~910)  Tokenizer, AST (unchanged)
├── bash_executor.src     (~822)  Control flow (unchanged)
├── bash_builtins.src     (~1088) Builtin functions (unchanged)
├── bash_preprocess.src   (~500)  NEW: process(), _evalArithmetic,
│                                  _evalStringConcat, _set logic
├── bash_dispatch.src     (~200)  NEW: _exec() shell, _prepareCommand,
│                                  chain/pipe handling, dispatch table
├── bash_cmd_core.src     (~150)  NEW: _ commands — _print, _sleep,
│                                  _exit, _home, _set, _get, _push, etc.
├── bash_cmd_fs.src       (~300)  NEW: _ commands — _read, _write, _view,
│                                  _mkdir, _cd, _pwd, _find, _put, _get
├── bash_cmd_net.src      (~400)  NEW: _ commands — _ports, _ping,
│                                  _port, _devices, _router, _fwrules,
│                                  _devports, _random
├── bash_cmd_sys.src      (~150)  NEW: _ commands — _whoami, _whatami,
│                                  _procs, _kill, _canwrite, _canexec
└── bash_cmd_x.src        (~???)  NEW: __ commands — future x framework
│                                  __exploit, __crack, __airmon, etc.
│                                  Receives Obj from bash dispatch.
```

### Dispatch Table Pattern
Instead of 37 `if cmd.name=="xxx"` blocks chained in one function, use a dispatch map:

```
_handlers = {}
_handlers["_ports"] = @_handlePorts
_handlers["_ping"]  = @_handlePing
_handlers["_print"]  = @_handlePrint
// ... etc
// x framework commands get Obj passed through
_handlers["__exploit"] = @_handleXExploit

_exec:
  handler = _handlers[cmd.name]
  if handler then return handler(Obj, cmd)
  // fallback to user funcs, command table
```

This makes adding new commands trivial and keeps `_exec()` under 50 lines.

---

## Phase 4: Simplify Scripting Syntax

### Short Variable Syntax (Future)
```
// Current
set_var(x, 10)
bash_print Value is get_var(x)

// New
_setvar(x, 10)
_print Value is _getvar(x)

// Future shorthand (optional)
$x = 10
_print Value is $x
```

### Parenthesized Calls Everywhere
Currently `_varCmds` handles `set_var(...)` syntax. Extend to all commands:
```
// Both work:
_ports 1.2.3.4            // space-separated (backwards compat)
_ports(1.2.3.4)           // parenthesized (cleaner)
```

### Function Definition (No Change Needed)
```
func myFunc(arg1, arg2)
  // ...
  return_value result
endfunc
```
The `func/endfunc` syntax is already clean.

---

## Phase 5: Backward Compatibility

### Alias Layer
Keep old names working via aliases during transition:

```
_aliases = {}
_aliases["bash_print"] = "_print"
_aliases["set_var"] = "_setvar"
_aliases["get_var"] = "_getvar"
_aliases["bash_get_ports"] = "_ports"
_aliases["ping_host"] = "_ping"
// ... all old names map to new
```

In `_prepareCommand`, resolve aliases before dispatch:
```
if _aliases.hasIndex(cmd.name) then
  cmd.name = _aliases[cmd.name]
end if
```

### Deprecation Strategy
1. **v1.0:** Both old and new names work. Old names print deprecation warning (once per session)
2. **v1.1:** Old names still work, no warning (silent alias)
3. **v2.0:** Remove aliases, old names error with "did you mean _ports?"

---

## Phase 6: Fix Known Bugs During Refactor

These get fixed as part of the restructuring:

| Bug | Fix Integrated In |
|-----|-------------------|
| set_var can't capture commands with args | Phase 2: `_returnCmds` list + dispatch |
| process() text-eating (indexOf matches anywhere) | Phase 3: preprocess rewrite with word-boundary checks |
| Dual command confusion | Phase 2: unified commands with bool |
| _bashCmds hardcoded no-arg list | Phase 2: replaced by `_returnCmds` |

---

## Execution Order

| Step | Phase | Risk | Dependencies |
|------|-------|------|-------------|
| 1 | Create `_returnCmds` list, fix set_var capture | Low | None |
| 2 | Split bash_commands.src into modules | Medium | Step 1 |
| 3 | Add dispatch table | Medium | Step 2 |
| 4 | Rename commands (new names) | High | Step 3 |
| 5 | Add alias layer for old names | Low | Step 4 |
| 6 | Update all .src scripts to new names | High | Step 5 |
| 7 | Update learn_bash.src & tests | Medium | Step 6 |
| 8 | Update man pages & docs | Low | Step 7 |
| 9 | Remove aliases (v2.0) | Low | After stabilization |

### Testing Strategy
- **After each step:** Run return_test.src (114 tests), debug1-4.src, full learn_bash.src
- **Regression gate:** No step proceeds until previous step is ALL PASS
- **New test file:** `refactor_test.src` — validates old names still work via aliases AND new names work

---

## Command Count Summary

| Category | Current | After Refactor | Change |
|----------|---------|----------------|--------|
| Output | 2 | 2 | `_print`, `_printnow` |
| Variables | 7 | 7 | `_setvar`, `_getvar`, `_push`, `_pop`, `_pull`, `_len`, `_in` |
| File System | 7 | 9 | `_read`, `_write`, `_view`, `_mkdir`, `_cd`, `_pwd`, `_find`, `_put`, `_get` |
| Network | 12 | **7** | `_ports`, `_ping`, `_port`, `_devices`, `_router`, `_devports`, `_fwrules` |
| System | 4 | 4 | `_whoami`, `_whatami`, `_procs`, `_kill` |
| Control | 3 | 3 | `_sleep`, `_exit`, `_home` |
| Permissions | 2 | 2 | `_canwrite`, `_canexec` |
| Other | 1 | 1 | `_random` |
| x Framework | 0 | (future) | `__exploit`, `__crack`, `__airmon`, etc. |
| **Total bash** | **38** | **35** | -3 (merged 5 dupes, clean split) |

---

## Open Questions

1. **`$x` shorthand for variables?** — Would require parser changes. Big win for usability but significant work.
2. **Pipe syntax** — Currently `cmd1 | cmd2`. Keep as-is or formalize?
3. **Error handling** — Add `try/catch` or keep `if _getvar(result)` pattern?
4. **Color helpers** — 19 color functions (`orange()`, `cyan()`, etc.). Keep as builtin functions or move to `_color(name, text)` unified helper?
5. **x framework commands** — `__exploit`, `__crack`, `__airmon` etc. are future. Bash dispatches to x by passing `Obj`. Define the `__` handler interface now so x commands plug in cleanly later.
