# AI Coding Agent

A command-line AI agent that autonomously explores, reads, runs, and edits
code to complete tasks using LLM function calling.

## Features

The agent can call these functions on its own:

- **get_files_info** — list files/directories
- **get_file_content** — read a file
- **run_python_file** — execute a Python file
- **write_file** — create or overwrite a file

Given a prompt, it decides which functions to call and iterates until the
task is done.

## Usage

```sh
uv run main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20."
```

## How It Works

1. The prompt, system prompt, and function schemas are sent to the LLM.
2. The LLM either answers directly or requests a function call.
3. `call_function.py` runs the requested function and returns the result.
4. The loop repeats until the LLM gives a final response or hits a max
   iteration limit.

## Structure

```
functions/       # Agent's callable tools
calculator/      # Example project the agent operates on
call_function.py # Dispatches function calls
prompts.py       # System prompt
main.py          # Entry point
```

## Notes

File operations are sandboxed to the working directory. The system prompt
in `prompts.py` heavily influences how reliably the agent completes tasks.