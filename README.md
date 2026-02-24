
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
To use NovaScript, you must declare the language at the top of each `.nova` file.

Use this to declare the language: 
``` 
use <language_name>
```

Example:
```
use german
```
Only that language’s keywords can be used in the file.

---

### 4.3 Keywords
NovaScript currently supports basic keywords and built-in commands.

🇯🇵 Japanese: 
- `hensuu` - variable declaration
- `shutsuryoku` - print statement
- `moshi` - if statement
- `soredehanai` - else statement

🇩🇪 German:
- `zahl` - variable declaration
- `ausgabe` - print statement
- `wenn` - if statement
- `sonst` - else statement

🇮🇹 Italian:
- `variabile` - variable declaration
- `stampa` - print statement
- `se` - if statement
- `altrimenti` - else statement

---

## 4.2 Variables
Variables use a simple assignment style similar to Python, but with a different operator.

NovaScript uses `->` instead of `=`.

Example:
```
hensuu sai -> 18 
```

---

## 4.3 Functions and Control Flow
Currently, NovaScript supports basic `if` and `else` statements in language mode.
More advanced control flow features (*like loops*) will be added in future updates.

---

## 5. Built-in Functions
NovaScript currently includes basic built-in functionality such as the shutsuryok statement (*in English, it's the print function*).
More built-in functions will be added over time.

---

## 6. Examples
`file.nova`
```
use japanese
hensuu sai -> 18
moshi sai > 10:
    shutsuryoku(1)
soredehanai:
    shutsuryoku(0)
```
Here, you declare a variable `sai` and assign `18` to it.
Since strings and Boolean statements haven't been implemented, you can use numbers as placeholder for return values.
However, if you directly compare numbers in a statement, you'll get a Boolean return value.
Example:
```
use japanese
shutsuryoku(5 > 1)
```
This would return `True`. Chain comparison is also supported. 
### Note: you can compare two values without using parentheses 
Like in this example above. To do a chain comparison, you must encase values in parentheses as such below:
```
use japanese
shutsuryoku(5 > 2 > 1)
```
More example programs will be added as more features are implemented.

---

## 7. Future Improvements
Planned features include:
- if...else statements
- Loops
- More built-in functions
- Expanded multi-language support
- Improved error handling
- String support (*currently NovaScript only supports numbers*)

---

## 📝 Note
This README will be updated as NovaScript evolves and new features are added.
Thank you for using NovaScript.

If you find this project interesting, consider starring the repository.


Ciao 😉