# X — User Guide

A comprehensive hacking framework for Grey Hack. Scan targets, exploit vulnerabilities, crack passwords, pivot through networks, automate tasks with bash scripts, and control it all with an AI assistant — from a single shell.

---

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Shell Basics](#shell-basics)
- [Port Scanning](#port-scanning)
- [Vulnerability Scanning](#vulnerability-scanning)
- [Exploit Database](#exploit-database)
- [Password Cracking](#password-cracking)
- [Privilege Escalation](#privilege-escalation)
- [Remote Access (SSH / FTP)](#remote-access-ssh--ftp)
- [Session Management](#session-management)
- [Proxy Chains](#proxy-chains)
- [Pivoting](#pivoting)
- [Network Reconnaissance](#network-reconnaissance)
- [Wireless Attacks](#wireless-attacks)
- [0day Framework](#0day-framework)
- [Remote Shell (RShell)](#remote-shell-rshell)
- [Email](#email)
- [Mission Contracts](#mission-contracts)
- [Heists](#heists)
- [File Operations](#file-operations)
- [Text Processing & Pipes](#text-processing--pipes)
- [Bash Scripting](#bash-scripting)
- [AI Agent](#ai-agent)
- [Configuration](#configuration)
- [Utilities](#utilities)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)

---

## Installation

### Requirements

- Grey Hack (the game)
- `metaxploit.so` — required for scanning and exploitation
- `crypto.so` — required for password cracking
- `aptclient.so` — required for package management
- `librshell.so` — required for remote shells

### Download & Install

X is hosted at **218.201.114.152**. To install:

```bash
apt-get install x /home/YOUR_USERNAME
apt-get install exploits /home/YOUR_USERNAME
apt-get install bash /home/YOUR_USERNAME
apt-get install man /home/YOUR_USERNAME
apt-get install passwords /home/YOUR_USERNAME
```

Replace `YOUR_USERNAME` with your in-game home directory name.

### First-Time Setup

After installing, launch X once, then run these commands:

```bash
exploits          # Install exploit database
bash              # Install bash scripts
man               # Install man pages
passwords         # Install password lists
```

Then initialize your password tables:

```bash
rainbow -n        # Build rainbow tables from wordlists
```

Verify everything is working:

```bash
sys check         # Auto-install any missing libraries
```

### Optional Setup

```bash
ai learn all      # Teach the AI agent all commands (recommended)
config -p          # Build rainbow index on launch
exp backup         # Backup your exploit database (do this regularly!)
```

---

## Getting Started

Launch X by running the compiled binary. You go straight into the X shell with 100+ built-in commands.

The prompt shows your context at a glance:

```
•[MAIN]•[P]••[tux~Workstation@92.11.2.162192.168.0.2] [/home/tux]
•   •:~$
```

- **MAIN** — your current session layer (MAIN, PROXY, PIVOT, etc.)
- **P** — passwd file status: green = you can read it, red = no read access, red X = passwd file is missing
- **tux~Workstation** — current user and system type (Workstation, Router, or Switch)
- **92.11.2.162:192.168.0.2** — public IP and LAN IP
- **/home/tux** — current directory

Type `?` or `man <command>` at any time for help:

```bash
man scan          # View scan documentation
man ai            # View AI documentation
man hunt          # View hunt documentation
```

---

## Shell Basics

### Navigation

```bash
ls                # List files (automatically shows full details)
cd /path          # Change directory
pwd               # Print current directory
tree              # Show directory tree
```

### File Management

```bash
cat file.txt      # View file contents
cp src dest       # Copy file
cp -r folder/ backup/  # Copy directory recursively
mv old new        # Move or rename file
rm file.txt       # Delete file
rm -r folder/     # Delete folder recursively
mkdir folder      # Create directory
touch file.txt    # Create empty file
vi file.txt       # Edit file in text editor
file scanner      # Show file info (path, permissions, owner, type, size)
find -n *.txt     # Search whole system for files
find --text readme  # Search for text files by name
find -n config -p /etc  # Search in specific directory
```

### Permissions

```bash
chmod 755 file    # Change permissions (rwxr-xr-x)
chmod u-rx file   # Remove user read+execute
chown root file   # Change file owner
chgrp admin file  # Change file group
```

### User Management

```bash
whoami            # Show current user
useradd newuser   # Create user
userdel user      # Delete user
passwd            # Change password
groups            # Show groups
```

### System Info

```bash
hostname          # Show hostname
ifconfig          # Show network interfaces
uptime            # Show uptime
neofetch          # System info with ASCII art
ps                # List running processes
kill 1234         # Kill process by PID
kill -a bash      # Kill all bash processes
lsof              # List open files/processes
reboot            # Reboot (requires root)
```

---

## Port Scanning

### Quick Scan (nmap)

Scan a target's open ports — like `nmap`:

```bash
nmap 192.168.1.1          # Scan specific IP
nmap example.com          # Scan domain
nmap -l                   # Scan localhost
nmap -p                   # Scan your public IP
nmap -r                   # Scan random IP
nmap -w 155.236.80.20     # Scan with whois data
```

Output shows open ports, services, versions, and LAN IPs.

---

## Vulnerability Scanning

### scan — The Main Attack Command

`scan` is the core command. It finds open ports, tests for vulnerabilities, and lets you exploit them.

```bash
scan 192.168.1.1          # Scan IP for vulnerabilities
scan example.com          # Scan domain
scan -l                   # Scan localhost
scan -lp                  # Scan localhost with 0day exploits
scan -n                   # Scan local network
scan -r                   # Scan random target on network
```

#### Targeted Scanning

```bash
scan -p 192.168.1.1 22        # Attack specific port (SSH)
scan -p 192.168.1.1 http      # Attack by service name
scan -pd /lib                 # Scan a library folder for exploits
```

#### Smart Scanning

```bash
scan --n apt c                # Network scan using aptclient for computer exploits
scan --l libssh.so 2          # Local scan with specific library and exploit index
scan --e shell                # Search all libraries for shell exploits
scan --e computer -u root     # Search for root computer exploits
scan --c 192.168.1.1 libssh.so c  # Connect to IP with specific library
```

#### Mass Scanning

```bash
scan -a                       # Scan all public IPs (1.0.0.0 to 255.255.255.255)
scan -a -s 10.0.0.0 -e 10.255.255.255  # Scan a specific IP range
```

#### Other Flags

```bash
scan -d                   # Disable all local network firewalls
scan -nf                  # Show network firewall status
scan -nd                  # Disable network firewalls
scan -b -p IP -l LAN_IP   # Binary scan between public and LAN IPs
```

#### Exploit Types

When scanning finds vulnerabilities, each exploit is classified:

| Type | Description |
|------|-------------|
| **shell** | Full command-line access to the target |
| **computer** | File system access on the target |
| **file** | Access to a single file |
| **bounce** | Redirect through a router to reach another IP |
| **null** | May need a parameter, or could be a password-change exploit |

After selecting an exploit, you enter the **post-exploitation menu** where you can crack passwords, browse files, escalate privileges, and more.

---

## Exploit Database

### exp — Manage Your Exploits

Your exploit database stores discovered vulnerabilities for reuse.

```bash
exp -l                    # List all exploits
exp -d                    # Dump libraries to file
exp refresh               # Refresh exploit database
exp backup                # Backup database
exp restore               # Restore from backup
exp defrag                # Clean up orphaned indexes
```

#### Search Exploits

```bash
exp -f -n =:init          # Search by name
exp -f -v >:1.0.3         # Search by version (greater than 1.0.3)
exp -f -e shell           # Search by exploit type
exp -f -u root            # Search by user level
exp -f -m 0x69F89F6       # Search by memory address
exp -f -s searchstring    # Search by value
```

#### View & Manage

```bash
exp -p 7                  # View all exploits at index 7
exp -p 7 2                # View specific exploit
exp view -l libssh.so -v 1.0.5  # View by library and version
exp -r -i 7 -l lib -v 1.0.0     # Remove exploit
```

#### Generate New Library Versions

```bash
exp router                # Generate new router library versions
exp ssh                   # Generate new SSH library versions
exp http                  # Generate new HTTP library versions
exp ftp                   # Generate new FTP library versions
exp smtp                  # Generate new SMTP library versions
exp all                   # Generate new versions for all services
```

#### Bloom Filter

```bash
exp bloom -s              # Show bloom filter statistics (saturation, false positive rate, item count)
exp bloom -a              # Analyze bloom filter distribution and bit patterns
exp bloom reset           # Reset bloom filter to zeros
exp bloom rebuild         # Rebuild bloom filter from cache
```

#### Grind — Generate New Library Version

Grinding runs a specific exploit repeatedly. After 35 runs, it generates a new version of the library.

```bash
exp grind -l libhttp.so 0x1234 "Value"              # Grind local library
exp grind -r 192.168.1.1 libhttp.so 0x1234 "Value"  # Grind remote library
```

---

## Password Cracking

### Dictionary Attacks

```bash
dict -l                   # Dictionary attack on localhost
dict -l -u admin          # Attack specific user
dict -s 192.168.1.1 22    # SSH dictionary attack
dict -s -u root 192.168.1.1 22   # SSH attack on specific user
dict -f 192.168.1.75 21   # FTP dictionary attack
dict -e user@mail.com     # Email account attack
dict -c btc admin         # Crypto wallet attack
dict -lp                  # Print cracked password
dict -i                   # Cache cracked password
```

Partial dictionary scans:

```bash
dict -e --start 0 --stop 1000 admin@mail.com        # Try first 1000 passwords
dict -c --start 5000 --stop 10000 btc admin          # Try passwords 5000-10000
```

### Rainbow Tables

```bash
rainbow -l                # Load tables into memory
rainbow -r                # Rebuild from lists
rainbow -n                # Initialize tables (prompts for list location)
rainbow -x                # Clear all tables
```

Generate passwords:

```bash
rainbow -m uln 8 50000       # 50k passwords, 8 chars, upper+lower+numbers
rainbow -m ulnR 15 100000    # 100k passwords, 1-15 length, random
rainbow -k 2 50000           # Markov chain order-2, 50k passwords
rainbow -k 3 25000           # Markov order-3 (most realistic)
rainbow -k 2 50000 -s        # Markov order-2, save to list directory
```

### Brute Force

```bash
su -b                     # Brute force root password
su -b -c                  # Try capitals-first passwords
su -b -C                  # Mixed-case first character
su -b -n                  # Letters only (no digits)
su -b -N                  # Digits only (0-9)
su -d                     # Dictionary attack via su
```

---

## Privilege Escalation

### su — Switch User

```bash
su root                   # Switch to root
su -r                     # Attempt root elevation
su -u USER PASSWORD       # Login as user with known password
su -s                     # Start user shell
su -s tux                 # Start shell as specific user
su -t                     # Terminal with user permissions
su -l                     # Re-launch X as this user
su -e rm file.txt         # Execute command as user
su -w                     # Wipe system log
su -p                     # Print passwd file
```

### Local Library Scanning

When you have a non-root shell, use `scan -l` to find local exploits that can escalate your privileges to root. This scans the libraries installed on the remote machine.

---

## Remote Access (SSH / FTP)

### SSH

```bash
ssh tux@remotehost            # Connect via SSH
ssh -P mypass tux@remotehost  # With password
ssh -p 2222 tux@remotehost    # Custom port
ssh -t tux@remotehost         # Enable tunneling
ssh -l tux@remotehost         # Force local shell
ssh help                      # Interactive mode
```

### SCP (File Transfer over SSH)

```bash
scp -d file.txt               # Download file
scp -u local.txt              # Upload file
```

### FTP

```bash
ftp tux@remotehost            # Connect via FTP
ftp -P mypass tux@remotehost  # With password
ftp -p 2121 tux@remotehost    # Custom port
ftp -t tux@remotehost         # Enable tunneling
ftp help                      # Interactive mode
get file.txt                  # Download file
put local.txt                 # Upload file
```

---

## Session Management

### sess — Manage Shell Sessions

When you exploit a target, you get a session. Manage multiple sessions with `sess`:

```bash
sess -l                   # List all sessions
sess -u 1                 # Switch to session 1
sess -r 1                 # Remove session 1
sess -r 1 -y              # Remove with auto-confirm
sess -a                   # Add current session to cache
sess -a ServerName        # Add with nickname
sess -n 1 BankServer      # Set nickname for session
sess -g BankServer        # Jump to session by nickname
sess -x                   # Clear all sessions
sess back                 # Return to previous session
sess -m                   # Session management mode
```

#### Execute Commands Remotely

```bash
sess -e ls -la            # Execute command in session
```

#### Transfer Files Between Sessions

```bash
sess -p 2 file.txt            # Pass file to session 2
sess -p 1 file.txt --path /home/user  # Pass file to specific path
```

---

## Proxy Chains

### proxy — Route Through Multiple Hops

Proxy chains route your traffic through compromised routers, hiding your real IP.

```bash
proxy -a                  # Standard proxy chain (proxy.dat or Map.conf)
proxy -x                  # Combined proxy (both proxy.dat + Map.conf)
proxy -q                  # Quick proxy (single router hop)
proxy -c                  # Count hops
proxy -p y                # Proxy.dat chain, skip prompts
proxy -m                  # Map.conf chain
proxy -r 5 y              # Random chain, 5 hops, auto-confirm
proxy -h -c 10            # 10-hop chain
proxy -n                  # Create new Map.conf file
```

#### Import/Export

```bash
proxy -ri filename        # Import map_ips.dat file
proxy -wo filename        # Export Map.conf to file
```

#### Decoy Recovery

```bash
proxy -d -r -i 1          # Start decoy with ID 1
proxy -d -i 1             # Return to session 1
proxy -d -n sessions      # Return to named session
```

---

## Pivoting

### pivot — Deploy X on a Target

Pivoting installs X on a compromised machine so you can operate from their network:

```bash
pivot                     # Minimal pivot (prompts for location)
pivot -y                  # Full pivot (complete X framework)
```

After pivoting, you can scan the target's local network, attack internal machines, and chain further pivots.

---

## Network Reconnaissance

### hunt — Find Services Across the Internet

`hunt` searches for specific services, versions, and targets:

```bash
hunt ssh                  # Find SSH services
hunt ssh -c 5             # Find 5 SSH services
hunt ssh -v 1.0.3         # Find specific SSH version
hunt ftp -c 10            # Find 10 FTP services
hunt http -v 1.0.1        # Find specific HTTP version
hunt router               # Find routers
hunt bank                 # Find bank services
hunt wifi                 # Find WiFi networks
hunt lib                  # Find any library
hunt lib -n crypto -d     # Find and download crypto library
hunt custom -p 8080       # Search custom port
hunt employee -c 5        # Find employee services
hunt special -n passwd    # Find special files
```

#### WiFi Searches

```bash
hunt awifi -e HomeNetwork       # Find WiFi by ESSID
hunt awifi -b 00:11:22:33:44:55 # Find WiFi by BSSID
```

### Other Recon

```bash
ping 192.168.1.1          # Test connectivity
nslookup example.com      # DNS lookup
whois 155.236.80.20       # WHOIS registration info
smtpUserList mail.com     # Enumerate SMTP users
```

---

## Wireless Attacks

```bash
airmon                    # Start wireless monitor mode
aireplay                  # Replay wireless frames
aircrack                  # Crack WiFi encryption
```

---

## 0day Framework

### 0day — PObject Exploitation

The 0day system lets you patch and manage zero-day exploits:

```bash
0day mode                 # Enable 0day mode
0day next                 # Next 0day cycle time
0day left                 # Time remaining in cycle
```

#### Credential Management

```bash
0day -m                   # Manage engineer credentials
0day -a NAME PASSWORD     # Add credentials
0day -v                   # View credentials
0day -r 1                 # Remove credential
0day purge                # Clear all data
0day claim USER PASS      # Claim neurobox account
```

#### Patching

```bash
0day -p libhttp.so        # Patch library
0day -c libhttp.so        # Check patch status
0day -pa /lib             # Patch all libraries in folder
```

#### Neurobox Scanning

```bash
0day neuro -e email -p pass -t target -i 1.XXX.1.1  # Neurobox scan
```

---

## Remote Shell (RShell)

### rshell — Persistent Remote Access

Deploy and manage remote shells on compromised machines:

```bash
rshell -s                 # Start temporary rshell
rshell -s 192.168.1.1     # Start with specific IP
rshell -s 192.168.1.1 1234 MyShell  # Custom port and name
rshell -b                 # Build rshell
rshell -i                 # Install and launch
rshell -bi                # Build and install
rshell import             # Import rshell server
```

#### Manage Rshells

```bash
rshell -l                 # List captured rshells
rshell list               # List all rshells
rshell -u 1               # Use rshell ID 1
rshell -k 1               # Kill rshell ID 1
rshell -x                 # Kill all rshells
rshell refresh            # Refresh rshell data
rshell logs               # View logs
rshell -h                 # History
rshell -h -u 1            # History for rshell 1
rshell dump               # Export rshell server list
```

#### File Transfer via Rshell

```bash
rshell -d 1 file.txt /tmp        # Download from rshell 1
rshell -da file.bin /tmp         # Download from all rshells
rshell -p 1 local.txt /tmp       # Upload to rshell 1
rshell -pa local.txt /tmp        # Upload to all rshells
rshell -z -u 1,2,3 file /tmp    # Upload to multiple rshells
```

#### Execute Commands

```bash
rshell -e 1 command param        # Execute on rshell 1
rshell -ea command param         # Execute on all rshells
```

---

## Email

```bash
email -s                  # Setup new email account
email -l user@mail.com    # Login to email
email -l user@mail.com pass  # Login with password
email -c                  # Open email GUI
email -v                  # View inbox
email -o 5                # Open email ID 5
email -n                  # Compose new email
email -r 12               # Delete email ID 12
email -x                  # Clear entire inbox
email -m user@mail.com pass 30  # Monitor inbox (30s refresh)
email -b target@mail.com Subject "Message" 100  # Send 100 emails
```

---

## Mission Contracts

```bash
missions                  # Process inbox contracts
missions --bypass-rshell  # Skip rshell requirements
```

Mission types: grade manipulation, police records, boot corruption, file retrieval, file deletion.

---

## Heists

### heist — Bank Heist Automation

```bash
heist -t 192.168.1.50 -b 192.168.1.100              # Basic heist
heist -t bank.com -b mybank.com -a 123456            # Target specific account
heist -t bank.com -b mybank.com --tp 8080 --bp 9090  # Custom ports
```

---

## File Operations

### Download & Upload

```bash
scp -d remotefile.txt     # Download via SSH
scp -u localfile.txt      # Upload via SSH
get remotefile.txt        # Download via FTP
put localfile.txt         # Upload via FTP
```

### Compression

```bash
zip file.txt              # Compress file
gzip file.txt             # GZip compress
tar folder/               # Create tar archive
```

### Other

```bash
diff file1 file2          # Compare two files
ln source /path          # Create symbolic link
ln -l                    # List all symbolic links
open file.txt             # Open with associated program
```

---

## Text Processing & Pipes

X supports Unix-style pipe chains. Connect commands with `|` to filter and transform data:

```bash
cat file.txt | grep "error" | wc -l       # Count error lines
ps | sort | uniq | wc -l                  # Count unique processes
cat /etc/passwd | cut -d: -f1 | sort      # Extract and sort usernames
echo "5 + 3" | bc                         # Calculator: 8
echo "hello" | tr 'a-z' 'A-Z'            # Uppercase: HELLO
```

### Available Pipe Commands

| Command | Purpose |
|---------|---------|
| `grep` | Search text patterns |
| `sed` | Find and replace |
| `awk` | Field extraction |
| `sort` | Sort lines |
| `uniq` | Remove duplicates |
| `wc` | Count words/lines/chars |
| `cut` | Extract columns |
| `tr` | Translate characters |
| `head` | First N lines |
| `tail` | Last N lines |
| `rev` | Reverse text |
| `trim` | Remove whitespace |
| `split` | Split strings |
| `join` | Join strings |
| `column` | Format into columns |
| `tee` | Split output to file + screen |
| `xclip` | Copy to clipboard |
| `bc` | Calculator |

### Pipe Variables

```bash
set VAR value                 # Store a value
cat file.txt | set CONTENT    # Capture command output
echo "$VAR"                   # Use stored value
echo "${NUM}nd"               # Braces for word boundaries
env                           # List all variables
unset VAR                     # Delete variable
```

### Debug Mode

```bash
debug on                  # Show pipe internals
debug off                 # Normal mode
debug status              # Check current state
```

---

## Bash Scripting

X includes a full bash scripting engine for automation.

### Running Scripts

```bash
run scriptname            # Run a script
@scriptname               # Shorthand
run --list                # List all scripts
run -e scriptname         # Edit a script
run -e NewScript          # Create and edit new script
run -n scriptname         # Create new script (no edit)
run --DEBUG script        # Debug mode
```

### Variables

```bash
_setvar(name, Alice)          # Set variable
_getvar(name)                 # Get variable
_print Hello, _getvar(name)!  # Use in output
```

### User Input

```bash
_setvar(name, get_string(Enter name:))     # Text input
_setvar(age, get_integer(Enter age:))      # Number input
_setvar(val, get_decimal(Enter value:))    # Decimal input
```

### Control Flow

```bash
# If/elif/else
if _getvar(age) >= 18
  _print Adult
elif _getvar(age) >= 13
  _print Teenager
else
  _print Child
endif

# While loop
_setvar(i, 0)
while _getvar(i) < 10
  _print _getvar(i)
  _setvar(i, _getvar(i) + 1)
endwhile

# For loop
for item in [apple, banana, orange]
  _print _getvar(item)
endfor

for i in range(1, 10)
  _print _getvar(i)
endfor

# Switch
switch _getvar(choice)
  case 1
    _print Option one
  case 2
    _print Option two
  default
    _print Unknown
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
```

### Array Operations

```bash
_setvar(items, [apple, banana])
_push items orange        # Add to end
_pop items                # Remove from end
_pull items               # Remove from start
_len mylist               # Get length
_in mylist apple          # Check if value exists
```

### Built-in Functions

**String:** `len()`, `upper()`, `lower()`, `substr()`, `concat()`, `contains()`, `replace()`, `trim_str()`, `split_str()`

**Math:** `floor()`, `ceil()`, `abs()`, `round()`, `min()`, `max()`, `random()`

**File:** `file_exists()`, `is_folder()`, `is_binary()`, `_fs_read()`, `get_permissions()`

**Context:** `get_user()`, `get_home()`, `get_shell_type()`, `get_root()`, `get_computer_lan_ip()`, `get_computer_public_ip()`, `get_layer()`

**Type:** `to_string()`, `to_int()`, `to_float()`, `typeof()`

**Map/JSON:** `map()`, `map_set()`, `map_get()`, `map_del()`, `map_has()`, `map_keys()`, `map_values()`, `json()`, `json_parse()`, `map_save()`, `map_load()`

**Time:** `timestamp()`, `date()`

For full bash scripting documentation, see the [Bash User Handbook](bash_user_handbook.md).

---

## AI Agent

X includes a natural language AI agent that translates your plain-English requests into commands.

### Basic Usage

```bash
ai show me test.txt           # View a file
ai scan 192.168.1.1           # Scan a target
ai list files in this directory
ai copy test.txt to backup.txt
ai delete oldfile.txt
ai change permissions of myfile to 644
```

### Modes

```bash
ai "scan target" -v           # Verbose output
ai "delete file.txt" -q       # Quiet mode
ai "scan -l" -d               # Dry-run (plan only, don't execute)
ai "exploit target" -a        # Aggressive (try all methods)
ai "scan target" -s           # Stealth mode
ai "what is chmod?" -t        # Trainer (show commands, don't execute)
ai "scan target" -D           # Debug (show decision-making)
```

### Agent Management

```bash
ai status                     # Show agent status
ai history                    # Command history
ai clear                      # Full reset
ai learn scan                 # Learn from scan's man page
ai learn all                  # Learn all man pages
ai save                       # Save configuration
ai load                       # Load saved configuration
ai undo                       # Undo last action
ai undo 5                     # Undo last 5 actions
ai set max_attempts 10        # Configure settings
ai show config                # Show configuration
ai reset config               # Reset to defaults
```

For full AI documentation, see the [AI User Handbook](ai_user_handbook.md).

---

## Configuration

### config — Framework Settings

```bash
config stats              # View all settings
config run                # Interactive settings menu
config on                 # Enable all options
config off                # Disable all options
config --reset            # Reset to defaults
```

#### Individual Settings

```bash
config -a                 # Auto-solve PObjects
config -g                 # Debug output
config -m                 # Update metaxploit on launch
config -e                 # Auto clear exploit scan buffer
config -p                 # Build rainbow index on launch
config -s                 # Auto-add sessions
config -i                 # Dirty router IP logging
config -l                 # Dynamic LAN IP tracking
config -y                 # Proxy log for crash recovery
config -h                 # Short home path display
config -z                 # Fast path home
config -r                 # Auto-reset password
config -b                 # Binary scan library
config -v bounce_lib      # Set bounce library
config -x 5               # Set exploit index
```

### Aliases

Create command shortcuts:

```bash
alias -s ll ls -la        # Create alias
alias -l                  # List all aliases
alias -r ll               # Remove alias
alias --clear             # Clear all aliases
```

---

## Utilities

### Process & System

```bash
htop                      # Interactive process monitor
htop --deploy             # Install htop on target
time ls -la               # Time a command
wait 5                    # Pause for 5 seconds
clean                     # Clean temporary files
repl                      # Interactive REPL shell
swap                      # Manage swap space
```

### Development

```bash
build source.src /home/user/Desktop     # Build a program
build -a script.src /usr/bin            # Build with import
build -r program.src /home/user         # Build and run
make program.src                        # Compile source
```

### Packages

```bash
pacman -i package         # Install package
pacman -u package         # Update package
pacman -r package         # Remove package
```

### Database Maintenance

Keep your exploit database current:

```bash
pacman exp router                  # Update router exploits
pacman -Sy -e -c 100              # General maintenance scan
pacman -Sy -e -c 1000             # Weekly deep maintenance
```

### Networking

```bash
ddos 192.168.1.1          # DDoS attack
ddos 192.168.1.0/24       # DDoS subnet
sniffer                   # Capture network traffic
netcat                    # Network utility
```

### Crypto & Misc

```bash
wallet                    # Cryptocurrency management
aes128                    # AES128 encryption/decryption
sha256                    # SHA256 hashing
coin                      # Coin flip
cal                       # Calendar
date                      # Current date/time
l33t                      # 1337 speak converter
notes                     # Notepad
```

### Man Pages

```bash
man COMMAND               # View help for any command
```

---

## Common Workflows

### Scan → Exploit → Root

```bash
nmap 192.168.1.1              # 1. Find open ports
scan 192.168.1.1              # 2. Scan for vulnerabilities
                              # 3. Select an exploit → get shell
dict -l                       # 4. Crack passwords
su root                       # 5. Escalate to root
su -w                         # 6. Wipe logs
```

### Build a Proxy Chain

```bash
hunt ssh -c 3                 # Find SSH targets
scan -p TARGET 22             # Exploit SSH
pivot                         # Pivot to target
proxy -a                      # Start proxy chain
```

### Pivot Through a Network

```bash
scan 192.168.1.1              # Exploit gateway
pivot                         # Deploy X on target
scan -n                       # Scan their internal network
                              # Exploit internal machines
```

### Automated Bash Script

```bash
run -e autoscan               # Create a script

# Example script content:
_setvar(target, get_string(Target IP:))
_print Scanning _getvar(target)...
scan _getvar(target)
```

---

## Troubleshooting

### Exploit Database Issues

```bash
exp refresh                   # Refresh database
exp defrag                    # Clean orphaned indexes
exp bloom rebuild             # Rebuild bloom filters
exp backup                    # Backup (do this regularly!)
exp restore                   # Restore from backup
```

### Rainbow Table Issues

```bash
rainbow -r                    # Rebuild tables
rainbow -n                    # Initialize fresh
```

### Session Crashes

- Use decoys: `proxy -d`
- Re-establish: `proxy -q`

### Permission Denied

```bash
su root                       # Try switching to root
su -b                         # Brute force root password
su -d                         # Dictionary attack
scan -l                       # Find local privilege escalation
```

### Missing Libraries

```bash
sys check                     # Auto-install missing libs
```

### Always Proxy

Use `proxy` before attacking targets to hide your real IP. Bad things happen without it.

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

**Repository:** `218.201.114.152`
**Version:** 0.9.7.3
