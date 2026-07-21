# Bash Script Execution System - Complete Feature Guide

## Table of Contents

1. [Overview](#overview)
2. [Command Reference](#command-reference)
3. [Getting Started](#getting-started)
4. [Comments](#comments)
5. [Variables](#variables)
6. [Arithmetic & Operators](#arithmetic--operators)
7. [Conditionals](#conditionals)
8. [Loops](#loops)
9. [Switch/Case Statements](#switchcase-statements)
10. [Loop Control](#loop-control)
11. [Error Handling (Try/Catch)](#error-handling-trycatch)
12. [Functions](#functions)
13. [Array Operations](#array-operations)
14. [Built-in Functions](#built-in-functions)
15. [Maps & JSON](#maps--json)
16. [Type Casting](#type-casting)
17. [Typed Input Prompts](#typed-input-prompts)
18. [System & File Commands](#system--file-commands)
19. [GreyHack Network Commands](#greyhack-network-commands)
20. [Advanced Features](#advanced-features)
21. [Best Practices](#best-practices)
22. [Troubleshooting](#troubleshooting)
23. [Appendix: Complete Tutorial Script](#appendix-complete-tutorial-script)

---

## Overview

The Bash Script Execution System is a production-ready scripting interpreter for GreyHack that provides:

- **Structured Control Flow**: if/elif/else, for, while, until, switch/case
- **User-Defined Functions**: With parameters, recursion support, and local scope
- **Dynamic Variables**: Automatic type handling for strings, numbers, lists, and maps
- **Array Operations**: push, pop, pull with full list manipulation
- **Built-in Functions**: String manipulation, math operations, file testing, and more
- **Network Commands**: Port scanning, LAN discovery, router introspection
- **Type Safety**: Typed input prompts and type casting functions

---

## Command Reference

### Control Flow Commands

```bash
if <condition>              # Start conditional block
elif <condition>            # Else-if condition
else                        # Else block
endif                       # End conditional

for <var> in <list>         # For loop with list
for <var> in range(s,e)     # For loop with range
while <condition>           # While loop
until <condition>           # Until loop
endfor                      # End for loop
endwhile                    # End while loop
enduntil                    # End until loop

switch <value>              # Switch statement
case <value>                # Case block
default                     # Default case
endswitch                   # End switch

break                       # Exit loop
continue                    # Skip to next iteration

try                         # Start error-handling block
catch [var]                 # Catch errors (optionally bind to variable)
endtry                      # End try/catch block (end try also works)
_throw <message>            # Throw an error from inside try block
```

### Built-in Variables

These variables are automatically available in all bash scripts. They update
automatically after a pivot (proxy/ssh). Access properties via `_setvar`.

```bash
COMPUTER                    # Current computer object
COMPUTER.local_ip           # Computer LAN IP
COMPUTER.public_ip          # Computer public IP
COMPUTER.active_net_card    # WIFI or ETHERNET
COMPUTER.get_name           # Hostname
COMPUTER.get_ports          # List of active ports
COMPUTER.is_network_active  # 1 if connected, 0 if not
COMPUTER.network_devices    # Network interface info
COMPUTER.network_gateway    # Gateway IP
COMPUTER.show_procs         # Active processes
SHELL                       # Current shell object
SHELL.host_computer         # Shell's host computer
ROOT                        # Root filesystem file object
ROOT.path                   # Root path
ROOT.name                   # File/folder name
ROOT.permissions            # Permission string
ROOT.owner                  # File owner
ROOT.group                  # File group
ROOT.size                   # File size
ROOT.is_folder              # 1 if folder, 0 if file
ROOT.is_binary              # 1 if binary, 0 if not
ROOT.is_symlink             # 1 if symlink, 0 if not
ROOT.parent                 # Parent folder (file object)
ROOT.allow_import           # 1 if importable binary
ROOT.get_content            # File content as string
ROOT.get_files              # List of files in folder
ROOT.get_folders            # List of folders in folder
ROOT.delete                 # Delete the file (returns empty string on success)
```

**Usage:**
```bash
// Store a property and print it
_setvar(ip, COMPUTER.local_ip)
_print cyan(LAN:) _getvar(ip)

// Chain through SHELL to computer
_setvar(host, SHELL.host_computer.get_name)
_print Hostname: _getvar(host)

// Iterate root folders with colors
_setvar(dirs, ROOT.get_folders)
for d in dirs
  _setvar(name, _getvar(d).name)
  _setvar(perms, _getvar(d).permissions)
  _print liteblue(_getvar(perms)) _getvar(name)
endfor
```

### Variable Commands

```bash
_setvar(name, value)        # Set variable
_getvar(name)               # Get variable value
_len name                # Get array length
_in array value          # Check if value in array
_push array value        # Add to end of array
_pop array               # Remove from end of array
_pull array              # Remove from start of array
```

### Function Commands

```bash
func name(params)           # Define function
endfunc                     # End function
_return value               # Return value from function (inside func body only)
// Note: _return returns a value FROM a function; "return" exits the whole script
```

### System Commands

```bash
_print <text>           # Print output (buffered)
_printnow <text>       # Print output (immediate)
_fs_read <path>            # Read file content
_fs_view <path>            # View file content
_fs_write <path> <text>    # Write to file
_fs_mkdir <path>           # Create directory
_fs_cd <path>              # Change directory
_fs_pwd                    # Print working directory
_sys_whoami                 # Get current username
_sys_whatami                # Get execution context
_fs_find <path> <pattern>  # Find files/content (use -c for content search, -e for exact match)
_home                   # Return to home shell (safe exit, unwinds all sessions)
_fs_put <local> <remote>   # Upload file via scp to remote shell
_fs_get <remote> <local>   # Download file via scp from remote shell
_sleep <seconds>            # Wait/pause execution (min 0.01, max 300)
pause                       # Wait for user to press Enter
;							# Command separator (always runs both sides)
&&							# Conditional AND (runs right side only if left succeeded)
_exit <code>                # Exit script with code (non-zero prints error)
return [message]            # Exit script early; optional message can be a command to run
_hold                       # Store current held object (from scanner/headless ops)
_setvar(name, _hold)        # Capture held object into a named variable
OBJ(name) cmd [args]        # Dispatch cmd to stored object; OBJ(name) home/exit closes it
_fs_glob <pattern>          # Expand glob pattern; prints matching paths
```

### GreyHack Network Commands

```bash
_net_ports <ip>           # Scan IP for open ports
_net_devices <ip>       # List devices on LAN
_net_router <ip>       # Display router information
_net_devports <r> <d>   # Show device ports
_net_fwrules <ip>    # Display firewall rules
_net_random                 # Get random reachable router IP
_net_ping <ip>              # Check if host is reachable
_net_port <ip> <port>       # Check if port is open
_sys_procs              # Show running processes
_sys_kill <pid>          # Terminate process
```

### Built-in Utility Functions

```bash
# String Functions
len(str)                    # Get string/list length
upper(str)                  # Convert to uppercase
lower(str)                  # Convert to lowercase
substr(str, start, end)     # Extract substring
concat(str1, str2, ...)     # Concatenate strings
contains(haystack, needle)  # Check if contains string
replace(str, old, new)      # Replace substring
join(list, separator)       # Join list into string
split_str(str, delim)       # Split string into list
trim_str(str)               # Trim whitespace

# Math Functions
floor(num)                  # Round down
ceil(num)                   # Round up
round(num)                  # Round to nearest integer
abs(num)                    # Absolute value
min(num1, num2)             # Minimum of two numbers
max(num1, num2)             # Maximum of two numbers
random(min, max)            # Random number

# Type Functions
to_string(val)              # Convert to string
to_int(val)                 # Convert to integer
to_float(val)               # Convert to float
typeof(val)                 # Get type of value
typeof_val(val)             # Alias for typeof
get_type(val)               # Get type name
to_yesno(val)               # Convert to yes/no string
to_truefalse(val)           # Convert to true/false string

# IP Validation Functions
_isValidIP(ip)              # Check if valid IPv4 address (1/0)
_isLanIP(ip)                # Check if LAN/private IP (1/0)

# File Test Functions
file_exists(path)           # Check if file exists
is_folder(path)             # Check if directory
is_binary(path)             # Check if binary file
_fs_canwrite(path)          # Check write permission (returns 1/0)
_fs_canwrite(path, "file")  # Return file object if writable, null if not
_fs_canexec(path)           # Check execute permission (returns 1/0)
_fs_canexec(path, "file")   # Return file object if executable, null if not
file_read(path)             # Read file content (alias: _fs_read)
get_permissions(path)       # Get file permissions string
get_permissions(path, "file") # Return file object instead of permissions string
_fs_glob(pattern)           # Expand glob pattern; returns list of matching paths

# System Context Functions
get_user()                  # Get current username string
get_user("object")          # Get full user object instead of string
get_home()                  # Get home directory path string
get_home("file")            # Get home directory as file object
get_shell_type()            # Get shell type
get_computer_lan_ip()       # Get computer LAN IP string
get_computer_lan_ip("object") # Get computer object instead of IP
get_computer_public_ip()    # Get computer public IP string
get_computer_public_ip("object") # Get computer object instead of IP
get_lanIP()                 # Alias for get_computer_lan_ip
get_publicIP()              # Alias for get_computer_public_ip
get_root()                  # Get root filesystem path string
get_root("file")            # Get root as file object
get_layer()                 # Get current layer info

# Utility Functions
timestamp()                 # Get Unix timestamp
date()                      # Get current date/time string
get_string(prompt)          # Prompt for string input
get_integer(prompt)         # Prompt for integer input
get_decimal(prompt)         # Prompt for decimal input
get_any(prompt)             # Prompt for any input
get_yesno(prompt)           # Prompt for yes/no (returns 1/0)
pause()                     # Wait for user to press Enter

# Color Functions (use inside _print or return statements)
orange(text)                # Orange
cyan(text)                  # Cyan
magenta(text)               # Magenta / Pink
lime(text)                  # Lime green
bred(text)                  # Bright red
green(text)                 # Green
password(text)              # Password-style (hidden / obscured)
liteblue(text)              # Light blue
blue(text)                  # Blue
white(text)                 # White
purple(text)                # Purple
iyellow(text)               # Intense yellow
yellow(text)                # Yellow
liteGrey(text)              # Light grey
error(text)                 # Error style (red)
red(text)                   # Red
grey(text)                  # Grey
black(text)                 # Black
bold(text)                  # Bold text

# Map Functions
map([key,val,...])          # Create map from key-value pairs
map_set(map, key, val)      # Set key to value
map_get(map, key)           # Get value by key
map_del(map, key)           # Delete key
map_has(map, key)           # Check if key exists (returns 1/0)
map_keys(map)               # Get list of keys
map_values(map)             # Get list of values
map_len(map)                # Get number of entries

# JSON Functions
json(value)                 # Convert map to JSON string
json_parse(string)          # Parse JSON string to map

# Map File Persistence
map_save(map, path)         # Save map to file as JSON
map_load(path)              # Load map from JSON file
```

### Operators

```bash
# Arithmetic
+                           # Addition
-                           # Subtraction
*                           # Multiplication
/                           # Division
%                           # Modulo
**                          # Power

# Comparison
==                          # Equal
!=                          # Not equal
<                           # Less than
>                           # Greater than
<=                          # Less than or equal
>=                          # Greater than or equal

# Logical
and                         # Logical AND
or                          # Logical OR
not                         # Logical NOT
!                           # Logical NOT (alternative)
```

---

## Getting Started

### Running a Script

```bash
run script_name               # Run script from bash directory
run /path/to/script           # Run with absolute path (requires --ALLOWABS)
run --DEBUG script             # Run with debug output
run script arg1 arg2          # Pass arguments (accessible as $1, $2, etc.)
```

### Script Arguments

Pass arguments after the script name. Inside the script, use `$1`, `$2`, etc. — they are replaced with the corresponding argument values before execution:

```bash
// Script: greet_user
// Run with: run greet_user Alice 25
_print Hello $1, you are $2 years old
```

### Script Flags

Place these flags anywhere in your script file (they are stripped before execution):

| Flag | Effect |
|------|--------|
| `--DEBUG` | Print detailed execution trace |
| `--ALLOWABS` | Allow absolute paths in `_fs_*` commands |
| `--SIGBREAK` | Allow breaking out of script on warnings |
| `--SIGCONT` | Continue execution on warnings instead of stopping |
| `--ONERROR:` / `--ONERROR cmd` | On SIGSTOP, run handler command (does not continue past errors; use `--SIGCONT` for that) |

Flags can also be passed on the command line: `run --DEBUG --SIGBREAK myscript`

### Basic Script Structure

All examples in this guide are ready to cut and paste into a bash script file and run immediately.

```bash
// Script: hello_world
// A simple greeting script
// Copy this entire example to test it!

_print Hello, World!

_setvar(username, get_string(Enter your name:))
_print Welcome, _getvar(username)!
```

---

## Comments

**Note**: All code examples can be copied directly into a bash script file and run as-is.

### Single-Line Comments

```bash
// This is a comment
_print Hello World  // Inline comment
```

### URL Preservation

```bash
// Visit http://example.com for more info
_print Check out https://github.com/example  // URLs preserved
```

**Key Points:**
- Use `//` for comments
- Comments can be inline after commands
- `http://` and `https://` are preserved in URLs

---

## Variables

### Built-in Variables

These are pre-set automatically when a bash script runs. They update on pivot.

| Variable | Type | Description |
|----------|------|-------------|
| `COMPUTER` | computer | Current session computer object |
| `SHELL` | shell | Current session shell object |
| `ROOT` | file | Root filesystem file object |

**Accessing properties:**
```bash
// Store in a variable, then print
_setvar(ip, COMPUTER.public_ip)
_print cyan(Public IP:) _getvar(ip)

_setvar(host, COMPUTER.get_name)
_print cyan(Hostname:) _getvar(host)

_setvar(gw, COMPUTER.network_gateway)
_print cyan(Gateway:) _getvar(gw)

// Shell chaining - get computer from shell, then access its properties
_setvar(comp, SHELL.host_computer)
_setvar(compip, _getvar(comp).public_ip)
_print green(Shell host IP:) _getvar(compip)

// Or chain directly
_setvar(lan, SHELL.host_computer.local_ip)
_print lime(Chain LAN:) _getvar(lan)

// Root filesystem
_setvar(folders, ROOT.get_folders)
_setvar(count, len(_getvar(folders)))
_print yellow(Folder count:) _getvar(count)

// Iterate files with property access
for d in folders
  _setvar(name, _getvar(d).name)
  _setvar(perms, _getvar(d).permissions)
  _setvar(own, _getvar(d).owner)
  _print liteblue(_getvar(perms)) green(_getvar(own)) _getvar(name)
endfor
```

### Setting Variables

```bash
// Basic variable assignment
_setvar(name, Alice)
_setvar(age, 25)
_setvar(score, 95.5)

// Using variables
_print Hello _getvar(name)
_print You are _getvar(age) years old
```

### Variable Types

```bash
// String variable
_setvar(message, Hello World)

// Number variable
_setvar(count, 42)
_setvar(pi, 3.14159)

// List variable
_setvar(colors, [red, green, blue])

// Empty list
_setvar(items, [])
```

### Dynamic Variable Resolution

```bash
// Variables are resolved at runtime
_setvar(x, 10)
_setvar(y, _getvar(x))  // y = 10
_setvar(z, _getvar(y))  // z = 10

_print x = _getvar(x)  // Output: x = 10
_print y = _getvar(y)  // Output: y = 10
```

### Complex Examples

**Complete Script - Copy and Run:**

```bash
// Script: user_profile
// Copy this entire script to test it!

_setvar(username, Alice)
_setvar(age, 28)
_setvar(city, New York)
_setvar(role, Developer)

_print ==== USER PROFILE ====
_print Name: _getvar(username)
_print Age: _getvar(age)
_print City: _getvar(city)
_print Role: _getvar(role)

// Shopping cart
_setvar(cart, [])
_push cart Apple
_push cart Banana
_push cart Orange
_print Items in cart: len(_getvar(cart))
```

---

## Arithmetic & Operators

### Basic Operators

```bash
_setvar(a, 10)
_setvar(b, 3)

// Addition
_setvar(sum, _getvar(a) + _getvar(b))
_print Sum: _getvar(sum)  // Output: Sum: 13

// Subtraction
_setvar(diff, _getvar(a) - _getvar(b))
_print Difference: _getvar(diff)  // Output: Difference: 7

// Multiplication
_setvar(prod, _getvar(a) * _getvar(b))
_print Product: _getvar(prod)  // Output: Product: 30

// Division
_setvar(quot, _getvar(a) / _getvar(b))
_print Quotient: _getvar(quot)  // Output: Quotient: 3.33...

// Modulo
_setvar(rem, _getvar(a) % _getvar(b))
_print Remainder: _getvar(rem)  // Output: Remainder: 1

// Power
_setvar(power, _getvar(a) ** 2)
_print Power: _getvar(power)  // Output: Power: 100
```

### Operator Precedence

```bash
// Precedence: ** > * / % > + -
_setvar(x, 2 + 3 * 4)        // x = 14 (not 20)
_setvar(y, 10 - 6 / 2)       // y = 7 (not 2)
_setvar(z, 2 ** 3 + 1)       // z = 9 (8 + 1)

// Parentheses override precedence
_setvar(r, (3 + 2) * 4)      // r = 20
```

### Division by Zero

Division and modulo by zero are safe — they return 0 instead of crashing:

```bash
_setvar(r, 5 / 0)   // r = 0
_setvar(r, 7 % 0)   // r = 0
```

### Complex Expressions

**Complete Script - Copy and Run:**

```bash
// Script: calculator

_setvar(price, 19.99)
_setvar(quantity, 3)
_setvar(tax_rate, 0.08)

_setvar(subtotal, _getvar(price) * _getvar(quantity))
_setvar(tax, _getvar(subtotal) * _getvar(tax_rate))
_setvar(total, _getvar(subtotal) + _getvar(tax))

_print Subtotal: $_getvar(subtotal)
_print Tax: $_getvar(tax)
_print Total: $_getvar(total)
```

---

## Conditionals

### Basic If Statement

```bash
_setvar(age, 25)

if _getvar(age) >= 18
  _print You are an adult
endif
```

### If-Else Statement

```bash
_setvar(score, 75)

if _getvar(score) >= 60
  _print You passed!
else
  _print You failed.
endif
```

### If-Elif-Else Chain

```bash
_setvar(score, 85)

if _getvar(score) >= 90
  _print Grade: A
elif _getvar(score) >= 80
  _print Grade: B
elif _getvar(score) >= 70
  _print Grade: C
elif _getvar(score) >= 60
  _print Grade: D
else
  _print Grade: F
endif
```

### Comparison Operators

```bash
// == (equal)
if _getvar(x) == 10
  _print x equals 10
endif

// != (not equal)
if _getvar(name) != ""
  _print Name is not empty
endif

// < (less than)
if _getvar(age) < 18
  _print Minor
endif

// > (greater than)
if _getvar(score) > 50
  _print Passing
endif

// <= (less than or equal)
if _getvar(temp) <= 32
  _print Freezing
endif

// >= (greater than or equal)
if _getvar(speed) >= 65
  _print Speeding!
endif
```

### Logical Operators

```bash
// AND operator
_setvar(age, 25)
_setvar(has_license, 1)

if _getvar(age) >= 18 and _getvar(has_license) == 1
  _print You can drive
endif

// OR operator
_setvar(day, Saturday)

if _getvar(day) == Saturday or _getvar(day) == Sunday
  _print It's the weekend!
endif

// NOT operator
_setvar(logged_in, 0)

if not _getvar(logged_in) == 1
  _print Please log in
endif

// Using ! instead of not
if ! _getvar(logged_in) == 1
  _print Please log in
endif
```

### Complex Conditions

```bash
// Nested conditions
_setvar(age, 25)
_setvar(income, 50000)
_setvar(credit_score, 720)

if _getvar(age) >= 21
  if _getvar(income) >= 30000 and _getvar(credit_score) >= 650
    _print Loan approved!
  else
    _print Insufficient income or credit
  endif
else
  _print Must be 21 or older
endif

// Complex boolean logic
_setvar(temp, 75)
_setvar(humidity, 60)

if _getvar(temp) >= 70 and _getvar(temp) <= 85 and _getvar(humidity) < 70
  _print Perfect weather!
endif
```

### Real-World Examples

**Complete Script - Copy and Run:**

```bash
// Script: login_validation

_setvar(username, get_string(Username:))
_setvar(password, get_string(Password:))

if _getvar(username) == admin and _getvar(password) == secret123
  _print Login successful
  _print Welcome, _getvar(username)!
else
  _print Invalid credentials
endif

// Age verification
_setvar(age, get_integer(Enter your age:))

if _getvar(age) < 13
  _print Content restricted to users 13+
elif _getvar(age) < 18
  _print Parental guidance required
elif _getvar(age) < 21
  _print Some restrictions apply
else
  _print Full access granted
endif
```

---

## Loops

### For Loop with List Literal

```bash
// Iterate over list
for item in [Apple, Banana, Cherry]
  _print Fruit: _getvar(item)
endfor

// Output:
// Fruit: Apple
// Fruit: Banana
// Fruit: Cherry
```

### For Loop with Variable

```bash
// Create a list variable
_setvar(colors, [Red, Green, Blue, Yellow])

// Iterate over variable
for color in colors
  _print Color: _getvar(color)
endfor
```

### For Loop with Range

```bash
// Count from 1 to 5
for i in range(1, 5)
  _print Count: _getvar(i)
endfor

// Output:
// Count: 1
// Count: 2
// Count: 3
// Count: 4
// Count: 5
```

### While Loop

```bash
// Basic while loop
_setvar(count, 0)

while _getvar(count) < 5
  _print Count: _getvar(count)
  _setvar(count, _getvar(count) + 1)
endwhile

// Output:
// Count: 0
// Count: 1
// Count: 2
// Count: 3
// Count: 4
```

### Until Loop

```bash
// Until loop (runs while condition is false)
_setvar(tries, 0)

until _getvar(tries) >= 3
  _print Attempt: _getvar(tries)
  _setvar(tries, _getvar(tries) + 1)
enduntil

// Output:
// Attempt: 0
// Attempt: 1
// Attempt: 2
```

### Nested Loops

```bash
// Multiplication table
for i in range(1, 5)
  for j in range(1, 5)
    _setvar(product, _getvar(i) * _getvar(j))
    _print _getvar(i) x _getvar(j) = _getvar(product)
  endfor
endfor
```

### Complex Loop Examples

**Complete Script - Copy and Run:**

```bash
// Script: find_primes

_print Finding primes from 2 to 20:

for num in range(2, 20)
  _setvar(is_prime, 1)
  
  for divisor in range(2, _getvar(num) - 1)
    _setvar(remainder, _getvar(num) % _getvar(divisor))
    if _getvar(remainder) == 0
      _setvar(is_prime, 0)
      break
    endif
  endfor
  
  if _getvar(is_prime) == 1
    _print _getvar(num) is prime
  endif
endfor

// Password retry logic
_setvar(max_tries, 3)
_setvar(tries, 0)

while _getvar(tries) < _getvar(max_tries)
  _setvar(password, get_string(Enter password:))
  
  if _getvar(password) == secret123
    _print Access granted!
    break
  endif
  
  _setvar(tries, _getvar(tries) + 1)
  _setvar(remaining, _getvar(max_tries) - _getvar(tries))
  _print Wrong password. _getvar(remaining) tries remaining.
endwhile

if _getvar(tries) >= _getvar(max_tries)
  _print Account locked
endif
```

---

## Switch/Case Statements

### Basic Switch

```bash
// Match on a numeric variable
_setvar(day, 3)

switch _getvar(day)
  case 1
    _print Monday
  case 2
    _print Tuesday
  case 3
    _print Wednesday
  case 4
    _print Thursday
  case 5
    _print Friday
  default
    _print Weekend
endswitch
```

### Switch with String Values

```bash
// Literal string matching — no quotes needed
_setvar(r, miss)
switch alpha
  case alpha
    _setvar(r, hit_alpha)
  case beta
    _setvar(r, hit_beta)
endswitch
// r = hit_alpha
```

### Switch with Variable

```bash
_setvar(val, cherry)
_setvar(r, miss)
switch _getvar(val)
  case apple
    _setvar(r, apple)
  case cherry
    _setvar(r, cherry)
  case banana
    _setvar(r, banana)
endswitch
// r = cherry
```

### Default Case

```bash
// Default fires when no case matches
_setvar(r, miss)
switch unknown
  case x
    _setvar(r, x)
  case y
    _setvar(r, y)
  default
    _setvar(r, default_hit)
endswitch
// r = default_hit
```

Default is skipped when a match is found. If no case matches and no default exists, execution continues after `endswitch` with no changes.

### Numeric Matching

```bash
// Numbers are compared by value
_setvar(n, 42)
_setvar(r, miss)
switch _getvar(n)
  case 41
    _setvar(r, wrong)
  case 42
    _setvar(r, forty_two)
  case 43
    _setvar(r, wrong)
endswitch
// r = forty_two
```

Zero and negative numbers also work:

```bash
_setvar(n, -5)
_setvar(r, miss)
switch _getvar(n)
  case 5
    _setvar(r, positive)
  case -5
    _setvar(r, negative)
  default
    _setvar(r, default)
endswitch
// r = negative
```

### First Match Wins

There is no fall-through. The first matching case executes and the switch exits:

```bash
_setvar(r, miss)
switch hello
  case hello
    _setvar(r, first)
  case hello
    _setvar(r, second)
endswitch
// r = first — second case never runs
```

### Complex Case Bodies

Case bodies can contain any construct — if/else, loops, multiple statements:

```bash
// If/else inside a case
_setvar(mode, advanced)
_setvar(level, 10)
_setvar(r, miss)
switch _getvar(mode)
  case basic
    _setvar(r, basic)
  case advanced
    if _getvar(level) > 5
      _setvar(r, advanced_high)
    else
      _setvar(r, advanced_low)
    endif
  default
    _setvar(r, default)
endswitch
// r = advanced_high
```

```bash
// For loop inside a case
_setvar(action, sum)
_setvar(r, 0)
switch _getvar(action)
  case sum
    for i in range(1, 5)
      _setvar(r, _getvar(r) + _getvar(i))
    endfor
  default
    _setvar(r, -1)
endswitch
// r = 15
```

### Nested Switches

Switches can be nested. The inner switch is fully contained within a case body:

```bash
_setvar(category, fruit)
_setvar(item, apple)
_setvar(r, miss)
switch _getvar(category)
  case fruit
    switch _getvar(item)
      case apple
        _setvar(r, red_fruit)
      case banana
        _setvar(r, yellow_fruit)
      default
        _setvar(r, unknown_fruit)
    endswitch
  case veggie
    _setvar(r, vegetable)
  default
    _setvar(r, unknown_category)
endswitch
// r = red_fruit
```

### Switch in Functions

```bash
func grade(score)
  _setvar(result, F)
  switch _getvar(score)
    case 4
      _setvar(result, A)
    case 3
      _setvar(result, B)
    case 2
      _setvar(result, C)
    case 1
      _setvar(result, D)
    default
      _setvar(result, F)
  endswitch
  _return _getvar(result)
endfunc

_setvar(r, grade(4))   // r = A
_setvar(r, grade(2))   // r = C
_setvar(r, grade(0))   // r = F (via default)
```

### Switch in Loops

```bash
_setvar(total, 0)
for cmd in [add, add, sub, add, sub]
  switch _getvar(cmd)
    case add
      _setvar(total, _getvar(total) + 1)
    case sub
      _setvar(total, _getvar(total) - 1)
  endswitch
endfor
// total = 1 (3 adds - 2 subs)
```

### Complete Menu Example

```bash
// Script: menu_system

_print ==== MAIN MENU ====
_print 1. View Profile
_print 2. Edit Settings
_print 3. Exit

_setvar(choice, get_integer(Enter choice:))

switch _getvar(choice)
  case 1
    _print Loading profile...
  case 2
    _print Opening settings...
  case 3
    _print Goodbye!
    _exit 0
  default
    _print Invalid choice
endswitch
```

**Key Points:**
- No fall-through — first match wins, then execution continues after `endswitch`
- Case values are resolved through `_getVal`: numbers, strings, and variables all work
- Default is optional — if absent and nothing matches, nothing happens
- Case bodies support all control flow: if/else, loops, function calls, nested switches
- Avoid using single-letter case values (like `a`, `b`) that might collide with existing variable names — use descriptive values instead

---

## Loop Control

### Break Statement

```bash
// Exit loop early
for i in range(1, 10)
  _print Number: _getvar(i)
  
  if _getvar(i) == 5
    _print Breaking at 5
    break
  endif
endfor

_print Loop ended

// Output:
// Number: 1
// Number: 2
// Number: 3
// Number: 4
// Number: 5
// Breaking at 5
// Loop ended
```

### Continue Statement

```bash
// Skip to next iteration
for i in range(1, 10)
  if _getvar(i) == 5
    _print Skipping 5
    continue
  endif
  
  _print Number: _getvar(i)
endfor

// Output:
// Number: 1
// Number: 2
// Number: 3
// Number: 4
// Skipping 5
// Number: 6
// Number: 7
// Number: 8
// Number: 9
// Number: 10
```

### Complex Control Flow

**Complete Script - Copy and Run:**

```bash
// Script: search_array

_setvar(numbers, [10, 25, 42, 17, 8, 99, 33])
_setvar(target, 42)
_setvar(found, 0)
_setvar(index, 0)

for num in numbers
  if _getvar(num) == _getvar(target)
    _print Found _getvar(target) at index _getvar(index)
    _setvar(found, 1)
    break
  endif
  _setvar(index, _getvar(index) + 1)
endfor

if _getvar(found) == 0
  _print Value not found
endif

// Process only even numbers
_print Even numbers:
for i in range(1, 20)
  _setvar(remainder, _getvar(i) % 2)
  if _getvar(remainder) != 0
    continue
  endif
  _print _getvar(i)
endfor
```

---

## Error Handling (Try/Catch)

Wrap code in `try`/`catch`/`end try` blocks to catch runtime errors and `_throw` statements without crashing the script.

### Basic Try/Catch

```bash
try
  _print Step 1: OK
  _print Step 2: OK
  _print Step 3: OK
catch err
  _print CAUGHT: _getvar(err)
endtry
// If no error occurs, the catch block is skipped entirely
```

### Throwing Errors with _throw

Use `_throw` inside a `try` block to jump immediately to `catch`:

```bash
try
  _print Step 1: OK
  _throw Something went wrong
  _print Step 3: SHOULD NOT SEE THIS
catch err
  _print CAUGHT: _getvar(err)
endtry
// Output: Step 1: OK, then CAUGHT: Something went wrong
```

### Catch Without Variable

You can omit the variable name on `catch` if you don't need the error message:

```bash
try
  _throw Oops
catch
  _print An error was caught
endtry
```

### Catching Real Errors

Runtime errors (e.g., from invalid file operations) are caught the same way:

```bash
try
  wipe /nonexistent/path
catch err
  _print Caught error: _getvar(err)
endtry
```

### Execution Continues After Try/Catch

Code after `end try` always runs, whether the `try` block succeeded or the `catch` block handled an error:

```bash
try
  _throw test error
catch err
  _print Handled: _getvar(err)
endtry
_print This line runs after the try/catch block
```

### Notes

- `end try` also works but `endtry` is preferred (consistent with `endif`, `endfor`, etc.)
- `_throw` only works inside a `try` block
- Try/catch blocks can be nested
- Try/catch state is preserved across session pivots (proxy/ssh)

---

## Functions

### Defining Functions

```bash
// Simple function
func greet
  _print Hello from function!
endfunc

// Call the function
greet
```

### Functions with Parameters

```bash
// Function with one parameter
func say_hello(name)
  _print Hello, _getvar(name)!
endfunc

say_hello(Alice)
say_hello(Bob)

// Function with multiple parameters
func calculate_area(width, height)
  _setvar(area, _getvar(width) * _getvar(height))
  _print Area: _getvar(area)
endfunc

calculate_area(5, 10)  // Output: Area: 50
calculate_area(7, 3)   // Output: Area: 21
```

### Functions with Return Values

```bash
// Function that returns a value
func add(a, b)
  _setvar(result, _getvar(a) + _getvar(b))
  _return _getvar(result)
endfunc

// Capture return value
_setvar(sum, add(10, 20))
_print Sum: _getvar(sum)  // Output: Sum: 30
```

### Recursive Functions

**Note**: Recursion depth is limited to 100 levels. For deep recursion, use iterative approaches.

```bash
// Factorial calculation (works for small values)
func factorial(n)
  if _getvar(n) <= 1
    _return 1
  else
    _setvar(n_minus_1, _getvar(n) - 1)
    _setvar(result, factorial(_getvar(n_minus_1)))
    _setvar(final, _getvar(n) * _getvar(result))
    _return _getvar(final)
  endif
endfunc

_setvar(fact5, factorial(5))
_print 5! = _getvar(fact5)  // Output: 5! = 120

// For larger values, use iterative approach:
func factorial_iterative(n)
  _setvar(result, 1)
  _setvar(i, 2)
  while _getvar(i) <= _getvar(n)
    _setvar(result, _getvar(result) * _getvar(i))
    _setvar(i, _getvar(i) + 1)
  endwhile
  _return _getvar(result)
endfunc
```

### Complex Function Examples

```bash
// Functions calling functions (proven in func_test)
func addOne(n)
  _return _getvar(n) + 1
endfunc

func double(n)
  _return _getvar(n) * 2
endfunc

func addTwo(n)
  _setvar(t, addOne(_getvar(n)))
  _return addOne(_getvar(t))
endfunc

_setvar(r, addTwo(10))   // r = 12

// Clamp function — multiple parameters with conditional logic
func clamp(val, lo, hi)
  if _getvar(val) < _getvar(lo)
    _return _getvar(lo)
  endif
  if _getvar(val) > _getvar(hi)
    _return _getvar(hi)
  endif
  _return _getvar(val)
endfunc

_setvar(r, clamp(50, 0, 10))   // r = 10 (clamped to upper)
_setvar(r, clamp(-5, 0, 10))   // r = 0 (clamped to lower)
_setvar(r, clamp(5, 0, 10))    // r = 5 (within range)
```

### Scope Isolation

Each function call gets its own local scope. Variables set inside a function do not leak to the caller, and the caller's variables are restored after the function returns:

```bash
_setvar(x, 100)

func setX()
  _setvar(x, 999)
endfunc

setX()
// x is still 100 — function scope is isolated
```

### Iterative Fibonacci

```bash
func fibIter(n)
  if _getvar(n) == 0
    _return 0
  endif
  if _getvar(n) == 1
    _return 1
  endif
  _setvar(prev, 0)
  _setvar(curr, 1)
  _setvar(counter, 2)
  while _getvar(counter) <= _getvar(n)
    _setvar(next, _getvar(prev) + _getvar(curr))
    _setvar(prev, _getvar(curr))
    _setvar(curr, _getvar(next))
    _setvar(counter, _getvar(counter) + 1)
  endwhile
  _return _getvar(curr)
endfunc

_setvar(r, fibIter(10))    // r = 55
_setvar(r, fibIter(20))    // r = 6765

// Call in a loop
for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  _setvar(fib_result, fibIter(_getvar(i)))
  _print F(_getvar(i)) = _getvar(fib_result)
endfor
```

---

## Array Operations

### Creating Arrays

```bash
// Empty array
_setvar(items, [])

// Array with initial values
_setvar(fruits, [Apple, Banana, Cherry])
_setvar(numbers, [1, 2, 3, 4, 5])
```

### Push (Add to End)

```bash
_setvar(stack, [])

_push stack First
_push stack Second
_push stack Third

// stack = [First, Second, Third]
```

### Pop (Remove from End)

```bash
_setvar(stack, [A, B, C, D])

_pop stack  // Removes D
_pop stack  // Removes C

// stack = [A, B]
```

### Pull (Remove from Start)

```bash
_setvar(queue, [First, Second, Third])

_pull queue  // Removes First

// queue = [Second, Third]
```

### Length

```bash
_setvar(items, [A, B, C, D, E])

_len items  // Output: 5
```

### Checking for Values

**Command style** (passes variable by name):
```bash
_setvar(colors, [red, green, blue, yellow])

_in colors blue   // Output: true (or 1)
_in colors purple // Output: false (or 0)
```

**Function style** (passes resolved list via `_getvar`, usable inside `_setvar` and expressions):
```bash
_setvar(colors, [red, green, blue, yellow])

_setvar(found, _in(_getvar(colors), blue))   // found = 1
_setvar(found, _in(_getvar(colors), purple)) // found = 0
```

### Complex Array Examples

**Complete Script - Copy and Run:**

```bash
// Script: shopping_cart

_setvar(cart, [])

_print ==== SHOPPING CART ====

// Add items
_push cart Laptop
_push cart Mouse
_push cart Keyboard

_len cart
_print Items in cart

// Display cart
_print Cart contents:
for item in cart
  _print - _getvar(item)
endfor

// Remove last item
_pop cart
_print Removed last item

// Check if item exists
_in cart Mouse
// Returns 1 if found

// Stack implementation
_setvar(stack, [])

_print Pushing values onto stack:
_push stack 10
_push stack 20
_push stack 30
_print Stack size: len(_getvar(stack))

_print Popping values:
_pop stack
_print Stack size: len(_getvar(stack))

// Queue implementation
_setvar(queue, [])

_print Enqueuing:
_push queue Task1
_push queue Task2
_push queue Task3

_print Dequeuing:
_pull queue
_print Remaining: len(_getvar(queue))
```

---

## Built-in Functions

### String Functions

#### len(str)

```bash
_setvar(message, Hello World)
_setvar(length, len(_getvar(message)))
_print Length: _getvar(length)  // Output: Length: 11
```

#### upper(str)

```bash
_setvar(text, hello world)
_setvar(uppercase, upper(_getvar(text)))
_print _getvar(uppercase)  // Output: HELLO WORLD
```

#### lower(str)

```bash
_setvar(text, HELLO WORLD)
_setvar(lowercase, lower(_getvar(text)))
_print _getvar(lowercase)  // Output: hello world
```

#### substr(str, start, end)

```bash
_setvar(text, Hello World)
_setvar(sub, substr(_getvar(text), 0, 5))
_print _getvar(sub)  // Output: Hello
```

#### concat(str1, str2, ...)

```bash
_setvar(first, Hello)
_setvar(last, World)
_setvar(full, concat(_getvar(first),  , _getvar(last)))
_print _getvar(full)  // Output: Hello World
```

#### contains(haystack, needle)

```bash
_setvar(text, Hello World)

if contains(_getvar(text), World)
  _print Found!
endif
```

#### replace(str, old, new)

```bash
_setvar(text, Hello World)
_setvar(result, replace(_getvar(text), World, Bash))
_print _getvar(result)  // Output: Hello Bash

// Delete by replacing with empty
_setvar(result, replace(foobar, foo, ))
// result = bar
```

#### join(list, separator)

```bash
_setvar(parts, [a, b, c])
_setvar(result, join(_getvar(parts), -))
_print _getvar(result)  // Output: a-b-c

// Empty separator concatenates
_setvar(result, join(_getvar(parts), ))
// result = abc

// Single element — no separator
_setvar(single, [only])
_setvar(result, join(_getvar(single), _))
// result = only
```

#### split_str(str, delim)

```bash
_setvar(csv, a-b-c)
_setvar(parts, split_str(_getvar(csv), -))
// parts = [a, b, c], len = 3

// Multi-character delimiter
_setvar(data, a::b::c)
_setvar(parts, split_str(_getvar(data), ::))
// parts len = 3

// No delimiter found — returns single-element list
_setvar(parts, split_str(hello, x))
// parts len = 1
```

#### trim_str(str)

```bash
_setvar(padded,   padded  )
_setvar(result, trim_str(_getvar(padded)))
_print _getvar(result)  // Output: padded
```

### Math Functions

#### floor(num)

```bash
_setvar(value, 3.7)
_setvar(floored, floor(_getvar(value)))
_print _getvar(floored)  // Output: 3
```

#### ceil(num)

```bash
_setvar(value, 3.2)
_setvar(ceiled, ceil(_getvar(value)))
_print _getvar(ceiled)  // Output: 4
```

#### abs(num)

```bash
_setvar(value, -42)
_setvar(absolute, abs(_getvar(value)))
_print _getvar(absolute)  // Output: 42
```

#### round(num)

```bash
_setvar(result, round(3.5))   // result = 4
_setvar(result, round(3.4))   // result = 3
```

#### min(a, b) / max(a, b)

```bash
_setvar(smaller, min(5, 9))   // smaller = 5
_setvar(larger, max(5, 9))    // larger = 9
```

#### random(min, max)

```bash
_setvar(dice, random(1, 6))
_print You rolled: _getvar(dice)
// random(5, 5) always returns 5
```

### Utility Functions

#### timestamp()

```bash
_setvar(now, timestamp())
_print Current timestamp: _getvar(now)
```

#### date()

```bash
_setvar(today, date())
_print Today is: _getvar(today)
```

#### pause()

Stop execution and wait for the user to press Enter:

```bash
_print Review the output above, then press Enter to continue...
pause
_print Continuing...
```

### File Test Functions

#### file_exists(path)

```bash
if file_exists(/etc/passwd)
  _print File exists
else
  _print File not found
endif
```

#### is_folder(path)

```bash
if is_folder(/home)
  _print It's a directory
else
  _print It's a file
endif
```

#### is_binary(path)

```bash
if is_binary(/bin/bash)
  _print Binary file
else
  _print Text file
endif
```

#### _isValidIP(ip)

Returns 1 if the string is a valid IPv4 address, 0 otherwise.

```bash
_setvar(target, get_string(Enter IP:))
if _isValidIP(_getvar(target)) == 0
  _print red(ERROR) Not a valid IP address
  _exit
end if
```

#### _isLanIP(ip)

Returns 1 if the IP is a private/LAN address (192.168.x.x, 10.x.x.x, 172.16-31.x.x), 0 otherwise.

```bash
_setvar(target, get_string(Enter IP:))
if _isLanIP(_getvar(target)) == 1
  _print yellow(NOTE) This is a LAN IP
else
  _print green(OK) This is a public IP
end if
```

#### _fs_glob(pattern)

Expand a glob pattern and return a list of matching file/directory paths:

```bash
// Find all .src files in current directory
_setvar(files, _fs_glob(*.src))
for f in files
  _print _getvar(f)
endfor

// Find all files matching a prefix
_setvar(matches, _fs_glob(/home/user/data_*))
_print Found: len(_getvar(matches)) files
```

### System Context Functions

Most context functions accept an optional string argument to change their return type:

```bash
// Default: returns string
_setvar(username, get_user())           // "admin"
_setvar(homepath, get_home())          // "/home/admin"
_setvar(rootpath, get_root())          // "/"
_setvar(lanip, get_computer_lan_ip())  // "192.168.1.5"
_setvar(pubip, get_computer_public_ip()) // "203.0.113.1"

// With "object" or "file" argument: returns the underlying object
_setvar(user_obj, get_user("object"))            // full user object
_setvar(home_file, get_home("file"))             // home dir as file object
_setvar(root_file, get_root("file"))             // root as file object
_setvar(lan_comp, get_computer_lan_ip("object")) // computer object (by LAN)
_setvar(pub_comp, get_computer_public_ip("object")) // computer object (by public IP)

// Object return enables property access
_setvar(home_file, get_home("file"))
_print Permissions: _getvar(home_file).permissions
_print Owner: _getvar(home_file).owner
```

The same applies to `get_permissions`, `_fs_canwrite`, and `_fs_canexec` — pass `"file"` as the second argument to get the file object back instead of a string/integer:

```bash
_setvar(f, get_permissions(/etc/passwd, "file"))  // file object, not perm string
_setvar(f, _fs_canwrite(/tmp/data.txt, "file"))   // file object if writable, null if not
_setvar(f, _fs_canexec(/bin/tool, "file"))        // file object if executable, null if not
```

### Complex Built-in Function Examples

```bash
// Text processing
_setvar(input, get_string(Enter text:))
_setvar(length, len(_getvar(input)))

_print Original: _getvar(input)
_print Length: _getvar(length)
_print Uppercase: upper(_getvar(input))
_print Lowercase: lower(_getvar(input))

// Password generator
_print Generating password:
_setvar(part1, random(1000, 9999))
_setvar(part2, random(1000, 9999))
_setvar(password, concat(PASS, _getvar(part1), -, _getvar(part2)))
_print Password: _getvar(password)

// File checker
_setvar(path, /etc/passwd)

if file_exists(_getvar(path))
  _print File exists: _getvar(path)
  
  if is_binary(_getvar(path))
    _print Type: Binary
  else
    _print Type: Text
  endif
  
  if is_folder(_getvar(path))
    _print It's a folder
  else
    _print It's a file
  endif
endif
```

---

## Maps & JSON

Maps are key-value data structures for storing named data. Combined with JSON functions and file persistence, they enable configuration management, data storage, and structured data passing.

### Creating Maps

#### map(key, val, ...)

```bash
// Create from key-value pairs
_setvar(user, map(name, Alice, age, 25, role, admin))
_print _getvar(user)

// Create empty map
_setvar(config, map())
```

### Getting and Setting Values

#### map_get(map, key)

```bash
_setvar(user, map(name, Alice, age, 25))
_setvar(name, map_get(_getvar(user), name))
_print Name: _getvar(name)  // Output: Name: Alice

// Missing key returns null
_setvar(missing, map_get(_getvar(user), email))
```

#### map_set(map, key, val)

```bash
_setvar(user, map(name, Alice))
map_set(_getvar(user), email, alice@example.com)
map_set(_getvar(user), age, 30)
_print _getvar(user)

// Overwrite existing key
map_set(_getvar(user), name, Bob)
```

### Checking and Deleting Keys

#### map_has(map, key)

```bash
_setvar(config, map(host, 192.168.1.1, port, 22))

if map_has(_getvar(config), host)
  _print Host configured: map_get(_getvar(config), host)
endif

if map_has(_getvar(config), password) == 0
  _print No password set
endif
```

#### map_del(map, key)

```bash
_setvar(data, map(a, 1, b, 2, c, 3))
map_del(_getvar(data), b)
_print Keys: map_keys(_getvar(data))  // [a, c]
```

### Inspecting Maps

#### map_keys(map)

```bash
_setvar(user, map(name, Alice, age, 25, role, admin))
_setvar(keys, map_keys(_getvar(user)))
_print Keys: _getvar(keys)  // [name, age, role]

// Iterate over keys
for k in keys
  _print _getvar(k): map_get(_getvar(user), _getvar(k))
endfor
```

#### map_values(map)

```bash
_setvar(user, map(name, Alice, age, 25))
_setvar(vals, map_values(_getvar(user)))
_print Values: _getvar(vals)  // [Alice, 25]
```

#### map_len(map)

```bash
_setvar(data, map(a, 1, b, 2, c, 3))
_print Size: map_len(_getvar(data))  // Output: Size: 3
```

### JSON Conversion

#### json(value)

```bash
// Convert map to JSON string
_setvar(user, map(name, Alice, score, 100))
_setvar(jsonStr, json(_getvar(user)))
_print _getvar(jsonStr)  // Output: {"name": "Alice", "score": 100}
```

#### json_parse(string)

```bash
// Parse JSON string back to map
_setvar(jsonStr, {"host": "10.0.0.1", "port": 22})
_setvar(config, json_parse(_getvar(jsonStr)))
_print Host: map_get(_getvar(config), host)  // Output: Host: 10.0.0.1
```

### File Persistence

#### map_save(map, path)

```bash
// Save map to file as JSON
_setvar(config, map(host, 192.168.1.1, port, 22, user, admin))
map_save(_getvar(config), /tmp/config.json)
_print Config saved!
```

#### map_load(path)

```bash
// Load map from JSON file
_setvar(config, map_load(/tmp/config.json))
_print Host: map_get(_getvar(config), host)
_print Port: map_get(_getvar(config), port)
```

### Complete Map Examples

```bash
// Build and use a configuration system
_setvar(defaults, map(theme, dark, lang, en, timeout, 30))

// Check for saved config
if file_exists(/tmp/app_config.json)
  _setvar(config, map_load(/tmp/app_config.json))
  _print Loaded saved config
else
  _setvar(config, _getvar(defaults))
  _print Using defaults
endif

// Display all settings
_setvar(keys, map_keys(_getvar(config)))
for k in keys
  _print _getvar(k) = map_get(_getvar(config), _getvar(k))
endfor

// Modify and save
map_set(_getvar(config), theme, light)
map_save(_getvar(config), /tmp/app_config.json)
_print Config saved with map_len(_getvar(config)) entries
```

```bash
// Inventory tracker
_setvar(inventory, map())
map_set(_getvar(inventory), apples, 10)
map_set(_getvar(inventory), bananas, 5)
map_set(_getvar(inventory), oranges, 8)

// Check stock
if map_has(_getvar(inventory), apples)
  _print Apple stock: map_get(_getvar(inventory), apples)
endif

// Remove sold-out item
map_del(_getvar(inventory), bananas)
_print Items in stock: map_len(_getvar(inventory))

// Convert to JSON for display
_setvar(report, json(_getvar(inventory)))
_print Inventory: _getvar(report)
```

---

## Type Casting

### to_string(val)

```bash
// Convert number to string
_setvar(num, 42)
_setvar(str, to_string(_getvar(num)))
_print Type: typeof(_getvar(str))  // Output: Type: string
```

### to_int(val)

```bash
// Convert to integer (truncates decimals)
_setvar(pi, 3.14159)
_setvar(int_value, to_int(_getvar(pi)))
_print _getvar(int_value)  // Output: 3

// Convert string to integer
_setvar(str_num, 123)
_setvar(num, to_int(_getvar(str_num)))
_print _getvar(num)  // Output: 123
```

### to_float(val)

```bash
// Convert string to float
_setvar(price_str, 19.99)
_setvar(price, to_float(_getvar(price_str)))
_print _getvar(price)  // Output: 19.99

// Convert integer to float
_setvar(count, 5)
_setvar(float_count, to_float(_getvar(count)))
_print _getvar(float_count)  // Output: 5.0
```

### typeof(val)

```bash
// Check variable types
_setvar(name, Alice)
_setvar(age, 25)
_setvar(items, [a, b, c])

_print Name type: typeof(_getvar(name))     // Output: string
_print Age type: typeof(_getvar(age))       // Output: number
_print Items type: typeof(_getvar(items))   // Output: list
```

### Complete Type Casting Example

**Complete Script - Copy and Run:**

```bash
// Script: type_converter

_print ==== TYPE CONVERTER ====

_setvar(input, get_string(Enter a value:))
_print Original value: _getvar(input)
_print Original type: typeof(_getvar(input))

// Convert to different types
_setvar(as_int, to_int(_getvar(input)))
_setvar(as_float, to_float(_getvar(input)))
_setvar(as_string, to_string(_getvar(input)))

_print As integer: _getvar(as_int) (type: typeof(_getvar(as_int)))
_print As float: _getvar(as_float) (type: typeof(_getvar(as_float)))
_print As string: _getvar(as_string) (type: typeof(_getvar(as_string)))

// Type-safe calculator
_setvar(num1_str, get_string(Enter first number:))
_setvar(num2_str, get_string(Enter second number:))

// Convert to numbers
_setvar(num1, to_float(_getvar(num1_str)))
_setvar(num2, to_float(_getvar(num2_str)))

// Perform calculation
_setvar(sum, _getvar(num1) + _getvar(num2))
_print Result: _getvar(sum)

// Convert back to string for display
_setvar(result_str, to_string(_getvar(sum)))
_print Result as string: _getvar(result_str)
```

---

## Typed Input Prompts

### get_string()

```bash
// Prompt for string input
_setvar(name, get_string(Enter your name:))
_print Hello, _getvar(name)!
```

### get_integer()

```bash
// Prompt for integer (automatically converts)
_setvar(age, get_integer(Enter your age:))
_print You are _getvar(age) years old

// Age is stored as integer
_setvar(next_year, _getvar(age) + 1)
_print Next year you'll be _getvar(next_year)
```

### get_decimal()

```bash
// Prompt for decimal number
_setvar(price, get_decimal(Enter price:))
_setvar(tax, _getvar(price) * 0.08)
_setvar(total, _getvar(price) + _getvar(tax))

_print Price: $_getvar(price)
_print Tax: $_getvar(tax)
_print Total: $_getvar(total)
```

### get_any()

```bash
// Accept any input type
_setvar(value, get_any(Enter any value:))
_print You entered: _getvar(value)
_print Type: typeof(_getvar(value))
```

### get_yesno()

```bash
// Prompt for yes/no input — returns 1 for yes/y, 0 for no/n/empty
_setvar(confirm, get_yesno(Delete all files?))

if _getvar(confirm) == 1
  _print Deleting...
else
  _print Cancelled
endif
```

Loops until the user enters a valid response (`yes`, `y`, `no`, `n`, or empty which defaults to no). Case-insensitive.

### menu()

Display an interactive menu for users to select from a list of options.

```bash
// Basic menu with numbers
_setvar(choices, [Start, Stop, Status, Exit])
_setvar(selected, menu(_getvar(choices), numbers))
_print You selected option: _getvar(selected)
```

**Syntax:**
```
menu(items_list, style, color, case_mode)
```

**Parameters:**
- `items_list` - Array/list of menu options
- `style` - `"numbers"` (1, 2, 3...) or `"letters"` (A, B, C...)
- `color` - Color for menu items (optional, defaults to cyan)
  - **Named colors**: `cyan`, `green`, `red`, `yellow`, `magenta`, `orange`, `blue`, `lime`, `white`
  - **Hex colors**: `#00bfff` or `00bfff` (6-character hex code)
- `case_mode` - Letter-input mode (optional, defaults to `insensitive`)
  - `insensitive`: accepts either uppercase or lowercase letter input
  - `strict`: requires uppercase letter labels (`A`-`Z`) in letters mode

**Returns:** 0-based index of selected option

**Examples:**

```bash
// Numbers menu with green color
_setvar(servers, [Web Server, Database, Cache, Load Balancer])
_setvar(choice, menu(_getvar(servers), numbers, green))

if _getvar(choice) == 0
  _print Configuring web server...
endif
```

```bash
// Letter menu with red (for dangerous operations)
_setvar(actions, [Delete User, Reset Password, Ban Account, Cancel])
_setvar(action, menu(_getvar(actions), letters, red))

if _getvar(action) == 0
  _print User will be deleted
endif
```

```bash
// Using default cyan color
_setvar(options, [Option A, Option B, Option C])
_setvar(result, menu(_getvar(options), letters))
_print Result index: _getvar(result)
```

```bash
// Explicit case-insensitive letters mode (same as default)
_setvar(result, menu(_getvar(options), letters, cyan, insensitive))

// Strict letters mode (must input uppercase label)
_setvar(result, menu(_getvar(options), letters, cyan, strict))
```

**Hex Color Examples:**

```bash
// Using hex color code for light blue
_setvar(items, [Item 1, Item 2, Item 3])
_setvar(choice, menu(_getvar(items), numbers, 00bfff))

// With # prefix
_setvar(choice, menu(_getvar(items), letters, #eb0cc6))
```

### Complex Input Example

**Complete Script - Copy and Run:**

```bash
// Script: user_registration

_print ==== USER REGISTRATION ====

_setvar(username, get_string(Username:))
_setvar(email, get_string(Email:))
_setvar(age, get_integer(Age:))
_setvar(weight, get_decimal(Weight (kg):))

// Validation
if len(_getvar(username)) < 3
  _print Username too short
  _exit 1
endif

if _getvar(age) < 13
  _print Must be 13 or older
  _exit 1
endif

// Display summary
_print ==== SUMMARY ====
_print Username: _getvar(username)
_print Email: _getvar(email)
_print Age: _getvar(age)
_print Weight: _getvar(weight) kg

// Calculate BMI
_setvar(height, get_decimal(Height (m):))
_setvar(height_squared, _getvar(height) * _getvar(height))
_setvar(bmi, _getvar(weight) / _getvar(height_squared))

_print BMI: _getvar(bmi)
```

---

## System & File Commands

### _print

```bash
// Simple print
_print Hello World

// Print variables
_setvar(name, Alice)
_print Hello _getvar(name)

// With colors
_print red(Error!) This is a problem
_print green(Success!) Operation complete
_print blue(Info:) Processing...
```

### _fs_read

```bash
// Read file content (returns string)
_setvar(content, _fs_read(/etc/passwd))
_print File content: _getvar(content)
```

### _fs_view

```bash
// Display file content
_fs_view /etc/passwd
```

### _fs_write

```bash
// Write to file
_fs_write test.txt Hello World

// Write variable content
_setvar(data, This is my data)
_fs_write output.txt _getvar(data)

// Write to relative path (current directory)
_fs_write notes.txt My important notes
```

### _fs_mkdir

```bash
// Create directory
_fs_mkdir mydir
_print Directory created
```

### _fs_cd

```bash
// Change directory
_fs_cd /home/user
_fs_pwd  // Show current directory
```

### _fs_pwd

```bash
// Print working directory
_fs_pwd
```

### _sys_whoami

```bash
// Get current username
_print Current user: _sys_whoami

// Store in variable
_setvar(user, _sys_whoami)
_print User: _getvar(user)
```

### _sys_whatami

```bash
// Get execution context type
_print Context: _sys_whatami

// Store in variable
_setvar(context, _sys_whatami)
_print Running in: _getvar(context)
```

### _fs_find

```bash
// Find files by name
_fs_find /home test

// Find with pattern
_fs_find /etc conf

// Search file contents
_fs_find /home password -c

// Exact filename match
_fs_find /var config.txt -e
```

### _sleep

```bash
// Wait 2 seconds
_print Starting...
_sleep 2
_print Done!
```

### _exit

```bash
// Exit with code 0 (success)
_exit 0

// Exit with error code
if _getvar(error) == 1
  _print Fatal error occurred
  _exit 1
endif
```

### Complex File Operations Example

```bash
// File management script
_print ==== FILE MANAGER ====

// Create directory structure
_fs_mkdir project
_fs_cd project
_fs_mkdir src
_fs_mkdir docs

// Create files
_fs_write src/main.txt Main application code
_fs_write docs/readme.txt Project documentation

// Read and display
_print ==== MAIN FILE ====
_fs_view src/main.txt

_print ==== README FILE ====
_fs_view docs/readme.txt

// Find files
_print ==== FINDING FILES ====
_fs_find . txt

// Display current location
_print Current directory: _fs_pwd
_print User: _sys_whoami
```

---

## GreyHack Network Commands

### _net_ports

```bash
// Scan IP for open ports
_net_ports 192.168.1.1

// Output:
// Found 3 open port(s) on 192.168.1.1
//   [OPEN] Port 22 - SSH 1.0
//   [OPEN] Port 80 - HTTP 2.0
//   [OPEN] Port 443 - HTTPS 2.0
```

### _net_devices

```bash
// List devices on LAN
_net_devices 192.168.1.1

// Output:
// Found 5 device(s) on LAN:
//   [DEVICE] 192.168.1.10
//   [DEVICE] 192.168.1.20
//   [DEVICE] 192.168.1.30
//   [DEVICE] 192.168.1.40
//   [DEVICE] 192.168.1.50
```

### _net_router

```bash
// Display router information
_net_router 192.168.1.1

// Output:
// === Router Information ===
// Local IP: 192.168.1.1
// Public IP: 203.0.113.1
// BSSID: Router_ABC
// ESSID: MyNetwork
// Kernel Version: 2.0.1
// Used Ports: 3
```

### _net_devports

```bash
// Show ports for specific device
_net_devports 192.168.1.1 192.168.1.10

// Output:
// Device 192.168.1.10 has 2 open port(s):
//   [OPEN] Port 22 - SSH 1.0
//   [OPEN] Port 80 - HTTP 2.0
```

### _net_fwrules

```bash
// Display firewall rules
_net_fwrules 192.168.1.1

// Output:
// === Firewall Rules ===
// [1] ALLOW 192.168.1.0/24 port 80
// [2] DENY 0.0.0.0/0 port 22
// [3] ALLOW 192.168.1.10 port 3306
```

### _net_random

```bash
// Get random reachable router IP
_setvar(target, _net_random)
_print Scanning: _getvar(target)
_net_ports _getvar(target)
```

### _net_ping

```bash
// Check if host is reachable
_net_ping 192.168.1.1
```

### _net_port

```bash
// Check if specific port is open
_net_port 192.168.1.1 22
_net_port 192.168.1.1 80
```

### _sys_procs

```bash
// Show running processes
_sys_procs
```

### _sys_kill

```bash
// Terminate process by PID
_sys_kill 1234
```

### _fs_canwrite / _fs_canexec

```bash
// Check file permissions (returns 1 if permitted, 0 if not)
if _fs_canwrite(/home/user/file.txt)
  _print Can write to file
endif

if _fs_canexec(/bin/program)
  _print Can execute program
endif
```

Pass `"file"` as the second argument to get the file object back instead of 1/0 — useful when you want to immediately work with the file:

```bash
// Return file object instead of 1/0
_setvar(f, _fs_canwrite(/tmp/output.txt, "file"))
if _getvar(f)
  _print Size: _getvar(f).size
  _print Owner: _getvar(f).owner
endif

_setvar(f, _fs_canexec(/usr/bin/tool, "file"))
if _getvar(f)
  _print Name: _getvar(f).name
endif
```

### Complete Network Scanner Example

**Complete Script - Copy and Run:**

```bash
// Script: network_scanner

_print ==== NETWORK SCANNER ====

// Get random target or use specific IP
_setvar(use_random, get_integer(Use random IP? (1=yes, 0=no):))

if _getvar(use_random) == 1
  _setvar(target, _net_random)
  _print Targeting random IP: _getvar(target)
else
  _setvar(target, get_string(Enter target IP:))
endif

// Ping host
_print Checking if host is reachable...
_net_ping _getvar(target)

// Scan ports
_print Scanning ports...
_net_ports _getvar(target)

// Get router info
_print Getting router information...
_net_router _getvar(target)

// List LAN devices
_print Finding LAN devices...
_net_devices _getvar(target)

// Check common ports
_print Checking common ports:
for port in [21, 22, 23, 25, 80, 443, 3306, 8080]
  _print Checking port _getvar(port)...
  _net_port _getvar(target) _getvar(port)
endfor

// Display firewall rules
_print Checking firewall rules...
_net_fwrules _getvar(target)

_print Scan complete!
```

---

## Advanced Features

### Command Chaining: `;` and `&&`

Two operators let you put multiple commands on one line:

**`;` (semicolon)** — Always executes both sides, regardless of success or failure:

```bash
// Both commands always run
_setvar(x, 10); _setvar(y, 20); _print Sum: _getvar(x) + _getvar(y)

// Useful for compact scripts
_setvar(name, Alice); _print Hello _getvar(name)
```

**`&&` (conditional AND)** — Only executes the right side if the left side **succeeded** (no error):

```bash
// Second command only runs if first succeeds
_fs_cd /root && _print Entered root directory

// Chain multiple — stops at first failure
echo hello && echo world && echo done

// Mix with pipes
echo hello | rev && echo Previous pipe succeeded
```

**Combining `;` and `&&`:**

```bash
// ; separates independent groups, && chains conditionally within
echo A && echo B ; echo C && echo D
// A runs, if A succeeds then B
// C always runs (new ; group), if C succeeds then D
```

### _print vs _printnow

```bash
// _print — buffered output, prints in execution order with other queued commands
_print Hello World

// _printnow — immediate output, bypasses the command queue
_printnow Status: Processing...
```

Use `_printnow` when you need output to appear immediately (e.g., progress indicators) rather than waiting for the command queue to flush.

### _return vs return

These two keywords do completely different things:

**`_return value`** — returns a value from a **function** to its caller. Use it inside `func`/`endfunc` blocks:

```bash
func add(a, b)
  _return _getvar(a) + _getvar(b)
endfunc

_setvar(sum, add(3, 4))   // sum = 7
```

**`return [message]`** — exits the **entire script** early. The optional message is printed (or executed as a command if it starts with a known command name):

```bash
// Exit script with message
if _getvar(error) == 1
  return red(Fatal error - exiting)
endif

// Exit with colored output
if not file_exists(/etc/passwd)
  return blue(Info:) File not found
endif

// Exit silently
if _getvar(done) == 1
  return
endif
```

> **Key rule**: Use `_return` inside functions. Use `return` to exit the whole script.

### Property Access (Dot Notation)

Access properties on objects returned by system functions using dot notation:

```bash
// File object properties
_setvar(file, _fs_read(/etc/passwd, file))
_print Path: _getvar(file).path
_print Name: _getvar(file).name
_print Size: _getvar(file).size
_print Permissions: _getvar(file).permissions
_print Owner: _getvar(file).owner
```

Supported property types:
- **File objects**: `.path`, `.name`, `.permissions`, `.owner`, `.group`, `.size`, `.is_folder`, `.is_binary`, `.is_symlink`, `.parent`
- **Computer objects**: `.local_ip`, `.public_ip`
- **Shell objects**: `.host_computer`
- **Maps**: Any key — `_getvar(config).api_key`

Nested property access also works: `_getvar(obj).home.path`

**Note:** IP addresses like `192.168.1.1` are not treated as property access — they are preserved as strings.

### _fs_put / _fs_get (Remote File Transfer)

Transfer files between local and remote systems over an active shell connection:

```bash
// Upload local file to remote system
_fs_put /home/user/payload.src /tmp/payload.src

// Download remote file to local system
_fs_get /etc/passwd /home/user/loot/passwd
```

Both require an active remote shell connection. `_fs_put` uploads from the local machine to the connected remote. `_fs_get` downloads from the remote to the local machine.

### Loop & Try/Catch State Across Pivots

When a bash script running inside a loop or try/catch block executes a pivot command (`proxy -q`, `ssh`), the loop/try state is automatically preserved. After the pivot session ends, execution resumes at the correct point in the loop — including advancing to the next iteration.

```bash
// This script pivots into each target, runs a command, and continues the loop
for target in [192.168.1.10, 192.168.1.20, 192.168.1.30]
  proxy -q _getvar(target)
  _print Connected to _getvar(target)
  // ... commands run on the remote ...
endfor
_print All targets processed
```

Try/catch error state is also preserved: if a pivot occurs inside a `try` block, the catch handler remains active in the new session.

### $STDIN — Pipeline Input

Scripts can receive piped input via the `$STDIN` placeholder. When the script is called with a pipe (`echo hello | run myscript`), `$STDIN` is replaced with the piped value before execution:

```bash
// Script: greet
// Run with: echo Alice | run greet
_print Hello, $STDIN!
```

If the script contains `$STDIN` but is run without a pipe, the user is prompted with `STDIN: ` to enter a value interactively.

```bash
// Script: process_line
// Run with pipe: echo hello world | run process_line
// Or standalone: run process_line  (prompts for STDIN)
_print Processing: $STDIN
_print Length: len($STDIN)
```

`$STDIN` substitution happens before execution, so it works in any expression or command — including conditions, assignments, and function arguments.

### _hold and OBJ Object Dispatch

Headless scanner operations (e.g., `scan`, `brute`) can leave a "held object" (such as a remote shell or exploit result) in `FLAGS["hold"]`. The `_hold` command and `OBJ()` dispatch syntax let scripts capture and reuse these objects.

**`_hold`** — stores the current held object (command form, prints confirmation):

```bash
// After a scan or brute that sets a held object:
_hold               // stores it into FLAGS["hold"]
```

**`_setvar(name, _hold)`** — captures the held object into a named variable:

```bash
_setvar(myshell, _hold)     // myshell now holds the shell/exploit object
```

**`OBJ(name) cmd [args]`** — dispatches a command to the stored object:

```bash
_setvar(myshell, _hold)
OBJ(myshell) whoami          // run whoami via the stored shell
OBJ(myshell) _fs_find /etc passwd   // run _fs_find on the remote
OBJ(myshell) home            // close the shell and set myshell to null
OBJ(myshell) exit            // same as home
```

This pattern allows automation scripts to open a shell once, reuse it across multiple commands, and clean up properly at the end.

### String Concatenation with +

The `+` operator performs numeric addition when both operands are numbers, and string concatenation when the left operand is a non-numeric string:

```bash
_setvar(a, 10)
_setvar(b, 20)
_setvar(sum, _getvar(a) + _getvar(b))   // sum = 30 (numeric)

_setvar(prefix, Total: )
_setvar(msg, _getvar(prefix) + _getvar(sum))  // msg = "Total: 30" (string concat)

// Building strings with +
_setvar(ip, 192.168.1.)
_setvar(host, _getvar(ip) + 100)   // host = "192.168.1.100"
```

When you need explicit concatenation regardless of types, prefer `concat(a, b, ...)` for clarity.

### Color Functions

All color functions wrap text with terminal color codes. Use them directly inside `_print`, `_printnow`, or `return` statements:

```bash
_print cyan(Status:) green(OK)
_print red(ERROR) Something went wrong
_print bold(Important:) This stands out
```

Full color palette:

| Function | Appearance |
|----------|------------|
| `red(text)` | Red |
| `green(text)` | Green |
| `blue(text)` | Blue |
| `cyan(text)` | Cyan |
| `yellow(text)` | Yellow |
| `orange(text)` | Orange |
| `magenta(text)` | Magenta/Pink |
| `lime(text)` | Lime green |
| `white(text)` | White |
| `grey(text)` | Grey |
| `black(text)` | Black |
| `purple(text)` | Purple |
| `liteblue(text)` | Light blue |
| `liteGrey(text)` | Light grey |
| `iyellow(text)` | Intense yellow |
| `bred(text)` | Bright red |
| `error(text)` | Error style (red) |
| `password(text)` | Password style |
| `bold(text)` | Bold text |

Colors can be nested, but nested colors may not render as expected in all terminal environments.

### pause

Pause script execution and wait for the user to press Enter before continuing:

```bash
_print About to do something important...
pause
_print Continuing...
```

### Complete Application Example

**Complete Script - Copy and Run:**

```bash
// Script: user_management
// Full application - copy entire script!

_print ========================================
_print       USER MANAGEMENT SYSTEM
_print ========================================

// Initialize user database
_setvar(users, [])
_setvar(running, 1)

// Main menu loop
while _getvar(running) == 1
  _print
  _print ==== MAIN MENU ====
  _print 1. Add User
  _print 2. List Users
  _print 3. Search User
  _print 4. Delete User
  _print 5. Exit
  _print
  
  _setvar(choice, get_integer(Enter choice:))
  
  switch _getvar(choice)
    case 1
      _print ==== ADD USER ====
      _setvar(username, get_string(Username:))
      _setvar(age, get_integer(Age:))
      _setvar(email, get_string(Email:))
      
      // Validation
      if len(_getvar(username)) < 3
        _print red(Error:) Username too short
        continue
      endif
      
      if _getvar(age) < 13
        _print red(Error:) Must be 13 or older
        continue
      endif
      
      // Create user record
      _setvar(user_record, concat(_getvar(username), |, _getvar(age), |, _getvar(email)))
      _push users _getvar(user_record)
      
      _print green(Success!) User added
      
    case 2
      _print ==== USER LIST ====
      _len users
      _print Total users:
      
      _setvar(index, 1)
      for user in users
        _print _getvar(index). _getvar(user)
        _setvar(index, _getvar(index) + 1)
      endfor
      
    case 3
      _print ==== SEARCH USER ====
      _setvar(search_name, get_string(Username to search:))
      _setvar(found, 0)
      
      for user in users
        if contains(_getvar(user), _getvar(search_name))
          _print Found: _getvar(user)
          _setvar(found, 1)
        endif
      endfor
      
      if _getvar(found) == 0
        _print yellow(Not found)
      endif
      
    case 4
      _print ==== DELETE USER ====
      _print Not implemented yet
      
    case 5
      _print Goodbye!
      _setvar(running, 0)
      
    default
      _print red(Error:) Invalid choice
  endswitch
endwhile

_print System exited
```

### Data Processing Example

**Complete Script - Copy and Run:**

```bash
// Script: log_analyzer

_print ==== LOG ANALYZER ====

// Read log file
_setvar(log_content, _fs_read(system.log))

if _getvar(log_content) == ""
  _print red(Error:) Could not read log file
  exit 1
endif

// Count different log levels
_setvar(error_count, 0)
_setvar(warning_count, 0)
_setvar(info_count, 0)

// Parse log (simplified)
_print Processing log entries...

// Display statistics
_print ==== STATISTICS ====
_print Error count: _getvar(error_count)
_print Warning count: _getvar(warning_count)
_print Info count: _getvar(info_count)

// Generate report
_setvar(report_file, log_report.txt)
_fs_write _getvar(report_file) Log Analysis Report
_fs_write _getvar(report_file) Errors: _getvar(error_count)
_fs_write _getvar(report_file) Warnings: _getvar(warning_count)
_fs_write _getvar(report_file) Info: _getvar(info_count)

_print Report saved to: _getvar(report_file)
```

### Game Example

**Complete Script - Copy and Run:**

```bash
// Script: guessing_game
// Fun game - copy entire script!

_print ========================================
_print         NUMBER GUESSING GAME
_print ========================================

_setvar(secret, random(1, 100))
_setvar(tries, 0)
_setvar(max_tries, 10)

_print I'm thinking of a number between 1 and 100
_print You have _getvar(max_tries) tries

while _getvar(tries) < _getvar(max_tries)
  _setvar(tries, _getvar(tries) + 1)
  _setvar(remaining, _getvar(max_tries) - _getvar(tries) + 1)
  
  _print
  _print Try _getvar(tries)/_getvar(max_tries)
  _setvar(guess, get_integer(Your guess:))
  
  if _getvar(guess) == _getvar(secret)
    _print green(CORRECT!) You found it in _getvar(tries) tries
    exit 0
  elif _getvar(guess) < _getvar(secret)
    _print blue(Too low!) Try higher
  else
    _print yellow(Too high!) Try lower
  endif
  
  if _getvar(remaining) > 0
    _print You have _getvar(remaining) tries left
  endif
endwhile

_print red(Game Over!) The number was _getvar(secret)
```

---

## Best Practices

### 1. Use Meaningful Variable Names

```bash
// Good
_setvar(user_age, 25)
_setvar(total_price, 99.99)

// Bad
_setvar(x, 25)
_setvar(y, 99.99)
```

### 2. Comment Your Code

```bash
// Calculate discount
_setvar(price, 100)
_setvar(discount_rate, 0.15)
_setvar(discount, _getvar(price) * _getvar(discount_rate))
_setvar(final_price, _getvar(price) - _getvar(discount))
```

### 3. Validate User Input

```bash
_setvar(age, get_integer(Enter age:))

if _getvar(age) < 0 or _getvar(age) > 150
  _print Invalid age
  exit 1
endif
```

### 4. Use Functions for Reusable Code

```bash
// Define once, use multiple times
func calculate_tax(amount)
  _setvar(tax_rate, 0.08)
  _setvar(tax, _getvar(amount) * _getvar(tax_rate))
  _return _getvar(tax)
endfunc

_setvar(tax1, calculate_tax(100))
_setvar(tax2, calculate_tax(200))
```

### 5. Handle Errors Gracefully

```bash
if not file_exists(/etc/passwd)
  _print red(Error:) File not found
  return
endif

_setvar(content, _fs_read(/etc/passwd))
_print File loaded successfully
```

---

## Troubleshooting

### Common Errors

**Variable not found:**
```bash
// Wrong
_print _getvar(undefined_var)

// Right
_setvar(my_var, value)
_print _getvar(my_var)
```

**Missing endif/endfor/endwhile:**
```bash
// Wrong
if _getvar(x) == 1
  _print Yes

// Right
if _getvar(x) == 1
  _print Yes
endif
```

**Type mismatch:**
```bash
// Wrong
_setvar(age, twenty-five)
if _getvar(age) > 18  // Error: string comparison

// Right
_setvar(age, 25)
if _getvar(age) > 18  // OK: number comparison
```

---

## Conclusion

This guide covers all features of the Bash Script Execution System with extensive examples. For more specific use cases, refer to the individual sections above. Happy scripting!

**Quick Reference:**
- Variables: `_setvar(name, value)` and `_getvar(name)`
- Loops: `for`, `while`, `until`
- Conditionals: `if/elif/else/endif`
- Functions: `func name(params) ... endfunc`
- Arrays: `_push`, `_pop`, `_pull`, `_len`
- I/O: `_print`, `_fs_read`, `_fs_write`
- Network: `_net_ports`, `_net_devices`, `_net_router`
- Type Casting: `to_string()`, `to_int()`, `to_float()`, `typeof()`

---

## Appendix: Complete Tutorial Script

The file `learn_bash.src` is a comprehensive, runnable tutorial that exercises every major feature of x bash. Run it with `@test` to verify the entire bash engine works correctly. Every example defines a function, calls it, and prints results with self-checking `[PASS]`/`[FAIL]` assertions.

### Chapters Covered

| Chapter | Topics |
|---------|--------|
| 1. Fundamentals | Hello world, variables, arithmetic, lists |
| 2. Functions | Parameters, return values, void, scope, recursion |
| 3. Control Flow | if/elif/else, for, while, until, break/continue, switch |
| 4. Strings | len, upper, lower, substr, contains, replace, split, join |
| 5. Math & Types | floor, ceil, abs, round, min, max, random, type casting |
| 6. System | Environment info, IPs, file system, reading/writing files |
| 7. Scanning | Port scanning, host checking, LAN discovery |
| 8. Programs | Primes, fibonacci, sorting, power, statistics, search |
| 9. Formatting | Terminal colors, formatted reports |
| 10. Advanced | Function composition, state machines, FizzBuzz, call chains |
| 11. Chaining | Nested builtin calls, complex expressions |
| 12. Recon | Port scanner wrappers, router/firewall info |
| 13. Processes | Listing processes, sleep and timing |
| 14. Capstone | Network inventory builder, mega chain, final verification |

### Helper Functions

The script starts with reusable helpers used throughout:

```bash
// Self-checking assertion — prints [PASS] or [FAIL]
func assert(label, actual, expected)
  if _getvar(actual) == _getvar(expected)
    _print   [PASS] _getvar(label)
  else
    _print   [FAIL] _getvar(label)  expected: _getvar(expected)  got: _getvar(actual)
  endif
endfunc

// Section headers and tips
func printHeader(title)
  _print
  _print ============================================
  _print   _getvar(title)
  _print ============================================
endfunc

func printLesson(title)
  _print
  _print --- _getvar(title) ---
endfunc
```

### Selected Examples

#### Variables & Arithmetic (Chapter 1)

```bash
func showArithmetic()
  _setvar(a, 10)
  _setvar(b, 3)
  _setvar(sum, _getvar(a) + _getvar(b))
  _print   10 + 3 = _getvar(sum)
  _setvar(pow, 2 ** 10)
  _print   2 ** 10 = _getvar(pow)
endfunc

func testArithmetic()
  _setvar(r, 7 + 3)
  assert(7+3 equals 10, _getvar(r), 10)
  _setvar(r, 6 * 7)
  assert(6x7 equals 42, _getvar(r), 42)
  _setvar(r, 2 ** 8)
  assert(2pow8 equals 256, _getvar(r), 256)
endfunc
```

#### Recursion (Chapter 2)

```bash
func factorial(n)
  if _getvar(n) <= 1
    _return 1
  else
    _setvar(prev, factorial(_getvar(n) - 1))
    _return _getvar(n) * _getvar(prev)
  endif
endfunc

_setvar(r, factorial(5))
assert(factorial(5) is 120, _getvar(r), 120)
```

#### While Loops — Collatz Conjecture (Chapter 3)

```bash
func collatzSteps(n)
  _setvar(steps, 0)
  while _getvar(n) != 1
    if _getvar(n) % 2 == 0
      _setvar(n, _getvar(n) / 2)
    else
      _setvar(n, _getvar(n) * 3 + 1)
    endif
    _setvar(steps, _getvar(steps) + 1)
  endwhile
  _return _getvar(steps)
endfunc

assert(collatz(6) takes 8 steps, collatzSteps(6), 8)
assert(collatz(27) takes 111 steps, collatzSteps(27), 111)
```

#### String Manipulation (Chapter 4)

```bash
func reverseStr(s)
  _setvar(out, )
  _setvar(i, len(_getvar(s)) - 1)
  while _getvar(i) >= 0
    _setvar(ch, substr(_getvar(s), _getvar(i), _getvar(i) + 1))
    _setvar(out, concat(_getvar(out), _getvar(ch)))
    _setvar(i, _getvar(i) - 1)
  endwhile
  _return _getvar(out)
endfunc

func isPalindrome(s)
  _setvar(rev, reverseStr(_getvar(s)))
  if _getvar(s) == _getvar(rev)
    _return 1
  else
    _return 0
  endif
endfunc

assert(elle is palindrome, isPalindrome(elle), 1)
assert(hello is not palindrome, isPalindrome(hello), 0)
```

#### File System Operations (Chapter 6)

```bash
func writeDemo()
  _fs_mkdir tmp_test
  _fs_cd tmp_test
  _fs_write hello.txt Hello from x bash!
  _setvar(contents, file_read(hello.txt))
  _print   Contents: _getvar(contents)
  _fs_cd ..
endfunc
```

#### Network Inventory (Chapter 14)

```bash
func buildInventory()
  _setvar(myIP, get_publicIP())
  _setvar(myLAN, get_lanIP())
  _setvar(user, get_user())
  _setvar(dt, date())

  _print   +=== NETWORK INVENTORY ===+
  _print   User: _getvar(user)
  _print   LAN: _getvar(myLAN)
  _print   Public: _getvar(myIP)

  _setvar(ports, _net_ports _getvar(myIP))
  if _getvar(ports)
    for port in _getvar(ports)
      _print     - _getvar(port)
    endfor
  endif
  _print   +=== END INVENTORY ===+
endfunc
```

### Running the Tutorial

```bash
@test
```

Expected: all lines show `[PASS]`. If any show `[FAIL]`, something in the bash engine needs attention.

See `Bash/tests/learn_bash.src` for the full source (~2600 lines, 14 chapters, ~150 assertions).