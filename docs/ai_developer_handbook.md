# AI Developer Handbook
## Technical Guide to the X AI Agent System

**Version:** 0.9.7.3  
**Last Updated:** March 2026  
**Author:** Brian Windorski

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Module Structure](#module-structure)
3. [AgentCore - Configuration & Knowledge System](#agentcore)
4. [AgentParser - Natural Language Processing](#agentparser)
5. [AgentPlanning - Plan Creation & Strategy](#agentplanning)
6. [AgentExecution - Plan Execution Engine](#agentexecution)
7. [AgentHandlers - Step Execution](#agenthandlers)
8. [AgentLearning - Pattern Reinforcement](#agentlearning)
9. [AgentRegistry - Command Metadata](#agentregistry)
10. [Recent Improvements (v0.9.7.3)](#recent-improvements)
11. [Testing with `ai test`](#testing)
12. [Adding New Commands](#adding-new-commands)
13. [Pitfalls & Common Issues](#pitfalls-and-common-issues)
14. [Pros & Cons](#pros-and-cons)
15. [Improvement Suggestions](#improvement-suggestions)
16. [Code Examples](#code-examples)

---

## Architecture Overview

The X AI Agent System is a **zero-hardcoded-registry natural language command interface** that translates human language into executable terminal commands. It learns command syntax dynamically from man pages and uses a sophisticated pattern matching system to understand user intent.

### Core Design Principles

1. **Dynamic Learning**: No hardcoded command lists. The system reads man pages on-the-fly to learn command capabilities.
2. **Phrase-Based Detection**: Uses scored phrase patterns (20-35 points) to identify commands from natural language.
3. **Modular Architecture**: Separated into 14 source files for maintainability.
4. **Context Preservation**: Tracks session state, command history, and user preferences.
5. **Multi-Step Planning**: Breaks complex goals into executable steps with fallback strategies.
6. **Persistent Learning**: Saves pattern scores, preferences, and templates to disk as JSON.
7. **Context-Weighted Synonyms**: Disambiguates words like "break" using surrounding context.
8. **Compound Commands**: Supports multi-command input ("scan X and then exploit Y").

### Data Flow

```
User Input (Natural Language)
    ↓
AgentParser: _parseConfig, _parseCommand
    ↓ (parsed fields: command, target, flags, user, group, permValue, etc.)
AgentPlanning: _createPlan, _buildXXXPlan
    ↓ (plan with steps array)
AgentExecution: _executePlan, _executeStep
    ↓ (step handlers)
AgentHandlers: _handleXXX functions
    ↓ (command execution)
Terminal Output
```

### Key Components

- **Phrase Detection**: Score-based system where patterns compete for highest match score
- **Field Extraction**: Extracts parameters like filenames, IP addresses, permissions, users
- **Plan Builders**: Convert parsed commands into multi-step execution plans
- **Step Handlers**: Execute individual steps with error handling and fallbacks
- **Knowledge Cache**: Stores parsed man pages to avoid repeated disk reads

---

## Module Structure

The AI system is split across modular source files (parser is further split for the 160k Grey Hack limit):

| Module | Purpose |
|--------|---------|
| `agent_core.src` | Configuration, initialization, config save/load |
| `agent_parser.src` | NL parse orchestration (phases 1–4) |
| `agent_parser_flow.src` | Early returns, autonomous / conditional flow |
| `agent_parser_action.src` | Phrase scoring, man-page / synonym action match |
| `agent_parser_fields.src` | Per-command field extraction |
| `agent_planning.src` | Plan creation, strategy, template recall, risk assessment |
| `agent_execute.src` | High-level execution dispatcher, compound command handler |
| `agent_execution.src` | Plan execution, step sequencing, error handling |
| `agent_handlers.src` | Step execution handlers (non-attack) |
| `agent_handlers_attack.src` | Scan / exploit handlers and autonomous exploit scoring |
| `agent_handlers_access.src` | getObject, escalate, crack, fetch shell, recon, backdoor, analyze |
| `agent_learning.src` | Pattern reinforcement, user preferences, learning persistence |
| `agent_knowledge.src` | Command knowledge cache, man-page learn, save/load |
| `agent_command_registry.src` | Command lookup, `learnFlagsFromManPage`, semantic flags |
| `agent_nlp.src` | NLP utilities, disambiguation |
| `agent_util.src` | Shared utility functions |
| `knowledge.src` | Persistent knowledge store (pipe-delimited) |
| `agent_test.src` | `ai test` harness |

### Why Modular?

Originally the AI was a single 8000+ line file. Splitting improves:
- **Maintainability**: Easier to find and fix bugs
- **Collaboration**: Multiple developers can work on different modules
- **Load Times**: Only load modules when needed
- **Debugging**: Isolated logging per module

---

## AgentCore

**File:** `agent_core.src`  
**Lines:** 1366  
**Global:** `globals.G_agent`

### Purpose

AgentCore is the **initialization hub and knowledge manager**. It:
- Loads configuration settings
- Initializes session context and history
- Provides the command knowledge cache
- Exposes utility functions (IP extraction, validation)

### Configuration Structure

```javascript
globals.G_agent.config = {
    outputLevel: 1,          // 0=silent, 1=normal, 2=verbose
    dryRun: false,          // Preview commands without executing
    aggressive: false,       // Enable aggressive exploitation
    stealth: false,         // Minimize detection footprint
    debug: false,           // Developer debug logging
    trainer: false,         // Pattern learning mode
    maxRetries: 3,          // Retry count for failed operations
    timeout: 30,            // Command timeout in seconds
    promptOnCritical: true, // Ask before dangerous operations
    promptOnAttack: true,   // Ask before offensive actions
    promptOnAmbiguous: true,// Ask when intent unclear
    promptOnSlow: true,     // Ask before slow operations
    promptOnDestructive: true, // Ask before file deletion
    autoFallback: true      // Automatically try alternatives
}
```

### Session Context

```javascript
globals.G_agentContext = {
    currentCommand: "",     // Last parsed command
    commandHistory: [],     // Array of previous commands
    activeSessions: {},     // Map of active sessions (shells, computers)
    dialogState: {},        // Multi-turn conversation state
    stateSnapshots: [],     // Undo/rollback checkpoints
    telemetry: [],          // Usage analytics
    patternHistory: [],     // Reinforcement learning data
    userPreferences: {}     // Learned user preferences
}
```

### Key Functions

#### `init()`
Initializes the AI system. Called automatically on first use.

```javascript
if not hasIndex(globals, "G_agent") then
    globals.G_agent = {}
    globals.G_agent.init()
end if
```

**What it does:**
- Creates default configuration
- Initializes command knowledge cache
- Sets up session context
- Loads user preferences from disk
- Registers all step handlers
- Initializes plan builders

#### `getCommandInfo(cmdName)`
Returns knowledge about a command by reading its man page.

```javascript
knowledge = globals.G_agent.getCommandInfo("chmod")
// Returns:
{
    "command": "chmod",
    "purpose": "Change file permissions",
    "requiresAdmin": false,
    "handlesFiles": true,
    "flags": {"-R": "Recursive"},
    "argv": ["permValue", "target"],
    "raw": "full man page text..."
}
```

**Caching:** Results are cached in `globals.G_agent.commandKnowledge` to avoid repeated man page reads.

#### `_extractIpFromText(text)`
Extracts IP addresses from natural language.

```javascript
ip = globals.G_agent._extractIpFromText("scan 192.168.1.1")
// Returns: "192.168.1.1"
```

Handles:
- IPv4 addresses
- CIDR notation (192.168.1.0/24)
- Hostnames (localhost, gateway)

### Example: Initialization Flow

```javascript
// User runs: ai "scan the local network"

// 1. AgentCore checks if initialized
if not globals.G_agent then
    // 2. Initialize configuration
    globals.G_agent.config = {outputLevel: 1, debug: false, ...}
    // 3. Load command knowledge cache
    globals.G_agent.commandKnowledge = {}
    // 4. Register handlers
    globals.G_agent._registerHandlers()
    // 5. Register plan builders
    globals.G_agent._registerPlanBuilders()
end if

// 6. Ready to process commands
```

---

## AgentParser

**File:** `agent_parser.src`  
**Lines:** 2975  
**Namespace:** `AgentParser`

### Purpose

AgentParser is the **natural language understanding engine**. It:
- Detects command intent from phrases
- Extracts parameters (files, IPs, users, permissions)
- Handles special cases and edge cases
- Maintains parsed command state

### Phrase Detection System

The core of the AI is **score-based phrase matching**. Each command has patterns with assigned scores.

#### How Scoring Works

```javascript
// Example patterns
patterns = {
    "chmod": {
        score: 27,
        keywords: ["permission", "chmod", "access rights"]
    },
    "mv": {
        score: 25,
        keywords: ["move", "rename", "relocate"]
    },
    "scan": {
        score: 20,
        keywords: ["scan", "probe", "check ports"]
    }
}
```

**Detection Process:**
1. Parse input for keywords
2. Calculate match score for each pattern
3. Select highest scoring pattern
4. Extract fields specific to that command

#### Score Ranges

| Score | Command Type | Example |
|-------|--------------|---------|
| 30-35 | High priority / specific | chog, iwlist, es |
| 25-29 | Medium priority | chmod, mv, cp |
| 20-24 | Low priority / generic | scan, find, grep |
| 10-19 | Dynamic fallback | Learned patterns |

### Pattern Conflict Resolution

**Problem:** Multiple commands can match the same phrase.

**Example:**
```
User: "remove all permissions of test"
- "remove" contains "move" → matches mv (25 points)
- "permissions" → matches chmod (27 points)
```

**Solution:** Use word boundaries and score comparison.

```javascript
// WRONG: Substring match
if indexOf(cmd, "move") != null then command = "mv"

// CORRECT: Word boundary match
if indexOf(cmd, "move ") != null or indexOf(cmd, " move") != null then
    if phraseScore == null or 25 > phraseScore then
        command = "mv"
        phraseScore = 25
    end if
end if
```

**Key Rule:** Only overwrite `command` if `newScore > phraseScore`.

### Field Extraction

After detecting the command, extract parameters.

#### Common Fields

- `target`: File, directory, or IP address
- `source`: Source file for copy/move operations
- `user`: Username for chown/chog
- `group`: Group name for chgrp
- `permValue`: Permission value for chmod (e.g., "755")
- `flag`: Command-line flag (e.g., "-R", "-l")
- `library`: Library name for exploit scanning
- `port`: Port number for network operations
- `service`: Service name (ssh, ftp, http)

#### Example: chmod Extraction

```javascript
// Pattern 1: "chmod of X to Y"
if indexOf(cmd, "chmod") != null and indexOf(cmd, " of ") != null then
    parts = split(cmd, " of ")
    if len(parts) >= 2 then
        afterOf = parts[1]
        toParts = split(afterOf, " to ")
        if len(toParts) >= 2 then
            parsed.target = toParts[0].trim()
            parsed.permValue = toParts[1].trim()
        end if
    end if
end if

// Pattern 2: "chmod X to Y"
if parsed.permValue == null and indexOf(cmd, " to ") != null then
    parts = split(cmd, " to ")
    if len(parts) == 2 then
        parsed.target = parts[0].replace("chmod", "").trim()
        parsed.permValue = parts[1].trim()
    end if
end if
```

#### Example: IP Extraction

```javascript
AgentParser._extractIpFromText = function(text)
    parts = split(text, " ")
    for part in parts
        // Check for IP pattern: X.X.X.X
        dotCount = 0
        for i in range(0, len(part) - 1)
            if part[i] == "." then dotCount += 1
        end for
        if dotCount == 3 then
            segments = split(part, ".")
            if len(segments) == 4 then
                valid = true
                for seg in segments
                    if to_int(seg) < 0 or to_int(seg) > 255 then
                        valid = false
                        break
                    end if
                end for
                if valid then return part
            end if
        end if
    end for
    return null
end function
```

### Special Handlers

#### Config Commands

Config commands (`ai aggressive on`) are detected early and bypass normal parsing.

```javascript
AgentParser._parseConfig = function(cmd)
    result = {"isConfig": false}
    
    // Skip if this is a setConfig/showConfig command
    if indexOf(cmd, "set ") != null or indexOf(cmd, "config ") != null then
        return result
    end if
    
    // Check for config keywords
    configKeywords = ["aggressive", "stealth", "dryRun", "debug"]
    settingFound = null
    
    for keyword in configKeywords
        if indexOf(cmd, keyword) != null then
            settingFound = keyword
            break
        end if
    end for
    
    if not settingFound then return result
    
    result.isConfig = 1
    
    // Determine value (on/off/toggle)
    if indexOf(cmd, " on") != null then
        globals.G_agent.config[settingFound] = true
    else if indexOf(cmd, " off") != null then
        globals.G_agent.config[settingFound] = false
    else
        // Toggle
        globals.G_agent.config[settingFound] = not globals.G_agent.config[settingFound]
    end if
    
    return result
end function
```

#### Hardcoded Patterns

Some commands have hardcoded patterns for performance:

```javascript
// Line 113 in agent_parser.src
hardcodedPatterns = ["scan", "fetch", "crackAll"]

if indexOf(cmd, "scan") != null then
    // Skip if this is actually an es or iwlist command
    if indexOf(cmd, "library") != null or 
       indexOf(cmd, "wireless") != null or 
       indexOf(cmd, "wifi") != null then
        // Let phrase detection handle it
        continue
    end if
    parsed.command = "scan"
end if
```

### Case Preservation

**Problem:** Commands are lowercase but filenames may be mixed case.

**Solution:** Store the original input in `parsed.raw` and extract from it.

```javascript
// Parse lowercase for matching
cmd = input.lower()
parsed.raw = input  // Keep original case

// Extract filename from original input
if indexOf(cmd, "file ") != null then
    // Find position in lowercase
    pos = indexOf(cmd, "file ") + 5
    // Extract from original (preserves case)
    filename = parsed.raw[pos:].trim()
    parsed.target = filename
end if
```

### Example: Full Parsing Flow

```javascript
// User input: "change permissions of MyFile.txt to 644"

// 1. Lowercase for detection
cmd = input.lower()  // "change permissions of myfile.txt to 644"
parsed.raw = input   // "change permissions of MyFile.txt to 644"

// 2. Phrase detection
if indexOf(cmd, "permission") != null and indexOf(cmd, "change") != null then
    command = "chmod"
    phraseScore = 27
end if

// 3. Field extraction (both patterns)
// Pattern 1: "of X to Y"
parts = split(cmd, " of ")  // ["change permissions", "myfile.txt to 644"]
afterOf = parts[1]          // "myfile.txt to 644"
toParts = split(afterOf, " to ")  // ["myfile.txt", "644"]
parsed.target = toParts[0]  // "myfile.txt" (wrong case!)

// 4. Case correction
// Extract from original input instead
ofPos = indexOf(parsed.raw, " of ") + 4
afterOf = parsed.raw[ofPos:]  // "MyFile.txt to 644"
toParts = split(afterOf, " to ")
parsed.target = toParts[0].trim()  // "MyFile.txt" (correct!)
parsed.permValue = toParts[1].trim()  // "644"

// 5. Result
parsed = {
    "command": "chmod",
    "target": "MyFile.txt",
    "permValue": "644",
    "raw": "change permissions of MyFile.txt to 644"
}
```

---

## AgentPlanning

**File:** `agent_planning.src`  
**Lines:** 1444  
**Namespace:** `AgentPlanning`

### Purpose

AgentPlanning converts parsed commands into **executable multi-step plans**. It:
- Creates step sequences
- Adds validation and fallback steps
- Assesses risk and success probability
- Adapts strategies based on context

### Plan Structure

```javascript
plan = {
    "goal": "Change file permissions",
    "steps": [
        {
            "type": "permissions",
            "description": "Set permissions on MyFile.txt to 644",
            "command": "chmod",
            "permValue": "644",
            "target": "MyFile.txt",
            "autonomous": false
        }
    ],
    "risk": "low",
    "estimatedTime": 5,
    "requiresEscalation": false
}
```

### Plan Builders

Each command type has a dedicated plan builder function.

#### Registration

```javascript
// agent_planning.src line 509-514
AgentPlanning._registerPlanBuilders = function()
    globals.G_agent._planBuilders = {}
    globals.G_agent._planBuilders.permissions = @globals.G_agent._buildPermissionsPlan
    globals.G_agent._planBuilders.scan = @globals.G_agent._buildScanPlan
    globals.G_agent._planBuilders.es = @globals.G_agent._buildEsPlan
    globals.G_agent._planBuilders.iwlist = @globals.G_agent._buildWifiPlan
    // ... more builders
end function
```

#### Example: Permissions Plan Builder

```javascript
AgentPlanning._buildPermissionsPlan = function(parsed, context)
    plan = {
        "goal": "Change permissions",
        "steps": [],
        "risk": "low"
    }
    
    step = {
        "type": "permissions",
        "command": parsed.command,  // chmod, chown, chgrp, or chog
        "target": parsed.target,
        "autonomous": false
    }
    
    // Copy relevant fields
    if hasIndex(parsed, "permValue") then step.permValue = parsed.permValue
    if hasIndex(parsed, "user") then step.user = parsed.user
    if hasIndex(parsed, "group") then step.group = parsed.group
    
    step.description = "Set " + parsed.command + " on " + parsed.target
    
    push(plan.steps, step)
    return plan
end function
```

#### Example: Scan Plan Builder

```javascript
AgentPlanning._buildScanPlan = function(parsed, context)
    plan = {
        "goal": "Scan target",
        "steps": [],
        "risk": "medium"
    }
    
    step = {
        "type": "scan",
        "command": "scan",
        "autonomous": true
    }
    
    // Handle flags
    if hasIndex(parsed, "flag") then
        step.flag = parsed.flag
        if parsed.flag == "-r" then
            step.description = "Scan random IP address"
        else if parsed.flag == "-l" then
            step.description = "Scan localhost"
        end if
    else
        step.target = parsed.target
        step.description = "Scan " + parsed.target
    end if
    
    // Add service if specified
    if hasIndex(parsed, "service") then
        step.service = parsed.service
    end if
    
    push(plan.steps, step)
    return plan
end function
```

### Multi-Step Plans

Complex operations require multiple steps with dependencies.

#### Example: Exploit Plan

```javascript
AgentPlanning._buildExploitPlan = function(parsed, context)
    plan = {"goal": "Exploit target", "steps": [], "risk": "high"}
    
    // Step 1: Scan for open ports
    scanStep = {
        "type": "scan",
        "target": parsed.target,
        "description": "Scan " + parsed.target + " for vulnerabilities"
    }
    push(plan.steps, scanStep)
    
    // Step 2: Find exploits
    findStep = {
        "type": "findExploits",
        "description": "Identify available exploits",
        "requiresObject": "computer"
    }
    push(plan.steps, findStep)
    
    // Step 3: Execute exploit
    exploitStep = {
        "type": "exploit",
        "description": "Execute exploit to gain access",
        "requiresObject": "computer"
    }
    push(plan.steps, exploitStep)
    
    // Step 4: Escalate (if needed)
    escStep = {
        "type": "escalate",
        "description": "Escalate to root privileges",
        "requiresObject": "shell",
        "optional": true
    }
    push(plan.steps, escStep)
    
    return plan
end function
```

### Fallback Steps

Plans can include fallback strategies for critical steps.

```javascript
// Primary step
primaryStep = {
    "type": "exploit",
    "description": "Exploit SSH vulnerability",
    "hasFallback": true
}
push(plan.steps, primaryStep)

// Fallback step
fallbackStep = {
    "type": "crackPassword",
    "description": "Brute force SSH password",
    "isFallback": true
}
push(plan.steps, fallbackStep)
```

**Execution behavior:**
- Execute primary step
- If primary succeeds, skip fallback
- If primary fails, execute fallback

### Risk Assessment

Plans are tagged with risk levels:

```javascript
if parsed.command == "rm" or parsed.command == "delete" then
    plan.risk = "high"
else if parsed.command == "exploit" or parsed.command == "attack" then
    plan.risk = "critical"
else
    plan.risk = "low"
end if

// Prompt user for high-risk operations
if plan.risk == "high" and globals.G_agent.config.promptOnDestructive then
    response = AgentPlanning._promptUser("This operation will delete files. Continue?")
    if not response then
        plan.canceled = true
        return plan
    end if
end if
```

---

## AgentExecution

**File:** `agent_execution.src`  
**Lines:** 518  
**Namespace:** `AgentExecution`

### Purpose

AgentExecution is the **plan execution engine**. It:
- Executes steps sequentially
- Tracks success/failure of each step
- Handles errors and triggers fallbacks
- Updates working objects as steps complete
- Injects dynamic steps (escalation, validation)

### Execution Flow

```javascript
AgentExecution._executePlan = function(Obj, plan, context)
    results = {
        "stepsCompleted": 0,
        "stepsFailed": 0,
        "success": false,
        "details": []
    }
    
    i = 0
    currentObj = Obj  // Track working object
    
    while i < len(plan.steps)
        step = plan.steps[i]
        
        // Execute step
        stepResult = globals.G_agent._executeStep(currentObj, step, context)
        push(results.details, stepResult)
        
        if stepResult.success then
            results.stepsCompleted += 1
            
            // Update working object if step returned new object
            if hasIndex(stepResult, "wrappedObj") then
                currentObj = stepResult.wrappedObj
            end if
        else
            results.stepsFailed += 1
            
            // Critical failure - try replanning
            if hasIndex(stepResult, "critical") and stepResult.critical then
                altPlan = globals.G_agent._createAlternativePlan(currentObj, step, results)
                if altPlan then
                    // Insert alternative steps
                    for altStep in altPlan.steps
                        push(plan.steps, altStep)
                    end for
                else
                    // No alternative - abort
                    results.message = "Critical step failed"
                    return results
                end if
            end if
        end if
        
        i += 1
    end while
    
    results.success = results.stepsFailed == 0
    return results
end function
```

### Step Execution

```javascript
AgentExecution._executeStep = function(Obj, step, context)
    // Look up handler for step type
    if not hasIndex(globals.G_agent._stepHandlers, step.type) then
        return {"success": false, "error": "No handler for step type: " + step.type}
    end if
    
    handler = globals.G_agent._stepHandlers[step.type]
    
    // Call handler
    result = handler(Obj, step, context)
    
    return result
end function
```

### Early Handlers (Bypass System)

Permission commands bypass the full step system for efficiency.

```javascript
AgentExecution._executeStep = function(Obj, step, context)
    command = step.command
    
    // Early handlers for simple commands
    if command == "chmod" then
        return globals.G_agent._handleChmod(Obj, step, context)
    else if command == "chown" then
        return globals.G_agent._handleChown(Obj, step, context)
    else if command == "chgrp" then
        return globals.G_agent._handleChgrp(Obj, step, context)
    else if command == "chog" then
        return globals.G_agent._handleChog(Obj, step, context)
    end if
    
    // Normal handler lookup
    // ...
end function
```

#### Example: chmod Handler

```javascript
AgentExecution._handleChmod = function(Obj, step, context)
    result = {"success": false, "step": "chmod"}
    
    // Extract fields
    permValue = step.permValue
    target = step.target
    
    if not permValue or not target then
        result.error = "Missing permission or target"
        return result
    end if
    
    // Build argv
    argv = [permValue, target]
    
    // Check for recursive flag
    argv = globals.G_agent._checkRecursiveFlag(Obj, "chmod", target, argv)
    
    // Execute command
    output = Obj.shell.host_computer.File(target).chmod(permValue)
    
    if output then
        result.success = true
        result.message = "Changed permissions on " + target + " to " + permValue
    else
        result.error = "chmod failed"
    end if
    
    return result
end function
```

### Recursive Flag Prompt

```javascript
AgentExecution._checkRecursiveFlag = function(Obj, command, target, argv)
    // Check if target is a directory
    isDir = false
    if typeof(Obj) == "map" and hasIndex(Obj, "shell") then
        file = Obj.shell.host_computer.File(target)
        if file and file.is_folder then isDir = true
    end if
    
    if isDir and globals.G_agent.config.promptOnAmbiguous then
        response = AgentPlanning._promptUser("Apply " + command + " recursively?")
        if response then
            // Insert -R flag at beginning
            argv = ["-R"] + argv
        end if
    end if
    
    return argv
end function
```

### Object Updating

As steps execute, they may return new objects (shells, computers, files).

```javascript
// Step returns a shell object
stepResult = {
    "success": true,
    "rawObject": shellObj,
    "wrappedObj": {"shell": shellObj, "computer": host_computer(shellObj)}
}

// Execution engine updates working object
if hasIndex(stepResult, "wrappedObj") then
    currentObj = stepResult.wrappedObj
end if

// Next step uses updated object
nextStepResult = handler(currentObj, nextStep, context)
```

### Dynamic Step Injection

The execution engine can inject steps mid-execution.

```javascript
// During execution, detect need for escalation
if stepResult.needsEscalation then
    escalateStep = {
        "type": "escalate",
        "description": "Escalate privileges",
        "requirements": step.requirements
    }
    // Insert after current step
    insert(plan.steps, i + 1, escalateStep)
end if
```

---

## AgentHandlers

**File:** `agent_handlers.src`  
**Lines:** 4206  
**Namespace:** `AgentHandlers`

### Purpose

AgentHandlers contains all **step type execution handlers**. Each handler:
- Validates step requirements
- Executes the operation
- Returns structured result

### Handler Structure

```javascript
AgentHandlers._handleXXX = function(Obj, step, context)
    result = {"success": false, "step": "xxx"}
    
    // 1. Validate requirements
    if not hasIndex(step, "target") then
        result.error = "No target specified"
        return result
    end if
    
    // 2. Execute operation
    output = Obj.shell.host_computer.someCommand(step.target)
    
    // 3. Parse output and return result
    if output then
        result.success = true
        result.output = output
    else
        result.error = "Command failed"
    end if
    
    return result
end function
```

### Scan Handler

```javascript
AgentHandlers._handleScan = function(Obj, step, context)
    result = {"success": false, "step": "scan"}
    
    // Check for flags
    if hasIndex(step, "flag") then
        if step.flag == "-r" then
            // Random IP scan
            randomIP = globals.G_agent._generateRandomIP()
            argv = ["-r"]
            result.description = "Scanning random IP: " + randomIP
        else if step.flag == "-l" then
            // Localhost scan
            argv = ["-l"]
            result.description = "Scanning localhost"
        else if step.flag == "-n" then
            // Network scan
            argv = ["-n"]
        end if
    else
        // Target-based scan
        target = step.target
        if not target then
            result.error = "No target specified for scan"
            return result
        end if
        
        argv = [target]
        
        // Add service if specified
        if hasIndex(step, "service") then
            argv.push(step.service)
        end if
    end if
    
    // Execute scan
    scanResult = Obj.shell.host_computer.scan(argv)
    
    if scanResult then
        result.success = true
        result.output = scanResult
        // Parse and wrap computer object if scan succeeded
        if typeof(scanResult) == "computer" then
            result.wrappedObj = {"computer": scanResult}
        end if
    else
        result.error = "Scan failed"
    end if
    
    return result
end function
```

### Exploit Handler

```javascript
AgentHandlers._handleExploit = function(Obj, step, context)
    result = {"success": false, "step": "exploit"}
    
    // Get computer object
    computer = null
    if hasIndex(Obj, "computer") then
        computer = Obj.computer
    else if typeof(Obj) == "computer" then
        computer = Obj
    end if
    
    if not computer then
        result.error = "No computer object to exploit"
        return result
    end if
    
    // Get available exploits
    exploitLib = include_lib("/lib/exploit.so")
    if not exploitLib then
        result.error = "Exploit library not available"
        return result
    end if
    
    availableExploits = exploitLib.scan(computer)
    if not availableExploits or len(availableExploits) == 0 then
        result.error = "No exploits found"
        return result
    end if
    
    // Try each exploit
    for exploit in availableExploits
        output = exploitLib.exploit(exploit)
        if output then
            result.success = true
            result.exploit = exploit
            // Check what we got
            if typeof(output) == "shell" then
                result.wrappedObj = {
                    "shell": output,
                    "computer": host_computer(output)
                }
            else if typeof(output) == "file" then
                result.wrappedObj = {"file": output}
            end if
            break
        end if
    end for
    
    if not result.success then
        result.error = "All exploits failed"
    end if
    
    return result
end function
```

### Data Extraction Handler

```javascript
AgentHandlers._handleDataExtraction = function(Obj, step, context)
    result = {"success": false, "step": "dataExtraction"}
    
    // Check for stored objects
    storedObj = globals.G_agent._selectStoredObject()
    
    if storedObj == "CANCELED" then
        result.error = "User canceled selection"
        return result
    end if
    
    if not storedObj then
        result.error = "No stored object available"
        return result
    end if
    
    // Check if router shell
    isRouterShell = hasIndex(storedObj.commands, "dig")
    
    if isRouterShell then
        // Use dig command
        digArgs = []
        if hasIndex(step, "flag") then push(digArgs, step.flag)
        
        output = storedObj.commands.dig(digArgs)
        
        if output then
            result.success = true
            result.data = output
        else
            result.error = "dig command failed"
        end if
    else
        // Use list command
        output = storedObj.commands.list()
        
        if output then
            result.success = true
            result.data = output
        else
            result.error = "list command failed"
        end if
    end if
    
    return result
end function
```

---

## AgentLearning

**File:** `agent_learning.src`  
**Lines:** 356  
**Namespace:** `AgentLearning`

### Purpose

AgentLearning implements **pattern reinforcement and persistent learning**. It:
- Tracks which patterns successfully matched (success/failure/total)
- Learns user-specific command and flag preferences
- Learns reusable templates from successful multi-step sequences
- Persists all learned data to disk as JSON
- Generates predictive suggestions based on context

### Pattern Reinforcement

```javascript
AgentLearning._reinforcePattern = function(command, success, context)
    // Extract pattern key (scan, exploit, crack, escalate, backdoor)
    patternKey = null
    cmdLower = lower(command)
    if indexOf(cmdLower, "scan") != null then patternKey = "scan"
    if indexOf(cmdLower, "exploit") != null then patternKey = "exploit"
    // ... etc
    
    // Track success/failure
    globals.G_agent.patternScores[patternKey].total += 1
    if success then
        globals.G_agent.patternScores[patternKey].success += 1
    else
        globals.G_agent.patternScores[patternKey].failure += 1
    end if
end function
```

### User Preference Tracking

```javascript
AgentLearning._trackUserPreferences = function(command, result)
    // Tracks command usage counts and flag preferences per command
    // e.g., if user frequently uses "scan -l", learns that preference
    globals.G_agent.userPreferences.commands[baseCmdLower] += 1
    
    // Track flags per command
    for flag in flags
        globals.G_agent.userPreferences.flags[baseCmdLower][flag] += 1
    end for
end function
```

### Learning Persistence (JSON)

Learning data is saved to `payload/data/agent_learning.json` using the same `System.toJSON`/`System.parse` format as config and knowledge files.

```javascript
// Save: Serializes patternScores, userPreferences, and templates to JSON
AgentLearning.saveLearning = function
    data = {}
    data.patternScores = globals.G_agent.patternScores
    data.userPreferences = globals.G_agent.userPreferences
    data.templates = globals.G_agent.sessionContext.templates
    jsonStr = System.toJSON(data, 1, 0)
    set_content(f, jsonStr)
end function

// Load: Parses JSON back into runtime structures
AgentLearning.loadLearning = function
    data = System.parse(content)
    // Restore pattern scores
    for key in indexes(data.patternScores)
        globals.G_agent.patternScores[key] = data.patternScores[key]
    end for
    // Restore templates (merge with existing, keep higher success count)
    for tmpl in data.templates
        // ... dedup by signature, push if new
    end for
end function
```

**File format example:**
```json
{
    "patternScores": {
        "scan": {"success": 5, "failure": 1, "total": 6},
        "exploit": {"success": 3, "failure": 0, "total": 3}
    },
    "userPreferences": {
        "commands": {"scan": 12, "exploit": 5},
        "flags": {"scan": {"-l": 3}}
    },
    "templates": [
        {
            "signature": "scan->exploit->crack",
            "successCount": 4,
            "lastUsed": 38.448,
            "steps": ["scan 1.2.3.4", "exploit ssh", "crack root"]
        }
    ]
}
```

**When is it called?**
- `saveLearning` is called after every successful command execution (in `agent_execute.src`)
- `loadLearning` is called during `init()` (in `agent_core.src`)

### Template Learning

Templates are learned automatically from successful multi-step sequences:

```javascript
// After each successful command, add to current sequence
push(globals.G_agent.sessionContext.currentSequence, command)

// When sequence reaches 3+ steps and succeeds, learn it
if len(sequence) >= 3 and result.success then
    globals.G_agent._learnTemplate(sequence)
    // Generates signature like "scan->exploit->crack"
    // Stores steps for later recall
end if
```

Templates with `successCount >= 2` are automatically recalled by the planner (see [Template Recall](#template-recall-in-planner)).

### Predictive Suggestions

After each operation, the system generates context-aware suggestions:

```javascript
// After scan
suggestions = ["Exploit found vulnerabilities"]
// After getting root
suggestions = ["Install backdoor for persistence"]
// After cracking password
suggestions = ["Use cracked credentials to login"]
```

---

## AgentRegistry

**File:** `agent_command_registry.src`  
**Lines:** 103  
**Namespace:** `AgentRegistry`

### Purpose

AgentRegistry stores **command metadata** that can't be extracted from man pages. It:
- Defines argv formats
- Maps flag meanings
- Specifies object type requirements
- Lists command aliases

### Registry Structure

```javascript
AgentRegistry.commandMeta = {
    "chmod": {
        "argv": ["permValue", "target"],
        "flags": {
            "-R": "Recursive"
        },
        "requiresObject": "file",
        "aliases": ["permissions", "access"]
    },
    "scan": {
        "argv": ["target", "service"],
        "flags": {
            "-r": "Random IP",
            "-l": "Localhost",
            "-n": "Network"
        },
        "requiresObject": "computer",
        "autonomous": true
    }
}
```

### Usage

```javascript
// Get command metadata
meta = AgentRegistry.commandMeta["chmod"]

// Build argv from step fields
argv = []
for field in meta.argv
    if hasIndex(step, field) then
        argv.push(step[field])
    end if
end for
```

---

## Recent Improvements

### v0.9.7.3 (March 2026)

Four major improvements were added to the AI agent system, followed by four more:

### 1. Context-Weighted Synonyms

**File:** `agent_parser.src`  
**Function:** `_expandWithSynonyms()`

The synonym system now uses **surrounding context** to disambiguate ambiguous words. Previously, a word like "break" would always map to a single command. Now it checks nearby words to pick the right match.

**How it works:**

```javascript
// Context hints for disambiguation
_synonymContext = {
    "crack": ["password", "hash", "login", "user", "account"],
    "exploit": ["system", "server", "port", "service", "vuln"],
    "scan": ["network", "ip", "host", "range", "port"],
    "fetch": ["file", "data", "download", "grab", "content"],
    // ... 12 context groups total
}
```

When a synonym matches multiple commands, each candidate gets a context score based on how many of its context hints appear in the input. Highest score wins.

**Example:**
```
"break the password" → crack (context: "password" matches crack group)
"break the system"   → exploit (context: "system" matches exploit group)
"probe the network"  → scan (context: "network" matches scan group)
```

### 2. Compound Command Parsing

**Files:** `agent_parser.src`, `agent_execute.src`

Users can now chain multiple commands in a single input using natural language connectors.

**Supported connectors:**
- "and then" → `scan 1.2.3.4 and then exploit it`
- "then" → `first scan the target then crack the password`
- "afterwards" → `exploit the server afterwards install backdoor`
- "after that" → `scan the network after that exploit ssh`

**How it works:**

The parser detects compound connectors, splits the input, and creates separate parsed commands for each sub-command. The executor then runs them sequentially, stopping on first failure.

```javascript
// Parser output for compound command
parsed = {
    "action": "compound",
    "compound": true,
    "subCommands": [
        {"raw": "scan 1.2.3.4"},
        {"raw": "exploit ssh"}
    ]
}

// Executor loops through sub-commands
for sub in parsed.subCommands
    result = globals.G_agent.execute(Obj, sub.raw)
    if not result.success then break
end for
```

**Note:** "first" is automatically stripped from the beginning of input when compound connectors are detected.

### 3. Learning Persistence (JSON)

**Files:** `agent_learning.src`, `agent_core.src`, `agent_execute.src`

All learning data is now persisted to `payload/data/agent_learning.json` between sessions. This includes pattern scores, user command/flag preferences, and learned templates.

- **Save:** Called after every successful command execution
- **Load:** Called during `init()` on startup
- **Format:** Standard JSON via `System.toJSON()`/`System.parse()` (same as config and knowledge)

See the [AgentLearning section](#agentlearning) for format details.

### 4. Template Recall in Planner (Fuzzy Matching)

**File:** `agent_planning.src`  
**Functions:** `_createPlan()`, `_scoreFuzzyTemplate()`

The planner checks learned templates before building a plan from scratch. Templates with `successCount >= 2` are scored using **fuzzy similarity matching** — the agent doesn't need an exact action word match anymore.

**How scoring works:**

| Match Type | Score | Example |
|-----------|-------|---------|
| Exact match (action in signature) | 1.0 | "scan" matches "scan->exploit->crack" |
| Similarity group match | 0.8 | "attack" matches "exploit" (same group) |
| High success bonus | +0.05-0.1 | Templates with >5 successes score slightly higher |
| No match | 0 | "install" vs "scan->exploit->crack" |

**Similarity groups:**
- exploit, attack, hack, pwn, compromise, break
- scan, probe, recon, enumerate, discover, check
- crack, brute, bruteforce, decrypt, password
- fetch, get, grab, pull, retrieve, extract, dump
- find, search, locate, look, list
- connect, ssh, shell, rshell, access, login
- install, deploy, setup, upload, push
- delete, remove, wipe, clean, purge

A template is used when its score exceeds **0.4** (at least a similarity group match). The highest-scoring template wins.

```javascript
// In _createPlan, before plan builder lookup:
bestTemplate = null
bestScore = 0
for tmpl in templates
    if tmpl.successCount >= 2 then
        score = _scoreFuzzyTemplate(parsed.action, tmpl)
        if score > bestScore then
            bestScore = score
            bestTemplate = tmpl
        end if
    end if
end for
if bestTemplate and bestScore >= 0.4 then
    // Use this template's steps as the plan
    plan.fromTemplate = true
    plan.templateScore = bestScore
end if
```

**Result:** "attack 1.2.3.4" can reuse a "scan->exploit->crack" template even though "attack" wasn't in the original signature.

### 5. Intent Clarification Dialog

**File:** `agent_parser.src`  
**Functions:** `_expandWithSynonyms()`, `_parseCommand()`

When the parser is uncertain about the user's intent, it now **asks** instead of guessing.

**Two clarification triggers:**

1. **Synonym tie-breaking:** When `_expandWithSynonyms` finds multiple synonym groups scoring equally, it presents a `Gui.choiceHybrid` menu letting the user pick the intended action.

2. **Fallback action prompt:** When the parser can't detect any action at all (would fall through to `directCommand`), it offers common actions: scan, exploit, crack, fetch, show, find, cancel.

**Example:**
```
> ai break the target
Agent: Multiple interpretations found. Did you mean:
  1. crack
  2. exploit
> [user selects "exploit"]
Agent: Planning exploit...
```

Both triggers require `promptOnAmbiguous` to be enabled (always true for interactive use, disabled in headless/test mode).

### 6. Enhanced Conditional Logic

**Files:** `agent_learning.src`, `agent_execute.src`

Two new conditional patterns and improved condition evaluation.

**New patterns in `_parseConditionals`:**

| Pattern | Example | Result |
|---------|---------|--------|
| "if X has/finds/shows Y, then Z" | "if scan has ssh, then exploit it" | `{condition: "has ssh", onCondition: "exploit it"}` |
| "X, if it works Y" | "scan 1.2.3.4, if it works exploit it" | `{condition: "success", onCondition: "exploit it"}` |
| "X, on success Y" | "scan 1.2.3.4, on success crack root" | `{condition: "success", onCondition: "crack root"}` |

**Enhanced condition evaluation in `execute()`:**

- **"vulnerable"** condition now searches through `primaryResult.details` step results (not just top-level data)
- **"has X"** condition: extracts keyword and searches through all result data, messages, and step details
- User-facing output shows condition status in skyblue

### 7. Multi-Target Support

**Files:** `agent_parser.src`, `agent_planning.src`, `agent_handlers.src`, `agent_execution.src`

Users can now target multiple IPs in a single command.

**Parser:** When 3+ IPs are detected (and no compound delimiters), the parser sets:
```javascript
parsed.action = "multiTarget"
parsed.multiTarget = true
parsed.targets = ["1.2.3.4", "5.6.7.8", "9.10.11.12"]
parsed.targetAction = "scan"  // first action word
```

**Planner:** `_buildMultiTargetPlan` creates one `multiTargetStep` per IP.

**Handler:** `_handleMultiTargetStep` executes each target as a sub-command via `globals.G_agent.execute(Obj, subCmd, {"headless":true})`, collecting results independently.

**Example:**
```
> ai scan 10.0.0.1 10.0.0.2 10.0.0.3
Agent: Multi-target scan on 3 targets
  Scanning 10.0.0.1...
  Scanning 10.0.0.2...
  Scanning 10.0.0.3...
```

---

## Testing

### The `ai test` Command

The AI system includes a built-in test suite accessible via the `ai test` command. This runs in-game and verifies all 4 recent improvements.

### Usage

```bash
ai test              # Run all test suites
ai test synonyms     # Test context-weighted synonyms only
ai test compound     # Test compound command parsing only
ai test persistence  # Test learning save/load only
ai test template     # Test template recall only
ai test fuzzy        # Test fuzzy template matching only
ai test conditional  # Test conditional parsing only
ai test multitarget  # Test multi-target parsing only
```

### Test Suites

| Suite | Tests | What it verifies |
|-------|-------|------------------|
| synonyms | 9 | Context-weighted disambiguation (break+password→crack, break+system→exploit, etc.) |
| compound | 8 | Compound connectors, sub-command splitting, "first" stripping, simple-not-compound |
| persistence | 10 | Save writes valid JSON with patterns/templates, load restores exact values after clear |
| template | 3 | Template recall for high-success templates, low-success templates skipped |
| fuzzy | 11 | Fuzzy similarity scoring: exact=1.0, group match>=0.7, unrelated=0, null=0, success bonus, plan creation |
| conditional | 7 | "if X has Y" pattern, "if it works" pattern, "on success" pattern, non-conditional returns null |
| multitarget | 6 | 3+ IPs trigger multiTarget, 2 IPs don't, plan creates multiTargetStep per IP |

### How Tests Work

Tests are implemented as an inline handler in `agent_handlers.src` (`_handleTest`). The handler uses a simple assert pattern:

```javascript
_assert = function(name, condition)
    if condition then
        print "  PASS: " + name
        passed += 1
    else
        print "  FAIL: " + name
        failed += 1
    end if
    total += 1
end function
```

The test command is wired through the standard pipeline:
1. **Parser:** `_commandPatterns` includes "test" → detects `ai test [suite]`
2. **Planner:** `_buildTestPlan` creates a test step with optional suite scope
3. **Handler:** `_handleTest` runs the specified suite(s) and prints results

### Adding New Tests

To add a new test suite, add a block in `_handleTest`:

```javascript
if suite == "all" or suite == "myfeature" then
    print yellow("=" * 50)
    print yellow("TEST: MY FEATURE")
    print yellow("=" * 50)
    
    // Your test assertions here
    _assert("test name", someCondition == true)
end if
```

No registration needed — the handler checks suite names directly.

---

## Adding New Commands

This section shows you **exactly how to add support for a new command** to the AI system.

### Step-by-Step Guide

#### 1. Choose Your Command

Let's add support for `tar` (archive files).

**Natural language goal:** "compress files into archive" or "tar myfiles into backup.tar"

#### 2. Add Phrase Pattern (agent_parser.src)

```javascript
// Around line 1220 in agent_parser.src
// Add to phrase detection section

// tar - compress/archive files (score: 26)
if (indexOf(cmd, "tar") != null or 
    indexOf(cmd, "compress") != null or 
    indexOf(cmd, "archive") != null) then
    if phraseScore == null or 26 > phraseScore then
        parsed.command = "tar"
        phraseScore = 26
    end if
end if
```

**Score selection:**
- Higher than generic commands (20-24)
- Lower than highly specific commands (30-35)
- 26 is good for medium-specific commands

#### 3. Add Field Extraction (agent_parser.src)

```javascript
// Around line 1700 in agent_parser.src
// Add to extraction section after other command extractions

// tar extraction
if parsed.command == "tar" then
    // Pattern: "tar X into Y" or "compress X to Y"
    if indexOf(cmd, " into ") != null then
        parts = split(cmd, " into ")
        if len(parts) >= 2 then
            // Extract source from original input (case preservation)
            intoPos = indexOf(parsed.raw, " into ")
            beforeInto = parsed.raw[:intoPos]
            afterInto = parsed.raw[intoPos + 6:]
            
            // Remove command words
            beforeInto = beforeInto.replace("tar", "").replace("compress", "").trim()
            parsed.source = beforeInto
            parsed.target = afterInto.trim()
        end if
    else if indexOf(cmd, " to ") != null then
        parts = split(cmd, " to ")
        if len(parts) >= 2 then
            toPos = indexOf(parsed.raw, " to ")
            beforeTo = parsed.raw[:toPos]
            afterTo = parsed.raw[toPos + 4:]
            
            beforeTo = beforeTo.replace("tar", "").replace("compress", "").trim()
            parsed.source = beforeTo
            parsed.target = afterTo.trim()
        end if
    end if
    
    // Extract flags (optional)
    if indexOf(cmd, "verbose") != null or indexOf(cmd, " -v") != null then
        parsed.flag = "-v"
    end if
    if indexOf(cmd, "zip") != null or indexOf(cmd, "gzip") != null then
        parsed.flag = "-z"
    end if
end if
```

#### 4. Create Plan Builder (agent_planning.src)

```javascript
// Around line 1400 in agent_planning.src
// Add plan builder function

AgentPlanning._buildTarPlan = function(parsed, context)
    plan = {
        "goal": "Create archive",
        "steps": [],
        "risk": "low"
    }
    
    step = {
        "type": "fileOperation",
        "command": "tar",
        "source": parsed.source,
        "target": parsed.target,
        "autonomous": false
    }
    
    if hasIndex(parsed, "flag") then
        step.flag = parsed.flag
    end if
    
    step.description = "Archive " + parsed.source + " into " + parsed.target
    
    push(plan.steps, step)
    return plan
end function

// Register the builder (around line 514)
AgentPlanning._registerPlanBuilders = function()
    // ... existing builders
    globals.G_agent._planBuilders.tar = @globals.G_agent._buildTarPlan
end function
```

#### 5. Create Step Handler (agent_execution.src or agent_handlers.src)

Option A: Early handler (simple commands)

```javascript
// In agent_execution.src around line 320
// Add to early handler section

else if command == "tar" then
    result = {"success": false, "step": "tar"}
    
    source = step.source
    target = step.target
    
    if not source or not target then
        result.error = "Missing source or target for tar"
        return result
    end if
    
    // Build argv
    argv = ["-cf", target, source]
    
    // Add flag if present
    if hasIndex(step, "flag") then
        // Insert flag before -cf
        argv[0] = step.flag + "cf"
    end if
    
    // Execute
    output = Obj.shell.host_computer.File(".").tar(argv)
    
    if output then
        result.success = true
        result.message = "Created archive " + target
    else
        result.error = "tar command failed"
    end if
    
    return result
end if
```

Option B: Full handler (complex commands)

```javascript
// In agent_handlers.src around line 4200

AgentHandlers._handleTar = function(Obj, step, context)
    result = {"success": false, "step": "tar"}
    
    // Validate requirements
    if not hasIndex(step, "source") or not hasIndex(step, "target") then
        result.error = "tar requires source and target"
        return result
    end if
    
    source = step.source
    target = step.target
    
    // Get shell
    shell = null
    if hasIndex(Obj, "shell") then
        shell = Obj.shell
    else if typeof(Obj) == "shell" then
        shell = Obj
    end if
    
    if not shell then
        result.error = "No shell available"
        return result
    end if
    
    // Build command
    argv = ["-cf", target, source]
    
    if hasIndex(step, "flag") and step.flag == "-v" then
        argv[0] = "-cvf"
    end if
    if hasIndex(step, "flag") and step.flag == "-z" then
        argv[0] = "-czf"
    end if
    
    // Execute
    computer = host_computer(shell)
    file = computer.File(".")
    output = file.tar(argv)
    
    if output then
        result.success = true
        result.message = "Created " + target
        result.output = output
    else
        result.error = "tar failed"
    end if
    
    return result
end function

// Register handler
AgentExecution._registerHandlers = function()
    // ... existing handlers
    globals.G_agent._stepHandlers.tar = @globals.G_agent._handleTar
end function
```

#### 6. Add Command Knowledge (Optional)

```javascript
// In agent_core.src around line 600
// Add to command knowledge defaults (for commands without man pages)

AgentCore._getDefaultKnowledge = function(cmdName)
    if cmdName == "tar" then
        return {
            "command": "tar",
            "purpose": "Create compressed archives",
            "handlesFiles": true,
            "flags": {
                "-c": "Create archive",
                "-x": "Extract archive",
                "-v": "Verbose output",
                "-z": "Gzip compression",
                "-j": "Bzip2 compression"
            },
            "argv": ["source", "target"]
        }
    end if
    // ... other defaults
end function
```

#### 7. Test Your Command

```bash
# Test various natural language patterns
ai "tar myfiles into backup.tar"
ai "compress Documents to archive.tar"
ai "create archive of Projects to backup.tar.gz with verbose"
```

### Summary Checklist

- [ ] Add phrase pattern with appropriate score
- [ ] Add field extraction with case preservation
- [ ] Create plan builder function
- [ ] Register plan builder
- [ ] Create step handler (early or full)
- [ ] Register step handler
- [ ] Add command knowledge (if no man page)
- [ ] Test natural language variations

---

## Pitfalls and Common Issues

### 1. Pattern Conflicts

**Problem:** Multiple commands match the same phrase.

**Example:**
```
"remove file permissions" matches both:
- rm (contains "remove")
- chmod (contains "permissions")
```

**Solutions:**

A. Use word boundaries:
```javascript
// WRONG
if indexOf(cmd, "remove") != null then command = "rm"

// CORRECT
if indexOf(cmd, "remove ") != null or indexOf(cmd, " remove") != null then
    command = "rm"
end if
```

B. Use score comparison:
```javascript
if indexOf(cmd, "remove") != null then
    if phraseScore == null or 23 > phraseScore then
        command = "rm"
        phraseScore = 23
    end if
end if

if indexOf(cmd, "permission") != null then
    if phraseScore == null or 27 > phraseScore then
        command = "chmod"
        phraseScore = 27  // Higher score wins
    end if
end if
```

C. Use exclusion keywords:
```javascript
// Skip "remove" if permission-related
if indexOf(cmd, "remove") != null then
    if indexOf(cmd, "permission") == null and indexOf(cmd, "access") == null then
        command = "rm"
    end if
end if
```

### 2. Score Overwrites

**Problem:** Lower-scoring patterns overwrite higher-scoring ones.

**Example:**
```javascript
// chmod sets score to 27
if indexOf(cmd, "permission") != null then
    command = "chmod"
    phraseScore = 27
end if

// mv overwrites without checking (WRONG!)
if indexOf(cmd, "move") != null then
    command = "mv"
    phraseScore = 25  // Lower score should NOT overwrite!
end if
```

**Solution:**
```javascript
// ALWAYS check score before overwriting
if indexOf(cmd, "move ") != null or indexOf(cmd, " move") != null then
    if phraseScore == null or 25 > phraseScore then
        command = "mv"
        phraseScore = 25
    end if
end if
```

### 3. Case Sensitivity

**Problem:** Filenames are case-sensitive but commands are lowercase.

**Example:**
```
User: "copy MyFile.txt to Documents"
Parsed: target = "myfile.txt"  // WRONG!
```

**Solution:** Store original input and extract from it.
```javascript
parsed.raw = input  // "copy MyFile.txt to Documents"
cmd = input.lower()  // "copy myfile.txt to documents"

// Detect command from lowercase
if indexOf(cmd, "copy") != null then command = "cp"

// Extract filename from ORIGINAL
toPos = indexOf(parsed.raw, " to ")
beforeTo = parsed.raw[:toPos]
filename = beforeTo.replace("copy", "").trim()  // "MyFile.txt"
parsed.source = filename
```

### 4. Missing Field Extraction

**Problem:** Command detected but parameters not extracted.

**Example:**
```javascript
// Command detected
if indexOf(cmd, "chmod") != null then command = "chmod"

// But no extraction!
// Result: parsed.permValue = null, parsed.target = null
```

**Solution:** Always add extraction after detection.
```javascript
if parsed.command == "chmod" then
    // Extract "chmod X to Y"
    if indexOf(cmd, " to ") != null then
        parts = split(cmd, " to ")
        parsed.target = parts[0].replace("chmod", "").trim()
        parsed.permValue = parts[1].trim()
    end if
end if
```

### 5. Hardcoded Pattern Priority

**Problem:** Hardcoded patterns (line 113) run before phrase detection.

**Example:**
```javascript
// Hardcoded scan pattern
if indexOf(cmd, "scan") != null then
    command = "scan"
end if

// Problem: "scan apt library" should trigger es, not scan!
```

**Solution:** Add skip logic for specialized commands.
```javascript
if indexOf(cmd, "scan") != null then
    // Skip if this is actually es or iwlist
    if indexOf(cmd, "library") != null or 
       indexOf(cmd, "wireless") != null or 
       indexOf(cmd, "wifi") != null then
        // Don't set command - let phrase detection handle it
    else
        command = "scan"
    end if
end if
```

### 6. Default Target Assignment

**Problem:** Default target overwrites extracted values.

**Example:**
```javascript
// Line 2928: Default target assignment
if not parsed.target then
    parsed.target = "~/Documents"
end if

// Problem: "scan random ip" sets flag="-r", but target gets set to Documents!
```

**Solution:** Skip default assignment for flagged commands.
```javascript
if not parsed.target then
    // Skip if command uses flags instead of targets
    if parsed.command == "scan" and hasIndex(parsed, "flag") then
        // Don't assign default target
    else
        parsed.target = "~/Documents"
    end if
end if
```

### 7. Recursive Flag Not Prompted

**Problem:** chmod/chown on directory doesn't ask about recursive.

**Cause:** Not checking if target is a directory.

**Solution:**
```javascript
AgentExecution._checkRecursiveFlag = function(Obj, command, target, argv)
    // Check if target is directory
    isDir = false
    if hasIndex(Obj, "shell") then
        file = Obj.shell.host_computer.File(target)
        if file and file.is_folder then isDir = true
    end if
    
    // Prompt user
    if isDir then
        response = AgentPlanning._promptUser("Apply recursively?")
        if response then
            argv = ["-R"] + argv
        end if
    end if
    
    return argv
end function
```

### 8. Plan Builder Not Registered

**Problem:** Plan created but steps never execute.

**Cause:** Forgot to register plan builder.

**Solution:**
```javascript
// 1. Create builder function
AgentPlanning._buildMyCommandPlan = function(parsed, context)
    // ...
end function

// 2. MUST register it!
AgentPlanning._registerPlanBuilders = function()
    globals.G_agent._planBuilders.mycommand = @globals.G_agent._buildMyCommandPlan
end function
```

### 9. Step Handler Not Registered

**Problem:** Step executes but handler not found.

**Error:** "No handler for step type: mycommand"

**Solution:**
```javascript
// 1. Create handler
AgentHandlers._handleMyCommand = function(Obj, step, context)
    // ...
end function

// 2. MUST register it!
AgentExecution._registerHandlers = function()
    globals.G_agent._stepHandlers.mycommand = @globals.G_agent._handleMyCommand
end function
```

### 10. Wrong Object Type

**Problem:** Handler expects shell but receives computer.

**Error:** "Cannot call command on null"

**Solution:** Always unwrap and validate object types.
```javascript
AgentHandlers._handleMyCommand = function(Obj, step, context)
    // Get shell from various object types
    shell = null
    if hasIndex(Obj, "shell") then
        shell = Obj.shell
    else if typeof(Obj) == "shell" then
        shell = Obj
    else if hasIndex(Obj, "computer") then
        // Try to get shell from computer
        // (may not exist)
        shell = null
    end if
    
    if not shell then
        result.error = "Command requires shell access"
        return result
    end if
    
    // Now safe to use shell
    output = shell.launch("command", "args")
end function
```

---

## Pros and Cons

### Pros

#### 1. Zero Hardcoded Commands
- System learns from man pages dynamically
- New commands automatically supported if man page exists
- No maintenance needed when game adds new commands

#### 2. Natural Language Interface
- Users can express intent in their own words
- Multiple phrasings for same command ("move X to Y", "relocate X to Y")
- Reduces learning curve for new users

#### 3. Modular Architecture
- Easy to add new commands
- Bug fixes isolated to specific modules
- Multiple developers can work simultaneously

#### 4. Context Awareness
- Tracks session state and command history
- Remembers previous objects (shells, computers)
- Learns user preferences over time

#### 5. Error Recovery
- Fallback steps for failed operations
- Dynamic replanning when critical steps fail
- User prompts for ambiguous situations

#### 6. Safety Features
- Dry-run mode to preview commands
- Prompts before destructive operations
- Risk assessment for dangerous commands

#### 7. Extensible Learning
- Pattern reinforcement improves accuracy
- User-specific preferences stored
- Telemetry for usage analytics

### Cons

#### 1. Complexity
- ~11,500 lines of code across 14 modules
- Steep learning curve for new developers
- Debugging pattern conflicts can be tedious

#### 2. Performance
- Man page parsing adds latency
- Phrase detection loops through all patterns
- Large context tracking increases memory usage

#### 3. Ambiguity Handling
- Natural language is inherently ambiguous
- Some phrases match multiple commands
- Users may get unexpected results

#### 4. Limited by Game API
- Can only do what game's command system allows
- Some operations require specific object types
- Error messages from game are opaque

#### 5. Maintenance Burden
- Pattern conflicts require manual fixes
- Score tuning needed for new commands
- Extraction logic can be brittle

#### 6. No Visual Feedback
- Text-only interface limits usability
- Users don't see what AI is planning
- No undo for executed commands

#### 7. Testing Difficulty
- Natural language inputs are infinite
- Hard to create comprehensive test suite
- Edge cases discovered by users in production

---

## Improvement Suggestions

### Short-Term Improvements

#### 1. Better Pattern Matching
**Current:** String indexOf with score comparison  
**Improvement:** Use regular expressions with capture groups
**Status:** Not started (GreyScript regex support is limited)

#### 2. Unified Field Extraction
**Current:** Each command has custom extraction logic  
**Improvement:** Generic parameter extractor using templates
**Status:** Not started

#### 3. Visual Plan Preview
**Current:** Plans execute immediately  
**Improvement:** Show plan steps before execution
**Status:** Not started (partially addressed by `dryRun` config)

#### 4. Command History Search
**Current:** No history search  
**Improvement:** Search previous commands
**Status:** Not started

#### 5. Undo Last Command
**Current:** No undo functionality  
**Improvement:** Reverse last operation via state snapshots
**Status:** Not started

### Medium-Term Improvements

#### 6. Intent Clarification Dialog
**Current:** AI guesses user intent  
**Improvement:** Ask clarifying questions when ambiguous
**Status:** Not started

#### ~~7. Batch Operations~~ ✅ IMPLEMENTED (v0.9.7.3)
**Implemented as:** Compound command parsing  
**Usage:** `ai scan 1.2.3.4 and then exploit ssh`  
**See:** [Compound Command Parsing](#2-compound-command-parsing)

#### 8. Conditional Logic
**Current:** Linear step execution  
**Improvement:** if/else branching in plans
**Status:** Not started

#### 9. Parallel Execution
**Current:** Sequential steps  
**Improvement:** Run independent steps in parallel
**Status:** Not started

#### ~~10. Smart Defaults~~ ✅ IMPLEMENTED (v0.9.7.3)
**Implemented as:** Learning persistence + user preference tracking  
**Details:** User command/flag preferences persist to disk and survive sessions  
**See:** [Learning Persistence](#3-learning-persistence-json)

### Long-Term Improvements

#### 11. Machine Learning Integration
**Current:** Rule-based pattern matching  
**Improvement:** Train neural network on user commands
**Status:** Not feasible (GreyScript has no ML libraries)

#### 12. Voice Input
**Current:** Text only  
**Improvement:** Speech recognition
**Status:** Not feasible (game limitation)

#### 13. Multi-Turn Conversations
**Current:** Ambiguous-action clarification uses `dialogState` (typed `ai <option>` follow-up)  
**Improvement:** Broader multi-turn context beyond clarification  
**Status:** Partial — `startDialog` / `resolveDialog` wired for `ambiguousAction`

#### ~~14. Proactive Suggestions~~ ✅ IMPLEMENTED
**Implemented as:** `_generateSuggestions()` in `agent_learning.src`  
**Details:** After each operation, context-aware suggestions are printed (e.g., "Escalate to root" after getting shell, "Install backdoor" after getting root)

#### 15. Collaborative Planning
**Current:** AI plans alone  
**Improvement:** User participates in planning
**Status:** Not started

---

## Code Examples

### Example 1: Simple Command Parsing

```javascript
// User input: "show me the file test.txt"

// 1. Parser detects command
cmd = "show me the file test.txt"
if indexOf(cmd, "show") != null and indexOf(cmd, "file") != null then
    command = "cat"
    phraseScore = 22
end if

// 2. Extract filename
if indexOf(cmd, "file ") != null then
    pos = indexOf(cmd, "file ") + 5
    target = cmd[pos:].trim()  // "test.txt"
end if

// 3. Create plan
plan = {
    "goal": "Display file contents",
    "steps": [
        {
            "type": "fileOperation",
            "command": "cat",
            "target": "test.txt"
        }
    ]
}

// 4. Execute
computer = get_shell.host_computer
file = computer.File("test.txt")
output = file.get_content()
print output
```

### Example 2: Multi-Step Plan

```javascript
// User input: "break into 192.168.1.1 and get the password file"

// 1. Parse command
parsed = {
    "command": "exploit",
    "target": "192.168.1.1",
    "goal": "getPasswords"
}

// 2. Create multi-step plan
plan = {
    "goal": "Exploit target and extract passwords",
    "steps": [
        {
            "type": "scan",
            "target": "192.168.1.1",
            "description": "Scan 192.168.1.1 for vulnerabilities"
        },
        {
            "type": "findExploits",
            "description": "Identify available exploits",
            "requiresObject": "computer"
        },
        {
            "type": "exploit",
            "description": "Execute exploit to gain shell",
            "requiresObject": "computer"
        },
        {
            "type": "escalate",
            "description": "Escalate to root",
            "requiresObject": "shell",
            "optional": true
        },
        {
            "type": "dataExtraction",
            "flag": "-p",
            "description": "Extract password file",
            "requiresObject": "shell"
        }
    ]
}

// 3. Execute plan step by step
results = globals.G_agent._executePlan(Obj, plan)
```

### Example 3: Pattern Conflict Resolution

```javascript
// User input: "remove all permissions from test.txt"

// WRONG WAY: First match wins
if indexOf(cmd, "remove") != null then
    command = "rm"  // Wrong! User wants chmod, not rm
end if

// CORRECT WAY: Score-based with keyword checks
phraseScore = null

// Check for rm
if indexOf(cmd, "remove ") != null or indexOf(cmd, " remove") != null then
    // But skip if permission-related
    if indexOf(cmd, "permission") == null and indexOf(cmd, "access") == null then
        if phraseScore == null or 23 > phraseScore then
            command = "rm"
            phraseScore = 23
        end if
    end if
end if

// Check for chmod (higher score)
if indexOf(cmd, "permission") != null then
    if phraseScore == null or 27 > phraseScore then
        command = "chmod"
        phraseScore = 27  // Higher score wins!
    end if
end if

// Result: command = "chmod" (correct!)
```

### Example 4: Case-Preserving Extraction

```javascript
// User input: "copy MyFile.txt to MyBackup.txt"

// Store original input
parsed.raw = "copy MyFile.txt to MyBackup.txt"
cmd = input.lower()  // "copy myfile.txt to mybackup.txt"

// Detect command from lowercase
if indexOf(cmd, "copy") != null then
    command = "cp"
end if

// Extract filenames from ORIGINAL input (preserves case)
if indexOf(cmd, " to ") != null then
    toPos = indexOf(parsed.raw, " to ")
    beforeTo = parsed.raw[:toPos]  // "copy MyFile.txt"
    afterTo = parsed.raw[toPos + 4:]  // "MyBackup.txt"
    
    source = beforeTo.replace("copy", "").trim()  // "MyFile.txt"
    target = afterTo.trim()  // "MyBackup.txt"
    
    parsed.source = source
    parsed.target = target
end if

// Result:
// parsed.command = "cp"
// parsed.source = "MyFile.txt"  (correct case!)
// parsed.target = "MyBackup.txt"  (correct case!)
```

### Example 5: Adding Command Knowledge

```javascript
// Get knowledge about chmod command
knowledge = globals.G_agent.getCommandInfo("chmod")

// Returns:
{
    "command": "chmod",
    "purpose": "Change file mode bits",
    "handlesFiles": true,
    "requiresAdmin": false,
    "flags": {
        "-R": "Change files and directories recursively",
        "-v": "Verbose output",
        "-c": "Report only when changes made"
    },
    "argv": ["mode", "file"],
    "raw": "chmod - change file mode bits\n\nSYNOPSIS\n..."
}

// Use knowledge to build command
argv = []
for param in knowledge.argv
    if hasIndex(step, param) then
        push(argv, step[param])
    end if
end for
// argv = ["755", "test.txt"]
```

### Example 6: Dynamic Plan Adaptation

```javascript
// Execute plan with dynamic injection

currentObj = {"shell": userShell}
i = 0

while i < len(plan.steps)
    step = plan.steps[i]
    result = executeStep(currentObj, step)
    
    if result.success then
        // Update working object
        if hasIndex(result, "wrappedObj") then
            currentObj = result.wrappedObj
        end if
        
        // Check if we need escalation
        if hasIndex(result, "needsEscalation") and result.needsEscalation then
            // Inject escalation step
            escalateStep = {
                "type": "escalate",
                "description": "Escalate privileges"
            }
            insert(plan.steps, i + 1, escalateStep)
        end if
    else
        // Step failed - try fallback
        if step.hasFallback then
            // Execute fallback on next iteration
            i += 1
            continue
        else
            // No fallback - abort
            break
        end if
    end if
    
    i += 1
end while
```

### Example 7: Learning from User Behavior

```javascript
// User runs: "ai aggressive on"
globals.G_agent.config.aggressive = true

// Track this preference
AgentLearning._learnPreference("usesAggressive", true)

// Next session: Auto-enable aggressive if user always uses it
if globals.G_agentContext.userPreferences.usesAggressive then
    globals.G_agent.config.aggressive = true
    print "AI: Aggressive mode enabled (user preference)"
end if
```

---

## Conclusion

The X AI Agent System is a sophisticated natural language command interface with a modular, extensible architecture. With 14 source files and ~11,500 lines, it provides a powerful way for users to interact with the game using everyday language.

**Key Takeaways for Developers:**
1. Always use score comparison to prevent pattern conflicts
2. Preserve original input case for filename extraction
3. Register both plan builders and step handlers
4. Test with `ai test` after making changes
5. Add exclusion logic for conflicting keywords
6. Use JSON (`System.toJSON`/`System.parse`) for all data persistence
7. Guard `range()` loops against empty lists (`range(0, -1)` crashes)

**Recent Additions (v0.9.7.3):**
- Context-weighted synonym disambiguation
- Compound command parsing ("X and then Y")
- JSON-based learning persistence
- Template recall in planner
- Built-in `ai test` command with 30 tests across 4 suites

For questions or contributions, refer to the codebase comments and this handbook.

---

**Document Version:** 2.0  
**AI System Version:** 0.9.7.3  
**Last Updated:** March 2026
