# AI Agent System

## Overview

The AI agent system provides intelligent command parsing and automated task execution for Grey Hack operations. It interprets natural language commands and routes them to appropriate execution paths based on the requested action and access level requirements.

## Configuration Management

### Config Commands

The agent supports two types of configuration commands:

#### Temporary Toggles (Not Saved)

Simple config names toggle settings temporarily without saving to disk:

```bash
ai debug       # Toggle debug mode
ai aggressive  # Toggle aggressive mode
ai stealth     # Toggle stealth mode
ai trainer     # Toggle trainer mode
ai dryRun      # Toggle dry-run mode
```

**Behavior:** Flips the boolean value without persistence. Settings revert on agent restart.

#### Permanent Settings (Saved to Disk)

Use `set` command to make permanent changes:

```bash
ai set debug on            # Enable debug and save
ai set debug off           # Disable debug and save
ai set outputLevel 2       # Verbose mode (0=silent, 1=normal, 2=verbose)
ai set maxRetries 5        # Set max retries and save
ai set timeout 30          # Set timeout and save
ai set promptOnAttack yes  # Enable attack prompts
```

**Behavior:** Sets value explicitly and saves to `agent_config.json`. Persists across sessions.

**Value Normalization:**
- `on`, `yes`, `true`, `enabled` → `true`
- `off`, `no`, `false`, `disabled` → `false`
- Numbers are parsed as integers/floats

#### Display Configuration

```bash
ai show config    # Display all settings organized by category
ai display config # Alias for show config
ai view config    # Alias for show config
```

**Output Format:**
```
=== Agent Configuration ===

[Behavior Settings]
  outputLevel: 1  # (0=silent, 1=normal, 2=verbose)
  debug: true
  dryRun: false

[Operation Modes]
  aggressive: false
  stealth: false
  trainer: false

[Operation Limits]
  maxRetries: 3
  timeout: 30
  maxTargets: 50
  maxDepth: 3

[User Prompts]
  promptOnAttack: true
  promptOnCritical: true
  promptOnAmbiguous: true
  promptOnSlowOperation: true
  promptOnMissingInfo: true
  promptOnDestructive: true
```

#### Reset Configuration

```bash
ai reset config         # Reset all settings to defaults and save
ai restore defaults     # Alias for reset config
```

**Default Values:**
- `outputLevel: 1` (0=silent, 1=normal, 2=verbose)
- `debug: false`
- `aggressive: false`
- `stealth: false`
- `dryRun: false`
- `trainer: false`
- `maxRetries: 3`
- `timeout: 30`
- `maxTargets: 50`
- `maxDepth: 3`
- `promptOnCritical: false`
- `promptOnAttack: true`
- `promptOnAmbiguous: true`
- `promptOnSlow: true`
- `promptOnDestructive: true`
- `autoFallback: false`

### Config File Location

Configuration is saved to `agent_config.json` in the same directory as `agent_knowledge.json`.

**File Structure:**
```json
{
  "config": {
    "outputLevel": 1,
    "debug": true,
    "maxRetries": 5,
    ...
  },
  "promptPreferences": {
    "question_hash": "always",
    ...
  }
}
```

### Available Configuration Options

#### Behavior Settings
- **outputLevel** (integer): Output verbosity (0=silent, 1=normal, 2=verbose)
- **debug** (boolean): Show internal decision making
- **dryRun** (boolean): Show plan without executing

#### Operation Modes
- **aggressive** (boolean): Try all available methods
- **stealth** (boolean): Minimize traces
- **trainer** (boolean): Show commands without executing

#### Operation Limits
- **maxRetries** (integer): Maximum retry attempts (default: 3)
- **timeout** (integer): Operation timeout in seconds (default: 30)
- **maxTargets** (integer): Maximum targets to process (default: 50)
- **maxDepth** (integer): Maximum recursion depth (default: 3)

#### User Prompts
- **promptOnAttack** (boolean): Ask before attacking
- **promptOnCritical** (boolean): Ask before critical operations
- **promptOnAmbiguous** (boolean): Ask when multiple choices available
- **promptOnSlow** (boolean): Warn before slow operations
- **promptOnDestructive** (boolean): Confirm destructive actions

#### Advanced Settings
- **autoFallback** (boolean): Automatically try alternatives on failure (default: false)

## Autonomous Mode

### Overview

Autonomous mode enables the agent to make all exploitation decisions automatically. When triggered by keywords like "you decide", "use your judgment", or "figure out", the agent:

1. **Scans target** using database-aware scanning (checks `Exploit.haveAlready()` first)
2. **Scores all exploits** from cached database without executing (metadata-based)
3. **Filters by requirements** (privilege, object type, library type, target IP)
4. **Executes best first** - tries highest scoring exploit until success
5. **Activates object** using `Exploit.getShell/getComputer/getFile`

### Autonomous Triggers

Keywords that activate autonomous mode:
- `you decide`
- `use your judgment`
- `figure out`
- `think for yourself`
- `choose your own`
- `be creative`

### Basic Autonomous Commands

```bash
ai you decide how to attack 29.91.110.203
ai use your judgment to scan 192.168.1.1
ai figure out how to exploit 10.0.0.1
```

### Requirement Filtering

Autonomous mode supports natural language requirements that filter exploits:

#### Privilege Requirements
```bash
ai you decide...I need a root computer on 192.168.0.3
ai decide...I need a user shell
ai attack...get me a guest computer
```

**Scoring**: root=100, user=50, guest=10

#### Object Type Requirements
```bash
ai decide...I need a shell
ai attack...get me a computer  
ai decide...I need a file
```

**Scoring**: shell=30, computer=20, file=10

#### Library Type Requirements
```bash
ai decide...I need a router shell
ai attack...get me an http computer
ai decide...I need an ssh shell
ai figure out...ftp access
ai decide...sql database access
```

Filters exploits to only those from matching library types.

#### Target IP Requirements
```bash
ai you decide...I need a computer on 192.168.0.3
ai attack 29.91.110.203...need shell on 192.168.0.5
```

For LAN IPs, triggers automatic router bounce attack.

### LAN Bounce Attacks

The agent provides fully automated exploitation of private network targets through router bounce mechanisms.

#### LAN IP Detection

**Supported Ranges:**
- `192.168.0.0/16` - Class C private networks
- `172.16.0.0/12` - Class B private networks (172.16.x.x - 172.31.x.x)
- `10.0.0.0/8` - Class A private networks
- `127.0.0.0/8` - Localhost/loopback addresses

**Detection:** `is_lan_ip(ip)` checks against these ranges

#### Multi-IP Command Support

**Syntax:** `get [object] on [LAN_IP] via [ROUTER_IP]`

**Parser Behavior:**
- Extracts ALL IPs from command
- Prioritizes LAN IPs as target
- Public IPs become router IP
- Stores in `parsed.extractedIps` array

**Examples:**
```bash
ai get all accounts on 192.168.0.7 via 74.108.64.217
ai get into 192.168.1.5 via 29.91.110.203
ai fetch shell from 10.0.0.15 via 94.90.194.186
```

#### Attack Path Priority

The agent uses a 4-tier priority system for LAN exploitation:

##### 1. Root Router Bounce (Best/Most Direct)

**Conditions:**
- Vulnerable library config settings are configured (vulnLibrary, vulnVersion, vulnMemAddr, vulnUnsafeVal)
- Router shell available via `Attack.scanCustom([publicIP, "router", "s"])`

**Method:** `Mission.getRootBounce(publicIP, lanIP, i)`

**Benefits:**
- Uses configured vulnerable library settings
- Guaranteed root access
- Most reliable and efficient path
- Respects user's custom configurations

**When Used:**
- User has configured vulnerable library for root exploits
- Router shell is accessible
- Highest priority when conditions met

##### 2. Direct Bounce Exploits

**Method:**
1. Scan router: `Exploit.extract(router, publicIP)`
2. Filter for bounce exploit types: 'l' (LAN), 'i' (internal), 'c' (computer)
3. Execute: `overflow(metaLib, memAddr, unsafeVal, lanIP)`
4. Returns computer object directly

**Benefits:**
- No shell route needed
- Fastest when bounce exploits available
- Direct exploitation without intermediate steps
- Skips shell acquisition if successful

**When Used:**
- Router has bounce exploits in cache
- No config settings configured (or shell route failed)
- Falls back to shell route if no bounce exploits found

##### 3. Shell Route

**Method:**
1. Get router shell: `Attack.scanCustom([publicIP, "router", "s"], true)`
2. Escalate privileges: `ShellObject.headlessSu(shell)`
3. Pack metaxploit: `ShellObject.packMeta(shell)`
4. Scan for bounce: `Exploit.scanForExploit(shell, ["bounce", lanIP], true, headless)`

**Benefits:**
- Works when no direct bounce exploits
- Automated exploit discovery from shell
- Handles both headless and interactive modes
- Supports continuation commands

**When Used:**
- No direct bounce exploits found
- Config settings not configured
- Router shell is available

##### 4. LAN Setup Fallback (Last Resort)

**Triggered Only When:**
- Config settings NOT configured, OR
- No router shell available

**Method:**
1. Scan network for ANY shell: `Attack.scanCustom(["http","s"], true)`
2. If no router shells, scan for any service
3. Use captured shell to scan network for routers
4. Pack metaxploit on captured shell
5. Proceed with bounce attack

**Benefits:**
- Most resilient approach
- Works without router shell
- Adapts to network conditions
- Last resort when others unavailable

**When Used:**
- No router shell available
- Config settings not configured
- Other paths failed

#### Smart Account Listing

The agent automatically selects the optimal list command based on rainbow table availability.

**Commands:**
- `list -sB` - Uses rainbow tables for instant password lookup (when available)
- `list -sD` - Direct brute force decipher with progress bars (when rainbow tables unavailable)

**Applied To:**
- Data extraction from LAN computers
- Continuation commands after bounce
- All parser-generated list commands

#### Data Extraction from LAN Targets

**Handler:** `_handleDataExtraction(Obj, step, context)`

**Flow:**
1. Detect LAN IP with `is_lan_ip(targetIp)`
2. Extract router IP from `step.extractedIps` or auto-detect
3. Convert to `getObject` bounce attack step
4. Execute `_handleGetObject()` to gain access
5. Run appropriate list command on obtained computer

**Example Command:**
```bash
ai get all accounts on 192.168.0.7 via 74.108.64.217
```

**Example Output (With Rainbow Tables):**
```
Agent: LAN target 192.168.0.7 detected - converting to bounce attack
Agent: Converting to LAN bounce attack: 74.108.64.217 -> 192.168.0.7
Agent: Attempting to access 192.168.0.7 via 74.108.64.217
Agent: Config settings configured - checking for router shell...
Agent: Using root router bounce method (most direct)
Agent: Got access to 192.168.0.7, listing accounts...
Agent: Rainbow tables available - using list -sB
[i] Using dictionary attack...
[i] Found the following Accounts:
User  Account: [ root ] password: [ Raristo ]
User  Account: [ Resnut ] password: [ lowme ]
Email Account: [ Resnut@coxukuxox.com ] password: [ schoco ]
```

**Example Output (Without Rainbow Tables):**
```
Agent: No rainbow tables - using list -sD (direct decipher)
Agent: Running list -sD on 192.168.0.7...
[i] Deciphering...
[###################################]==[ 100% ]
[###################################]==[ 100% ]
[###################################]==[ 100% ]
[i] Found the following Accounts:
User  Account: [ root ] password: [ Raristo ]
```

#### Router Auto-Detection

When only LAN IP provided, agent auto-detects router:

**Detection Methods (Priority Order):**
1. Check `step.extractedIps` for public IP
2. Check `context.target` for different IP
3. Scan network: `Attack.scanCustom(["router","s"], true)`
4. Extract from shell: `shell.host_computer.lan_ip`

**Example:**
```bash
ai get into 192.168.0.7  # No router specified
# Agent scans network and finds router automatically
```

#### Autonomous Mode Integration

**Works seamlessly with autonomous commands:**
```bash
ai you decide how to attack 192.168.1.5
ai use your judgment to scan 29.91.110.203 I need a root computer on 192.168.0.3
ai figure out how to get into 10.0.0.15
```

**Autonomous Flow:**
1. Scans router (public IP)
2. Finds exploits in cache
3. Detects LAN target requirement
4. Automatically selects bounce attack path
5. Executes with appropriate priority
6. Returns wrapped object

**Example:**
```bash
ai use your judgment to scan 29.91.110.203 I need a root computer on 192.168.0.3
```

**Execution:**
1. Scans 29.91.110.203 (router)
2. Finds 2 libraries in cache
3. Detects 192.168.0.3 is LAN IP
4. Checks config settings → configured
5. Gets root shell on router
6. Uses Mission.getRootBounce
7. Bounces to 192.168.0.3 for root computer
8. Opens computer object for user

### Scoring System

Exploits are scored by combining:

**Base Scores**:
- Shell: 30
- Computer: 20  
- File: 10
- Root: 100
- User: 50
- Guest: 10

**Requirement Bonuses** (when matching):
- Target IP match: +30
- Privilege match: +50
- Object type match: +20
- Library type match: +20

**Example**: Root shell on exact target IP = 30 + 100 + 30 + 50 + 20 = 230

### Database Integration

Autonomous mode leverages the exploit database:

- **Exploit.haveAlready(metaLib)**: Checks if library+version cached
- **Exploit.headless(metaLib)**: Only called for NEW libraries
- **Database metadata**: `exploit.e` (s/c/f), `exploit.u` (r/u/g)
- **Score-first strategy**: All scoring from metadata, no execution until selected

This eliminates redundant scanning and enables intelligent exploit selection.

## Command Parsing

### Command Structure

The agent parses natural language commands to extract:
- **Action Type**: What operation to perform (get object, execute command, etc.)
- **Object Type**: Target type (computer, shell, file)
- **Access Level**: Required privilege level (root, admin, elevated, etc.)
- **Network Parameters**: Public IP and LAN IP addresses
- **Execution Mode**: Headless (intermediate) or interactive (final)

### Example Commands

```
need a root computer from 94.90.194.186 on 172.16.9.5
need an admin computer from [publicIP] on [lanIP]
need an elevated shell from [publicIP] on [lanIP]
need the best computer from [publicIP] on [lanIP]
need a highest computer from [publicIP] on [lanIP]
```

### Chaining Operations

The agent supports chaining keywords to create multi-step operations where earlier steps are headless (non-interactive):

**Chaining Keywords**: `to`, `then`, `and then`, `also`, `unless`

**Example Commands**:
```
get root on 94.90.194.186 then extract emails
need shell on [IP] to crack passwords
get computer on [IP] also backdoor it
need access to [IP] unless root available
```

When chaining keywords are detected, the first step executes in headless mode, allowing the agent to proceed directly to the next operation without user interaction.

### Conditional/Fallback Operations

The agent supports conditional execution with automatic fallback:

**Conditional Keywords**: `if`, `or just`, `or get`, `otherwise`

**Example Commands**:
```
get emails if easy or just get users
extract bank or get users
get emails otherwise get users
```

**Execution Flow**:
1. Agent tries the primary operation (emails/bank)
2. If successful, skips the fallback step
3. If failed, automatically executes the fallback operation (users)

## Access Level Detection

### Root/Admin Keywords

The agent sets `needRoot=true` when detecting these keywords:
- **root** - Requires root user access
- **admin** - Requires administrator privileges
- **elevated** - Requires elevated permissions
- **best** - Implies highest available access
- **highest** - Explicitly requests maximum privileges

### Implementation

Located in `agent.src` around line 870:

```greyscript
if requestingObject then
  //Determine if root access is required
  needRoot=false
  if indexOf(cmd,"root")!=null then needRoot=true
  if indexOf(cmd,"admin")!=null then needRoot=true
  if indexOf(cmd,"elevated")!=null then needRoot=true
  if indexOf(cmd,"best")!=null then needRoot=true
  if indexOf(cmd,"highest")!=null then needRoot=true
```

## Data Extraction

### Email Extraction

**Command Pattern**: `i need all the emails from [IP]`

**Parsing**:
- Sets `action="extractData"`
- Sets `dataType="email"`
- Extracts target IP from command

**Execution Path**:
1. Attack router at target IP to get shell
2. Get headless shell using `Exploit.getShell`
3. Execute dig command: `shell.commands["dig"](["-e", "-s"])`
   - `-e` flag for email data
   - `-s` flag to save extracted data
4. Parse output for success/failure indicators

**Implementation**: Located in `Agent._handleDataExtraction` (line ~2516)

### Data Type Mappings

The agent maps data type keywords to dig command flags:

| Data Type | Keyword | Dig Flag | Command |
|-----------|---------|----------|---------|
| Email | `email` | `-e` | `shell.commands["dig"](["-e", "-s"])` |
| Bank | `bank` | `-b` | `shell.commands["dig"](["-b", "-s"])` |
| User | `user`, `account`, `credential` | `-u` | `shell.commands["dig"](["-u", "-s"])` |
| RShell | `rshell` | `-r` | `shell.commands["dig"](["-r", "-s"])` |
| All | `data`, `everything` | `-a` | `shell.commands["dig"](["-a", "-s"])` |

### Router Shell Execution

The agent uses the shell command system, not raw shell launches:

**Correct**: `shell.commands["dig"](["-e", "-s"])`
**Incorrect**: `shell.shell.launch("dig -e -s")` ❌

This is because `dig` is a custom X command, not a native shell command. It must be called through the shell object's command map.

## Command Knowledge System

### Mission Path (Root Access)

**When**: `needRoot=true` (command contains root/admin/elevated/best/highest)

**Method**: `Mission.getRootBounce(publicIP, lanIP, i)`

**Purpose**: 
- Uses vulnerable library exploitation
- Targets root-level access specifically
- Leverages mission system's existing root access methods
- Settings-dependent behavior

**Use Cases**:
- Penetration testing requiring root shells
- Administrative access for system modifications
- Privilege escalation scenarios

### Automated Path (Any Access)

**When**: `needRoot=false` (standard computer/shell requests)

**Method**: `Attack.scanCustom` → `ShellObject.headlessSu` → `Exploit.scanForExploit`

**Purpose**:
- Automated exploitation of any available access
- Uses any user level (root, user, or guest)
- Headless scanning and exploitation
- More flexible but no privilege guarantee

**Use Cases**:
- General access to target systems
- Reconnaissance operations
- Non-privileged task execution

## Conditional Routing Logic

Located in `agent.src` around line 2589:

```greyscript
if needRoot then
  Mission.getRootBounce(publicIP, lanIP, i)
else
  // Automated path
  Attack.scanCustom(...)
  ShellObject.headlessSu(...)
  Exploit.scanForExploit(...)
end if
```

## Object Types

### Computer
- Full system access
- File system navigation
- Service enumeration
- Network operations

### Shell
- Command execution interface
- User-level permissions
- Interactive or headless modes
- Can be upgraded to root via exploits

### File
- Direct file object access
- Read/write operations
- Permission-dependent access

## Execution Modes

### Interactive Mode
- Final goal of command chain
- User interaction enabled
- Full shell interface
- Direct command execution

### Headless Mode
- Intermediate step in chain
- Automated operations only
- No user interaction
- Used for pivoting/chaining

## Integration with Other Systems

### Mission System
- `Mission.getRootBounce`: Primary root access method
- Uses vulnerable library database
- Supports multi-hop exploitation
- Configuration via settings

### Exploit System
- `Exploit.scanForExploit`: Automated exploit discovery
- `Exploit.headless`: Library scanning
- Exploit cache management
- Router extraction for proxy chains

### Attack System
- `Attack.scanCustom`: Custom IP scanning
- Port enumeration
- Service identification
- Exploit opportunity detection

### Shell Management
- `ShellObject.headlessSu`: Privilege escalation attempts
- Shell persistence
- Session management
- Logging and tracking

## Agent State Management

### Global State
- `needRoot`: Boolean flag for access level requirement
- `requestingObject`: Boolean flag indicating object request
- `objectType`: String identifying target type
- `isHeadless`: Boolean flag for execution mode
- `parsed.action`: Action type identifier

### Session Context
- Current shell tracking
- Hop chain management
- Proxy state preservation
- Cache integration

## Error Handling

### Loop Prevention
- Proper conditional routing prevents infinite loops
- Each path has distinct failure modes
- Fallback mechanisms for unavailable exploits
- IP tracking to avoid duplicate attempts

### Failure Modes
- Mission path failure: Falls back to manual methods
- Automated path failure: Continues to next target
- Empty router extracts: Logged and skipped
- Missing exploits: Cache loading attempted

## Performance Considerations

### Exploit Caching
- Per-host exploit cache during operations
- Global cache persistence across sessions
- Key format: `lib_name_version`
- Reduces redundant metaxploit scans

### IP Tracking
- `seen={}` map tracks attempted IPs
- Prevents duplicate router attempts
- Per-function scope (router, hop, decoy)
- Avoids wasted cycles on dead IPs

### Router Prioritization
- Root exploits tried before guest exploits
- Manual sorting: `qRoot=[]`, `qGuest=[]`
- Concatenation: `q=qRoot+qGuest`
- Maximizes privilege level obtained

## Best Practices

### Command Clarity
- Use explicit keywords (root, admin, elevated)
- Include both public IP and LAN IP when known
- Specify object type clearly
- State execution mode if non-standard

### Access Level Selection
- Use root/admin only when necessary
- Standard access sufficient for most operations
- Root access triggers different code path
- Consider operational security implications

### Error Recovery
- Monitor agent logs for loop indicators
- Check conditional routing logic if loops occur
- Verify needRoot parsing for new keywords
- Test both execution paths independently

## Troubleshooting

### Agent Loops
**Symptom**: Agent repeats same operation indefinitely

**Diagnosis**:
1. Check if conditional routing uses proper `needRoot` flag
2. Verify keyword detection in command parsing
3. Ensure both paths (mission/automated) are accessible
4. Look for missing exploit cache entries

**Solution**: Verify agent.src line ~2589 uses `if needRoot then` not `if true then`

### Failed Root Access
**Symptom**: Root access requested but not obtained

**Diagnosis**:
1. Verify `needRoot=true` is set (check keywords)
2. Check if Mission.getRootBounce is available
3. Review settings configuration
4. Validate vulnerable library database

**Solution**: Use correct keywords or check mission system configuration

### No Automated Access
**Symptom**: Automated path fails to get any shell

**Diagnosis**:
1. Check exploit cache is loaded
2. Verify Attack.scanCustom functionality
3. Review target has exploitable services
4. Check network connectivity

**Solution**: Run `Exploit.loadCache` or restart with cache refresh

## Future Enhancements

### Potential Improvements
- Priority-based exploit selection
- Machine learning for exploit success prediction
- Adaptive retry strategies
- Multi-target parallel operations
- Enhanced natural language understanding
- Context-aware command interpretation

### Keyword Expansion
- Add language variations (superuser, privileged, administrator)
- Support for custom privilege levels
- Configurable keyword mappings
- Internationalization support

## Advanced Features

### Chaining Operations

The agent supports chaining keywords to create multi-step operations where earlier steps are headless (non-interactive):

**Chaining Keywords**: `to`, `then`, `and then`, `also`, `unless`

**Example Commands**:
```
ai get root on 94.90.194.186 then extract emails
ai need shell on [IP] to crack passwords
ai get computer on [IP] also backdoor it
ai need access to [IP] unless root available
```

**How It Works**: When chaining keywords are detected, `isHeadless=true` is set for the first step, allowing the agent to proceed directly to the next operation without entering the interactive loop.

**Implementation**: Located in `agent.src` line ~879

### Conditional/Fallback Operations

The agent supports conditional execution with automatic fallback:

**Conditional Keywords**: `if`, `or just`, `or get`, `otherwise`

**Example Commands**:
```
ai get emails if easy or just get users
ai extract bank or get users
ai get emails otherwise get users
```

**Execution Flow**:
1. Agent creates primary step with `hasFallback=true` flag
2. Agent creates fallback step with `isFallback=true` flag
3. Executes primary operation first
4. If primary succeeds, skips fallback step automatically
5. If primary fails, executes fallback operation

**Implementation**: 
- Parsing: `agent.src` line ~965
- Plan creation: `agent.src` line ~2180
- Execution logic: `agent.src` line ~2330

### Shorthand Command System

**Overview**: Single-word commands that execute common operations using the last target from session context.

**Available Shorthands**:

| Command | Action | Description |
|---------|--------|-------------|
| `ai emails` / `ai email` | Extract email data | Runs dig -e on last target |
| `ai bank` / `ai banks` | Extract bank data | Runs dig -b on last target |
| `ai users` / `ai user` | Extract user data | Runs dig -u on last target |
| `ai rshell` / `ai rshells` | Extract rshells | Runs dig -r on last target |
| `ai data` / `ai all` | Extract all data | Runs dig -a on last target |
| `ai scan` | Scan target | Scans last target |

**How It Works**:
1. Agent detects single-word command without IPs/targets
2. Retrieves last target from `sessionContext.lastTarget`
3. Creates extraction/scan plan with context target
4. Executes without requiring full command syntax

**Example Workflow**:
```
ai i need all emails from 94.90.194.186  // Sets last target to 94.90.194.186
ai users                                  // Uses 94.90.194.186 from context
ai bank                                   // Uses 94.90.194.186 from context
ai scan                                   // Scans 94.90.194.186
```

**Benefits**:
- Rapid successive operations on same target
- Minimal typing for common tasks
- Intuitive natural language interface
- Automatic context management

**Implementation**: Located in `agent.src` line ~825 (parsing) and line ~2162 (context resolution)

## Troubleshooting

### LAN Bounce Exploit Failures

**Error Message**: `"No exploits found for type: l"` or `"Unable to find or execute bounce exploit to [IP]"`

**Root Cause**: The exploit database doesn't have any exploits marked as bounce type ("l") for router libraries.

**Why This Happens**:
1. Bounce exploits are **auto-detected from ANY library on a router** (not just kernel_router.so)
2. When an exploit on a router returns a `computer` object, it's actually accessing a LAN device
3. Detection requires `Exploit.headless(library, true)` to be run with the router flag
4. During headless scanning, exploits are tested - those that return `computer` objects get marked as type "l" (bounce)
5. If exploits fail during testing (return strings/errors/numbers), they remain type "?" (unknown)

**Automatic Fix (v1.2+)**:
The AI agent now automatically:
- Detects when router libraries are cached but haven't been tested for bounce exploits
- Runs `Exploit.headless(metaLib, true)` with router flag to properly identify bounce exploits
- Works with **any library on a router**, not just kernel_router.so

**Manual Solution** (if automatic fix doesn't work):

1. **Ensure router has libraries with exploits**:
   ```bash
   # From shell on router
   ls /lib
   ```

2. **Manually scan router libraries** to update the exploit database:
   ```bash
   # Scan all libraries on the router
   metalib scan
   
   # Or scan a specific library
   metalib scan libname
   ```

3. **Verify exploits were detected**:
   ```bash
   # Check exploit cache for bounce exploits
   metalib list
   # Look for exploits with type 'l' or 'i'
   ```

4. **Alternative: Use Mission.getRootBounce** (requires config settings):
   ```bash
   # Set vulnerable library configuration
   ai set vulnLibrary library.so
   ai set vulnVersion 1.1.5
   ai set vulnMemAddr 844
   ai set vulnUnsafeVal 233
   ```

**Technical Details**:

From `Exploit.headless()` in exploit.src (updated logic):
```greyscript
Exploit.headless=function(m,isRouter=false)
  // ... scan exploits ...
  //If on router and returns computer, it's a bounce exploit (LAN access)
  if isRouter and obj=="computer" then
    self.change(v,m,"bounce",ex)
    hasSaved=true
    continue
  end if
```

**Key Insight**: Any library on a router that has an exploit returning a `computer` object is a bounce exploit, because the computer is actually a LAN device behind that router. The library name (kernel_router, libssh, etc.) is irrelevant - what matters is:
1. The library is on a router
2. The exploit returns a computer object

**Code Fix Applied** (agent_handlers.src):
```greyscript
//Pass true to indicate this is a router library
Exploit.headless(metaLib, true)

//Check if exploits have been tested
needsUpdate=false
hasUntestedExploits=false
hasBounceExploits=false
for exploit in cache.exploits
  if hasIndex(exploit,"e") then
    if exploit.e=="?" or exploit.e=="t" then hasUntestedExploits=true
    if exploit.e=="l" or exploit.e=="i" or exploit.e=="c" then hasBounceExploits=true
  end if
end for
//Test untested exploits if no bounce exploits found yet
if hasUntestedExploits and not hasBounceExploits then needsUpdate=true
```

**Workaround**: If bounce exploits can't be detected, the AI agent will fall back to the shell-based route:
1. Get root shell on router
2. Pack metaxploit on shell
3. Use `Exploit.scanForExploit()` from the router shell to reach LAN targets

This fallback is slower but doesn't require pre-configured bounce exploits.

## Stored Objects Workflow

The AI agent supports storing compromised objects (computers, shells, files) for persistent use across multiple commands. This allows you to capture remote access once and execute multiple operations without re-exploiting.

### Storing Objects

**Syntax:** Add `and store` or `and store it` to any object acquisition command.

**Examples:**
```bash
ai I need a root computer on 192.168.1.3 from 144.35.59.147 and store
ai get a shell on 10.0.0.5 via 94.90.194.186 and store it
ai fetch file /etc/passwd from 172.16.0.10 and store
```

**Behavior:**
- Parser detects `store` keyword and sets `shouldStore` flag
- Handler obtains the object (computer/shell/file) 
- Wrapped session object is stored in `globals.G_agentContext.storedObjects`
- Multiple objects can be stored simultaneously (managed as array)

### Using Stored Objects

**Automatic Usage:**
Once an object is stored, ALL subsequent AI commands automatically execute against the most recently stored object instead of your local workstation.

**Examples:**
```bash
# Store remote computer
ai get root computer on 192.168.1.3 from 144.35.59.147 and store

# Now these commands execute on 192.168.1.3 (not local workstation)
ai get all accounts          # Lists accounts on stored computer
ai goto /etc                 # Changes directory on stored computer
ai list /home                # Lists directory on stored computer
ai get all emails            # Extracts emails from stored computer
```

**Important:** Navigation commands like `ai goto /lib` will change the directory context on the stored remote object, not your local terminal. The stored object maintains its own session state including current directory.

### Managing Stored Objects

**View Stored Objects:**
```bash
ai status
```

**Output:**
```
[i] AI Agent Status:
  Commands executed: 5
  Active sessions: 0
  Last target: 192.168.1.3
  Last action: getObject
  Compromised hosts: 0
  Available shells: 0
  Stored objects: 1
    1. Root Computer - 144.35.59.147 : 192.168.1.3
  Output: Normal
  Dry run: 0
  Aggressive: 0
  Stealth: 0
```

**Clear Stored Objects:**
```bash
ai clear stored objects       # Clear all stored objects
ai clear stored object 1      # Clear specific object by index
```

**Behavior:**
- Clearing stored objects returns command execution to your local workstation
- Multiple stored objects are managed in order (most recent = last stored)
- When multiple objects exist, commands use the most recent one

### Stored Object Types

**Supported Types:**
- **Computer Objects**: Full computer access with command interface
- **Shell Objects**: Shell access with limited commands
- **File Objects**: File handles for reading/writing

**Access Levels:**
- `Root` - Administrator/root access
- `User` - Standard user access

### Context-Aware Command Execution

The agent automatically detects machine types and selects appropriate commands based on the target system.

**Machine Types:**
- **Router/Switch**: Network routing devices
- **Workstation**: Standard computers
- **Camera**: Surveillance/IoT devices
- **Corrupted**: Damaged/inaccessible systems

**Command Selection:**

| Machine Type | Account Listing | Email Extraction | Data Commands |
|--------------|----------------|------------------|---------------|
| Router/Switch | `dig -u` | `dig -e` | `dig` commands |
| Workstation/Camera | `list -sB` (with rainbow) or `list -sD` (without) | `list -sB` | `list` commands |
| Corrupted | Error: "System is corrupted" | N/A | N/A |

**Corrupted Systems:**
- Automatically detected and rejected before exploitation attempts
- Returns error immediately to save time

**Example:**
```bash
ai list accounts
```

**Behavior:**
- Router/Switch → executes `dig -u` (router-specific user enumeration)
- Workstation/Camera → executes `list -sB` or `list -sD` based on rainbow table availability
- Corrupted → returns error without execution

### Navigation Patterns

The agent supports natural language navigation commands that execute on the current context (local or stored object).

**Syntax:**
```bash
ai go to <location>
ai goto <location>
ai navigate to <location>
```

**Location Resolution:**
- `root` → `/root`
- `home` → `~`
- `etc` → `/etc`
- `var` → `/var`
- `usr` → `/usr`
- `bin` → `/bin`
- `opt` → `/opt`
- `lib` → `/lib` (absolute path if starts with `/`, else relative)

**Examples:**
```bash
ai goto home              # cd ~
ai go to /etc             # cd /etc
ai goto var               # cd /var
ai goto lib               # cd lib (relative)
ai goto /lib              # cd /lib (absolute)
```

**With Stored Objects:**
```bash
# Store remote computer
ai get root computer on 192.168.1.3 from 144.35.59.147 and store

# Navigation executes on stored object (192.168.1.3)
ai goto /etc              # Changes directory on 192.168.1.3
ai go to lib              # Changes directory on 192.168.1.3
```

**Important:** Navigation commands modify the directory context of the active session (stored object or local workstation). The change persists within that session but won't be visible in your main terminal prompt if executing on a stored object.

## Internal Features

### Dialog State

The agent maintains dialog state for multi-turn conversations:

**State Structure:**
```javascript
{
  "active": false,          // Whether dialog is in progress
  "context": null,          // Current context
  "question": null,         // Pending question
  "expectedResponse": null, // Expected response format
  "callback": null          // Handler function
}
```

**Usage**: Internal system for managing conversational flow and user prompts.

### State Snapshots

The agent maintains state snapshots for undo/rollback functionality (future enhancement):

**Configuration:**
- Maximum snapshots: 10
- Snapshots include: command, target, source, timestamp

**Note**: Undo functionality is currently a placeholder for future implementation.

### Telemetry Logging

The agent logs telemetry data for session analysis:

**Tracked Data:**
- Session start time
- Commands executed
- Decisions made
- Operation outcomes

**Purpose**: Internal analytics for pattern learning and agent improvement.

### Pattern Reinforcement

The agent tracks pattern scores to learn from successful operations:

**Mechanism:**
- Tracks which patterns successfully matched
- Learns user-specific command preferences
- Adjusts phrase scores over time (capped at 35)
- Stores learned data to disk periodically

**Note**: Enable `trainer` mode to activate pattern reinforcement learning.

## Related Documentation

- [STRATEGIC_KNOWLEDGE.md](STRATEGIC_KNOWLEDGE.md) - Strategic planning and knowledge persistence
- [KNOWLEDGE_PERSISTENCE.md](KNOWLEDGE_PERSISTENCE.md) - Cross-session data retention
- [GREYSCRIPT_REFERENCE.md](GREYSCRIPT_REFERENCE.md) - Language syntax and constraints
- [X.md](X.md) - Main system documentation

## Dependencies

### Required Libraries
- `agent.src` - Agent command parsing and routing
- `Mission.src` - Mission-based exploitation (root access)
- `Attack.src` - Attack scanning and discovery
- `Exploit.src` - Exploit database and execution
- `ShellObject.src` - Shell management and operations

### Supporting Systems
- Proxy management (router exploitation)
- Cache system (password/exploit caching)
- Log system (operation tracking)
- Session management (shell tracking)

## Notes

- Agent routing logic must check `needRoot` flag properly
- Root exploit prioritization applies to proxy router operations
- GreyScript constraints: no inline `else if` after `then`
- Router user levels: only "r" (root) or "g" (guest), never "u" (user)
- Exploit caching significantly improves performance
- IP tracking prevents infinite loops on unavailable targets