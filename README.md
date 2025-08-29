# C/Python Code Converter

This project consists of two separate C programs designed to convert code snippets between C and Python. Each program is a simple command-line utility that takes input C or Python code and outputs a translation into the other language.

---

## 📂 `Cproject24.c` - C to Python Converter

This program takes lines of C code from standard input and attempts to convert them into equivalent Python code. It handles basic variable declarations, print statements, and control flow structures.

### Key Features

* **Variable Declarations**: Converts `int` and `float` variable declarations to Python-style assignments.
    * `int a;` becomes `a = 0`
    * `float b;` becomes `b = 0.0`
* **`printf` Statements**: Translates C's `printf` function calls to Python's `print()` function.
    * `printf("Hello, World!\n");` becomes `print("Hello, World!")`
* **`if` Statements**: Converts `if` statements with their conditions.
    * `if (a > 0)` becomes `if a > 0:`
* **`for` Loops**: Translates simple `for` loops into Python's `for...in range()` syntax.
    * `for (int i = 0; i < 10; i++)` becomes `for i in range(0, 10):`
* **Assignments**: Handles simple variable assignments.
    * `b = 1.5;` becomes `b = 1.5`
* **Block Endings**: Adds comments for the end of a code block (e.g., after `}`).

---

## 📂 `pythonTOc.c` - Python to C Converter

This program takes a hardcoded block of Python code and translates basic assignments and `print` statements into C. The input Python code is a string literal within the `main` function.

### Key Features

* **Variable Assignments**: Converts variable assignments from Python to C syntax.
    * `num1 = 5` becomes `num1 = 5;`
* **`print` Statements**: Translates Python `print()` calls to C's `printf()` function.
    * `print("The sum is: ", result)` becomes `printf("The sum is: ", result);`

---

## 🛠️ How to Compile and Run

To use these programs, you'll need a C compiler like GCC.

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2.  **Compile the C to Python converter:**
    ```bash
    gcc Cproject24.c -o c2py
    ```

3.  **Run `c2py`:**
    You can pipe C code into the program or type it directly.
    ```bash
    echo 'int x;' | ./c2py
    # Output:
    # x = 0
    ```
    Or, for interactive use:
    ```bash
    ./c2py
    Enter C code:
    int myVar;
    # (Press Ctrl+D to send EOF)
    # Output:
    # myVar = 0
    ```

4.  **Compile the Python to C converter:**
    ```bash
    gcc pythonTOc.c -o py2c
    ```

5.  **Run `py2c`:**
    This program has hardcoded input, so you simply run the executable.
    ```bash
    ./py2c
    # Output:
    # C code generated from Python code:
    # num1 = 5;
    # num2 = 10;
    # result = num1 + num2;
    # printf("The sum is: ", result);
    ```

---

## 📝 Limitations and Future Improvements

* **Error Handling**: Both programs have limited error handling. Malformed input may lead to unexpected results or crashes.
* **Complex Statements**: The converters only handle a limited subset of each language. More complex expressions, function calls, or data structures are not supported.
* **Python to C Converter**: The `pythonTOc.c` program currently only works with hardcoded input. It could be improved by reading input from a file or standard input, similar to `Cproject24.c`.
* **Type System**: The C to Python converter doesn't infer data types from assignments, and the Python to C converter makes a simple assumption. A more robust solution would handle type inference and conversions more intelligently.
