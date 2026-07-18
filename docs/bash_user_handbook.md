# Bash User Handbook
## Your Complete Guide to Writing Scripts in X

**Welcome!** This handbook teaches you how to write bash scripts in X, even if you've never programmed before. You'll start with simple scripts and work your way up to powerful automation tools.

---

## Table of Contents

1. [What Are Bash Scripts?](#what-are-bash-scripts)
2. [Your First Script](#your-first-script)
3. [Working with Variables](#working-with-variables)
4. [Getting User Input](#getting-user-input)
5. [Making Decisions (If/Else)](#making-decisions-ifelse)
6. [Repeating Actions (Loops)](#repeating-actions-loops)
7. [Creating Functions](#creating-functions)
8. [Error Handling (Try/Catch)](#error-handling-trycatch)
9. [Script Arguments & Flags](#script-arguments--flags)
10. [Working with Lists](#working-with-lists)
11. [Math Operations](#math-operations)
12. [Working with Files](#working-with-files)
13. [Network Operations](#network-operations)
14. [Useful Built-in Functions](#useful-built-in-functions)
15. [Common Script Examples](#common-script-examples)
16. [Tips & Tricks](#tips--tricks)
17. [Troubleshooting](#troubleshooting)
18. [Appendix: Complete Tutorial Script](#appendix-complete-tutorial-script)

---

## What Are Bash Scripts?

**Bash scripts** are files that contain a series of commands that execute automatically. Instead of typing commands one by one, you write them once in a script and run them anytime!

### Why Use Scripts?

- 🚀 **Automation**: Run complex tasks with one command
- 💾 **Reusability**: Write once, use many times
- 🎯 **Consistency**: Do things the same way every time
- ⏱️ **Speed**: Execute 100 commands instantly
- 🔄 **Loops**: Repeat actions without repetition

### How Scripts Work

1. You write commands in a text file
2. Save the file in your bash directory
3. Run it with `run scriptname`
4. The script executes all commands automatically

---

## Your First Script

Let's create your very first script!

### Hello World

Create a file called `hello` in your bash directory:

```bash
// My first script!
_print Hello, World!
```

**Run it:**
```bash
run hello
```

**Output:**
```
Hello, World!
```

🎉 **Congratulations!** You just wrote and ran your first script!

### Simple Greeter

Now let's make it interactive:

```bash
// Simple greeter script
_setvar(name, get_string(Your name:))
_print Nice to meet you, _getvar(name)!
```

**What happens:**
1. Asks you to type your name
2. Stores your name in a variable called `name`
3. Prints a personalized greeting

**Try it:**
```bash
run hello
```

**Output:**
```
Your name: Alice
Nice to meet you, Alice!
```

---

## Working with Variables

Variables store information you want to use later. Think of them as labeled boxes.

### Built-in Variables

Some variables are available automatically in every script — no need to create them:

```bash
// Get computer info and print it
_setvar(ip, COMPUTER.local_ip)
_print Your LAN IP: _getvar(ip)

_setvar(pub, COMPUTER.public_ip)
_print Your public IP: _getvar(pub)

_setvar(host, COMPUTER.get_name)
_print Hostname: _getvar(host)

_setvar(gw, COMPUTER.network_gateway)
_print Gateway: _getvar(gw)

// Root filesystem
_setvar(rpath, ROOT.path)
_print Root path: _getvar(rpath)

// Chain through shell to get computer hostname
_setvar(name, SHELL.host_computer.get_name)
_print Chain hostname: _getvar(name)

// List all folders in root with colors
_setvar(dirs, ROOT.get_folders)
for d in dirs
  _setvar(dn, _getvar(d).name)
  _setvar(dp, _getvar(d).permissions)
  _print liteblue(_getvar(dp)) _getvar(dn)
endfor
```

| Variable | What it gives you |
|----------|-------------------|
| `COMPUTER` | The current computer (`.local_ip`, `.public_ip`, `.get_name`, `.get_ports`, `.active_net_card`, `.is_network_active`, `.network_devices`, `.network_gateway`, `.show_procs`) |
| `SHELL` | The current shell (has `.host_computer`) |
| `ROOT` | The root filesystem (`.path`, `.name`, `.permissions`, `.owner`, `.group`, `.size`, `.is_folder`, `.is_binary`, `.is_symlink`, `.parent`, `.allow_import`, `.get_content`, `.get_files`, `.get_folders`, `.delete`) |

> **Note:** These update automatically when you pivot to another machine via proxy or ssh.
> Access properties using `_setvar(varname, COMPUTER.property)` then `_getvar(varname)` to print.

### Creating Variables

Use `_setvar(name, value)` to create a variable:

```bash
_setvar(username, Alice)
_setvar(age, 25)
_setvar(score, 98.5)
```

### Using Variables

Use `_getvar(name)` to get the value back:

```bash
_print Your name is _getvar(username)
_print You are _getvar(age) years old
_print Your score: _getvar(score)
```

### Complete Example

```bash
// User profile script
_setvar(name, John)
_setvar(age, 30)
_setvar(city, New York)

_print === USER PROFILE ===
_print Name: _getvar(name)
_print Age: _getvar(age)
_print City: _getvar(city)
```

**Output:**
```
=== USER PROFILE ===
Name: John
Age: 30
City: New York
```

### Variable Tips

💡 **Tip 1**: Use descriptive names
- Good: `username`, `total_price`, `user_age`
- Bad: `x`, `temp`, `data`

💡 **Tip 2**: Variables can hold different types
- Text: `_setvar(name, Alice)`
- Numbers: `_setvar(count, 42)`
- Lists: `_setvar(items, [apple, banana])`

---

## Getting User Input

Make your scripts interactive by asking for input!

### Simple Text Input

```bash
_setvar(answer, get_string(What's your favorite color?))
_print Your favorite color is _getvar(answer)
```

### Number Input

```bash
_setvar(age, get_integer(How old are you?))
_print You are _getvar(age) years old
```

### Decimal Number Input

```bash
_setvar(price, get_decimal(Enter price:))
_print The price is $_getvar(price)
```

### Complete Input Example

```bash
// User registration script
_print === REGISTRATION ===

_setvar(username, get_string(Username:))
_setvar(email, get_string(Email:))
_setvar(age, get_integer(Age:))

_print
_print Registration Complete!
_print Username: _getvar(username)
_print Email: _getvar(email)
_print Age: _getvar(age)
```

### Interactive Menus

Show your users a beautiful menu to choose from:

```bash
// Create a menu and get user selection
_setvar(options, [Start Service, Stop Service, View Logs, Exit])
_setvar(choice, menu(_getvar(options), numbers, green))
_print You selected: _getvar(choice)
```

**Menu Syntax:**
```
menu(list, style, color, case_mode)
```

- **list**: Array of options to display
- **style**: `"numbers"` (1, 2, 3...) or `"letters"` (A, B, C...)
- **color**: Color name (`red`, `green`, `blue`, `cyan`, `yellow`, `orange`, `magenta`, `lime`, `white`, `grey`, `black`, `purple`, `liteblue`, `liteGrey`, `iyellow`, `bred`, `error`, `password`, `bold`) or hex code (`#00bfff`, `00bfff`)
- **case_mode** (optional): Letter input mode, `insensitive` (default) or `strict`
  - `insensitive`: accepts lowercase or uppercase letter input
  - `strict`: requires uppercase label input in letters mode

Returns the 0-based index of the selected option.

**Example: Menu with Action**

```bash
_setvar(actions, [Deploy, Rollback, View Status, Exit])
_setvar(selection, menu(_getvar(actions), letters, cyan))

if _getvar(selection) == 0
  _print Deploying...
endif

if _getvar(selection) == 1
  _print Rolling back...
endif

if _getvar(selection) == 2
  _print Checking status...
endif

if _getvar(selection) == 3
  _print Goodbye!
endif
```

**Different Menu Styles:**

```bash
// Number menu (default cyan)
_setvar(items, [Option 1, Option 2, Option 3])
_setvar(num_choice, menu(_getvar(items), numbers))

// Letter menu with colors
_setvar(servers, [Server A, Server B, Server C])
_setvar(server_choice, menu(_getvar(servers), letters, green))

// Letter menu with strict case mode
_setvar(server_choice_strict, menu(_getvar(servers), letters, green, strict))

// Red action menu
_setvar(danger, [Delete All, Wipe Config, Reset System])
_setvar(action, menu(_getvar(danger), numbers, red))
```

---

## Making Decisions (If/Else)

Use `if` statements to make your script do different things based on conditions.

### Basic If

```bash
_setvar(age, 20)

if _getvar(age) >= 18
  _print You are an adult
endif
```

### If with Else

```bash
_setvar(score, 75)

if _getvar(score) >= 60
  _print You passed!
else
  _print You failed
endif
```

### If with Multiple Choices

```bash
_setvar(score, 85)

if _getvar(score) >= 90
  _print Grade: A - Excellent!
elif _getvar(score) >= 80
  _print Grade: B - Good job!
elif _getvar(score) >= 70
  _print Grade: C - Passing
else
  _print Grade: F - Need to study more
endif
```

### Comparison Operators

Use these to compare values:

- `==` - Equal to
- `!=` - Not equal to
- `<` - Less than
- `>` - Greater than
- `<=` - Less than or equal
- `>=` - Greater than or equal

### Combining Conditions

Use `and` and `or` to combine multiple conditions:

```bash
// Checking eligibility
_setvar(age, 25)
_setvar(has_license, 1)

if _getvar(age) >= 18 and _getvar(has_license) == 1
  _print You can drive!
else
  _print You cannot drive yet
endif
```

### Real-World Example: Login System

```bash
// Simple login script
_setvar(username, get_string(Username:))
_setvar(password, get_string(Password:))

if _getvar(username) == admin and _getvar(password) == secret123
  _print green(Login successful!)
  _print Welcome back, admin!
else
  _print red(Login failed!)
  _print Invalid username or password
endif
```

---

## Repeating Actions (Loops)

Loops let you repeat actions without writing the same code over and over.

### For Loop - Simple List

```bash
// Print each fruit
for fruit in [Apple, Banana, Cherry]
  _print I like _getvar(fruit)
endfor
```

**Output:**
```
I like Apple
I like Banana
I like Cherry
```

### For Loop - Counting

```bash
// Count from 1 to 5
for i in range(1, 5)
  _print Count: _getvar(i)
endfor
```

**Output:**
```
Count: 1
Count: 2
Count: 3
Count: 4
Count: 5
```

### While Loop

Repeat while a condition is true:

```bash
_setvar(count, 1)

while _getvar(count) <= 5
  _print Number: _getvar(count)
  _setvar(count, _getvar(count) + 1)
endwhile
```

### Until Loop

Repeat until a condition becomes true:

```bash
_setvar(tries, 0)

until _getvar(tries) >= 3
  _print Attempt: _getvar(tries)
  _setvar(tries, _getvar(tries) + 1)
enduntil
```

### Real-World Example: Menu System

```bash
// Simple menu
_setvar(running, 1)

while _getvar(running) == 1
  _print
  _print === MENU ===
  _print 1. Say Hello
  _print 2. Show Date
  _print 3. Exit
  
  _setvar(choice, get_integer(Choose:))
  
  if _getvar(choice) == 1
    _print Hello there!
  elif _getvar(choice) == 2
    _print Current time: timestamp()
  elif _getvar(choice) == 3
    _print Goodbye!
    _setvar(running, 0)
  else
    _print Invalid choice
  endif
endwhile
```

### Breaking Out Early

Use `break` to exit a loop:

```bash
// Find a number
for i in range(1, 100)
  if _getvar(i) == 50
    _print Found it!
    break
  endif
endfor
```

Use `continue` to skip to the next iteration:

```bash
// Print only even numbers
for i in range(1, 10)
  _setvar(remainder, _getvar(i) % 2)
  if _getvar(remainder) != 0
    continue
  endif
  _print _getvar(i) is even
endfor
```

---

## Creating Functions

Functions are reusable blocks of code with a name. Write once, use anywhere!

### Simple Function

```bash
// Define the function
func greet
  _print Hello from my function!
endfunc

// Use the function
greet
greet
greet
```

**Output:**
```
Hello from my function!
Hello from my function!
Hello from my function!
```

### Function with Parameters

```bash
// Function that says hello to someone
func say_hello(name)
  _print Hello, _getvar(name)!
  _print Nice to meet you!
endfunc

// Use it with different names
say_hello(Alice)
say_hello(Bob)
say_hello(Charlie)
```

**Output:**
```
Hello, Alice!
Nice to meet you!
Hello, Bob!
Nice to meet you!
Hello, Charlie!
Nice to meet you!
```

### Function That Returns a Value

```bash
// Calculate area
func calculate_area(width, height)
  _setvar(area, _getvar(width) * _getvar(height))
  _return _getvar(area)
endfunc

// Use the function
_setvar(room_area, calculate_area(10, 15))
_print Room area: _getvar(room_area) square feet
```

### Real-World Example: Password Validator

```bash
// Password validator function
func validate_password(password)
  _setvar(length, len(_getvar(password)))
  
  if _getvar(length) < 8
    _print red(Password too short!)
    _return 0
  endif
  
  if _getvar(length) > 20
    _print red(Password too long!)
    _return 0
  endif
  
  _print green(Password valid!)
  _return 1
endfunc

// Use the validator
_setvar(pw, get_string(Enter password:))
_setvar(is_valid, validate_password(_getvar(pw)))

if _getvar(is_valid) == 1
  _print Creating account...
else
  _print Please try again
endif
```

---

## Error Handling (Try/Catch)

Sometimes things go wrong — a file doesn't exist, a network command fails, or you want to throw your own errors. Wrap risky code in `try`/`catch` to handle errors gracefully instead of crashing.

### Basic Try/Catch

```bash
try
  _print Attempting something risky...
  wipe /nonexistent/path
catch err
  _print yellow(Caught an error:) _getvar(err)
endtry
_print Script continues normally!
```

**What happens:**
1. The code inside `try` runs
2. If an error occurs, execution jumps to `catch`
3. The error message is stored in `err` (optional — you can omit it)
4. Code after `end try` always runs

### Throwing Your Own Errors

Use `_throw` to trigger the catch block manually:

```bash
func divide(a, b)
  if _getvar(b) == 0
    _throw Cannot divide by zero!
  endif
  _return _getvar(a) / _getvar(b)
endfunc

try
  _setvar(result, divide(10, 0))
  _print Result: _getvar(result)
catch err
  _print red(Error:) _getvar(err)
endtry
// Output: Error: Cannot divide by zero!
```

### Catch Without Variable

If you don't need the error message:

```bash
try
  _throw something bad happened
catch
  _print An error occurred, but we handled it
endtry
```

> **Note:** `end try` also works, but `endtry` is preferred for consistency with `endif`, `endfor`, etc. Try/catch blocks can be nested.

---

## Script Arguments & Flags

### Passing Arguments

Pass values to your script when you run it:

```bash
run myscript Alice 25
```

Inside the script, use `$1`, `$2`, etc.:

```bash
// Script: myscript
_print Hello $1, you are $2 years old!
// Output: Hello Alice, you are 25 years old!
```

### Reading from a Pipe with $STDIN

Your script can receive piped input using the `$STDIN` placeholder. Any place you write `$STDIN` in your script, it gets replaced with whatever was piped in:

```bash
// Script: shout
// Run with: echo hello world | run shout
_print upper($STDIN)
// Output: HELLO WORLD
```

If you run the script without piping anything, it will prompt you to type the input:

```bash
run shout
// Prompts: STDIN: 
// Then you type and press Enter
```

`$STDIN` works anywhere in the script — conditions, function calls, variable assignments:

```bash
// Script: check_ip
_setvar(target, $STDIN)
if _isValidIP(_getvar(target))
  _net_ports _getvar(target)
else
  _print red(Invalid IP:) $STDIN
endif
```

### Script Flags

Add flags anywhere in your script to control behavior:

```bash
--DEBUG
--SIGBREAK
// Your script code here...
_print Running with debug output!
```

| Flag | What It Does |
|------|-------------|
| `--DEBUG` | Shows step-by-step execution details |
| `--ALLOWABS` | Allows absolute file paths (normally restricted) |
| `--SIGBREAK` | Break out of script on warnings |
| `--SIGCONT` | Continue running on warnings |

Flags can also be passed on the command line: `run --DEBUG myscript`

---

## Working with Lists

Lists (arrays) store multiple values in one variable.

### Creating Lists

```bash
// Empty list
_setvar(items, [])

// List with values
_setvar(fruits, [Apple, Banana, Cherry])
_setvar(numbers, [1, 2, 3, 4, 5])
```

### Adding Items (Push)

Add items to the end of a list:

```bash
_setvar(cart, [])

_push cart Laptop
_push cart Mouse
_push cart Keyboard

// cart now has 3 items
```

### Removing from End (Pop)

```bash
_setvar(stack, [A, B, C, D])

_pop stack  // Removes D
_pop stack  // Removes C

// stack now has [A, B]
```

### Removing from Start (Pull)

```bash
_setvar(queue, [First, Second, Third])

_pull queue  // Removes First

// queue now has [Second, Third]
```

### Checking List Size

```bash
_setvar(items, [A, B, C])
_len items  // Returns 3
```

### Checking if Value Exists

**Command style** (passes variable by name):
```bash
_setvar(colors, [red, green, blue])

_in colors blue    // Returns true
_in colors yellow  // Returns false
```

**Function style** (passes resolved list via `_getvar`, usable inside `_setvar` and expressions):
```bash
_setvar(colors, [red, green, blue])

_setvar(found, _in(_getvar(colors), blue))   // found = 1
_setvar(found, _in(_getvar(colors), yellow)) // found = 0
```

### Looping Through Lists

```bash
_setvar(fruits, [Apple, Banana, Cherry, Orange])

_print My favorite fruits:
for fruit in fruits
  _print - _getvar(fruit)
endfor
```

### Real-World Example: Shopping Cart

```bash
// Shopping cart manager
_setvar(cart, [])

_print === SHOPPING CART ===

// Add items
_push cart Laptop
_print Added: Laptop

_push cart Mouse  
_print Added: Mouse

_push cart Keyboard
_print Added: Keyboard

// Show cart
_print
_print Your cart:
for item in cart
  _print - _getvar(item)
endfor

// Show total items
_print
_print Total items: len(_getvar(cart))

// Remove last item
_pop cart
_print
_print Removed last item
_print Items remaining: len(_getvar(cart))
```

---

## Math Operations

Do calculations in your scripts!

### Basic Operations

```bash
_setvar(a, 10)
_setvar(b, 3)

// Addition
_setvar(sum, _getvar(a) + _getvar(b))
_print Sum: _getvar(sum)

// Subtraction  
_setvar(diff, _getvar(a) - _getvar(b))
_print Difference: _getvar(diff)

// Multiplication
_setvar(product, _getvar(a) * _getvar(b))
_print Product: _getvar(product)

// Division
_setvar(quotient, _getvar(a) / _getvar(b))
_print Quotient: _getvar(quotient)

// Remainder (Modulo)
_setvar(remainder, _getvar(a) % _getvar(b))
_print Remainder: _getvar(remainder)

// Power
_setvar(power, _getvar(a) ** 2)
_print Power: _getvar(power)
```

### Math Functions

```bash
// Absolute value
_setvar(negative, -42)
_setvar(positive, abs(_getvar(negative)))
_print Absolute: _getvar(positive)

// Rounding
_setvar(price, 19.99)
_print Rounded down: floor(_getvar(price))
_print Rounded up: ceil(_getvar(price))
_print Rounded nearest: round(_getvar(price))

// Random number
_setvar(dice, random(1, 6))
_print You rolled: _getvar(dice)

// Min and Max
_print Minimum: min(5, 10)
_print Maximum: max(5, 10)
```

### Real-World Example: Calculator

```bash
// Simple calculator
_print === CALCULATOR ===

_setvar(num1, get_decimal(First number:))
_setvar(num2, get_decimal(Second number:))

_print
_print Results:
_print Addition: _getvar(num1) + _getvar(num2) = calc(_getvar(num1) + _getvar(num2))
_print Subtraction: _getvar(num1) - _getvar(num2) = calc(_getvar(num1) - _getvar(num2))
_print Multiplication: _getvar(num1) * _getvar(num2) = calc(_getvar(num1) * _getvar(num2))
_print Division: _getvar(num1) / _getvar(num2) = calc(_getvar(num1) / _getvar(num2))

// Store the actual calculations
_setvar(sum, _getvar(num1) + _getvar(num2))
_setvar(diff, _getvar(num1) - _getvar(num2))
_setvar(prod, _getvar(num1) * _getvar(num2))
_setvar(quot, _getvar(num1) / _getvar(num2))

_print
_print Sum: _getvar(sum)
_print Difference: _getvar(diff)
_print Product: _getvar(prod)
_print Quotient: _getvar(quot)
```

### Real-World Example: Shopping Total

```bash
// Calculate shopping total with tax
_print === SHOPPING TOTAL ===

_setvar(price, get_decimal(Item price:))
_setvar(quantity, get_integer(Quantity:))

_setvar(subtotal, _getvar(price) * _getvar(quantity))
_setvar(tax, _getvar(subtotal) * 0.08)
_setvar(total, _getvar(subtotal) + _getvar(tax))

_print
_print Subtotal: $_getvar(subtotal)
_print Tax (8%): $_getvar(tax)
_print Total: $_getvar(total)
```

---

## Working with Files

Read, write, and manage files in your scripts.

### Reading Files

```bash
// Read entire file
_setvar(content, _fs_read(/etc/passwd))
_print _getvar(content)
```

### Writing Files

```bash
// Write to a file
_fs_write myfile.txt Hello, World!

// Write variable content
_setvar(message, This is my message)
_fs_write output.txt _getvar(message)
```

### Viewing Files

```bash
// Display file contents
_fs_view /etc/passwd
```

### File Information

```bash
// Check if file exists
if file_exists(/etc/passwd)
  _print File exists!
else
  _print File not found
endif

// Check if it's a folder
if is_folder(/home)
  _print It's a directory
else
  _print It's a file
endif

// Check if it's binary
if is_binary(/bin/program)
  _print Binary file
else
  _print Text file
endif
```

### Creating Directories

```bash
_fs_mkdir myfolder
_print Created folder: myfolder
```

### Navigation

```bash
// Change directory
_fs_cd /home/user

// Show current directory
_fs_pwd

// Show current user
_print Current user: _sys_whoami
```

### Finding Files

```bash
// Find files by name
_fs_find /home myfile

// Search file contents
_fs_find /home password -c

// Exact filename match
_fs_find /var config.txt -e
```

### Real-World Example: Log File Analyzer

```bash
// Read and analyze a log file
_print === LOG ANALYZER ===

_setvar(logfile, get_string(Log file path:))

if file_exists(_getvar(logfile))
  _setvar(content, _fs_read(_getvar(logfile)))
  _setvar(size, len(_getvar(content)))
  
  _print File: _getvar(logfile)
  _print Size: _getvar(size) characters
  _print
  _print Contents:
  _fs_view _getvar(logfile)
else
  _print red(Error:) File not found!
endif
```

### Real-World Example: Backup Script

```bash
// Simple backup script
_print === BACKUP TOOL ===

_setvar(filename, get_string(File to backup:))

if file_exists(_getvar(filename))
  // Read the file
  _setvar(content, _fs_read(_getvar(filename)))
  
  // Create backup with timestamp
  _setvar(backup_name, concat(_getvar(filename), .backup))
  _fs_write _getvar(backup_name) _getvar(content)
  
  _print green(Success!) Backed up to _getvar(backup_name)
else
  _print red(Error:) File not found!
endif
```

---

## Network Operations

Scan and interact with networks (Grey Hack specific).

### Scan for Open Ports

```bash
// Scan an IP address
_net_ports 192.168.1.1
```

### List LAN Devices

```bash
// Show all devices on local network
_net_devices 192.168.1.1
```

### Show Router Information

```bash
// Display router details
_net_router 192.168.1.1
```

### Show Device Ports

```bash
// Show ports for a specific device
_net_devports 192.168.1.1 192.168.1.10
```

### Show Firewall Rules

```bash
// Display firewall configuration
_net_fwrules 192.168.1.1
```

### Check if Host is Reachable

```bash
// Ping a host
_net_ping 192.168.1.1
```

### Check if Port is Open

```bash
// Test specific port
_net_port 192.168.1.1 22
_net_port 192.168.1.1 80
```

### Validate IP Addresses

```bash
// Check if input is a valid IP
_setvar(ip, get_string(Enter IP:))

if _isValidIP(_getvar(ip)) == 0
  _print red(ERROR) Not a valid IP address
  _exit
end if

// Check if it's a LAN or public IP
if _isLanIP(_getvar(ip)) == 1
  _print yellow(NOTE) _getvar(ip) is a LAN IP
else
  _print green(OK) _getvar(ip) is a public IP
end if
```

### Real-World Example: Network Scanner

```bash
// Complete network scanner
_print === NETWORK SCANNER ===

_setvar(target, get_string(Target IP:))

// Validate the IP first
if _isValidIP(_getvar(target)) == 0
  _print red(ERROR) Invalid IP address
  _exit
end if

_print Scanning _getvar(target)...
_print

// Ping first
_print Checking if host is reachable...
_net_ping _getvar(target)

// Scan ports
_print
_print Scanning for open ports...
_net_ports _getvar(target)

// Show router info
_print
_print Router information:
_net_router _getvar(target)

// List LAN devices
_print
_print LAN devices:
_net_devices _getvar(target)

_print
_print Scan complete!
```

---

## Useful Built-in Functions

### String Functions

```bash
// Length of string
_setvar(text, Hello)
_print Length: len(_getvar(text))

// Uppercase
_print Uppercase: upper(_getvar(text))

// Lowercase
_print Lowercase: lower(_getvar(text))

// Substring
_setvar(sub, substr(_getvar(text), 0, 3))
_print Substring: _getvar(sub)

// Check if contains
if contains(_getvar(text), ell)
  _print Found it!
endif

// Join list into string
_setvar(words, [Hello, World])
_setvar(sentence, join(_getvar(words), " "))
_print _getvar(sentence)

// Split string into list
_setvar(sentence, Hello World)
_setvar(words, split_str(_getvar(sentence), " "))

// Concatenate strings
_setvar(full, concat(Hello, " ", World))
_print _getvar(full)

// Replace text
_setvar(fixed, replace(Hello World, World, Everyone))
_print _getvar(fixed)

// Trim whitespace
_setvar(clean, trim_str(  hello  ))
_print _getvar(clean)
```

### Type Checking

```bash
_setvar(name, Alice)
_setvar(age, 25)

_print Type of name: typeof(_getvar(name))
_print Type of age: typeof(_getvar(age))
```

### Type Conversion

```bash
// Convert to string
_setvar(num, 42)
_setvar(str, to_string(_getvar(num)))

// Convert to integer
_setvar(text, 123)
_setvar(number, to_int(_getvar(text)))

// Convert to float
_setvar(decimal, to_float(3.14))
```

### Boolean Conversion

```bash
_setvar(flag, 1)
_print Yes/No: to_yesno(_getvar(flag))
_print True/False: to_truefalse(_getvar(flag))

_setvar(flag, 0)
_print Yes/No: to_yesno(_getvar(flag))
_print True/False: to_truefalse(_getvar(flag))
```

### Date and Time

```bash
// Current timestamp (Unix epoch)
_print Timestamp: timestamp()

// Human-readable date/time
_print Date: date()
```

### Pausing Execution

You can pause a script and wait for the user to press Enter:

```bash
_print Here are the results above. Press Enter when ready...
pause
_print Continuing...
```

Useful for step-by-step scripts where the user needs time to read output before it continues.

### Finding Files with Glob Patterns

`_fs_glob` expands a pattern and returns a list of matching paths:

```bash
// Find all .src files
_setvar(files, _fs_glob(*.src))
for f in files
  _print Found: _getvar(f)
endfor

// Count files matching a pattern
_setvar(matches, _fs_glob(/home/user/backup_*))
_print Backups found: len(_getvar(matches))
```

The pattern can use `*` (any characters) and `?` (single character).

### Maps (Key-Value Storage)

```bash
// Create a map
_setvar(user, map(name, Alice, age, 25))

// Get a value
_print Name: map_get(_getvar(user), name)

// Set a value
map_set(_getvar(user), email, alice@example.com)

// Check if key exists
if map_has(_getvar(user), email)
  _print Has email!
endif

// Delete a key
map_del(_getvar(user), email)

// Get all keys and values
_setvar(keys, map_keys(_getvar(user)))
_setvar(vals, map_values(_getvar(user)))
_print Keys: _getvar(keys)
_print Values: _getvar(vals)

// Get number of entries
_print Size: map_len(_getvar(user))
```

### JSON

```bash
// Convert map to JSON string
_setvar(data, map(name, Alice, score, 100))
_setvar(jsonStr, json(_getvar(data)))
_print _getvar(jsonStr)

// Parse JSON string back to map
_setvar(parsed, json_parse(_getvar(jsonStr)))
_print Name: map_get(_getvar(parsed), name)
```

### Map File Persistence

```bash
// Save map to file
_setvar(config, map(host, 192.168.1.1, port, 22))
map_save(_getvar(config), /tmp/config.json)

// Load map from file
_setvar(loaded, map_load(/tmp/config.json))
_print Host: map_get(_getvar(loaded), host)
```

---

## Common Script Examples

### Example 1: User Registration

```bash
// User registration system
_print === USER REGISTRATION ===
_print

_setvar(username, get_string(Username:))
_setvar(email, get_string(Email:))
_setvar(age, get_integer(Age:))

// Validation
if len(_getvar(username)) < 3
  _print red(Error:) Username too short (min 3 characters)
  _exit 1
endif

if _getvar(age) < 13
  _print red(Error:) Must be 13 or older
  _exit 1
endif

// Success
_print
_print green(Registration successful!)
_print
_print Account Details:
_print Username: _getvar(username)
_print Email: _getvar(email)
_print Age: _getvar(age)
```

### Example 2: Password Generator

```bash
// Random password generator
_print === PASSWORD GENERATOR ===

_setvar(length, get_integer(Password length (8-20):))

if _getvar(length) < 8 or _getvar(length) > 20
  _print red(Error:) Length must be between 8 and 20
  _exit 1
endif

// Generate password parts
_setvar(part1, random(1000, 9999))
_setvar(part2, random(1000, 9999))
_setvar(part3, random(100, 999))

_setvar(password, concat(PASS, _getvar(part1), -, _getvar(part2), X, _getvar(part3)))

_print
_print green(Generated password:)
_print _getvar(password)
_print
_print Save this password securely!
```

### Example 3: To-Do List

```bash
// Simple to-do list
_setvar(todos, [])
_setvar(running, 1)

while _getvar(running) == 1
  _print
  _print === TO-DO LIST ===
  _print
  _print 1. Add task
  _print 2. Show tasks
  _print 3. Remove last task
  _print 4. Exit
  
  _setvar(choice, get_integer(Choose:))
  
  if _getvar(choice) == 1
    _setvar(task, get_string(Task name:))
    _push todos _getvar(task)
    _print green(Task added!)
    
  elif _getvar(choice) == 2
    _print
    _print Your tasks:
    _setvar(count, 0)
    for task in todos
      _setvar(count, _getvar(count) + 1)
      _print _getvar(count). _getvar(task)
    endfor
    
  elif _getvar(choice) == 3
    _pop todos
    _print yellow(Removed last task)
    
  elif _getvar(choice) == 4
    _print Goodbye!
    _setvar(running, 0)
    
  else
    _print red(Invalid choice)
  endif
endwhile
```

### Example 4: Number Guessing Game

```bash
// Number guessing game
_print === GUESS THE NUMBER ===
_print I'm thinking of a number between 1 and 100
_print

_setvar(secret, random(1, 100))
_setvar(tries, 0)
_setvar(max_tries, 10)

while _getvar(tries) < _getvar(max_tries)
  _setvar(tries, _getvar(tries) + 1)
  _setvar(remaining, _getvar(max_tries) - _getvar(tries) + 1)
  
  _print
  _print Try _getvar(tries) of _getvar(max_tries)
  _setvar(guess, get_integer(Your guess:))
  
  if _getvar(guess) == _getvar(secret)
    _print
    _print green(CORRECT!) You found it in _getvar(tries) tries!
    _exit 0
  elif _getvar(guess) < _getvar(secret)
    _print blue(Too low!) Try a higher number
  else
    _print yellow(Too high!) Try a lower number
  endif
  
  _print Tries remaining: _getvar(remaining)
endwhile

_print
_print red(Game Over!) The number was _getvar(secret)
```

### Example 5: System Monitor

```bash
// Simple system monitor
_print === SYSTEM MONITOR ===
_print

_print Current Directory:
_fs_pwd

_print
_print Current User:
_print _sys_whoami

_print
_print System Context:
_print _sys_whatami

_print
_print Running Processes:
_sys_procs

_print
_print Press Enter to exit
get_string()
```

---

## Advanced: Held Objects and Object Dispatch

Some commands (like scanner operations) leave a "held object" as their result. You can store and reuse these with `_hold`, `_setvar`, and `OBJ()`.

### Storing a Held Object

```bash
// After running a command that creates a held object:
_setvar(my_shell, _hold)   // Capture the held object into a variable
```

### Dispatching Commands to a Stored Object

Use `OBJ(name)` to send commands to a stored object:

```bash
OBJ(my_shell) ls /home     // Run 'ls /home' on the stored shell
OBJ(my_shell) cat /etc/passwd
```

### Closing a Stored Object

```bash
OBJ(my_shell) home         // Send home command (close)
OBJ(my_shell) exit         // Alternative: send exit
```

> **Note**: This is an advanced feature. You'll mainly need it when working with scanner tools or remote shell sessions.

---

## Tips & Tricks

### 💡 Tip 1: Use Comments Liberally

```bash
// This is a comment explaining what the script does
// Comments help you remember what each part does later

// Calculate total price
_setvar(price, 19.99)
_setvar(quantity, 3)
_setvar(total, _getvar(price) * _getvar(quantity))  // Price times quantity
```

### 💡 Tip 2: Break Complex Scripts into Functions

Instead of one long script:
```bash
func validate_input(value)
  // Validation logic here
  _return 1
endfunc

func process_data(data)
  // Processing logic here
  _return result
endfunc

func display_results(results)
  // Display logic here
endfunc

// Main script
validate_input(mydata)
process_data(mydata)
display_results(results)
```

### 💡 Tip 3: Use Descriptive Variable Names

```bash
// Good names (clear and descriptive)
_setvar(user_age, 25)
_setvar(total_price, 99.99)
_setvar(is_valid, 1)

// Bad names (unclear)
_setvar(x, 25)
_setvar(temp, 99.99)
_setvar(flag, 1)
```

### 💡 Tip 4: Validate User Input

```bash
_setvar(age, get_integer(Enter your age:))

if _getvar(age) < 0 or _getvar(age) > 150
  _print red(Error:) Invalid age!
  _exit 1
endif

// Continue with valid age
_print Your age is _getvar(age)
```

### 💡 Tip 5: Use Colors for Better Output

```bash
_print green(Success!) Operation completed
_print red(Error!) Something went wrong
_print yellow(Warning:) Please check this
_print blue(Info:) Just so you know
_print bold(Important!) Read this carefully
```

Full color palette: `red`, `green`, `blue`, `cyan`, `yellow`, `orange`, `magenta`, `lime`, `white`, `grey`, `black`, `purple`, `liteblue`, `liteGrey`, `iyellow`, `bred`, `error`, `password`, `bold`

Hex colors also work in `menu()`: `#00bfff`, `#ff6600`, etc.

### 💡 Tip 6: Test Small Pieces First

Don't write a huge script all at once! Test small pieces:

```bash
// Test 1: Just the input
_setvar(name, get_string(Name:))
_print You entered: _getvar(name)

// When that works, add more...
```

### 💡 Tip 7: Use Sleep for Dramatic Effect

```bash
_print Preparing to launch...
_sleep 1
_print 3...
_sleep 1
_print 2...
_sleep 1
_print 1...
_sleep 1
_print green(LAUNCH!)
```

---

## Troubleshooting

### Problem: Script doesn't run

**Symptoms:** Nothing happens when you type `run scriptname`

**Solutions:**
1. Make sure the script is in your bash directory
2. Check that you're using the correct filename
3. Run without any file extension: `run scriptname` not `run scriptname.txt`

### Problem: Variable not found

**Symptoms:** Error like "variable undefined"

**Solutions:**
1. Make sure you created the variable with `_setvar`
2. Check spelling - variables are case-sensitive
3. Use `_getvar(name)` to retrieve values

```bash
// Wrong
_setvar(username, Alice)
_print username  // This prints the word "username"

// Right
_setvar(username, Alice)
_print _getvar(username)  // This prints "Alice"
```

### Problem: If statement doesn't work

**Symptoms:** Wrong branch executes or nothing executes

**Solutions:**
1. Don't forget `endif` at the end
2. Use `_getvar()` to access variables in conditions
3. Make sure you're using the right comparison operator

```bash
// Wrong
if _getvar(age) = 18  // Single = is wrong
  _print Adult
endif

// Right
if _getvar(age) == 18  // Use == for comparison
  _print Adult
endif
```

### Problem: Loop never stops

**Symptoms:** Script runs forever

**Solutions:**
1. Make sure your condition eventually becomes false
2. Check that you're updating the counter variable
3. Use `break` if you need to exit early

```bash
// Wrong - infinite loop
_setvar(count, 0)
while _getvar(count) < 5
  _print Count: _getvar(count)
  // Forgot to increment count!
endwhile

// Right
_setvar(count, 0)
while _getvar(count) < 5
  _print Count: _getvar(count)
  _setvar(count, _getvar(count) + 1)  // Increment!
endwhile
```

### Problem: Math doesn't work

**Symptoms:** Numbers add as text instead of adding mathematically

**Solutions:**
1. Make sure you're using `_getvar()` for variables
2. Convert strings to numbers with `to_int()` or `to_float()`

```bash
// Wrong
_setvar(a, "10")
_setvar(b, "20")
_setvar(sum, _getvar(a) + _getvar(b))  // Might concatenate as "1020"

// Right
_setvar(a, 10)  // Store as number, not string
_setvar(b, 20)
_setvar(sum, _getvar(a) + _getvar(b))  // Now adds to 30
```

### Problem: File not found

**Symptoms:** Error when trying to read/write files

**Solutions:**
1. Check the file path is correct
2. Use `file_exists()` to verify before reading
3. Use absolute paths (`/home/user/file.txt`) if unsure

```bash
// Better approach
_setvar(filename, /etc/passwd)

if file_exists(_getvar(filename))
  _setvar(content, _fs_read(_getvar(filename)))
  _print _getvar(content)
else
  _print red(Error:) File not found!
endif
```

---

## Quick Reference

### Essential Commands

```bash
// Variables
_setvar(name, value)           // Create/update variable
_getvar(name)                  // Get variable value

// Input
get_string(prompt)             // Get text input
get_integer(prompt)            // Get number input
get_decimal(prompt)            // Get decimal input
get_yesno(prompt)              // Get yes/no input (returns 1 or 0, empty defaults to no)

// Output
_print message             // Print to screen (buffered)
_printnow message         // Print immediately (use when order matters near prompts)

// Conditionals
if condition                   // Start if block
elif condition                 // Else if
else                          // Else block
endif                         // End if block

// Loops
for var in list               // Loop through list
for var in range(start, end)  // Loop through range
while condition               // Loop while true
endfor                        // End for loop
endwhile                      // End while loop

// Functions
func name(params)             // Define function
_return value                 // Return from function
endfunc                       // End function

// Lists
_push list value           // Add to end
_pop list                  // Remove from end
_pull list                 // Remove from start
_len list                  // Get list size

// Files
_fs_read(path)               // Read file
_fs_write path content       // Write file
_fs_view path                // Display file
file_exists(path)             // Check if exists
is_folder(path)              // Check if directory
is_binary(path)              // Check if binary file
_fs_mkdir path               // Create directory
_fs_cd path                  // Change directory
_fs_pwd                      // Print working directory
_fs_find path pattern        // Find files
_fs_glob pattern             // Expand glob pattern (returns list)

// String Functions
len(val)                     // String/list length
upper(val)                   // Uppercase
lower(val)                   // Lowercase
substr(str,start[,end])      // Substring
concat(...)                  // Concatenate strings
contains(str,search)         // Check if contains
replace(str,search,repl)     // Replace text
split_str(string,delim)      // Split to list
join(list,delim)             // Join list to string
trim_str(string)             // Trim whitespace

// Math Functions
floor(val)                   // Round down
ceil(val)                    // Round up
abs(val)                     // Absolute value
round(val)                   // Round nearest
min(a,b)                     // Minimum
max(a,b)                     // Maximum
random(min,max)              // Random number

// Type & Boolean
to_string(val)               // Convert to string
to_int(val)                  // Convert to integer
to_float(val)                // Convert to float
typeof(val)                  // Get type name
to_yesno(val)                // 1→yes, 0→no
to_truefalse(val)            // 1→true, 0→false

// Context
get_user()                   // Current username
get_home()                   // Home directory
get_root()                   // Root path
timestamp()                  // Unix timestamp
date()                       // Formatted date
pause                        // Wait for Enter key

// Advanced: Held Objects (scanner/remote shells)
_hold                        // Capture held object
_setvar(name, _hold)         // Store held object to variable
OBJ(name) cmd [args]         // Run command on stored object
OBJ(name) home               // Close stored object

// Maps
map([key,val,...])            // Create map
map_set(map,key,val)         // Set key
map_get(map,key)             // Get value
map_del(map,key)             // Delete key
map_has(map,key)             // Check key exists
map_keys(map)                // Get all keys
map_values(map)              // Get all values
map_len(map)                 // Number of entries

// JSON & Persistence
json(value)                  // Map to JSON string
json_parse(string)           // JSON string to map
map_save(map,path)           // Save map to file
map_load(path)               // Load map from file

// Network
_net_ports ip                // Scan open ports
_net_devices ip              // List LAN devices
_net_router ip               // Router info
_net_devports ip device      // Device ports
_net_fwrules ip              // Firewall rules
_net_ping ip                 // Check reachable
_net_port ip port            // Check single port
```

---

## What's Next?

🎓 **You're ready to write scripts!**

Start with simple scripts and gradually add more features:

1. **Start Simple**: Begin with input/output scripts
2. **Add Logic**: Learn if/else and loops
3. **Create Functions**: Organize reusable code
4. **Build Tools**: Make useful automation scripts
5. **Share & Learn**: Show your scripts to others!

### Need Help?

- Look at the examples in this guide
- Start simple and build up gradually
- Don't be afraid to experiment!

---

**Happy Scripting! 🚀**

Remember: Every expert was once a beginner. Start simple, practice often, and you'll be writing amazing scripts in no time!

---

## Appendix: Complete Tutorial Script

This is the full source of `learn_bash.src` — a comprehensive, runnable tutorial that exercises every major feature of x bash. Run it with `@test` (or rename it and use `run learn_bash`) to verify your bash engine works correctly. Every example defines a function, calls it, and prints results so you can see exactly what happens.

Read through the source code to learn how each feature works. Modify it, break it, fix it — that's how you learn.

### How to Use

1. Copy (or symlink) this file into your bash scripts directory
2. Run it: `@test` or `run learn_bash`
3. Read the output alongside the source code
4. All `[PASS]` lines are self-checking assertions — if you see `[FAIL]`, something is broken

### What It Covers

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
| 13. Processes | Listing processes, _sleep and timing |
| 14. Capstone | Network inventory builder, mega chain, final verification |

### Full Source

```bash
// ================================================================
// x Bash Learning Guide & Tutorial Test Script
// ================================================================
// This script teaches new players how to use x's bash scripting
// language through working examples. Every section defines
// real functions, calls them, and prints results so you can
// see exactly what happens.
//
// Run this script with:   @test
//
// Each section builds on the previous ones. Read the comments
// to understand what each line does, then check the output.
// ================================================================

// ---------------------------------------------------------------
// HELPER: assert function used throughout for self-checking
// ---------------------------------------------------------------
func assert(label, actual, expected)
  if _getvar(actual) == _getvar(expected)
    _print   [PASS] _getvar(label)
  else
    _print   [FAIL] _getvar(label)  expected: _getvar(expected)  got: _getvar(actual)
  endif
endfunc

// ---------------------------------------------------------------
// HELPER: section header printer
// ---------------------------------------------------------------
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

func printTip(msg)
  _print   TIP: _getvar(msg)
endfunc

func printNote(msg)
  _print   NOTE: _getvar(msg)
endfunc
```

The script then proceeds through 14 chapters of increasingly complex examples. Each lesson:

1. **Defines functions** that demonstrate the concept
2. **Calls them** with specific inputs
3. **Prints results** so you can see what happened
4. **Asserts correctness** with `assert()` calls that verify expected output

#### Key Patterns Used Throughout

```bash
// Store a value
_setvar(name, value)

// Read a value
_getvar(name)

// Call a function and capture its return
_setvar(result, myFunction(arg1, arg2))

// Assert the result is correct
assert(description, _getvar(result), expectedValue)

// Print output
_print   Some text: _getvar(variable)
```

#### Example: Prime Number Checker (from Chapter 8)

```bash
func isPrime(n)
  if _getvar(n) < 2
    _return 0
  endif
  _setvar(i, 2)
  while _getvar(i) * _getvar(i) <= _getvar(n)
    if _getvar(n) % _getvar(i) == 0
      _return 0
    endif
    _setvar(i, _getvar(i) + 1)
  endwhile
  _return 1
endfunc

_setvar(r, isPrime(7))
assert(7 is prime, _getvar(r), 1)
_setvar(r, isPrime(9))
assert(9 is not prime, _getvar(r), 0)
```

#### Example: Recursive Factorial (from Chapter 2)

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

#### Example: State Machine Login (from Chapter 10)

```bash
func checkPassword(input, correct)
  if _getvar(input) == _getvar(correct)
    _return granted
  else
    _return denied
  endif
endfunc

func loginSystem(attempts, password)
  _setvar(maxAttempts, _getvar(attempts))
  _setvar(attempt, 0)
  _setvar(status, locked)

  while _getvar(attempt) < _getvar(maxAttempts)
    _setvar(attempt, _getvar(attempt) + 1)
    if _getvar(attempt) == _getvar(maxAttempts)
      _setvar(result, checkPassword(_getvar(password), _getvar(password)))
    else
      _setvar(result, checkPassword(wrong, _getvar(password)))
    endif

    if _getvar(result) == granted
      _setvar(status, granted)
      _setvar(attempt, _getvar(maxAttempts))
    else
      _print   Attempt _getvar(attempt): Access denied
    endif
  endwhile

  _return _getvar(status)
endfunc

_setvar(r, loginSystem(3, secret123))
assert(login succeeds on last attempt, _getvar(r), granted)
```

#### Expected Output (abbreviated)

```
============================================================
    x BASH LEARNING GUIDE & TUTORIAL
============================================================

============================================
  CHAPTER 1: FUNDAMENTALS
============================================

--- Lesson 1.1: Hello World & Printing ---
  Hello World! Welcome to x bash.
  ...
  [PASS] 7+3 equals 10
  [PASS] 6x7 equals 42
  ...

============================================
  CHAPTER 14: PUTTING IT ALL TOGETHER
============================================
  ...
  [PASS] factorial(6) is 720
  [PASS] fibonacci(15) is 610
  ...

============================================================
    TUTORIAL COMPLETE!
============================================================
```

If all lines show `[PASS]`, your bash engine is working correctly.
