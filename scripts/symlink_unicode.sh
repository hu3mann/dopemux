#!/bin/bash
# Dopemux: Symlink (or copy if on non-symlink OS) unicode dopamine files

files=(
  "agents.md:📜-AGENTS-MANIFEST.md"
  "README.md:📖-README.md"
  "log.md:🕯️-AGENT-LOG.md"
  "agent-UltraSlicer.md:🪓-UltraSlicer.md"
  "agent-PatchDaemon.md:🩹-PatchDaemon.md"
  "agent-DopamineGoblin.md:🧠-DopamineGoblin.md"
  "agent-ManifestWarden.md:🗄️-ManifestWarden.md"
  "agent-UX-Scold.md:🧑‍⚖️-UX-Scold.md"
  "agent-DeadAgentBot.md:⚰️-DeadAgentBot.md"
  "agent-TEMPLATE.md:🧬-TEMPLATE.md"
  "audit.md:🕵️-AUDIT.md"
)

for f in "${files[@]}"; do
  src=$(echo $f | cut -d: -f1)
  dst=$(echo $f | cut -d: -f2)
  if [ -e "$src" ]; then
    ln -sf "$src" "$dst"
  fi
done