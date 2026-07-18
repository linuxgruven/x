# Uncalled Functions

> Generated: 2026-02-26  
> Scanned: 762 `.src` files — 35,417,328 chars — 2,028 function definitions  
> Script: `/tmp/find_uncalled.py`  
> Method: word-boundary frequency count; a function is flagged when its identifier appears nowhere in the codebase except its own definition line.

**Total uncalled: 21**  
> 41 previously-listed functions were removed from production source files on 2026-02-27 and archived in `testing/unused.src`.

---

## testing/ (expected dead code — prototype/experimental files)

### testing/unused.src *(archived dead code — safe to delete)*

| Function |
|----------|
| `AgentCommandKnowledge.matchKeywords` |
| `AgentCommandKnowledge.matchSemanticFlags` |
| `AgentCommandRegistry.matchSemanticFlags` |
| `AgentCore.getConfig` |
| `AgentHandlers._getLastFile` |
| `AgentHandlers.saveLearnedState` |
| `AgentHandlers.loadLearnedState` |
| `AgentHandlers.askClarification` |
| `AgentHandlers.respondToClarification` |
| `AgentHandlers.clearTelemetry` |
| `AgentLearning._matchTemplate` |
| `AgentPlanning._selectBestExploit` |
| `AgentPlanning._buildNavigationPlan` |
| `Knowledge.prune` |
| `AI.predict` |
| `AI.recommend` |
| `AI.listModels` |
| `AI.saveModel` |
| `AI.loadModel` |
| `AI.getHistory` |
| `Builder.launchAppEX` |
| `Crack.getFile_` |
| `Crack.iterPasswords` |
| `Disk.findBySize` |
| `Disk.findByName` |
| `Disk.getLargestFiles` |
| `Disk.getDirectorySize` |
| `Email.getAccounts` |
| `Email.getAccounts2` |
| `Exploit.unpackExploit` |
| `Io.fileFilter` |
| `Man.getCommandHelp` |
| `Man.browseLocalFiles` |
| `LibServer.targetLib` |
| `LibServer.lockLibs` |
| `LibServer.unlockLibs` |
| `Config.clearVulnerable` |
| `Pipe._expandGlob` |
| `Pipe._globMatch` |
| `Pipe._handleRedirect` |
| `Pipe._stripQuotes` |

### testing/0day.src
| Line | Function |
|------|----------|
| 514 | `zday.on_load` |

### testing/battle_ship_server_multi.src
| Line | Function |
|------|----------|
| 88 | `BattleServerMulti.findGameById` |

### testing/byte.src
| Line | Function |
|------|----------|
| 14 | `ByteBuffer.WriteShort` |
| 19 | `ByteBuffer.WriteInt` |
| 26 | `ByteBuffer.WriteString` |
| 46 | `ByteBuffer.ReadShort` |
| 52 | `ByteBuffer.ReadInt` |
| 60 | `ByteBuffer.ReadString` |
| 81 | `ByteBuffer.FromString` |

### testing/progressbar.src
| Line | Function |
|------|----------|
| 42 | `loopProgressBar` |

### testing/ref.src
| Line | Function |
|------|----------|
| 54 | `MyClass` |

### testing/shake.src
| Line | Function |
|------|----------|
| 26 | `uint64.shiftr` |

### testing/torrent_client.src
| Line | Function |
|------|----------|
| 141 | `downloadPiece` |
| 203 | `assembleFile` |

### testing/weapons.src
| Line | Function |
|------|----------|
| 601 | `Game.generateParty` |

### testing/xdata.src
| Line | Function |
|------|----------|
| 44 | `XDataValue.toRaw` |
| 90 | `XDataTable.addColumn` |
| 93 | `XDataTable.getColumn` |
| 1152 | `XData.listPlugins` |
| 1299 | `XData.createRecord` |
| 1306 | `XData.fromCSV` |

---

## Notable Clusters

| Cluster | Count | Notes |
|---------|-------|-------|
| `testing/unused.src` | 41 | Archived dead code — moved from production on 2026-02-27 |
| `testing/*` (other) | 21 | Prototype files — expected |
