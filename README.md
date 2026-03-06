# Mini Coding Agent For Future Self-Improving System

A lightweight agent framework designed as a stepping stone toward self-improving AI. Start simple — an agent loop with tools — then grow into persistent memory, self-reflection, and autonomous learning.

Built with Google Gemini and the tool-use agent loop pattern.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   main.py                       │
│                                                 │
│  User Prompt                                    │
│       │                                         │
│       ▼                                         │
│  ┌─────────── Agent Loop (max 20 iters) ──────┐ │
│  │                                             │ │
│  │  message[] ──► Gemini API ──► response      │ │
│  │                                  │          │ │
│  │                    ┌─────────────┤          │ │
│  │                    │             │          │ │
│  │              has tool calls?   no tool calls │ │
│  │                    │             │          │ │
│  │                    ▼             ▼          │ │
│  │            call_function()   print text     │ │
│  │                    │           break        │ │
│  │                    ▼                        │ │
│  │           append tool result                │ │
│  │           to message[]                      │ │
│  │                    │                        │ │
│  │                    └──── next iteration     │ │
│  └─────────────────────────────────────────────┘ │
│                                                 │
│  call_function.py ──► functions/                │
│                        ├── get_files_info.py    │
│                        ├── get_file_content.py  │
│                        ├── write_file.py        │
│                        └── run_python_file.py   │
└─────────────────────────────────────────────────┘
```

## Agent Loop

1. User prompt is wrapped into `message[]` (conversation history)
2. `message[]` is sent to Gemini API with tool schemas
3. If Gemini responds with **tool calls** → execute via `call_function()`, append results to `message[]`, loop
4. If Gemini responds with **plain text** → print it, `break`
5. Safety cap: max 20 iterations

The key: `message[]` accumulates the full conversation (user prompt + LLM responses + tool results), so each iteration the model sees everything that happened before.

## Tools

All tools are sandboxed to `working_directory` ("calculator/"). Path traversal outside it is rejected.

| Tool | What it does |
|------|-------------|
| `get_files_info` | Lists files in a directory with size and type (file vs dir) |
| `get_file_content` | Reads file content as string, truncated at 10,000 chars |
| `write_file` | Creates or overwrites a file, auto-creates parent dirs |
| `run_python_file` | Runs a `.py` file via `python3`, returns stdout/stderr (30s timeout) |

## Usage

```bash
python main.py "your prompt here"
python main.py "your prompt here" --verbose
```

## Project Structure

```
Agent/
├── main.py              # Entry point + agent loop
├── call_function.py     # Tool dispatcher
├── config.py            # Constants (MAX_CHARS)
├── functions/
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
└── calculator/          # Sandboxed working directory
```

---

## Roadmap: Self-Evolving Memory System

Currently the agent has **zero memory** — each run starts from scratch. The plan is a three-layer memory system that lets the agent learn from experience.

### Layer 1: Session Memory (conversation context)

**Already exists** as `message[]`. Holds the current conversation.

- Scope: single run, in-memory list
- No changes needed

### Layer 2: Project Memory (cross-session knowledge)

A `memory.json` file that persists across runs.

```python
# On startup: load and inject into system prompt
memory = load_json("memory.json")  # {patterns:[], decisions:[], errors:[]}
system_prompt += f"\nProject memory:\n{format_memory(memory)}"

# New tool: save_memory — LLM calls this when it learns something
def save_memory(category: str, content: str):
    memory[category].append({"content": content, "ts": now()})
    write_json("memory.json", memory)
```

Three categories:
- **patterns** — code conventions, project structure ("tests use pytest", "imports are absolute")
- **decisions** — architectural choices ("chose SQLite over Postgres for simplicity")
- **errors** — recurring mistakes and their fixes ("ModuleNotFoundError → activate venv first")

### Layer 3: Reflection Memory (self-improvement)

After each session, the agent reviews its own performance and extracts lessons.

```python
# After agent loop ends:
reflection_prompt = f"""
Review this session:
- Tools called: {tool_call_log}
- Errors hit: {error_log}
- What should be done differently next time?
Output a JSON list of lessons.
"""
lessons = call_llm(reflection_prompt)
append_to("reflections.json", lessons)

# Next startup: load recent reflections into system prompt
# Periodically summarize old reflections to prevent unbounded growth
```

### Memory Lifecycle

```
Session N:
  startup ──► load Layer 2 + Layer 3 into system prompt
     │
  agent loop ──► Layer 1 (in-memory)
     │            ├── save_memory() → update Layer 2
     │            └── tool_call_log → feed Layer 3
     │
  shutdown ──► reflection → update Layer 3
                            │
                            ▼
                  prune old entries if > threshold
                  summarize stale reflections

Session N+1:
  startup ──► load updated Layer 2 + Layer 3
              (agent is now smarter than last time)
```

This creates a feedback loop: **act → reflect → remember → act better**.
