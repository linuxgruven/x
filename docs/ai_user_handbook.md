# AI User Handbook
## Complete Guide to Using X's AI Agent

**Welcome!** This handbook teaches you everything you need to know about using X's AI system, even if you've never used it before.

---

## Table of Contents

1. [What is the AI?](#what-is-the-ai)
2. [Getting Started](#getting-started)
3. [Basic Commands](#basic-commands)
4. [File Operations](#file-operations)
5. [Permission Management](#permission-management)
6. [Network Scanning](#network-scanning)
7. [Exploitation & Hacking](#exploitation-and-hacking)
8. [Data Extraction](#data-extraction)
9. [Configuration](#configuration)
10. [Natural Language Tips](#natural-language-tips) *(compound commands, synonyms, learning, conditionals, multi-target, clarification)*
11. [Common Patterns](#common-patterns)
12. [Troubleshooting](#troubleshooting)
13. [Examples Gallery](#examples-gallery)

---

## What is the AI?

The **X AI Agent** is a natural language command assistant that understands what you want to do and executes terminal commands for you.

### Why Use AI?

The AI understands many different ways to express the same intent!

### What Can It Do?

- 📂 **File Operations**: Copy, move, delete, create files
- 🔐 **Permissions**: Change file permissions, owners, and groups  
- 🌐 **Network Scanning**: Scan IPs, ports, and networks
- 💻 **Exploitation**: Find and exploit vulnerabilities
- 📧 **Data Extraction**: Get emails, passwords, and files
- ⚙️ **System Management**: Search files, view contents, manage processes
- 🔗 **Compound Commands**: Chain multiple actions in one input
- 🧠 **Learning**: Remembers your preferences and successful patterns between sessions

---

## Getting Started

### Basic Syntax

All AI commands start with `ai` followed by your request:

```bash
ai your request here
```

**For read-only commands** (viewing, listing, searching), quotes are optional:
```bash
ai show me test.txt
ai scan 192.168.1.1
ai list files
```

**For write commands** (copying, moving, deleting, changing permissions), use quotes to be safe:
```bash
ai copy test.txt to backup.txt
ai delete oldfile.txt
ai change permissions of myfile to 644
```

### Your First Command

Let's try reading a file:

```bash
ai show me the file test.txt
```

**What happens:**
1. AI detects you want to read a file (`cat` command)
2. AI extracts the filename: `test.txt`
3. AI executes the command and shows you the contents

That's it! No need to remember command syntax.

### Help Command

Ask the AI for help with any command:

```bash
ai what does chmod do?
ai how do I use scan?
ai explain the exploit command
```

---

## Basic Commands

### Viewing Files

**Show file contents:**
```bash
ai show me myfile.txt
ai read the file config.txt
ai display document.txt
ai cat myfile.txt  # Traditional command also works
```

**View directory contents:**
```bash
ai list files in this directory
ai show me what's in Documents
ai ls  # Traditional command also works
```

### Searching

**Search for text in files:**
```bash
ai search for 'password' in config.txt
ai find the word 'admin' in logfile.txt
ai grep 'error' in system.log
```

**Find files by name:**
```bash
ai find files named test.txt
ai locate all .txt files
ai search for files containing 'backup' in the name
```

### Creating Files

**Create an empty file:**
```bash
ai create an empty file called newfile.txt
ai touch test.txt
ai make a new file named data.txt
```

**Create a directory:**
```bash
ai create a directory called MyFolder
ai make a new folder named Projects
ai mkdir TestDir
```

---

## File Operations

### Copying Files

**Basic copy:**
```bash
ai copy test.txt to backup.txt
ai duplicate myfile.txt as myfile_backup.txt
ai cp document.txt to Documents/document.txt
```

**Copy with path:**
```bash
ai copy myfile.txt to /home/user/Documents
ai duplicate test.txt to Desktop/test_copy.txt
```

**What gets copied:**
- The file itself
- File contents
- Original permissions preserved

### Moving/Renaming Files

**Move file to different location:**
```bash
ai move test.txt to Documents
ai relocate myfile.txt to Desktop
ai mv old.txt to Archive/old.txt
```

**Rename file:**
```bash
ai rename test.txt to newname.txt
ai move oldname.txt to newname.txt
ai change test.txt name to final.txt
```

**Move and rename:**
```bash
ai move myfile.txt to Documents/renamed.txt
```

### Deleting Files

**Delete a file:**
```bash
ai delete test.txt
ai remove oldfile.txt
ai erase backup.txt
ai rm unwanted.txt
```

**⚠️ Warning:** File deletion is permanent! The AI will ask for confirmation before deleting.

### Creating Links

**Create a symbolic link:**
```bash
ai create a link from source.txt to link.txt
ai make a symlink from myfile.txt to shortcut.txt
ai ln source.txt to destination.txt
```

**What is a link?**  
A link is like a shortcut. Editing the link edits the original file.

---

## Permission Management

File permissions control who can read, write, or execute files.

### Understanding Permissions

**Permission Levels:**
- **Read (r/4)**: View file contents
- **Write (w/2)**: Modify file contents  
- **Execute (x/1)**: Run file as program

**Permission Numbers:**
- `777` = Full access (read + write + execute for everyone)
- `755` = Owner can do everything, others can read and execute
- `644` = Owner can read and write, others can only read
- `444` = Read-only for everyone
- `000` = No permissions for anyone

### Changing Permissions (chmod)

**Using permission numbers:**
```bash
ai change permissions of test.txt to 755
ai set permissions of myfile.txt to 644
ai chmod test.txt to 777
```

**Using descriptions:**
```bash
ai make test.txt executable
ai give full permissions to myfile.txt
ai set test.txt to read only
ai remove all permissions from secret.txt
```

**Change permissions of X to Y patterns:**
```bash
ai change permissions of test.txt to 755
ai set permissions of myfile.txt to read only
ai chmod test.txt to 777
ai give permissions of script.sh to executable
```

**Recursive permissions (for directories):**
```bash
ai change permissions of MyFolder to 755
# AI will ask: "Apply recursively to all files inside?"
```

### Changing Owner (chown)

**Change file owner:**
```bash
ai change owner of test.txt to root
ai chown test.txt to admin
ai set owner of myfile.txt to guest
```

**Using direct pattern:**
```bash
ai chown root test.txt
```

**Recursive:**
```bash
ai change owner of MyFolder to root
# AI will ask about recursive
```

### Changing Group (chgrp)

**Change file group:**
```bash
ai change group of test.txt to admin
ai chgrp test.txt to users
ai set group of myfile.txt to developers
```

### Changing Owner and Group (chog)

**Change both at once:**
```bash
ai chog guest test.txt
ai change owner and group of test.txt to root
ai chog of myfile.txt to admin
```

---

## Network Scanning

Network scanning finds computers, open ports, and vulnerabilities.

### Basic Scanning

**Scan a specific IP:**
```bash
ai scan 192.168.1.1
ai probe 10.0.0.5
ai check 172.16.0.1 for open ports
```

**Scan with service:**
```bash
ai scan 192.168.1.1 port 22
ai check 10.0.0.5 for ssh
ai probe 192.168.1.1 on port 80
```

### Scan Flags

**Scan random IP:**
```bash
ai scan a random ip
ai scan random network
ai probe a random host
```

**Scan localhost:**
```bash
ai scan local
ai scan localhost
ai check my computer
```

**Scan local network:**
```bash
ai scan the network
ai scan lan
ai probe home network
```

### What You'll See

```
Scanning 192.168.1.1...
Found computer: 192.168.1.1
Open ports:
  22 (SSH)
  80 (HTTP)
  443 (HTTPS)
Services:
  SSH version 2.0
  Apache web server
```

**Next steps after scanning:**
- Exploit vulnerabilities
- Crack passwords
- Extract data

---

## Exploitation and Hacking

### Discrete Exploit Scanning (es)

**Scan for library exploits:**
```bash
ai scan apt library
ai check metaxploit for vulnerabilities
ai scan crypto library
```

**Scan remote service:**
```bash
ai scan ssh on 192.168.1.1
ai scan ftp on 10.0.0.5 port 21
ai check http on 192.168.1.100
```

**What is es?**  
`es` (exploit scan) is a discrete scanning tool that:
- Checks local libraries for exploits
- Scans remote services for vulnerabilities
- Quieter than normal scan

### Finding Exploits

**After scanning:**
```bash
ai find exploits for this computer
ai show available exploits
ai what vulnerabilities exist?
```

### Executing Exploits

**Exploit a target:**
```bash
ai exploit 192.168.1.1
ai attack this computer
ai break into this system
```

**What happens:**
1. AI scans for vulnerabilities
2. Finds available exploits
3. Executes most promising exploit
4. Returns shell or file access

### Cracking Passwords

**Crack a password file:**
```bash
ai crack the password file
ai brute force passwords
ai crack user passwords
```

**Crack specific user:**
```bash
ai crack password for root
ai brute force admin password
```

### Privilege Escalation

**Escalate to root access:**
```bash
ai escalate to root
ai get root access
ai escalate privileges
```

**What happens:**
```
Agent: Understood - Execute cal command for root access
Agent: Executing plan...
NOVEMBER-( 2005 )
SU MO TU WE TH FR SA
      1  2  3  4  5  
6  7  8  9  10 11 12 
13 14 15 16 17 18 19 
20 21 22 23 24 25 26 
27 28 29 30
Done. Awaiting further instructions.
```

The AI uses the `cal` command to gain root privileges on the target system.

---

## Data Extraction

After gaining access to a system, extract valuable data.

### Router Data (dig)

**Extract email data:**
```bash
ai extract email data
ai dig for emails
ai get mail from router
```

**Extract banking data:**
```bash
ai extract bank information
ai dig for banking data
ai get financial records
```

**Extract passwords:**
```bash
ai extract passwords
ai dig for password file
ai get user credentials
```

**Extract all data:**
```bash
ai extract everything
ai dig all data from router
ai get all available information
```

### Shell Data

**List files:**
```bash
ai list files on this computer
ai show directory contents
```

**Download files:**
```bash
ai download /etc/passwd
ai get the password file
```

---

## Configuration

The AI has settings you can change.

### Output Level

**Control verbosity:**
```bash
ai verbose mode on      # Show detailed logs
ai verbose mode off     # Normal output
ai quiet mode on        # Minimal output
ai quiet mode off       # Normal output
```

**Or set directly:**
```bash
ai set outputLevel to 2  # 0=silent, 1=normal, 2=verbose
```

### Dry Run Mode

**Preview commands without executing:**
```bash
ai dry run on           # Preview mode
ai dry run off          # Execute mode
```

**Example:**
```bash
ai dry run on
ai delete test.txt
# AI shows: "Would execute: rm test.txt" (but doesn't delete)
```

### Aggressive Mode

**Enable aggressive exploitation:**
```bash
ai aggressive mode on
ai aggressive mode off
```

**What it does:**
- Tries all exploits instead of safest one
- Uses brute force when possible
- Reduces delays between attempts

### Stealth Mode

**Minimize detection:**
```bash
ai stealth mode on
ai stealth mode off
```

**What it does:**
- Uses slower, quieter scanning
- Randomizes attack timing
- Clears logs when possible

### Debug Mode

**Show technical details:**
```bash
ai debug mode on
ai debug mode off
```

**Use when:**
- Commands aren't working as expected
- You want to see what AI is thinking
- Reporting bugs

### View Configuration

**See current settings:**
```bash
ai show config
ai display configuration
ai view settings
```

**Reset to defaults:**
```bash
ai reset config
ai restore default settings
```

---

## Natural Language Tips

### The AI Understands Many Phrasings

**Same command, different words:**
```bash
ai show me test.txt
ai display test.txt
ai read test.txt
ai cat test.txt
ai view the contents of test.txt
ai let me see test.txt
```

All of these do the same thing!

### Use Natural Sentences

**You can be conversational:**
```bash
ai can you show me the file test.txt?
ai I need to see what's in myfile.txt
ai please scan the local network
```

### Command Names Work Too

**If you know the command name:**
```bash
ai chmod test.txt to 755"
ai grep 'password' in config.txt"
ai scan 192.168.1.1
```

### Case Doesn't Matter

**Filenames preserve case, but commands don't:**
```bash
ai SHOW ME TEST.TXT"      # Works, but filename becomes uppercase
ai Show Me test.txt"      # Preserves test.txt case
ai show me TeSt.TxT"      # Preserves TeSt.TxT case
```

**Best practice:** Use normal capitalization for filenames.

### Compound Commands (Chaining)

You can chain multiple actions in a single input using natural connectors:

```bash
ai scan 124.55.66.77 and then exploit it
ai get me a root router shell from 10.0.0.1 and store
ai exploit 192.168.1.1 afterwards extract emails
ai first scan 172.16.0.5 then crack the password
```

**Supported connectors:**
- "and then"
- "then" (with or without "first" at the start)
- "afterwards"
- "after that"

The AI understands IPs well — it knows the difference between public and private addresses and parses them from anywhere in your sentence.

The AI runs each part in order, stopping if any step fails.

### Smarter Word Understanding

The AI uses context to understand ambiguous words:

```bash
ai break the password        # → crack (because "password")
ai break the system          # → exploit (because "system")
ai check the network         # → scan (because "network")
ai grab the file             # → fetch (because "file")
ai wipe the logs             # → remove (because "logs")
```

Surrounding words help the AI pick the right meaning.

### Learning & Memory

The AI remembers your patterns between sessions:

- **Command preferences**: If you frequently use certain commands, the AI prioritizes them
- **Flag preferences**: Your preferred flags per command are remembered
- **Successful patterns**: Multi-step sequences that worked are saved as templates and reused

This data persists to disk automatically — no setup needed.

### Conditional Commands

You can make the AI do something only if a condition is met:

```bash
ai if scan has ssh, then exploit it
ai scan 10.0.0.1, if it works exploit it
ai scan 192.168.1.1, on success crack root
ai if scan finds open ports, then exploit them
```

**Supported patterns:**
- "if X has/finds/shows Y, then Z" — check if result contains something
- "X, if it works Y" — do Y only if X succeeds
- "X, on success Y" — same as above
- "X, if successful Y" — same as above

The AI evaluates the condition against the result of the first command. If the condition isn't met, it skips the followup and tells you.

### Multi-Target Commands

Target multiple IPs in a single command by listing 3 or more:

```bash
ai scan 10.0.0.1 10.0.0.2 10.0.0.3
ai exploit 192.168.1.1 192.168.1.2 192.168.1.3
```

The AI runs the action on each target independently, reporting results for each one. This is much faster than typing the same command for each IP individually.

**Note:** Two IPs separated by a compound connector (like "and then") are treated as a compound command, not multi-target. Multi-target kicks in at 3+ IPs.

### Intent Clarification

When the AI isn't sure what you mean, it asks instead of guessing:

```bash
> ai break the target
Agent: Multiple interpretations found. Did you mean:
  1. crack
  2. exploit
> [pick one]
```

This also works when the AI doesn't recognize any action:

```bash
> ai do something to the server
Agent: What would you like to do?
  1. scan
  2. exploit
  3. crack
  ...
> [pick one]
```

### Smarter Template Matching

When the AI has learned successful sequences (like scan→exploit→crack), it can now reuse them even when you use different words. For example, saying "attack" will match templates containing "exploit" because the AI knows they're related.

Related word groups the AI understands:
- **exploit/attack/hack/pwn/compromise/break** — all mean "exploit"
- **scan/probe/recon/enumerate/discover/check** — all mean "scan"
- **crack/brute/bruteforce/decrypt/password** — all mean "crack"
- **fetch/get/grab/pull/retrieve/extract/dump** — all mean "fetch"

---

## Common Patterns

### "of X to Y" Pattern

Many commands use "of X to Y" structure:

```bash
ai change permissions of test.txt to 755"
ai change owner of test.txt to root"
ai change group of test.txt to admin"
ai move content of source.txt to dest.txt"
```

### Direct Pattern

Some commands support direct structure:

```bash
ai chmod test.txt to 755"           # Direct
ai chown root test.txt"             # Direct
ai chgrp admin test.txt"            # Direct
```

### "X into Y" Pattern

For copy/archive operations:

```bash
ai copy test.txt into backup.txt"
ai move myfile.txt into Archive"
ai tar myfiles into backup.tar"
```

### Flag-Based Commands

Some commands use flags instead of targets:

```bash
ai scan random"              # Uses -r flag
ai scan local"               # Uses -l flag
ai scan network"             # Uses -n flag
ai list wifi networks"       # Uses iwlist -l
```

---

## Troubleshooting

### "Command not recognized"

**Problem:** AI doesn't understand your request.

**Solutions:**
1. Be more specific: "show file" → "show me test.txt"
2. Use command name: "chmod test.txt to 755"
3. Try different wording: "display" instead of "show"

### "No target specified"

**Problem:** AI knows what command but not which file/IP.

**Solutions:**
1. Include the target: "scan 192.168.1.1" not just "scan"
2. Be explicit: "delete test.txt" not just "delete"

### "Permission denied"

**Problem:** You don't have rights to perform action.

**Solutions:**
1. Check if you're root: `whoami`
2. Escalate privileges if you have a shell
3. Use AI to escalate: "ai escalate to root"

### Wrong File Case

**Problem:** File not found because case is wrong.

**Example:**
```bash
ai show me MYFILE.TXT
# Looks for MYFILE.TXT but file is actually MyFile.txt
```

**Solution:** Use exact case:
```bash
ai show me MyFile.txt
```

### Command Did Something Unexpected

**Problem:** AI interpreted your request differently than intended.

**Solutions:**
1. Enable dry run first: `ai dry run on"`
2. Be more specific in your request
3. Use the exact command name if you know it

**Example of being more specific:**
```bash
# Ambiguous
ai remove permissions"  # Could mean chmod or rm!

# Clear
ai remove all permissions from test.txt"  # chmod
ai delete the file test.txt"              # rm
```

### AI is Too Slow

**Problem:** Commands take a long time.

**Causes:**
- Reading man pages (first time only)
- Complex operations (scanning networks)
- Waiting for user prompts

**Solutions:**
1. Disable prompts: `ai promptOnAmbiguous off"`
2. Use simple commands when possible
3. Be patient during network operations

---

## Examples Gallery

### Complete Workflows

#### Workflow 1: Scan and Exploit

```bash
# Step 1: Scan target
ai scan 192.168.1.1

# Step 2: Check what we found
# (AI shows open ports and services)

# Step 3: Exploit target
ai exploit 192.168.1.1"

# Step 4: Escalate privileges (if needed)
ai escalate to root"

# Step 5: Extract data
ai extract all data from router"
```

#### Workflow 2: File Management

```bash
# Step 1: Create a backup directory
ai create a directory called Backups"

# Step 2: Copy important files
ai copy important.txt to Backups/important_backup.txt"
ai copy data.txt to Backups/data_backup.txt"

# Step 3: Change permissions on backups
ai change permissions of Backups to 444"

# Step 4: Verify
ai list files in Backups"
```

#### Workflow 3: Network Reconnaissance

```bash
# Step 1: Scan local network
ai scan the local network"

# Step 2: Scan specific interesting hosts
ai scan 192.168.1.1 port 22"
ai scan 192.168.1.5 port 80"

# Step 3: Check for exploits
ai scan ssh on 192.168.1.1"
ai scan http on 192.168.1.5"

# Step 4: Exploit vulnerable services
ai exploit 192.168.1.1"
```

### Quick Reference

#### File Operations
```bash
ai show me test.txt"                       # View file
ai copy test.txt to backup.txt            # Copy
ai move test.txt to Documents"             # Move
ai delete test.txt                        # Delete
ai create an empty file called test.txt   # Create
```

#### Permissions
```bash
ai change permissions of test.txt to 755"  # chmod
ai change owner of test.txt to root"       # chown
ai change group of test.txt to admin"      # chgrp
ai chog guest test.txt"                    # chog
```

#### Searching
```bash
ai search for 'password' in config.txt"    # grep
ai find files named test.txt"              # find
ai locate all .txt files"                  # find
```

#### Networking
```bash
ai scan 192.168.1.1                       # scan IP
ai scan random"                            # scan -r
ai scan local"                             # scan -l
ai scan ssh on 192.168.1.1"                # es
ai show wifi networks"                     # iwlist
```

#### Exploitation
```bash
ai exploit 192.168.1.1"                    # Attack target
ai crack passwords"                        # Crack
ai escalate to root"                       # Escalate
ai extract email data"                     # Extract
```

#### Configuration
```bash
ai verbose mode on"                        # Verbose
ai dry run on"                             # Dry run
ai aggressive mode on"                     # Aggressive
ai stealth mode on"                        # Stealth
ai show config"                            # View config
```

### Real-World Scenarios

#### Scenario 1: Hack Into a Computer

**Goal:** Get shell access to 192.168.1.1

```bash
# Enable stealth to avoid detection
ai stealth mode on"

# Scan target
ai scan 192.168.1.1
# Output: Found SSH on port 22, HTTP on port 80

# Try exploiting SSH
ai scan ssh on 192.168.1.1"
# Output: Found vulnerability in SSH service

# Exploit it
ai exploit 192.168.1.1"
# Output: Shell obtained!

# Escalate to root
ai escalate to root"
# Output: Root shell obtained!

# Extract data
ai extract all data from router"
```

#### Scenario 2: Secure Your Files

**Goal:** Protect sensitive files

```bash
# Create secure directory
ai create a directory called SecureFiles"

# Move sensitive files
ai move passwords.txt to SecureFiles"
ai move secrets.txt to SecureFiles"

# Lock down permissions
ai change permissions of SecureFiles to 700"
# This means only you can access

# Change owner to root (if you're root)
ai change owner of SecureFiles to root"

# Verify
ai list files in SecureFiles"
```

#### Scenario 3: Network Mapping

**Goal:** Map all devices on local network

```bash
# Enable verbose mode for details
ai verbose mode on"

# Scan the network
ai scan the local network"
# Output: Found 5 hosts

# Scan each host
ai scan 192.168.1.1
ai scan 192.168.1.2"
ai scan 192.168.1.3"

# Check for exploits on interesting hosts
ai scan ssh on 192.168.1.1"
ai scan ftp on 192.168.1.2"
ai scan http on 192.168.1.3"

# Create report
ai create a file called network_map.txt"
# (manually add findings)
```

#### Scenario 4: Data Exfiltration

**Goal:** Extract data from compromised router

```bash
# Assuming you have router access

# Check what's available
ai list data on router"

# Extract emails
ai extract email data"

# Save to file
ai create a file called emails.txt"
# (data automatically saved)

# Extract passwords
ai extract password data"

# Extract banking info
ai extract bank information"

# Download everything
ai extract everything"
```

#### Scenario 5: Clean Up Tracks

**Goal:** Remove evidence after exploitation

```bash
# Enable dry run to see what would be deleted
ai dry run on"

# Delete logs
ai delete /var/log/auth.log"
ai delete /var/log/syslog"

# Verify dry run output looks good
# Then disable dry run
ai dry run off"

# Actually delete
ai delete /var/log/auth.log"
ai delete /var/log/syslog"

# Remove your user
ai delete user hacker"

# Clear command history
ai delete ~/.bash_history"
```

---

## Advanced Tips

### Chaining Commands

You can execute multiple AI commands in sequence:

```bash
ai scan 192.168.1.1 && ai exploit 192.168.1.1"
```

### Using Variables

Store results for later use:

```bash
TARGET="192.168.1.1"
ai scan $TARGET"
ai exploit $TARGET"
```

### Aliases

Create shortcuts for common AI commands:

```bash
alias aiscan='ai scan'
alias aiexploit='ai exploit'

# Usage
aiscan 192.168.1.1
aiexploit 192.168.1.1
```

### Scripting

Put AI commands in scripts:

```bash
#!/bin/bash
# auto_hack.sh

echo "Starting automated hack..."

ai scan 192.168.1.1
ai exploit 192.168.1.1"
ai escalate to root"
ai extract all data"

echo "Hack complete!"
```

---

## Tips for Success

### 1. Start Simple

Begin with basic commands:
- View files
- List directories
- Simple searches

Then progress to:
- Scanning
- Exploitation
- Data extraction

### 2. Use Dry Run

Before destructive operations:
```bash
ai dry run on"
ai delete important_file.txt"
# Check if this is what you want
ai dry run off"
```

### 3. Enable Verbose Mode

When learning:
```bash
ai verbose mode on"
```

This shows you:
- What the AI is doing
- Which commands are executed
- Detailed progress

### 4. Be Specific

**Vague:**
```bash
ai "scan"  # Scan what?
```

**Specific:**
```bash
ai scan 192.168.1.1
```

### 5. Save Your Work

After successful commands:
```bash
ai create a file called commands.txt
# Note: Manually save your command history
```

### 6. Read Output Carefully

The AI provides helpful information:
- Confirmation messages
- Error details
- Next step suggestions

### 7. Experiment Safely

Use non-critical files for testing:
```bash
ai create an empty file called test.txt
ai change permissions of test.txt to 777
ai delete test.txt
```

---

## Common Mistakes

### Mistake 1: Not Using Quotes for Complex Commands

**Most commands work fine without quotes:**
```bash
ai show me test.txt  # Works!
ai scan 192.168.1.1  # Works!
```

**But use quotes for complex write operations to be safe:**
```bash
ai "copy file with spaces.txt to backup folder/file.txt"
ai delete important file.txt
```

### Mistake 2: Wrong File Case

**Wrong:**
```bash
ai show me MYFILE.TXT
# But file is actually MyFile.txt
```

**Right:**
```bash
ai show me MyFile.txt
```

### Mistake 3: Missing Target

**Wrong:**
```bash
ai "scan"
# Error: No target specified
```

**Right:**
```bash
ai scan 192.168.1.1
```

### Mistake 4: Confusing Commands

**Wrong:**
```bash
ai remove permissions"
# Unclear: Delete file or remove permissions?
```

**Right:**
```bash
ai remove all permissions from test.txt"  # chmod
ai delete the file test.txt"              # rm
```

### Mistake 5: Not Checking Before Deleting

**Wrong:**
```bash
ai delete *.txt"
# Deletes ALL .txt files!
```

**Right:**
```bash
ai dry run on"
ai delete *.txt"
# Check what would be deleted
ai dry run off"
# Then delete if okay
```

---

## Getting Help

### Ask the AI

```bash
ai help
ai what commands are available?"
ai how do I use scan?"
ai explain chmod
```

### Check Configuration

```bash
ai show config"
ai display current settings"
```

### Enable Debug Mode

```bash
ai debug mode on"
# Run your problematic command
ai show me test.txt"
# Look at debug output for clues
```

### Read Error Messages

The AI provides helpful error messages:

```
Agent: No target specified for scan
```

This tells you: You need to specify what to scan!

```
Agent: File not found: test.txt
```

This tells you: The file doesn't exist or wrong case!

---

## Keyboard Shortcuts

### Command History

Use arrow keys to recall previous commands:
- ↑ (Up Arrow): Previous command
- ↓ (Down Arrow): Next command

### Tab Completion

Some shells support tab completion:
```bash
ai show me tes<TAB>"
# Completes to: ai show me test.txt"
```

### Cancel Command

Press `Ctrl+C` to cancel a running command.

---

## Best Practices

### 1. Security

- Use stealth mode when hacking
- Clean up logs after exploitation
- Don't leave obvious traces

### 2. Organization

- Create folders for different projects
- Use descriptive filenames
- Back up important data

### 3. Efficiency

- Learn common patterns
- Use dry run for complex commands
- Enable verbose when debugging

### 4. Safety

- Test on non-critical files first
- Always backup before destructive operations
- Understand what a command does before running it

---

## Conclusion

You now know everything you need to use X's AI Agent effectively!

**Remember:**
1. Use natural language
2. Be specific with targets
3. Check output carefully
4. Use dry run for destructive operations
5. Enable verbose when learning

**Start with simple commands and gradually work up to complex operations.**

### Quick Start Checklist

- [ ] Try viewing a file: `ai show me test.txt"`
- [ ] Try copying a file: `ai copy test.txt to backup.txt`
- [ ] Try scanning: `ai scan local"`
- [ ] Configure settings: `ai verbose mode on"`
- [ ] Read this handbook again when stuck

**Good luck hacking!** 🚀

---

**Document Version:** 2.0  
**AI System Version:** 0.9.7.3  
**Last Updated:** March 2026

For technical details, see the [AI Developer Handbook](ai_developer_handbook.md).
