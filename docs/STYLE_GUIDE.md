# X Shell - Code Style Guide

This document defines the coding conventions and style guidelines for the X Shell project.

## ArgumentParser Usage

### Standard Pattern
```greyscript
_p=ArgumentParser.init
_p.addArgument("flag",false,"flag")
_p.addArgument("u",false,"store")
argv=_p.parseArgs("commandName",argv)
if argv isa Error then return
```

### Argument Types

#### Boolean Flag (no value)
```greyscript
_p.addArgument("verbose",true,"flag")   // Long form: --verbose
_p.addArgument("v",false,"flag")        // Short form: -v
// Access: argv.verbose or argv.v
// Returns: true if present, null if absent
```

#### String Value
```greyscript
_p.addArgument("output",true,"store")   // Long form: --output value
_p.addArgument("o",false,"store")       // Short form: -o value
// Access: argv.output or argv.o
// Returns: string value or null
```

#### Numeric Value
```greyscript
_p.addArgument("port",true,"storeNumber")   // Long form: --port 8080
_p.addArgument("p",false,"storeNumber")     // Short form: -p 8080
// Access: argv.port or argv.p
// Returns: number or null
```

### Positional Arguments
Arguments not captured by flags go into `argv.rest` array:
```greyscript
argv=_p.parseArgs("cmd",argv)
// Command: cmd -u root shell bounce 192.168.1.1
// Result: argv.u="root", argv.rest=["shell","bounce","192.168.1.1"]
```

### Parameter Format Rules
- **First parameter**: Flag name (string)
- **Second parameter**: Long form flag (boolean)
  - `true` = `--flagname` (double dash)
  - `false` = `-f` (single dash)
- **Third parameter**: Type (string)
  - `"flag"` = boolean presence flag
  - `"store"` = string value
  - `"storeNumber"` = numeric value

### Common Patterns
```greyscript
// Optional user filter with default
_p.addArgument("u",false,"store")
argv=_p.parseArgs("cmd",argv)
if not argv.u then argv.u="root"

// Numeric with validation
_p.addArgument("p",false,"storeNumber")
argv=_p.parseArgs("cmd",argv)
if argv.p and (argv.p<1 or argv.p>65535) then
  return Error.set("Invalid port: "+argv.p)
end if

// Multiple aliases for same function
_p.addArgument("all",true,"flag")
_p.addArgument("a",false,"flag")
argv=_p.parseArgs("cmd",argv)
if argv.a then argv.all=true  // Normalize to long form
```

## Character Encoding

### ASCII Only
- **Never use Unicode characters** (✓, ✗, ™, ©, →, etc.) in GreyScript code
- GreyScript does not support Unicode properly
- Use ASCII alternatives:
  - Instead of ✓ use `[+]` or `[OK]`
  - Instead of ✗ use `[X]` or `[FAIL]`
  - Instead of → use `->` or `==>`

## Naming Conventions

### Variables and Functions
- **Style**: camelCase
- **Examples**: 
  - `myVariable`, `userData`, `currentSession`
  - `getUserData()`, `executeCommand()`, `parseInput()`
- **Private/Internal**: Prefix with underscore: `_internalHelper()`, `_getCommandHelp()`

### Objects/Namespaces
- **Style**: PascalCase
- **Examples**: `Agent`, `Attack`, `Exploit`, `Man`

### Object Properties
- **Style**: camelCase
- **Examples**: 
  - `Agent.config.maxRetries`
  - `Agent.config.dryRun`
  - `Agent.config.promptOnCritical`

### Constants
- **Style**: camelCase or UPPER_CASE
- **Examples**: `maxRetries`, `MAX_CONNECTIONS`

## File Conventions

### File Extensions
- **Source files**: `.src`
- **Documentation**: `.md`

### File Organization
- Library files in: `src/libs/`
- Command implementations in: `src/command/`
- Utilities in: `utilities/`
- Testing in: `testing/`

### Build Process
- **Source files** are in `src/` directory
- **Build files** are in `build/` directory
- **IMPORTANT**: The game executes code from `build/` folder
- **NEVER edit files in `build/` folder** - they are auto-generated and will be overwritten
- **All edits MUST be made in source files** (`src/` directory)
- **To find error line numbers**: Check the `build/` file to locate the error, then fix it in the corresponding `src/` file
- After editing source files, rebuild to update the `build/` folder

## Code Structure

### Global Namespace Pattern
- **Use global objects** as namespaces (e.g., `Agent`, `Attack`, `Man`)
- **Methods belong to globals**: `Agent.methodName=function`
- **Use `self`** inside methods to reference the parent object
- **Check globals exist**: `if typeof(GlobalName)!="map" then return null`
- Avoid local standalone functions; attach to appropriate global namespace

### Spacing Rules
- **No spaces around `=`**: `var=value` not `var = value`
- **No spaces in parameter lists**: `function(param1,param2,param3)`
- **No spaces after commas**: Use `push(list,item)` not `push(list, item)`
- **No spaces in function calls**: `myFunction(arg1,arg2)`
- **No blank lines**: Avoid blank lines between code statements and function definitions
- **No inline map literals with commas in function arguments**: GreyScript parses commas as argument separators, not map element separators

```greyscript
// Correct ✓
functionName=function(paramOne,paramTwo)
  result=doSomething(paramOne,paramTwo)
  return result
end function
myVar=calculateValue(10,20,30)
config={"key":value,"another":test}
// Correct ✓ - Create map separately before passing
context={}
context.target=targetValue
context.goal=goalValue
result=myFunction(param,context)
// Incorrect ✗
functionName = function(paramOne, paramTwo)
result = doSomething(paramOne, paramTwo)
myVar = calculateValue(10, 20, 30)
// Incorrect ✗ - Inline map with commas causes "Too Many Arguments" error
result=myFunction(param,{"target":value,"goal":other})
```

### Indentation
- Use **2 spaces** per indentation level
- No tabs

### Line Length
- Prefer lines under 100 characters when practical
- Break long lines at logical points

### Conditionals
- **Use multi-line format for multiple statements**: Each statement on its own line within if/then/end if blocks
- **Use single-line format only for single statements**: `if condition then action` or `if condition then action else altAction`
- **Never chain multiple statements with semicolons** in conditional blocks
- **Avoid long if-else chains**: Limit to 10 or fewer `else if` statements - use dispatch patterns instead

```greyscript
// Correct ✓ - Single statement can be single-line
if test then doSomething else doOther

if value==null then return false

if hasIndex(map,"key") then result=map["key"] else result=default

// Correct ✓ - Multiple statements use multi-line format
if not targetIp or targetIp=="" then
  result.error="Empty target IP"
  result.critical=true
  return result
end if

if needsRoot and shellResult.user.raw!="root" then
  shellResult=ShellObject.headlessSu(shellResult)
  if shellResult isa Error then return null
end if

// Incorrect ✗ - Do not chain multiple statements with semicolons
if condition then firstAction;secondAction;thirdAction else altAction

if not targetIp or targetIp=="" then result.error="Empty target IP";result.critical=true;return result

// Incorrect ✗ - Long if-else chains are hard to maintain
if action=="scan" then
  // handle scan
else if action=="crack" then
  // handle crack
else if action=="exploit" then
  // handle exploit
// ... 40+ more else if statements ...
else if action=="lastOption" then
  // handle lastOption
end if

// Correct ✓ - Use dispatch pattern for many cases
// Initialize registry/map of handlers
handlers={}
handlers.scan=@handleScan
handlers.crack=@handleCrack
handlers.exploit=@handleExploit
// ... register all handlers ...

// Dispatch to handler
if hasIndex(handlers,action) then
  handler=handlers[action]
  result=handler(params)
else
  result=handleDefault(params)
end if
```

### Operators
- **Use compound assignment operators**: `+=`, `-=`, `*=`, `/=`

```greyscript
// Correct ✓
counter+=1
value-=10
total+=amount
score*=2
average/=count

// Incorrect ✗
counter=counter+1
value=value-10
total=total+amount
```

### Map Property Access and Function Calls

**CRITICAL**: GreyScript does NOT support chaining map property access with function calls in a single expression.

```greyscript
// INCORRECT ✗ - This will cause compiler error "got LParen where EOL is required"
output=obj.commands["list"](["-sB"])
result=wrappedObj.commands[cmdName](cmdArgs)

// CORRECT ✓ - Get function reference first, then call it
listCmd=obj.commands["list"]
output=listCmd(["-sB"])

cmdFunc=wrappedObj.commands[cmdName]
result=cmdFunc(cmdArgs)
```

**Why this matters**: GreyScript's parser requires End-Of-Line after map/property access expressions. Attempting to immediately invoke with `(args)` violates this syntax rule.

**Pattern to follow**:
1. Get the function reference from the map: `funcRef=map["key"]`
2. Call the function on the next line: `result=funcRef(args)`

### Comments
- Header blocks for files with ASCII art separators
- Function purposes described in comments above definitions
- Inline comments for complex logic

### Function Definitions
```greyscript
// Functions are methods on global objects
// No spaces around = or after commas
GlobalObject.methodName=function(paramOne,paramTwo)
  // Use 'self' to reference the parent object
  value=self.config.someProperty
  result=self._internalHelper(value)
  return result
end function

// Private/internal methods prefixed with underscore
GlobalObject._internalHelper=function(data)
  // Internal implementation
  // Can also use 'self' here
  return self._processData(data)
end function
```

### Function References (@function)
**IMPORTANT**: When a function is stored as a reference using `@function` syntax, it **cannot use `self`**. You must call the class by name instead.

```greyscript
// Correct ✓ - Function reference stored in registry
GlobalObject._helperFunction=function(param)
  // Cannot use 'self' here - must use class name
  result=GlobalObject.otherMethod(param)
  value=GlobalObject.config.setting
  return result
end function

// Store as reference
registry={}
registry.helper=@GlobalObject._helperFunction

// Incorrect ✗ - Using self in a function that will be referenced
GlobalObject._helperFunction=function(param)
  // This will fail when called via @function reference
  result=self.otherMethod(param)  // ERROR
  return result
end function
```

**Rule**: If your function will be stored in a map/registry using `@functionName`, use the explicit class name instead of `self`.

### Nested Functions and Self
**Depth 1 functions** (direct methods on objects) can use `self` normally.
**Depth 2 functions** (inner functions inside other functions) **cannot use `self`** unless you capture it first.

```greyscript
// Correct ✓ - Depth 1 function using self
GlobalObject.method=function(param)
  value=self.config.setting  // Works fine
  return value
end function

// Correct ✓ - Depth 2 with captured self
GlobalObject.method=function(param)
  outerSelf=self  // Capture self for inner function
  helper=function(innerParam)
    // Use captured reference instead of self
    return outerSelf.config.setting+innerParam
  end function
  return helper(param)
end function

// Incorrect ✗ - Depth 2 trying to use self directly
GlobalObject.method=function(param)
  helper=function(innerParam)
    return self.config.setting+innerParam  // ERROR - self not available
  end function
  return helper(param)
end function
```

### Function Calls and Parentheses
- **Parentheses are only required when passing parameters**
- **No-parameter functions must NOT have parentheses**

```greyscript
// Correct ✓
result=myFunction(param1,param2)  // With parameters
value=calculateSomething           // No parameters, no parentheses
data=fetchData                     // No parameters, no parentheses

// Incorrect ✗
result=myFunction param1,param2    // Missing parentheses with parameters
value=calculateSomething()         // Unnecessary parentheses
data=fetchData()                   // Unnecessary parentheses
```

### Object/Module Pattern
```greyscript
// PascalCase for object/namespace
ModuleName={}

// camelCase for methods
ModuleName.methodName=function
  // Implementation
end function

// camelCase for config/data properties
ModuleName.config={
  "propertyOne": value,
  "propertyTwo": value
}
```

## Language-Specific Notes

### GreyScript/X Shell
- File extension: `.src`
- Function assignment syntax: `name=function ... end function`
- Object creation: `Object={}`
- Method definition: `Object.method=function ... end function`

## Built-in Function Calls

### GreyScript uses global function syntax, not method calls:

**Correct ✓**
```greyscript
push(myList,item)
indexOf(text,"search")
hasIndex(myMap,"key")
indexes(myMap)              // Get all keys from map
join(lines,char(10))
split(text,",")
len(myList)
lower(text)
upper(text)
trim(text)
```

**Incorrect ✗**
```greyscript
myList.push(item)          // Wrong
text.indexOf("search")     // Wrong
myMap.indexes              // Wrong - use indexes(myMap)
myMap.hasIndex("key")      // Wrong
lines.join(char(10))       // Wrong
text.split(",")            // Wrong
myList.len()               // Wrong
text.lower()               // Wrong
```

### Exception: String.replace() Method

**String replacement MUST use method syntax:**

```greyscript
// Correct ✓
cleanText=myString.replace("old","new")
cleanText=myString.replace("pattern","replacement","i")  // With regex options

// Incorrect ✗
cleanText=replace(myString,"old","new")  // Wrong for strings
```

**Maps and Lists use global function syntax:**

```greyscript
// Correct ✓
newMap=replace(myMap,oldKey,newKey)
newList=replace(myList,oldValue,newValue)

// Incorrect ✗
newMap=myMap.replace(oldKey,newKey)      // Wrong
newList=myList.replace(oldValue,newValue)  // Wrong
```

**Summary:**
- `string.replace(pattern,newValue,regexOptions)` - Method call on strings
- `replace(map,...)` - Global function for maps
- `replace(list,...)` - Global function for lists

## Best Practices

1. **Always use camelCase** for variables and functions
2. **Use descriptive names** that convey purpose
3. **Prefix internal/private functions** with underscore
4. **Use global function syntax** for built-ins (push, indexOf, hasIndex, etc.)
5. **No spaces around `=` or after commas** in any context
6. **Keep functions focused** on single responsibilities
7. **Add comments** for complex logic and file headers
8. **Consistent formatting** throughout the codebase

## Examples

### Good ✓
```greyscript
// Define global namespace object
Agent={}
Agent.config={"max_retries":3}

// Methods use self to access parent object
// No spaces around = or after commas
Agent.executeCommand=function(targetIp,options)
  retryCount=0
  while retryCount<self.config.max_retries
    result=self._attemptConnection(targetIp)
    if result then return result
    retryCount+=1
  end while
  return null
end function

Agent._attemptConnection=function(ipAddress)
  // Check if other globals exist and use single-line conditionals
  if typeof(Attack)!="map" then return null
  if not ipAddress then return null
  // Call methods on other globals
  return Attack.connect(ipAddress)
end function
```

### Avoid ✗
```greyscript
// Don't use snake_case for functions/variables
execute_command=function(target_ip,options)
  retry_count=0
  // ...
end function

// Don't create standalone local functions
myLocalFunction=function(data)
  // Should be attached to a global namespace instead
end function

// Don't use 'this' - use 'self'
Agent.method=function
  value=this.config  // ✗ Wrong
  value=self.config  // ✓ Correct
end function

// Don't use spaces
function_name = function(param1, param2)  // ✗ Wrong
functionName=function(param1,param2)      // ✓ Correct
```

## AI Assistant Instructions

When writing code for this project:
- **Always use camelCase** for variables and function names
- Use PascalCase for object/namespace names
- Use snake_case only for object properties and config keys
- Follow the file extension `.src` for source files
- Match the existing code structure and patterns
- Refer to existing files like `agent.src` for style examples
