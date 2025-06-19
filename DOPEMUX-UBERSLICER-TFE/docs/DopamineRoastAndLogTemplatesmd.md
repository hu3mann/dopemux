💊 **DØPEMÜX ULTRASLICER — DOPAMINE/ROAST LOGGING TEMPLATE**
*(Drop-in for devlog\_writer.py, CLI, or as a logging utility for all phases. Filthy, focused, and ready to humiliate LLM drift.)*

---

### **1. Dopemux Dopamine Log Function**

```python
import datetime

def dopamine_log(event, block_id=None, level=5, tags=None, roast=None, devlog_path="TFE-DEVLOG.txt"):
    """
    Logs a dopamine hit, error, or roast to the Dopemux devlog.

    event: str        — Main event description.
    block_id: str     — Block ID (if available).
    level: int        — Dopamine level (1–10).
    tags: list        — Any ritual/meta tags (e.g., ['api', 'hallucination']).
    roast: str        — Optional roast/filthy comment.
    devlog_path: str  — Where to append log.
    """
    now = datetime.datetime.utcnow().isoformat()
    tags_str = ", ".join(tags) if tags else ""
    block_str = f"[{block_id}]" if block_id else ""
    line = (
        f"💊 [{now}] {block_str} "
        f"(Dopamine: {level}/10) {event} "
        f"{f'| Tags: {tags_str}' if tags else ''} "
        f"{f'→ {roast}' if roast else ''}\n"
    )
    with open(devlog_path, "a") as f:
        f.write(line)
```

---

### **2. Dopamine Hit Example**

```python
dopamine_log(
    event="Block processed successfully.",
    block_id="block-8ff1",
    level=8,
    tags=["api", "extraction", "phase1"],
    roast="Felt better than coffee and three Adderalls."
)
```

**Result:**

```
💊 [2025-06-19T10:20:01.219Z] [block-8ff1] (Dopamine: 8/10) Block processed successfully. | Tags: api, extraction, phase1 → Felt better than coffee and three Adderalls.
```

---

### **3. Hallucination/Drift Example**

```python
dopamine_log(
    event="Schema drift detected — hallucination risk.",
    block_id="block-0020",
    level=3,
    tags=["api", "hallucination", "filth"],
    roast="Block output was as coherent as a 3am doomscroll. Fix your context, LLM."
)
```

**Result:**

```
💊 [2025-06-19T10:20:55.721Z] [block-0020] (Dopamine: 3/10) Schema drift detected — hallucination risk. | Tags: api, hallucination, filth → Block output was as coherent as a 3am doomscroll. Fix your context, LLM.
```

---

### **4. Filthy, Roast-Heavy Logging Ideas**

* `"Block validated. Dopamine at max. Proceed to next chunk, you filthy animal."`
* `"LLM drift detected. Logging as #filth. Someone’s getting roasted in the review."`
* `"Manifest updated. If you broke anything, I'll find you."`
* `"API call failed harder than my last Tinder date. Retrying..."`

---

### **5. Usage: Where to Call**

* After every **block processed** (success, error, drift, or hallucination)
* On **manifest/metafile updates**
* When **API or Langchain failures** occur
* On **creative overrides or ritual events**
* For **dopamine surges** (big wins, completed runs, or finished pipelines)

---

### **6. BONUS: Dopamine Banner for Terminal/CLI**

```python
def dopamine_banner(event, level=7):
    banners = [
        "☠️ ULTRASLICER — MAX CONTEXT EXTRACT",
        "💊 DØPEMÜX TERMINAL INITIATED",
        "🧠 SCHEMA LOCKED. DOPAMINE FLOWING.",
        "🔥 ALL BLOCKS PROCESSED. FILES UNTOUCHED BY DRIFT.",
    ]
    print("\n" + ("="*50))
    print(f"💊 DOPAMINE HIT [{level}/10]: {event}")
    print(banners[level % len(banners)])
    print(("="*50) + "\n")
```

---

## **Drop-in Ready.**

Use anywhere that needs dopamine, humiliation, or a system status banner.
Want to wire this to the devlog auto-patcher or manifest hooks? Say the word.
