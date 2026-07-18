# X Shell Command Reference

Complete command documentation for the X Shell GreyScript framework.

## Table of Contents

- [System & Process Management](#system--process-management)
- [File Operations](#file-operations)
- [Network Operations](#network-operations)
- [Security & Exploitation](#security--exploitation)
- [Text Processing](#text-processing)
- [Development Tools](#development-tools)
- [Package Management](#package-management)
- [Utilities](#utilities)

---

## System & Process Management

### htop
Interactive process monitoring with real-time CPU/memory visualization.

**Usage:** `htop [--deploy]`

**Flags:**
- `--deploy` - Install htop on target system

**Features:**
- Real-time process list with CPU/memory bars
- Color-coded resource usage
- PID, user, CPU%, memory%, command display
- Auto-refresh every 3 seconds

**Examples:**
```bash
htop                    # Launch monitor
htop --deploy           # Install on system
```

---

### ps
Display running processes (used in pipes).

**Usage:** `ps [-u user] [-C command]`

**Flags:**
- `-u <user>` - Filter by username
- `-C <command>` - Filter by command name

**Output Format:** `USER PID CPU% MEM% COMMAND`

**Examples:**
```bash
ps                      # All processes
ps -u root              # Root's processes
ps -C sshd              # SSH daemon processes
ps -u guest -C bash     # Guest's bash processes
ps | wc -l              # Count processes
```

---

### kill
Terminate processes by PID or name.

**Usage:** `kill <pid|name>... [--all|-a [name]]`

**Arguments:**
- `<pid>` - Process ID to kill
- `<name>` - Process name to kill

**Flags:**
- `-a` / `--all` - Kill all processes
- `-a <name>` - Kill all processes matching name

**Examples:**
```bash
kill 1234               # Kill PID 1234
kill Terminal.exe       # Kill by name
kill -a bash            # Kill all bash processes
kill -a                 # Kill all (dangerous!)
```

---

### lsof
List open files and processes for current user.

**Usage:** `lsof`

**Features:**
- Shows all running processes
- Displays full path to executables
- Current user context only

**Examples:**
```bash
lsof                    # List all open files
```

---

### uptime
Display system uptime and load information.

**Usage:** `uptime`

**Features:**
- Shows boot time
- Current uptime duration
- User count
- Load averages (if available)

**Examples:**
```bash
uptime                  # Show system uptime
```

---

### reboot
Reboot the computer (requires root).

**Usage:** `reboot`

**Examples:**
```bash
reboot                  # Restart system
```

---

### wait
Pause execution for specified seconds.

**Usage:** `wait <seconds>`

**Arguments:**
- `<seconds>` - Number of seconds to wait

**Examples:**
```bash
wait 5                  # Wait 5 seconds
wait 0.5                # Wait half second
```

---

### time (date)
Display current system time and date.

**Usage:** `time`
**Alias:** `date`

**Features:**
- Prints current time and date

**Examples:**
```bash
time                    # Display current time and date
```

---

### neofetch
Display system information with ASCII art.

**Usage:** `neofetch`

**Features:**
- Hostname and user
- OS information
- Kernel version
- Uptime
- Shell type
- CPU info
- Memory usage
- Disk usage
- Network info
- ASCII art logo

**Examples:**
```bash
neofetch                # Show system info
```

---

### systemLock
Monitor and log system access attempts.

**Usage:** `systemLock`

**Features:**
- Monitors login attempts
- Logs unauthorized access
- Alerts on suspicious activity
- Continuous background monitoring

**Examples:**
```bash
systemLock              # Start system monitor
```

---

### ids
Intrusion Detection System with multi-vector monitoring.

**Usage:** `ids`

**Features:**
- Process monitoring
- File integrity checking
- Firewall rule monitoring
- Real-time alerts
- Automatic response options

**Examples:**
```bash
ids                     # Launch IDS
```

---

### missions
Automated mission contract handler for email-based contracts.

**Usage:** `missions [--bypass-rshell]`

**Flags:**
- `--bypass-rshell` - Skip rshell server requirement check

**Mission Types:**
- **ACADEMIC** - Grade manipulation (requires GUI access)
- **POLICE** - Police record modification (requires GUI access)
- **CORRUPTION** - Boot process corruption (rename /boot to /boots)
- **GETFILE** - Remote file retrieval and download
- **DELETEFILE** - File deletion on target systems
- **CREDENTIALS** - Password extraction from /etc/passwd

**Features:**
- Automatic email parsing of mission contracts
- Intelligent exploit acquisition and prioritization
- Shell priority: root > user > guest
- Router bounce attacks for indirect access
- GUI automation for manual tasks
- Result reporting and statistics
- Log clearing after operations

**Requirements:**
- Active mail session (`email -l`)
- Exploit database (`exp` command)
- Mission email with subject: "Mission Contract"
- Router attack configuration for some missions (`config -v`)

**Configuration:**
Many missions require router attack settings in `~/.xrc`:
- Router Attack Library - Library for advanced attacks (set via `config -v NAME`, e.g., `config -v ssh`)
- Router Attack Method - Specific exploit to use (set via `config -x INDEX`, e.g., `config -x 3`)

Configure via: `config -v` and `config -x` or manually edit `~/.xrc`

**Examples:**
```bash
# Setup
email -l missions@mail.com      # Login to mission account
apt update -e -c 5              # Update exploits (5 passes)

# Run missions
missions                        # Process all contracts
missions --bypass-rshell        # Skip rshell check

# Check configuration
config                          # View current settings
config -v                       # Interactive setup
```

**Output Example:**
```
Mission Statistics:
  Academic: 2
  Police: 1
  GetFile: 3

Academic Mission #1:
  IP: 192.168.1.100
  Target: 192.168.1.50
  Student: John Doe
  Subject: Mathematics
  Action: change to 8
  [SUCCESS] Successfully modified grade
```

**Notes:**
- Academic/Police missions open GUIs for manual completion
- CRITICAL: Configure router attack settings via `config -v`
- Many missions require router attack library configuration
- RShell servers managed via `rshell list` command
- Failed missions marked with yellow/red text
- "Any User" missions exclude guest accounts

**See Also:** email, exp, open, rshell, config

---

### reload
Reload cached data lists and databases.

**Usage:** `reload -a|-d|-P|-m|-c`

**Flags:**
- `-a` - Reload all cached lists and databases
- `-d` - Reload exploit database
- `-P` - Rebuild rainbow table hash index
- `-m` - Reload metaxploit framework data
- `-c` - Reload crypto library data

**Features:**
- Database cache management
- Exploit list refresh
- Rainbow table indexing
- Framework data reload
- Corruption recovery

**Examples:**
```bash
reload -a               # Reload everything
reload -d               # Reload exploits only
reload -P               # Rebuild rainbow index
reload -m               # Reload metaxploit
reload -c               # Reload crypto data
```

**See Also:** load, exp

---

### stats
Display X statistics and metrics.

**Usage:** `stats -s|-l|-d|-dl [-s]`

**Flags:**
- `-s` - General system statistics
- `-l` - Library usage statistics
- `-d` - Database statistics
- `-dl [-s]` - Detailed database view (optional sort with -s)

**Features:**
- System performance metrics
- Library usage tracking
- Database statistics
- Resource usage analysis

**Examples:**
```bash
stats -s                # System statistics
stats -l                # Library statistics
stats -d                # Database statistics
stats -dl -s            # Detailed sorted database stats
```

---

### spawn
Spawn new X instance for multi-session work.

**Usage:** `spawn [-p|--pass PASSWORD] [-u USER]`

**Flags:**
- `-p` - Launch as root with password prompt (secure)
- `--pass PASSWORD` - Launch as root with password specified
- `-u USER` - Launch as specific user

**Features:**
- Multi-session support
- User switching
- Root spawning
- MAIN session only

**Examples:**
```bash
spawn                   # Spawn as current user
spawn -p                # Spawn as root (prompt)
spawn --pass mypass     # Spawn as root (password)
spawn -u tux            # Spawn as user tux
```

**See Also:** sess

---

### exit
Exit framework or active session.

**Usage:** `exit [y]`

**Arguments:**
- `[y]` - Skip confirmation prompt

**Aliases:** `x`, `home`

**Features:**
- Session termination
- Connection cleanup
- Optional confirmation
- Return to main system

**Examples:**
```bash
exit                    # Exit with prompt
exit y                  # Exit immediately
x                       # Quick exit alias
home                    # Return home alias
```

**See Also:** close

---

### close
Close session or object without terminating.

**Usage:** `close`

**Alias:** `c`

**Features:**
- Keep sessions active
- Close without termination
- Preserves connections
- Alternative to exit/home

**Note:** Use `close` to keep sessions active. Using `x`, `exit`, or `home` terminates active sessions.

**Examples:**
```bash
close                   # Close session
c                       # Quick close alias
```

**See Also:** exit, home

---

### home
Close all nested objects and return to top-level running object.

**Usage:** `home`

**Features:**
- Closes all nested objects (shell/computer/file)
- If on a pivot or proxy, returns to that pivot/proxy
- Only returns to main if no active pivots/proxies

**Examples:**
```bash
home                    # Return to top-level object
```

**See Also:** exit, close

---

### audit
Run a security audit on the current computer.

**Usage:** `audit [-q] [-p] [-r] [-f]`

**Flags:**
- `-q` - Quick mode: filesystem and account checks only (skips ports/procs)
- `-p` - Ports only
- `-r` - Processes only
- `-f` - Full mode (default)

**Features:**
- Severity-tagged report (CRITICAL/WARNING/INFO/OK)
- Security score out of 100
- Filesystem, account, port, and process scanning

**Examples:**
```bash
audit                   # Full audit
audit -q                # Quick check
audit -p                # Ports only
```

---

## File Operations

### ls
List directory contents with detailed information.

**Usage:** `ls [directory] [-a|--all] [-o|--octal]`

**Arguments:**
- `[directory]` - Directory to list (default: current)

**Flags:**
- `-a` / `--all` - Recursive listing
- `-o` / `--octal` - Show octal permissions

**Features:**
- Color-coded by type (directories, files, links, bins)
- Permission display (symbolic or octal)
- Owner and group information
- File size in human-readable format
- Last modified timestamp
- Icon support for file types

**Examples:**
```bash
ls                      # List current directory
ls /home                # List /home
ls -a                   # Recursive all subdirs
ls -o                   # Show octal permissions
ls -a -o /etc           # Recursive with octal
```

---

### cd
Change working directory with smart navigation.

**Usage:** `cd [directory]`

**Arguments:**
- `[directory]` - Target directory (default: home)

**Special Patterns:**
- `~` - Home directory
- `..` - Parent directory
- `-` - Previous directory
- `*` - Wildcard (opens interactive menu)

**Features:**
- Tab completion support
- Wildcard matching with selection menu
- History tracking (previous directory)
- Auto-completion for partial matches

**Examples:**
```bash
cd                      # Go to home
cd /etc                 # Go to /etc
cd ..                   # Go up one level
cd -                    # Go to previous dir
cd lib*                 # Wildcard menu (lib, libs, library)
```

---

### cdl
Change directory and list contents in one operation.

**Usage:** `cdl [directory]`

**Arguments:**
- `[directory]` - Target directory (default: home)

**Special Patterns:**
- `..` - Parent directory
- `-` / `back` - Previous directory

**Features:**
- Combined cd + ls operation
- Time-saving reconnaissance tool
- Standard cd shortcuts
- Auto-listing after navigation

**Examples:**
```bash
cdl                     # Go home and list
cdl /etc                # Go to /etc and list
cdl ..                  # Go up one level and list
cdl -                   # Go to previous dir and list
cdl back                # Same as cdl -
cdl /var/log            # Navigate to logs and show contents
```

---

### pwd
Print working directory.

**Usage:** `pwd`

**Examples:**
```bash
pwd                     # Show current directory
```

---

### mkdir
Create new directories with batch support.

**Usage:** `mkdir <directory>... [-y] [-l] [-p path]`

**Arguments:**
- `<directory>...` - One or more directory names

**Flags:**
- `-y` - Overwrite if exists
- `-l` - Loop mode (create until 'x')
- `-p <path>` - Prefix path for all directories

**Features:**
- Batch creation
- Interactive loop mode
- Prefix path support
- Overwrite protection

**Examples:**
```bash
mkdir newdir            # Create single directory
mkdir dir1 dir2 dir3    # Create multiple
mkdir -y testdir        # Overwrite if exists
mkdir -l                # Loop mode (create many)
mkdir -p /var/ test1 test2  # Create in /var/
```

---

### mkcd
Create directory and change into it atomically.

**Usage:** `mkcd <directory>`

**Arguments:**
- `<directory>` - Directory to create and enter

**Examples:**
```bash
mkcd newproject         # Create and cd
mkcd /var/workspace     # Create nested and cd
```

---

### touch
Create empty files or update timestamps.

**Usage:** `touch <file>...`

**Arguments:**
- `<file>...` - One or more files to create/update

**Features:**
- Creates empty files if not exist
- Updates timestamps if exist
- Batch creation support
- Glob pattern support

**Examples:**
```bash
touch file.txt          # Create single file
touch a.txt b.txt c.txt # Create multiple
touch *.log             # Update all .log files
```

---

### rm
Remove files and directories.

**Usage:** `rm <path>... [-r|-R]`

**Arguments:**
- `<path>...` - Files or directories to remove

**Flags:**
- `-r` / `-R` - Recursive deletion (for directories)

**Features:**
- Single or batch deletion
- Directory removal with recursive flag
- Glob pattern support
- Confirmation prompts

**Examples:**
```bash
rm file.txt             # Remove file
rm *.tmp                # Remove all .tmp files
rm -r directory         # Remove directory recursively
rm file1.txt file2.txt  # Remove multiple files
```

---

### rmdir
Remove empty directories.

**Usage:** `rmdir <directory>...`

**Arguments:**
- `<directory>...` - Empty directories to remove

**Features:**
- Only removes empty directories
- Batch removal support
- Glob pattern support
- Safety checks

**Examples:**
```bash
rmdir olddir            # Remove empty directory
rmdir dir1 dir2         # Remove multiple
rmdir test*             # Remove all matching
```

---

### qrm
Quick remove with minimal prompts.

**Usage:** `qrm <path>...`

**Arguments:**
- `<path>...` - Files or directories to remove

**Features:**
- Fast deletion without confirmations
- Recursive by default
- Batch support
- Glob patterns

**Examples:**
```bash
qrm *.log               # Remove all logs
qrm temp/               # Remove directory
qrm file1 file2 dir1    # Remove multiple
```

---

### cp
Copy files and directories.

**Usage:** `cp <source> <dest> [name] [-r] [-l] [-n name] [-z]`

**Arguments:**
- `<source>` - Source file or directory
- `<dest>` - Destination path
- `[name]` - Optional new name

**Flags:**
- `-r` - Recursive copy (for directories)
- `-l` - Create link instead of copy
- `-n <name>` - Specify name
- `-z` - Create zip archive

**Features:**
- File and directory copying
- Rename during copy
- Link creation
- Zip compression
- Batch operations
- Glob support

**Examples:**
```bash
cp file.txt /var                # Copy file
cp file.txt /var backup.txt     # Copy and rename
cp -r /etc/config /backup       # Copy directory
cp -z files/ archive.zip        # Create zip
cp *.txt /backup                # Copy all .txt files
```

---

### mv
Move or rename files and directories.

**Usage:** `mv <source> <dest> [name] [-r] [-l] [-n name] [-z]`

**Arguments:**
- `<source>` - Source file or directory
- `<dest>` - Destination path
- `[name]` - Optional new name

**Flags:**
- `-r` - Recursive move (for directories)
- `-l` - Create link
- `-n <name>` - Specify name
- `-z` - Create zip

**Features:**
- Move or rename files/directories
- Cross-directory moves
- Rename during move
- Batch operations
- Glob support

**Examples:**
```bash
mv file.txt newname.txt         # Rename file
mv file.txt /var                # Move file
mv file.txt /var backup.txt     # Move and rename
mv -r olddir /var newdir        # Move directory
mv *.log /archive               # Move all logs
```

---

### cat
Display file contents with optional syntax highlighting.

**Usage:** `cat <file>... [-n] [-f]`

**Arguments:**
- `<file>...` - Files to display

**Flags:**
- `-n` - Show line numbers
- `-f` - Force syntax highlighting

**Features:**
- Multi-file concatenation
- Syntax highlighting for .src files
- Line numbers option
- Glob pattern support
- Large file handling

**Examples:**
```bash
cat file.txt            # Display file
cat file1.txt file2.txt # Display multiple
cat -n script.src       # With line numbers
cat *.log               # Display all logs
cat -f code.src         # Force highlighting
```

---

### more
Paginated file viewer with scrolling.

**Usage:** `more <file> [-c number]`

**Arguments:**
- `<file>` - File to view

**Flags:**
- `-c <number>` - Lines per page (default: 25)

**Features:**
- Paginated viewing
- Forward/backward navigation
- Search functionality
- Custom page size
- Large file support

**Controls:**
- Space/Enter - Next page
- 'b' - Previous page
- 'q' - Quit
- '/' - Search

**Examples:**
```bash
more largefile.txt      # View with pagination
more -c 50 data.txt     # 50 lines per page
```

---

### head
Display beginning of file with optional auto-refresh.

**Usage:** `head <file> [-l lines] [-p seconds]`

**Arguments:**
- `<file>` - File to display

**Flags:**
- `-l <lines>` - Number of lines to show (default: 10)
- `-p <seconds>` - Periodic refresh interval

**Features:**
- First N lines display
- Auto-refresh mode for logs
- Configurable line count
- Real-time monitoring

**Examples:**
```bash
head log.txt            # First 10 lines
head -l 20 file.txt     # First 20 lines
head -l 5 -p 2 log.txt  # 5 lines, refresh every 2s
```

---

### tail
Display end of file with optional follow mode.

**Usage:** `tail <file> [-l lines] [-f]`

**Arguments:**
- `<file>` - File to display

**Flags:**
- `-l <lines>` - Number of lines to show (default: 10)
- `-f` - Follow mode (real-time updates)

**Features:**
- Last N lines display
- Real-time log following
- Configurable line count
- Auto-scroll

**Examples:**
```bash
tail log.txt            # Last 10 lines
tail -l 20 file.txt     # Last 20 lines
tail -f log.txt         # Follow mode (Ctrl+C to stop)
```

---

### tree
Display directory tree structure.

**Usage:** `tree [directory]`

**Arguments:**
- `[directory]` - Root directory (default: current)

**Features:**
- Hierarchical tree view
- Color-coded by type
- Size information
- Permission display
- Nested structure visualization

**Examples:**
```bash
tree                    # Current directory tree
tree /etc               # /etc directory tree
```

---

### treeWide
Wide directory tree with full paths.

**Usage:** `treeWide [directory]`

**Arguments:**
- `[directory]` - Root directory (default: current)

**Examples:**
```bash
treeWide                # Wide tree format
treeWide /var           # Wide tree of /var
```

---

### file
Display comprehensive file/directory information.

**Usage:** `file <path> [-o] [-s]`

**Arguments:**
- `<path>` - File or directory path

**Flags:**
- `-o` - Show octal permissions
- `-s` - Show system stats

**Features:**
- File type detection
- Permission display (symbolic/octal)
- Owner and group
- File size
- Timestamps (created, modified, accessed)
- Path information
- System stats

**Examples:**
```bash
file script.sh          # File info
file -o binary          # With octal permissions
file -s /etc            # With system stats
```

---

### stat
Display file statistics.

**Usage:** `stat <file>`

**Arguments:**
- `<file>` - File path

**Features:**
- Detailed file metadata
- Inode information
- Block size
- Links count
- Full timestamp details

**Examples:**
```bash
stat important.txt      # Show file stats
```

---

### ln
Create symbolic links or list existing links.

**Usage:** `ln <source> <dest> [name] [-l]`

**Arguments:**
- `<source>` - Target file/directory
- `<dest>` - Link destination
- `[name]` - Optional link name

**Flags:**
- `-l` - List all symlinks in system

**Features:**
- Symbolic link creation
- Link listing
- Glob pattern support
- Multi-link creation

**Examples:**
```bash
ln /bin/tool /usr/bin mytool    # Create link
ln -l                           # List all symlinks
ln *.sh /usr/bin                # Link multiple files
```

---

### find
Advanced filesystem search with multiple criteria.

**Usage:** `find [-a pattern] [-p path] [-i] [-e] [-c] [--type]`

**Flags:**
- `-a <pattern>` - Filename pattern
- `-p <path>` - Search path (default: current)
- `-i` - Case-insensitive
- `-e` - Exact match
- `-c` - Search file contents

**Type Filters:**
- `--binary` - Binary executables only
- `--folder` - Directories only
- `--text` - Text files only
- `--link` - Symlinks only

**Permission Filters:**
- `-r` - Readable files only
- `-w` - Writable files only
- `-x` - Executable files only

**Features:**
- Recursive search
- Wildcard support
- Content search
- Type filtering
- Permission filtering
- Regex patterns

**Examples:**
```bash
find -n "*.txt"                 # Find all .txt files
find -n config -i               # Case-insensitive search
find -p /etc -a "*.conf"        # Search in /etc
find -c "password"              # Search file contents
find --binary -x                # Find executables
find -n "test*" --folder        # Find test directories
```

---

### locate
Fast file search using full path matching.

**Usage:** `locate <pattern> [-s]`

**Arguments:**
- `<pattern>` - Filename or pattern to search

**Flags:**
- `-s` - Strict/exact match mode

**Features:**
- Fast whole-system search
- Pattern matching
- Exact match mode
- Full path search

**Examples:**
```bash
locate config.txt               # Find config.txt
locate -s passwd                # Exact match only
locate "*.log"                  # Find all log files
```

---

### open
Open file or directory with default application.

**Usage:** `open <path>`

**Arguments:**
- `<path>` - File or directory to open

**Features:**
- Default app selection
- Directory opening in file manager
- Text file editor
- Binary execution

**Examples:**
```bash
open .                  # Open current directory
open file.txt           # Open in editor
open script.src         # Open GreyScript file
```

---

### vi
Text editor with syntax highlighting.

**Usage:** `vi <file>...`

**Arguments:**
- `<file>...` - Files to edit

**Features:**
- Full-screen text editor
- Syntax highlighting
- Multi-file editing
- Line numbers
- Search and replace
- Glob pattern support

**Examples:**
```bash
vi file.txt             # Edit single file
vi script1.src script2.src  # Edit multiple
vi *.conf               # Edit all .conf files
```

---

### clean
Empty file contents (file remains).

**Usage:** `clean [file]`

**Arguments:**
- `[file]` - File to clean (default: prompt)

**Features:**
- Clears file content
- File structure preserved
- No deletion
- Quick reset

**Examples:**
```bash
clean log.txt           # Clear log file
clean                   # Prompt for file
```

---

### chmod
Change file permissions (symbolic or octal).

**Usage:** `chmod <mode> <path>... [-R|-r]`

**Arguments:**
- `<mode>` - Permission mode (octal or symbolic)
- `<path>...` - Files/directories to modify

**Flags:**
- `-R` / `-r` - Recursive (apply to all subdirectories/files)

**Modes:**
- **Octal**: 755, 644, 777, etc.
- **Symbolic**: u+x, go-w, a+r, etc.
  - u (user), g (group), o (others), a (all)
  - + (add), - (remove), = (set)
  - r (read), w (write), x (execute)

**Features:**
- Octal and symbolic modes
- Recursive application
- Batch operations
- Glob pattern support

**Examples:**
```bash
chmod 755 script.sh             # Octal mode
chmod u+x script.sh             # Add execute for user
chmod go-w file.txt             # Remove write for group/others
chmod a+r document.txt          # Add read for all
chmod -R 644 /var/www           # Recursive octal
chmod -r u+x *.sh               # Add execute to all .sh files
```

---

### chown
Change file owner.

**Usage:** `chown <user> <path>... [-R|-r]`

**Arguments:**
- `<user>` - New owner username
- `<path>...` - Files/directories to modify

**Flags:**
- `-R` / `-r` - Recursive

**Features:**
- Change file ownership
- Recursive application
- Batch operations
- Glob pattern support

**Examples:**
```bash
chown root file.txt             # Change owner
chown -R admin /etc/config      # Recursive change
chown user *.txt                # Change multiple files
```

---

### chgrp
Change file group.

**Usage:** `chgrp <group> <path>... [-R|-r]`

**Arguments:**
- `<group>` - New group name
- `<path>...` - Files/directories to modify

**Flags:**
- `-R` / `-r` - Recursive

**Features:**
- Change file group
- Recursive application
- Batch operations
- Glob pattern support

**Examples:**
```bash
chgrp admin file.txt            # Change group
chgrp -R developers /project    # Recursive change
chgrp staff *.txt               # Change multiple files
```

---

### chog
Change owner and group simultaneously with permissions.

**Usage:** `chog <user> <path>... [-R|-r]`

**Arguments:**
- `<user>` - New owner (group set to user's primary)
- `<path>...` - Files/directories to modify

**Flags:**
- `-R` / `-r` - Recursive

**Features:**
- Changes owner, group, and permissions
- Sets full rwx permissions
- Recursive application
- Batch operations
- Glob pattern support

**Examples:**
```bash
chog root script.sh             # Full ownership change
chog -R admin /srv/app          # Recursive with perms
chog user *.conf                # Change multiple files
```

---

### fw (folderWatcher)
Monitor directory for changes in real-time.

**Usage:** `fw [PAUSE] FOLDER`  
**Alias:** `folderWatcher`

**Arguments:**
- `<directory>` - Directory to watch
- `[interval]` - Check interval in seconds (default: 5)

**Features:**
- Real-time change detection
- New file alerts
- Modified file alerts
- Deleted file alerts
- Timestamp tracking
- Continuous monitoring

**Examples:**
```bash
fw /var                 # Watch /var (5s interval)
fw /var/log 2           # Watch with 2s interval
folderWatcher /home/user 10  # 10s interval
```

---

### lw (logWatcher)
Monitor system log in real-time.

**Usage:** `lw`
**Alias:** `logWatcher`

**Features:**
- Watches /var/system.log
- Real-time log streaming
- Auto-scroll
- Color-coded entries
- Timestamp display

**Examples:**
```bash
logWatcher              # Watch system log
```

---

## Network Operations

### ifconfig
Display and configure Ethernet network interface.

**Usage:** `ifconfig [interface] [ip] [gateway]`

**Arguments:**
- `[interface]` - Network interface name (default: eth0)
- `[ip]` - IP address to assign
- `[gateway]` - Gateway address

**Features:**
- Display network configuration
- Set IP address
- Configure gateway
- Interface status
- MAC address display

**Examples:**
```bash
ifconfig                        # Show config
ifconfig eth0                   # Show eth0
ifconfig eth0 192.168.1.100 192.168.1.1  # Configure
```

---

### iwconfig
Display and configure WiFi network interface.

**Usage:** `iwconfig [interface] [essid] [bssid] [password]`

**Arguments:**
- `[interface]` - WiFi interface (default: wlan0)
- `[essid]` - Network ESSID
- `[bssid]` - Router BSSID (MAC)
- `[password]` - Network password

**Features:**
- Display WiFi configuration
- Connect to networks
- Signal strength display
- MAC address display
- Encryption status

**Examples:**
```bash
iwconfig                        # Show WiFi config
iwconfig wlan0                  # Show wlan0
iwconfig wlan0 MyNetwork AA:BB:CC:DD:EE:FF password123
```

---

### jump
Quick network connection (auto-detects Ethernet/WiFi).

**Usage:** 
- Ethernet: `jump <ip> <gateway>`
- WiFi: `jump <essid> <bssid> [password]`

**Features:**
- Auto-detection of connection type
- Quick Ethernet setup
- Quick WiFi connection
- Minimal syntax

**Examples:**
```bash
jump 192.168.1.100 192.168.1.1          # Ethernet
jump HomeWiFi AA:BB:CC:DD:EE:FF pass    # WiFi
```

---

### ping
Test network connectivity with ICMP echo.

**Usage:** `ping <host>`

**Arguments:**
- `<host>` - Hostname or IP address

**Features:**
- ICMP echo request
- DNS resolution
- Latency measurement
- Packet loss detection
- Round-trip time

**Examples:**
```bash
ping google.com         # Ping by hostname
ping 8.8.8.8            # Ping by IP
```

---

### nslookup
DNS hostname resolution.

**Usage:** `nslookup <hostname>`

**Arguments:**
- `<hostname>` - Domain name to resolve

**Features:**
- DNS query
- IP address resolution
- Multiple result handling
- Error reporting

**Examples:**
```bash
nslookup google.com     # Resolve to IP
nslookup github.com     # Resolve GitHub
```

---

### whois
Display detailed router/host information.

**Usage:** `whois <ip>`

**Arguments:**
- `<ip>` - IP address to query

**Features:**
- Router information
- Open ports display
- LAN devices
- Public IP
- Local IP
- Gateway info
- Service detection

**Examples:**
```bash
whois 192.168.1.1       # Query router
whois 8.8.8.8           # Query remote IP
```

---

### nmap
Network port scanner with service detection.

**Usage:** `nmap <target> [-r|-l|-p] [-e]`

**Arguments:**
- `<target>` - IP address or hostname

**Flags:**
- `-r` - Use remote IP for scan source
- `-l` - Use local IP
- `-p` - Use public IP
- `-e` - Extended information

**Features:**
- Port scanning
- Service detection
- Version detection (extended)
- Banner grabbing
- LAN IP detection
- Multiple target types

**Examples:**
```bash
nmap 192.168.1.1        # Basic scan
nmap target.com -e      # Extended scan
nmap 10.0.0.1 -l        # Scan from local IP
```

---

### scanlib
Scan and exploit vulnerable libraries on target.

**Usage:** `scanlib <target>`

**Arguments:**
- `<target>` - IP address to scan

**Features:**
- Library enumeration
- Vulnerability detection
- Exploit suggestions
- Metaxploit integration

**Examples:**
```bash
scanlib 192.168.1.50    # Scan libraries
```

---

### scanrouter
Scan router for vulnerabilities and open ports.

**Usage:** `scanrouter <ip>`

**Arguments:**
- `<ip>` - Router IP address

**Features:**
- Port enumeration
- Service detection
- Vulnerability assessment
- Exploit database lookup

**Examples:**
```bash
scanrouter 192.168.1.1  # Scan router
```

---

### scanaddress
Scan memory zone addresses in a .so library for vulnerabilities.

**Usage:** `scanaddress [-av] LIB_PATH ZONE [ZONE...]` | `command | scanaddress [-v] LIB_PATH` | `scanaddress -a [-v] LIB_PATH`

**Flags:**
- `-a` - Auto mode: finds all zones and scans each one
- `-v` - Verbose: prints each zone address before scanning

**Features:**
- Runs `scan_address` on one or more zones
- Zones can be passed as arguments or piped from `scanlib`
- Requires metaxploit

**Examples:**
```bash
scanaddress -a /lib/crypto.so               # Auto-scan all zones
scanlib /lib/libhttp.so | scanaddress /lib/libhttp.so  # Pipe from scanlib
scanaddress -av /lib/libhttp.so | grep exploit  # Verbose, filter exploits
```

---

### scp
Secure copy files over SSH.

**Usage:** `scp <source> <dest>`

**Arguments:**
- `<source>` - Local or remote file path
- `<dest>` - Destination path

**Features:**
- Secure file transfer
- Shell connection required
- Bidirectional transfer
- Progress indication

**Examples:**
```bash
scp local.txt /remote/path      # Upload
scp /remote/file.txt /local     # Download
```

---

### rsync
Synchronize files/directories.

**Usage:** `rsync <source> <dest> [-r] [-v]`

**Arguments:**
- `<source>` - Source path
- `<dest>` - Destination path

**Flags:**
- `-r` - Recursive
- `-v` - Verbose

**Features:**
- Incremental sync
- Recursive directory sync
- Minimal data transfer
- Progress display

**Examples:**
```bash
rsync file.txt /backup          # Sync file
rsync -r /home/user /backup     # Sync directory
```

---

### ddos
Denial of Service attack tools and network flooding.

**Usage:** `ddos [-p target] [-d] [-r count] [-f count] [-ff] [-c cycles] [-b]`

**Flags:**
- `-p <target>` - Target IP for port flooding
- `-d` - Deploy reverse shells
- `-r <count>` - Create N reverse shell files
- `-f <count>` - Filesystem flood (N files)
- `-ff` - Extreme filesystem flood
- `-c <cycles>` - Number of attack cycles
- `-b` - Background mode

**Features:**
- Port flooding
- Reverse shell deployment
- Filesystem flooding
- Multi-cycle attacks
- Background operation

**Examples:**
```bash
ddos -p 192.168.1.1 -c 5        # Port flood 5 cycles
ddos -r 10                      # Deploy 10 rshells
ddos -f 1000                    # Create 1000 files
ddos -d -b                      # Deploy rshells background
```

---

### airmon
WiFi monitor mode management.

**Usage:** `airmon <start|stop> <interface>`

**Arguments:**
- `<start|stop>` - Enable or disable monitor mode
- `<interface>` - WiFi interface name

**Features:**
- Monitor mode control
- Packet capture preparation
- Interface management

**Examples:**
```bash
airmon start wlan0      # Enable monitor mode
airmon stop wlan0       # Disable monitor mode
```

---

### aireplay
WiFi packet injection for capturing handshakes.

**Usage:** `aireplay <bssid> <essid> [acks]`

**Arguments:**
- `<bssid>` - Target router MAC address
- `<essid>` - Network ESSID
- `[acks]` - Number of packets to inject (default: 100)

**Features:**
- Deauth packet injection
- Handshake capture
- Packet generation
- Progress display

**Examples:**
```bash
aireplay AA:BB:CC:DD:EE:FF HomeNet     # Inject 100 packets
aireplay AA:BB:CC:DD:EE:FF HomeNet 500 # Inject 500 packets
```

---

### aircrack
Crack WiFi passwords from capture files.

**Usage:** `aircrack <capture_file>`

**Arguments:**
- `<capture_file>` - .cap file path

**Features:**
- WPA/WPA2 cracking
- Dictionary attack
- Handshake analysis
- Multi-file support

**Examples:**
```bash
aircrack capture.cap    # Crack from capture
aircrack wpa.cap        # Crack WPA handshake
```

---

## Security & Exploitation

### decipher
Password hash cracker for MD5 hashes.

**Usage:** `decipher <hash|file> [-d] [-u user]`

**Arguments:**
- `<hash>` - MD5 hash to crack
- `<file>` - File containing hashes (e.g., /etc/passwd)

**Flags:**
- `-d` - Dictionary mode (uses wordlist)
- `-u <user>` - Filter by username in passwd file

**Features:**
- MD5 hash cracking
- Dictionary attacks
- Crypto library integration
- /etc/passwd parsing
- Progress display
- Multiple hash support

**Examples:**
```bash
decipher 5f4dcc3b5aa765d61d8327deb882cf99    # Crack single hash
decipher /etc/passwd -u root                # Crack root password
decipher -d hashes.txt                      # Dictionary attack
```

---

### hc (hashcat)
MD5 hash cracking and generation utility.

**Usage:** `hc -d MD5` | `hc -h MD5` | `hc -w WORD` | `hc -f -d|-b [-o] FILE`

**Flags:**
- `-d <hash>` - Decipher (computational crack) a hash
- `-h <hash>` - Dictionary attack (rainbow tables)
- `-w <word>` - Generate MD5 hash from word
- `-f <file> -d|-b` - Crack hashes in file (decipher or dictionary)
- `-o` - Overwrite file with cracked results

**Features:**
- MD5 hash generation
- Dictionary-based cracking
- Crypto library cracking
- Batch file processing
- Progress tracking

**Examples:**
```bash
hashcat -w password123                      # Generate hash
hashcat -h 5f4dcc3b5aa765d61d8327deb882cf99 # Dictionary crack
hashcat -d 5f4dcc3b5aa765d61d8327deb882cf99 # Crypto crack
hashcat -f hashes.txt                       # Crack file
```

---

### hf (hashfile)
Bulk hash cracking — processes all MD5 hashes in a file.

**Usage:** `hf FILE` | `hf -p`

**Flags:**
- `-p` - Crack hashes in /etc/passwd

**Features:**
- Batch hash cracking
- /etc/passwd support
- Progress tracking
- Result caching

**Examples:**
```bash
hashfile hashes.txt     # Crack file
hf -p                   # Crack /etc/passwd
```

---

### scrub
Securely wipe files and log entries.

**Usage:** `scrub <file>`

**Arguments:**
- `<file>` - File to securely delete

**Features:**
- Secure file deletion
- Multi-pass overwrite
- Log entry removal
- No recovery possible

**Examples:**
```bash
scrub sensitive.txt     # Secure delete
scrub evidence.log      # Wipe file
```

---

### 0day
PObject 0day exploitation framework.

**Usage:** `0day [command] [options]`

**Commands:**
- `-m` - List managed engineers
- `-a <name> <pass>` - Add engineer credentials
- `-v` - View patch status
- `-r <index>` - Remove engineer
- `purge` - Clear all engineers
- `-p <library>` - Patch library
- `-c <library|ip:port> [true]` - Exploit library/service
- `-pa <path>` - Patch all libraries in path
- `mode [ip]` - Launch 0day mode
- `neuro [options]` - Automated Neurobox scanning
- `next` - Next Neurobox IP
- `left` - IPs remaining in Neurobox

**Library Shortcuts:**
`router`, `ssh`, `ftp`, `http`, `chat`, `rshell`, `repo`, `cam`, `sql`, `smtp`, `init`, `kernel`, `net`, `apt`, `cry`, `meta`

**Neuro Flags:**
- `-e <email>` - Email address
- `-p <pass>` - Email password
- `-t <target>` - Target IP
- `-i <ip>` - Start IP
- `-l <start>` - Start line
- `--bash <script>` - Execute bash script

**Features:**
- PObject exploitation
- Library patching
- Engineer credential management
- Automated Neurobox scanning
- Interactive PObject interpreter
- Multi-hop attack support
- Requires root shell

**PObject Interpreter Commands:**
`help`, `exit`, `cls`, `libs`, `scan`, `meta`, `ports`, `probe`, `main`, `chmod`, `chown`, `chgrp`, `cp`, `mv`, `rn`, `rm`, `mkdir`, `touch`, `passwd`, `useradd`, `userdel`, `groupadd`, `groupdel`, `ps`

**Examples:**
```bash
# Engineer management
0day -m                         # List engineers
0day -a admin mypass            # Add engineer
0day -v                         # View patch status
0day -r 1                       # Remove engineer

# Library operations
0day -p ssh                     # Patch libssh.so
0day -c router                  # Exploit router
0day -c 192.168.1.1:22 true     # Exploit IP:port with verbose
0day -pa /lib                   # Patch all in /lib

# 0day mode and Neurobox
0day mode                       # Launch 0day mode
0day mode 192.168.1.1           # With rshell server IP
0day neuro -e mail@test.com -p pass -t 192.168.1.1
0day next                       # Next Neurobox IP
0day left                       # Remaining IPs
```

**Contexts:** main, proxy, shell only (disabled for ftpshell)

**See Also:** exploit, scan, lms

---

### inject
Inject reverse shell backdoor into source files.

**Usage:** `inject <file> [-i ip] [-p port] [-n name]`

**Arguments:**
- `<file>` - Source file to inject

**Flags:**
- `-i <ip>` - Callback IP address
- `-p <port>` - Callback port
- `-n <name>` - Process name to hide as

**Features:**
- Reverse shell injection
- Process name masking
- Auto-compilation option
- Stealth mode

**Examples:**
```bash
inject script.src -i 1.2.3.4 -p 1222        # Basic injection
inject app.src -i 1.2.3.4 -p 1222 -n ps     # With masking
```

---

### zap
Quick exploitation and pwning tools.

**Usage:** `zap`

**Features:**
- Rapid exploitation
- Auto-escalation
- Multi-vector attacks
- Session establishment

**Examples:**
```bash
zap                     # Launch exploitation
```

---

### wallet
Cryptocurrency wallet management.

**Usage:** `wallet`

**Features:**
- Coin balance display
- Transaction history
- Multiple wallet support
- Transfer functions

**Examples:**
```bash
wallet                  # Manage wallets
```

---

### blockchain
Cryptocurrency coin and subwallet creation.

**Usage:** `blockchain [-n coin_name] [-u username] [-p password]`

**Flags:**
- `-n <name>` - Coin name
- `-u <username>` - Username
- `-p <password>` - Password

**Features:**
- Create new coins
- Generate subwallets
- Blockchain initialization
- Wallet management

**Examples:**
```bash
blockchain -n MyCoin -u admin -p secret     # Create coin
blockchain -n TestCoin                      # Create test coin
```

---

### smtp (smtpUserList)
List user email accounts on SMTP servers by exploiting a service vulnerability.

**Usage:** `smtp [-p PORT] IP_or_DOMAIN`

**Flags:**
- `-p <port>` - Specify custom SMTP port

**Features:**
- SMTP user enumeration
- Email address discovery
- Service vulnerability exploitation

**Examples:**
```bash
smtp mail.company.com       # List users on default port
smtp -p 25 mail.server.com  # Custom port 25
smtp 192.168.1.50           # By IP
```

---

### su
Switch user context.

**Usage:** `su [user] [password]`

**Arguments:**
- `[user]` - Username (default: root)
- `[password]` - User password

**Features:**
- User context switching
- Root escalation
- Password prompt
- Deferred command support

**Examples:**
```bash
su                      # Switch to root (prompt)
su admin                # Switch to admin (prompt)
su root password123     # Switch with password
```

---

### passwd
Change user password.

**Usage:** `passwd <username> [password]`

**Arguments:**
- `<username>` - User to change password for
- `[password]` - New password (optional, will prompt)

**Features:**
- Password modification
- Root-only for others
- Password strength checking
- Confirmation prompts

**Examples:**
```bash
passwd root             # Change root password (prompt)
passwd user newpass123  # Change with password
```

---

### useradd
Add new user account.

**Usage:** `useradd <username> <password>`

**Arguments:**
- `<username>` - New username
- `<password>` - User password

**Features:**
- User account creation
- Home directory setup
- Default permissions
- Group assignment

**Examples:**
```bash
useradd john password123    # Create user
useradd admin SecurePass!   # Create admin
```

---

### userdel
Delete user account.

**Usage:** `userdel <username>`

**Arguments:**
- `<username>` - User to delete

**Features:**
- User account removal
- Home directory cleanup
- Group removal
- Permission cleanup

**Examples:**
```bash
userdel john            # Delete user
userdel oldadmin        # Remove old admin
```

---

### groups
Display user's group memberships.

**Usage:** `groups <username>`

**Arguments:**
- `<username>` - User to query

**Features:**
- Group membership display
- Primary group indication
- Secondary groups list

**Examples:**
```bash
groups root             # Show root's groups
groups john             # Show john's groups
```

---

### groupadd
Add user to group.

**Usage:** `groupadd <user> <group>`

**Arguments:**
- `<user>` - Username
- `<group>` - Group name (creates if doesn't exist)

**Features:**
- Group membership assignment
- Auto-create groups
- Permission inheritance

**Examples:**
```bash
groupadd john developers    # Add to developers
groupadd admin sudo         # Add to sudo
```

---

### groupdel
Remove user from group.

**Usage:** `groupdel <user> <group>`

**Arguments:**
- `<user>` - Username
- `<group>` - Group name

**Features:**
- Group membership removal
- Permission revocation
- Multi-group support

**Examples:**
```bash
groupdel john developers    # Remove from developers
groupdel user admin         # Remove from admin
```

---

### psLock
Lock specific processes from termination.

**Usage:** `psLock`

**Features:**
- Process protection
- Kill prevention
- Critical process locking
- Unlock functionality

**Examples:**
```bash
psLock                  # Lock processes
```

---

### psMon
Monitor and log process activity.

**Usage:** `psMon`

**Features:**
- Process monitoring
- Activity logging
- Resource tracking
- Alert generation

**Examples:**
```bash
psMon                   # Monitor processes
```

---

## Text Processing

### grep
Search for patterns in files with regex support.

**Usage:** `grep <pattern> <file>... [-i] [-l] [-n|-v] [-o] [-c] [-e]`

**Arguments:**
- `<pattern>` - Search pattern
- `<file>...` - Files to search (or use in pipes)

**Flags:**
- `-i` - Case-insensitive search
- `-l` - Show line numbers
- `-n` / `-v` - Invert match (show non-matching lines)
- `-o` - Count only (return number)
- `-c` - Count matching lines
- `-e` - Enable regex mode

**Features:**
- Pattern matching
- Regex support
- Multi-file search
- Line numbers
- Count matches
- Invert matching
- Glob pattern support

**Examples:**
```bash
grep "error" log.txt            # Find "error"
grep "ERROR" log.txt -i         # Case-insensitive
grep "failed" log.txt -l        # With line numbers
grep "success" log.txt -v       # Invert (non-matching)
grep "warning" *.log            # Search all .log files
grep "pattern" file.txt -c      # Count matches
grep "[0-9]+" data.txt -e       # Regex search
```

---

### sed
Stream editor for find and replace operations.

**Usage:** `sed <pattern> <replacement> [file]`

**Arguments:**
- `<pattern>` - Text to find
- `<replacement>` - Replacement text
- `[file]` - File to process (or use in pipes)

**Features:**
- Text substitution
- Regex support
- Global replacement
- Pipe integration
- In-place editing option

**Examples:**
```bash
sed "old" "new" file.txt        # Replace old with new
cat file.txt | sed "foo" "bar"  # Pipe usage
sed "error" "ERROR" *.log       # Multiple files
```

---

### awk
Field extraction and text processing.

**Usage:** `awk '<script>' [file]`

**Arguments:**
- `<script>` - AWK script/pattern
- `[file]` - File to process (or use in pipes)

**Special Variables:**
- `$0` - Entire line
- `$1, $2, ...` - Fields (space-separated by default)
- `$NF` - Last field
- `NF` - Number of fields
- `NR` - Line number

**Flags:**
- `-F<delimiter>` - Set field separator

**Features:**
- Field extraction
- Custom delimiters
- Pattern matching
- Mathematical operations
- Built-in variables

**Examples:**
```bash
awk '{print $1}' data.txt               # First field
awk -F: '{print $1}' /etc/passwd        # Colon delimiter
awk '{print $1, $3}' file.txt           # Multiple fields
awk '{print NR, $0}' file.txt           # Line numbers
awk -F: '{print $1, $NF}' data.txt      # First and last
```

---

### cut
Extract sections from each line.

**Usage:** `cut <file> [-b positions] [-c positions] [-f fields] [-d delimiter]`

**Arguments:**
- `<file>` - File to process

**Flags:**
- `-b <positions>` - Byte positions (e.g., 1-5, 10-, -20)
- `-c <positions>` - Character positions
- `-f <fields>` - Field numbers (1-based)
- `-d <delimiter>` - Field delimiter (default: whitespace)

**Features:**
- Byte extraction
- Character extraction
- Field extraction
- Custom delimiters
- Range support

**Examples:**
```bash
cut -f 1 data.txt               # First field
cut -f 1,3 data.txt             # Fields 1 and 3
cut -f 2 -d : /etc/passwd       # Second field, colon delim
cut -c 1-10 file.txt            # First 10 characters
cut -b 5-15 data.bin            # Bytes 5-15
```

---

### sort
Sort lines of text.

**Usage:** `sort [file]`

**Arguments:**
- `[file]` - File to sort (or use in pipes)

**Flags:**
- `-n` - Numeric sort
- `-r` - Reverse order
- `-u` - Unique (remove duplicates)

**Features:**
- Alphabetical sorting
- Numeric sorting
- Reverse sorting
- Deduplication
- Pipe integration

**Examples:**
```bash
sort file.txt                   # Alphabetical sort
sort -n numbers.txt             # Numeric sort
sort -r file.txt                # Reverse sort
sort -u file.txt                # Sort and deduplicate
cat data.txt | sort             # Pipe usage
```

---

### uniq
Remove or count duplicate lines.

**Usage:** `uniq [file]`

**Arguments:**
- `[file]` - File to process (or use in pipes)

**Flags:**
- `-c` - Count occurrences
- `-i` - Case-insensitive

**Features:**
- Remove consecutive duplicates
- Count duplicates
- Case-insensitive mode
- Works best with sorted input

**Examples:**
```bash
uniq file.txt                   # Remove duplicates
uniq -c file.txt                # Count occurrences
uniq -i file.txt                # Case-insensitive
sort file.txt | uniq            # Sort then deduplicate
```

---

### wc
Count words, lines, and characters.

**Usage:** `wc [file] [-l] [-w] [-c]`

**Arguments:**
- `[file]` - File to count (or use in pipes)

**Flags:**
- `-l` - Count lines only
- `-w` - Count words only
- `-c` - Count characters only

**Features:**
- Line counting
- Word counting
- Character counting
- Multi-file support
- Glob pattern support

**Examples:**
```bash
wc file.txt                     # All counts
wc -l file.txt                  # Line count
wc -w file.txt                  # Word count
wc -c file.txt                  # Character count
wc *.txt                        # Count all .txt files
cat file.txt | wc -l            # Pipe usage
```

---

### rev
Reverse strings or lines.

**Usage:** `rev [file]`

**Arguments:**
- `[file]` - File to reverse (or use in pipes)

**Features:**
- String reversal
- Line-by-line processing
- Pipe integration

**Examples:**
```bash
rev file.txt                    # Reverse each line
echo "hello" | rev              # Output: olleh
cat data.txt | rev              # Pipe usage
```

---

### tr
Translate or delete characters from input.

**Usage:** `tr [OPTIONS] <set1> [set2] [file]`

**Pipe Usage:** `echo TEXT | tr [OPTIONS] <set1> [set2]`

**Flags:**
- `-d` - Delete characters in SET1
- `-s` - Squeeze repeated characters
- `-c` - Complement SET1 (use all characters NOT in SET1)
- `-w` - Write output back to file (requires file argument)

**Notes:**
- `SET1` is always required (`tr -s` alone is invalid)
- `tr -d` also requires `SET1` (`tr -d` alone is invalid)
- `file` is required only when not using pipe input

**Common Errors:**
```bash
echo hello world | tr -s
# Error: Missing arguments: tr [OPTIONS] SET1 [SET2] FILE

echo hello world | tr -d
# Error: Missing arguments: tr [OPTIONS] SET1 [SET2] FILE
```

**Character Sets:**
- Individual characters: `aeiou`
- Ranges: `a-z`, `0-9`, `A-Z`

**Features:**
- Character translation
- Character deletion
- Repeated character squeezing
- Range support
- Pipe integration

**Examples:**
```bash
# Character translation
echo hello | tr aeiou 43100             # h3ll0
echo HELLO WORLD | tr A-Z a-z           # hello world
echo hello world | tr a-z A-Z           # HELLO WORLD

# Character deletion
echo hello123world456 | tr -d 0-9       # helloworld
echo a:b:c:d | tr -d :                  # abcd
echo hello world | tr -d ' '            # helloworld

# Squeeze repeated characters
echo hello    world | tr -s ' '         # hello world
echo heeelllooo | tr -s elo             # helo

# Combined operations
echo Hello   World123 | tr -d 0-9 | tr -s ' '  # Hello World
cat file.txt | tr A-Z a-z | tr -s ' '   # Normalize

# With piping
cat /etc/passwd | tr : ' ' | awk '{print $1}'  # Extract usernames
echo test123 | tr -d 0-9 | rev          # Delete digits then reverse

```

**See Also:** sed, awk, grep, cut, rev

---

### split
Split strings into arrays or files.

**Usage:** `split <delimiter> [file]`

**Arguments:**
- `<delimiter>` - Split delimiter
- `[file]` - File to split (or use in pipes)

**Features:**
- Custom delimiter splitting
- Array output
- Multi-line support
- Pipe integration

**Examples:**
```bash
split , data.csv                # Split CSV
echo "a:b:c" | split :          # Output: [a, b, c]
split " " words.txt             # Split on spaces
```

---

### join
Join array elements or lines with delimiter.

**Usage:** `join [delimiter] [file]`

**Arguments:**
- `[delimiter]` - Join delimiter (default: space)
- `[file]` - File to join (or use in pipes)

**Features:**
- Custom delimiter joining
- Array to string conversion
- Multi-line joining
- Pipe integration

**Examples:**
```bash
echo ["a", "b", "c"] | join ,   # Output: a,b,c
join - items.txt                # Join with dash
join "" letters.txt             # Join with no separator
```

---

### diff
Compare two files line by line.

**Usage:** `diff <file1> <file2>`

**Arguments:**
- `<file1>` - First file
- `<file2>` - Second file

**Features:**
- Line-by-line comparison
- Show differences
- Unified diff format
- Color-coded output

**Examples:**
```bash
diff old.txt new.txt            # Compare files
diff config.bak config.txt > changes.txt
```

---

### l33t
Convert text to/from l33t speak.

**Usage:** `l33t [-t|-f] [-i input] [-o output]`

**Flags:**
- `-t` - Convert to l33t speak
- `-f` - Convert from l33t speak
- `-i <file>` - Input file
- `-o <file>` - Output file

**Features:**
- L33t speak conversion
- Reverse conversion
- File I/O support
- Character substitution

**Examples:**
```bash
l33t -t -i input.txt -o output.txt      # To l33t
l33t -f -i l33t.txt -o normal.txt       # From l33t
echo "hello" | l33t -t                  # Pipe usage
```

---

### print
Display text with formatting.

**Usage:** `print <text...>`

**Arguments:**
- `<text...>` - Text to display

**Features:**
- Simple text output
- No newline option
- Color support via Text lib

**Examples:**
```bash
print Hello World               # Display text
print "Line 1" "Line 2"         # Multiple args
```

---

### echo
Display text with redirect support.

**Usage:** `echo <text...> [> file] [>> file]`

**Arguments:**
- `<text...>` - Text to display

**Redirects:**
- `> file` - Overwrite file
- `>> file` - Append to file

**Examples:**
```bash
echo Hello World                # Display
echo "log entry" >> log.txt     # Append
echo "config" > config.txt      # Overwrite
```

---

### write
Write text to file (interactive).

**Usage:** `write <file>`

**Arguments:**
- `<file>` - File to write to

**Features:**
- Interactive text entry
- Multi-line support
- Append mode
- Save confirmation

**Examples:**
```bash
write notes.txt                 # Interactive write
```

---

### xclip (xc)
Clipboard utility for storing and retrieving text values.

**Usage:** `xc` | `xc TEXT` | `xc --number [NUMBER]` | `xc [-p] [INDEX]` | `xc --clear`

**Flags:**
- `--number [NUMBER]` - Append numeric value to clipboard
- `-p [INDEX]` - Passive retrieval (no display)
- `--clear` - Remove all entries

**Features:**
- Multi-entry clipboard with indexed storage
- Resets when terminal session closes
- Supports `>` and `>>` redirect input
- Redirect input is never printed (security)

**Examples:**
```bash
xc                            # View all entries
xc password123                # Store text
xc 0                          # Get first entry
xc --clear                    # Clear clipboard
cat passwords.txt > xc        # Redirect file to clipboard
scan -l >> xc                 # Append scan output
```

---

### column
Format text into aligned columns.

**Usage:** `column [-s SEP] FILE` | `command | column [-s SEP] [-t]`

**Flags:**
- `-s <sep>` - Use separator as field delimiter (default: whitespace)
- `-t` - Auto-table mode (default when no separator specified)

**Features:**
- Reads from piped stdin or file argument
- Pads fields for vertical alignment
- Last field on each row is never padded

**Examples:**
```bash
cat /etc/passwd | column -s :   # Align colon-delimited fields
column -s : /etc/passwd         # Read file directly
ps | column                     # Align process output
```

---

### jq
Extract fields from structured key-value or JSON-style text.

**Usage:** `jq [-r] [-c] expression [file]` | `command | jq [-r] [-c] expression`

**Flags:**
- `-r` - Raw output (value only, no key prefix)
- `-c` - Compact output (suppress blank lines between multi-field results)

**Features:**
- Parses `key: value`, `key=value`, and JSON-style formats
- Dot-notation (`jq .key.subkey`)
- Multi-field extraction (`jq [.k1,.k2]`)
- `.` to print all pairs
- Reads from stdin or file argument

**Examples:**
```bash
cat /etc/apt/sources.txt | jq .official_server
cat config.txt | jq -r .host           # Value only
jq .host /home/tux/config.txt          # Read from file
cat data.txt | jq [.name,.ip]          # Multiple fields
```

---

### tee
Read from stdin and write to files and stdout simultaneously.

**Usage:** `tee [-a] [FILE...]`

**Flags:**
- `-a` / `--append` - Append to files rather than overwriting

**Features:**
- Captures pipe output to one or more files while passing through
- If no files specified, passes input through to stdout only

**Examples:**
```bash
bc ip | tee scan_target.txt | nmap      # Save IP while scanning
nmap 192.168.1.1 | tee results.txt | grep open  # Save and filter
echo Status: OK | tee -a activity.log  # Append to log
ls | tee list1.txt list2.txt           # Write to multiple files
```

---

### trim
Strip leading and trailing whitespace from each line.

**Usage:** `trim FILE` | `trim -w FILE` | `command | trim`

**Flags:**
- `-w` / `--write` - Write trimmed output back to file in-place

**Features:**
- By default prints trimmed output to stdout
- With `-w`, modifies the file in-place
- Supports piped input

**Examples:**
```bash
trim notes.txt                  # Print trimmed lines
trim -w config.ini              # Overwrite file with trimmed content
cat data.txt | trim             # Trim piped input
```

---

## Development Tools

### build
Compile GreyScript source files.

**Usage:** `build <source> <output> [-a] [-r]`

**Arguments:**
- `<source>` - .src file to compile
- `<output>` - Output directory

**Flags:**
- `-a` - Allow imports
- `-r` - Run after build

**Features:**
- GreyScript compilation
- Import resolution
- Binary output
- Auto-execution option
- Error reporting

**Examples:**
```bash
build script.src /bin                   # Compile to /bin
build app.src /usr/bin -a               # With imports
build tool.src /bin -r                  # Compile and run
```

---

### make
Advanced build system for custom binaries and tools.

**Usage:** `make [-b flags name] [-a] [-t name] [-r] [-pm|-pp|-pc] [-i bin mode]`

**Flags:**
- `-b <flags> <name>` - Build with flags (S,V,R,T,P,E,D,C,F)
  - S: System info, V: Verbose, R: rshell, T: Terminal output
  - P: Progress bar, E: Encryption, D: Database, C: Crypto
  - F: Firewall disable
- `-a` - Build all tools
- `-t <name>` - Build specific tool
- `-r` - Build rshell backdoor
- `-pm` - Build proxy manager
- `-pp` - Build proxy parser
- `-pc` - Build proxy chain
- `-i <bin> <mode>` - Inject code into binary

**Features:**
- Multi-flag compilation
- Tool-specific builds
- Proxy chain creation
- Code injection
- rshell generation
- Custom binaries

**Examples:**
```bash
make -b RP htop                 # Build htop with rshell+progress
make -a                         # Build all tools
make -t nmap                    # Build nmap tool
make -r                         # Build rshell
make -pm                        # Build proxy manager
make -i /bin/tool S             # Inject system info
```

---

### exec
Execute binaries with directory search.

**Usage:** `exec <file> [args...] [-u] [-b]`

**Arguments:**
- `<file>` - Binary to execute
- `[args...]` - Command arguments

**Flags:**
- `-u` - Search /usr/bin
- `-b` - Search /bin

**Features:**
- Binary execution
- Multi-directory search
- Argument passing
- Path resolution

**Examples:**
```bash
exec tool                       # Execute ./tool
exec -b nmap 192.168.1.1        # Execute /bin/nmap
exec -u program arg1 arg2       # Execute /usr/bin/program
```

---

### ai
AI-powered natural language command execution.

**Usage:** `ai <natural_language_command>`

**Arguments:**
- `<natural_language_command>` - Plain English command description

**Separators (priority order):**
- `and then` - Highest priority step separator
- `also` - Secondary step separator
- `,` (comma) - Tertiary separator
- `and` - Lowest priority separator

**Features:**
- Natural language parsing
- Multi-step automation
- Conditional execution ("if not root then su")
- Context switching support
- IP/port/service extraction
- Credential detection
- GUI app translation (21 apps)
- Deferred command mechanism

**Examples:**
```bash
ai scan 192.168.1.1 for ssh                     # Port scan
ai get ssh from 192.168.1.1 then show accounts  # Multi-step
ai connect to ftp.example.com also download config.txt
ai exploit target.com, if not root then su, then install backdoor
ai open email local with login                  # Open GUI app
```

**Conditional Examples:**
```bash
ai if not root then su                          # Check privilege
ai get shell then if not root then escalate     # Multi-conditional
```

**Service Detection:**
```bash
ai connect to ssh 192.168.1.1 port 22          # Explicit port
ai get ftp shell from target.com                # Service type
ai scan for http and exploit                    # Service scan
```

---

### run
Advanced bash script interpreter with full programming features.

**Usage:** `run script|@script [-e [name]] [--list] [-n [name]] [-o] [--FILE file script] [--DEBUG] [--ALLOWABS]`

**Shorthand:** `@script_name`

**Flags:**
- `-e [name]` - Edit existing bash script in vi
- `--list` - List all available bash scripts
- `-n [name]` - Create new bash script in vi
- `-o` - Open bash folder
- `--FILE <file> <script>` - Execute with parameters from file
- `--DEBUG` - Enable debug mode with execution flow
- `--ALLOWABS` - Allow absolute path execution
- `--SIGBREAK` - Break execution on warnings
- `--SIGCONT` - Continue after errors
- `--ONERROR <cmd>` - Execute command on error

**Control Flow:**
- `if/elif/else/endif` - Conditionals (==, !=, <, >, <=, >=, and, or, not)
- `switch/case/default/endswitch` - Pattern matching
- `while/endwhile` - Condition-based loops
- `until/enduntil` - Loop until condition true
- `for/endfor` - Iteration (lists, ranges, variables)
- `break` - Exit loop
- `continue` - Skip to next iteration

**Functions:**
- `func name(params) / endfunc` - Define functions (recursion depth: 10)
- `return_value expr` - Return value with arithmetic
- `return [command]` - Exit script/function

**Variables:**
- `_setvar(name,value)` - Set variable
- `_getvar(name)` - Retrieve variable
- Arithmetic: +, -, *, /, %, ** (power)

**Arrays:**
- `_push list value` - Add to end
- `_pop list` - Remove from end
- `_pull list` - Remove from start
- `_len name` - Get length
- `_in list value` - Check existence

**Built-in Functions:**
- String: `len()`, `upper()`, `lower()`, `substr()`, `concat()`, `contains()`, `replace()`, `join()`, `split_str()`, `trim_str()`
- Math: `floor()`, `ceil()`, `abs()`, `round()`, `min()`, `max()`, `random()`, `timestamp()`, `date()`
- File: `file_exists()`, `is_folder()`, `is_binary()`, `file_read()`
- Permissions: `get_permissions()`, `_fs_canwrite()`, `_fs_canexec()`
- Context: `get_user()`, `get_home()`, `get_shell_type()`, `get_computer_lan_ip()`, `get_computer_public_ip()`, `get_root()`, `get_layer()`
- Type: `typeof_val()`, `get_type()`
- Boolean: `to_yesno()`, `to_truefalse()`

**Typed Input:**
- `get_string [prompt]` - String input
- `get_integer [prompt]` - Integer input
- `get_decimal [prompt]` - Decimal input
- `get_any [prompt]` - Any value (unlimited use)
- `get_yesno [prompt]` - Yes/no input (returns 1/0)

**Bash Commands:**
- `_print` - Print with color support and variable substitution
- `_fs_read` - Read file content
- `_fs_view` - Display file content
- `_fs_write` - Write to file
- `_fs_find` - Search files (-c content, -e exact)
- `_fs_put` - Upload file to remote (shell only)
- `_fs_get` - Download file from remote (shell only)
- `_home` - Safe return to caller (prevents IPC deadlock)
- `_sys_whoami` - Get current username
- `_sys_whatami` - Get execution context type
- `_fs_pwd` - Print working directory
- `_net_ports` - Scan router for ports
- `_net_router` - Display router information
- `_net_devices` - List LAN devices
- `_net_devports` - Show device ports  
- `_net_fwrules` - Display firewall rules
- `_net_random` - Generate random public IP

**Color Functions:**
`orange()`, `cyan()`, `magenta()`, `lime()`, `bred()`, `green()`, `password()`, `blue()`, `liteblue()`, `yellow()`, `white()`, `purple()`, `iyellow()`, `liteGrey()`, `error()`, `red()`, `grey()`, `black()`, `bold()`

**Examples:**
```bash
# Basic execution
run myscript.src        # Run script
@myscript               # Shorthand
run script.src arg1 arg2  # With parameters

# Script management
run --list              # List all scripts
run -n newscript        # Create new script
run -e oldscript        # Edit script
run -o                  # Open bash folder

# Conditionals
if _getvar(age) >= 18
  _print Access granted
else
  _print Access denied
endif

# Loops
for ip in [192.168.1.1,192.168.1.2,192.168.1.3]
  _print Scanning _getvar(ip)
  scan --c _getvar(ip) router
endfor

# Functions
func multiply(a,b)
  return_value _getvar(a)*_getvar(b)
endfunc
_setvar(result,multiply(6,7))
_print 6 * 7 = _getvar(result)

# User input
_setvar(target,get_string(Enter target IP:))
_print Targeting: _getvar(target)

# Debug mode
run --DEBUG script.src
```

**See Also:** bash.md (in docs/), ai

---

### editor
Simple GUI text editor.

**Usage:** `edit <file>` or `edit -n <name> [text]`

**Command:** `edit`

**Flags:**
- `-n <name> [text]` - Create new file with optional initial text

**Features:**
- Graphical interface
- File creation and editing
- Optional initial content

**Examples:**
```bash
edit /home/tux/config.src           # Edit existing file
edit -n /home/tux/notes.txt          # Create new empty file
edit -n readme.txt Welcome!          # Create with initial text
```

**See Also:** cat, vi, post

---

### repl
Glosure interactive REPL and script runner.

**Usage:** `repl` | `repl FILE [ARGS...]` | `repl -e EXPR` | `repl -i [FILE [ARGS...]]` | `repl -p PATH [FILE [ARGS...]]`

**Flags:**
- `FILE` - Execute a Glosure source file
- `-e <expr>` - Evaluate a single expression inline
- `-i` - Interactive mode (optionally after running a file, keeping defs in scope)
- `-p <path>` - Set a scripts search prefix directory

**Features:**
- Lisp-like scripting language (Glosure)
- `def`, `lambda`, `if`, `while`, `for`, `foreach`, `defun`, `begin`, `dot`, `array`, `dict`
- All x shell commands available via `(x 'cmd')`
- Last result bound to `_`
- REPL commands: `clear`, `exit`, `;quit`

**Examples:**
```bash
repl                                    # Start interactive REPL
repl -e (+ 10 (* 3 4))                 # Evaluate expression (prints 22)
repl -i test 177.165.65.149 22          # Run file then drop into REPL
repl script.gls arg1 arg2              # Execute script with arguments
```

---

## Package Management

### pacman
Arch-style package manager for Grey Hack system.

**Usage:** `pacman <command> [options]`

**Commands:**
- `setup` - Initialize pacman and apt structure
- `-Sl` - List all repositories
- `-Sy` - Synchronize and update package databases
- `-S` - Install packages
- `-Ss <query>` - Search for packages
- `-Si [repo]` - Show packages from repository
- `-Sa <ip> [port]` - Add repository
- `-Sd <ip>` - Delete repository
- `-Su` - Upgrade packages

**Sync/Update Flags (-Sy):**
- `-e` - Update exploit database only
- `-l` - Update local exploit database
- `-f` - Update only scannable libraries
- `--force` - Force rescan all libraries
- `-c <count>` - Number of passes (default: 10)

**Install Flags (-S):**
- `-m` - Install/upgrade metaxploit.so
- `-c` - Install/upgrade crypto.so
- `-b` - Install/upgrade both critical libraries
- `-a` - Install arbitrary packages
- `-p <path>` - Specify install path
- `-i <path>` - Alternative path specification

**Add Repo Flags (-Sa):**
- `-r` - Fetch random public repository

**Upgrade Flags (-Su):**
- `-y` - Auto-confirm upgrades
- `-a <package>` - Upgrade specific package
- `-p <path>` - Specify search path
- `-i <path>` - Specify install path

**Features:**
- Arch-style interface
- Automatic path detection by extension
- Root permission handling for system dirs
- Multi-package installation
- Exploit database synchronization
- Deep library extraction via shell exploits
- Repository management
- Smart upgrade detection

**Examples:**
```bash
pacman setup                    # Initialize system
pacman -Sl                      # List repositories
pacman -Sa -r                   # Add random repo
pacman -Sa 192.168.1.1 1542     # Add specific repo
pacman -Sd 192.168.1.1          # Remove repo
pacman -Sy                      # Sync/update databases
pacman -Sy -e -c 20             # Update exploits (20 passes)
pacman -Sy -f                   # Update scannable only
pacman -Sy --force              # Force rescan all
pacman -S -m                    # Install metaxploit
pacman -S -b                    # Install both critical libs
pacman -S -a nmap               # Install nmap
pacman -S -a tool.exe -p /bin   # Install to /bin
pacman -Ss nmap                 # Search for nmap
pacman -Si                      # Show packages from default repo
pacman -Si 192.168.1.1          # Show from specific repo
pacman -Su                      # Upgrade all packages
pacman -Su -a nmap -y           # Upgrade nmap, auto-confirm
```

**See Also:** [build](#build)

---

## Utilities

### bc
Advanced calculator with functions.

**Usage:** `bc <operation> [args...]`

**Operations:**
- **Arithmetic:** `+`, `-`, `*`, `/`, `%`, `^` (power)
- **Functions:** `sqrt`, `abs`, `sin`, `cos`, `tan`, `floor`, `ceil`, `round`
- **Constants:** `pi`, `e`
- **Random:** `rnd [max]`, `rip [count]` (random IPs)
- **Conversion:** `bin`, `hex`, `oct`, `char`, `code`

**Features:**
- Order of operations (PEMDAS)
- Trigonometric functions
- Random number generation
- Random IP generation
- Number base conversion
- Character/ASCII conversion

**Examples:**
```bash
bc 10 + 5                       # 15
bc 2 ^ 10                       # 1024
bc sqrt 144                     # 12
bc sin 0                        # 0
bc pi                           # 3.14159...
bc rnd 100                      # Random 0-100
bc rip 5                        # 5 random IPs
bc hex 255                      # FF
bc char 65                      # A
bc code A                       # 65
```

---

### !
Execute last command from history.

**Usage:** `!`

**Features:**
- Re-run most recent command
- No modification
- Quick repetition

**Examples:**
```bash
scan -l                         # Run scan command
!                               # Re-execute scan -l

hunt ssh                        # Find SSH service
!                               # Find another SSH service
!                               # And another

exploit -l 192.168.1.50 ssh s   # Exploit target
!                               # Retry exploitation
```

**See Also:** !!, !!!

---

### !!
Display command history.

**Usage:** `!!`

**Features:**
- Show history buffer
- Review past operations
- Command selection

**Examples:**
```bash
!!                              # Show command history

# Review recent operations
scan -l                         # Execute commands
exploit -l TARGET ssh s         # More commands
!!                              # Review what was done

# Combined usage
!!                              # View history
!                               # Execute last command
```

**See Also:** !, !!!

---

### !!!
Print last issued command without executing.

**Usage:** `!!!`

**Features:**
- Display last command
- No execution
- Command verification

**Examples:**
```bash
scan -l                         # Execute a command
!!!                             # Print scan -l

# Verification workflow
exploit -l 192.168.1.50 ssh s   # Run complex command
!!!                             # Verify what was executed
!                               # Re-execute if correct

# Command comparison
!!!                             # Show last command
!!                              # Show full history
!                               # Execute last command
```

**See Also:** !, !!

---

### swap
Swap contents of two files.

**Usage:** `swap <file1> <file2>`

**Arguments:**
- `<file1>` - First file
- `<file2>` - Second file

**Features:**
- Atomic content swap
- Preserves permissions
- No data loss

**Examples:**
```bash
swap config.txt config.bak      # Swap configs
swap a.txt b.txt                # Swap contents
```

---

### rn
Rename files with pattern support.

**Usage:** `rn <old> <new> [path]`

**Arguments:**
- `<old>` - Pattern to find
- `<new>` - Replacement pattern
- `[path]` - Directory (default: current)

**Features:**
- Batch renaming
- Pattern matching
- Wildcard support
- Recursive option

**Examples:**
```bash
rn .txt .bak                    # Rename extensions
rn old new /var                 # Rename in /var
rn test prod                    # Rename test to prod
```

---

### bork
Reverse all filenames in directory (chaos mode).

**Usage:** `bork [directory]`

**Arguments:**
- `[directory]` - Directory to process (default: current)

**Features:**
- Reverse all filenames
- Extension preservation
- Recursive option
- Undo capability

**Examples:**
```bash
bork                            # Reverse current dir
bork /var                       # Reverse /var
```

---

### post
Append entries to persistent notes file.

**Usage:** `post <text...>`

**Arguments:**
- `<text...>` - Text to append

**Features:**
- Persistent notes
- Timestamp entries
- Append mode
- Quick access

**Examples:**
```bash
post Remember to backup         # Add note
post "Meeting at 3pm"           # Add reminder
```

---

### postPW
Append password entries to secure notes.

**Usage:** `postPW <text...>`

**Arguments:**
- `<text...>` - Password entry

**Features:**
- Secure password storage
- Encrypted notes
- Timestamp entries
- Quick recall

**Examples:**
```bash
postPW root@server: pass123     # Store password
postPW admin login credentials  # Store creds
```

---

### man
View command help documentation and manual pages.

**Usage:** `man <command>` or `<command> --help`

**Commands:**
- `man <command>` - Display command manual
- `man apropos <keyword>` - Search man pages
- `man search <keyword>` - Find commands by keyword  
- `man dump [command]` - Export man pages to files
- `cmds` / `help` - List all commands

**Wildcards:**
- `~` - Home directory
- `.` - Current directory
- `..` - Parent directory
- `*` - Wildcard pattern

**Examples:**
```bash
man ls                          # View ls manual
man apropos network             # Find network commands
man dump ssh                    # Export ssh man page
cmds                            # List all commands
```

---

## Network & Remote Access

### ssh
Securely access remote computers via SSH.

**Usage:** `ssh [-l] [-t] [-p port] [-P password] user@host`

**Flags:**
- `-p <port>` - Custom port (default: 22)
- `-P <password>` - Provide password
- `-t` - Enable tunneling (map public IP)
- `-l` - Force local main shell

**Features:**
- Secure remote access
- File transfer with scp
- Password encryption support
- Interactive mode

**Examples:**
```bash
ssh tux@remotehost              # Connect with prompt
ssh -P linux tux@host           # With password flag
ssh -p 2222 admin@server        # Custom port
ssh -t -P mypass root@target    # Tunnel with password
scp -d file.txt                 # Download file
scp -u local.txt                # Upload file
```

**See Also:** ftp, sssh, nmap

---

### sssh
SSH that returns shell object instead of terminal.

**Usage:** `sssh [-l] [-t] [-p port] [-P password] user@host`

**Flags:**
- `-p <port>` - Custom port (default: 22)
- `-P <password>` - Provide password
- `-t` - Enable tunneling
- `-l` - Force local main shell

**Features:**
- Returns shell object for scripting
- Programmatic remote access
- Same flags as ssh command

**Examples:**
```bash
sssh tux@remotehost             # Get shell object
sssh -p 2222 admin@server       # Custom port
sssh -t -P pass root@target     # Tunnel with password
```

**See Also:** ssh, ftp

---

### ftp
File Transfer Protocol for file exchange.

**Usage:** `ftp [-l] [-t] [-p port] [-P password] user@host`

**Flags:**
- `-p <port>` - Custom port (default: 21)
- `-P <password>` - Provide password
- `-t` / `--tunnel` - Enable tunneling
- `-l` - Force local main shell

**Features:**
- File upload/download
- Directory navigation
- No remote command execution
- Interactive mode with help

**Examples:**
```bash
ftp tux@remotehost              # Connect with prompt
ftp -p 2121 admin@server        # Custom port
ftp -t -P pass root@target      # Tunnel with password
get file.txt                    # Download (when connected)
put local.txt                   # Upload (when connected)
```

**See Also:** ssh, sssh, scp

---

### proxy
Advanced proxy chain and routing management.

**Usage:** `proxy [options]`

**Key Flags:**
- `-b` - Build proxy chain from Map.conf
- `-q` - Quick single hop router proxy
- `-c` - Count hops in chain
- `-x` - Combine proxy.dat and Map.conf
- `-ri <file>` - Import IPs to Map.conf
- `-wo <file>` - Export Map.conf
- `-d` - Create crash decoy
- `-d -r` - Remove and recreate decoy

**Features:**
- Multi-hop proxy chains
- IP mapping and routing
- Decoy creation
- Chain management

**Examples:**
```bash
proxy -b                        # Build proxy chain
proxy -q                        # Quick single hop
proxy -c                        # Count hops
proxy -ri custom_ips.dat        # Import IPs
proxy -d                        # Create decoy
```

---

### pivot
Copy and launch X framework on target systems.

**Usage:** `pivot [-y]`

**Flags:**
- `-y` - Full pivot (complete X framework copy)

**Pivot Types:**
- **Minimal** (default) - Used for scanning libraries, installing services
- **Full** (-y flag) - Complete X framework copy with all features

**Features:**
- Remote framework deployment
- Continued operations on compromised systems
- Auto-detection of existing X installations
- Maximum pivots (self launches): 17

**Examples:**
```bash
# Basic pivoting
scan -p 192.168.1.50 22         # Exploit SSH
pivot                            # Minimal pivot (prompted)
pivot -y                         # Full pivot

# Multi-hop pivoting
scan 192.168.1.100              # Compromise first target
pivot                            # Pivot to first system
scan -n                          # Scan from pivot
scan -p 192.168.2.50 22         # Exploit second target
pivot                            # Nested pivot

# Strategic operations
pivot -y                         # Full pivot for extended ops
scan -l                          # Scan libraries after pivot
scan -n                          # Scan network from pivot

# Pivot chain
hunt ssh -c 1                    # Find SSH target
scan -p TARGET 22                # Exploit found target
pivot                            # Establish pivot point
```

**See Also:** pull, hops, proxy

---

### pull
Upload payload folder for fresh launch.

**Usage:** `pull`

**Features:**
- Payload folder upload
- Fresh framework initialization
- Required before launching
- Pivoted instances only

**Examples:**
```bash
# Pre-launch setup
pull                             # Upload payload data
launch                           # Start framework

# Pivot workflow
pull                             # Upload to pivoted system
start                            # Initialize framework
```

**See Also:** pivot

---

### hops
View, wipe, or interact with proxy chain.

**Usage:** `hops -v|-w|-s <index>`

**Flags:**
- `-v` - View all proxy chain hops
- `-w` - Wipe logs from all hops
- `-s <index>` - Take shell from specific hop

**Features:**
- Proxy chain visualization
- Log cleaning across chain
- Shell control from any hop
- Chain management

**Examples:**
```bash
hops -v                          # List all hops
hops -w                          # Clean logs from all proxies
hops -s 3                        # Take control of 3rd hop
hops -s 1                        # Take control of first hop
```

**See Also:** proxy, pivot

---

### netcat
Display comprehensive LAN network information.

**Usage:** `netcat`

**Features:**
- Extensive subnet details
- Network reconnaissance
- Alternative to recon/map
- Shell objects only (main, shell, pivot, proxy)

**Examples:**
```bash
netcat                          # Show LAN info
```

**See Also:** nmap, ifconfig, iwconfig

---

## System Tools

### rat
Remote RAT server file editor.

**Usage:** `rat [ip] [port] [password]`

**Features:**
- On-the-fly RAT file editing
- Remote management
- Interactive credential prompts

**Examples:**
```bash
rat 136.22.27.184 22 xxxx       # Connect with password
rat 136.22.27.184 22            # Prompt for password
rat                             # Prompt for all details
```

**See Also:** ssh, ftp

---

### main
Control main instance from pivoted sessions.

**Usage:** `main <command>` or `main [-u|-d] [-p path] [--log] files...`

**Flags:**
- `-u` - Upload files from main to target
- `-d` - Download files from target to main
- `-p <path>` - Specify source/destination path
- `--log` - Transfer system.log file

**Features:**
- Run commands on main instance
- File transfer between main and target
- Log file management
- Pivot/proxy contexts only

**Examples:**
```bash
main ls -la                     # Run command on main
main -u file1 file2             # Upload to target
main -d -p /downloads data.txt  # Download to path
main -u --log                   # Upload system.log
```

**See Also:** pivot, proxy

---

### loop
Memory buffer overflow exploitation tool.

**Usage:** `loop -r ip:port memory unsecure_value wait [extra]`  
**Usage:** `loop -l library memory unsecure_value wait [extra]`

**Flags:**
- `-r` - Remote attack (IP:PORT)
- `-l` - Local attack (library file)

**Examples:**
```bash
loop -r 127.1.1.1:22 0x29320210 destr 5
loop -l /lib/libssh.so 0xAABBCCDD exploit 10
```

**See Also:** decipher, scanlib, build

---

### logs
System log file management and transfer.

**Usage:** `logs [-s|-r|-u|-d]`

**Flags:**
- `logs` - Download, edit, re-upload system.log
- `-s` - Send to server:/temp
- `-r` - Retrieve from server:/temp
- `-u` - Upload to server
- `-d` - Download from server

**Features:**
- Log editing workflow
- Server storage (requires x database)
- Shell objects only
- Requires root for modifications

**Examples:**
```bash
logs                            # Edit target log
logs -s                         # Send to server
logs -r                         # Retrieve from server
```

**See Also:** cat, vi, chmod

---

### lt
Log route tracking and visualization.

**Usage:** `lt -a|-r|-l|-x|-m|-w <args>`

**Flags:**
- `-a <from_ip> <to_ip>` - Add IP pair to tracker
- `-r <index>` - Remove entry by index
- `-l` - List all tracked routes
- `-x` - Clear all entries
- `-m` - Enter management mode (interactive)
- `-w` - Write to ip_tracker.lst in current directory

**Color Coding:**
- Yellow = LAN IP address
- Green = Public IP address

**Tracing Strategy:**
When both IPs are green, attack the router and examine logs. Search for the LAN IP in logs, then track that system. Final entry should show two green IPs when you reach origin.

**Features:**
- Visual route tracking
- Multi-hop path following
- Router bounce tracing
- Color-coded IP display
- Connection chain management

**Examples:**
```bash
# Build route chain
lt -a 177.61.158.111 192.168.0.2    # Add first hop
lt -a 177.61.158.111 101.35.57.9    # Add second hop
lt -a 101.35.57.9 26.87.87.62       # Continue tracking

# View and manage
lt -l                                # List all routes
lt -m                                # Interactive mode
lt -r 2                              # Remove entry 2
lt -x                                # Clear all
lt -w                                # Save to file
```

**See Also:** logs, cat

---

### specs
Display system specifications calculator.

**Usage:** `specs`

**Examples:**
```bash
specs                           # Show system info
```

**See Also:** ifconfig, iwconfig

---

### cal
Display calendar with output redirection support.

**Usage:** `cal [> file] [>> file]`

**Examples:**
```bash
cal                             # Show calendar
cal > cal.txt                   # Save to file
cal >> cal.txt                  # Append to file
```

---

### devices
List available devices for operations.

**Usage:** `devices`

**Examples:**
```bash
devices                         # List all devices
```

---

### do
Repeat commands multiple times or continuously.

**Usage:** `do -c <count> <command>` or `do --while <command>`

**Flags:**
- `-c <count>` - Execute N times
- `--while` - Execute continuously until 'q' is pressed

**Examples:**
```bash
do -c 5 print hello             # Print 5 times
do -c 10 ls                     # List 10 times
do --while nmap 192.168.1.1     # Continuous scanning
```

**See Also:** wait, arrow

---

### mark
Internal timer for benchmarking.

**Usage:** `mark`

**Features:**
- Start/display elapsed time
- Benchmarking tool
- Seconds counter

**Examples:**
```bash
mark                            # Start timer
mark                            # Show elapsed time
```

**See Also:** wait, time

---

## Encryption & Security

### pzip
File encryption with crypto library.

**Usage:** `pzip [-c|-e|-d] [-r] [-p password] <file|path>`

**Flags:**
- `-c` - Check encryption status
- `-e` - Encrypt file/directory
- `-d` - Decrypt file/directory
- `-r` - Recursive (directories)
- `-p <password>` - Specify password

**Examples:**
```bash
pzip -c /etc/passwd             # Check status
pzip -e -p mypass /etc/passwd   # Encrypt file
pzip -e -r /bin                 # Encrypt directory
pzip -d -p mypass file.enc      # Decrypt
```

**See Also:** enc, dec, aes128

---

### encrypt (enc)
Encrypt file with X algorithm.

**Usage:** `enc <file> [seed|key]`

**Features:**
- X encryption algorithm
- Immune to crypto library overflows
- Optional seed/key

**Examples:**
```bash
enc secret.txt                  # Encrypt file
enc data.bin mykey123           # With key
```

**See Also:** dec, pzip

---

### decrypt (dec)
Decrypt file with X algorithm.

**Usage:** `dec <file> [seed|key]`

**Features:**
- X decryption algorithm
- Immune to crypto library overflows
- Optional seed/key

**Examples:**
```bash
dec secret.txt                  # Decrypt file
dec data.bin mykey123           # With key
```

**See Also:** enc, pzip

---

### aes128
128-bit AES encryption and decryption.

**Usage:** `aes128 -e|-d|-k <key> <string>`

**Flags:**
- `-e <key> <string>` - Encrypt password or string with 128-bit key
- `-d <key> <string>` - Decrypt password or string with 128-bit key
- `-k` - Generate new AES 128-bit encryption key

**Features:**
- Advanced Encryption Standard
- Key generation
- String/password encryption
- 128-bit security

**Examples:**
```bash
# Generate key
aes128 -k                       # Generate 128-bit key

# Encrypt
aes128 -e a1b2c3d4 mypassword   # Encrypt with key

# Decrypt
aes128 -d a1b2c3d4 encrypted    # Decrypt with key
```

**See Also:** enc, dec, sha256, pzip

---

### sha256
SHA-256 cryptographic hashing.

**Usage:** `sha256 <text>` or `sha256 -c <hash>`

**Flags:**
- `-c <hash>` - Attempt to crack SHA-256 hash

**Features:**
- 256-bit hash generation
- Cryptographic security
- Hash cracking
- One-way transformation

**Examples:**
```bash
# Generate hash
sha256 password123              # Hash a password
sha256 Hello World              # Hash text string

# Crack hash
sha256 -c a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3
```

**See Also:** decipher, crack, aes128

---

## Additional Commands from Man2

### server
Manage database or LMS server operations.

**Usage:** `server [-l|-t|-s|-o|-f|-p|-r|-n|-z|refresh]`

**Flags:**
- `-l` - Launch a binary or script
- `-t` - Start a terminal
- `-s` - Start a shell
- `-o OPEN_FLAG [PARAMS]` - Open files or resources
- `-f` - View filesystem statistics
- `-p` - View and manage server processes
- `-r` - Wipe trash
- `-n` - View the notes file
- `-z` - Secure the server and filesystem
- `refresh` - Refresh the exploit database

**Features:**
- Manage server without running sys -d
- Execute common management commands
- Launch binaries and start sessions
- View stats and manage processes
- Requires active server connection

**Examples:**
```bash
server -l scanner.bin   # Launch scanner on server
server -t               # Start terminal session
server -f               # View filesystem stats
server -z               # Secure server filesystem
server refresh          # Update exploit database
```

**See Also:** [sys](#sys), [service](#service), [net](#net)

---

### net
Network toolkit for SSH connections, IP spoofing, and server installation.

**Usage:** `net [-c|-l|-b|-g|-x|-z|-i]`

**Flags:**
- `-c IP PORT USER PASSWORD` - Connect to network
- `-l` - List background connections
- `-b -l [SECONDS] [-m MIN] [-x MAX]` - Change local LAN IP dynamically
- `-b -f FILE [SECONDS]` - Change local LAN IP from file
- `-b -w FILE [SECONDS]` - Change WiFi connection from file
- `-g` - View network configuration
- `-x ID` - Close background network connection
- `-z` - Clear the network cache
- `-i rshell|ssh|ftp|http|chat|repo` - Install server on localhost

**Features:**
- Background SSH connections
- Dynamic IP rotation for evasion
- WiFi connection rotation
- Server installation from vfile/share
- Network configuration management

**Examples:**
```bash
net -c 192.168.1.5 22 admin pass123  # Connect to SSH
net -l                                # List background connections
net -b -l                             # Auto-rotate LAN IP
net -b -l -m 10 -x 100 5             # Rotate IP .10-.100 every 5s
net -b -w wifi.txt                    # Rotate WiFi from list
net -i ssh                            # Install SSH server
```

**See Also:** [ssh](#ssh), [service](#service), [ifconfig](#ifconfig)

---

### vfile
Virtual file cache management system.

**Usage:** `vfile [-l|-a|-ap|-al|-ts|-v|-g|-r|-x]`

**Flags:**
- `-l` - List cached files
- `-a FILE [FILE...]` - Add files to cache
- `-ap` - Add passwd to cache
- `-al` - Add system.log to cache
- `-ts` - Transfer vfile to share
- `-v ID` - View cached file
- `-g ID [ID...]` - Get files from cache (download)
- `-r ID [ID...]` - Remove files from cache
- `-x` - Clear all cache

**Features:**
- Store files with virtual IDs
- Temporary memory cache
- Transfer between objects
- Download to local machine
- Quick access to passwd/system.log
- Cache cleared when x closes

**Examples:**
```bash
vfile -l                # List cached files
vfile -a exploit.bin    # Add file to cache
vfile -ap               # Add passwd to cache
vfile -v 1              # View cached file ID 1
vfile -g 1 2 3          # Download files 1, 2, 3
vfile -ts               # Transfer to share
```

**See Also:** [share](#share), [cat](#cat), [cp](#cp)

---

### share
Persistent file sharing system.

**Usage:** `share [-l|-a|-v|-g|-r|-x]`

**Flags:**
- `-l` - List shared files
- `-a FILE [FILE...]` - Add files to share
- `-v ID` - View shared file
- `-g ID [ID...]` - Get files from share
- `-r ID [ID...]` - Remove files from share
- `-x` - Clear all shared files

**Features:**
- Persistent file storage
- Survives x restart
- Transfer files between sessions
- Library and binary sharing
- Unique ID assignment

**Examples:**
```bash
share -l                # List shared files
share -a tool.bin       # Add file to share
share -v 1              # View shared file
share -g 1 2            # Download files
share -r 1              # Remove file
```

**See Also:** [vfile](#vfile), [libs](#libs), [cp](#cp)

---

### libs
Manage system libraries and dependencies.

**Usage:** `libs [-l|-s|-d|-i|-r]`

**Flags:**
- `-l` - List available libraries
- `-s LIB` - Search for specific library
- `-d LIB` - Download library
- `-i LIB` - Install library
- `-r LIB` - Remove library

**Features:**
- Library management
- Dependency resolution
- Installation automation
- Version tracking

**Examples:**
```bash
libs -l                 # List libraries
libs -s metaxploit      # Search for library
libs -d crypto.so       # Download library
libs -i aptclient.so    # Install library
```

**See Also:** [load](#load), [lms](#lms), [share](#share)

---

### load
Load specific libraries into memory.

**Usage:** `load [-m|-c|-b|-a|-t|-s]`

**Flags:**
- `-m` - Load Metaxploit (metaxploit.so)
- `-c` - Load Crypto (crypto.so)
- `-b` - Load Blockchain (blockchain.so)
- `-a` - Load APTClient (aptclient.so)
- `-t` - Load TrafficNet (libtrafficnet.so)
- `-s` - Load Smart Appliance (libsmartappliance.so)

**Features:**
- Load libraries into memory
- Immediate function access
- Six supported libraries
- Reduces disk access

**Examples:**
```bash
load -m                 # Load metaxploit framework
load -c                 # Load crypto library
load -b                 # Load blockchain library
load -t                 # Load traffic network library
```

**See Also:** [libs](#libs), [lms](#lms)

---

### hunt
Network search tool for finding services and computers.

**Usage:** `hunt TYPE [OPTIONS]`

**Types:**
- `custom -p PORT` - Search custom port
- `lib [-n NAME]` - Find libraries
- `repo|rshell|ssh|ftp` - Find specific services
- `special [-n NAME]` - Find special computers
- `employee|student|criminal` - Find person types
- `http|smtp|chat|bank|cam|router|sql` - Find service types
- `neuro|wifi` - Find neurobox/WiFi
- `awifi [-b BSSID] [-e ESSID]` - Search WiFi by BSSID/ESSID
- `file [-n NAME]` - Find files

**Flags:**
- `-k` - Latch watchdog stop when finished
- `-p PORT` - Custom port number
- `-n NAME` - Name filter
- `-s` - Save results to directory
- `-d` - Download library
- `-c COUNT` - Result count (default: 1)
- `-v VERSION` - Version filter
- `-b BSSID` - WiFi BSSID filter
- `-e ESSID` - WiFi ESSID filter

**Features:**
- 21 different hunt types
- Network service discovery
- Resource finding
- WiFi network scanning
- Press 'q' during a hunt to stop early

**Examples:**
```bash
hunt custom -p 8080 -c 5        # Find 5 systems on port 8080
hunt lib -n crypto -d           # Find and download crypto libs
hunt ssh -c 3 -v 1.0            # Find 3 SSH v1.0 services
hunt special -n Bank            # Find banks
hunt employee -s -c 10          # Find 10 employees, save
hunt wifi -c 5                  # Find 5 WiFi networks
hunt awifi -e HomeNetwork       # Find specific WiFi ESSID
```

**See Also:** [scan](#scan), [nmap](#nmap), [wifi](#wifi)

---

### compare
Compare two values or strings.

**Usage:** `compare VALUE1 VALUE2`

**Features:**
- Compare numbers or strings
- Equality checking
- Useful in scripts and conditionals

**Examples:**
```bash
compare 10 10           # Check if equal
compare "abc" "abc"     # String comparison
compare 5 10            # Number comparison
```

---

### decimal
Convert number to decimal format.

**Usage:** `decimal NUMBER`

**Features:**
- Convert to decimal representation
- Number format conversion

**Examples:**
```bash
decimal 0xFF            # Convert hex to decimal
decimal 0b1010          # Convert binary to decimal
```

**See Also:** [binary](#binary), [percent](#percent)

---

### binary
Convert number to binary format.

**Usage:** `binary NUMBER`

**Features:**
- Convert to binary representation
- Number format conversion

**Examples:**
```bash
binary 255              # Convert to binary
binary 128              # Convert to binary
```

**See Also:** [decimal](#decimal), [percent](#percent)

---

### percent
Calculate percentage.

**Usage:** `percent PART TOTAL`

**Features:**
- Calculate percentage values
- Mathematical operations
- Useful for progress indicators

**Examples:**
```bash
percent 25 100          # Calculate 25% of 100
percent 50 200          # Calculate 50% of 200
```

**See Also:** [average](#average), [median](#median)

---

### median
Calculate median of numbers.

**Usage:** `median NUMBER [NUMBER...]`

**Features:**
- Calculate middle value
- Statistical analysis
- Works with multiple values

**Examples:**
```bash
median 1 2 3 4 5        # Median of 5 numbers
median 10 20 30         # Median of 3 numbers
```

**See Also:** [average](#average), [percent](#percent)

---

### sessions
Manage active X sessions.

**Usage:** `sessions [-l|-k]`

**Flags:**
- `-l` - List active sessions
- `-k ID` - Kill session by ID

**Features:**
- View all X instances
- Terminate specific sessions
- Session management

**Examples:**
```bash
sessions -l             # List all sessions
sessions -k 2           # Kill session ID 2
```

---

### service
Manage system services and servers.

**Usage:** `service [-v|-l|-r] [SERVICE -i|start|stop]`

**Services:** rshell, ssh, ftp, http, chat, repo

**Flags:**
- `-v` - View default service info
- `-l` - List all found services
- `-r` - Reload local service list
- `SERVICE -i` - Install service (requires root & repo)
- `SERVICE start|stop` - Control service

**Features:**
- Service installation
- Start/stop control
- Service monitoring
- Requires repository setup for install

**Examples:**
```bash
service -l              # List all services
service ssh -i          # Install SSH service
service ssh start       # Start SSH service
service http stop       # Stop HTTP service
```

**See Also:** [apt](#apt), [lms](#lms), [net](#net)

---

### gmon
Directory change monitor.

**Usage:** `gmon [-p PATH] [--deploy]`

**Flags:**
- `-p PATH` - Specify directory to monitor (default: /home/guest)
- `--deploy` - Launch as background process

**Features:**
- Monitor directory for changes
- File modification tracking
- Background deployment
- Requires root if not deployed

**Examples:**
```bash
gmon                    # Monitor /home/guest
gmon --deploy           # Monitor in background
gmon -p /var            # Monitor /var directory
gmon -p /home --deploy  # Monitor /home in background
```

**See Also:** [htop](#htop)

---

### kiddy
Website defacement tool (sk).

**Usage:** `sk [-f FILE] [-w [-n NAME] [-p PATH]]`

**Flags:**
- `-f FILE` - Deface with custom HTML file
- `-w` - Write default template to disk
- `-n NAME` - Template filename (default: sk)
- `-p PATH` - Template path (default: data folder)

**Features:**
- Website defacement
- Default or custom HTML
- Template generation
- Active computer targeting

**Examples:**
```bash
sk                      # Deface with default page
sk -f /home/tux/custom.html  # Custom HTML
sk -w                   # Write template
sk -w -n mypage -p /var # Write to /var as mypage
```

---

### average
Calculate average of numbers.

**Usage:** `average NUMBER [NUMBER...]`

**Features:**
- Calculate mean value
- Statistical operations
- Multiple number support

**Examples:**
```bash
average 10 20 30        # Average of 3 numbers (20)
average 5 10 15 20 25   # Average of 5 numbers (15)
average 100 200         # Average of 2 numbers (150)
```

**See Also:** [median](#median), [percent](#percent)

---

### check
Verify user assignment.

**Usage:** `check`

**Features:**
- Verify current user assignment
- Fix corrupted permissions
- Automatic reset if discrepancy found

**Examples:**
```bash
check                   # Verify and fix user
```

---

### alias
Command aliasing system.

**Usage:** `alias [-s|-r|-l]`

**Flags:**
- `-s ALIAS COMMAND [PARAMS]` - Set alias
- `-r ALIAS` - Remove alias
- `-l` - List all aliases

**Features:**
- Create command shortcuts
- Persistent across sessions
- Parameter support
- Faster access to frequent commands

**Examples:**
```bash
alias -l                # List all aliases
alias -s ll ls -la      # Create ll alias
alias -s scan nmap -sS  # Create scan alias
alias -r ll             # Remove ll alias
```

---

### index
Display X interface legend.

**Usage:** `index`

**Features:**
- Explain prompt indicators
- Session type colors
- Access level display
- System state indicators

**Prompt Indicators:**
- `[MAIN]` - Local Host Object (blue)
- `[PIVOT[n]]` - Main after pivot (orange)
- `[PROXY[n]]` - Main after proxy (purple)
- `[SHELL]` - Captured Shell Object (green)
- `[COMPUTER]` - Captured Computer Object (yellow)
- `[FILE]` - Captured File Object (red)
- `[P]` - Have Read Access To PASSWD (green/red)
- `[R]` - Have Root Password (green)

**Examples:**
```bash
index                   # View interface legend
```

---

### info
Print cached root password.

**Usage:** `info`

**Features:**
- Display root password from cache
- Must be previously cached
- Quick password retrieval

**Examples:**
```bash
info                    # Print root password
info && echo root:$(info) > creds.txt  # Save to file
scan -l && info         # Exploit then retrieve password
```

**See Also:** [show](#show), [shadow](#shadow), [addpass](#addpass)

---

### show
Display cached credentials and public IP.

**Usage:** `show`

**Features:**
- Display root password and public IP
- Public IP always shown
- Password shown if cached
- Combined information display

**Examples:**
```bash
show                    # Display credentials and IP
scan -l && show         # Exploit then show info
show > target_info.txt  # Save to file
show | grep password    # Extract password only
```

**See Also:** [info](#info), [shadow](#shadow), [addpass](#addpass)

---

### coin
Cryptocurrency wallet manager.

**Usage:** `coin -n COIN_NAME -u USER [-p PASS]`

**Flags:**
- `-n COIN_NAME` - Coin service name
- `-u USER` - Username for authentication
- `-p PASS` - Password (optional, will prompt if omitted)

**Features:**
- Access coin services
- Manage balances and transfers
- Interactive or direct login
- Transaction management

**Examples:**
```bash
coin -n BitForce -u hacker123           # Login with prompt
coin -n CryptoBank -u admin -p secret   # Direct login
coin -n BitMiner -u miner01             # Interactive password
coin -n WalletService -u bot -p $(cat .coinpass)  # From file
```

**See Also:** [web](#web), [bank](#bank)

---

### start
Launch X instances or terminal sessions.

**Usage:** `start x [PATH]|[-t|-s|--terminal]`

**Flags:**
- `x [PATH]` - Launch new X instance at optional PATH
- `-t` - Terminal interface (disabled during pivot)
- `-s` - Remote shell (SSH/FTP connection)
- `--terminal` - Full terminal session (closes X)

**Features:**
- Launch nested X instances (max 17 pivots)
- Terminal-like interfaces
- Remote shell connections
- Multi-hop pivoting support

**Examples:**
```bash
start x                 # Launch X in current dir
start x /root           # Launch X in /root
start -t                # Terminal interface
start -s 98.110.69.115 22 root password ssh  # SSH connection
start --terminal        # Full terminal (exits X)
```

**See Also:** [pivot](#pivot), [pull](#pull), [launch](#launch)

---

### pivot
Copy and launch X framework on target systems.

**Usage:** `pivot [-y]`

**Flags:**
- `pivot` - Minimal pivot (for scanning/basic ops)
- `-y` - Full pivot (complete X framework)

**Features:**
- Copy X to compromised systems
- Minimal or full framework
- Reuses existing X if present
- Maximum 17 self-launches
- Prompted for location

**Examples:**
```bash
scan -p 192.168.1.50 22  # Exploit SSH
pivot                     # Minimal pivot
pivot -y                  # Full pivot with all features
scan -n && scan -p TARGET 22 && pivot  # Multi-hop chain
```

---

### dirty
Dirty router log management.

**Usage:** `dirty [-l|-a|-s|-m|-r|-c|-x]`

**Flags:**
- `-l` - List dirty routers
- `-a` - Add router to dirty buffer
- `-s` - Scrub logs on tracked routers
- `-m` - Manual clean
- `-r` - Reload buffer
- `-c` - Count dirty routers
- `-x` - Clear all entries

**Features:**
- Track routers with uncleared logs
- Automated log scrubbing
- May need multiple runs
- Buffer persistence

**Examples:**
```bash
dirty -l                # List uncleared routers
dirty -c                # Show count
dirty -a                # Add current router
dirty -s                # Scrub logs
dirty -s && dirty -c    # Scrub and check remaining
dirty -x                # Clear buffer
```

**See Also:** [clean](#clean), [scan](#scan)

---

### gzip
File and text compression utility.

**Usage:** `gzip [-c|-u] [-t] [--force] [-f FILE|TEXT] [-r DIR]`

**Flags:**
- `-c` - Compress file/string to base64
- `-u` - Uncompress base64 file/string
- `-t` - Output to console instead of file
- `--force` - Skip .gz extension check (caution)
- `-f FILE|TEXT` - File path or text string
- `-r DIRECTORY` - Recursive directory operation

**Features:**
- Base64 compression
- File and text support
- Recursive directory operations
- Console or file output
- Default requires .gz suffix for uncompress

**Examples:**
```bash
gzip -c -f data.txt     # Compress to data.txt.gz
gzip -c -f "secret message"  # Compress text
gzip -c -r /home/user/docs   # Compress directory
gzip -u -f data.txt.gz  # Uncompress file
gzip -u -f archive.dat --force  # Force without .gz
gzip -c -f data.txt -t  # Compress to console
gzip -c -f logs.txt && rm logs.txt  # Compress and delete
```

**See Also:** [tar](#tar), [zip](#zip)

---

### pingport (pp)
Ping network port repeatedly.

**Usage:** `pp [-w WAIT] [-c COUNT] IP PORT`

**Flags:**
- `-w WAIT` - Seconds between pings (0.01-300, default: 1)
- `-c COUNT` - Number of ping attempts

**Features:**
- Repeated port pinging
- Launch attack when available
- Configurable wait time
- Limited or infinite attempts

**Examples:**
```bash
pp 192.168.1.50 22      # Ping SSH continuously
pp 10.0.0.5 80          # Ping HTTP port
pp -c 10 192.168.1.50 22  # Ping 10 times
pp -w 0.5 192.168.1.50 22  # Ping every 0.5 seconds
pp -w 5 -c 20 10.0.0.5 80  # Every 5s, 20 times
pp -c 60 -w 60 192.168.1.1 80  # Monitor for 1 hour
```

**See Also:** [scan](#scan), [ports](#ports), [nmap](#nmap)

---

### ports
List open ports on system.

**Usage:** `ports`

**Features:**
- Display all open network ports
- Show port numbers
- Associated services
- Current system only

**Examples:**
```bash
ports                   # List all open ports
```

**See Also:** [scan](#scan), [nmap](#nmap), [pp](#pingport)

---

### web
Private HTTP interweb service.

**Usage:** `web`

**Features:**
- Install and launch private HTTP server
- Secure browsing for coin/bank/repo services
- Not port forwarded (local only)
- Requires root privileges
- Auto-closes on terminal exit
- Repository fetch capability only

**Examples:**
```bash
web                     # Start private HTTP server
```

**See Also:** [service](#service), [open](#open), [start](#start)

---

### scan
Comprehensive vulnerability scanner and exploit framework.

**Usage:** `scan [-l|-lp|-n|-r|-d|-nf|-nd|-nfd|-a|-p|-pd|--n|--l|--c] [TARGET]`

**Flags:**
- `-l` - Scan and attack localhost
- `-lp` - Localhost with 0day exploits
- `-n` - Scan local network
- `-r` - Find random network
- `-d` - Disable all firewalls
- `-nf` - Show network firewalls
- `-nd` - Disable network firewalls
- `-nfd` - Show and disable network firewalls
- `-a [-w CRITERIA] [-s START_IP] [-e END_IP]` - Mass IP scan
- `-p IP PORT|LIBRARY` - Attack partial object
- `-pd PATH` - Scan library folder (recommend /lib)
- `--n [-r ROUTER_IP] LIBRARY OBJECT [EXTRA]` - Smart LAN scan
- `--l LIBRARY INDEX [EXTRA]` - Custom local scan
- `--c IP LIBRARY OBJECT [EXTRA]` - Custom public scan
  - `LIBRARY` supports partial names and `find` for auto-selection
  - `OBJECT` accepts short codes and friendly names (`shell`, `computer`, `file`, `lan`, `bounce`, `rootpass`, `userpass`)
  - auto shell selection prefers non-router shells unless `--router` is passed
  - `--router` can be placed anywhere after `--c`

**Port Shortcuts:**
- router:0, ssh:22, ftp:21, http:80, chat:6667
- rshell:1222, repo:1542, cam:37777, sql:3306, smtp:25

**Object Types:**
- s=shell, c=computer, f=file, l=lan bounce
- i=internal lan bounce, d=disable firewall
- p=change root password, w=change user password

**Features:**
- Localhost, LAN, and remote scanning
- Automated exploitation
- Partial object attacks
- Smart library scanning
- Custom exploit index
- Firewall management
- Mass IP scanning

**Examples:**
```bash
scan -l                 # Scan localhost
scan -lp                # Localhost with 0day
scan -n                 # Scan local network
scan target.com         # Attack remote host
scan -r                 # Find random target
scan -p target.host 0   # Attack router port
scan -p target.host 22  # Attack SSH
scan -p /lib/init.so    # Attack with library
scan --n http s         # Find shell via HTTP on LAN
scan --l apt 6 router.local  # Custom local exploit
scan --c target.host router l gateway.local  # Remote LAN bounce
scan --c target.host find s  # Auto-find and execute best shell exploit
scan --c target.host find shell  # Same as above with friendly object name
scan --c target.host find shell --router  # Require router shell only (port 0)
scan --c --router target.host find shell  # Same, flag-first ordering
scan -nf                # Show network firewalls
scan -a -w Neurobox -s 1.196.1.169 -e 1.196.255.169  # Mass scan
scan -pd /lib           # Index library exploits
```

**See Also:** [open](#open), [exploits](#exploits), [system](#system)

---

## Additional Commands from Man3

### system (sys)
System management framework.

**Usage:** `sys -e | -z | -t [PATH] | restore [OPTIONS] | -c | -s | list OPTIONS | -r | -l | -b | -d | -ld | -a`

**Options:**
- `-e` - Encrypt filesystem (default target: root /)
- `-z` - Decrypt filesystem (default target: root /)
- `-t [PATH]` - Brick system or directory (**WARNING: DESTRUCTIVE**)
- `restore --all|--boot|--system|--perms|--etc` - Restore system components
- `-c` - Soft secure system (chmod root and delete passwd)
- `-s` - Hard secure system (enhanced soft secure, **WARNING: DO NOT RUN IF /home MODIFIED**)
- `list -n -c` - Check name file duplicates
- `list -n -x` - Clear master name list
- `list -n -l` - Load master name list
- `list -p -c` - Check password duplicates
- `list -p -x` - Clear master password list
- `list -p -l` - Load master password list
- `-r` - Resecure hard-secured system
- `-l` - Create x system link in /bin
- `-b` - Remove all /bin files
- `-d` - Manage database server
- `-ld` - Manage library database
- `-a` - Audit /bin binaries

**Features:**
- Comprehensive system management
- Filesystem encryption and decryption
- Security hardening modes (soft and hard)
- Master name and password list management
- System restoration capabilities
- Database administration
- Binary auditing and management

**Examples:**
```bash
sys -e                  # Encrypt root filesystem
sys -z                  # Decrypt root filesystem
sys -c                  # Soft secure system
sys -s                  # Hard secure system
sys restore --all       # Restore everything
sys list -n -l          # Load master name list
sys -d                  # Manage database
sys -a                  # Audit /bin binaries
```

**See Also:** [secure](#secure), [restore](#restore), [encrypt](#encrypt)

---

### exploits (exp)
Exploit database management.

**Usage:** `exp -l | -d | -f OPTIONS CRITERIA | -p INDEX [EXPLOIT_INDEX] | -r OPTIONS | -x | grind OPTIONS | defrag | SERVICE [-p PASSES] | reset | view -l LIB -v VER | refresh | bloom OPTIONS | backup | restore [SNAPSHOT]`

**Search Options:**
- `-f -n CRITERIA` - Search by name (use operators: =:name)
- `-f -v CRITERIA` - Search by version (use operators: >:1.0.3)
- `-f -e CRITERIA` - Search by exploit type (shell, computer, file, lan)
- `-f -m CRITERIA` - Search by memory address
- `-f -s CRITERIA` - Search by string tree value
- `-f -u CRITERIA` - Search by user level (root, user, guest)
- `-f -r CRITERIA` - Search by requirement tree

**Database Operations:**
- `-l` - List all exploits
- `-d` - Dump libraries to file (saves as 'libs')
- `-p INDEX` - View all exploits at library INDEX
- `-p INDEX EXPLOIT_INDEX` - View specific exploit
- `-r -i INDEX | -l LIBRARY -v VERSION` - Remove exploit
- `-x` - Remove ALL exploits
- `defrag` - Remove orphaned indexes
- `refresh` - Refresh exploit cache

**Grinding:**
- `grind -l LIBRARY MEMORY UNSECURED (EXTRA)` - Grind local library
- `grind -r IP LIBRARY MEMORY UNSECURED (EXTRA)` - Grind remote library

**Updates:**
- `router [-p PASSES]` - Update router exploits (default: 100 passes)
- `http|ssh|ftp|smtp|rshell|repo|sql [-p PASSES]` - Update service exploits (default: 10)
- `all [-p PASSES]` - Update all exploits

**Bloom Filter:**
- `bloom -s` - Show bloom filter statistics
- `bloom -a` - Analyze bloom filter distribution
- `bloom reset` - Reset bloom filter to zeros
- `bloom rebuild` - Rebuild bloom filter from cache

**Backup/Restore:**
- `backup` - Backup exploit database (creates snapshot: payload/snapshot/day_month_year_N)
- `restore [SNAPSHOT]` - Restore from snapshot (shows menu if no snapshot specified)

**Features:**
- Comprehensive exploit database management
- Powerful search with operators
- Custom exploit grinding
- Service-specific updates
- Bloom filter optimization
- Backup and restore functionality

**Examples:**
```bash
exp -l                          # List all exploits
exp -f -v >:1.0.3              # Find versions greater than 1.0.3
exp -f -u =:root -e =:shell    # Root shell exploits
exp -p 7 2                      # View exploit [2] from library [7]
exp grind -l init 0x2BB8CD82 seltaddparent
exp router                      # Update router exploits
exp ssh -p 20                   # 20 SSH update passes
exp bloom -s                    # Show filter stats
exp backup                      # Create snapshot
exp restore 27_Jan_2000_1      # Restore specific snapshot
```

**See Also:** [scan](#scan), [metaxploit](#metaxploit), [deepscan](#deepscan)

---

### passwords (pass)
Password generator and database manager.

**Usage:** `pass | pass OPTIONS [LENGTH] [COUNT] | pass OPTIONS -R MIN MAX [COUNT]`

**Options:**
- `pass` - View and edit password database
- `OPTIONS [LENGTH] [COUNT]` - Generate fixed-length password list
- `OPTIONS -R MIN MAX [COUNT]` - Generate random-length passwords

**Option Flags (combine multiple):**
- `u` - Include uppercase letters (A-Z)
- `l` - Include lowercase letters (a-z)
- `n` - Include numbers (0-9)
- `s` - Include special characters
- `c` - Capitalize first character (cannot combine with u)

**Features:**
- Advanced password testing tool
- Custom password list generation
- Configurable character sets
- Fixed or random length support
- Database management interface

**Examples:**
```bash
pass                        # Open password database
pass ln 8 100               # 100 8-char lowercase+number passwords
pass uln 10 500             # 500 10-char mixed-case alphanumeric
pass ulns 12 200            # 200 12-char with special chars
pass uln -R 8 16 1000       # 1000 passwords, 8-16 chars each
pass cln 8 100              # Capitalized first letter
pass n 4 1000               # 1000 4-digit PIN codes
```

**See Also:** [brute](#brute), [dict](#dict), [rainbow](#rainbow)

---

### get
Get bank accounts, email accounts, map/proxy accounts, and more.

**Usage:** `get -p | -z [-c] | -i | -w | -n [OPTIONS] | -m [OPTIONS] | -b [OPTIONS] | -e [OPTIONS]`

**Options:**
- `-p` - Download the passwd file
- `-z` - Determine best letter combination for smallest file compile size (add `-c` to keep searching past the first match; press 'q' to stop)
- `-i` - View local network status
- `-w` - Show wifi information
- `-n [-c [QUANTITY] -s -n [SAVENAME]]` - Get random names (for <=19k should be safe)
- `-m [-c [QUANTITY] -d -s -n [SAVENAME]]` - Get map/proxy accounts
- `-b [-c [QUANTITY] -d -s -n [SAVENAME]]` - Get bank accounts
- `-e [-c [QUANTITY] -d -s -n [SAVENAME]]` - Get email accounts

**Account Flags:**
- `-c [QUANTITY]` - Specify number of accounts (fuzzy meaning targets QUANTITY systems)
- `-d` - Use decipher method (default: dictionary attack)
- `-s` - Use shells
- `-n [SAVENAME]` - Save results to file

**Features:**
- Multi-account harvesting
- Dictionary or decipher methods
- Configurable quantities
- Network and WiFi info viewing
- Random name generation

**Examples:**
```bash
get -p                          # Download passwd file
get -i                          # View network status
get -w                          # Show WiFi info
get -n -c 100                   # Get 100 random names
get -m -c 5 -d                  # Get 5 map accounts with decipher
get -b -c 10 -s                 # Get 10 bank accounts using shells
get -e -c 20 -n emails.txt      # Get 20 email accounts, save to file
```

**See Also:** [scan](#scan), [hunt](#hunt), [jack](#jack)

---

### rshell
X's rshell framework for reverse shell management.

**Usage:** `rshell -s [IP [PORT] [NAME]] | import | -b | -i | -bi | -d|-da|-dc|-dca OPTIONS | -p|-pa|-pc|-pca OPTIONS | dump [PATH] | -z OPTIONS | -e|-ea COMMAND | -l | -u INDEX | -c OPTIONS | logs | list | refresh | -k INDEX | -x [PNAME] | -h [OPTIONS]`

**Server Management:**
- `-s [IP] [PORT] [NAME]` - Start temporary rshell with optional server IP, port, and name
- `import` - Import a rshell server
- `-b` - Build a rshell
- `-i` - Install already built rshell and launch
- `-bi` - Build and install rshell

**File Operations:**
- `-d INDEX TFILE_PATH DPATH` - Download file from rshell by ID
- `-da TFILE_PATH DPATH` - Download from all rshells
- `-dc INDEX TFILE_PATH DPATH` - Download to active object
- `-dca TFILE_PATH DPATH` - Download from all to active object
- `-p INDEX TFILE_PATH UPATH` - Upload file to rshell by ID
- `-pa TFILE_PATH UPATH` - Upload to all rshells
- `-pc INDEX TFILE_PATH UPATH` - Upload to active object
- `-pca TFILE_PATH UPATH` - Upload to all from active object
- `dump [PATH]` - Dump rshell server list to file

**Command Execution:**
- `-z -e INDEX,INDEX,... COMMAND [PARAMS]` - Execute on multiple rshells
- `-z -k INDEX,INDEX,...` - Kill multiple rshells
- `-e INDEX COMMAND [PARAMS]` - Execute on rshell by ID (NOT available with rshell lite)
- `-ea COMMAND [PARAMS]` - Execute across all rshells (NOT available with rshell lite)

**Management:**
- `-l` - List captured rshells
- `-u INDEX` - Open shell from selected rshell ID
- `-c -a|-h|-r|-s` - Clear caches (all/history/rshells/server)
- `logs` - Download all system.log files from rshells
- `list` - List all imported rshell servers
- `refresh` - Check for new rshells
- `-k INDEX [PNAME]` - Kill captured rshell by ID
- `-x [PNAME]` - Kill all captured rshells
- `-h -l` - List rshells from history
- `-h -u INDEX` - Open shell from history
- `-h -c` - Clear history cache

**Features:**
- Full rshell lifecycle management
- Batch file operations
- Multi-rshell command execution
- History tracking
- Server import/export

**Examples:**
```bash
rshell -s                       # Start temporary rshell
rshell -bi                      # Build and install
rshell -l                       # List captured rshells
rshell -d 0 /etc/passwd ./loot  # Download passwd from first rshell
rshell -p 1 exploit.src /var    # Upload exploit to second rshell
rshell -z -e 1,2,3 ps          # Execute ps on rshells 1,2,3
rshell -ea ls -la              # Execute ls on all rshells
rshell -k 0                     # Kill first rshell
rshell refresh                  # Check for new connections
```

**See Also:** [rat](#rat), [ssh](#ssh), [netcat](#netcat)

---

### make
Binary build and infection framework.

**Usage:** `make -t [-y] (-f) (-c [-b]|[-e]) (-p [PASSWORD]) (-s [START]) BINARY | -rec | -r | -cs | -pm | -pp | -pc | -i BINARY V|R|T|C | -l | -v BINARY | -a [-y] | -b [OPTIONS] BINARY | -p BINARY`

**Standalone Tools:**
- `-t BINARY` - Make standalone tool (use -y to keep in current dir)
- `-rec` - System recovery binary
- `-r` - Generic rshell binary
- `-cs` - Custom server frontend
- `-pm` - Proxy from Map.conf
- `-pp` - Proxy from proxy.dat
- `-pc` - Proxy custom input

**Binary Infection:**
- `-i BINARY V` - Inject virus
- `-i BINARY R` - Inject rshell
- `-i BINARY T` - Inject RAT (requires /root/rat file on C2 server)
- `-i BINARY C` - Inject custom payload

**Build Operations:**
- `-l` - List buildable binaries
- `-v BINARY` - View binary source
- `-a (-y)` - Build all default binaries (use -y to place in /bin)
- `-b BINARY` - Build single binary
- `-b S BINARY` - View source
- `-b T BINARY` - Build with RAT
- `-b V BINARY` - Build with virus
- `-b R BINARY` - Build with rshell
- `-b P BINARY` - Build with password
- `-b E BINARY` - Build encrypt filesystem
- `-b D BINARY` - Build decrypt filesystem
- `-b C BINARY` - Build with custom payload
- `-b F BINARY` - Build from file content
- `-p BINARY` - View source code

**Features:**
- Complete binary building framework
- Malware injection capabilities
- Standalone tool creation
- Proxy binary generation
- Password protection support
- Custom payload integration

**Examples:**
```bash
make -l                         # List all binaries
make -b ls                      # Build ls binary
make -a                         # Build all defaults
make -t lock                    # Create lock tool
make -i /bin/cat V              # Inject virus into cat
make -b V ls                    # Build ls with virus
make -pm                        # Proxy from Map.conf
make -rec                       # System recovery binary
```

**See Also:** [build](#build), [compile](#compile), [sys](#sys)

---

### mc
Interactive file explorer and manager.

**Usage:** `mc [-d] (path1) (path2)`

**Options:**
- `-d` - Start in dual panel mode
- `path1` - Starting directory for left panel (optional)
- `path2` - Right panel directory for dual mode (optional)

**Display Features:**
- Directory Size - Shows total size of files
- File Counts - Number of files and folders
- Permissions - Toggle between symbolic and octal
- Symlinks - Show or hide symbolic link targets
- Hidden Files - Toggle files starting with '.'

**Sorting:**
- Sort By Name - Alphabetical (default)
- Sort By Size - File size sorting
- Sort By Date - Modification date sorting
- Reverse Order - Reverse current sort
- Un-Sort - Disable sorting

**File Operations:**
- Rename File - Rename files and directories
- New File - Create new files
- New Directory - Create new directories
- Delete Files - Delete files and directories
- Change Permissions - Set permissions (supports octal)

**Navigation:**
- cd... - Change to any directory
- Quick Nav - Jump to /, home, or other panel
- Filter - Filter current directory by name
- Search for File - Recursively search and navigate

**Dual Panel Features:**
- Copy Files - Copy between panels with progress
- Move Files - Move between panels with progress
- Switch Panel - Toggle between left and right
- Single Panel - Return to single panel mode
- [X] indicates active panel

**Features:**
- Full-featured file manager
- Dual panel support
- Advanced sorting and filtering
- Permission management (octal/symbolic)
- File operations with progress
- Hidden file support

**Examples:**
```bash
mc                              # Open in current directory
mc /home                        # Open /home directory
mc -d                           # Open dual panel mode
mc -d /home/user /var           # Dual panel with paths
```

**See Also:** [ls](#ls), [cd](#cd), [chmod](#chmod)

---

### cache
Remote system attack cache management.

**Usage:** `cache -l | -u NICKNAME|INDEX | -e NICKNAME|INDEX | -y | -n | -v | -d | -r NICKNAME|INDEX | -x | --u OPTIONS INDEX`

**Options:**
- `-l` - List captured systems
- `-u NICKNAME|INDEX` - Use cached system
- `-e NICKNAME|INDEX` - Edit cached entry
- `-y` - Reload cache from disk
- `-n` - Add new entry
- `-v` - Load external cache file
- `-d` - Dump cache to file (cache.dat)
- `-r NICKNAME|INDEX` - Remove cached system
- `-x` - Clear entire cache

**Remote Operations:**
- `--u -a INDEX` - Attack cached system
- `--u -t INDEX [PORT] [SERVICE]` - Start terminal connection
- `--u -s INDEX [PORT] [SERVICE]` - Open shell connection
- `--u -u INDEX [PORT] [SERVICE]` - Upload to cached system

**Features:**
- Persistent access to compromised systems
- SSH and FTP backdoor storage
- Populated by 'jack' command
- Terminal, shell, and upload operations
- Default connection: SSH port 22

**Examples:**
```bash
cache -l                        # List all cached systems
cache -n                        # Add new cache entry
cache -u 0                      # Use first cached system
cache -u rshell                 # Use system by nickname
cache --u -s 0                  # Open shell on first system
cache --u -t 1 21 ftp          # FTP terminal on port 21
cache -d                        # Export cache to file
cache -x                        # Clear all cached systems
```

**See Also:** [jack](#jack), [recon](#recon), [rshell](#rshell)

---

### iwlist
View local WiFi networks.

**Usage:** `iwlist`

**Features:**
- Scan all WiFi networks in range
- Display ESSID, BSSID details
- Show signal strength
- Encryption type information
- Channel information
- Local wireless adapter scanning

**Examples:**
```bash
iwlist                          # Display all WiFi networks
iwlist                          # Check encryption types
iwlist                          # Find weak security networks
```

**See Also:** [wifi](#wifi), [hunt](#hunt), [scan](#scan)

---

### hide
Hide or modify root file system visibility.

**Usage:** `hide -s (-c [CHAR]) (-n [NUMBER]) | -f FILE | -t`

**Options:**
- `-s (-c [CHAR]) (-n [NUMBER])` - Hide/unhide root file system directories
  - `-c` - Specify custom character display
  - `-n` - Number of character repetitions
- `-f FILE` - Hide or unhide individual file (toggles visibility)
- `-t` - Hide or unhide .Trash folder (toggles)

**Features:**
- Manipulate root file system visibility
- Custom character display patterns
- Individual file hiding
- Trash folder visibility control
- Obfuscation for concealment

**Examples:**
```bash
hide -s                         # Show: ./bin, ./boot, ./etc...
hide -s -n 10 -c _             # Show: __________/bin...
hide -s -n 10 -c .-            # Show: .-.-.-.-.-.-.-.-.-.-/bin...
hide -f /root/exploit.src      # Hide exploit script
hide -t                         # Toggle .Trash visibility
hide -s -n 5 -c XX             # Create XXXXXXXXXX pattern
```

**See Also:** [wipe](#wipe), [rm](#rm), [ls](#ls)

---

### wipe
System file corruption and log clearing.

**Usage:** `wipe -x | -c | -m | -lx | -lc | -lt | -l | -b [-y] | -s [-y] | -t | -a | --deploy [SECONDS]`

**Options:**
- `-x` - Wipe x framework traces
- `-c` - Wipe x config files
- `-m` - Wipe proxy chain logs (Map.conf)
- `-lx` - Wipe local log with X graphic
- `-lc` - Wipe log with custom ASCII (from /payload/data/ascii)
- `-lt` - Wipe log with custom text
- `-l` - Wipe local log file (standard)
- `-b (-y)` - Wipe boot system, clear system.log if possible (optional -y for auto-confirm)
- `-s (-y)` - Wipe entire file system (**DESTRUCTIVE**, optional -y for auto-confirm)
- `-t` - Wipe user Trash folder
- `-a` - Wipe bank transaction log
- `--deploy [.01-300 SECONDS]` - Deploy delayed log wiper

**Features:**
- System wiping tool
- Log clearing (with custom ASCII)
- Boot folder removal
- File system corruption
- X framework trace removal
- Delayed log wiper deployment

**Examples:**
```bash
wipe -l                         # Standard log wipe
wipe -lx                        # Wipe with X graphic
wipe -lc                        # Custom ASCII art
wipe -x                         # Remove x traces
wipe -b                         # Remove boot folder
wipe -b -y                      # Auto-confirm boot wipe
wipe --deploy 5                 # 5 second delayed wipe
```

**See Also:** [clean](#clean), [rm](#rm), [logwatcher](#logwatcher)

---

### run
Advanced bash script interpreter with full programming features.

**Usage:** `@script | run script|path | run -e [NAME] | run --list | run -n [NAME] | run -o | run --FILE FILE SCRIPT | run --DEBUG script | run --ALLOWABS script`

**Control Flow:**
- `if/elif/else/endif` - Conditional branching with operators (==, !=, <, >, <=, >=, and, or, not)
- `switch/case/default/endswitch` - Pattern matching
- `while/endwhile` - Condition-based loops
- `until/enduntil` - Loop until condition true
- `for/endfor` - Iteration over lists, ranges, or variables
- `break` - Exit loop
- `continue` - Skip to next iteration

**Functions:**
- `func name(param1,param2) / endfunc` - Define functions with parameters
- `return_value expression` - Return value with arithmetic
- `return` - Exit script/function (optionally execute command first)
- Recursion depth: 10 levels with true local scope

**Variables & Arithmetic:**
- `_setvar(name,value)` - Set variable (strings, numbers, lists)
- `_getvar(name)` - Retrieve variable (auto-substituted)
- Operators: +, -, *, /, %, ** (power)
- List literals: `_setvar(items,[apple,banana,cherry])`

**Array Operations:**
- `_push list value` - Add to end
- `_pop list` - Remove from end
- `_pull list` - Remove from start
- `_len name` - Get length
- `_in list value` - Check existence

**Built-in Functions:**
- String: len(), upper(), lower(), substr(), concat(), contains(), replace()
- Math: floor(), ceil(), abs(), round(), min(), max(), random(), timestamp(), date()
- Array: join(list,delim), split_str(), trim_str()
- File: file_exists(), is_folder(), is_binary(), file_read()
- Permissions: get_permissions(), _fs_canwrite(), _fs_canexec()
- Context: get_user(), get_home(), get_shell_type(), get_computer_lan_ip(), get_computer_public_ip(), get_root()
- Type: typeof_val(), get_type(val)
- Layer: get_layer()
- Boolean: to_yesno(), to_truefalse()

**Typed Input Prompts:**
- `get_string` - Prompt for string
- `get_integer` - Prompt for integer
- `get_decimal` - Prompt for decimal
- `get_any` - Prompt for any value (unlimited use)
- `get_yesno` - Prompt for yes/no (returns 1 or 0)

**Other Commands:**
- `_print` - Print with variable substitution and color
- `_fs_read` - Read file content
- `_fs_view` - Display file content
- `_fs_write` - Write content to file
- `_fs_find` - Search for files
- `_fs_put` - Upload file (shell only)
- `_fs_get` - Download file (shell only)
- `_home` - Safe bash-script-friendly alternative to home
- `_sys_whoami` - Get current username
- `_sys_whatami` - Get execution context type
- `_fs_pwd` - Print working directory

**Network Reconnaissance:**
- `_net_ports` - Scan router for ports
- `_net_router` - Display router info
- `_net_devices` - List LAN devices
- `_net_devports` - Show device ports
- `_net_fwrules` - Display firewall rules
- `_net_random` - Generate random public IP

**Script Management:**
- `run script` - Run script from bash folder
- `@script` - Shorthand invocation
- `run -e [NAME]` - Edit script
- `run --list` - List all scripts
- `run -n [NAME]` - Create new script
- `run -o` - Open bash folder
- `run --FILE FILE SCRIPT` - Execute with file parameters
- `run --DEBUG script` - Enable debug mode
- `run --ALLOWABS script` - Allow absolute paths

**Flags:**
- `--DEBUG` - Show execution details
- `--SIGBREAK` - Break on warnings
- `--SIGCONT` - Continue after errors
- `--ALLOWABS` - Allow absolute paths
- `--ONERROR cmd` - Execute command on error

**Features:**
- Full programming language
- 10-level recursion
- Typed input prompts
- 20+ built-in functions
- Network reconnaissance
- Context-aware execution
- Script parameters ($1, $2, etc.)

**Examples:**
```bash
run myscript.src                # Run script
@myscript                       # Shorthand
run script.src 192.168.1.1      # With parameters
run -e myscript.src             # Edit script
run --list                      # List all scripts
run --DEBUG script.src          # Debug mode

# Conditional
if _getvar(age) >= 18
  _print Access granted
else
  _print Access denied
endif

# Loop
for ip in [192.168.1.1,192.168.1.2]
  _print Scanning _getvar(ip)
  scan --c _getvar(ip) router
endfor

# Function
func calculate(a,b)
  return_value _getvar(a)*_getvar(b)
endfunc
_setvar(answer,calculate(6,7))
```

**See Also:** [bash](#bash), [script](#script), [automation](#automation)

---

### favs
Manage favorite and trusted IP addresses.

**Usage:** `favs | favs -i IP NICKNAME | favs -r INDEX | favs -e`

**Options:**
- `favs` - List all favorite and trusted IPs
- `-i IP NICKNAME` - Add new favorite or trusted IP with nickname
- `-r INDEX` - Remove favorite by index number
- `-e` - Edit existing favorites

**Features:**
- Favorite IP management
- Trusted system list
- Quick access for automated operations
- RShell server integration (nickname 'rshell')
- Passwordless X launch on trusted IPs

**Examples:**
```bash
favs                            # View all saved IPs
favs -i 222.222.222.222 rshell # Add rshell server
favs -i 198.51.100.42 homebase # Add home server
favs -r 0                       # Remove first entry
favs -e                         # Interactive edit mode
rshell -s                       # Auto-connects to rshell favorite
```

**See Also:** [rshell](#rshell), [cache](#cache), [shadow](#shadow)

---

### shadow
Root password cache system.

**Usage:** `shadow -a [IP] ([PASSWORD]) | -l | -r [FILE] | -w [-d] | -x [-q]`

**Options:**
- `-a [IP] ([PASSWORD])` - Add new IP and password to cache
- `-l` - List all cached shadow passwords
- `-r [FILE]` - Read shadow file into cache (supports encrypted/plaintext)
- `-w [-d]` - Write cache to shadow file (use -d for decrypted plaintext)
- `-x [-q]` - Clear all shadow passwords (use -q for quiet mode)

**File Format:**
```
ip:password
ip:password
...
```

**Features:**
- Cache IP/root password combinations
- Speed up r00ted system logins
- Auto-populated by dict -l and dict lp
- [R] status indicator when password cached
- Encrypted or plaintext storage
- NOT compatible with file objects (-w flag)

**Examples:**
```bash
shadow -a                       # Add with prompts
shadow -a target.host r00tpass123
shadow -l                       # List all cached passwords
shadow -r /home/user/backup.shadow
shadow -w                       # Export encrypted
shadow -w -d                    # Export decrypted plaintext
shadow -x                       # Clear cache with confirmation
dict -l                         # Dictionary attack populates shadow
```

**See Also:** [dict](#dict), [brute](#brute), [rainbow](#rainbow)

---

### anon
Toggle streaming mode on or off.

**Usage:** `anon`

**Features:**
- Only hides passwords
- Use streaming mode for more comprehensive hiding

**Examples:**
```bash
anon                            # Toggle streaming mode
```

**See Also:** [privacy](#privacy), [security](#security)

---

### rainbow
Rainbow table password management.

**Usage:** `rainbow -l | -r | -n | -q | -m OPTIONS [LENGTH] QUANTITY | -k ORDER COUNT | -x`

**Options:**
- `-l` - Load rainbow tables into memory (auto-loads)
- `-r` - Rebuild rainbow tables from lists
- `-n` - Initialize tables from lists (prompts for location)
- `-q` - Quick add temporary files (cleared on restart)
- `-m OPTIONS [LENGTH] QUANTITY` - Generate passwords in memory (temporary)
- `-k ORDER COUNT [-s]` - Markov chain generation from existing lists (ORDER=1-3, COUNT=quantity, -s saves to list dir)
- `-x` - Clear all rainbow tables

**Generation Options (-m):**
- `u` - Include uppercase letters
- `l` - Include lowercase letters
- `n` - Include numbers
- `s` - Include special characters
- `R` - Use random lengths

**Markov Chain (-k):**
- Trains on existing password lists to learn character transition patterns
- ORDER controls ngram depth: 1=more variety, 2=balanced, 3=most realistic
- Generates statistically similar passwords that aren't in the original lists
- Higher order requires larger training sets to be effective

**Features:**
- Rainbow table management
- Precomputed password databases
- Hash cracking acceleration
- In-memory password generation
- Markov chain pattern-based generation
- All files must start with 'list' prefix

**Examples:**
```bash
rainbow -n                      # Create tables from lists
rainbow -r                      # Rebuild from modified lists
rainbow -m ulnR 15 100000       # Generate 100k passwords
rainbow -m uln 8 50000          # Generate 50k 8-char passwords
rainbow -k 2 50000              # Markov chain: 50k order-2 passwords
rainbow -k 3 25000              # Markov chain: 25k order-3 (most realistic)
rainbow -k 2 50000 -s           # Markov + save to lists (then rainbow -n)
rainbow -q                      # Add temporary password files
rainbow -x                      # Clear all tables
```

**See Also:** [addpass](#addpass), [hashcat](#hashcat), [decipher](#decipher)

---

### set
File and system modification utilities.

**Usage:** `set -a | -n [MESSAGE] | -b OPTIONS | -l | -t [USER] [PASSWORD] | -u | -e | -f [PASSWORD] | -z | -s | -x | -o|-g|-c OPTIONS | -i | -p | -q | -rn [PATH] [LENGTH]`

**Options:**
- `-a` - Unlock all files
- `-n ([MESSAGE])` - Leave note in directory
- `-b -d ([COUNT]) ([LENGTH]) ([PATH])` - File bomb with defaults
- `-b -n ([NAME]) ([COUNT]) ([LENGTH]) ([PATH])` - File bomb custom name
- `-b -m ([MESSAGE]) ([COUNT]) ([LENGTH]) ([PATH])` - File bomb custom message
- `-l` - Toggle system logging
- `-t ([USER]) ([PASSWORD])` - Create ghost account (default: tux / h4ck)
- `-u` - Edit users
- `-e` - Email user settings
- `-f ([PASSWORD])` - Password-protected archive
- `-z` - Zip archive from text
- `-s` - Scriptkiddy website (create website.html)
- `-x` - Hard lock system (**WARNING: DESTRUCTIVE - DO NOT RUN ON HOME SYSTEM**)
- `-o -f` - Change file owner
- `-o -d` - Change directory owner
- `-g -f` - Change file group
- `-g -d` - Change directory group
- `-c -f` - Change file permissions (chmod)
- `-c -d` - Change directory permissions
- `-i` - Set different LAN IP
- `-p` - Chmod payload directory (guest access)
- `-q` - Create apt sources.txt (set to default)
- `-rn ([PATH]) ([LENGTH])` - Rename all files randomly (default: current dir, length 20)

**Features:**
- Comprehensive file modification toolkit
- File bombing capabilities
- Ghost account creation
- Permission management
- Archive creation
- System locking (destructive)

**Examples:**
```bash
set -a                          # Unlock all files
set -n                          # Leave default note
set -n "Hacked by x"           # Custom note message
set -b -d 100 30 /var          # 100 files, 30 char names
set -t                          # Create tux ghost account
set -t admin p4ssw0rd          # Custom ghost account
set -o -f                       # Change file owner
set -l                          # Toggle logging
set -rn /var 25                # Randomize filenames
```

**See Also:** [chmod](#chmod), [chown](#chown), [sys](#sys)

---

### clear (clr, cls)
Clear the screen of all characters.

**Usage:** `clear`

**Aliases:** clr, cls

**Examples:**
```bash
clear                           # Clear screen
clr                             # Alias
cls                             # Alias
```

**See Also:** [terminal](#terminal)

---

### bit
Bitwise operation.

**Usage:** `bit & NUMBER NUMBER | bit | NUMBER NUMBER | bit ^ NUMBER NUMBER | bit << NUMBER NUMBER | bit >> NUMBER NUMBER | bit >>> NUMBER NUMBER`

**Options:**
- `bit & NUMBER NUMBER` - Bitwise AND
- `bit | NUMBER NUMBER` - Bitwise OR
- `bit ^ NUMBER NUMBER` - Bitwise XOR
- `bit << NUMBER NUMBER` - Left Shift
- `bit >> NUMBER NUMBER` - Right Shift
- `bit >>> NUMBER NUMBER` - Unsigned Right Shift

**Examples:**
```bash
bit & 12 10                     # AND: 8
bit | 12 10                     # OR: 14
bit ^ 12 10                     # XOR: 6
bit << 5 2                      # Left shift: 20
bit >> 20 2                     # Right shift: 5
```

**See Also:** [bc](#bc), [math](#math)

---

### list
System information and vulnerability scanner.

**Usage:** `list -l [PATH] | -h [-d] [-b] | -x | -t | -p | -z | -m | -n | -i | -c | -f | -d | -a | -s [OPTIONS]`

**Options:**
- `-l ([PATH])` - List library versions (default: /lib)
- `-h` - Scan for special files (pdf, txt, jpg, log, chat, exe)
- `-h (-d)` - Detailed file information
- `-h (-b)` - Include /bin in search
- `-x` - Scan for special files (same as -h)
- `-t` - Print text files
- `-p` - Print passwd file
- `-z` - Print hidden files
- `-m` - View Map.conf
- `-n` - List local networks
- `-i` - View all text file contents
- `-c` - View Config folders
- `-f` - Scan for vulnerable files
- `-d` - Scan for vulnerable directories
- `-a` - List all directories and files
- `-s` - List accounts and hashes
- `-s -b (-B | -D)` - List Bank accounts (with dictionary or decipher)
- `-s -p (-B | -D)` - List passwd accounts (with dictionary or decipher)
- `-s -e (-B | -D)` - List Mail accounts (with dictionary or decipher)

**Features:**
- Comprehensive system info gathering
- Vulnerability scanning
- File and directory discovery
- Account enumeration
- Network topology viewing
- Integrated cracking (dictionary or decipher)

**Examples:**
```bash
list -h                         # Scan for special files
list -h -d                      # Detailed file info
list -p                         # View passwd file
list -m                         # View Map.conf
list -f                         # Scan vulnerable files
list -s                         # List all accounts
list -spD                       # Decipher passwd accounts
list -s -b -B                   # Dictionary bank accounts
```

**See Also:** [recon](#recon), [deepscan](#deepscan), [ls](#ls)

---

### brute
Brute force password cracking.

**Usage:** `brute -l (-u [USER]) | -i | -c COIN [USER] | -e [USER] | -s IP [PORT] | -f IP [PORT]`

**Options:**
- `-l` - Local brute force attack (optional -u for specific user)
- `-i` - Insert cracked root password to cache
- `-c COIN [USER]` - Cryptocurrency wallet attack
- `-e [USER]` - Email account attack
- `-s IP [PORT]` - SSH brute force
- `-f IP [PORT]` - FTP brute force

**Features:**
- Exhaustive password trying
- Local and remote attacks
- Email and cryptocurrency support
- SSH and FTP service targeting
- More thorough but slower than dictionary

**Examples:**
```bash
brute -l                        # Brute all local users
brute -l -u root                # Target specific user
brute -i                        # Crack and cache root password
brute -c btc admin              # Crack Bitcoin wallet
brute -e user@mail.com         # Crack email account
brute -s 203.0.113.50 22       # SSH brute force
brute -f 198.51.100.10 21      # FTP brute force
```

**See Also:** [dict](#dict), [hashcat](#hashcat), [decipher](#decipher)

---

### dict
Dictionary attack password cracking.

**Usage:** `dict -l (-u [USER]) | -lp | -i | -e [OPTIONS] [USER] | -e -u [USER] --file | -c [OPTIONS] COIN [USER] | -s [OPTIONS] IP [PORT] | -f [OPTIONS] IP [PORT]`

**Options:**
- `-l` - Local dictionary attack (optional -u for specific user)
- `-lp` - Print cracked root password
- `-i` - Insert root password to cache
- `-e [USER]` - Email account attack (use --start/--stop for partial dictionary)
- `-e -u [USER] --file` - Email attack from file
- `-c COIN [USER]` - Cryptocurrency wallet attack
- `-s IP [PORT]` - SSH dictionary attack (optional -u for specific user)
- `-f IP [PORT]` - FTP dictionary attack

**Partial Dictionary:**
- `--start [INDEX]` - Start from dictionary index
- `--stop [INDEX]` - Stop at dictionary index

**Features:**
- Rainbow table-based cracking
- Faster than brute force
- Partial dictionary ranges
- Email, crypto, SSH, FTP support
- Shadow cache population

**Examples:**
```bash
dict -l                         # Dictionary all users
dict -l -u admin                # Target specific user
dict -lp                        # Print root password
dict -i                         # Cache root password
dict -e --start 0 --stop 1000 user@mail.com
dict -s 203.0.113.50 22        # SSH dictionary attack
dict -s -u root 198.51.100.10 22
dict -f 203.0.113.75 21        # FTP dictionary attack
```

**See Also:** [brute](#brute), [hashcat](#hashcat), [rainbow](#rainbow)

---

### hostname
Display the host name.

**Usage:** `hostname`

**Examples:**
```bash
hostname                        # Display host name
```

**See Also:** [whoami](#whoami), [uname](#uname)

---

### notes
Small notepad to jot down notes and items of interest for later viewing.

**Usage:** `notes`

**Features:**
- Simple notepad interface
- Quick note taking
- View saved notes

**Examples:**
```bash
notes                           # Open notepad
```

**See Also:** [editor](#editor), [vim](#vim)

---

### email
Email client and mail management.

**Usage:** `email -c | -v | -o ID | -l [USER] [PASSWORD] | -s | -n | -b RECIPIENT SUBJECT [MESSAGE] [COUNT] | -r ID | -x | -m ACCOUNT [PASSWORD] REFRESH`

**Options:**
- `-c` - Open email client interface
- `-v` - View inbox messages
- `-o ID` - Open specific email by ID
- `-l [USER] ([PASSWORD])` - Login to email account
- `-s` - Setup new email account configuration
- `-n` - Compose new email message
- `-b RECIPIENT SUBJECT [MESSAGE] [COUNT]` - Email bomb attack
- `-r ID` - Remove email by ID
- `-x` - Clear all emails from inbox
- `-m ACCOUNT [PASSWORD] REFRESH` - Monitor account with auto-refresh

**Limitation:** One email account per session

**Features:**
- Command-line email client
- Inbox monitoring
- Email bombing capabilities
- Account login and management
- Message composition

**Examples:**
```bash
email -s                        # Setup new account
email -l user@mail.com         # Login with password prompt
email -c                        # Open email client GUI
email -v                        # View all messages
email -o 5                      # Open email ID 5
email -n                        # Compose new message
email -b target@victim.com Spam Test 100
email -r 12                     # Delete email ID 12
email -x                        # Clear entire inbox
email -m user@mail.com pass123 30
```

**See Also:** [smtp](#smtp), [open](#open), [notes](#notes)

---

### rec
System backup and recovery utility.

**Usage:** `rec -b | -r`

**Options:**
- `-b` - Backup essential files (Main and Shell objects only)
- `-r` - Restore from backup (Main, Shell, and Computer objects)

**Features:**
- Framework backup and restore
- Disaster recovery
- Essential file snapshots
- Configuration preservation

**Examples:**
```bash
rec -b                          # Backup current system state
rec -r                          # Restore from backup
rec -b                          # Create pre-attack backup
scan -l                         # Perform operations
rec -r                          # Recover if needed
```

**See Also:** [backup](#backup), [restore](#restore), [system](#system)

---

### sniffer (sniff)
Network packet capture and analysis.

**Usage:** `sniffer [--save|--deploy]`

**Options:**
- `sniff` - Launch integrated packet sniffer (real-time)
- `sniff --save` - Capture packets to file
- `sniff --deploy` - Deploy standalone sniffer (background)

**Features:**
- Network packet analyzer
- Traffic monitoring and capture
- Credential harvesting
- Traffic analysis
- Network reconnaissance
- Only one flag at a time

**Examples:**
```bash
sniff                           # Start live packet capture
sniff --save                    # Capture and save packets
sniff --deploy                  # Deploy persistent sniffer
sniff                           # Monitor for plaintext credentials
```

**See Also:** [tcpdump](#tcpdump), [wireshark](#wireshark), [scan](#scan)

---

### randix
Custom math function for binary operations.

**Usage:** `randix -b NUMBER | randix -n BINNUMBER`

**Options:**
- `randix -b NUMBER` - Get binary representation of number
- `randix -n BINNUMBER` - Get number representation of binary

**Examples:**
```bash
randix -b 42                    # Convert to binary
randix -n 101010                # Convert from binary
```

**See Also:** [bc](#bc), [bit](#bit)

---

### jack
Initiate local dictionary attack.

**Usage:** `jack [NICKNAME]`

**Features:**
- Local dictionary attack
- Root password insertion to cache
- Optional nickname parameter
- Cache population

**Examples:**
```bash
jack                            # Basic attack
jack homebase                   # With nickname
```

**See Also:** [dict](#dict), [cache](#cache), [shadow](#shadow)

---

### pwgen
Generate passwords.

**Usage:** `pwgen | pwgen -s | pwgen -l NUMBER`

**Options:**
- `pwgen` - Generate password (15 chars)
- `pwgen -s` - Generate hard password (20 chars)
- `pwgen -l NUMBER` - Generate password with NUMBER chars

**Examples:**
```bash
pwgen                           # 15-char password
pwgen -s                        # 20-char hard password
pwgen -l 25                     # 25-char password
```

**See Also:** [pass](#pass), [bc](#bc)

---

### drop
Alias to [-x] commands/flags for clearing caches and files.

**Usage:** `drop -m | -a | -p | -f | -w | -c | -d | -v | -l | -s`

**Options:**
- `-m` - Clear /lib except init.so and net.so
- `-a` - Clear all passwords and virtual/hard files [shadow] [cache] [dirty] [vfile] [share] [libs]
- `-p` - Clear all passwords [shadow] [cache]
- `-f` - Clear all files [vfile] [share] [libs]
- `-w` - Clear shadow file [shadow]
- `-c` - Clear cache [cache]
- `-d` - Clear dirty file [dirty]
- `-v` - Clear vfile file cache [vfile]
- `-l` - Clear shared libs folder [libs]
- `-s` - Clear share folder [share]

**Examples:**
```bash
drop -m                         # Clear /lib libraries
drop -a                         # Clear everything
drop -p                         # Clear all passwords
drop -c                         # Clear cache
drop -w                         # Clear shadow file
```

**See Also:** [clean](#clean), [rm](#rm)

---

### linklibs
Remote library linking for performance.

**Usage:** `linklibs | linklibs -a | -m | -c | -u`

**Options:**
- `linklibs` - Toggle all libraries (links both if none active, unlinks all if any linked)
- `-a` - Link all libraries (metaxploit and crypto)
- `-m` - Link metaxploit only (for exploit scanning)
- `-c` - Link crypto only (for hash deciphering)
- `-u` - Unlink all libraries (return to local processing)

**Features:**
- Remote hardware acceleration
- Exploit scanning enhancement
- Hash cracking performance boost
- Ideal for router operations
- Low-powered device support

**Examples:**
```bash
linklibs -a                     # Link both libraries
linklibs -m                     # Link metaxploit for scanning
linklibs -c                     # Link crypto for cracking
linklibs                        # Auto link if none active
linklibs -u                     # Unlink all libraries
```

**See Also:** [library](#library), [decipher](#decipher), [scan](#scan)

---

### addpass
Add password to rainbow tables.

**Usage:** `addpass [PASSWORD]`

**Features:**
- Add custom password to rainbow tables
- Duplicate check before insertion
- Improve cracking success rates
- Support for common passwords and discovered credentials

**Examples:**
```bash
addpass password123             # Add weak password
addpass SecureP@ss987          # Add cracked password
addpass CompanyName123         # Add organization-specific
addpass Welcome2024            # Add seasonal password
```

**See Also:** [rainbow](#rainbow), [pass](#pass), [hashcat](#hashcat)

---

## Advanced Features

### > (arrow)
Redirect command output to a file, overwriting existing content.

**Usage:** `command > [filename]`

**Features:**
- If no filename is specified, output saves to `command_name.txt` automatically
- Overwrites existing files
- All output goes to file, not terminal

**Examples:**
```bash
ls > directory_list.txt         # Save listing to file
nmap host.ip.addr >             # Auto-saves to nmap.txt
grep "error" log.txt > errors.txt
```

---

### >> (arrow2)
Append command output to an existing file.

**Usage:** `command >> FILE`

**Features:**
- File must already exist
- Adds to end of file
- All output goes to file, not terminal

**Examples:**
```bash
echo New entry >> log.txt       # Append to log
ps >> processes.txt             # Append process list
```

---

### ; and && (and)
Chain multiple commands using `;` (unconditional) or `&&` (conditional).

**Usage:** `command ; command` | `command && command`

**Features:**
- `;` runs all commands regardless of success/failure
- `&&` short-circuits on failure (second runs only if first succeeds)
- Can mix both in one line

**Examples:**
```bash
ls ; pwd ; whoami               # Run three commands sequentially
cd /tmp && ls                   # List only if cd succeeds
cd /etc && cat passwd ; echo done  # Mixed chaining
```

---

### ! (bang)
Re-execute the most recent command from history.

**Usage:** `!`

**Examples:**
```bash
scan -l                         # Run command
!                               # Re-runs scan -l
```

---

### !! (bang2)
Display the command history buffer.

**Usage:** `!!`

**Examples:**
```bash
!!                              # View command history
```

---

### !!! (bang3)
Print the last issued command without executing it.

**Usage:** `!!!`

**Examples:**
```bash
!!!                             # Print last command for verification
```

---

### Pipes
Chain commands with `|` for data flow:

```bash
cat file.txt | grep "error" | wc -l     # Count errors
ls -l | awk '{print $1}'                # Extract permissions
find -n "*.log" | wc -l                 # Count log files
ps | grep "ssh" | wc -l                 # Count SSH processes
```

### Globs
Use wildcards for file patterns:

```bash
rm *.tmp                        # All .tmp files
cat test*.txt                   # All test*.txt
chmod +x *.sh                   # All .sh files
```

---

## Piping System

### pipe
Unix-style command chaining with output redirection.

**Usage:** `command1 | command2 | command3` or `command > file` or `command >> file`

**Operators:**
- `|` - Pipe output from one command to next
- `>` - Redirect output to file (overwrite)
- `>>` - Append output to file

**Supported Pipe Commands:**
`awk`, `bc`, `cat`, `column`, `cut`, `debug`, `decipher`, `diff`, `echo`, `env`, `file`, `find`, `grep`, `head`, `join`, `jq`, `l33t`, `locate`, `ls`, `nmap`, `nslookup`, `ping`, `ps`, `pwd`, `rev`, `scanaddress`, `scanlib`, `scanrouter`, `sed`, `set`, `sort`, `split`, `stat`, `tail`, `tee`, `time`, `tr`, `trim`, `uniq`, `unset`, `uptime`, `wc`, `whois`, `xc`, `xclip`

**Features:**
- Multi-command chains
- File output redirection
- Pipe variables with $VAR expansion
- Variable capture from pipe output
- Default filename: pipe_out.txt
- Redirects must be at END of chain
- Cannot redirect in middle of pipes

**Common Errors:**
```bash
# Wrong in pipe chain:
bc ip | pipe set IP
# Right:
bc ip | set IP

# Wrong standalone:
env IP
unset IP
debug on

# Right standalone:
pipe env IP
pipe unset IP
pipe debug on

# Invalid redirect position:
cmd1 > out.txt | cmd2
# Redirects must be at end of chain
```

**Pipe Variables:**
Store and reuse data across pipe commands using bash-like variable syntax.

```bash
# Variable assignment
set VAR value               # Store value in VAR
set VAR 10                  # Store number
set NAME "John Doe"         # Store string

# Capture from pipe
cat file.txt | set CONTENT  # Store pipe output
echo "5 * 2" | bc | set N   # Store calculation result
cat /etc/passwd | wc -l | set COUNT  # Store line count

# Variable expansion
echo "$VAR"                 # Expand variable
echo "Hello $NAME"          # Expand in string
echo "${VAR}text"           # Use braces for word boundaries

# Variable management
env                         # List all variables
env VAR                     # Show specific variable
env VAR=value               # Set variable (alternative)
env -c                      # Clear all variables
unset VAR                   # Remove variable

# Debug mode
debug on                    # Enable debug output
debug off                   # Disable debug output
debug status                # Show current state
```

**Variable Examples:**
```bash
# Math with variables
set X 10 | set Y 20 | echo "$X + $Y" | bc | set RESULT | echo "Result: $RESULT"

# Extract and store root hash
cat /etc/passwd | grep "^root:" | cut -d: -f2 | set ROOTHASH | echo "$ROOTHASH"

# Count and display
cat /etc/passwd | wc -l | set COUNT | echo "Found $COUNT users"

# Store multiple lines
cat /etc/passwd | cut -d: -f1 | set USERS | echo "$USERS"

# Complex operations
set A 3 | set B 4 | echo "($A * $A) + ($B * $B)" | bc | set C | echo "Result: $C"
```

**Output Redirection:**
```bash
command > file              # Overwrite file
command >> file             # Append to file
command >                   # Save to pipe_out.txt
command >>                  # Append to pipe_out.txt
```

**Common Patterns:**
```bash
# Text processing
cat file.txt | grep "error" | wc -l     # Count errors
ps | grep sshd | awk '{print $2}'       # Extract PIDs

# Variables with calculations
set NUM 5 | echo "$NUM * 2" | bc | set RESULT | echo "Result: $RESULT"
cat data.txt | wc -l | set LINES | echo "File has $LINES lines"

# Character transformation
echo "HELLO" | tr A-Z a-z               # Lowercase
cat data.txt | tr -d 0-9                # Remove digits
echo "hello    world" | tr -s ' '       # Squeeze spaces

# Field extraction
cat /etc/passwd | cut -d: -f1           # Extract usernames
ps | awk '{print $1,$5}'                # Print user and command

# Sorting and deduplication
cat names.txt | sort | uniq             # Sort and dedupe
ls | sort -r                            # Reverse sort

# Pattern matching
cat log.txt | grep "failed" | wc -l     # Count failures
find /etc -name "*.conf" | grep ssh     # Find SSH configs

# Hash cracking
cat hashes.txt | decipher               # Crack MD5 hashes

# Calculations
echo "5*3+2" | bc                       # Calculate: 17
cat numbers.txt | bc sum                # Sum numbers

# Output to files
ps | grep bash > processes.txt          # Save to file
cat log.txt | grep error >> errors.txt  # Append errors
```

**awk Examples:**
```bash
# Field extraction
ps | awk '{print $1}'                   # Print field 1
cat /etc/passwd | awk -F: '{print $1}'  # Custom delimiter
echo "a b c" | awk '{print $2}'         # Print "b"

# Last field
echo "one two three" | awk '{print $NF}' # Print "three"

# Field count
echo "a b c d" | awk '{print NF}'       # Print 4
```

**sed Examples:**
```bash
# Find and replace
echo "hello world" | sed 's/world/universe/'
cat file.txt | sed 's/old/new/g' > updated.txt
echo "abc123def" | sed 's/[0-9]//g'    # Remove digits
```

**cut Examples:**
```bash
# Character ranges
echo "hello" | cut -c 1-3               # "hel"
echo "world" | cut -c 2-                # "orld"

# Field extraction
echo "a:b:c" | cut -d: -f2              # "b"
echo "1,2,3" | cut -d, -f1,3            # "1,3"
```

**sort Examples:**
```bash
cat names.txt | sort                    # Alphabetical
cat numbers.txt | sort -n               # Numerical
ls | sort -r                            # Reverse
```

**Notes:**
- Pipe chains can be arbitrarily long
- Output is passed as text between commands
- Each command processes input and sends to next
- Extremely powerful for data processing workflows
- See [pipe.md](pipe.md) for complete reference

**See Also:** grep, awk, sed, tr, cut, sort, wc

---

## See Also

- [BASH_FEATURES.md](BASH_FEATURES.md) - Bash scripting system
- [pipe.md](pipe.md) - Pipe command details
- [X.md](X.md) - Core architecture
- [STYLE_GUIDE.md](STYLE_GUIDE.md) - Code conventions
- [GREYSCRIPT_REFERENCE.md](GREYSCRIPT_REFERENCE.md) - Language reference

## Additional Commands from Man4

### iploop
Automated exploit loop attack.

**Usage:** `iploop IP [PARAM] | iploop -l | iploop -x`

**Arguments:**
- `IP` - Target IP for automated exploitation
- `[PARAM]` - Optional attack parameter

**Flags:**
- `-l` - List captured objects from watchlist
- `-x` - Clear watchlist results

**Features:**
- Automated exploit cycling
- Continuous attack until watchlist fills
- All active exploits attempted
- Ideal for periodic target monitoring
- Use bang (!) to re-execute quickly

**Examples:**
```bash
iploop 10.0.0.5             # Loop all exploits
iploop 192.168.1.100 root   # Target root access
iploop -l                   # View captures
iploop -x                   # Clear results
```

**See Also:** [exploits](#exploits), [scan](#scan), [attack](#attack)

---

### temp
Temporary data store for unique entries.

**Usage:** `temp -a STRING | temp -l | temp -c | temp -r | temp -w`

**Flags:**
- `-a STRING` - Add item to store (rejects duplicates)
- `-l` - List all stored items
- `-c` - Clear all items
- `-r` - Read from file
- `-w` - Write to temp.lst file

**Features:**
- Unique-only storage (auto-reject duplicates)
- In-memory collection
- IP address tracking
- Target management
- File import/export

**Examples:**
```bash
temp -a 10.0.0.5            # Store IP
temp -a 192.168.1.100       # Add target
temp -l                     # List all
temp -r targets.txt         # Import list
temp -w                     # Export to temp.lst
temp -c                     # Clear all
```

**See Also:** [list](#list), [cache](#cache), [scan](#scan)

---

### recon
Remote reconnaissance and data gathering.

**Usage:** `recon [--extreme] [OPTIONS] IP`

**Flags:**
- `-a IP` - Extended recon with admin email attack
- `-s IP` - Search for specific files; use `-f` for filename and `-p` for search path
- `-r IP` - Reverse/email-focused reconnaissance
- `--filter [IP]` - Interactively filter printed dataset
- `-u` - Show/filter user dataset instead of email dataset
- `--save` - Save results to `reconData.txt` in current directory
- `-i LAN_IP` - Restrict LAN bounce targeting to one LAN IP
- `--file PATH` - Process IP list from file, one IP per line
- `--extreme` - Expand LAN bounce enumeration from `0-50` to `0-255`

**Features:**
- Public information gathering
- Email and credential collection
- User and bank dataset gathering when readable
- File search mode with configurable name and path
- Uses LAN bounce when available, then falls back to direct exploits
- Interactive dataset filtering and optional save-to-file output

**Examples:**
```bash
recon 203.0.113.50          # Basic recon
recon -a 198.51.100.10      # Attack admin email
recon --extreme 198.51.100.25  # Max addressing
recon -s -f passwords.txt 203.0.113.100  # File search
recon -r 203.0.113.241      # Email-focused recon
recon --filter 203.0.113.241  # Filter email dataset
recon -u --filter 203.0.113.241  # Filter user dataset
recon --save 203.0.113.241  # Save recon results
recon --file targets.txt    # Batch recon
```

**See Also:** [dig](#dig), [scan](#scan), [nslookup](#nslookup)

---

### pRoot
Automated root shell and framework pivot.

**Usage:** `pRoot [y]`

**Arguments:**
- `[y]` - Skip confirmation prompts

**Features:**
- Automated privilege escalation
- Automatic framework pivot to user home
- Shell objects only
- Streamlined post-exploitation
- Confirmation bypass for scripting

**Examples:**
```bash
pRoot                       # Get root with prompts
pRoot y                     # Skip confirmations
scan -l && pRoot            # Exploit then escalate
```

**See Also:** [sudo](#sudo), [su](#su), [passwd](#passwd)

---

### probe
System type detection (NPC vs player).

**Usage:** `probe`

**Features:**
- System fingerprinting
- NPC vs player classification
- Preliminary checks
- Most effective on workstations
- Less reliable on servers

**Examples:**
```bash
probe                       # Check system type
```

**See Also:** [scan](#scan), [info](#info), [stat](#stat)

---

### es
Discrete exploit scanning.

**Usage:** `es IP|DOMAIN PORT [ARGUMENT] | es LIBRARY [ARGUMENT] | es -l | es -u INDEX | es -x [INDEX]`

**Flags:**
- `-l` - List captured objects
- `-u INDEX` - Use captured object by index
- `-x INDEX` - Clear objects (supports ranges: 1-5)

**Features:**
- Most discrete scanning method
- Minimal network detection
- Specific service targeting
- Local library scanning (accepts partial names)
- May find newer exploits than local libs

**Examples:**
```bash
es apt                      # Scan APT library
es ssh                      # Scan SSH library
es 180.94.158.132 80       # Scan web service
es 203.0.113.50 22         # Scan SSH service
es -l                       # List results
es -u 0                     # Use first exploit
es -x 2-5                   # Clear range
```

**See Also:** [scan](#scan), [exploits](#exploits), [nmap](#nmap)

---

### config
Framework configuration management.

**Usage:** `config [OPTION]`

**Options:**
- `-c` - Create/recreate config file
- `-a` - Toggle auto solve PObjects
- `-k` - Toggle PObject solver debug
- `-m` - Toggle metaxploit update on launch
- `-e` - Toggle auto clear exploit scan buffer
- `-p` - Toggle load passwords on launch
- `-d` - Toggle load exploit database on launch
- `-o` - Toggle load library database on launch
- `-s` - Toggle auto-add sessions
- `-i` - Toggle dirty router IP logging
- `-l` - Toggle dynamic LAN IP tracking
- `-y` - Toggle proxy log for crash recovery
- `-h` - Toggle short home path
- `-z` - Toggle check dsession before scan
- `-r` - Toggle use rshell shell objects
- `-b` - Toggle clear shadow cache on startup
- `-v [NAME]` - Set vulnerable library for auto missions
- `-x [INDEX]` - Set exploit index from vulnerable library
- `stats` - View current settings
- `run` - Interactive config prompt
- `on` - Enable all settings
- `off` - Disable all settings
- `--reset` - Reset to defaults (requires relaunch)

**Features:**
- Framework behavior control
- Once exists, stops self-removal on exit
- Auto-recreates on corruption
- All settings disabled by default
- Long processes can be stopped by pressing 'q'

**Examples:**
```bash
config -c                   # Create config
config status               # View settings
config on                   # Enable all
config off                  # Disable all
config run                  # Interactive setup
config -d                   # Toggle exploit db load
config -v libssh.so         # Set lib for missions
config -x 3                 # Use exploit index 3
config --reset              # Reset defaults
```

**See Also:** [sys](#sys), [make](#make), [set](#set)

---

### batch
Execute batch command file.

**Usage:** `batch FILE`

**Arguments:**
- `FILE` - File containing commands (one per line)

**Features:**
- Batch script executor
- Automate command sequences
- Framework and bash script support
- Repeatable operations

**Examples:**
```bash
batch commands.txt          # Run batch file
batch /root/auto.bat        # Execute automation
```

**File Format Example:**
```
mark
@auto 105.145.194.135 192.168.9.2
mark
```

**See Also:** [exec](#exec), [script](#script)

---

### lms
Library Management System framework.

**Usage:** `lms [OPTIONS]`

**Features:**
- Comprehensive database management
- Library version tracking
- Dependency resolution
- Service integration
- Advanced library operations

**Examples:**
```bash
lms                         # Open LMS
```

**See Also:** [libs](#libs), [load](#load), [share](#share)

---

### pack
Pack or repack libraries and routers for portable deployment.

**Usage:** `pack -a|-m|-c|-r|-s|-t|--check [-y] [-i IP]`

**Flags:**
- `-a` - Pack all (crypto, metaxploit, router)
- `-m [-y]` - Pack metaxploit.so (skip removal confirmation with -y)
- `-c [-y]` - Pack crypto.so (skip removal confirmation with -y)
- `-r [-i IP]` - Pack router (optionally specify IP)
- `-s` - Pack smart appliance libraries
- `-t` - Pack traffic management libraries
- `--check` - List all currently packed items

**Features:**
- Library packaging for deployment
- Crypto encryption/decryption (requires root)
- Router packaging
- Appliance library packaging
- Portable library management
- Stored in /payload/data folder

**Notes:**
- X automatically manages metaxploit.so and crypto.so in data
- Other libraries require manual placement
- Target system libraries take precedence over packed versions
- Crypto operations require root access

**Examples:**
```bash
# Pack all libraries
pack -a                     # Pack crypto, metaxploit, router

# Pack individual items
pack -m                     # Pack metaxploit with confirmation
pack -m -y                  # Pack metaxploit skip confirmation
pack -c -y                  # Pack crypto skip confirmation
pack -r                     # Pack current router
pack -r -i 192.168.1.1      # Pack specific router
pack -s                     # Pack appliance libraries
pack -t                     # Pack traffic libraries

# Check packed items
pack --check                # List all packed items
```

**See Also:** lms, libs, 0day

---

### dig
Router network crawler and reconnaissance.

**Usage:** `dig [OPTIONS]`

**Flags:**
- `--extreme` - Maximum network enumeration
- `--lwipe` - Wipe logs during crawl

**Features:**
- Extensive router reconnaissance
- Network topology mapping
- Multi-hop crawling
- Log wiping capabilities
- Deep network intelligence

**Examples:**
```bash
dig                         # Standard crawl
dig --extreme               # Maximum enumeration
dig --lwipe                 # Crawl and wipe logs
```

**See Also:** [recon](#recon), [scan](#scan), [nmap](#nmap)

---

### app
Smart appliance interface.

**Usage:** `app [OPTIONS]`

**Features:**
- Smart appliance control
- Power management
- Temperature control
- Device interface

**Examples:**
```bash
app                         # Open appliance interface
```

**See Also:** [service](#service), [open](#open)

---

### cam
Camera surveillance system.

**Usage:** `cam [OPTIONS]`

**Features:**
- Camera surveillance
- Vehicle tracking
- Remote monitoring
- Capture management

**Examples:**
```bash
cam                         # Open camera system
```

**See Also:** [monitor](#monitor), [sniff](#sniff)

---

### scanlan
Graphical LAN topology scanner.

**Usage:** `scanlan`

**Features:**
- Graphical LAN scanner
- Network topology visualization
- Device discovery
- Interactive mapping

**Examples:**
```bash
scanlan                     # Launch graphical scanner
```

**See Also:** [scan](#scan), [nmap](#nmap), [iwlist](#iwlist)

---

### zip
Archive creator, unpacker, and viewer.

**Usage:** `zip [OPTIONS] FILE`

**Features:**
- Create archives
- Unpack archives
- View archive contents
- Compression utility

**Examples:**
```bash
zip files.zip               # Create archive
zip -x files.zip            # Extract archive
zip -l files.zip            # List contents
```

**See Also:** [gzip](#gzip), [tar](#tar), [cp](#cp)

---

### tar
File and folder archiver (tarballs).

**Usage:** `tar -c|-x|-v|-m|-u [options] <file>`

**Flags:**
- `-c <file>` - Create archive from folder
  - `-n <name>` - Custom tarball name
  - `-s <path>` - Save path
  - `-r` - Remove source after creation
- `-x <tarfile>` - Extract archive
  - `-e <path>` - Extract to specific path
  - `-r` - Remove tarball after extraction
- `-v <--memory|tarfile>` - View contents
- `-m <file>` - Store tarball in memory
  - `-r` - Remove source after storing
- `-u` - Retrieve tarball from memory
  - `-r` - Clear memory after extraction

**Features:**
- Folder archiving to text files
- File and folder structure preservation
- Memory storage support
- Multi-file extraction
- NOT for binary files
- Use on small files only (RAM issues with large files)

**File Object Limitation:** File objects can only use `-m` flag

**Examples:**
```bash
# Create archives
tar -c /home/user/folder            # Create tarball
tar -c -r -n backup /home/data      # Named tarball, remove source
tar -c -s /home/tux/docs myproject  # Create in specific location

# Extract archives
tar -x backup.tar                   # Extract to current dir
tar -x -e /home/restore backup.tar  # Extract to path
tar -x -r data.tar                  # Extract and remove tarball

# View and memory
tar -v backup.tar                   # List files in tarball
tar -m /home/user/folder            # Store in memory
tar -u                              # Retrieve from memory
```

**Warning:** Not for binary files. Large files cause RAM issues.

**See Also:** zip, gzip, pack

---

### active
Show active network interface.

**Usage:** `active`

**Features:**
- Display active interface
- Network status
- Connection info

**Examples:**
```bash
active                      # Show active interface
```

**See Also:** [ifconfig](#ifconfig), [iwconfig](#iwconfig)

---

### reset
Clear X internal cache and shell cache.

**Usage:** `reset`

**Features:**
- Clear framework cache
- Reset shell cache
- Memory cleanup
- Fresh state

**Examples:**
```bash
reset                       # Clear all caches
```

**See Also:** [clean](#clean), [drop](#drop)

---

### grab
Download remote log files.

**Usage:** `grab [OPTIONS]`

**Flags:**
- `-w` - Wipe logs after download

**Features:**
- Remote log download
- Optional log wiping
- Evidence collection
- Forensic cleanup

**Examples:**
```bash
grab                        # Download logs
grab -w                     # Download and wipe
```

**See Also:** [logs](#logs), [wipe](#wipe), [scrub](#scrub)

---

### heist
Bank heist automation helper.

**Usage:** `heist [OPTIONS]`

**Features:**
- Bank heist automation
- Transaction manipulation
- Financial operations
- Cryptocurrency integration

**Examples:**
```bash
heist                       # Launch heist helper
```

**See Also:** [bank](#bank), [coin](#coin), [wallet](#wallet)

---

### rnet
Refresh network interface.

**Usage:** `rnet`

**Features:**
- Refresh network interface
- Reconnect to network
- Reset connection
- Network recovery

**Examples:**
```bash
rnet                        # Refresh interface
```

**See Also:** [ifconfig](#ifconfig), [active](#active)

---

### lock
Lock configuration files to prevent saves.

**Usage:** `lock [FILE]`

**Features:**
- Lock config files
- Prevent modifications
- Configuration protection
- Write protection

**Examples:**
```bash
lock config.conf            # Lock config
```

**See Also:** [chmod](#chmod), [set](#set)

---

### disk
All-purpose disk management.

**Usage:** `disk [OPTIONS]`

**Features:**
- Comprehensive disk management
- Extensive sorting and filtering
- Partition management
- Storage analysis
- Multiple operations

**Examples:**
```bash
disk                        # Open disk manager
```

**See Also:** [df](#df), [du](#du), [mount](#mount)

---

### x
Hints and tricks command.

**Usage:** `x [TOPIC]`

**Features:**
- Framework hints and tips
- Init file explanations
- Search features guide
- Quick reference
- Help system

**Examples:**
```bash
x                           # Show all hints
x init                      # Init file help
x search                    # Search features
```

**See Also:** [man](#man), [help](#help), [cmds](#cmds)

---

### whoami
Display current user information.

**Usage:** `whoami`

**Features:**
- Show current username
- User identification
- Context verification

**Examples:**
```bash
whoami                      # Display current user
```

**See Also:** [hostname](#hostname), [uname](#uname), [groups](#groups)

---

### whatami
Display current object type.

**Usage:** `whatami`

**Features:**
- Show execution context type
- Object type identification
- Context awareness
- Shell vs Computer vs File detection

**Examples:**
```bash
whatami                     # Display object type
```

**See Also:** [whoami](#whoami), [probe](#probe)

---

## Additional Commands

### cron
Schedule X shell commands from a crontab file.

**Usage:** `cron [-f FILE]`

**Flags:**
- `-f FILE` - Use a custom crontab path (default: `~/Config/crontab`)

**Description:** Reads a crontab file and runs each job at its scheduled time. Unlike the standalone `/tools/cron` binary, this runs jobs through the X shell so any X command, alias, macro, builtin, external binary, or bash script works as a job. Prefix a bash script name with `@` to run it via `Bash.run`. Press `q` to stop, `r` to force-reload. The crontab auto-reloads whenever its content changes.

**Crontab Format:**
```
m  h  dom  mon  dow  command [args...]
```
Fields: minute (0-59), hour (0-23), day-of-month (1-31), month (1-12), day-of-week (0-6).
Wildcards: `*` any, `*/N` every N, `a,b,c` list, `a-b` range. Lines starting with `#` are comments.

**Examples:**
```bash
cron                            # Run with default ~/Config/crontab
cron -f /home/tux/jobs.cron     # Use custom crontab file
```

**Crontab Examples:**
```
0 * * * *   rm /home/tux/Config/Bank.txt   # every hour at :00
*/5 * * * * wipe                            # every 5 minutes
0 3 * * *   clean                           # daily at 3:00 AM
* * * * *   ls /home ; cat /etc/passwd      # run a chain
0 4 * * *   @backup                         # bash script in bash dir
*/10 9-17 * * 1-5  audit                   # every 10m, weekday hours
```

**See Also:** [vi](#vi), [alias](#alias)

---

### dump
Export man pages to text files.

**Usage:** `man dump` | `man dump COMMAND`

**Description:** Export man page documentation to plain text files. Without arguments, dumps all man pages to numbered files (`man_pages_1`, `man_pages_2`, etc.). With a command argument, exports that specific command's man page to `man_COMMAND.txt`. Strips color and formatting tags for plain text output.

**Examples:**
```bash
man dump                        # Export all man pages to files
man dump scan                   # Create man_scan.txt
man dump exploit                # Create man_exploit.txt
```

**See Also:** [man](#man)

---

### hex
Hexadecimal calculator with arithmetic and bitwise operations.

**Usage:** `hex VALUE` | `hex VALUE OPERATOR VALUE2` | `command | hex [OPERATOR VALUE2]`

**Description:** Perform arithmetic or bitwise operations on hex or decimal values. Input accepts `0x`-prefixed hex (e.g. `0x2A99789D`) or plain decimal. Output is always shown as `0xRESULT (decimal N)`. Useful for working with exploit memory addresses from mtree.

**Operators:**
- `+` `-` `*` `/` — Arithmetic
- `-and` — Bitwise AND
- `-or`  — Bitwise OR
- `-xor` — Bitwise XOR
- `-ls`  — Left shift
- `-rs`  — Right shift

**Examples:**
```bash
hex 0x2A99789D                  # Display with decimal equivalent
hex 0x2A99789D + 0x100          # Add 0x100 to a memory address
hex 0xFF -and 0x0F              # Bitwise AND: 0xF (decimal: 15)
hex 0x1 -ls 8                   # Left shift: 0x100 (decimal: 256)
hex 715553949                   # Decimal to hex: 0x2A99789D
cat mtree | hex + 0x100         # Add offset to every address in a file
```

**See Also:** [binary](#binary), [decimal](#decimal), [bit](#bit), [radix](#radix)

---

### initd
Manage `/etc/init.d` startup compiled scripts.

**Usage:** `initd -l` | `initd -a PATH` | `initd -r NAME`

**Flags:**
- `-l` — List all compiled scripts registered in `/etc/init.d`
- `-a PATH` — Copy the compiled script at PATH into `/etc/init.d` (runs on next boot)
- `-r NAME` — Delete the entry named NAME from `/etc/init.d`

**Examples:**
```bash
initd -l                        # Show all startup entries
initd -a /home/tux/hacktoolkit  # Register script to run on boot
initd -r hacktoolkit            # Remove from startup
```

**See Also:** [build](#build), [chmod](#chmod), [cp](#cp)

---

### paste
Merge lines of files side by side.

**Usage:** `paste FILE1 FILE2 [FILE...]` | `paste -d DELIM FILE1 FILE2` | `paste -s FILE` | `stdin | paste FILE`

**Flags:**
- `FILE1 FILE2` — Merge column by column, tab-separated (default)
- `-d DELIM` — Use DELIM as column separator instead of tab
- `-s` — Serial mode: merge all lines of each file into one tab-separated line per file
- `> FILE` / `>> FILE` — Redirect output

**Examples:**
```bash
paste ips.txt users.txt         # Merge IP list and user list side by side
paste -d , ips.txt ports.txt    # Comma-separated: 192.168.1.1,22
paste -s ips.txt                # Join all IPs onto one tab-separated line
paste -s -d , ips.txt           # Join all IPs comma-separated
seq 1 5 | paste -s -d ,         # 1,2,3,4,5 on one line
paste ips.txt users.txt > merged.txt  # Write to file
```

**See Also:** [seq](#seq), [column](#column), [join](#join), [cut](#cut)

---

### printf
Format and print data.

**Usage:** `printf FORMAT [ARG...]` | `stdin | printf FORMAT`

**Description:** Format and print ARGs according to FORMAT. Supports width, precision, and padding controls. When piped, stdin values are appended as additional arguments. Supports `>` and `>>` redirect.

**Format Specifiers:**
- `%s` — String
- `%d` — Decimal integer
- `%f` — Floating-point number
- `%x` / `%X` — Hex (lower/uppercase)
- `%o` — Octal
- `%c` — Character (from ASCII code)

**Format Flags:**
- `%-20s` — Left-align in width 20
- `%20s` — Right-align in width 20
- `%03d` — Zero-pad integer to width 3
- `%.2f` — Float with 2 decimal places
- `%+d` — Always show sign

**Escape Sequences:** `\n` newline, `\t` tab, `\r` carriage return, `\\` backslash

**Examples:**
```bash
printf "%s\n" hello             # Print hello on its own line
printf "%d + %d = %d\n" 3 5 8  # 3 + 5 = 8
printf "%.2f\n" 3.14159         # 3.14
printf "%x\n" 255               # ff
printf "%08x\n" 255             # 000000ff
printf "%-20s %s\n" host 192.168.1.1  # Left-align hostname column
echo 255 | printf "%x"          # Convert piped number to hex
```

**See Also:** [echo](#echo), [seq](#seq), [bc](#bc)

---

### radix
Convert numbers between any two bases.

**Usage:** `radix FROM_BASE TO_BASE VALUE` | `command | radix FROM_BASE TO_BASE`

**Description:** Convert a number from one base to another. Supports bases 2–36, using digits 0-9 and letters a-z for values above 9. When reading from a pipe, each line is treated as a value to convert.

**Arguments:**
- `FROM_BASE` — The base of the input value (2–36)
- `TO_BASE` — The base to convert to (2–36)
- `VALUE` — The number to convert (use lowercase for bases above 10)

**Examples:**
```bash
radix 10 2 255                  # Decimal to binary: 11111111
radix 2 10 11111111             # Binary to decimal: 255
radix 10 16 255                 # Decimal to hex: ff
radix 16 10 ff                  # Hex to decimal: 255
radix 10 8 255                  # Decimal to octal: 377
seq 1 10 | radix 10 16          # Convert 1-10 to hex
```

**See Also:** [binary](#binary), [decimal](#decimal), [bit](#bit), [hex](#hex)

---

### seq
Print a sequence of numbers.

**Usage:** `seq LAST` | `seq FIRST LAST` | `seq FIRST STEP LAST` | `seq [-s SEP] FIRST LAST`

**Flags:**
- `LAST` — Print 1 to LAST (inclusive)
- `FIRST LAST` — Print FIRST to LAST, step 1
- `FIRST STEP LAST` — Print FIRST to LAST incrementing by STEP (use negative STEP to count down)
- `-s SEP` — Use SEP as separator instead of newline
- `> FILE` / `>> FILE` — Redirect output

**Examples:**
```bash
seq 5                           # 1 2 3 4 5
seq 3 7                         # 3 4 5 6 7
seq 0 2 10                      # 0 2 4 6 8 10 (step 2)
seq 10 -1 1                     # Count down 10 to 1
seq -s , 1 5                    # 1,2,3,4,5
seq 1 5 | xargs -n1 echo Attempt  # Attempt 1 through Attempt 5
seq 80 90 | xargs -n1 pingport 192.168.1.1  # Scan a port range
seq 1 100 > numbers.txt         # Write 1-100 to file
```

**See Also:** [printf](#printf), [paste](#paste), [bc](#bc)

---

### yes
Enable or disable automatic yes to all prompts.

**Usage:** `yes` | `yes --off` | `yes -c`

**Description:** Sets a session-wide flag that automatically confirms all yes/no prompts without user input. Useful when running commands with `-i` (interactive) that would otherwise prompt before each operation. The flag is automatically cleared at the end of any pipeline, so `yes | cmd -i ...` works for pipeline-scoped auto-confirmation.

**Flags:**
- `yes` — Enable auto-yes; all GUI prompts return true automatically
- `yes --off` — Disable auto-yes and restore normal prompt behaviour
- `yes -c` — Check the current state of auto-yes (ON or OFF)

**Examples:**
```bash
yes                             # Enable auto-yes for all subsequent prompts
cp -i *.txt /backup             # All overwrite prompts auto-confirmed
yes --off                       # Re-enable normal prompting
yes | cp -i file.txt /etc       # Auto-confirm for this command only (pipeline-scoped)
yes -c                          # Print whether auto-yes is currently ON or OFF
```

**See Also:** [cp](#cp), [mv](#mv), [rm](#rm)

---