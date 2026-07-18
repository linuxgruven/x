# GreyScript Language Reference

## Overview
GreyScript is the scripting language for Grey Hack game. This reference covers key language features, types, and patterns used in this project.

Source: [greyscript-meta](https://github.com/ayecue/greyscript-meta) - comprehensive metadata library

---

## Core Language Features

### Syntax
- **Comments**: `//` single line
- **Functions**: `functionName = function(arg1, arg2)...end function`
- **Conditionals**: `if...then...else if...else...end if`
- **Loops**: `while...end while`, `for item in list...end for`
- **Range**: `range(start, end)` - inclusive on both ends
- **String interpolation**: `"Hello " + name` or concatenation
- **Self reference**: `self` in methods refers to parent object
- **Null checking**: `if not variable then...` or `if variable then...`
- **Type checking**: `typeof(obj)`, `obj isa type`
- **Index checking**: `hasIndex(map, key)`

### Data Types
- `string` - text
- `number` - integers and floats
- `list` - arrays `[]`
- `map` - dictionaries/objects `{}`
- `null` - null value
- `funcRef` - function reference

### Type Coercion
- `to_int(value)` - convert to integer
- `str(value)` - convert to string
- `split(string, delimiter)` - returns list
- `join(list, delimiter)` - returns string

---

## Game Object Types

### File System
- **file** - file object (inherits from map)
  - `get_content(file)` - read file content
  - `set_content(file, content)` - write file
  - `has_permission(file, "r"|"w"|"x")` - check permissions
  - `path(file)` - get absolute path
  - `name(file)` - get filename
  - `parent(file)` - get parent folder
  - `get_folders(folder)` - list subfolders
  - `get_files(folder)` - list files
  - `delete(file)` - remove file
  - `chmod(file, permissions, recursive)` - change permissions

### Network Objects
- **computer** - computer/server object
  - `host_computer(shell)` - get computer from shell
  - `File(computer, path)` - get file object
  - `create_folder(computer, path, name)` - returns number on success
  - `touch(computer, path, filename)` - create file
  - `show_procs(computer)` - list processes
  - `network_devices(computer)` - get network interfaces
  
- **router** - network router object
  - `get_router(ip)` - get router by IP
  - `used_ports(router)` - list ports
  - `port 0` - router itself (kernel_router service)
  
- **shell** - remote shell access
  - `get_shell` - get current shell (only when pivoted)
  - `connect_service(shell|ip, ip, port, user, pass)` - connect via SSH
  - `host_computer(shell)` - get computer from shell
  - `scp(shell, source_path, dest_path, remote_shell)` - copy files
  - `launch(shell, program_path, arguments)` - execute program
  - `shell.su(password)` - elevate to root (returns string on error)
  - `shell.user` - current username
  
- **port** - service port
  - `port_number(port)` - get port number
  - `is_closed(port)` - check if closed
  - `get_lan_ip(port)` - get LAN IP

### Exploitation Objects
- **metaxploit** - metasploit library
  - `overflow(metaLib, memory, buffer)` - exploit vulnerability
  - Returns: shell, computer, file, or error
  
- **crypto** - cryptography library
  - Used for password operations

---

## Critical Patterns & Gotchas

### Shell Context
```greyscript
// WRONG: get_shell only works when pivoted
shell = get_shell  // Fails if not in remote context

// RIGHT: Use globals.G_main.shell for home shell
shell = globals.G_main.shell  // Always available

// Router chaining: Use Builder.packCOEX for remote router access
z = Builder.packCOEX(fromShell, ip)
router = z.router
metaxploit = z.metaxploit
```

### Type Checking Best Practices
```greyscript
// Check for Error type
if result isa Error then return

// Check for null
if not object then return

// Check type name
if typeof(ex) == "shell" then...
if indexOf(typeof(ex), "shell") != null then...  // Catches ftp-shell too

// Check list
if result isa list then...
if not len(list) then...  // Empty check
```

### Map/Object Patterns
```greyscript
// Check key exists
if hasIndex(map, "key") then...

// Safe access with default
if hasIndex(map, "key") then value = map.key else value = default

// Iteration
for key in map.indexes
  value = map[key]
end for

// File is a map!
file = File(computer, "/etc/passwd")
if hasIndex(file, "some_property") then...  // Valid!
```

### String Operations
```greyscript
// hasIndex works on strings!
if hasIndex(string, "substring") then...  // Check contains

// indexOf for position
pos = indexOf(string, "search")  // Returns null if not found

// Character codes
code("A")  // Get ASCII code
char(65)   // Get character from code
char(10)   // Newline
```

### List Operations
```greyscript
// hasIndex works on lists!
if hasIndex(list, index) then...

// Push/pop
push(list, item)      // Add to end
list.insert(0, item)  // Add to start
list.pop              // Remove from end
list.pull             // Remove from start

// Range
for i in range(0, len(list)-1)  // INCLUSIVE on both ends!
  item = list[i]
end for
```

### Number Operations
```greyscript
// Math functions (via globals in this project)
abs(x)           // Absolute value
floor(x)         // Round down
ceil(x)          // Round up (custom implementation)
round(x)         // Round to nearest
log(x, base)     // Logarithm (base 10 default)
Math.exp(x)      // e^x (custom Taylor series)

// Bitwise operations
bitAnd(a, b)     // AND
bitOr(a, b)      // OR  
bitXor(a, b)     // XOR
```

---

## Common Error Patterns

### Router Operations
```greyscript
// Always check for null/empty extracts
t = Exploit.extractRouter(r)
if not t or not len(t) then continue  // BOTH checks needed!
if t isa Error then continue

// Router port 0 is the router service itself
if m.port_number == 0 then continue  // Skip router, get actual services
```

### Port Connections
```greyscript
// Router uses port 0, SSH uses port 22
// When saving router chains, use port 0
push(data, hop.ip + ":0:" + hop.user + ":" + hop.password)

// When connecting to regular hosts, use port 22
connect_service(shell, ip, 22, user, pass)
```

### File System
```greyscript
// File operations return type varies
result = computer.touch(path, filename)
if typeof(result) == "string" then...  // Error message
if result isa number then...           // Success (1)

// create_folder also returns different types
result = create_folder(computer, path, name)
if not result isa number then...  // Error or null
```

### Shell Results
```greyscript
// su() returns string on failure, nothing on success
suResult = shell.su(password)
if typeof(suResult) == "string" then
  // su failed, still have user-level shell
else
  // su succeeded, now root
end if
```

---

## Project-Specific Patterns

### Exploit Cache Pattern
```greyscript
// Per-operation exploit cache (avoid repeated lookups)
exploitCache = {}
E = lib_name(metaLib) + "_" + version(metaLib)

if hasIndex(exploitCache, E) then
  q = exploitCache[E]
else if hasIndex(globals.G_exploitCache, E) then
  q = globals.G_exploitCache[E].exploits
  exploitCache[E] = q
else
  Exploit.headless(metaLib)
  q = globals.G_exploitCache[E].exploits
  exploitCache[E] = q
end if
```

### IP Deduplication Pattern
```greyscript
// Avoid retrying same IPs (Net.rip can return duplicates)
seen = {}
while true
  ip = Net.rip
  if hasIndex(seen, ip) then continue
  seen[ip] = 1
  // Process unique IP...
end while
```

### Root Password Extraction
```greyscript
// /etc/passwd format: username:hash (if len=2 and hash len=32)
passwdFile = File(computer, "/etc/passwd")
if passwdFile then
  content = get_content(passwdFile)
  lines = split(content, char(10))
  for line in lines
    parts = split(trim(line), ":")
    if len(parts) == 2 and parts[0] == "root" and len(parts[1]) == 32 then
      rootPass = Crack.hash(parts[1])
      if rootPass then
        Shadow.add([ip, rootPass])
        break
      end if
    end if
  end for
end if
```

---

## Performance Considerations

### Bloom Filter (524288-bit)
- 8192 integers (32-bit each)
- 3 hash functions with % 524288 modulo
- Sampling for stats (64 of 8192 integers)
- ~0.1% FPR at 1-2k items, ~1.4% at 5k, ~6% at 10k

### Exploit Processing
- Cache exploits per lib/version to avoid repeated scans
- Use local per-function exploit cache for hot paths
- Skip empty exploit results early
- Break loops when target found

### Router Chaining
- Use Builder.packCOEX for multi-hop to avoid home IP in logs
- Track seen IPs to prevent duplicate attempts
- Early continue on failed steps (don't nest deeply)

---

## Useful References

### Official
- Game: Grey Hack (Steam)
- Meta Library: https://github.com/ayecue/greyscript-meta

### Type Signatures Available
- any, general (globals), string, number, list, map
- file, computer, shell, router, port, service
- metaxploit, crypto, apt-client
- ftp-shell, ftp-computer, ftp-file
- net-session, meta-lib, meta-mail
- blockchain, wallet, coin, sub-wallet
- debug-library, traffic-net, smart-appliance

### Tags
- `method` - object method
- `function` - global function
- `general` - builtin/intrinsic
- `ssh incompatible` - doesn't work over SSH
- `detached` - runs independently
