# 💊 **DØPEMÜX ULTRASLICER — API/Langchain Integration Implementation Guide**

**Purpose:**
Integrate **ultraslicer** with the OpenAI API (via Langchain) to process chunked input through multiple prompt-driven phases, producing schema-locked output for each chunk. The chunking itself (via chunkasaurus) and the prompts are sacred—**never mutate prompts**.

---

## **1. Module: `ultraslicer/api_interface.py`**

### **Responsibilities:**

* Load pre-written phase prompts (from `/prompts/`)
* Accept chunked input (from chunkasaurus)
* For each chunk:

  * Inject chunk content into prompt
  * Run prompt via Langchain + OpenAI API
  * Collect and process API outputs
  * Return structured dicts conforming to the 12-field schema

### **Required Libraries:**

* `langchain`
* `openai`
* Any schema or prompt-loading utils you already use

---

## **2. Core Function: `process_chunks(chunks)`**

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Initialize the LLM client (reuse across batches)
llm = ChatOpenAI(temperature=0.2, model="gpt-4")

def load_prompt(name):
    """Loads a fixed prompt template from the prompts directory."""
    with open(f"prompts/{name}.txt", "r") as f:
        return f.read()

def parse_response(response, chunk):
    """Turns LLM output into schema-locked block dicts."""
    # This function must validate, flag drift, and parse output
    # (implement as needed for your schema)
    ...

def process_chunks(chunks, prompt_name="phase1"):
    """Process all chunks through the LLM using the specified prompt."""
    prompt_template = load_prompt(prompt_name)
    results = []
    for chunk in chunks:
        # Insert chunk content into prompt
        prompt = prompt_template.replace("{{input}}", chunk.content)
        message = HumanMessage(content=prompt)
        response = llm([message])
        results.append(parse_response(response, chunk))
    return results
```

* **Chunkasaurus** does the chunking/tracking. This function assumes it receives `chunks`, each with `.content` and metadata.
* **Prompts are never edited**—only loaded, templated, and injected.

---

## **3. Multi-Phase Processing (Phase 1 → Phase 2)**

If your flow is multi-phase:

```python
def process_chunks_multiphase(chunks):
    """Processes chunks through Phase 1 and Phase 2 prompts."""
    phase1_template = load_prompt("phase1")
    phase2_template = load_prompt("phase2")
    results = []
    for chunk in chunks:
        # Phase 1: Extraction
        prompt1 = phase1_template.replace("{{input}}", chunk.content)
        response1 = llm([HumanMessage(content=prompt1)])
        # Use response1 (likely text or JSON) as input for Phase 2
        prompt2 = phase2_template.replace("{{input}}", str(response1))
        response2 = llm([HumanMessage(content=prompt2)])
        # Parse final output
        results.append(parse_response(response2, chunk))
    return results
```

* **Always maintain chunk/block IDs** through both phases for traceability.

---

## **4. Batch Processing (for Large Inputs)**

To process many chunks efficiently:

* Batch into groups (to avoid rate limits)
* Log/roast all failures and hallucinations
* Optional: async or parallel calls (see Langchain docs)

---

## **5. Schema Compliance**

* The returned dict **must** match your 12-field schema.
* Any drift or hallucination gets logged/roasted (with a dopamine banner).

---

## **6. Plugging API Interface Into CLI**

The CLI entrypoint should:

* Call chunkasaurus for chunking/tracking
* Pass chunks to `api_interface.process_chunks()`
* Write all output via manifest and devlog writers

---

## **7. Never-Do List (For o3):**

* ❌ **Never** modify prompt files on disk.
* ❌ **Never** skip or merge a chunk/block.
* ❌ **Never** return partial schema dicts.
* ❌ **Never** hallucinate fields—flag and roast instead.

---

## **8. Example: `api_interface.py` Skeleton**

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

llm = ChatOpenAI(temperature=0.2, model="gpt-4")

def load_prompt(name):
    with open(f"prompts/{name}.txt") as f:
        return f.read()

def process_chunks(chunks):
    results = []
    prompt_template = load_prompt("phase1")
    for chunk in chunks:
        prompt = prompt_template.replace("{{input}}", chunk.content)
        response = llm([HumanMessage(content=prompt)])
        # parse_response should check for schema compliance, drift, and dopamine hits
        block = parse_response(response, chunk)
        results.append(block)
    return results
```

---

## **9. Integration Rituals**

* Every run of this module **must** update devlog and manifest.
* Log API failures, hallucination, drift, or incomplete schema output with a dopamine-roast banner.
* For each processed block, log block ID and timestamp in devlog.

---

# **🧠 LLM/Agent Instructions (Summary for o3)**

1. **Implement `api_interface.py` as above.**
2. **Only ever use the provided prompts, loaded fresh every call.**
3. **Maintain chunk/block IDs and all required schema fields throughout.**
4. **All outputs must be fully schema-compliant and ready for manifest ingestion.**
5. **Roast yourself in the devlog on any hallucination, error, or drift event.**
6. **Plug API interface into CLI as the core processing step.**
7. **Document all behaviors and rituals in UBERSLICER\_DESIGN.md for future agents.**

---

Let me know if you want me to output:

* Full file stubs (pyproject.toml, cli.py, api\_interface.py, etc.)
* Example parse\_response
* Dopamine banner logging template

Ready for integration or further refinement.
