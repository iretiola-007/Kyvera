
# NovaScript 

Code in your language. Think in your style. 🤏🏼

---

***📘 Documentation***
## 1. Introduction

NovaScript is a lightweight programming language inspired by Python. It is built with a custom interpreter written in Python and follows a Python-like structure while introducing its own unique features.

NovaScript’s main feature is **multi-language support**, currently supporting **Japanese, German, and Italian**, with more languages planned for future releases.

The goal of NovaScript is to provide a simple, flexible, and extensible language that can grow over time.

---


## 2. Installation
### Requirements
- Python 3.x installed on your system


### Setup
Clone the repository:
```
git clone https://github.com/iretiola-007/novascript.git
cd novascript
```

---


## 3. Getting Started
To run a `.nova` file:
```
python run.py filename.nova
```

Example: 
```
python run.py hello_de.nova
```

---


## 4. Syntax Overview

## 4.1 Language declaration 
To use NovaScript, you need to declare which language you're using in each `.nova` file

Use this to declare the language: 
``` 
use <language_name>
```

Example:
```
use german
// only German code must be written
```

---

### 4.3 Keywords
NovaScript currently supports basic keywords and built-in commands.

For Japanese: 
- hensuu (variable declaration)
- shutsuryoku (print statement)
- moshi (if statement)
- soredehanai (else statement)

For German:
- zahl (variable declaration)
- ausgabe (print statement)
- wenn (if statement)
- sent (else statement)

For Italian:
- variabile (variable declaration)
- stampa (print statement)
- se (if statement)
- altrimenti (else statement)

---

## 4.2 Variables
Variables can be created using a simple assignment syntax, similar, but not the same as Python.

Example:
```
hensuu sai -> 18 
// an arrow is used instead of the traditional equal sign "="
```

---

## 4.3 Functions and Control Flow

Functions and full Control Flow features are not yet implemented.
For now you can only use `if...else` statements.
Other statements will be added in future updates.

---

## 5. Built-in Functions
NovaScript currently includes basic built-in functions like the print statement (*in language modes*)

---

## 6. Examples
Example programs will be added as more features are implemented.

---

## 7. Future Improvements

Planned features include:
- if...else statements
- Loops
- More built-in functions
- Expanded multi-language support
- Improved error handling
- Strings (*you read right...for now NovaScript only supports numbers*)


## Note
This README will be updated as NovaScript evolves and new features are added.