# X — Complete Reference Guide

X is a comprehensive hacking framework for [Grey Hack](https://store.steampowered.com/app/605230/Grey_Hack/). It provides over 100 commands for scanning, exploitation, password cracking, proxy chains, pivoting, automation, and AI-assisted operations — all from a single shell.

This guide covers everything from first install to advanced workflows. Use `man COMMAND` inside X at any time for detailed help on any command.

---

## Table of Contents

1. [Installation](#installation)
2. [First Launch & Setup](#first-launch--setup)
3. [The Prompt](#the-prompt)
4. [Getting Help](#getting-help)
5. [Shell Basics](#shell-basics)
6. [Port Scanning — nmap](#port-scanning--nmap)
7. [Vulnerability Scanning — scan](#vulnerability-scanning--scan)
8. [Exploit Database — exp](#exploit-database--exp)
9. [Password Cracking](#password-cracking)
10. [Privilege Escalation — su](#privilege-escalation--su)
11. [Shadow Cache](#shadow-cache)
12. [Remote Access — SSH, FTP, SCP](#remote-access--ssh-ftp-scp)
13. [Session Management — sess](#session-management--sess)
14. [Proxy Chains — proxy](#proxy-chains--proxy)
15. [Pivoting — pivot](#pivoting--pivot)
16. [Network Reconnaissance](#network-reconnaissance)
17. [Wireless Attacks](#wireless-attacks)
18. [0day Framework](#0day-framework)
19. [Remote Shell — rshell](#remote-shell--rshell)
20. [Email — email](#email--email)
21. [Mission Contracts — missions](#mission-contracts--missions)
22. [Heists — heist](#heists--heist)
23. [Build & Package System](#build--package-system)
24. [Library Management — lms](#library-management--lms)
25. [Bash Scripting — run](#bash-scripting--run)
26. [AI Agent — ai](#ai-agent--ai)
27. [Configuration — config, alias, favs](#configuration--config-alias-favs)
28. [File Operations](#file-operations)
29. [Text Processing & Pipes](#text-processing--pipes)
30. [Surveillance & Monitoring](#surveillance--monitoring)
31. [Offensive Toolkit](#offensive-toolkit)
32. [Cryptography & Encoding](#cryptography--encoding)
33. [Stealth & Anti-Forensics](#stealth--anti-forensics)
34. [System Utilities](#system-utilities)
35. [Common Workflows](#common-workflows)
36. [Troubleshooting](#troubleshooting)
37. [Credits](#credits)

---

## Installation

### Install Steps

After installing the X binary, run each of these in order from the Grey Hack terminal:

1. `x` — run X first to create the payload structure
2. `man` — install man pages
3. `passwords` — install password lists
4. `sources` — install sources
5. `bash` — install bash scripts
6. `bash-tests` — install bash tests
7. `exploits` — install exploit database

Then save `libhttp.so v1.0.0` to `~/payload/savedLibs`.

### First-Time Setup (inside X)

Once X is running, issue these commands:

```bash
rainbow -n
```
Select **yes** to auto-load rainbow tables on startup.

```bash
config -y
```
Enables auto-reconnect to your last proxy after a crash.

```bash
config -v http
config -x 9
```
Sets up your root bounce library.

Once you have a hack shop, or after running `pacman -Sr` to grab a random repo:

```bash
sys check
```
Verifies all required libraries are installed.

### Optional — AI Agent

```bash
ai learn all       # Teach the AI agent every command (speeds up AI significantly)
```

### Keeping Your Exploit Database Current

Always proxy before hacking:

```bash
@proxy
```

Then sync your exploit database regularly:

```bash
pacman -Sy -e -c 100    # Full hardware: 100 passes
pacman -Sy -e -c 10     # Default/weak hardware: start here
```

> Don't run high pass counts on default hardware — use `-c 10` or lower until you upgrade.

---

## First Launch & Setup

After running the install steps above, launch X. You land in the X shell immediately.

> **Tip:** Without a config file, X removes itself on exit. With one, it persists.

```bash
config -c          # Create config file
config status      # Check current settings
```

Other useful config toggles:

```bash
config -m          # Auto-update metaxploit on launch
config -s          # Auto-add sessions to cache
exp backup         # Backup exploit database (do this regularly!)
```

---

## The Prompt

```
•[MAIN]•[P]••[tux~Workstation@92.11.2.162:192.168.0.2] [/home/tux]
•   •:~$
```

| Field | Meaning |
|-------|---------|
| `MAIN` | Current session layer: MAIN, PROXY, PIVOT, SHELL, etc. |
| `[P]` | Passwd file status — green = readable, red = no access, red X = missing |
| `tux~Workstation` | Current user and machine type (Workstation, Router, Switch) |
| `92.11.2.162:192.168.0.2` | Public IP : LAN IP |
| `/home/tux` | Current working directory |
| `[R]` | Appears when a cached root password exists for this machine (from `shadow`) |

---

## Getting Help

```bash
man COMMAND        # View the man page for any command
man scan           # Example: scan documentation
?                  # List all available commands
ai "what does scan do"   # Ask the AI agent in plain English
```

Man pages are installed to `/payload/man/` and are readable even in environments without the `man` command.

---

## Shell Basics

### Navigation

```bash
ls                 # List files and directories with details
cd /path           # Change directory
cd ~               # Go to home directory
cd -               # Return to previous directory
pwd                # Print current directory
tree               # Show directory tree
```

### File Management

```bash
cat file.txt       # View file contents
cp src dest        # Copy file
cp -r folder/ backup/   # Copy directory recursively
mv old new         # Move or rename
rm file.txt        # Delete file
rm -r folder/      # Delete folder recursively
mkdir folder       # Create directory
touch file.txt     # Create empty file
vi file.txt        # Open file in text editor
file scanner       # Show file info (permissions, owner, type, size)
stat file.txt      # Detailed file statistics
disk               # Show disk usage
```

### Text Editing

```bash
vi file.txt        # Open vi editor
                   # Inside vi: ne = new empty file, :w = save, :q = quit
```

### Searching

```bash
find -n *.txt                  # Search whole system for files by name pattern
find -n config -p /etc         # Search in /etc for files named "config"
find --text readme             # Search for text files by name
find chat .pdf                 # Find files named "chat" OR ending in ".pdf"
locate keyword                 # Fast indexed file search
grep "pattern" file.txt        # Search text in a file
grep -r "pattern" /path        # Recursive text search
```

### Permissions

```bash
chmod 755 file     # rwxr-xr-x
chmod 644 file     # rw-r--r--
chmod u-rx file    # Remove user read+execute
chown root file    # Change owner to root
chgrp admin file   # Change group
```

### User Management

```bash
whoami             # Current user
useradd newuser    # Create user
userdel user       # Delete user
passwd             # Change password interactively
groups             # Show your groups
```

### System Info

```bash
hostname           # Machine hostname
ifconfig           # Network interfaces
uptime             # System uptime
neofetch           # ASCII system info display
specs              # Hardware specifications
ps                 # List running processes
htop               # Interactive process monitor
kill 1234          # Kill process by PID
kill -a bash       # Kill all processes named "bash"
lsof               # List open files / processes
```

### Redirection & Chaining

```bash
command > file.txt           # Redirect output to file (overwrite)
command >> file.txt          # Append output to file
cmd1 | cmd2                  # Pipe output of cmd1 to cmd2
cmd1 ; cmd2                  # Run cmd2 after cmd1 (always)
cmd1 && cmd2                 # Run cmd2 only if cmd1 succeeds
```

---

## Port Scanning — nmap

`nmap` scans for open ports and services. It is reconnaissance only — it does not exploit anything.

```bash
nmap 192.168.1.1            # Scan specific IP
nmap example.com            # Scan domain
nmap -l                     # Scan localhost
nmap -p                     # Scan your own public IP
nmap -r                     # Scan a random IP
nmap -w 155.236.80.20       # Scan with WHOIS + router version + firewall rules
nmap -sn 1.2.3.4            # Discover all LAN devices behind the router at 1.2.3.4
```

Save output:

```bash
nmap 192.168.1.1 > scan.txt      # Save to file (no terminal output)
nmap 192.168.1.1 >> scan.txt     # Append to file
```

`-sn` recursively discovers sub-routers and marks devices as `[Edge Router]`, `[Router]`, or `[Device]`.

**See also:** `man nmap`

---

## Vulnerability Scanning — scan

`scan` is the primary attack command. It discovers vulnerabilities and provides an interactive exploit menu.

### Basic Usage

```bash
scan 192.168.1.1            # Scan remote IP
scan example.com            # Scan domain
scan -l                     # Scan localhost
scan -lp                    # Scan localhost including 0day exploits
scan -n                     # Interactive scan of local network
scan -r                     # Scan a random target
```

### LAN Targets

```bash
scan 192.168.1.5            # Scan LAN IP directly (auto-finds parent router)
```

X automatically finds the correct parent router, lists open ports, shows any firewall rules, and launches the exploit menu.

### Targeted Port/Library Scanning

```bash
scan -p 192.168.1.1 22      # Attack port 22 (SSH) specifically
scan -p 192.168.1.1 http    # Attack by service shortname
scan -pd /lib               # Scan a library folder for all exploits
```

Port shortnames: `router` (0), `ssh` (22), `ftp` (21), `http` (80), `chat` (6667), `rshell` (1222), `repo` (1542), `cam` (37777), `sql` (3306), `smtp` (25)

### Smart Scanning (--n, --l, --e, --c)

```bash
scan --n apt c              # Network scan: use aptclient for computer exploits
scan --n libssh.so 2        # Network scan: specific library, exploit index 2
scan --l libssh.so 2        # Local scan: specific library and index
scan --e shell              # Search ALL libraries for shell-type exploits
scan --e computer -u root   # Search for root-level computer exploits
scan --c 192.168.1.1 libssh.so c  # Connect to IP with specific library for computer exploit
```

### Mass Scanning

```bash
scan -a                                        # Scan all public IPs
scan -a -s 10.0.0.0 -e 10.255.255.255         # Scan specific range
scan -a -w "ssh"                               # Filter: only targets matching "ssh"
```

Results are saved as text files in your current directory.

### Network Firewall Management

```bash
scan -d                     # Disable ALL local network firewalls
scan -nf                    # Show network firewall status
scan -nd                    # Try to disable network firewalls
scan -nfd                   # Show then disable network firewalls
```

### Bounce Attack

```bash
scan --b -p PUBLIC_IP -l LAN_IP    # Root bounce to LAN (same path missions/ai use)
```

On the router as root this runs:
1. `scan --e bounce -u root LAN` / `scan --e computer -u root LAN` against local `/lib`
2. If no root lan bounce: install `config -v` lib, retry `--e`, then `scan --l <lib> <index> LAN` (`config -x`)

Wipes logs automatically. `config -v` / `-x` only required when the router has no local root bounce.

### Exploit Types

After scanning, each vulnerability is labeled:

| Type | What You Get |
|------|-------------|
| `shell` | Full command-line shell on the target |
| `computer` | File system access on the target computer |
| `file` | Access to a single specific file |
| `bounce` | LAN bounce — redirect through a router to reach an internal IP |
| `null` | May need an extra parameter (e.g. username/password reset exploit) |

### Post-Exploitation Menu

After exploiting, you enter a menu with options like:
- Crack passwords
- Browse files
- Escalate privileges
- Download libraries
- Add exploits to your database
- Update metaxploit

**See also:** `man scan`

---

## Exploit Database — exp

Your exploit database stores discovered vulnerabilities for reuse without re-scanning.

### View & Search

```bash
exp -l                          # List all exploits
exp -p 7                        # View all exploits at index 7
exp -p 7 2                      # View specific exploit at index 7, position 2
exp view -l libssh.so -v 1.0.5  # View by library name and version
```

Search with operators (`=`, `!=`, `>`, `>=`, `<`, `<=`, substring default):

```bash
exp -f -n =:init                # Name exactly equals "init"
exp -f -v >:1.0.3               # Version greater than 1.0.3
exp -f -e shell                 # Exploit type contains "shell"
exp -f -e =:shell               # Exploit type exactly "shell"
exp -f -e !=:lan                # Exclude LAN-type exploits
exp -f -u root                  # User field contains "root"
exp -f -m 0x69F89F6             # Memory address search
exp -f -s "searchstring"        # String tree value search
exp -f -r criteria              # Router/service field search
```

### Update & Generate

```bash
exp router                      # Generate new router library versions
exp ssh                         # Generate new SSH versions
exp ftp / exp http / exp smtp / exp rshell / exp repo / exp sql
exp all                         # Generate all service types
exp all -p 50                   # Generate with 50 passes (more results)
exp refresh                     # Refresh database indices
```

### Maintenance

```bash
exp defrag                      # Remove orphaned indexes
exp reset                       # Reset database
exp backup                      # Backup database (do this regularly!)
exp restore                     # Restore from latest backup
exp restore snapshot_name       # Restore specific snapshot
```

### Bloom Filter

The bloom filter accelerates exploit lookups:

```bash
exp bloom -s                    # Bloom filter statistics (saturation, false positive rate)
exp bloom -a                    # Analyze bit pattern distribution
exp bloom reset                 # Reset bloom filter
exp bloom rebuild               # Rebuild from cache
```

### Grind — Create Custom Exploits

Run a specific exploit 35 times to generate a new library version:

```bash
exp grind -l libhttp.so 0x1234 "Value"               # Grind local library
exp grind -r 192.168.1.1 libhttp.so 0x1234 "Value"   # Grind remote library
```

### Top Exploits

```bash
exp top                         # Show top exploits by usage
exp top -e shell                # Top shell exploits
exp top -u root                 # Top root-level exploits
exp top -n 20                   # Top 20 results
```

**See also:** `man exploits`

---

## Password Cracking

### dict — Dictionary Attacks

`dict` runs wordlist attacks against local, SSH, FTP, email, and crypto targets.

```bash
# Local attacks
dict -l                         # Dictionary attack on localhost
dict -l -u admin                # Attack specific user on localhost
dict -lp                        # Print cracked password (don't cache)
dict -i                         # Cache the cracked password in shadow

# Remote SSH/FTP attacks
dict -s 192.168.1.1 22          # SSH dictionary attack
dict -s -u root 192.168.1.1 22  # SSH attack, specific user
dict -f 192.168.1.75 21         # FTP dictionary attack

# Email and crypto
dict -e user@mail.com           # Email account attack
dict -c btc admin               # Crypto wallet attack

# Partial scans (for resuming or targeted ranges)
dict -e --start 0 --stop 1000 admin@mail.com     # First 1000 passwords
dict -c --start 5000 --stop 10000 btc admin      # Passwords 5000–10000
```

### rainbow — Rainbow Tables

Rainbow tables pre-compute password hashes for instant cracking:

```bash
rainbow -n                      # Initialize tables (prompts for wordlist path)
rainbow -l                      # Load tables into memory
rainbow -r                      # Rebuild tables from wordlists
rainbow -x                      # Clear all tables
```

Generate custom wordlists:

```bash
rainbow -m uln 8 50000          # 50k passwords, 8 chars, uppercase+lowercase+numbers
rainbow -m ulnR 15 100000       # 100k passwords, 1–15 chars, random length
rainbow -k 2 50000              # Markov chain order-2, 50k passwords
rainbow -k 3 25000              # Markov order-3 (most realistic/natural)
rainbow -k 2 50000 -s           # Markov order-2, save to list directory
```

Character set flags for `-m`: `u`=uppercase, `l`=lowercase, `n`=numbers, `s`=symbols, `R`=random length

### brute / su — Brute Force

Brute-force root password directly:

```bash
su -b                           # Brute force root password
su -b -c                        # Try capitals-first (e.g. "Password123")
su -b -C                        # Mixed-case first character
su -b -n                        # Letters only, no digits
su -b -N                        # Digits only (0–9)
su -d                           # Dictionary attack via su
```

**Tip:** Use `config -p` to preload the rainbow index on startup. `su -b` is fast when the index is loaded.

**See also:** `man dict`, `man rainbow`, `man su`, `man brute`

---

## Privilege Escalation — su

`su` manages user switching and local privilege escalation.

```bash
su root                         # Switch to root (requires password)
su -r                           # Attempt root elevation
su -u USER PASSWORD             # Login as specific user with known password
su -s                           # Start a shell with current user's permissions
su -s tux                       # Start a shell as user "tux"
su -t                           # Terminal with user permissions
su -l                           # Re-launch X as this user
su -e rm file.txt               # Execute one command as current user
su -w                           # Wipe system log
su -p                           # Print passwd file
```

When you have a non-root shell and need root access:

1. Try `su -b` (brute force) or `su -d` (dictionary)
2. Try `scan -l` to find local privilege escalation exploits
3. Try `scan -lp` to include 0day exploits in the local scan

---

## Shadow Cache

The shadow cache stores IP:password pairs for fast re-authentication.

```bash
shadow -a                       # Add credentials (prompts for IP and password)
shadow -a 192.168.1.1 r00tpass  # Add specific IP:password
shadow -l                       # List all cached passwords
shadow -r                       # Import shadow file (prompts for path)
shadow -r /home/user/shadow.bak # Import specific file
shadow -w                       # Write cache to ./shadow (encrypted)
shadow -w -d                    # Write decrypted plaintext
shadow -x                       # Clear all cached passwords
shadow -x -q                    # Clear quietly
```

Shadow file format (one per line): `ip:password`

The `[R]` indicator in your prompt means a cached root password exists for the current machine.

**jack** — automated local dictionary attack that populates the shadow cache:

```bash
jack                            # Local dictionary attack + cache result
jack MyServer                   # Same, with nickname stored
```

Requires SSH or FTP to be available on the target.

**See also:** `man shadow`, `man jack`

---

## Remote Access — SSH, FTP, SCP

### SSH

```bash
ssh tux@192.168.1.1             # Connect via SSH
ssh -P mypass tux@192.168.1.1   # With password
ssh -p 2222 tux@remotehost      # Custom port
ssh -t tux@remotehost           # Enable tunneling
ssh -l tux@remotehost           # Force local X shell on remote
ssh help                        # Interactive connection assistant
```

### SCP — File Transfer over SSH

```bash
scp -d /remote/file.txt         # Download file from SSH target
scp -u /local/file.txt          # Upload file to SSH target
```

### FTP

```bash
ftp tux@192.168.1.1             # Connect via FTP
ftp -P mypass tux@remotehost    # With password
ftp -p 2121 tux@remotehost      # Custom port
ftp -t tux@remotehost           # Enable tunneling
ftp help                        # Interactive connection assistant
```

Inside FTP shell:

```bash
get file.txt                    # Download file
put local.txt                   # Upload file
```

**See also:** `man ssh`, `man ftp`, `man scp`

---

## Session Management — sess

Sessions let you work on multiple computers simultaneously and switch between them instantly.

```bash
sess -l                         # List all active sessions
sess -u 1                       # Switch to session ID 1
sess -r 1                       # Remove session ID 1
sess -r 1 -y                    # Remove with updated list shown
sess -a                         # Add current session to cache
sess -a BankServer              # Add with nickname "BankServer"
sess -n 1 BankServer            # Rename session 1 to "BankServer"
sess -g BankServer              # Jump to session by nickname
sess -rn BankServer             # Remove session by nickname
sess back                       # Return to previous session
sess -m                         # Interactive session management GUI
sess -x                         # Clear all sessions except Main
```

### Execute Commands Remotely

```bash
sess -e 1 cat /etc/passwd       # Execute command in session 1
```

### Transfer Files Between Sessions

```bash
sess -p 2 file.txt              # Pass file.txt to session 2
sess -p 1 file.txt --path /tmp  # Pass to session 1, save in /tmp
```

**Tip:** Use `config -s` to automatically add sessions to the cache whenever you get a new shell.

**See also:** `man sessions`

---

## Proxy Chains — proxy

Proxy chains route your traffic through compromised routers, hiding your real IP from targets.

### Setup

Create `proxy.dat` first (format: `ip:port:user:password`, one per line):

```bash
vi proxy.dat                    # Open editor, then use: ne proxy.dat
```

### Running Proxy Chains

```bash
proxy -a                        # Standard proxy (proxy.dat preferred over Map.conf)
proxy -x                        # Combined proxy (both proxy.dat + Map.conf)
proxy -q                        # Quick proxy (single router hop)
yes; proxy -p                   # proxy.dat chain (yes skips prompts)
proxy -m                        # Map.conf chain
yes; proxy -r 5                 # Random 5-hop chain (yes skips prompts)
proxy -h -c 10                  # 10-hop chain (1 hop = -q behavior)
proxy -c                        # Count available hops
```

### Map.conf Management

```bash
proxy -n                        # Create a new empty Map.conf (overwrites existing!)
proxy -ri filename              # Import map_ips.dat file into Map.conf
proxy -wo filename              # Export Map.conf to map_ips.dat file
```

### Crash Recovery Decoys

Decoys absorb connection crashes when pivoting deep chains:

```bash
proxy -d -r -i 1                # Start decoy tied to session ID 1
proxy -d -i 1                   # Return to session ID 1 after crash
proxy -d -n mySession           # Return to named session
```

Enable `config -y` so proxy configuration is saved automatically. After a crash or disconnect, run `proxy -q` again to re-establish instantly.

**See also:** `man proxy`

---

## Pivoting — pivot

Pivoting installs X on a compromised machine and launches it, letting you operate from inside their network.

```bash
pivot                           # Minimal pivot (prompts for install directory)
pivot -y                        # Minimal pivot, auto-install to home directory
pivot --full                    # Full pivot — uploads X and your entire payload directory
```

**Minimal** pivot: copies X binary and an empty payload structure.  
**Full** pivot: copies X binary, man pages, password lists, rainbow tables, saved exploits, and everything else.

Maximum nested pivots: 17 levels deep.

After pivoting, you are running X on the target. From there:

```bash
scan -n                         # Scan their internal network
scan -l                         # Find local privilege escalation
dig -a                          # Crawl the entire LAN for sensitive data
```

**See also:** `man pivot`

---

## Network Reconnaissance

### hunt — Find Services Across the Internet

`hunt` searches the internet for computers running specific services.

```bash
hunt ssh                        # Find 1 SSH service (default)
hunt ssh -c 5                   # Find 5 SSH services
hunt ssh -v 1.0.3               # Find SSH version 1.0.3 specifically
hunt ftp -c 10                  # Find 10 FTP services
hunt ftp -d                     # Find FTP and download its library
hunt http -v 1.0.1 -s           # Find HTTP version 1.0.1, save results
hunt router                     # Find routers
hunt bank                       # Find bank services
hunt cam                        # Find cameras
hunt chat                       # Find chat services
hunt smtp                       # Find SMTP mail servers
hunt sql                        # Find SQL databases
hunt lib                        # Find any library server
hunt lib -n crypto -d           # Find crypto library and download it
hunt lib -n libssh -v 2.1       # Find specific library version
hunt custom -p 8080             # Hunt for a custom port
hunt employee -c 5              # Find 5 employee computers
hunt special -n passwd          # Find computers with special "passwd" file
hunt neuro                      # Find Neurobox networks
hunt wifi                       # Find WiFi networks
hunt awifi -e HomeNetwork       # Find WiFi by ESSID
hunt awifi -b 00:11:22:33:44:55 # Find WiFi by BSSID
hunt file -n exploit            # Find computers with file named "exploit"
```

Common flags for all hunt types:
- `-c COUNT` — how many results to return (default: 1)
- `-s` — save results to current directory
- `-d` — attempt to download the found library
- `-k` — stop early when complete
- `-v VERSION` — filter by version

Press `q` during a hunt to stop early.

### recon — Remote Reconnaissance

`recon` gathers intelligence on a target: email accounts, passwords, banking data, binary files.

```bash
recon 203.0.113.50              # Full reconnaissance (user dataset + company info)
recon -a 203.0.113.50           # Extended recon + admin email crack attempt
recon -r 203.0.113.50           # Email-focused recon only
recon -s 203.0.113.50           # Search for specific file (default: decipher in /etc)
recon -s -f shadow -p /etc 203.0.113.50   # Search for "shadow" in /etc
recon --filter 203.0.113.50     # Interactive dataset filtering
recon --filter -u 203.0.113.50  # Filter user dataset instead of email dataset
recon --save                    # Save results to reconData.txt
recon --extreme 203.0.113.50    # Expand LAN bounce from 0–50 to 0–255 addresses
recon -i 192.168.1.5 203.0.113.50  # Restrict LAN bounce to specific IP
recon --file /home/tux/ips.txt  # Batch recon from file (one IP per line)
```

### dig — Router LAN Crawler

`dig` must be run **from a router shell**. It crawls the entire LAN and extracts data from every connected computer.

```bash
# Must be on a router first (scan and exploit the router, get a shell on it)
dig -a                          # Scan all data types (email, bank, rshell, users)
dig -e                          # Extract email data (Mail.txt files)
dig -e --wipe                   # Extract email data and delete Mail.txt files
dig -b                          # Extract bank data (Bank.txt files)
dig -b --wipe                   # Extract and delete Bank.txt files
dig -r                          # Search for rshell data
dig -u                          # Extract user/credential data
```

Common flags for all dig modes:
- `--extreme` — expand address range from 0–50 to 0–255
- `--lwipe` — wipe the dig log file
- `--router` — include routers in the scan
- `--filter` — interactively filter result datasets
- `-s` — save dataset when data is found
- `-i LAN_IP` — target a specific LAN IP

```bash
# Search operations
dig search -f shadow -p /etc    # Search for file named "shadow" in /etc
dig search -f "\.txt$" --all    # Regex search, scan all machines (not just first match)
dig search -v shadow            # Specify file to view in result set

# Remote execution
dig -x ls -sB                   # Run "ls -sB" on all LAN computers
dig -x list "\.txt$"            # Run "list" with regex pattern on all hosts
dig -x -i 192.168.1.5 cat /etc/passwd  # Run on specific LAN IP only

# Remove file from entire network
dig -rm -f /home/guest/Bank.txt

# Scan cache management
dig cache                       # List saved scan caches
dig cache MyCache               # View cached results
dig cache MyCache --email       # View only email entries
dig cache MyCache --bank        # View only bank entries
dig cache clear                 # Clear all caches
dig cache clear MyCache         # Clear specific cache
```

**Note:** `dig` requires a LAN bounce to function. You must be operating from the router itself.

### Other Recon Tools

```bash
ping 192.168.1.1                # Test connectivity
pingport 192.168.1.1 22         # Test specific port reachability
nslookup example.com            # DNS lookup
whois 155.236.80.20             # WHOIS registration data
smtpUserList mail.com           # Enumerate SMTP user accounts
hops                            # Show current proxy hop count/route
```

**See also:** `man hunt`, `man recon`, `man dig`, `man nmap`

---

## Wireless Attacks

```bash
airmon                          # Start wireless monitor mode
aireplay                        # Replay captured wireless frames
aircrack                        # Crack WiFi encryption (WEP/WPA)
```

Typical WiFi attack workflow:
1. `hunt wifi` — find a target WiFi network
2. `airmon` — enable monitor mode
3. `aireplay` — capture traffic / deauthenticate clients
4. `aircrack` — crack the captured handshake

**See also:** `man airmon`, `man aireplay`, `man aircrack`

---

## 0day Framework

The 0day system provides access to PObject exploits — zero-day vulnerabilities tied to the Grey Hack exploit cycle.

### Mode & Status

```bash
0day mode                       # Enable 0day mode (optionally: 0day mode RSHELL_IP)
0day next                       # Show time until next 0day cycle
0day left                       # Time remaining in current cycle
```

### Credentials

```bash
0day -m                         # Manage engineer credentials (interactive)
0day -a NAME PASSWORD           # Add engineer credentials
0day -v                         # View stored credentials
0day -r 1                       # Remove credential at index 1
0day purge                      # Clear all credentials and data
0day claim USER PASS            # Claim a Neurobox account
```

### Patching Libraries

Once you have credentials from an engineer, you can patch their libraries:

```bash
0day -p libhttp.so              # Patch library (shortname: http)
0day -c libhttp.so              # Check patch status
0day -c libhttp.so true         # Check patch status (include all info)
0day -pa /lib                   # Patch all libraries in /lib folder
```

Library shortcuts: `router`, `ssh`, `ftp`, `http`, `chat`, `rshell`, `repo`, `cam`, `sql`, `smtp`, `init`, `kernel`, `net`, `apt`, `cry`, `meta`

### Neurobox Scanning

```bash
0day neuro -e you@mail.com -p pass -t TARGET -i 1.XXX.1.1
0day neuro -r                   # Random neurobox search
0day neuro --bash myscript      # Run bash script during neuro operation
```

### PObject Interpreter

After a successful 0day exploit, you enter the PObject Interpreter:

```
•[libhttp.so:1.0.3]•91.0.1.1:192.168.0.2•
PObject Interpreter :~$
```

Available commands inside the interpreter:

```bash
help             # Display available commands
libs             # List all libraries on target
scan             # Scan a port or library
meta             # Launch exploit selection
ports            # Show open ports on edge router
probe            # Check if path/file exists
main             # Execute commands from main shell context
exit             # Exit interpreter
cls              # Clear screen
```

File operations (from file partial object): `chmod`, `chown`, `chgrp`, `cp`, `mv`, `rn`, `rm`

Computer operations (from computer partial object): `mkdir`, `touch`, `passwd`, `useradd`, `userdel`, `groupadd`, `groupdel`

**See also:** `man 0day`

---

## Remote Shell — rshell

`rshell` provides persistent backdoor access to compromised machines. Once installed, a rshell phones home and you can issue commands remotely.

### Quick Start

```bash
rshell -s                       # Start rshell (auto-resolves IP from favs)
rshell -s 192.168.1.1           # Start with specific rshell server IP
rshell -s 192.168.1.1 1222 MyShell  # Custom port and name
rshell -bi                      # Build and install in one step
```

Add your rshell server to favorites for auto-connect:

```bash
favs -i YOUR_SERVER_IP rshell   # Save as "rshell" for auto-detection
rshell -s                       # Now auto-connects to favs rshell entry
```

### Building & Installing

```bash
rshell -b                       # Build rshell binary
rshell -i                       # Install an already-built rshell and launch it
rshell -bi                      # Build and install
rshell import                   # Import a rshell server configuration
```

### Managing Connections

```bash
rshell -l                       # List all active rshell connections
rshell list                     # Full rshell list with details
rshell -u 1                     # Use rshell connection ID 1
rshell -k 1                     # Kill rshell ID 1
rshell -x                       # Kill all rshells
rshell refresh                  # Refresh rshell connection data
rshell logs                     # View connection logs
rshell -h                       # Show history
rshell -h -u 1                  # History for specific rshell
rshell dump                     # Export rshell server list
```

### File Transfer

```bash
rshell -d 1 /remote/file.txt /local/   # Download from rshell 1
rshell -da /remote/file.txt /local/    # Download from ALL rshells
rshell -dc 1 /remote/file.txt          # Download to active object
rshell -p 1 /local/file.txt /remote/   # Upload to rshell 1
rshell -pa /local/file.txt /remote/    # Upload to ALL rshells
rshell -pc 1 /local/file.txt           # Upload from active object
```

Batch operations on multiple rshells:

```bash
rshell -z -u 1,2,3 file.txt /tmp/      # Upload to rshells 1, 2, 3
rshell -z -d 1,2,3 /remote/file.txt    # Download from rshells 1, 2, 3
rshell -z -k 1,2,3                     # Kill rshells 1, 2, 3
rshell -z -e 1,2,3 cat /etc/passwd     # Execute command on rshells 1, 2, 3
```

### Execute Commands

```bash
rshell -e 1 cat /etc/passwd     # Execute on rshell 1
rshell -ea cat /etc/passwd      # Execute on ALL rshells
```

### History

```bash
rshell -h                       # Show all rshell history
rshell -h -l                    # List history entries
rshell -h -u 1                  # History for rshell ID 1
rshell -h -c                    # Clear history
```

**See also:** `man rshell`

---

## Email — email

X includes a full email client for reading, sending, monitoring, and attacking email accounts.

> **Note:** One email account per session.

```bash
email -s                        # Setup / register email account
email -l user@mail.com          # Login (prompts for password)
email -l user@mail.com pass     # Login with password
email -c                        # Open email GUI client
email -v                        # View all inbox messages
email -o 5                      # Open email ID 5
email -n                        # Compose new email (interactive)
email -r 12                     # Delete email ID 12
email -x                        # Clear entire inbox
email -m user@mail.com pass 30  # Monitor inbox with 30-second auto-refresh
email -b target@mail.com "Subject" "Message" 100  # Send 100 emails (email bomb)
```

**See also:** `man email`

---

## Mission Contracts — missions

`missions` automates contract work from your email inbox. It reads emails with subject **"Mission Contract"** and handles the task automatically.

```bash
missions                        # Process all pending contracts
missions --bypass-rshell        # Skip rshell server requirement
```

### Supported Mission Types

| Type | What it does |
|------|-------------|
| **ACADEMIC** | Opens admin + student GUI apps — you modify grades manually and confirm |
| **POLICE** | Opens admin + police GUI apps — you modify records manually and confirm |
| **CORRUPTION** | Renames `/boot` to `/boots` on the target, breaking the system boot |
| **GETFILE** | Downloads the specified file from the target network |
| **DELETEFILE** | Deletes the specified file from the target network |

All mission types require a shell on the target LAN. GETFILE and DELETEFILE can use an rshell+router bounce if no direct shell is available.

**See also:** `man missions`

---

## Heists — heist

`heist` acquires root on your bank and each target, waits for your manual transfer, then corrupts `/server/transactions.log` on both. Prefers a shell already in `sess` (by id, nick, or IP).

```bash
heist                              # At prompt: sess 2
heist sess 2                       # Your bank = session id 2
heist sess bank                    # Your bank = nick "bank"
heist mybank.com 141 target.com 141
```

**See also:** `man heist`

---

## Build & Package System

### build — Compile Source Files

```bash
build script.src /home/tux/Desktop     # Compile .src to destination
build -a script.src /usr/bin           # Compile with allow-import flag
build -r program.src /home/tux         # Compile and run immediately
build -a -r tool.src /usr/local/bin    # Compile with import and run
```

### make — Binary Build & Infection Framework

`make` builds standalone tools, infects existing binaries, and creates specialty binaries.

```bash
make -l                         # List all buildable binaries
make -v BINARY                  # View binary source code
make -a                         # Build all default binaries
make -a -y                      # Build all and place in /bin
make -b ls                      # Build single binary (ls)
```

Build with infection payloads:

```bash
make -b V BINARY                # Build with virus
make -b R BINARY                # Build with rshell
make -b T BINARY                # Build with RAT (remote access trojan)
make -b P BINARY                # Build with password protection
make -b E BINARY                # Build with filesystem encryption
make -b D BINARY                # Build with filesystem decryption
make -b C BINARY                # Build with custom payload
make -b F BINARY                # Build from file content
make -b G BINARY                # Build with GCO reader (emails GCO data to you)
make -b S BINARY                # Show source before building
```

Infection of existing binaries:

```bash
make -i BINARY V                # Inject virus into binary
make -i BINARY R                # Inject rshell into binary
make -i BINARY T                # Inject RAT
make -i BINARY C                # Inject custom payload
```

Standalone tools:

```bash
make -t BINARY                  # Build as standalone tool
make -t -y BINARY               # Standalone tool, keep in current dir
make -rec                       # System recovery binary
make -r                         # Generic rshell binary
make -cs                        # Custom server frontend
make -pm                        # Proxy from Map.conf
make -pp                        # Proxy from proxy.dat
make -pc                        # Proxy with custom input
```

View source:

```bash
make -p BINARY                  # View buildable source code
```

### pacman — Package Manager

```bash
pacman -Si package              # Install package from repository
pacman -Si -m                   # Install / upgrade metaxploit.so
pacman -Si -c                   # Install / upgrade crypto.so
pacman -Si -b                   # Install / upgrade both
pacman -Ss package              # Search for package
pacman -Sv                      # Show available packages
pacman -Sl                      # List configured repositories
pacman -Sr                      # Add random repository
pacman -Sr -r 192.168.1.100 -p 1542  # Add specific repository
pacman -Sd REPO_IP              # Delete repository
pacman -Sy                      # Sync package databases
pacman -Sy -e                   # Sync exploit database (public ports)
pacman -Sy -e -f                # Force rescan of all libraries
pacman -Sy -e -c 100            # Sync exploits, 100 passes
pacman -Sy -l                   # Sync local library exploits
pacman -Su                      # System upgrade
pacman setup                    # Interactive setup
```

**See also:** `man build`, `man make`, `man pacman`

---

## Library Management — lms

LMS (Library Management System) maintains a centralized database of `.so` library files across a dedicated server. It automates exploit database updates and keeps your library collection organized.

> **Requires LMS server setup before use.** Configure with: `sys -ld`

### Database Statistics

```bash
lms stats                       # Storage, database stats, capacity
lms -lc                         # Total library count
```

### Adding Libraries

```bash
lms -a /lib/net.so              # Add single library to database
lms add /lib                    # Add all libraries from directory (recursive)
```

### Finding & Retrieving Libraries

```bash
lms -c net.so 1.0.3             # Check if library version exists
lms -c libssh.so:2.1.5          # Check with colon notation
lms -l                          # List all libraries in database
lms -g net.so 1.0.3             # Retrieve library to current directory
lms -g net.so 1.0.3 /lib        # Retrieve to specific path
```

### Removing Libraries

```bash
lms -r net.so 1.0.3             # Remove specific version
lms -ra net.so                  # Remove ALL versions of a library
```

### Updating Exploit Database

```bash
lms -u                          # Scan all libraries and import new exploits
lms -u last                     # Only test against most recent directory
lms -e                          # Exploit database update only
lms -e last                     # Exploit update, most recent directory only
lms -p                          # Pack database: scan random IPs + update exploits (10 passes)
lms -p -c 50                    # Pack with 50 passes
```

### Maintenance

```bash
lms refresh                     # Rebuild database indices
lms dups                        # Find duplicates, remove them, reorganize folders
lms -rfc                        # Recover /lib directory after crash/corruption
```

### Watching for New Libraries

```bash
lms watch                       # Monitor /lib (default, 300s interval)
lms watch -d /downloads -w 30   # Watch /downloads, check every 30 seconds
```

**See also:** `man lms`

---

## Bash Scripting — run

X includes a full-featured bash scripting engine. Scripts are stored in `/payload/data/bash/`.

### Running Scripts

```bash
run scriptname                  # Run a saved script
@scriptname                     # Shorthand syntax
run --list                      # List all saved scripts
run -e scriptname               # Edit existing script (or create new)
run -n scriptname               # Create new script without opening editor
run -o                          # Open scripts directory
run --DEBUG scriptname          # Run with debug output
run --ALLOWABS scriptname       # Allow absolute path commands
```

### Variables

```bash
_setvar(name, Alice)            # Set variable "name" to "Alice"
_getvar(name)                   # Get variable value
_print Hello, _getvar(name)!    # Print with variable substitution
```

### User Input

```bash
_setvar(name, get_string(Enter name:))       # Text input
_setvar(age, get_integer(Enter age:))        # Integer input
_setvar(val, get_decimal(Enter decimal:))    # Decimal input
```

### Control Flow

```bash
# Conditionals
if _getvar(age) >= 18 and _getvar(age) < 65
  _print Working age adult
elif _getvar(age) >= 13
  _print Teenager
else
  _print Child or senior
endif

# While loop
_setvar(i, 0)
while _getvar(i) < 10
  _print _getvar(i)
  _setvar(i, _getvar(i) + 1)
endwhile

# Until loop (runs until condition is true)
_setvar(ready, 0)
until _getvar(ready) == 1
  _print Waiting...
  _setvar(ready, get_integer(Ready? 1=yes:))
enduntil

# For loop over list
for item in [apple, banana, orange]
  _print _getvar(item)
endfor

# For loop with range
for i in range(1, 10)
  _print _getvar(i)
endfor

# Switch statement
switch _getvar(choice)
  case 1
    _print Option one
  case 2
    _print Option two
  default
    _print Unknown option
endswitch
```

### Functions

```bash
func add(x, y)
  _return _getvar(x) + _getvar(y)
endfunc

func greet(name)
  _print Hello, _getvar(name)!
endfunc

# Call a function
_setvar(result, add(5, 3))
_print Result: _getvar(result)
greet(World)
```

Recursion is supported up to 10 levels deep with full local scope.

### Error Handling

```bash
try
  scan --c $1 router s
catch err
  _print Failed: _getvar(err)
end try

_throw Connection failed       # Raise an error inside try block
```

### Array Operations

```bash
_setvar(items, [apple, banana])
_push items orange              # Append to end
_pop items                      # Remove from end
_pull items                     # Remove from start
_len mylist                     # Get length
_in mylist apple                # Check if value exists: returns 0 or 1
```

### Built-in Functions

**String:** `len()`, `upper()`, `lower()`, `substr()`, `concat()`, `contains()`, `replace()`, `trim_str()`, `split_str()`

**Math:** `floor()`, `ceil()`, `abs()`, `round()`, `min()`, `max()`, `random()`

**File:** `file_exists()`, `is_folder()`, `is_binary()`, `_fs_read()`, `get_permissions()`

**Context:** `get_user()`, `get_home()`, `get_shell_type()`, `get_root()`, `get_computer_lan_ip()`, `get_computer_public_ip()`, `get_layer()`

**Type conversion:** `to_string()`, `to_int()`, `to_float()`, `typeof()`

**Map/JSON:** `map()`, `map_set()`, `map_get()`, `map_del()`, `map_has()`, `map_keys()`, `map_values()`, `json()`, `json_parse()`, `map_save()`, `map_load()`

**Time:** `timestamp()`, `date()`

**Built-in variables in scripts:**

| Variable | Description |
|----------|-------------|
| `COMPUTER` | Current session computer object (`.local_ip`, `.public_ip`, `.get_name`, etc.) |
| `$1 $2 ...` | Script arguments |

**See also:** `man run`, the [Bash User Handbook](bash_user_handbook.md)

---

## AI Agent — ai

X includes a natural language AI agent. Describe what you want to do in plain English and the agent plans and executes it.

### Basic Commands

```bash
ai scan 192.168.1.1             # Scan a target
ai show me /etc/passwd          # Read a file
ai copy test.txt to backup.txt  # File operation
ai delete oldfile.txt           # Delete file
ai list files in /home          # List directory
ai change permissions of myfile to 644
```

### Execution Modes

```bash
ai "exploit target" -v          # Verbose: show detailed steps
ai "scan -l" -q                 # Quiet: minimal output
ai "scan 192.168.1.1" -d        # Dry-run: show plan, don't execute
ai "attack target" -a           # Aggressive: try all methods
ai "scan target" -s             # Stealth: minimize traces
ai "what is chmod" -t           # Trainer: show commands without running
ai "scan target" -D             # Debug: show internal decision making
```

### Agent Management

```bash
ai status                       # Show agent status, sessions, config
ai history                      # Show command history
ai clear                        # Full reset
ai clear stored                 # Clear stored knowledge only
ai clear 5                      # Clear last 5 history entries
```

### Training

```bash
ai learn scan                   # Learn from scan man page (--e/--l/--b flags, etc.)
ai learn all                    # Wipe old agent_knowledge*.json and regenerate from all man pages
```

`ai learn all` deletes every `agent_knowledge_*.json` under data/ai/, clears the in-memory cache, then rebuilds from man pages. Planning consults those OPTIONS and prefers **`--` bash autos** (`--b`, `--e`, `--l`, `--c`, `--n`, `--s`) — those set `$scan_ok` / `$hold` for scripting.

### Configuration

```bash
ai show config                  # Show current configuration
ai reset config                 # Reset to defaults
ai set max_attempts 10          # Set a config value
ai debug / verbose / quiet      # Toggle output modes
```

### Save & Restore

```bash
ai save                         # Save agent configuration
ai load                         # Load saved configuration
ai undo                         # Undo last agent action
ai undo 5                       # Undo last 5 actions
ai rollback 3                   # Rollback to state 3 steps ago
ai snapshots                    # List available rollback snapshots
ai export                       # Export agent state to file
ai telemetry                    # Export telemetry data
```

**See also:** `man ai`, the [AI User Handbook](ai_user_handbook.md)

---

## Configuration — config, alias, favs

### config — Framework Settings

```bash
config -c                       # Create config file
config status                   # View all current settings
config run                      # Interactive settings menu
config on                       # Enable all options
config off                      # Disable all options
config --reset                  # Reset to defaults
```

Individual toggles:

| Flag | Effect |
|------|--------|
| `-a` | Auto-solve PObjects |
| `-k` | PObject solver debug output |
| `-g` | Debug output mode |
| `-m` | Update metaxploit on launch |
| `-e` | Auto-clear exploit scan buffer |
| `-p` | Build rainbow index on launch |
| `-s` | Auto-add sessions to cache |
| `-i` | Dirty router IP logging |
| `-l` | Dynamic LAN IP tracking |
| `-y` | Proxy log for crash recovery |
| `-h` | Short home path in prompt |
| `-z` | Fast path home |
| `-r` | Auto-reset password |
| `-b` | Binary scan library |
| `-v NAME` | Set bounce library name |
| `-x INDEX` | Set exploit index |
| `-w` | Toggle wide display mode |

### alias — Command Shortcuts

```bash
alias -s gs "grep -i"           # Create alias: gs → grep -i
alias -l                        # List all aliases
alias -r ll                     # Remove alias "ll"
alias --clear                   # Remove all aliases
```

### favs — Trusted IP Addresses

`favs` stores frequently used IP addresses. The special nickname `rshell` is used by `rshell -s` for auto-connection.

```bash
favs                            # List all favorites
favs -i 222.222.222.222 rshell  # Add your rshell server
favs -i 198.51.100.42 homebase  # Add home base server
favs -r 0                       # Remove entry at index 0
favs -e                         # Edit existing entries
```

**See also:** `man config`, `man alias`, `man favs`

---

## File Operations

### Viewing & Editing

```bash
cat file.txt                    # Display file contents
vi file.txt                     # Edit file (built-in editor)
vfile file.txt                  # View file (read-only)
head -n 20 file.txt             # First 20 lines
tail -n 10 file.txt             # Last 10 lines
diff file1.txt file2.txt        # Compare two files
```

### mc — Interactive File Manager

`mc` is a full-featured interactive file explorer with sorting, filtering, permission management, and optional dual-panel mode for side-by-side directory operations.

```bash
mc                              # Open in current directory
mc /home/tux                    # Open a specific directory
mc -d                           # Dual panel mode
mc -d /home/tux /var            # Dual panel with specific paths
```

Inside `mc`, available operations include: rename, new file/directory, delete, change permissions (octal or symbolic), sort by name/size/date, filter by name, toggle hidden files, and search recursively. In dual panel mode, `[X]` marks the active panel and you can copy or move files between panels with a progress indicator.

### mc — SSH Remote Access

Each panel can independently connect to a remote SSH server, turning `mc` into a cross-server file manager:

```bash
# From inside mc: open Options Menu → Connect to SSH
# Enter: IP, port (default 22), username (default root), password
# Panel header shows: username@IP once connected
# Options Menu → Disconnect SSH to return to local filesystem
```

- **Copy/Move between panels** — works across two SSH sessions using SCP
- **Cross-server transfers** — both panels can be on different remote machines simultaneously
- Both panels need shell access for cross-server operations; disconnect returns to your home directory

**Keyboard shortcuts (from Options Menu):** `s` connect SSH, `d` disconnect SSH, `c` copy, `m` move, `p` switch panel, `2` dual panel, `1` single panel, `e` execute command, `D` delete, `R` rename, `M` change permissions, `f` search, `F` filter, `q` quick nav, `x` exit.

**See also:** `man mc`

### Copying, Moving, Deleting

```bash
cp source dest                  # Copy file
cp -r folder/ backup/           # Copy directory recursively
mv old new                      # Move or rename
rm file.txt                     # Delete file (creates log entry)
rm -r folder/                   # Delete directory recursively
qrm file.txt                    # Quiet delete (no log entry)
qrm file1 file2 folder/         # Quiet delete multiple
```

### Creating

```bash
mkdir folder                    # Create directory
touch file.txt                  # Create empty file
ln source /path/link            # Create symbolic link
ln -l                           # List all symbolic links
```

### Compression

```bash
zip file.txt                    # Compress file with zip
gzip file.txt                   # GZip compress
tar folder/                     # Create tar archive
pzip file.txt                   # Password-protected zip
rsync source dest               # Remote sync
```

### File Info

```bash
file scanner                    # Show file type, permissions, owner, size
stat file.txt                   # Detailed file statistics
disk                            # Disk usage summary
find -n *.log                   # Find all .log files
find -n config -p /etc          # Find "config" files under /etc
find /home *.log *.cfg          # Find .log OR .cfg files in /home
locate keyword                  # Fast indexed search (searches everywhere)
```

### Remote File Access

```bash
grab                            # Download router log (port 0)
grab -p 22                      # Download SSH log
grab -p 21 -w                   # Download FTP log and wipe it
scp -d /remote/file.txt         # Download via SSH
scp -u /local/file.txt          # Upload via SSH
```

**See also:** `man find`, `man locate`, `man grab`, `man cp`, `man mv`, `man rm`, `man mc`

---

## Text Processing & Pipes

X supports Unix-style pipe chains. Connect commands with `|` to filter and transform output.

```bash
cat /etc/passwd | grep root | cut -d: -f1
ps | sort | uniq | wc -l
nmap 192.168.1.1 | grep open | awk '{print $1}'
cat file.txt | head -n 20 | tail -n 5
echo "5 + 3" | bc
```

### Pipe Variables

```bash
set VAR value                   # Store a value in a variable
cat file.txt | set CONTENT      # Capture command output into variable
echo "$VAR"                     # Use variable
echo "${NUM}nd"                 # Braces for word-boundary clarity
env                             # List all shell variables
unset VAR                       # Delete variable
```

### Text Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `grep` | Search text patterns | `grep "error" log.txt` |
| `grep -i` | Case-insensitive search | `grep -i "failed" log.txt` |
| `grep -v` | Invert match | `grep -v "ok" log.txt` |
| `sed` | Find and replace | `echo "hello" \| sed s/hello/world/` |
| `awk` | Field extraction | `awk '{print $2}' file.txt` |
| `cut` | Extract columns | `cut -d: -f1 /etc/passwd` |
| `sort` | Sort lines | `sort file.txt` |
| `sort -r` | Reverse sort | `sort -r file.txt` |
| `sort -n` | Numeric sort | `sort -n numbers.txt` |
| `uniq` | Remove duplicate lines | `sort file.txt \| uniq` |
| `uniq -c` | Count occurrences | `sort file.txt \| uniq -c` |
| `wc` | Count words/lines/chars | `wc -l file.txt` |
| `wc -w` | Word count | `wc -w file.txt` |
| `tr` | Translate characters | `echo "hello" \| tr a-z A-Z` |
| `head` | First N lines | `head -n 5 file.txt` |
| `tail` | Last N lines | `tail -n 5 file.txt` |
| `rev` | Reverse text | `echo "hello" \| rev` |
| `trim` | Strip whitespace | `echo " hi " \| trim` |
| `column` | Format as columns | `cat data.txt \| column` |
| `tee` | Output to file + stdout | `ls \| tee list.txt` |
| `split` | Split string | `echo "a:b:c" \| split :` |
| `join` | Join strings | `echo "a b c" \| join -` |
| `seq` | Generate number sequence | `seq 1 10` |
| `printf` | Formatted output | `printf "%d items\n" 5` |
| `paste` | Merge lines | `paste file1 file2` |
| `xclip` | Copy to clipboard | `cat file.txt \| xclip` |
| `bc` | Math calculator | `echo "2^10" \| bc` |

### Debug Mode

```bash
debug on                        # Show pipe internals (token parsing, routing)
debug off                       # Return to normal mode
debug status                    # Show current debug state
```

---

## Surveillance & Monitoring

### cam — Camera Systems

```bash
cam -a                          # Access camera system GUI (switch between cameras)
cam -c                          # Get camera admin NPC name (needed for -v)
cam -v ABC123 password          # Locate vehicle by license plate
```

### app — Smart Appliances

```bash
app -m                          # View appliance model information
app -o                          # Override with defaults (power: 500, temp: 50)
app -o 1000 75                  # Override power to 1000, temperature to 75
app -a on                       # Enable malfunction alarm
app -a off                      # Disable malfunction alarm
```

### sniffer — Network Packet Capture

```bash
sniffer                         # Live packet capture (credential harvesting)
sniffer --save                  # Capture and save encode.src to current directory
sniffer --deploy                # Deploy as standalone background sniffer
```

### gmon — Directory Monitor

```bash
gmon                            # Monitor /home/guest (default)
gmon -p /home/tux               # Monitor specific directory
gmon --deploy                   # Launch as background process
```

### fw — Folder Watcher

```bash
fw /home/tux/watched            # Watch folder, alert on changes (10s interval)
fw /var/log 5                   # Watch with 5-second refresh
```

### ids — Intrusion Detection

```bash
ids                             # Start IDS (monitors processes, filesystem, router)
ids > ids.log                   # Log alerts to file
```

### devices — List Available Devices

```bash
devices                         # Show all available devices
```

**See also:** `man cam`, `man app`, `man sniffer`, `man gmon`, `man fw`, `man ids`

---

## Offensive Toolkit

### ddos — Denial of Service

```bash
ddos -d                         # Unlimited rshell flood (zombie connections)
ddos -r 1000                    # Flood with 1000 rshell connections
ddos -ff                        # Unlimited file flood
ddos -f 5000                    # Flood with 5000 files
ddos -c 10                      # Hardware grind (10 decipher cycles)
ddos -p -c 100 -p 80 192.168.1.1  # Port flood attack
ddos -b                         # Hardware tuning (fine-grained health consumption)
```

### inject — Source Code Backdoor

Inject a rshell backdoor into a source file:

```bash
inject -i HOST -p 1222 -n sshd exploit.src   # Inject rshell into source file
inject -n apache -i HOST -p 4444 web.src      # Flexible parameter order
inject help malware.src                        # Interactive guided injection
```

The `help` mode pulls the rshell server IP from your favorites automatically.

### sk — Website Defacement

```bash
sk                              # Deface active computer's website (default content)
sk -f /home/tux/custom.html     # Deface with custom HTML file
sk -w                           # Write default template to data folder
sk -w -n mypage -p /server      # Write template as "mypage" to /server
```

### rat — Remote Access Trojan Management

`rat` manages your RAT file on a remote C2 server. Requires `/root/rat` on the C2.

```bash
rat 136.22.27.184 22 password   # Connect to RAT server
rat 136.22.27.184 22            # Prompt for password
rat                             # Prompt for all connection details
```

Build a RAT-infected binary with `make -b T BINARY`.

### dirty — Router Log Tracking

Track which routers still have uncleaned logs (your "dirty" trail):

```bash
dirty -l                        # List unclean routers
dirty -c                        # Count dirty routers
dirty -a                        # Add current router to dirty list
dirty -s                        # Scrub logs on all tracked routers
dirty -m                        # Manual buffer cleaning
dirty -r                        # Reload buffer from storage
dirty -x                        # Clear entire dirty buffer
```

Enable automatic tracking with `config -i`.

**See also:** `man ddos`, `man inject`, `man kiddy`, `man rat`, `man dirty`

---

## Cryptography & Encoding

### aes128 — AES Encryption

```bash
aes128                          # Interactive AES128 encrypt/decrypt
```

### sha256 — SHA256 Hashing

```bash
sha256 "mystring"               # Hash a string
echo "text" | sha256            # Hash from pipe
```

### encrypt / decrypt

```bash
encrypt file.txt                # Encrypt file
decrypt file.txt.enc            # Decrypt file
decipher                        # Decipher mode
```

### Base Conversion

```bash
binary 255                      # Decimal to binary: 11111111
hex 255                         # Decimal to hex: ff
decimal 0xff                    # Hex to decimal: 255
radix 2 16 11111111             # Convert between bases (binary → hex)
```

### Bitwise Operations

```bash
bit and 0xFF 0x0F               # Bitwise AND
bit or 0x0F 0xF0                # Bitwise OR
bit xor 0xFF 0x0F               # Bitwise XOR
bit not 0xFF                    # Bitwise NOT
```

### l33t — Leet Speak

```bash
l33t "hello world"              # Convert to 1337: h3ll0 w0rld
echo "text" | l33t              # From pipe
```

**See also:** `man aes128`, `man sha256`, `man encrypt`, `man decrypt`, `man binary`, `man hex`, `man decimal`, `man bit`

---

## Stealth & Anti-Forensics

### wipe — Clear Logs & Traces

```bash
wipe -x                         # Wipe X framework traces
wipe -c                         # Wipe X config files
wipe -m                         # Wipe proxy chain logs (Map.conf entries)
wipe -l                         # Wipe local system log
wipe -lx                        # Wipe log with ASCII X graphic
wipe -lc                        # Wipe log with custom ASCII (from /payload/data/ascii)
wipe -lt                        # Wipe log with custom text (prompted)
wipe -b                         # Wipe boot folder (system.log if accessible)
wipe -b yes                     # Wipe boot with auto-confirm
wipe -s                         # Wipe entire filesystem (DESTRUCTIVE)
wipe -a                         # Wipe all
wipe --deploy 60                # Deploy delayed log wiper (fires after 60 seconds)
```

### qrm — Quiet File Removal

```bash
qrm file.txt                    # Delete without creating a log entry
qrm exploit.src backdoor.bin    # Delete multiple files silently
qrm /root/attack_tools/         # Delete entire folder silently
```

### hide — File System Obfuscation

```bash
hide -s                         # Toggle root filesystem directory visibility
hide -s -c _ -n 10              # Show as "__________/bin..." (10 underscores)
hide -s -c .- -n 10             # Show as ".-.-.-.-.-/bin..."
hide -f /root/exploit.src       # Toggle individual file visibility
hide -t                         # Toggle .Trash folder visibility
```

### scrub — Config Cleanup

```bash
scrub                           # Remove all files from Config folder
                                # (prompts for Map.conf and Browser.txt)
```

### grab — Download & Wipe Logs

```bash
grab                            # Download router log (port 0)
grab -p 22                      # Download SSH log
grab -w                         # Download and wipe router log
grab -p 21 -w                   # Download FTP log and wipe it
grab -p 80 -w                   # Download HTTP log and wipe it
```

### anon — Streaming Mode

```bash
anon                            # Toggle streaming mode (hides passwords from output)
```

**Stealth Workflow:**

```bash
# After any attack:
dirty -a                        # Track this router
wipe -l                         # Clear local log
grab -w                         # Download and wipe router log
dirty -s                        # Scrub all tracked dirty routers
```

**See also:** `man wipe`, `man qrm`, `man hide`, `man scrub`, `man grab`

---

## System Utilities

### Process Management

```bash
ps                              # List running processes
htop                            # Interactive process monitor
htop --deploy                   # Install htop on target then launch
kill 1234                       # Kill process by PID
kill -a bash                    # Kill all processes named "bash"
lsof                            # List open files / processes
spawn                           # Spawn a new X instance
spawn -p                        # Spawn as root (password prompt)
spawn -u tux                    # Spawn as user tux
```

### System Control

```bash
reboot                          # Restart the system
reboot -s                       # Reboot in safe mode
check                           # Verify and auto-fix user assignment
```

### Web & Services

```bash
web                             # Start private HTTP interweb service
open -b                         # Open browser application
open -e                         # Open mail application
open -t                         # Open terminal
open -f                         # Open file explorer
open -c                         # Open code editor
open -a                         # Open admin monitor
open -k                         # Open stocks viewer
open -x                         # Open exploit viewer
open -p                         # Open police records
open -u                         # Open student records
open -r                         # Open traffic records
open -y                         # Open employee records
```

Use `--l` flag with `open` to open applications from the main system when on a pivot/shell.  
Use `--deploy` to SCP an app from your `/usr/bin` to the target, launch, then clean up.

### Personal Tools

```bash
notes                           # Open notepad
mark                            # Bookmark manager
wallet                          # Cryptocurrency wallet
wallet -u hacker                # Login to wallet
wallet --create                 # Create new wallet
coin                            # Coin flip
cal                             # Calendar
date                            # Current date/time
bc                              # Calculator (interactive or pipe: echo "2^10" | bc)
repl                            # Interactive REPL shell
```

### Utilities

```bash
wait 5                          # Pause for 5 seconds
time cat /etc/passwd            # Time a command
clean                           # Clean temporary files
swap                            # Manage swap space
temp                            # View CPU temperature
index                           # Build file index
cache                           # View/manage system cache
```

### Networking Info

```bash
ifconfig                        # Network interfaces
iwconfig                        # Wireless interface config
iwlist                          # List wireless networks
hops                            # Show proxy hop count and route
dig cache                       # View cached LAN scan data
```

### Security

```bash
audit                           # Run full security audit (score out of 100)
audit -q                        # Quick audit (filesystem + accounts only)
audit -p                        # Ports only
audit -r                        # Processes only
ids                             # Start intrusion detection monitoring
```

**See also:** `man audit`, `man ids`, `man spawn`, `man reboot`, `man open`, `man wallet`

---

## Common Workflows

### Scan → Exploit → Root → Cover Tracks

```bash
nmap 192.168.1.1                # 1. Find open ports
scan 192.168.1.1                # 2. Scan for vulnerabilities (pick shell exploit)
dict -l                         # 3. Crack passwords from inside the shell
su root                         # 4. Escalate to root
su -w                           # 5. Wipe system log
grab -w                         # 6. Download and wipe router log
```

### Build a Proxy Chain Before Attacking

```bash
hunt ssh -c 3                   # Find 3 SSH targets
scan -p TARGET1 22              # Exploit first
pivot -y                        # Pivot to target 1
scan -p TARGET2 22              # Exploit second
proxy -a                        # Start proxy chain through compromised routers
```

### Mass LAN Data Collection

```bash
scan 1.2.3.4                    # Exploit the target's router (get router shell)
# Now on the router:
dig -a --lwipe -s               # Collect all data from all LAN computers
dig cache                       # Review collected datasets
dig -x cat /etc/passwd          # Run commands on all LAN hosts
```

### Pivot to Internal Network

```bash
scan 192.168.1.1                # Exploit the edge router
pivot --full                    # Full pivot (upload everything to their system)
# Now operating as X on their network:
scan -n                         # Discover all internal machines
scan -l                         # Check for local privilege escalation
dig -a                          # Crawl the entire LAN
```

### Automated Mission Workflow

```bash
email -l you@mail.com           # Login to email
email -v                        # Check for mission contracts
missions                        # Auto-process all mission contracts
```

### Password Cracking Chain

```bash
# Initialize (one-time setup):
rainbow -n                      # Initialize tables
config -p                       # Auto-load rainbow on startup

# At runtime:
scan 192.168.1.1                # Get a shell
dict -l                         # Dictionary attack on localhost
su root                         # Login with cracked password
shadow -l                       # Check cached passwords
```

### Exploit Database Maintenance

Run these regularly to keep your exploit DB fresh:

```bash
exp backup                      # Always backup first
exp all -p 50                   # Generate new versions for all services
pacman -Sy -e -c 100            # Sync from public repositories
exp defrag                      # Clean orphaned entries
exp bloom rebuild               # Rebuild bloom filter
```

### Build & Infect Workflow

```bash
make -l                         # See what you can build
make -b ls                      # Build a clean "ls" binary
make -i ls R                    # Infect it with rshell
# Deploy to target:
scp -u ls                       # Upload to target
# When target runs ls, it phones home to your rshell server
```

### Bank Heist Workflow

```bash
scan TARGET_BANK                # Get a shell on the target bank
heist -t TARGET_BANK -b MY_BANK # Run heist automation
email -v                        # Check for transaction notifications
wallet -u me                    # Check wallet balance
```

---

## Troubleshooting

### Exploit Database Issues

```bash
exp refresh                     # Refresh database indices
exp defrag                      # Remove orphaned entries
exp bloom rebuild               # Rebuild bloom filter
exp backup                      # Backup first, then:
exp restore                     # Restore from last good backup
```

### Rainbow Table Issues

```bash
rainbow -r                      # Rebuild from wordlists
rainbow -n                      # Re-initialize fresh (prompts for path)
config -p                       # Enable auto-load rainbow on startup
```

### Session Crashes

- Enable `config -y` (proxy crash recovery log)
- Use decoys: `proxy -d`
- Re-establish: `proxy -q`

### Permission Denied

```bash
su root                         # Try switching to root
su -b                           # Brute force root password
su -d                           # Dictionary attack on root
scan -l                         # Find local privilege escalation exploits
scan -lp                        # Include 0day in local scan
```

### Missing Libraries

```bash
sys check                       # Auto-detect and install missing libraries
pacman -Si metaxploit.so        # Manually install metaxploit
pacman -Si crypto.so            # Manually install crypto
```

### User Assignment Corrupted

```bash
check                           # Verify and auto-fix current user assignment
```

### Logs Still Show Your Activity

```bash
dirty -l                        # Check what routers are tracked as dirty
dirty -s                        # Scrub all tracked router logs
grab -w                         # Download and wipe router log (port 0)
grab -p 22 -w                   # Also wipe SSH log
wipe -l                         # Wipe local log
```

### Always Use a Proxy

Run `proxy -q` or `proxy -a` before attacking any target. Without it, your real IP appears in every target's log. Bad things happen.

```bash
proxy -q                        # Quickest way to start — single router hop
```

---

## Credits

X was created with contributions from:

- **fantom**, **subnet**, **microx** — Core concepts
- **Nyx**, **3nigma**, **KEKE** — GUI and code inspiration
- **JoeStrout** — JSON Parser
- **bloodwhite** — Main debugger
- **Jessa**, **IDelta** — 0day countdown and solver
- **GSQ**, **tyy** — PObject code
- **Olipro**, **usesPython** — Code innovations and corrections
- **gk258** — Innovations
- **Volk** — SSH encryption
- **Chrome** — Math/String libraries
- **Clover** — Crypto functions and innovations
- **maho citrus** — Blockchain and REPL terminal
- **JessaTehCrow** — Text formatting
- And many others from the Matrix/Discord community

---

**Version:** 0.9.7.8-4  
**More docs:** [user_guide.md](user_guide.md) · [bash_user_handbook.md](bash_user_handbook.md) · [ai_user_handbook.md](ai_user_handbook.md) · [pipe_handbook.md](pipe_handbook.md) · [x_man_pages.md](x_man_pages.md)
