# X Database System — Full Technical Write-Up

## Table of Contents

1. [Overview](#overview)
2. [On-Disk Structure](#on-disk-structure)
3. [The Cyrillic-Encoded Record Format](#the-cyrillic-encoded-record-format)
4. [The Three Trees — String Deduplication](#the-three-trees--string-deduplication)
5. [The Bloom Filter](#the-bloom-filter)
6. [Creating a New Database File](#creating-a-new-database-file)
7. [Loading the Database (Boot Sequence)](#loading-the-database-boot-sequence)
8. [Scanning — Discovering New Exploits](#scanning--discovering-new-exploits)
9. [Updating the Database](#updating-the-database)
10. [Writing / Saving to Disk](#writing--saving-to-disk)
11. [Defragmentation](#defragmentation)
12. [The In-Memory Cache](#the-in-memory-cache)
13. [Bitwise Flags](#bitwise-flags)
14. [File Size Management](#file-size-management)
15. [Data Flow Diagram](#data-flow-diagram)
16. [Key Gotchas & Limitations](#key-gotchas--limitations)

---

## Overview

X's database is a custom exploit-tracking system built for Grey Hack. It stores information about every library vulnerability X has ever discovered: the memory address, the unsafe check string, the exploit type, the user privilege level, and any 0-day requirement references.

Because Grey Hack imposes strict file-size limits and has no built-in database engine, X implements its own:

- **String deduplication** via three "tree" indices (stree, mtree, rtree)
- **Compact binary-like encoding** using Cyrillic delimiters
- **A bloom filter** for fast "have we seen this library?" checks
- **Bitwise flags** for cache state management
- **Numbered file sharding** to stay under per-file size limits

---

## On-Disk Structure

After installation, the exploit database lives at `~/payload/exploits/` with this layout:

```
~/payload/exploits/
├── bloom                    # Bloom filter (comma-separated integers)
├── stree/                   # String tree (unsafe check values)
│   ├── 1
│   ├── 2
│   └── ...
├── mtree/                   # Memory tree (hex addresses)
│   ├── 1
│   └── ...
├── rtree/                   # Reference tree (exploit requirement strings)
│   ├── 1
│   └── ...
├── aptclient/               # Exploit data per library family
│   ├── 1
│   └── ...
├── init/
│   ├── 1
│   └── ...
├── net/
│   ├── 1
│   └── ...
├── kernel_module/
├── kernel_router/
├── libcam/
├── libftp/
├── libhttp/
├── librepository/
├── librshell/
├── libsmartappliance/
├── libsmtp/
├── libsql/
├── libssh/
├── libtrafficnet/
└── crypto/
```

Each library family gets its own folder. Within each folder, numbered files (`1`, `2`, `3`, ...) hold the actual exploit records. When a file exceeds ~155KB, a new numbered file is created.

---

## The Cyrillic-Encoded Record Format

Exploit data is stored as single-line records using Cyrillic characters as field delimiters. This is a space-saving encoding — each Cyrillic character is a multi-byte UTF-8 sequence but acts as a single unambiguous delimiter that won't collide with exploit data.

### Delimiter Reference

| Character | Name | Role |
|-----------|------|------|
| **Б** | Be | Value separator (key**Б**value) |
| **Д** | De | Exploit boundary (separates exploits within a line) |
| **Г** | Ge | Field separator (between key-value pairs within one exploit) |
| **Ш** | Sha | Sub-value separator (within 0-day reference indices) |
| **ю** | Yu | Key name for exploit requirements field |
| **щ** | Shcha | Key name for extra flag (password type, lan IP) |

### Record Structure

A single line in a library file looks like this:

```
{lib_name}_{version}Б{flags}Д{exploit1}Д{exploit2}Д...
```

**Header segment:** `init.so_1.0.0Б4`
- `init.so_1.0.0` — library name + version (the cache key)
- `Б4` — bitwise flags (4 = VERIFIED)

**Exploit segment:** `eБ0ГsБ269ГmБ75ГюБ1Ш2Ш3`
- `eБ0` — packed exploit type byte (type + user + extra encoded in one integer, see below)
- `sБ269` — stree index 269 (unsafe check string)
- `mБ75` — mtree index 75 (memory address)
- `юБ1Ш2Ш3` — rtree indices 1, 2, 3 (exploit requirements, Ш-separated)

### Packed Exploit Byte

The `e` field is a single packed byte encoding three pieces of information:

```
Bits 0-3: Exploit type   (s=shell, c=computer, f=file, l=bounce, etc.)
Bits 4-5: User level     (r=root, u=user, g=guest)
Bits 6-7: Extra flag     (n=new password, y=lan IP, z=internal lan IP)
```

The packing formula:
```
packed = typeCode | (userCode << 4) | (extraCode << 6)
```

Unpacking:
```
typeCode  = packed AND 0x0F
userCode  = (packed >> 4) AND 0x03
extraCode = (packed >> 6) AND 0x03
```

### Full Example

Raw line:
```
init.so_1.0.0Б4ДeБ0ГsБ269ГmБ75ГюБ1Ш2Ш3ДeБ0ГsБ270ГmБ75ГюБ3Ш2Ш4
```

Decoded:
- **Library:** `init.so` version `1.0.0`, flags = `4` (VERIFIED)
- **Exploit 1:** type=unknown(0), stree[269], mtree[75], requirements: rtree[1], rtree[2], rtree[3]
- **Exploit 2:** type=unknown(0), stree[270], mtree[75], requirements: rtree[3], rtree[2], rtree[4]

---

## The Three Trees — String Deduplication

Many exploits share the same memory addresses, unsafe check strings, and 0-day requirement descriptions. Storing these as full strings in every exploit record would be enormously wasteful. Instead, X uses three lookup tables (the "trees") that map strings to integer indices.

### stree — String Tree

**Purpose:** Stores unique "unsafe check" value strings.

**On disk:** `~/payload/exploits/stree/1`, `stree/2`, etc. One string per line.

**Example content:**
```
plessage
mdatebuttonc
lembofit
eaddge
sultcompre
```

**In memory:** `globals.G_stree` — a map of `{ string: integer_index }`

**Operations:**
- `setstree(s)` — Adds string `s` if new, returns its integer index
- `getstree(i)` — Returns the string at index `i` (reverse lookup via `indexOf`)
- `loadstree()` — Reads all stree files and builds the in-memory map

When a file gets full (`set_content` returns failure), a new numbered file is created and the active file pointer (`globals.G_fstree`) is updated.

### mtree — Memory Tree

**Purpose:** Stores unique hex memory addresses from `scan_address()`.

**On disk:** `~/payload/exploits/mtree/1`, etc. One address per line.

**Example content:**
```
0x10FE4BE7
0x8E175D0
0x304F6B61
0x7BA0BB20
```

**In memory:** `globals.G_mtree` — a map of `{ "0xABCD1234": integer_index }`

**Operations:** Identical pattern to stree — `setmtree()`, `getmtree()`, `loadmtree()`.

### rtree — Reference Tree (Requirements)

**Purpose:** Stores the unique requirement strings for **all** exploits — not just 0-days. Every `*` line returned by `scan_address()` is a requirement that must be met for the exploit to succeed (e.g., specific library versions, user counts, path existence, port forwarding rules). Occasionally a 0-day requirement slips in among them, but the rtree's primary role is tracking the conditions each exploit needs.

**On disk:** `~/payload/exploits/rtree/1`, etc. One requirement per line.

**Example content:**
```
* 0day exploit.
* Checking root active user.
* Checking guest active user.
* Using namespace <b>kernel_module.so</b> compiled at version >= <b>1.0.0</b>
* Checking registered users equal to 2.
* Checking path /bin exists in the file system.
* 3 port forwarding configured from router to the target computer.
```

**In memory:** `globals.G_rtree` — a map of `{ requirement_string: integer_index }`

**Bootstrap:** When no rtree exists, the first entry `"* 0day exploit."` is automatically created at index 0.

### Why Three Trees?

Each tree handles a different data domain with different characteristics:
- **stree** strings are typically short GUI/code fragments
- **mtree** addresses are always 32-bit hex values
- **rtree** requirements are longer descriptive sentences covering all exploit conditions

Keeping them separate avoids index collision and allows each to shard independently when files fill up.

---

## The Bloom Filter

### What It Is

The bloom filter is a probabilistic data structure that answers one question extremely fast: **"Have we ever seen this library+version before?"**

- **False positives possible:** It might say "yes" when the answer is "no" (rare)
- **False negatives impossible:** If it says "no", the library is definitely not in the database

### Specifications

| Property | Value |
|----------|-------|
| Total bits | 524,288 |
| Storage | 16,384 integers × 32 bits |
| Hash functions | 3 |
| On-disk format | Comma-separated integers in `~/payload/exploits/bloom` |

### Hash Functions

For a given key `libName:version`, three independent hash values are computed:

```
hash1 = Σ(char_code × position)           mod 524288
hash2 = XOR(char_code × 31) for each char mod 524288
hash3 = Σ(char_code × (position×17 + 13)) mod 524288
```

Each hash maps to one bit in the filter. All three bits must be set for a "possibly exists" result.

### How the Bloom Filter is Used

#### Adding a Library
When a new library is first encountered (via `Exploit.get()`), `addToBloom(libName, version)` is called:

1. Compute three hash indices from the library key
2. Set the corresponding bits in the 16,384-integer array using `bitOr`
3. Persist the updated filter to disk via `saveBloom()`

#### Checking a Library
`checkBloom(libName, version)` tests all three bit positions:

1. If **any** bit is 0 → the library is **definitely not** in the database (return `false`)
2. If **all three** bits are 1 → the library **might** be in the database (return `true`)

#### Why It Matters
Without the bloom filter, checking whether a library has been scanned before would require:
1. Opening the correct folder
2. Reading every file in it
3. Parsing every line to look for the version string

The bloom filter short-circuits this to a single array lookup — no disk I/O needed after initial load.

### Persistence

The bloom filter is saved as a flat comma-separated string of integers:

```
17472,8736,257,34944,17412,8706,1052672,559104,...
```

It is loaded once at boot (`loadBloom`) and written back after every `addToBloom()` call and after every `write()` operation.

### Statistics & Monitoring

`bloomStats()` provides capacity analysis using sampling (checks bit density in the first 64 integers and extrapolates):

| Saturation | Status |
|-----------|--------|
| < 10% | Excellent — under 2,000 items |
| 10–25% | Good — 2,000–4,000 items |
| 25–50% | Moderate — 4,000–8,000 items |
| 50–80% | High — 8,000–16,000 items |
| > 80% | Critical — filter accuracy degrading |

---

## Creating a New Database File

### Initial Installation (`database/_installer.src`)

The installer bootstraps the entire database from pre-built source data:

1. **Import all 20 source modules** (`import_code` for each `.src` file)
2. **Kill existing X processes** to avoid conflicts
3. **Back up existing exploits** (copies to `exploits.bck`)
4. **Create the bloom filter file:**
   ```
   touch(computer, exploits_path, "bloom")
   set_content(bloom_file, trim(bloom1))
   ```
5. **For each library family** (aptclient, crypto, init, net, etc.):
   ```
   create_folder(computer, exploits_path, "aptclient")
   touch(computer, exploits_path + "/aptclient", "1")
   set_content(file, trim(aptclient1))
   ```

The pre-built data in each `.src` file contains the full Cyrillic-encoded exploit records as string literals (the `aptclient1=`, `init1=`, etc. variables).

### Runtime Creation (New Library Encountered)

When X encounters a library that has no database entry:

1. **`Exploit.get(metaLib)` is called**
2. The library prefix is extracted (e.g., `"init"` from `"init.so"`)
3. If the folder doesn't exist:
   ```
   create_folder → creates ~/payload/exploits/init/
   touch         → creates ~/payload/exploits/init/1
   ```
4. The bloom filter is updated: `addToBloom(lib_name, version)`
5. A cache entry is created with empty exploits array and the `VERIFIED` flag
6. If the folder exists but the latest file exceeds 155KB, a new numbered file is created

---

## Loading the Database (Boot Sequence)

When X starts, `Exploit.loadCache()` executes this sequence:

```
1. loadstree()     → Read all stree files, build string→index map
2. loadmtree()     → Read all mtree files, build address→index map
3. loadrtree()     → Read all rtree files, build reference→index map
4. loadBloom()     → Read bloom file, rebuild integer array
5. Scan folders    → For each folder in ~/payload/exploits/:
   a. Skip stree/mtree/rtree folders
   b. For each numbered file:
      - Register in binary tree (G_exploitBtree)
      - Split content by newlines
      - For each line:
        - Split by "Д" to get header + exploit segments
        - Parse header: library key + flags
        - For each exploit segment:
          - Split by "Г" to get fields
          - Split each field by "Б" to get key-value
          - Unpack "e" field from packed byte
          - Build exploit object {e, s, m, u, ю, щ}
      - Store in G_exploitCache[key]
      - Set VERIFIED flag
```

**Performance:** Load time is tracked and reported (e.g., "Exploit cache loaded in 0.42s").

---

## Scanning — Discovering New Exploits

`Exploit.scan(metaLib)` discovers vulnerabilities by probing the Grey Hack metaxploit API:

1. **Ensure cache entry exists** — calls `get()` if needed
2. **Call `scan(metaxploit, lib)`** — returns list of memory addresses
3. **For each address**, call `scan_address(metaxploit, lib, address)`:
   - Parse output line by line
   - Lines starting with `"Unsafe check"` → extract the value string, store via `setstree()`
   - Memory address → store via `setmtree()`
   - Lines starting with `"*"` → exploit requirements (may include 0-day), store via `setrtree()`
4. **Build exploit objects:**
   ```
   {
     "e": "?" or "t",    // Unknown type (to be classified later)
     "s": stree_index,   // String tree reference
     "m": mtree_index,   // Memory tree reference
     "u": "?",           // Unknown user (to be classified later)
     "ю": "1Ш2Ш3"       // 0-day rtree indices, Ш-separated
   }
   ```
5. **Update cache flags:**
   - Clear `SCANNABLE`
   - Set `DIRTY`
   - Set `HAS_0DAY` if 0-day references found
6. **Write to disk** via `write()`
7. **Check for version adjacency** via `checkUpdate()` — may flag nearby versions for rescan

---

## Updating the Database

After scanning discovers exploits, they are initially classified as type `"?"` (unknown). The update process (`Exploit.update()`) runs each unknown exploit to classify it:

1. **For each exploit where `e == "?"` or `e == "t"`:**
   - Execute `Exploit.run(exploit, metaLib)`
   - This calls `overflow(lib, memory_address, unsafe_string, [optional])`
   - Based on the return type, classify:
     - `shell` → type `"s"`
     - `computer` → type `"c"`
     - `file` → type `"f"`
     - `null` → prompt user: password change? bounce? failure?
     - `1` (for routers) → firewall disable
2. **Update the exploit object** with the correct type and user level
3. **Write changes to disk**

Update modes:
- `--all` / `-a` — Update every library
- `--single` / `-s` — Interactive menu to pick a library
- Numeric index — Update a specific library by position

---

## Writing / Saving to Disk

`Exploit.write(metaLib)` persists the in-memory cache to the filesystem:

1. **Compute checksum** from exploit count
2. **Set VERIFIED flag, clear DIRTY flag** — data is now clean
3. **Build the record string:**
   ```
   {key}Б{flags}Д{packed_exploit_1}Д{packed_exploit_2}...
   ```
   Each exploit is packed: `eБ{packed_byte}ГsБ{stree_idx}ГmБ{mtree_idx}ГюБ{rtree_refs}`
4. **Write strategy** (preserves other libraries in the same file):
   - **Empty file** → write directly
   - **Existing content, valid index** → in-place line replacement
   - **Index mismatch or out of range** → append to end of file
5. **Save bloom filter** to ensure persistence

The write function uses the `idx` field from the cache entry to know which line in the file belongs to this library. It splits the file content by newlines, replaces the correct line, and writes the whole file back.

---

## Defragmentation

Over time, the stree and mtree accumulate orphaned entries — strings and memory addresses that were once referenced by exploit records but no longer are (e.g., after rescans overwrite old data or exploits get reclassified). These orphans waste space and inflate tree file sizes.

`Exploit.defrag` rebuilds the stree and mtree from scratch, keeping only entries that are actively referenced by at least one exploit in the cache.

### How It Works

1. **Walk every cached exploit** and collect the mtree/stree values that are actually in use
2. **Build new compact maps** with fresh sequential indices (0, 1, 2, ...), skipping any orphaned entries
3. **Update every exploit object** in the cache with its new mtree and stree indices
4. **Write every affected library** back to disk via `write()` so the new indices are persisted
5. **Delete old tree files** and write new compacted ones using the `build160k()` helper, which shards entries into files of up to ~160KB each
6. **Call `refresh()`** to reload the in-memory state from the freshly written disk data

### What Gets Defragmented

| Tree | Defragmented? | Why |
|------|--------------|-----|
| **mtree** | Yes | Memory addresses accumulate orphans as exploits are rescanned |
| **stree** | Yes | Unsafe check strings accumulate orphans similarly |
| **rtree** | No | Requirement strings are rarely orphaned and tend to be reused across exploits |

### Output

Defrag prints before/after sizes so you can see the reduction:

```
mtree size before defrag: 4821
mtree size after defrag: 3200
stree size before defrag: 5102
stree size after defrag: 3450
```

### When It Runs

- **Manual:** Run `exp defrag` from the command line
- **Automatic prompt:** After certain operations (like partial object processing), X may ask "Do you want to defrag the database?" via a yes/no prompt

### The `build160k` Helper

Tree entries are written one-per-line. The `build160k()` function accumulates lines into chunks, starting a new chunk whenever the current one reaches ~160KB (`len >= 159950`). Each chunk becomes a numbered file (`1`, `2`, `3`, ...) in the tree folder. This ensures tree files respect Grey Hack's file size limits even after compaction.

---

## The In-Memory Cache

### Global Variables

```
globals.G_exploitCache   — Main cache: { "lib_version": cache_entry }
globals.G_exploitBtree   — File index: { "/path/to/file": file_object }
globals.G_bloom          — { "filter": [16384 integers], "file": file_object }
globals.G_stree          — String tree: { "string": index }
globals.G_mtree          — Memory tree: { "0xAddr": index }
globals.G_rtree          — Requirement tree: { "* requirement": index }
globals.G_fstree         — Active stree file handle
globals.G_fmtree         — Active mtree file handle
globals.G_frtree         — Active rtree file handle
```

### Cache Entry Structure

```
{
  "flags": 4,                    // Bitwise flags (SCANNABLE|DIRTY|VERIFIED|HAS_0DAY)
  "exploits": [                  // Array of exploit objects
    {
      "e": "s",                  // Type: shell
      "s": 269,                  // stree index
      "m": 75,                   // mtree index
      "u": "r",                  // User: root
      "ю": "1Ш2Ш3",             // Exploit requirement rtree refs
      "щ": "n"                   // Extra: new password
    }
  ],
  "file": "/path/to/exploits/init/1",  // Which file stores this
  "idx": 3,                             // Line number within file
  "checksum": 5                          // Exploit count checksum
}
```

---

## Bitwise Flags

Each cache entry carries a flags field using bitwise encoding:

| Bit | Constant | Value | Meaning |
|-----|----------|-------|---------|
| 0 | `SCANNABLE` | 1 | Library needs to be scanned (new or version-adjacent update) |
| 1 | `DIRTY` | 2 | In-memory data differs from disk (needs write) |
| 2 | `VERIFIED` | 4 | Data integrity confirmed (loaded from disk or freshly written) |
| 3 | `HAS_0DAY` | 8 | Contains exploits with 0-day among their requirements |

Operations use safe bitwise helpers that avoid GreyScript's broken `bitXor` with large constants:

```
setFlag(flags, flag)   → bitOr(flags, flag)
clearFlag(flags, flag) → if bitAnd(flags,flag)==flag then bitXor(flags,flag) else flags
hasFlag(flags, flag)   → bitAnd(flags, flag) == flag
```

---

## File Size Management

Grey Hack imposes file size limits. X handles this at two levels:

1. **Tree files (stree/mtree/rtree):** When `set_content()` fails (returns non-1), a new numbered file is created in the same folder. The active file pointer is updated.

2. **Library exploit files:** Before appending a new library entry, the code checks:
   ```
   if len(get_content(last_file)) > 155000 then
       // Create new numbered file
   ```
   This ensures no single file exceeds ~155KB.

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────┐
│                   BOOT                           │
│                                                  │
│  loadstree() → G_stree    (string→index map)    │
│  loadmtree() → G_mtree    (address→index map)   │
│  loadrtree() → G_rtree    (reference→index map) │
│  loadBloom() → G_bloom    (bit array)            │
│  loadCache() → G_exploitCache (all exploits)     │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│               SCAN (new library)                 │
│                                                  │
│  1. get(metaLib)     → ensure cache entry        │
│  2. scan()           → memory addresses          │
│  3. scan_address()   → unsafe checks + 0-days    │
│  4. setstree(value)  → deduplicate strings        │
│  5. setmtree(addr)   → deduplicate addresses      │
│  6. setrtree(ref)    → deduplicate requirements     │
│  7. Build exploit objects with indices            │
│  8. Update flags (clear SCANNABLE, set DIRTY)    │
│  9. write(metaLib)   → persist to disk            │
│ 10. addToBloom()     → update bloom filter        │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│              UPDATE (classify unknowns)          │
│                                                  │
│  For each exploit where e=="?" or e=="t":        │
│  1. getmtree(e.m)  → resolve memory address      │
│  2. getstree(e.s)  → resolve unsafe string        │
│  3. overflow(lib, addr, string)                   │
│  4. Classify result → update e.e and e.u          │
│  5. write(metaLib) → persist changes              │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│              WRITE (persist to disk)             │
│                                                  │
│  1. Set VERIFIED, clear DIRTY                    │
│  2. Pack exploits → Cyrillic-encoded line        │
│  3. In-place update or append to file            │
│  4. Save bloom filter                            │
└─────────────────────────────────────────────────┘
```

---

## Key Gotchas & Limitations

### GreyScript `bitXor` Bug
GreyScript's `bitXor(2, 4294967295)` returns `-2147483646` instead of `4294967293`. This breaks traditional bit-clearing patterns like `bitAnd(flags, bitXor(flag, 0xFFFFFFFF))`. The safe `clearFlag` pattern is:
```
if bitAnd(flags, flag) == flag then return bitXor(flags, flag)
return flags
```

### Bloom Filter False Positives
The bloom filter can report false positives (says "yes" when the library isn't actually stored). This is by design — the system falls back to the full cache lookup, so correctness is preserved. False negatives never occur.

### File Size Limits
Grey Hack files have a maximum content size. The database handles this by sharding across numbered files, but corruption can occur if a write is interrupted mid-operation.

### Tree Growth & Defragmentation
The stree and mtree grow indefinitely as new strings and addresses are discovered. Running `exp defrag` compacts them by removing orphaned entries and reassigning indices (see [Defragmentation](#defragmentation)). The rtree is not defragmented. A refresh (`Exploit.refresh()`) clears in-memory state and reloads from disk but doesn't shrink files on its own.

### Tree Index Stability
Tree indices are assigned sequentially during loading. If tree files are reordered or modified externally, all exploit records referencing those indices become invalid.
