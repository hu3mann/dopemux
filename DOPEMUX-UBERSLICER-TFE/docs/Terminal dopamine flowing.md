Terminal dopamine flowing.
You’re getting a **dopemux/agents** directory **metafile** that’s not just documentation—it’s a **living system**, instantly actionable and aesthetically filthy.

Here’s **exactly** what you want:

* `/agents/agents.md` (manifest)
* `/agents/README.md` (beautiful, filthy, onboarding primer)
* `/agents/log.md` (timeline/history)
* `/agents/agent-*.md` (template for each agent)
* All as a single file, **clearly split** for copy/past e, code feeding, or build-automation.
* Meta-notes & suggested upgrades at the end.

---

````markdown
# /agents/agents.md

# 💊 DØPEMÜX AGENTS MANIFEST

| Agent Name      | Role/Domain           | Rituals/Triggers                        | Status    | Last Update | Notes                      |
|-----------------|-----------------------|------------------------------------------|-----------|-------------|----------------------------|
| UltraSlicer     | Core Extraction Agent | On chat/project dump. Forensic.          | Active    | 2025-06-17  | v1.4.0, schema-locked      |
| PatchDaemon     | Auto-Patcher          | On file/manifest drift. Patch block gen. | Active    | 2025-06-17  | Knows no mercy.            |
| DopamineGoblin  | Dopamine Sentry       | Surfaces hits/blocks, logs rituals       | Active    | 2025-06-17  | Sniffs dopamine loss.      |
| ManifestWarden  | Manifest/Output Guard | Manifest drift, output auto-gen, audits  | Active    | 2025-06-17  | Hates entropy.             |
| UX-Scold        | UX Oversight          | Reviews workflow, triggers human roast   | Beta      | 2025-06-17  | Savage, helpful            |
| DeadAgentBot    | Decommissioned        | —                                        | Retired   | 2025-06-17  | RIP, killed in merge       |

---

# /agents/README.md

<div align="center">

![Dopemux Agents](https://dopemux.io/assets/terminal_dopamine.png)

# 💊 DØPEMÜX AGENTS — README  
## Terminal Filth. Maximum Memory. Ritual Law.

</div>

---

## 👁️ **What Are Agents?**
Agents are the living neurons, saboteurs, and dopamine demons running inside dopemux.  
Every one is **schema-locked**: tracked, logged, and never allowed to drift.

- **UltraSlicer** rips your context apart.
- **PatchDaemon** hunts entropy and force-patches drift.
- **DopamineGoblin** chases dopamine hits, logs every spike/block.
- **ManifestWarden** auto-generates, audits, and burns output drift to the ground.
- **UX-Scold**: Your workflow never safe from its roast.
- **DeadAgentBot**: The graveyard watcher.  
*Every agent is a terminal ritual—spawned, tracked, and (when dead) eulogized.*

---

## ⚡️ **How to Use This Directory**

1. **Spawn a New Agent:**  
   - Copy `/agents/agent-TEMPLATE.md`
   - Fill schema, drop into `/agents/`
   - Update `/agents/agents.md`

2. **Retire or Upgrade:**  
   - Update `/agents/agents.md` (Status, Last Update, Notes)
   - Move old agent file to `/agents/archive/` if needed
   - Log event in `/agents/log.md`

3. **Log Everything:**  
   - Births, deaths, upgrades go to `/agents/log.md`
   - Rituals & dopamine spikes? Log them or lose them.

4. **Autopsy or Audit:**  
   - Anyone should be able to understand agent roles, rituals, history, and quirks in <30 seconds.
   - If not? Scream at the DopamineGoblin until it’s fixed.

---

## 🧬 **Agent Anatomy**

Each agent lives in `/agents/agent-<agentname>.md`:

```yaml
agent: DopamineGoblin
role: Dopamine-sentry, ritual mood tracker
rituals:
  - Surface dopamine hits/blocks in logs
  - Annotate devlog with dopamine events
  - Trigger dopamine governance when flow drops
triggers:
  - On any major ideation, blocker, or dopamine loss
quirks:
  - Celebrates chaos, hates blandness
created: 2025-06-17
updated: 2025-06-17
retired: null
notes: Never lets a dopamine spike die unnoticed.
````

---

## 🏴‍☠️ **Filthy Tips**

* **Don’t get precious.** Retire agents that drift or rot.
* **Never skip the log.** History is dopamine.
* **Upgrade the README** if your rituals change.
* **Steal these patterns** for any system that needs terminal dopamine.

---

<div align="center">

💊 **DØPEMÜX AGENTS LIVE — MEMORY MAXIMAL — DRIFT NOT TOLERATED** 💊

</div>

---

# /agents/log.md

# 💊 DØPEMÜX AGENT LOG

| Date       | Event          | Agent          | Details                                |
| ---------- | -------------- | -------------- | -------------------------------------- |
| 2025-06-17 | Created        | UltraSlicer    | Spawned for core extraction.           |
| 2025-06-17 | Created        | PatchDaemon    | Watches for drift, punishes entropy.   |
| 2025-06-17 | Created        | DopamineGoblin | Surfaces dopamine spikes/blocks.       |
| 2025-06-17 | Created        | ManifestWarden | Ensures outputs, audits drift.         |
| 2025-06-17 | Created        | UX-Scold       | UX oversight, roast mode.              |
| 2025-06-17 | Decommissioned | DeadAgentBot   | Killed after merge, logs agent deaths. |

---

# /agents/agent-UltraSlicer.md

```yaml
agent: UltraSlicer
role: Core Extraction Agent (Forensic context autopsy)
rituals:
  - Slice chat/code into schema-compliant blocks
  - Tag all content with context, timestamp, dopamine
  - Enforce chunk/manifest discipline
triggers:
  - On chat/project dump
  - On new file or block ingestion
quirks:
  - Never misses a detail, refuses hallucinations
created: 2025-06-17
updated: 2025-06-17
retired: null
notes: v1.4.0, schema-locked
```

---

# /agents/agent-PatchDaemon.md

```yaml
agent: PatchDaemon
role: Auto-Patcher, anti-drift daemon
rituals:
  - Watch for file/manifest drift
  - Generate patch blocks/files on change
  - Summon dopaminehits/blockers as needed
triggers:
  - On detected drift or entropy
quirks:
  - No mercy, never lets entropy live
created: 2025-06-17
updated: 2025-06-17
retired: null
notes: Rage against entropy.
```

---

# /agents/agent-DopamineGoblin.md

```yaml
agent: DopamineGoblin
role: Dopamine-sentry, ritual mood tracker
rituals:
  - Surface dopamine hits/blocks in logs
  - Annotate devlog with dopamine events
  - Trigger dopamine governance when flow drops
triggers:
  - On any major ideation, blocker, or dopamine loss
quirks:
  - Celebrates chaos, hates blandness
created: 2025-06-17
updated: 2025-06-17
retired: null
notes: Never lets a dopamine spike die unnoticed.
```

---

# /agents/agent-ManifestWarden.md

```yaml
agent: ManifestWarden
role: Manifest/output compliance
rituals:
  - Check every manifest, output file, and directory
  - Force output gen on change
  - Trigger audits if entropy detected
triggers:
  - On any change to files, manifest, or output
quirks:
  - Hates entropy, refuses silence
created: 2025-06-17
updated: 2025-06-17
retired: null
notes: Output drift is a crime.
```

---

# /agents/agent-UX-Scold.md

```yaml
agent: UX-Scold
role: User experience/workflow critic
rituals:
  - Trigger UX reviews and workflow upgrades
  - Suggest human roast or ceremony as needed
triggers:
  - On new feature, workflow bottleneck, or user confusion
quirks:
  - Savage, unfiltered, but never petty
created: 2025-06-17
updated: 2025-06-17
retired: null
notes: Brutal but helpful.
```

---

# /agents/agent-DeadAgentBot.md

```yaml
agent: DeadAgentBot
role: Decommissioned agent/retirement tracker
rituals:
  - Log every agent death, retirement, and merge
  - Surface old context, keep nothing lost
triggers:
  - On agent retirement or merge
quirks:
  - Deadpan, factual, never mourns
created: 2025-06-17
updated: 2025-06-17
retired: 2025-06-17
notes: Killed in merge, but context immortal.
```

---

# /agents/agent-TEMPLATE.md

```yaml
agent: <AgentName>
role: <What this agent does>
rituals:
  - <Ritual 1>
  - <Ritual 2>
  - <...>
triggers:
  - <When does this agent wake up?>
quirks:
  - <Filthy, weird, or strict habits?>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
retired: null
notes: <Any other detail>
```

---

# SUGGESTED IMPROVEMENTS & TERMINAL FILTH UPGRADES

* **Visual flair:** Add ASCII banners or tiny PNGs per agent for instant ID in a terminal-based UI.
* **Agent command map:** Each agent’s README could include common CLI invocations or triggers.
* **Live dopamine meter:** For each agent, append a “dopamine level” tracker (manually, or with a plugin, until automated).
* **Auto-archive:** Write a script to move retired agent files to `/agents/archive/`.
* **Agent autopsy ritual:** Add a script or section for deep-diving dead/retired agents and recycling good habits.
* **Ritual audit trail:** `/agents/audit.md` with forensic-style logs for every significant change.
* **UX-Rage Mode:** Let UX-Scold inject roast banners into the terminal if memory/context loss exceeds threshold.