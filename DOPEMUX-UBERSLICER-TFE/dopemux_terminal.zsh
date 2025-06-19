#!/bin/zsh

print -P "%F{6}💊 DØPEMÜX ULTRASLICER v1.4.0 — Terminal Dopamine Ritual%f"
print -P "%F{4}Type 'help' for all commands. Rituals logged to devlog/audit.%f"

while true; do
  print -n "%F{2}$ %f"
  read cmd
  if [[ "$cmd" == "exit" ]]; then break; fi
  if [[ "$cmd" == "help" ]]; then
    print -P "%F{3}Commands:%f\n  extract <file> <outdir>\n  audit <file>\n  dopamine_hit\n  exit"
  elif [[ "$cmd" == extract* ]]; then
    PYTHONPATH=src python3 -m dopemux_ultraslicer ${(z)cmd}[2] ${(z)cmd}[3]
  elif [[ "$cmd" == audit* ]]; then
    PYTHONPATH=src python3 -c "from dopemux_ultraslicer.dopemux_utils import log_audit; log_audit('manual','Manual audit triggered')"
    print "[OK] Manual audit block added."
  elif [[ "$cmd" == dopamine_hit* ]]; then
    PYTHONPATH=src python3 -c "from dopemux_ultraslicer.dopemux_utils import log_dev; log_dev('dopamine_hit',['Manual dopamine hit'])"
    print "[OK] Dopamine hit ritual complete."
  else
    print "[ERROR] Unknown command. Type 'help'."
  fi
done
