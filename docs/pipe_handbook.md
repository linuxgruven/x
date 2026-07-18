# Pipe Command Reference

Unix-style pipe chain functionality and text processing commands for data filtering, transformation, and analysis.

## Table of Contents
- [Overview](#overview)
- [Pipe Variables](#pipe-variables)
- [Pipe Chain Syntax](#pipe-chain-syntax)
- [Calculator (bc)](#calculator-bc)
- [Text Search (grep)](#text-search-grep)
- [Stream Editor (sed)](#stream-editor-sed)
- [Pattern Processing (awk)](#pattern-processing-awk)
- [Sorting and Deduplication](#sorting-and-deduplication)
- [String Manipulation](#string-manipulation)
- [File Operations](#file-operations)
- [Process Listing (ps)](#process-listing-ps)
- [Word Counting (wc)](#word-counting-wc)
- [Field Extraction (cut)](#field-extraction-cut)
- [Character Translation (tr)](#character-translation-tr)
- [Head and Tail](#head-and-tail)
- [Build Command Lines (xargs)](#build-command-lines-xargs)
- [Complex Pipeline Examples](#complex-pipeline-examples)

## Overview

The pipe system allows chaining multiple commands together using the `|` operator. Each command processes the output from the previous command, enabling powerful data transformation workflows.

### Available Commands

| Command | Purpose |
|---------|---------|
| `bc` | Calculator with math functions |
| `cat` | Display file contents |
| `grep` | Search text patterns |
| `ls` | List directory contents |
| `ps` | List running processes |
| `sed` | Find and replace text |
| `awk` | Field extraction and processing |
| `sort` | Sort lines |
| `uniq` | Remove duplicates |
| `wc` | Count words, lines, characters |
| `cut` | Extract columns/fields |
| `trim` | Remove whitespace |
| `tr` | Translate characters |
| `rev` | Reverse strings |
| `split` | Split strings into arrays |
| `join` | Join arrays into strings |
| `head` | Display first N lines or bytes |
| `tail` | Display last N lines or bytes |
| `echo` | Print text |
| `nslookup` | DNS hostname lookup |
| `find` | Search for files |
| `xargs` | Build and run command lines from stdin |
| `xc` | Copy to clipboard |
| `decipher` | Decode text |
| `set` | Store variables |
| `env` | List/show/clear variables |
| `unset` | Remove variables |
| `debug` | Toggle debug output |

## Pipe Variables

Store and reuse data across pipe commands using bash-like variable syntax.

### Variable Assignment

```bash
# Direct assignment
set VAR value               # Store value in VAR
set NUM 42                  # Store number
set NAME "John Doe"         # Store string with spaces

# Capture from pipe
cat file.txt | set CONTENT  # Store entire file
echo "5 * 2" | bc | set N   # Store calculation result
cat /etc/passwd | wc -l | set COUNT  # Store line count
```

### Variable Expansion

```bash
# Basic expansion
echo "$VAR"                 # Expand variable
echo "Value: $NUM"          # Expand in string context

# Braces for word boundaries
set NUM 42
echo "${NUM}nd place"       # Outputs: "42nd place"
echo "$NUMnd place"         # Would look for $NUMnd, fail

# Multiple variables
set X 10 | set Y 20 | echo "$X + $Y"  # Outputs: "10 + 20"
```

### Variable Management

```bash
# List all variables
env                         # Show all stored variables
env                         # Output: VAR=value, NUM=42, etc.

# Show specific variable
env VAR                     # Display value of VAR

# Alternative set syntax
env VAR=value               # Set using env command

# Remove variable
unset VAR                   # Delete VAR from storage

# Clear all variables
env -c                      # Remove all stored variables
```

### Debug Mode

```bash
# Enable debug output (shows variable expansion and pipe flow)
debug on                    # Turn on yellow debug messages

# Disable debug output
debug off                   # Turn off debug messages

# Check status
debug status                # Show current debug state
```

### Variable Examples

```bash
# Simple math
set NUM 5 | echo "$NUM * 2" | bc | set RESULT | echo "Result: $RESULT"
# Output: Result: 10

# Extract root password hash
cat /etc/passwd | grep "^root:" | cut -d: -f2 | set ROOTHASH
echo "Hash: $ROOTHASH"

# Count and display
cat /etc/passwd | wc -l | set COUNT | echo "Found $COUNT users"

# Store multiple lines
cat /etc/passwd | cut -d: -f1 | set USERS
echo "$USERS"
# Output: (all usernames, one per line)

# Complex calculations
set A 3 | set B 4
echo "($A * $A) + ($B * $B)" | bc | set C
echo "Result: $C"
# Output: Result: 25

# Reusing variables
set IP "192.168.1.1"
echo "Ping $IP" | cat /etc/hosts | grep "$IP"
```

### Variable Persistence

Variables persist across commands until explicitly cleared:
- Available throughout session
- Survive across multiple pipe chains
- Persist across pivots
- Clear with `env -c` or `unset VAR`
- Reset on session restart

## Pipe Chain Syntax

data | command1 args | command2 args | command3 args

- Data flows through the pipe from left to right
- Each command processes output from the previous command
- Final command returns the processed result
- All commands must be connected with pipes (|)

### Basic Examples

# Simple pipe: read file and count lines
cat /etc/passwd | wc -l

# Three-stage pipe: read, filter, count
cat access.log | grep "error" | wc -l

# Filter and sort
ls | grep ".txt" | sort

## Calculator (bc)

Powerful calculator with arithmetic operations, mathematical functions, and special features.

### Arithmetic Operations

# Basic arithmetic
echo "5 + 3" | bc  # 8
echo "10 - 4" | bc # 6
echo "7 * 6" | bc  # 42
echo "20 / 4" | bc # 5
echo "17 % 5" | bc # 2 (modulo/remainder)
echo "2 ^ 8" | bc  # 256 (power)

# Order of operations (follows PEMDAS)
echo "5 + 3 * 2" | bc      # 11 (multiplication first)
echo "2 + 3 * 4 - 5" | bc  # 9
echo "10 / 2 + 3" | bc     # 8

### Mathematical Functions

# Square root
echo sqrt 16 | bc  # 4
echo sqrt 2 | bc   # 1.414214

# Absolute value
echo abs -5 | bc   # 5
echo abs 3.7 | bc  # 3.7

# Rounding functions
echo floor 3.7 | bc  # 3
echo ceil 3.2 | bc   # 4
echo round 3.5 | bc  # 4
echo round 3.4 | bc  # 3

# Sign function
echo sign -5 | bc  # -1
echo sign 0 | bc   # 0
echo sign 10 | bc  # 1

### Trigonometric Functions

# Basic trig (radians)
echo sin 0 | bc  # 0
echo cos 0 | bc  # 1
echo tan 0 | bc  # 0

# Pi constant
echo sin pi | bc  # ~0 (sin(π))
echo cos pi | bc  # -1 (cos(π))

# Inverse trig
echo asin 0.5 | bc  # 0.523599 (π/6)
echo acos 0 | bc    # 1.5708 (π/2)
echo atan 1 | bc    # 0.785398 (π/4)

### Utility Functions

# Sum of numbers
echo sum 1 2 3 4 5 | bc  # 15

# Random numbers
echo rnd | bc     # Random 0-1
echo rnd 10 | bc  # Random 0-10

# Range generation
echo range 5 | bc       # [0, 1, 2, 3, 4]
echo range 2 7 | bc     # [2, 3, 4, 5, 6, 7]
echo range 0 10 2 | bc  # [0, 2, 4, 6, 8, 10]

### Character Conversions

# ASCII code to character
echo char 65 | bc      # [ A ]
echo char 72 105 | bc  # [ Hi ]

# Character to ASCII code
echo code A | bc      # [ 65 ]
echo code Hello | bc  # [ 72, 101, 108, 108, 111 ]

### Chained Calculations

# Comma-separated chain: (10 + 5) * 2 - 3
echo "10 + 5, * 2, - 3" | bc  # 27

# Multi-step calculation
echo "100 / 4, sqrt" | bc  # 5 (sqrt(25))
echo "2 ^ 4, + 10" | bc    # 26 (16 + 10)

### Special Features

# Random IP address generation
echo ip | bc    # 192.168.1.45
echo ip 5 | bc  # Generate 5 random IPs

## Text Search (grep)

Search for patterns in text with various options.

### Basic Search

# Find lines containing "error"
cat /var/log/system.log | grep "error"

# Find lines containing "root" in passwd file
cat /etc/passwd | grep "root"

# Search in file directly
cat /home/user/notes.txt | grep "TODO"

### Case-Insensitive Search

# -i flag for case-insensitive
cat file.txt | grep -i "warning"
cat log.txt | grep -i "error"

# Matches: ERROR, error, Error, ErRoR
cat system.log | grep -i "error"

### Inverted Match (Exclude)

# -v flag to exclude matches
cat file.txt | grep -v "debug"
cat /etc/passwd | grep -v "nologin"

# Show all non-comment lines
cat config.conf | grep -v "^#"

### Combined Flags

# Case-insensitive exclusion
cat log.txt | grep -iv "debug"

# Multiple grep stages
cat file.txt | grep "error" | grep -v "ignore"

### Practical Examples

# Find all .txt files
ls | grep ".txt"

# Find all error logs except debug
cat system.log | grep "error" | grep -v "debug"

# Find IP addresses in log
cat access.log | grep -E "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"

# Find users with bash shell
cat /etc/passwd | grep "/bin/bash"

## Stream Editor (sed)

Find and replace text in streams.

### Basic Substitution

# Replace first occurrence
echo "hello world" | sed "s/world/universe/"
# Output: hello universe

# Replace all occurrences (g flag)
cat file.txt | sed "s/old/new/g"

# Replace in file
cat config.txt | sed "s/localhost/192.168.1.1/g"

### Practical Examples

# Fix common typos
cat document.txt | sed "s/teh/the/g"

# Update error status
cat log.txt | sed "s/ERROR/FIXED/"

# Replace multiple spaces with single space
cat data.txt | sed "s/  */ /g"

# Remove leading/trailing spaces (simplified)
cat file.txt | sed "s/^ *//"  # Leading
cat file.txt | sed "s/ *$//"  # Trailing

# Change domain in URLs
cat links.txt | sed "s/oldsite.com/newsite.com/g"

# Redact passwords
cat config.txt | sed "s/password=.*/password=REDACTED/g"

### Combined with Other Commands

# Find and replace, then save
cat config.txt | sed "s/debug=true/debug=false/" > new_config.txt

# Replace in filtered results
cat log.txt | grep "user" | sed "s/username/user_id/g"

## Pattern Processing (awk)

Extract and process fields from structured text.

### Field Extraction

# Print first field (default delimiter: space)
echo "one two three" | awk '{print $1}'
# Output: one

# Print second field
echo "one two three" | awk '{print $2}'
# Output: two

# Print last field ($NF = Number of Fields)
echo "one two three" | awk '{print $NF}'
# Output: three

# Print entire line ($0)
echo "hello world" | awk '{print $0}'
# Output: hello world

### Custom Delimiters

# Use colon as delimiter
cat /etc/passwd | awk -F: '{print $1}'
# Prints usernames (first field)

# CSV processing
cat data.csv | awk -F, '{print $1}'
# Print first column

# Custom delimiter with -F flag
echo "a:b:c:d" | awk -F: '{print $2}'
# Output: b

# Tab-delimited
cat data.tsv | awk -F"\t" '{print $1 $3}'

### Multiple Fields

# Print multiple fields
cat /etc/passwd | awk -F: '{print $1, $2}'
# Print username and password hash

# Fields with custom separator
echo "a b c d" | awk '{print $1, $3}'
# Output: a c

# Combine fields
cat data.csv | awk -F, '{print $1 "-" $2}'

### Field Count

# Print number of fields
echo "one two three four" | awk '{print NF}'
# Output: 4

# Use NF to get last field
echo "a b c d e" | awk '{print $NF}'
# Output: e

### Practical Examples

# Extract usernames from passwd
cat /etc/passwd | awk -F: '{print $1}'

# Get LAN IPs from random nmap scan
nmap -r | awk '{print $5}'

# Extract port numbers from nmap
nmap 192.168.1.1 | awk '{print $1}'

# Extract file names from ls -l (field 3: permissions size filename)
ls -l | awk '{print $3}'

# Process CSV: extract name and email
cat users.csv | awk -F, '{print $1 $3}'

# Get second column from space-separated data
cat data.txt | awk '{print $2}'

# Print first and last fields
echo "start middle1 middle2 end" | awk '{print $1 $NF}'
# Output: start end

# Combine nmap with awk field extraction
nmap -r | awk '{print $5}' | awk -F: '{print $1}'
# Scans random IP, extracts LAN addresses

## Sorting and Deduplication

### Sort Command

# Alphabetical sort
cat names.txt | sort

# Reverse alphabetical sort
cat names.txt | sort -r

# Numeric sort
cat numbers.txt | sort -n
# Example input: 10, 2, 100
# Alphabetical: 10, 100, 2
# Numeric (-n): 2, 10, 100

# Numeric reverse sort
cat scores.txt | sort -rn

### Unique Command

# Remove consecutive duplicates
cat file.txt | uniq

# Count occurrences
cat file.txt | uniq -c

# Case-insensitive deduplication
cat file.txt | uniq -i

### Combined Sort and Unique

# Sort and remove duplicates
cat names.txt | sort | uniq

# Sort, deduplicate, and count
cat log.txt | sort | uniq -c

# Numeric sort with deduplication
cat numbers.txt | sort -n | uniq

# Find most common entries
cat access.log | sort | uniq -c | sort -rn

### Practical Examples

# Sort usernames
cat /etc/passwd | awk -F: '{print $1}' | sort

# List unique IPs from log
cat access.log | awk '{print $1}' | sort | uniq

# Top 10 most common errors
cat error.log | grep "ERROR" | sort | uniq -c | sort -rn | head -10

# Alphabetize and deduplicate list
cat email_list.txt | sort | uniq > clean_list.txt

## String Manipulation

### Reverse (rev)

# Reverse a string
echo "hello" | rev
# Output: olleh

# Reverse each line
echo "hello world" | rev
# Output: dlrow olleh

# Reverse file contents line by line
cat file.txt | rev

### Split Command

# Split by space (default)
echo "one two three" | split
# Output: [one, two, three]

# Split by custom delimiter
echo "a,b,c,d" | split ,
# Output: [a, b, c, d]

# Split by colon
echo "name:email:phone" | split :
# Output: [name, email, phone]

# Split CSV
echo "red,green,blue" | split ,
# Output: [red, green, blue]

### Join Command

# Join with space (default)
echo ["hello", "world"] | join
# Output: hello world

# Join with custom delimiter
echo ["a", "b", "c"] | join -
# Output: a-b-c

# Join with comma
echo ["red", "green", "blue"] | join ,
# Output: red,green,blue

# Join with empty string
echo ["h", "e", "l", "l", "o"] | join ""
# Output: hello

### Trim Command

# Remove leading and trailing whitespace
echo "  hello  " | trim
# Output: hello

# Trim multiple lines
cat file.txt | trim

# Trim in pipeline
cat data.txt | grep "value" | trim

### Practical Examples

# Split CSV and process
cat data.csv | split , | awk '{print $1}'

# Reverse and rejoin
echo "hello world" | split | rev | join " "

# Clean and join list
cat items.txt | trim | sort | join ", "

## File Operations

### Cat Command

# Display file contents
cat /etc/passwd | wc -l

# Cat with pipe
cat file.txt | grep "error"

# Multiple operations
cat log.txt | grep "warning" | wc -l

### Ls Command

# List current directory (standalone uses Command.ls)
ls
ls /home
ls /etc

# Pipe ls to enable flag support (uses Pipe.ls)
# Long format (-l): shows permissions, size, filename
# Format: 3 fields - $1=permissions, $2=size, $3=filename
ls -l | cat
ls -l /var/log | cat

# Show all files (-a): includes hidden files starting with .
ls -a | cat
ls -a /home/user | cat

# Human-readable sizes (-h): displays sizes as K, M, G
ls -lh | cat
ls -lh /var/log | cat

# Combined flags (requires piping to use Pipe.ls)
ls -la | cat      # Long format with all files
ls -lah | cat     # Long format, all files, human-readable
ls -lh /var | cat # Long format with human sizes for /var

# List and filter with grep
ls | grep ".txt"
ls /etc | grep "conf"
ls -l | grep "log"

# List and count
ls | wc -l
ls /var/log | grep ".log" | wc -l

# List and sort
ls | sort
ls -l | sort

# List to file (redirection)
ls > filelist.txt
ls -la >> directory_contents.txt

### Find Command

# Find files by name
find /home -name "*.txt" | wc -l

# Find and process
find . -type f | grep ".log"

# Find and count
find /var/log -name "*.log" | wc -l

# Find specific files
find . -name "config.conf" | wc -l

### Echo Command

# Print text
echo "hello world" | wc -w

# Echo and process
echo "test string" | grep "test"

# Echo to file (redirection, not pipe)
echo "log entry" >> log.txt

# Echo list
echo ["a", "b", "c"] | join ,

### Nslookup Command

# Lookup hostname
echo "example.com" | nslookup
# Returns IP address

# Process list of hostnames
cat domains.txt | nslookup

# Lookup and save results
echo "google.com" | nslookup > ip.txt

## Process Listing (ps)

List running processes on the computer in a format suitable for pipe processing.

### Basic Usage

# List all processes
ps

# Output format: USER PID CPU% MEM% COMMAND
# Example: root 1234 5.2% 12.3% /bin/sshd

### Filter by User

# Show only root's processes
ps -u root

# Show specific user's processes
ps -u guest

# Count root's processes
ps -u root | wc -l

### Filter by Command

# Show processes with "sshd" in command name
ps -C sshd

# Show all bash processes
ps -C bash

# Show Python processes
ps -C python

### Combined Filters

# Show root's bash processes
ps -u root -C bash

# Show guest's Python processes
ps -u guest -C python | wc -l

### Process Analysis with Pipes

# Count total running processes
ps | wc -l

# Find specific process
ps | grep "nginx"

# List all process commands
ps | awk '{print $5}'

# Show non-root processes
ps | grep -v "root"

# Extract PIDs only
ps | awk '{print $2}'

# Show processes sorted by user
ps | sort

# Count processes by command type
ps | awk '{print $5}' | sort | uniq -c

### Common Use Cases

# Monitor specific service
ps -C apache2 | wc -l

# Check if process is running
ps | grep "mysql"

# List all user processes
ps | grep -v "root" | wc -l

# Get process statistics
ps -u root | wc -l
ps -u guest | wc -l

# Export process list
ps > processes.txt

# Filter and save
ps -u root > root_processes.txt

## Word Counting (wc)

### Line Count

# Count lines
cat file.txt | wc -l

# Count matching lines
cat log.txt | grep "error" | wc -l

# Count files
ls | wc -l

# Count users
cat /etc/passwd | wc -l

### Word Count

# Count words
cat file.txt | wc -w

# Count words in string
echo "hello world test" | wc -w
# Output: 3

# Count words after filtering
cat document.txt | grep "chapter" | wc -w

### Character Count

# Count characters
cat file.txt | wc -c

# Count characters in string
echo "hello" | wc -c
# Output: 5

# Count filtered characters
cat file.txt | grep "error" | wc -c

### Practical Examples

# Count error occurrences
cat system.log | grep -i "error" | wc -l

# Count unique users
cat access.log | awk '{print $1}' | sort | uniq | wc -l

# Total word count in all files
cat *.txt | wc -w

# Count non-comment lines
cat script.src | grep -v "^//" | wc -l

## Field Extraction (cut)

### Column Extraction

# Extract first column (default delimiter: tab)
cat data.txt | cut -f1

# Extract column from CSV
cat data.csv | cut -d, -f1

# Extract multiple columns
cat data.csv | cut -d, -f1,3

# Extract range of columns
cat data.csv | cut -d, -f2-4

### Character Extraction

# Extract first 10 characters
cat file.txt | cut -c1-10

# Extract characters 5 to 15
cat file.txt | cut -c5-15

# Extract from position to end
cat file.txt | cut -c10-

### Practical Examples

# Extract usernames (first field, colon delimiter)
cat /etc/passwd | cut -d: -f1

# Extract IP addresses (first field, space delimiter)
cat access.log | cut -d" " -f1

# Extract date from log
cat log.txt | cut -c1-10

# Extract email domain
cat emails.txt | cut -d@ -f2

# Get filename from path
echo "/home/user/file.txt" | cut -d/ -f4

## Character Translation (tr)

### Character Replacement

# Replace characters
echo "hello" | tr "e" "a"
# Output: hallo

# Multiple character replacement
echo "hello" | tr "el" "ax"
# Output: haxxo

# Replace spaces with underscores
echo "hello world" | tr " " "_"
# Output: hello_world

### Case Conversion

# Lowercase to uppercase
echo "hello" | tr "a-z" "A-Z"
# Output: HELLO

# Uppercase to lowercase
echo "HELLO" | tr "A-Z" "a-z"
# Output: hello

# Mixed case
echo "Hello World" | tr "A-Z" "a-z"
# Output: hello world

### Practical Examples

# Convert DOS to Unix line endings
cat dosfile.txt | tr -d "\r"

# Remove all numbers
cat file.txt | tr -d "0-9"

# Replace all vowels
echo "hello world" | tr "aeiou" "*****"
# Output: h*ll* w*rld

# Clean up filenames (spaces to underscores)
echo "my file name.txt" | tr " " "_"
# Output: my_file_name.txt

## Head and Tail

Display first or last N lines/bytes from input.

### Head Command

# Display first N lines
cat file.txt | head -n 5
# Show first 5 lines

echo ["line1", "line2", "line3", "line4", "line5"] | head -n 3
# Output: ["line1", "line2", "line3"]

# Display first N bytes
cat file.txt | head -c 100
# Show first 100 bytes

# Default shows first 10 lines
cat log.txt | head
# Show first 10 lines

### Tail Command

# Display last N lines
cat file.txt | tail -n 5
# Show last 5 lines

echo ["line1", "line2", "line3", "line4", "line5"] | tail -n 2
# Output: ["line4", "line5"]

# Skip first N lines with +NUM syntax
cat data.csv | tail -n +2
# Show from line 2 onwards (skip header)

# Display last N bytes
cat file.txt | tail -c 100
# Show last 100 bytes

# Show from byte N to end with +NUM syntax
cat file.txt | tail -c +50
# Show from byte 50 to end

# Default shows last 10 lines
cat log.txt | tail
# Show last 10 lines

### Practical Examples

# Remove CSV header
cat data.csv | tail -n +2 | head -n 10
# Skip first line, show next 10

# Process list without header
ps | tail -n +2 | sort
# Remove ps header, sort remaining

# Get middle section
cat file.txt | head -n 50 | tail -n 10
# Lines 41-50

# Extract specific byte range
cat binary.dat | tail -c +100 | head -c 50
# Bytes 100-149

# Sample first entries from each section
cat log.txt | grep "ERROR" | head -n 5
# First 5 errors

# Show last few entries
cat access.log | grep "404" | tail -n 10
# Last 10 404 errors

## Build Command Lines (xargs)

Reads stdin, splits it on a delimiter (newline by default), and runs a target command once per chunk with those items appended as arguments. Lets any single-target command operate on a list without writing a script.

### Options

| Option | Description |
|--------|-------------|
| `-n N` | Pass N items per invocation. `-n 1` runs CMD once per line. Default: all items in one call. |
| `-I PH` | Replace each occurrence of `PH` in INITIAL-ARGS with the input item. Implies `-n 1`. Plain literal substitution (not regex). |
| `-d DELIM` | Use DELIM (single char) as input separator instead of newline. |
| `-t` | Trace: print each command before running it. |

### Behaviour

- The target CMD must be a known X command in the current shell's command table (X commands, builtins, aliases). Pipe-builtins like `set`/`env`/`echo` and bash scripts (`@name`) are not resolvable from xargs.
- Empty and whitespace-only lines are skipped.
- Output from every invocation is collected and forwarded to the next pipe stage (or printed if xargs is the last stage).
- Capped at 5000 items to prevent runaway loops. Press `q` to abort during long runs.
- Refuses to recurse into itself (`xargs xargs ...` is rejected).

### Examples

# Scan each IP one at a time
cat ips.txt | xargs -n1 scan

# Rename in place using a placeholder
ls *.log | xargs -I{} mv {} {}.old

# Bulk delete files matched by find
find /tmp -name "*.bak" | xargs rm

# Trace what xargs is about to run
ls *.enc | xargs -n1 -t decipher

# Chain xargs output into another stage
cat hosts.txt | xargs -n1 dig | grep -v "no route"

# Custom delimiter (comma-separated input)
echo "a,b,c" | xargs -d , -n1 echo

## Complex Pipeline Examples

### Log Analysis

# Find unique error IPs and count them
cat access.log | grep "error" | awk '{print $1}' | sort | uniq -c | sort -rn

# Extract failed login attempts
cat auth.log | grep "Failed password" | awk '{print $11}' | sort | uniq -c

# Top 10 most accessed pages
cat access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -n 10

# Recent errors from large log (skip old entries)
cat huge.log | tail -n 10000 | grep "ERROR" | tail -n 50

# Process data without headers
cat report.csv | tail -n +2 | awk -F, '{print $1}' | sort | uniq

### Data Processing

# Extract and clean email list
cat contacts.txt | grep "@" | cut -d, -f2 | trim | sort | uniq

# Calculate average from numbers
cat numbers.txt | awk '{sum+=$1} END {print sum/NR}'

# Filter, extract, and count
cat data.csv | grep -v "^#" | cut -d, -f3 | sort -n | uniq -c

### File Management

# Find large log files
find /var/log -name "*.log" | xargs ls -lh | grep "M"

# Count source files excluding tests
find . -name "*.src" | grep -v test | wc -l

# List duplicate filenames
find . -type f | awk -F/ '{print $NF}' | sort | uniq -d

### Text Processing

# Extract emails and domains
cat file.txt | grep -o "[a-z]*@[a-z]*\.[a-z]*" | cut -d@ -f2 | sort | uniq

# Clean and format list
cat raw_list.txt | trim | sort | uniq | awk '{print "- " $0}'

# Process multi-column data
cat data.txt | awk '{print $1 "," $3}' | sort | sed "s/,/ -> /g"

### Combined Operations

# Extract, filter, transform, and count
cat /etc/passwd | cut -d: -f1 | grep -v "^#" | sort | wc -l

# Multi-stage text transformation
cat input.txt | tr "A-Z" "a-z" | sed "s/old/new/g" | sort | uniq

# Complex log analysis
cat access.log | grep "POST" | awk '{print $1}' | sort | uniq -c | sort -rn | head -20

# Data validation pipeline
cat data.csv | grep -v "^$" | cut -d, -f1-3 | trim | sort | uniq > clean_data.csv

## Output Redirection

### Write to File

# Overwrite file
cat input.txt | grep "error" > errors.txt

# Append to file (cat still uses pipe internally)
cat new_log.txt | cat >> main_log.txt

# Save processed results
cat data.txt | sort | uniq > unique_data.txt

### Clipboard Operations

# Copy to clipboard
cat file.txt | xc

# Copy filtered results
cat log.txt | grep "error" | xc

# Copy processed data
cat list.txt | sort | uniq | xc

## Tips and Best Practices

1. **Start Simple**: Build pipes incrementally, testing each stage
2. **Use grep -v**: Exclude unwanted lines before processing
3. **Sort Before uniq**: `uniq` only removes consecutive duplicates
4. **Check Field Numbers**: Use `awk '{print NF}'` to count fields
5. **Test Regex**: Verify patterns with simple grep before complex pipes
6. **Use -n for Numbers**: Sort numeric data with `sort -n`
7. **Trim Data**: Use `trim` to clean whitespace before processing
8. **Redirect Output**: Save results with `>` or `>>`
9. **Count Results**: End pipes with `wc -l` to count matches
10. **Debug Pipes**: Remove stages from end to isolate issues

## Common Patterns

# Filter, extract, deduplicate
cat file.txt | grep "pattern" | awk '{print $2}' | sort | uniq

# Count unique values
cat data.txt | awk '{print $1}' | sort | uniq | wc -l

# Top N most common
cat file.txt | sort | uniq -c | sort -rn | head -10

# Clean and save
cat raw.txt | trim | sort | uniq > clean.txt

# Multi-field extraction
cat data.csv | cut -d, -f1,3 | sort

# Case-insensitive deduplication
cat list.txt | tr "A-Z" "a-z" | sort | uniq

## Error Handling

- Empty results return `[]`
- Invalid commands return Error objects
- File not found returns `[]`
- Permission denied returns `[]`
- Invalid regex patterns fail silently

## Performance Considerations

- Large files: Use grep to filter early in pipeline
- Memory usage: Avoid loading entire files when possible
- Sorting: Can be expensive on large datasets
- Regex: Complex patterns slow down grep
- Field extraction: awk is efficient for structured data