---

# Test Case Generation Language Specification 🚀🎉

Welcome to the **Test Case Generation Language**! This document provides a complete overview of the syntax and conventions for writing test cases. Whether you’re generating simple variables or complex data structures, this language has got you covered! 💻🔥

---

## General Rules 💡

- **Each line ends with a semicolon (`;`).**  
- Supports **basic data types:**  
  - `int` 👉 **Integer**
  - `float` 👉 **Floating numbers**
  - `char` 👉 **Character**

- **Default Value Ranges:**  
  - **int:** Defaults to a positive long long integer between <span style="color:blue;">0</span> and <span style="color:blue;">2^64</span>.
  - **float:** Defaults to a number between <span style="color:green;">0</span> and <span style="color:green;">2^64</span> with precision up to 6 digits.
  - **char:** Defaults to a random lowercase character (unless specified as lower, upper, number, or special).

---

## Variable Declarations 📝

### Single Variable Declaration

Declare simple variables like this:  
```plaintext
int a;
float b;
char c;
```

You can also specify limits:  
```plaintext
int a(10, 100);            // 'a' is between 10 and 100 😎
float b(0, 1000, 6);         // 'b' is between 0 and 1000 with 6-digit precision 🌟
```

### Multiple Variables in One Statement

Use commas to separate multiple declarations:  
```plaintext
int a, int b, float c, char d;
```

---

## Array Declarations 📊

### How to Declare an Array

1. **First, declare the size:**  
   ```plaintext
   int size_of_array;
   ```
2. **Then, declare the array:**  
   ```plaintext
   array int size_of_array;
   ```
> **Note:** The same default limits apply (0 to 2^64 for ints, floats with 6-digit precision, and lowercase for chars). 😃

---

## String Declarations 🖋️

### Declaring a String

Declare a string by first specifying its size, then defining the string with the desired character set:
```plaintext
int n;
string s(n, lower);                  // 's' is a lowercase string 😍
string t(n, lower + upper + number);   // 't' is a mixed string with letters and numbers 💥
```

**Character Set Options:**
- `lower` 👉 Lowercase letters
- `upper` 👉 Uppercase letters
- `number` 👉 Numeric digits
- `special` 👉 Special characters  
Combine using `+` for mixtures!

---

## Special Data Structures 🌟

### Permutations

Generate a permutation of integers from 1 to n:  
```plaintext
permutation(n);
```
*Example:*  
```plaintext
int n;
permutation(n);
```

### Graphs

Declare graphs with the following syntax:  
```plaintext
graph(index, V, E, directed, weighted(lower, upper));
```
- **index:** `1` for 1-based indexing, `0` for 0-based.
- **V:** Number of vertices.
- **E:** Number of edges.
- **directed:** `1` if directed, `0` if undirected.
- **weighted:** Provide lower and upper limits if weighted.

*Example:*  
```plaintext
graph(1, 5, 7, 0, 1(10, 50));
```

### Trees

Declare trees with:  
```plaintext
tree(index, V, weighted(lower, upper));
```
- **index:** `1` for 1-based indexing, `0` for 0-based.
- **V:** Number of vertices.
- **weighted:** `1` if weighted (limits specified), `0` if not.

*Example:*  
```plaintext
tree(1, 10, 1(5, 20));
```

### Binary Strings

Generate a random binary string:  
```plaintext
binary_string(size);
```
Or, for a binary string with a given number of 0's and 1's:  
```plaintext
binary_string(size, #0, #1);
```
> **Note:** Ensure `#0 + #1 = size`; otherwise, an error is raised! ⚠️

### 2D Matrices

Declare a 2D matrix as follows:  
```plaintext
matrix(datatype, rows, cols);
```
Data types can be:  
- `int(lower, upper)`
- `float(lower, upper, precision)`
- `char(lower, upper, set)`  
*Examples:*  
```plaintext
matrix(int(1, 100), 3, 3);
matrix(float(0, 1000, 6), 4, 4);
matrix(char(lower), 2, 5);
```
For characters, you can mix sets using `+` (e.g., `char(lower + special)`).

---

## Assignment Expressions 🔄

You can assign values using expressions. For instance:  
```plaintext
int n;
int b = 2 * n;
int c = n + 2;
int z = n / 5;
```

---

## Comments 💬

### Single-line Comments

Use `//` for single-line comments:
```plaintext
// This is a comment
int a;
```

### Multi-line Comments

Use `/* ... */` for multi-line comments:
```plaintext
/* 
   This is a multi-line comment.
   It can span several lines.
*/
```

---

## Conclusion 🎯🌈

This **Test Case Generation Language** empowers you to quickly create robust test cases with a rich syntax that supports various data types, arrays, strings, and special data structures. Whether you're a beginner or a seasoned competitive programmer, this language offers flexibility, clarity, and fun! 🎉💻

Happy Testing and Coding! 🚀✨

---

*Embrace the power of coding with colors and emojis!* 😄🌟

