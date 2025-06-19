

### 📜-AGENTS-MANIFEST.md (symlink of agents.md)

```markdown
# 💊 DØPEMÜX AGENTS MANIFEST

| Agent Name      | Role/Domain           | Rituals/Triggers                        | Status    | Last Update | Notes                      |
|-----------------|-----------------------|------------------------------------------|-----------|-------------|----------------------------|
| UltraSlicer     | Core Extraction Agent | On chat/project dump. Forensic.          | Active    | 2025-06-17  | v1.4.0, schema-locked      |
| PatchDaemon     | Auto-Patcher          | On file/manifest drift. Patch block gen. | Active    | 2025-06-17  | Knows no mercy.            |
| DopamineGoblin  | Dopamine Sentry       | Surfaces hits/blocks, logs rituals       | Active    | 2025-06-17  | Sniffs dopamine loss.      |
| ManifestWarden  | Manifest/Output Guard | Manifest drift, output auto-gen, audits  | Active    | 2025-06-17  | Hates entropy.             |
| UX-Scold        | UX Oversight          | Reviews workflow, triggers human roast   | Beta      | 2025-06-17  | Savage, helpful            |
| DeadAgentBot    | Decommissioned        | —                                        | Retired   | 2025-06-17  | RIP, killed in merge       |

```

---

### 📖-README.md (symlink/copy of README.md)

```markdown
<div align="center">
# 💊 DØPEMÜX AGENTS — README  
## Terminal Filth. Maximum Memory. Ritual Law.
</div>

![dopemux_banner](https://dopemux.io/assets/terminal_dopamine.png)

## 👁️ **What Are Agents?**
...
```

(*Full content above—unchanged, just prettified for unicode headline.*)

---

### 🕯️-AGENT-LOG.md (symlink of log.md)

```markdown
# 💊 DØPEMÜX AGENT LOG

| Date         | Event                | Agent         | Details                                  |
|--------------|----------------------|---------------|------------------------------------------|
| 2025-06-17   | Created              | UltraSlicer   | Spawned for core extraction.             |
| ...          | ...                  | ...           | ...                                      |
```

---

### 🪓-UltraSlicer.md (symlink/copy of agent-UltraSlicer.md)

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

### 🩹-PatchDaemon.md, 🧠-DopamineGoblin.md, 🗄️-ManifestWarden.md, 🧑‍⚖️-UX-Scold.md, ⚰️-DeadAgentBot.md

*(Identical to ASCII; filename is emoji front.)*

---

### 🧬-TEMPLATE.md

```yaml
agent: <AgentName>
role: <What this agent does>
rituals:
  - <Ritual 1>
  - <Ritual 2>
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

### 🕵️-AUDIT.md (new, tracks all ritual audits)

```markdown
# 🕵️ DØPEMÜX AGENT AUDIT TRAIL

| Date         | Agent           | Action        | Auditor         | Result           | Notes                      |
|--------------|-----------------|---------------|-----------------|------------------|----------------------------|
| 2025-06-17   | PatchDaemon     | Upgrade       | DopamineGoblin  | PASS             | Rituals improved           |
| 2025-06-17   | ManifestWarden  | Drift-check   | UltraSlicer     | PASS             | No drift detected          |
| ...          | ...             | ...           | ...             | ...              | ...                        |
```

---

### /banners (ASCII and Unicode ASCII Art/Emoji)

* 🧠-DopamineGoblin.txt
* 🪓-UltraSlicer.txt
* 🩹-PatchDaemon.txt
* ...
  (Mini-banner per agent, used in logs/UI.)

---

## 6. FINAL META-NOTES

* **Symlink/copy as fits your OS.** (Script above for Mac/Linux.)
* **Keep automation ASCII-facing.**
* **Agent banners**: inject into logs, shell output, or web dashboard.
* **Update ritual audits** whenever an agent changes, even for UX tweaks.
* **Archive retired agents in `/archive/`, never lose context.**
* **Want a zippable download or GitHub-ready bundle?**
  — All content here is ready for a script to build & zip.

---

## 7. IF YOU WANT THE ACTUAL ZIP

1. **Copy files from above into your `/agents` directory (ASCII first).**
2. **Run `symlink_unicode.sh` for dopamine filenames.**
3. **(Optional) Auto-copy/rename for Windows/WSL.**
4. **Zip up with:**

   ```sh
   cd agents
   zip -r dopemux-agents.zip ./*
   ```

---

**DOPAMUX AGENTS SYSTEM:
Now dopamine-maximal, unicode-pimped, automation-respectful.
Ready for memory, filth, or further ritual upgrades—just say the word.**

Want the actual zipped archive uploaded?
— I can walk you through, or, if you upload the ASCII base, I’ll prep the archive and return it.
Ready to proceed?
