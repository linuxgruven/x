# Scanner — Port & Exploit Scanner

A comprehensive, interactive port scanner and exploit framework for Grey Hack. Scans targets, discovers vulnerabilities via metaxploit, classifies exploit results, and provides post-exploitation tools, mass LAN exploitation, RShell management, pivoting, WiFi cracking, 0day exploit cycles, library patching to harden against 0day attacks, and more — all from a single script.

> **Note:** The source has no comments and uses short variable/function names (e.g. `_tl`, `_acr2`, `_pe`) to stay under Grey Hack's 160,000 character limit. This doc serves as the primary reference for understanding the code.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Main Menu](#main-menu)
- [Scanning Flow](#scanning-flow)
  - [Port Discovery](#1-port-discovery)
  - [Exploit Scanning](#2-exploit-scanning)
  - [Exploit Types](#3-exploit-types)
- [Post-Exploitation Menu](#post-exploitation-menu)
  - [Crack Passwords](#c-crack-passwords)
  - [Switch User (Su)](#s-switch-user)
  - [Launch Apps](#a-launch-apps)
  - [Shell Commands](#-shell-commands)
  - [Local Library Scan](#l-local-library-scan)
  - [LAN Network Scan](#n-lan-network-scan)
  - [Dig (Mass LAN Exploit)](#dg-dig-mass-lan-exploit)
  - [Grab Emails/Banks](#g-grab-emailsbanks)
  - [File Browser](#f-file-browser)
  - [Download / Upload Files](#d-download--u-upload)
  - [Rename Files](#r-rename)
  - [RShell](#rs-rshell)
  - [WiFi Crack](#wf-wifi-crack)
  - [PObject Interpreter](#po-pobject-interpreter)
  - [Devices](#dv-devices)
  - [Pivot](#pv-pivot)
  - [0day Cycle Status](#0d-0day-cycle-status)
  - [Add Password](#p-add-password)
  - [Wipe Log](#w-wipe-log)
  - [Whois Lookup](#i-whois-lookup)
- [Deploy](#dy-deploy)
- [Load Remote Library](#ld-load-remote-library)
- [All Cached Credentials](#pc-all-cached-credentials)
- [Echo (File I/O)](#e-echo-file-io)
- [Dig System](#dig-system)
- [Recon (LAN Sweep)](#recon-lan-sweep)
- [RShell Manager](#rshell-manager)
- [Bouncing](#bouncing)
- [Credential Cache](#credential-cache)
- [Home Command](#home-command)
- [Navigation Reference](#navigation-reference)
- [Examples](#examples)
- [Standalone Tools](#standalone-tools)
  - [Log Wiper (wiper)](#log-wiper-wiper)
  - [Library Updater (updater)](#library-updater-updater)
  - [System Monitor (monitor)](#system-monitor-monitor)

---

## Requirements

- **metaxploit.so** — Optional. Looked for in `/lib/` then current directory. Without it, you can still use WiFi cracking, hunt, whois, echo, and other non-exploit features. Required for exploit scanning, PObject, dig, and recon.
- **crypto.so** — Optional. Required for password cracking and WiFi cracking. Looked for in `/lib/` then current directory.

## Installation

1. Copy the source code from the [scanner.src GitHub file](scanner.src)
2. In-game, open **CodeEditor.exe** (found in `/usr/bin/` or launch from desktop)
3. Paste the code into the editor
4. Click **Build** to compile it (optionally save the file first). Naming the binary `dddd` reduces the compiled file size to just over 100k.

The compiled binary will be placed in your home directory. No other dependencies needed — the script self-contains all helpers.

---

## Usage

```
scanner [target] [-r] [-q] [-po|-nr|-dg|-ls|-ns|-wf|-rc]
```

| Argument | Description |
|----------|-------------|
| `target` | IP address or domain name to scan |
| `-r`     | Scan a random public IP instead |
| `-q`     | Quick scan — show port table only, skip exploit testing (like `nmap`) |
| `-po`    | Launch directly into PObject menu |
| `-nr`    | Launch directly into Neuro scan |
| `-dg`    | Launch directly into Dig (must be on a router) |
| `-ls`    | Launch directly into Local scan |
| `-ns`    | Launch directly into LAN scan |
| `-wf`    | Launch directly into WiFi crack |
| `-rc`    | Launch directly into Recon menu (prompts for IP if not provided) |

**Examples:**

```bash
scanner 192.168.0.1          # Scan specific IP
scanner www.somewhere.com    # Resolve domain, then scan
scanner -r                   # Scan a random public IP
scanner 10.0.0.1 -q          # Quick port scan only
scanner -po                  # Jump straight to PObject
scanner -dg                  # Jump straight to Dig
scanner 10.0.0.5 -rc         # Recon a specific IP
```

If no arguments are given, scanner launches in **interactive mode** with the main menu.

---

## Main Menu

```
[ip] Scan target IP or domain
[r]  Scan random IP
[ls] Local scan     [ns] LAN scan      [dg] Dig
[po] PObject        [wf] WiFi          [rc] Recon
[ht] Hunt           [pv] Pivots        [h]  Host
[rs] RShell (servers/shells)
[e]  Echo >|>>      [w]  whois         [0d] 0day
[cm] clear mail     [cl] clear screen
[?]  Help
[x]  Exit
```

**Status bar** shows: local/scan metax+crypto status, rshell server/shell counts, internet status, and pivot depth if pivoted.

| Option | Description |
|--------|-------------|
| `ip` | Enter an IP or domain to scan |
| `r` | Scan a random public IP |
| `rs` | Open the RShell manager |
| `0d` | Show 0day exploit cycle timing and remaining window |
| `nr` | Neuro scan — find a target IP via email (requires Neurobox engineer creds) |
| `dg` | Dig — mass LAN exploitation via router IP |
| `ls` | Scan local libraries for exploits |
| `ns` | Deep recursive LAN scan with device mapping |
| `po` | PObject interpreter — remote code exec via debug_tools |
| `wf` | WiFi cracking (airmon/aireplay/aircrack) |
| `rc` | Recon — targeted intelligence gathering on a router's LAN |
| `ht` | Hunt — scan random IPs looking for a specific service type |
| `pv` | Manage active pivot sessions |
| `h` | Open host menu for your local machine |
| `e` | Echo text, or write/append to files with `>` / `>>` |
| `w` | Whois lookup on IP or domain |
| `cm` | Log in to email and delete all messages |
| `cl` | Clear the terminal |

---

## Scanning Flow

### 1. Port Discovery

Scanner queries the target's router for all used ports (plus port 0 for the router itself), then displays a table. If only port 0 (router) is found, it is automatically scanned for exploits.

```
Target: 45.195.87.14
PORT    STATE    SERVICE       VERSION    LAN
0       open     router        1.0.5      192.168.1.1
21      open     ftp           1.0.0      192.168.1.3
3306    closed   employees     1.0.3      192.168.25.6
80      open     http          1.0.2      192.168.25.6

  LAN Devices (8):
    192.168.1.2
    192.168.1.3 ports:21
    192.168.1.1 ports:8080,21,3306,80
    172.16.22.1 ports:8080
```

LAN devices are shown with their known open ports. From here:

- Enter a **port number** to scan that port for exploits
- Enter **`a`** to scan all ports at once
- Enter a **target index** (e.g. `1`) to jump to a previously-scanned result
- Enter **`b`** to go back
- Press **Enter** to re-display (won't accidentally exit)

After scanning, discovered attack vectors are listed:

```
[1] • libhttp.so (Version: 1.0.2) -> 192.168.25.6:80
    |-> Not Patched
    23 exploits found
    Sh:3 - Co:3 - Fi:3 - Un:14
[2] • kernel_router.so (Version: 1.0.5) -> 192.168.1.1:0
    |-> Not Patched
    4 exploits found
    Sh:2 - Co:0 - Fi:1 - Bo:0 - Fw:1 - Un:0
```

### 2. Exploit Scanning

Select a target to see its individual exploits:

```
--- Exploits for libhttp.so on 192.168.25.6:80 ---
#    TYPE        USER        ADDRESS       VALUE
1    shell       guest       0x6320B054    datauseuptimekeyc
2    computer    root        0x6320B054    ressequalb
3    file        root        0x4A365044    ins_h
4    null                    0x281EBD98    evolumerighlighlig
```

Select an exploit by number to run it. Successful exploits open the post-exploitation menu.

### 3. Exploit Types

| Type | Description |
|------|-------------|
| **shell** | Returns a shell object — full command access |
| **computer** | Returns a computer object — file system access |
| **file** | Returns a file object — single file access |
| **bounce** | Router exploit that can target any computer under the edge router |
| **firewall** | Disables the router's firewall |
| **null** | Returned null — may be a password-change or bounce exploit |

---

## Post-Exploitation Menu

After exploiting a target, you get an interactive menu. Available options depend on exploit type (shell/computer/file):

```
[c]  Crack (N accounts)
[s]  Su (N cracked creds)
[g]  Grab emails/banks
[f]  Browse files
[a]  Apps (N)
[d]  Download    [u]  Upload      [r]  Rename
[l]  Local scan  [n]  LAN scan    [dg] Dig
[wf] WiFi        [po] PObject     [dv] Devices
[pv] Pivot x to this host
[dy] Deploy bin from main
[rs] RShell (servers/shells)
[e]  Echo >|>>   [w]  wipe        [i]  whois   [0d] 0day
[p]  passwords   [pc] all cached creds  [ld] load lib
[b]  Back  Type home to return to main
```

### `c` — Crack Passwords

Reads `/etc/passwd`, displays all user accounts with their hashes, then offers:

- Enter a **number** to crack a specific account
- Enter **`a`** to crack all
- Enter **`b`** to skip

Cracked credentials are automatically stored in the IP-scoped credential cache (see [Credential Cache](#credential-cache)).

### `s` — Switch User

If you have cracked credentials and aren't already root, presents a list of cracked username/password pairs for this machine. Select one to log in as that user. If successful, your session upgrades to that user's shell.

### `a` — Launch Apps

*(Shell only)* Lists all executables in `/usr/bin`, `/bin`, and user home directories. Select an app by number, optionally with arguments:

```
[App # + args, or 'b' to go back] > 3 --help
```

### `!` — Shell Commands

*(Shell only)* Prefix any command with `!` to execute it directly on the remote machine:

```
[guest@10.0.0.1 shell] > !ls /home
[guest@10.0.0.1 shell] > !chmod 777 /tmp/file
```

Includes special handlers:
- **`! chmod`** — octal permissions (e.g. `! chmod 755 /path`) and `-r` recursive flag
- **`! mkdir`** — create directory (e.g. `! mkdir /path/name`), resolves relative paths to user home
- **`! qrm`** — delete file without logs (e.g. `! qrm /path`)

### `l` — Local Library Scan

*(Shell only)* Scans libraries installed on the **remote** machine for local exploits. This is how you escalate privileges when you have a non-root shell.

### `n` — LAN Network Scan

*(Shell only)* Maps the internal network from the compromised machine. Discovers all LAN devices and displays type, firewall status, and open ports. Select a device to scan its ports for exploits.

Device types detected: Edge Rtr, Router, Switch, Camera (port 37777), Appliance (port 1883), RShell (port 1222), ADB (port 5555), Device (generic).

### `dg` — Dig (Mass LAN Exploit)

*(Shell only, requires internet + router + LAN devices)* Mass exploitation of all devices on the target's LAN. See [Dig System](#dig-system) for full details.

### `g` — Grab Emails/Banks

Extracts `Mail.txt` and `Bank.txt` from user home directories on the target machine. Cracks email/bank hashes with decipher.

### `f` — File Browser

Interactive file system explorer. Shows permissions, owner, group, size. Interesting files are highlighted with * (Bank.txt, Mail.txt, Browser.txt, passwd, shadow, system.log, .key, authorized_keys, FileExplorer.exe).

```
#    PERMS       OWNER     GROUP     SIZE    NAME
1    drwxr-xr-x  root      root      -       bin/
2    -rw-r--r--  root      root      1234    passwd
3    -rw-------  tux       tux       567     Bank.txt *
```

Controls: **number** to enter/view, **path** to navigate directly, **`b`** to go up, **`x`** to exit.

### `d` — Download / `u` — Upload

**Download** pulls a remote file to your local `~/Downloads/`. **Upload** *(shell only)* sends a local file to the remote machine. When pivoted, both prompt whether to use the **main** machine or the **pivot** machine as the local endpoint.

### `r` — Rename

Rename any file or folder on the remote filesystem (requires write permission).

### `rs` — RShell

Opens the [RShell Manager](#rshell-manager). From here you can install servers, start clients, import servers, and manage connected shells.

### `wf` — WiFi Crack

*(Shell only)* Discovers nearby WiFi networks (BSSID, signal %, ESSID), then cracks them. Can crack all networks or a selected one. Optionally connect to cracked networks.

### `po` — PObject Interpreter

*(Shell only)* Interactive exploit interpreter for unpatched libraries. When opened from a Host menu, it operates on the **remote** machine (uploads metaxploit.so if needed). When opened from the main menu, it operates on your local machine.

#### Overview

PObject works by exploiting Grey Hack's `debug_tools` / `unit_testing` chain to get a **pComputer** and **pFile** handle on the target — essentially a remote shell without needing a traditional exploit. This gives you file operations, user management, and process control through the vulnerability's memory address.

#### Startup Display

On launch, PObject shows:
- **Public/Local IPs** of the target machine
- **Edge router ports** and services (from the LAN-facing router)
- **All libraries in `/lib/`** with version and patch status (`[P]` = patched, `[P:version]` = patched at version)

```
════════════════════════ PObject ═════════════════════════
  Public: 14.175.137.87  Local: 192.168.0.9

  --- Local Edge Router Ports (192.168.0.1) ---
  0   192.168.0.1      kernel_router
  21  192.168.0.2      ftp 1.0.3
  80  192.168.0.1      http 1.0.5

  --- Local Libraries (/lib) ---
  1   init.so               1.0.4
  2   kernel_module.so      1.0.2 [P]
  3   net.so                1.0.3
  4   libssh.so             1.0.4
  5   libhttp.so            1.0.5
```

#### Scanning Flow

From the PObject menu you can scan a library three ways:

| Input | What happens |
|-------|-------------|
| `ip:port` | Connects to remote port, dumps the lib, scans it |
| `lib name` or `/lib/libssh.so` | Loads the local lib file directly |
| `#` (number) | Selects from the numbered `/lib/` list above |

The scan process:
1. Checks if the library is patched — if so, skips it
2. Prompts for **Neuro credentials** (email + password) for `debug_tools`
3. Calls `debug_tools(user, pass)` to get a `debugLibrary`
4. Runs `unit_testing` on the debug library to find a vulnerable memory address
5. If **auto mode** is ON (default), automatically accepts the first valid `unit_testing` result
6. Saves the exploit to `~/0day_exploits` (see 0day Exploit Saving below)
7. Calls `payload()` on the memory address to acquire a **pComputer** and **pFile** handle
8. Drops into the **PObject Interpreter** shell

#### Interpreter Shell

Once a vulnerability is acquired, you get a shell-like prompt:

```
--- PObject Interpreter ---
  libssh.so v1.0.4 @ 0x6CBCF75E
  Auto Enabled
  Computer: [file, create_folder, touch, ...]
  File:     [chmod, copy, move, ...]
  scan, probe, meta, libs, ports, methods, auto, pt, exit

[PObject] :~$
```

| Command | Description |
|---------|-------------|
| `scan <lib\|port\|#>` | Switch to a different library without leaving the interpreter |
| `probe <path>` | Test if a file path exists on the target via `payload()` |
| `meta [lib]` | Run **all** exploits on a library — shows shells, computers, files, bounces, firewalls |
| `libs` | Enumerate all 18 standard libraries on the target with version and patch status |
| `ports` | Show open ports on the edge router |
| `methods` | List available pComputer and pFile methods |
| `auto` / `a` | Toggle auto-accept mode for `unit_testing` prompts (ON by default) |
| `pt` | Patch libraries on the target (root only) |
| `mkdir <path>` | Create a folder |
| `touch <dir> <name>` | Create a file |
| `ps` | List running processes |
| `passwd <user> <pass>` | Change a user's password |
| `useradd <user> <pass>` | Create a new user |
| `userdel <user>` | Delete a user |
| `kill <pid>` | Kill a process |
| `chmod [-r] <path> <perm>` | Change permissions (supports octal: `777`, `755`, `644`) |
| `cp <path> <dst>` | Copy a file |
| `mv <path> <dst>` | Move a file |
| `rm [-r] <path>` | Delete a file or folder |
| `rn <path> <name>` | Rename a file |
| `chown [-r] <path> <user>` | Change file owner |
| `chgrp [-r] <path> <grp>` | Change file group |
| `nr` | Launch Neuro scan from within PObject |
| `exit` / `b` | Return to PObject menu |

The `scan` command inside the interpreter lets you pivot to other libraries without leaving PObject — it re-runs the full debug_tools/unit_testing chain on the new library and updates the interpreter context.

#### 0day Exploit Saving

When PObject discovers a vulnerability via `unit_testing`, it automatically saves the exploit to `~/0day_exploits` in the format:

```
lib_name v1.0.5 @ 0x7C5F0226 unsecured_value
```

Duplicates are skipped. These saved exploits can be viewed with the **poviewer** tool (see below) and used later via the **custom exploit** option in any exploit menu.

#### Custom Exploit (`c`)

All three exploit menus (local scan, LAN scan, remote scan) include a **`c` custom** option. This lets you manually enter a memory address and unsafe check value — useful for replaying saved 0day exploits against matching library versions:

```
[Exploit #, 'c' custom, 'ba' bounce all, 'b' back, '?' help] > c
[Memory address] > 0x7C5F0226
[Unsafe check value] > ewportsizelancessagesadd
```

The exploit result is handled the same as any other overflow — shell, computer, file, bounce, or firewall.

### `dv` — Devices

*(Shell only)* Access smart appliances (port 1883: model ID, override settings/power/temp, toggle alarm) and traffic nets (port 37777: view/control traffic devices and properties).

### `pv` — Pivot

*(Shell only)* Uploads the scanner binary and required libraries (metaxploit, crypto, librshell) to the target, then launches a new scanner session rooted at that host. All subsequent scans operate from the remote machine's network position. Pivots also act as proxies — pivoting 3 times deep gives you 3 layers of proxy indirection.

### `0d` — 0day Cycle Status

Displays the current 0day exploit window timing and remaining time.

### `p` — Add Password

Manually add a root password to the credential cache for the current machine. Useful when you already know the password from a previous session or a password-change exploit.

### `w` — Wipe Log

Deletes `/var/system.log` on the remote machine. Only shown when you have write permission.

### `i` — Whois Lookup

Reverse DNS / whois on an IP or domain.

### `dy` — Deploy

*(Remote shell only)* Uploads a binary from your main machine to the remote host and launches it. Specify a binary name (searches `~/Downloads/`) or a full path.

### `ld` — Load Remote Library

*(Shell only)* Load a library from the remote host by path (e.g. `/lib/crypto.so`). Useful for loading an unmanaged library or using a library against that machine. Pivots already auto-load metaxploit and crypto.

### `pc` — All Cached Credentials

Displays all credentials stored in the credential cache across all hosts, grouped by IP.

### `e` — Echo (File I/O)

Echo text to the terminal, or write/append to files:

```
[host] > echo hello                    # Print text
[host] > echo some data > /tmp/file    # Create/overwrite file
[host] > echo more data >> /tmp/file   # Append to file
[host] > e hello > myfile              # Short form (e prefix)
```

Relative paths resolve to the user's home directory.

---

## Dig System

Dig performs mass exploitation across all devices on a target's LAN. After entering a router IP, it discovers LAN devices, scans for exploits, and extracts data in bulk.

### Dig Menu

```
[e]  Emails
[bk] Bank accounts
[u]  User data
[s]  Search file
[d]  Full dig menu
```

| Option | Description |
|--------|-------------|
| `e` | Extract Mail.txt from all machines — shows IP, user, account, hash |
| `bk` | Extract Bank.txt from all machines — shows IP, user, account, hash |
| `u` | Extract /etc/passwd + email/bank from user homedirs per machine |
| `rt` | Retrieve the root password for the network |
| `r` | Extract rshell configs/databases from machines |
| `s` | Search for a filename pattern across all machines (e.g. `decipher`, `dungeonseeker`) |
| `sw` | Wipe system.log on all reachable machines |

### Inline Filter

Within email, bank, and user data views, use **`f <term>`** to filter results:

```
[Crack #/a/f/x] > f admin     # Filter to lines containing "admin"
[Crack #/a/f/x] > f           # Clear filter, show all
```

Filters match against IP, user, account, hash, email, and bank fields (case-insensitive).

---

## Recon (LAN Sweep)

Targeted intelligence gathering on a specific router's LAN. Enter a target IP, then select a task:

| Task | Description |
|------|-------------|
| `e` | Extract emails from LAN machines |
| `bk` | Extract bank accounts from LAN machines |
| `u` | Extract user data from LAN machines |
| `s` | Search for specific file across LAN |
| `d` | Open full dig menu with all options |

---

## RShell Manager

Manage remote shell servers and connected shells.

```
RShell Manager
  Servers: 1  Shells: 3

  Imported servers:
    1   65.90.183.64

  Connected shells:
    1   Acket          145.130.33.5:10.0.21.2
    2   root           98.138.46.143:192.168.1.2
    3   guest          172.16.0.5:10.0.0.3

[s]  Install rshell server
[c]  Start rshell client
[i]  Import server by IP
[r]  Refresh shells
[#]  Open shell by number
[b]  Back
```

| Option | Description |
|--------|-------------|
| `s` | Upload librshell.so to target and install server (shell required) |
| `c` | Start rshell client on target (shell required) |
| `i` | Import an existing rshell server by IP |
| `r` | Refresh — rediscover all connected shells from all servers |
| `#` | Enter a shell number to open it in the post-exploitation menu |

When installing a server, scanner also auto-uploads metaxploit.so and caches it for that host.

---

## Bouncing

Router exploits (port 0) often return **bounce** or **null** type results that can redirect to other public IPs:

1. Select a null/bounce exploit
2. Enter the public IP you want to reach
3. If successful, you get a shell/computer on the bounce target

Use **`ba`** (bounce all) to automatically try all null exploits against a target IP at once.

---

## Credential Cache

Cracked passwords are stored in an **IP-scoped** cache. Credentials are keyed by the target machine's public IP, so they're only used for `su` on the correct machine — no cross-machine password attempts.

Creds are populated automatically when cracking via `c`, and can be added manually via `p`. The cache persists across the entire scan session, including across RShell connections and pivots.

---

## Home Command

Type **`home`** at any prompt inside the Host menu (post-exploitation) to immediately return to the scanner's main menu, no matter how deep you are.

The `home` command works from:
- The Host menu itself (`[user@ip type] >`)
- Port selection (`[Port #, ...]`)
- Target selection (`[Target #, ...]`)
- Exploit selection (`[Exploit #, ...]`)
- Sub-menus: file browser, local scan, LAN scan, dig, devices, WiFi, apps, RShell, crack, and all other nested menus

When triggered, `home` sets an internal flag (`gco.H`) that cascades through every nested loop, breaking out of each one in sequence until it reaches the main menu. The flag is cleared at the top of each main loop iteration.

If you're **pivoted**, `home` returns to the pivot session's main menu — not your home machine. To leave the pivot entirely, use `x` (exit) from the main menu.

---

## Navigation Reference

| Key | Action |
|-----|--------|
| `#` | Select item by number |
| `a` | Scan/crack all |
| `b` | Go back to previous menu |
| `x` | Exit current section |
| `?` | Show help screen |
| `home` | Return to main menu from anywhere inside the Host menu (see [Home Command](#home-command)) |
| `ba` | Bounce all null exploits against a target IP |
| `f <term>` | Filter results (dig/recon data views) |
| `f` | Clear filter |
| Enter | Re-display current menu (won't accidentally exit) |

---

## Examples

### Basic scan → exploit → crack → su → root

```
scanner 45.33.21.100

PORT    STATE    SERVICE       VERSION    LAN
0       open     router        1.2.3      192.168.0.1
22      open     ssh           1.0.0      192.168.0.2
80      open     http          2.1.0      192.168.0.3

[Port #, 'a' scan all, 'b' back, '?' help] > a
[i] Scanning for exploits...

[1] • libssh.so (1.0.0) -> 192.168.0.2:22
    Sh:2 - Co:0 - Fi:1 - Un:3

[Target #, 'b' back, '?' help] > 1

#    TYPE        USER        ADDRESS       VALUE
1    shell       guest       0x7A3F        lqkSjf
2    shell       tux         0x4B12        rTpVx2

[Exploit #, 'ba' bounce all, 'b' back, '?' help] > 2

[+] Got shell!
    User: tux
    Host: 45.33.21.100

[tux@45.33.21.100 shell] > c

#    USER            HASH
1    root            e265b84b1626c33802363f494ac7e1be
2    tux             416ce9d59057755589909b85da86bf4e

[Crack #/a/b] > 1
root            P@ssw0rd123

[tux@45.33.21.100 shell] > s

  Cracked credentials:
  1) root : P@ssw0rd123

[Connect as #, or 'b' to skip] > 1
[+] Got root shell!
    User: root
    Host: 45.33.21.100
```

### RShell → remote access

```
[root@45.33.21.100 shell] > rs

[rshell] > s
[+] rshell server installed!
[+] Imported 45.33.21.100 — 0 shells

[rshell] > r
[+] Refreshed: 2 shell(s) from 1 server(s)

  Connected shells:
    1   Acket          145.130.33.5:10.0.21.2
    2   guest          98.138.46.143:192.168.1.2

[rshell] > 1
[+] Opening shell...
    User: Acket
    Host: 145.130.33.5
```

### Pivot through LAN

```
[tux@45.33.21.100 shell] > n

#    LAN IP            TYPE        FW   PORTS
1    192.168.0.1       Edge Rtr    F    0,22,80
2    192.168.0.4       Camera           37777
3    192.168.0.5       Appliance        1883

[Device # to scan, 'r' refresh, 'b' back] > 2
```

### Mass exploitation with Dig

```
scanner

[tux@192.168.1.16] > dg
[Enter router IP] > 45.33.21.100

[e]  Emails
[bk] Bank accounts
[u]  User data
[s]  Search file
[d]  Full dig menu

> e
[i] Scanning LAN devices...
[i] Extracting emails from 8 devices...

#    IP               USER            ACCT            HASH
1    192.168.0.2      root            admin@corp.com  a3f8...
2    192.168.0.3      tux             user@mail.com   b7c2...

[Crack #/a/f/x] > f corp
  (filtered to 1 result)

[Crack #/a/f/x] > 1
[i] Cracking admin@corp.com...
admin@corp.com  SecretPass
```

### Quick port scan

```bash
scanner 10.0.0.1 -q
```

Outputs the port table and exits immediately — useful for quick recon without triggering exploits.

---

## 0day Exploit Workflow

Most Grey Hack tools can only use exploits they discover in the current session — once you leave, those addresses and values are gone. Scanner's 0day pipeline solves this by **persisting exploits to disk** and letting you **replay them on demand** against any target running the same library version.

### How It Works

In Grey Hack, every library version shares the same set of memory addresses and unsafe check values across all machines. If you find that `libssh.so v1.0.4` has an exploit at `0x6CBCF75E` with value `dingetelend_`, that same address + value works on **every machine** running `libssh.so v1.0.4`.

### The Pipeline

```
┌─────────────┐     auto-save     ┌──────────────────┐     browse     ┌──────────┐
│  PObject     │ ──────────────>  │  ~/0day_exploits  │ ────────────> │ poviewer │
│  unit_test   │                  │  (text file)      │               │          │
└─────────────┘                   └──────────────────┘               └──────────┘
                                         │
                                         │ replay via 'c' custom
                                         ▼
                                  ┌──────────────────┐
                                  │  Any exploit menu │
                                  │  (local/LAN/remote)│
                                  └──────────────────┘
```

1. **Discover**: Use `scanner -po` or the `po` menu to scan libraries. When `unit_testing` finds a vulnerability, it's automatically saved to `~/0day_exploits` in the format:
   ```
   libssh.so v1.0.4 @ 0x6CBCF75E dingetelend_
   ```
   Duplicates are skipped automatically.

2. **Browse**: Use `poviewer` to view, filter, and manage your exploit database. Filter by library name or version to find what you need.

3. **Replay**: When scanning a target (local, LAN, or remote), if you see a library version you have a saved 0day for, press **`c`** in the exploit menu to enter the address and value manually. The overflow runs just like any other exploit — shell, computer, file, bounce, or firewall.

### Why This Matters

- **Persistence** — Exploits survive across sessions. Discover once, use forever (until the lib is patched or the 0day cycle ends).
- **Speed** — Skip the slow `unit_testing` / exploit scanning phase entirely on repeat targets.
- **Coverage** — PObject can find vulns that the normal scanner flow doesn't surface (debug_tools + unit_testing explores different code paths than metaxploit.scan).
- **Offline prep** — Scan your own machine's libraries to build an exploit database before attacking anyone.

---

## PObject Exploit Viewer (poviewer)

A standalone tool for browsing saved 0day exploits from `~/0day_exploits`.

```
════════════════════════════════════════════════════════════
  0day Exploits (4 total)
════════════════════════════════════════════════════════════

#    LIBRARY                 VERSION   ADDRESS       VALUE
------------------------------------------------------------
1    kernel_router.so        1.0.4     0xC1E3C21     imekeyr
2    libhttp.so              1.0.5     0x7C5F0226    ewportsizelancessagesadd
3    libsql.so               1.0.0     0x7F09BD2E    self
4    libssh.so               1.0.4     0x6CBCF75E    dingetelend_

[r] Refresh
[l] Libs (browse by lib:version)
[f] Filter (current: none)
[c] Clear filter
[d] Delete entry
[x] Exit
[0day] >
```

| Option | Description |
|--------|-------------|
| `r` | Reload entries from `~/0day_exploits` |
| `l` | Show library summary grouped by lib:version with exploit counts, select one to auto-filter |
| `f` | Free-text filter by library name, version, or address |
| `c` | Clear the current filter |
| `d` | Delete a specific entry by number (with confirmation) |
| `x` | Exit the viewer |

### Workflow

1. Run `scanner -po` and scan libraries — exploits are auto-saved to `~/0day_exploits`
2. Run `poviewer` to browse saved exploits, filter by lib:version to find matching entries
3. When scanning a target with a matching library version, use **`c` custom** in the exploit menu to replay the saved address + value

---

## Standalone Tools

The `tools/` directory contains small standalone utilities meant to run alongside the scanner or independently on compromised machines.

### Log Wiper (wiper)

Continuously clears `/var/system.log` to hide your activity.

```
wiper [interval]
```

| Argument | Default | Description |
|----------|---------|-------------|
| `interval` | `5` | Seconds between wipes (minimum 1) |

**How it works:** Creates an empty file with `touch`, then `move`s it over `system.log` — effectively replacing the log with a blank file. Exits if write permission is lost.

### Library Updater (updater)

Auto-updates `metaxploit.so` and `crypto.so` on a loop. Keeps your exploit libraries current during long sessions.

```
updater [interval]
```

| Argument | Default | Description |
|----------|---------|-------------|
| `interval` | `300` | Seconds between update checks (0.01–300) |

**Startup behavior:**
1. Loads `aptclient.so` from `/lib/` or current directory
2. Searches for each library in user home and `/lib/`
3. Downloads missing libraries to user home via apt
4. Reports found/missing library locations

**Loop behavior:** Checks `aptclient.check_upgrade` for each library. If an update is available, installs it in-place at the library's current location.

### System Monitor (monitor)

Continuous filesystem and process monitor with intrusion detection. Detects changes to any file on the system, tracks process creation/termination, and provides automated defenses.

```
monitor [timeout] [watchpath1] [watchpath2] ...
```

| Argument | Default | Description |
|----------|---------|-------------|
| `timeout` | `0` (continuous) | Seconds between scans (0 = no delay) |
| `watchpath` | `/home/guest` | Additional paths to quarantine new files from |

**Features:**

- **File change detection** — Reports new files (`+`), removed files (`x`), and modified files (`?`) with details (size, owner, group, permissions, content changes)
- **Process monitoring** — Reports new (`>`) and stopped (`-`) processes with command, PID, and user
- **Blacklist** — Re-reads `~/blacklist.txt` each cycle. Lines are process name patterns (one per line, `#` for comments). Matching processes are killed automatically
- **Guest guard** — Kills ALL processes owned by the `guest` user
- **Quarantine** — New files appearing in watched paths (default `/home/guest`) have all permissions stripped and are moved to `/root/quarantine`

**Blacklist example** (`~/blacklist.txt`):
```
# Kill any reverse shell or chat clients
rshell_client
chat_client
# Kill scanners
nmap
```
