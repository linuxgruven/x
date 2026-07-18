X - Full Help & Reference
=========================

  X is a hacking framework for Grey Hack. It gives you a unified shell
  with 100+ commands for scanning, exploitation, recon, password cracking,
  pivoting, proxying, and automation — all in one place.

  X is designed to feel like a real Linux/Unix shell. If you have any
  experience with Bash, terminal commands, or Unix-style tools, you will
  feel right at home. Commands like cat, grep, awk, cut, find, sed, sort,
  and pipe syntax all work the way you would expect.

  If you are coming from Windows or a different Grey Hack tool,
  expect a short learning curve. The concepts are the same as Linux —
  files, paths, pipes, flags — but the style takes a little getting used
  to. The man pages and this README are your best starting points.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TABLE OF CONTENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Installation
  2. Initial Setup
  3. Understanding the Prompt
  4. Database Maintenance
  5. Basic Usage
       5a. Proxying
       5b. Scanning
       5c. Dig (LAN Recon)
       5d. Piping
  6. Help System
  7. Q & A


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. INSTALLATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  IMPORTANT: Do NOT place installer files inside the payload folder.
             Place them in your home directory. The payload folder is
             created automatically and must stay at the top level.

  Layout required:

    /home/<user>/
      X             <-- installers go here (home dir, not in payload)
      man
      passwords
      ...
      payload/      <-- created by X on first run, do not put installers here

  Run each installer IN ORDER from your home directory:

    1. X           - Run first. Sets up the required folder structure.
    2. man         - Installs man pages.
    3. passwords   - Installs password wordlists.
    4. sources     - Installs source code packages.
    5. bash        - Installs some basic bash scripts.
    6. bash-tests  - Installs some extended bash scripts.
                     (use these to get a better understanding of bash)
    7. exploits    - Installs the exploit library.

  Each installer accepts a --delete flag that removes the installer
  file itself after a successful run. Use this to clean up your home
  directory once installation is complete:

    man --delete
    bash --delete
    exploits --delete
    (etc.)

  After all installers have run, save a copy of libhttp.soV1.0.0 to:

    ~/payload/savedLibs/


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2. INITIAL SETUP  (run these once, inside X)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  rainbow -n
    Build your rainbow tables. Select yes when asked to auto-load.

  config -y
    (Optional) Enables auto-reconnect to your last proxy on startup.
    Recommended — saves time every session.

  config -v http
    Set your root bounce library to HTTP.

  config -x 9
    Set the bounce exploit index to 9 (adjust to match your library).

  sys check
    Auto-installs any missing system libraries. Run this to set up needed
    libraries that x will use when in autonomous mode.

  ai learn all
    (Optional) Teaches the AI assistant every command. Speeds up AI
    responses significantly. Run once after first install.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  3. UNDERSTANDING THE PROMPT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  The prompt shows your current context at a glance:

    [MAIN][P][tux~Workstation@92.11.2.162:192.168.0.2] [/home/tux]

    MAIN        - Session layer (MAIN, PROXY, PIVOT, RSHELL, etc.)
    P           - Passwd access: green = readable, red = no access,
                  red X = passwd file missing
    R           - Root indicator: green [R] = root password cached for
                  this network (all machines on the same network share
                  the same root password), not shown otherwise
    tux         - Current user
    Workstation - System type (Workstation, Router, Switch)
    92.11.2.162 - Public IP
    192.168.0.2 - LAN IP
    /home/tux   - Current working directory


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4. DATABASE MAINTENANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  !! IMPORTANT — A stale or empty database is the #1 reason attacks fail.
     If scan finds a vulnerability but the exploit doesn't work, or dig
     says it has no bounce, the database is almost always the problem.
     Run "pacman -Sy -e" and "exp router" regularly.

  !! ROUTER EXPLOITS ARE CRITICAL — nearly every remote attack path goes
     through a router in some way:
       - Bounce exploits (needed by dig, recon, and others) come from
         router kernel libraries. Without them, LAN bouncing doesn't work.
       - exp bounce discovers bounce exploits.
       - exp router covers the router kernel across many targets.
     Run "exp router" and "exp bounce" more often than other services.
     If you can't bounce, you can't reach most LAN targets.

  Keep your exploit database fresh. Always be proxied before running these.

  ── pacman -Sy -e ──────────────────────────────────────────────────────

    Syncs your exploit database, targeting public ports on the internet.
    This is the main update command — run it regularly.

      pacman -Sy -e            - Sync exploits (public ports)
      pacman -Sy -e -c 10      - Sync with 10 attempts per target
      pacman -Sy -e -c 100     - Sync with 100 (needs decent hardware)
      pacman -Sy -e -f         - Re-scan library versions already in the database
      pacman -Sy -e --force    - Force-scan every library encountered (full rescan)

    Start with -c 10 on default hardware. Increase once you upgrade.

  ── pacman -Sy -l ──────────────────────────────────────────────────────

    Separate command — syncs your exploit database targeting local
    libraries (not public internet ports).

      pacman -Sy -l            - Sync exploits (local libraries)
      pacman -Sy -l -c 10      - Sync local with 10 attempts per target

  ── exp router ─────────────────────────────────────────────────────────

    Runs passes against targets to update exploits for a specific service.
    Each command searches for new exploits and adds them to the database.
    Default passes: router=100, all others=10.

      exp router     - Update router exploits (100 passes default) *PRIORITY*
      exp bounce     - Discover LAN bounce exploits from router /lib *PRIORITY*
      exp ssh        - Update SSH exploits
      exp http       - Update HTTP exploits
      exp ftp        - Update FTP exploits
      exp smtp       - Update SMTP exploits
      exp rshell     - Update rshell exploits
      exp repo       - Update repository exploits
      exp sql        - Update SQL exploits

  ── exp all  (optional -p) ─────────────────────────────────────────────

    Refreshes all exploit types at once. Use -p to control how many
    passes it runs per library (default is 10).

      exp all           - Refresh all exploit types (10 passes each)
      exp all -p 25     - Refresh all with 25 passes (more thorough)
      exp all -p 5      - Quick refresh (fewer passes, less coverage)

    Higher pass counts find rarer exploits but take longer to complete.

  ── other useful exp commands ──────────────────────────────────────────

      exp -l            - List all exploits in the database
      exp top           - Show the easiest exploits in the database (fewest
                          requirements first) — useful for finding quick wins
      exp backup        - Back up your exploit database (do this often!)
      exp restore       - Restore from backup
      exp defrag        - Clean up orphaned index entries
      exp bloom -s      - Show bloom filter stats (saturation, item count)

  !! 0DAYS — When a 0day cycle is active, libraries on target machines have
     known unpatched vulnerabilities that are much easier to exploit. This is
     the best time to scan and build your database. You can also use 0day to
     patch libraries on your system or servers
     (preventing others from using them against you).

       0day mode        - Enable 0day mode (disables auto log wiping so you
                          don't accidentally clear mission logs that contain
                          information needed to complete the 0day mission)
       0day -p ssh      - Patch the SSH library on the current target
       0day -pa /lib    - Patch all libraries in /lib on the current target
       0day left        - Time remaining in the current 0day cycle
       0day next        - Time until the next 0day cycle begins
       0day purge       - Clear all stored PObject data when done

     When the cycle ends, run "0day purge" to clear out the stale 0day
     exploit data and stored engineer credentials.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5. BASIC USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  !! QUITTING X — If you have any active sessions (shells, proxies,
     pivots), always quit with "sess -x" instead of just closing the
     terminal. This lets each session clean up properly — closing shells,
     clearing stashes, and releasing resources. Hard-closing without it
     can leave logs.

       sess -x    - Cleanly close all active sessions and quit X
       sess       - List all active sessions before deciding

  ── 5a. PROXYING ───────────────────────────────────────────────────────

    Always connect to a proxy before hacking. This routes your traffic
    through intermediate machines so you aren't traced back.

      @proxy           - Quick shortcut: start a proxy chain (bash script)
      proxy -q         - Single-hop quick proxy (fastest to set up)
      proxy -a         - Full proxy chain from proxy.dat / Map.conf
      proxy -r 5       - Build a random 5-hop proxy chain
      proxy -h -c 3    - Build 3 quick-proxy hops

    If x crashes or you lose connection, run proxy -q again to instantly
    reconnect to your last saved proxy (requires config -y to be set).

  ── 5b. SCANNING ───────────────────────────────────────────────────────

    scan is the core attack command. It finds open ports, tests for
    vulnerabilities, and launches the post-exploitation menu.

    Basic targets:

      scan 1.2.3.4          - Scan a public IP
      scan example.com      - Scan by domain name
      scan -l               - Scan localhost
      scan -n               - Scan your local network interactively
      scan -r               - Pick a random target

    Targeted port/service attacks:

      scan -p 1.2.3.4 22    - Attack a specific port (e.g. SSH on 22)
      scan -p 1.2.3.4 http  - Attack by service name
      scan -pd /lib         - Scan a local library folder for exploits

    Smart scanning (uses your exploit database):

      scan --n apt c                - LAN scan using aptclient, computer objects
      scan --e shell                - Search all libraries for shell exploits
      scan --e computer -u root     - Search for root-level computer exploits
      scan --c 1.2.3.4 libssh.so c  - Direct connect with specific library
      scan --l libssh.so 2          - Local scan, specific library and index

    LAN IP direct scan (from inside a router):

      scan 192.168.1.5         - Scan a LAN device directly
      echo 192.168.1.5 | scan  - Pipe a LAN IP into scan

    Bounce scanning (pivot through a router to a LAN target):

      scan --s 192.168.1.5 http s   - Bounce scan: attack http on LAN IP

    Exploit result types:

      shell     - Full command-line access to the target
      computer  - File system access on the target
      file      - Access to a single specific file
      bounce    - Route through a router to reach another machine
      null      - May need a parameter, or is a password-change exploit

    After selecting an exploit you enter the post-exploitation menu
    where you can crack passwords, browse files, escalate privileges,
    install backdoors, and more.

  ── 5c. DIG (LAN RECON) ────────────────────────────────────────────────

    dig crawls the LAN behind a router and extracts sensitive data —
    emails, bank credentials, user accounts, and files — automatically.

    REQUIREMENTS:
      - You must be on a router (or pipe in a router IP)
      - You need a working LAN bounce exploit in your database

    Common operations:

      dig -a            - Scan all data types across the LAN
      dig -e            - Extract email credentials only
      dig -b            - Extract bank credentials only
      dig -r            - Extract rshell/remote access data
      dig -u            - Extract user account data
      dig -g            - Grab all data from every LAN device (users, emails, bank, files)

    Targeting specific LAN IPs:

      dig -a -i 192.168.1.5              - Scan one specific machine
      dig -a -i 192.168.1.5,192.168.1.9  - Scan multiple IPs

    Pipe a router's public IP into dig (no need to be on the router):

      echo 1.2.3.4 | dig --ip -a       - Full scan on router at 1.2.3.4
      echo 1.2.3.4 | dig --ip -e       - Email scan via router 1.2.3.4
      bc ip | dig --ip -a              - Scan a random router's LAN

    Saving and reviewing results:

      dig -a -s mydata      - Save results to mydata.txt
      dig cache             - List all saved result sets
      dig cache mydata      - View a saved result set
      dig cache clear       - Clear all saved data

    Escalate to root first (installs bounce lib if needed):

      dig -a --root         - Root the router first, then scan LAN
      echo 1.2.3.4 | dig --ip -a --root

    Scan range control:

      dig -a --extreme 255  - Scan all 255 addresses per subnet (thorough)
      dig -a --extreme 10   - Fast scan, first 10 addresses only

  ── 5c(ii). RECON  (dig's little brother) ──────────────────────────────

    recon targets a single public IP directly. No router access required —
    but the router at that IP needs a public bounce exploit available for
    recon to reach the LAN machines behind it. If no bounce is found it
    falls back to direct exploits on the target.

      recon 1.2.3.4              - Full recon on a target IP
      recon -a 1.2.3.4           - Also attempt to crack the admin email
      recon -r 1.2.3.4           - Email-focused recon only
      recon -g 1.2.3.4           - Grab all text files from the target
      recon --subjects 1.2.3.4   - Also fetch email subject lines
      recon --save 1.2.3.4       - Save results to reconData.txt
      recon --extreme 1.2.3.4    - Expand LAN address range (0-255)
      recon --file ips.txt       - Batch recon from a file of IPs

    Use recon when you have a public IP and want to pull data without
    being on the router yourself. Use dig when you want to sweep an
    entire LAN and have shell access on the router (or can pipe one in).

  ── 5d. PIPING ─────────────────────────────────────────────────────────

    X supports Unix-style pipes. Chain commands with | to pass output
    from one command as input to the next.

    Basic examples:

      cat /etc/passwd | grep root
      ls | grep ".txt"
      scan -l | grep shell
      nmap 1.2.3.4 | cut -f 1

    Text processing:

      cat file.txt | grep "pattern"        - Search for lines
      cat file.txt | sed "old/new"         - Find and replace
      cat file.txt | awk '{print $2}'      - Extract a field
      cat file.txt | sort | uniq           - Sort and deduplicate
      cat file.txt | wc -l                 - Count lines
      cat file.txt | head -5               - First 5 lines
      cat file.txt | tail -5               - Last 5 lines
      cat file.txt | cut -d ":" -f 1       - Cut by delimiter

    Variables (store and reuse pipe data):

      echo "hello world" | set MSG         - Store in $MSG
      echo "$MSG"                          - Print it back
      cat /etc/passwd | wc -l | set COUNT
      echo "Total users: $COUNT"

    Building command lines from input:

      find -n *.log | xargs | main -d      - Download all .log files
      echo "1.2.3.4" | scan                - Pipe IP into scan
      bc ip | dig --ip -a                  - Pipe random IP into dig

    Redirection (write pipe output to a file):

      cat file.txt | grep root > output.txt    - Write to file
      ls | grep .src >> list.txt               - Append to file


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  6. HELP SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Almost every command has a built-in man page. When in doubt, check it.

    man <command>     - View the manual page for any command
    man scan          - Scan documentation and all flags
    man dig           - Dig recon framework documentation
    man proxy         - Proxy chain documentation
    man exp           - Exploit database management
    man pacman        - Package manager documentation
    man dict          - Password cracking documentation
    man ai            - AI assistant documentation
    man bash          - Bash scripting engine documentation
    man pipe          - Pipe and text processing reference

  At the X prompt:

    ?                 - Quick overview of all available commands


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7. Q & A
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Q: My exploit database is empty. Where do I start?
  A: Run "pacman -Sr" to find and add a random hack shop repository,
     then run "pacman -Sy -e -c 10" to populate it. After that run
     "exp all" to generate usable exploits from the results.

  Q: scan/dig says I have no bounce exploit. How do I get one?
  A: Run "exp bounce" after a database sync. If that finds nothing,
     try "exp router" too — router exploits include bounces. You can
     also use "dig -a --root" which installs a bounce lib automatically.

  Q: I keep getting traced. What am I doing wrong?
  A: You're probably not using a proxy. Always run "proxy -q" (or
     "@proxy") before starting any scan or exploit. More hops = safer.

  Q: proxy -q crashed and I lost my chain. How do I reconnect fast?
  A: If you ran "config -y" during setup, just run "proxy -q" again —
     it reloads your last saved proxy file automatically.

  Q: scan found a vulnerability but says the exploit failed.
  A: Your exploit version may be outdated. Run "pacman -Sy -e --force" to
     force-rescan every library encountered, then "exp all" to rebuild. You can also
     try "exp grind -r" to search for a new remote version of a specific library.

  Q: dig says "must be executed from a router". What does that mean?
  A: dig requires you to have shell access on a router. Either scan into
     one first, or pipe its public IP in: "echo 1.2.3.4 | dig --ip -a".

  Q: Where do I get metaxploit.so / crypto.so?
  A: Run "pacman -Si -b" to install both. If you don't have a repo set
     up yet, run "pacman -Sr" first to add one automatically.

  Q: How do I back up my exploit database?
  A: Run "exp backup". Do this regularly — especially before running
     any force-rescan that could wipe your existing entries.

  Q: What is the proper way to quit X?
  A: If you have any active sessions (shells, proxies, pivots, rshells),
     use "sess -x" to quit. This triggers clean-up for every open session
     before exiting. Just closing the terminal skips this and can leave
     orphaned processes or corrupt session state next time you start.
     Use "sess -l" to see what sessions are open before you close.

  Q: Something seems broken after an update. What should I try first?
  A: Run "sys check" — it auto-detects and reinstalls missing libraries.
     If that doesn't help, check "man <command>" for the broken command.

  Q: I want to automate a workflow. Can I script in X?
  A: Yes — X includes a full bash scripting engine. See "man run" for
     syntax, or browse the scripts in ~/payload/data/bash/ for examples.

  Q: Can I extend X with my own commands and logic?
  A: Absolutely. The bash engine lets you write your own tools that run
     inside X just like any built-in command. You can use all of X's
     commands, pipe output between them, store variables, loop over
     results, and call exploits — essentially adding new commands on top
     of the framework. Drop your scripts into ~/payload/bash/ and run
     them by name. See "man run" for the full syntax reference.


Stay safe, happy hacking o7


USEFUL COMMANDS FOR NEW PLAYERS

    exp backup    - Backup your exploit database (do this regularly!)
    scan <ip>     - Scan a target for open ports and services
    hunt          - Find targets automatically
    proxy         - Connect through a proxy (@proxy to stay safe)


SESSIONS

  After exploiting a target you can optionally save the object as a session
  with sess -a if you want to come back to it later. Manage saved sessions
  with sess:

    sess -a           - Save current object as a session
    sess -l           - List all active sessions
    sess -u 1         - Switch to session 1
    sess -n 1 Name    - Give a session a nickname
    sess -g Name      - Jump to a session by nickname
    sess back         - Return to the previous session
    sess -x           - Close all sessions (clean up when you're done)

  No matter how deep you are - inside a shell, computer, or file -
  you can always type "home" to return to your top level session.