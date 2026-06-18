# Contributing to Kyvera

Thanks for your interest in contributing! Kyvera is an early-stage project and there is plenty of room to help. This guide will walk you through how the codebase is structured, what kinds of contributions are welcome, and how to get started without breaking things.

---

## Table of contents

- [Project structure](#project-structure)
- [How the interpreter works](#how-the-interpreter-works)
- [Setting up your environment](#setting-up-your-environment)
- [Types of contributions](#types-of-contributions)
    - [Adding a new language](#adding-a-new-language)
    - [Fixing a bug](#fixing-a-bug)
    - [Adding a new keyword or feature](#adding-a-new-keyword-or-feature)
- [Before you open a PR](#before-you-open-a-pr)
- [Known issues](#known-issues)

---

## Project structure

```
Kyvera/
├── run.py                  # Entry point — reads a .kyv file and kicks off the pipeline
├── kyvera/
│   ├── core/
│   │   ├── lexer.py        # Turns source code into a list of tokens
│   │   ├── parser.py       # Turns tokens into an AST (abstract syntax tree)
│   │   ├── ast.py          # Defines the node types that make up the AST
│   │   └── interpreter.py  # Walks the AST and executes the program
│   ├── languages/
│   │   ├── loader.py       # Looks up and returns a language pack by name
│   │   ├── japanese.py     # Japanese keyword mappings
│   │   ├── german.py       # German keyword mappings
│   │   └── italian.py      # Italian keyword mappings
│   └── errors/             # Intended for custom error types (not yet implemented)
└── examples/               # Example .kyv programs
```

---

## How the interpreter works

Understanding the pipeline is the most important thing before making any change.

When you run `python run.py myfile.kyv`, here is what happens step by step:

**1. Language detection** (`run.py`)
The first line of the file is read to find `use <language>`. This tells the interpreter which language pack to load.

**2. Lexing** (`lexer.py`)
The source code is scanned line by line and broken into tokens. A token is a tuple of `(type, value)` — for example `("VAR", None)` or `("NUMBER", 18)`. The lexer also tracks indentation and emits `INDENT` and `DEDENT` tokens for block structure.

**3. Parsing** (`parser.py`)
The token list is read and turned into an AST — a tree of node objects defined in `ast.py`. Statements (variable declarations, print, if) are parsed from the main token stream. Expressions (arithmetic, comparisons, logic) are parsed separately using a secondary position tracker `expr_pos` that walks a sliced sub-list of tokens.

**4. Interpreting** (`interpreter.py`)
The AST is walked node by node. Statements use a `visit_<NodeType>` dispatch pattern. Expressions are evaluated recursively through a separate `evaluate()` method. Variable values are stored in a plain dict on the interpreter.

---

## Setting up your environment

You need Python 3.x. No external packages are required.

```bash
git clone https://github.com/iretiola-007/kyvera.git
cd kyvera
python run.py examples/konnichiwa.kyv
```

**Before making any changes**, clear the Python cache. Stale `.pyc` files can make it look like your edits are working (or broken) when they are not:

```bash
find . -type d -name __pycache__ -exec rm -rf {} +
```

Run this every time you pull new changes too.

---

## Types of contributions

### Adding a new language

This is the easiest and most self-contained contribution you can make. Each language is a single Python file that maps that language's keywords to Kyvera's internal token types.

**Step 1 — Create the language file**

Add a new file at `kyvera/languages/<language>.py`. Here is the template:

```python
KEYWORDS = {
    "your_word_for_var":    "VAR",
    "your_word_for_print":  "PRINT",
    "your_word_for_if":     "IF",
    "your_word_for_else":   "ELSE",
    "your_word_for_input":  "INPUT",
    "your_word_for_func":   "FUNCTION",
    "your_word_for_return": "RETURN",
}

ERRORS = {
    "SYNTAX": "your translation of 'Syntax Error'",
    "NAME":   "your translation of 'Name Error'",
}
```

Only `VAR`, `PRINT`, `IF`, and `ELSE` are currently functional. The others (`INPUT`, `FUNCTION`, `RETURN`) are defined in existing language packs but not yet wired up in the interpreter — include them anyway so the file is ready when those features land.

**Step 2 — Register the language**

Open `kyvera/languages/loader.py` and add your language to the imports and the `LANGUAGES` dict:

```python
from . import japanese, german, italian, your_language   # add your import

LANGUAGES = {
    "japanese": japanese,
    "german":   german,
    "italian":  italian,
    "your_language": your_language,                       # add your entry
}
```

The name you use as the dict key is what users write in `use <name>` at the top of their `.kyv` file.

**Step 3 — Write an example file**

Add a small `.kyv` file to the `examples/` folder that demonstrates your language. Keep it simple — a variable declaration, a print statement, and a basic comparison is enough.

**Step 4 — Test it**

```bash
python run.py examples/your_example.kyv
```

If the output looks right, you're done.

---

### Fixing a bug

Before changing anything, make sure you understand exactly what the bug is. The fastest way to do that is to add temporary `print` statements to trace what's happening at each stage of the pipeline:

```python
# In run.py, after tokenizing:
print(tokens)

# In run.py, after parsing:
print(ast)
```

Run your broken `.kyv` file and read the output. Compare what the lexer produced to what you expected. Then compare what the parser built to what you expected. Most bugs live in the gap between those two things.

Once you have found the problem, make the smallest possible change that fixes it. A PR that touches one function is much easier to review than one that refactors three files.

---

### Adding a new keyword or feature

New features need changes in up to four places. Work through them in this order:

**1. Language packs** (`kyvera/languages/*.py`)
Add the new keyword mapping to every language file. The value should be the internal token type string you are going to use, for example `"LOOP"`.

**2. Lexer** (`kyvera/core/lexer.py`)
The lexer already handles keywords automatically by looking them up in the language pack's `KEYWORDS` dict — so if you added the keyword in step 1, the lexer will emit the right token type without any changes needed here. You only need to touch the lexer if you are adding new punctuation or new token patterns.

**3. Parser** (`kyvera/core/parser.py`)
Add a new AST node class in `ast.py` for the construct you are building, then add a `parse_<thing>()` method to the parser and call it from the main `parse()` loop when the relevant token type is seen.

**4. Interpreter** (`kyvera/core/interpreter.py`)
Add a `visit_<NodeType>()` method that handles your new node. Follow the pattern of the existing visit methods.

---

## Before you open a PR

- Clear `__pycache__` and run the examples in `examples/` to make sure nothing you changed broke existing behaviour.
- Keep each PR focused on one thing. A bug fix and a new feature should be two separate PRs.
- If you are fixing a bug, describe what the bug was and how you confirmed the fix works in the PR description.
- If you are adding a language, mention in the PR which keywords you translated and what source you used (dictionary, native speaker, etc).

---

## Known issues

These are confirmed bugs in the current codebase. If you want to help but are not sure where to start, any of these would be a great first contribution:

- **`else` blocks do not execute.** The parser allocates `else_body` but never reads past the `if` block to populate it. The `ELSE` token from the language pack is tokenised correctly but silently skipped during parsing.
- **`ast.py` defines `BinOpNode` twice** with different attribute names (`operator` vs `op`). The interpreter works around this with a `getattr` fallback. The fix is to pick one and remove the other.
- **`UnaryOpNode` has a typo** in its constructor: `def __init` instead of `def __init__`. This means it cannot be instantiated and is currently non-functional.
- **Unresolved merge conflict markers** remain in `examples/salve.kyv` and `kyvera/errors/placeholder_file`. These should be cleaned up.
- **Compiled `.pyc` files are committed** to the repository. A `.gitignore` should be added to exclude them.
