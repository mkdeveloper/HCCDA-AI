# NumPy for Beginners
## Student Notes

*Arrays: the number format behind AI code*

---

## How to Use These Notes

These are notes, not a list of commands. In every section you read a short explanation, type the code yourself, and
look at what happens. If your result is not what the notes describe, read the step again.

> **GOLDEN RULE**
> Do not copy and paste. Type each cell yourself and predict the result before you run it.

**The boxes you will see**

| Box | What it asks you to do |
|---|---|
| **LOOK FOR** | Stop and observe something specific in the result |
| **REMEMBER** | A key idea worth keeping |
| **WATCH OUT** | A common mistake to avoid |
| **TRY IT YOURSELF** | A short exercise. No copying, use what you just learned |

**Learning path**

| # | Topic | Goal |
|---|---|---|
| 1 | Why NumPy? | Understand how an array differs from a list |
| 2 | Creating arrays | Build arrays with `np.array`, `zeros`, `ones`, `arange`, `linspace` |
| 3 | Shape, size and type | Read `shape`, `ndim`, `size` and `dtype` |
| 4 | Indexing and slicing | Pick out items, rows, columns and filtered values |
| 5 | Maths on whole arrays | Calculate on every item at once |
| 6 | Totals and the axis | Calculate sums and averages across rows or columns |
| 7 | Broadcasting | Combine a table with a smaller array |
| 8 | Practice project | Analyse a table of student marks |

---

## Setup

Do this once. Run each command in a terminal:

```bash
uv init numpy_lab
cd numpy_lab
uv add numpy
uv add --dev ipykernel
```

Create a notebook named `numpy_lab.ipynb` in the `numpy_lab` folder and open it in VS Code. When VS Code asks for a
kernel, select the project's **`.venv`** Python environment.

**One notebook, all the code.** Each code block in these notes is one cell. Add a new code cell, paste the code, run it
with **Shift + Enter**, and keep the cells in order.

> **LOOK FOR**
> Check the bottom of VS Code or the notebook header. It should show the `.venv` environment you selected.

---

## 1. What Is NumPy?

Python is the language. NumPy is a library that adds **arrays**: grids of numbers that you can do maths on all at once.

A **list** can hold anything. A **NumPy array** holds numbers of one kind, packed together. Because of that, one
operation works on every number in the array in one step.

**Cell: lists and arrays**

```python
import numpy as np

marks_list = [60, 75, 90]
marks_array = np.array([60, 75, 90])

print(marks_list * 2)
print(marks_array * 2)
print(marks_list + marks_list)
print(marks_array + marks_array)
```

> **LOOK FOR**
> Compare the first two lines of output. The list was repeated; the array was doubled.

> **REMEMBER**
> `*` on a list repeats the list. `*` on an array multiplies every number.

> **WATCH OUT**
> Adding two arrays adds matching positions. Adding two lists joins them into one longer list.

> **TRY IT YOURSELF**
> Predict the result of `marks_array / 2` before you run it. Then try `marks_list / 2`. Read the error message. What
> does it say?

**Quick Check**

1. What does `marks_array * 2` do?
2. Why does `marks_list * 2` not double the numbers?

---

## 2. Creating Arrays

`np.array` turns a list into an array. Some functions create arrays without you typing every number:

| Function | What it creates |
|---|---|
| `np.array([1, 2, 3])` | an array from a list you write |
| `np.zeros(3)` | 3 zeros |
| `np.ones((2, 3))` | 2 rows and 3 columns of ones (the shape is one tuple) |
| `np.full((2, 2), 7)` | a 2 by 2 grid filled with 7 |
| `np.arange(0, 10, 2)` | 0, 2, 4, 6, 8 (stops **before** 10) |
| `np.linspace(0, 1, 5)` | 5 evenly spaced numbers, **including** both ends |

**Cell: creating arrays**

```python
import numpy as np

a = np.array([1, 2, 3, 4])
b = np.zeros(3)
c = np.ones((2, 3))
d = np.full((2, 2), 7)
e = np.arange(0, 10, 2)
f = np.linspace(0, 1, 5)

print(a)
print(b)
print(c)
print(d)
print(e)
print(f)
```

> **LOOK FOR**
> `zeros` shows `0.` with a dot. Zeros are decimals by default.

> **WATCH OUT**
> `arange` leaves out the end value. `linspace` includes it.

> **TRY IT YOURSELF**
> 1. Make an array of the even numbers from 2 to 20.
> 2. Make 5 evenly spaced numbers from 0 to 100.
> 3. Make a 3 by 3 array of zeros.

**Quick Check**

1. What is the difference between `np.arange` and `np.linspace`?
2. What shape does `np.ones((2, 3))` have?

---

## 3. Shape, Size and Type

Every array knows four things about itself:

| Attribute | Meaning |
|---|---|
| `shape` | the size as (rows, columns) |
| `ndim` | how many directions: 1 for a line, 2 for a table |
| `size` | the total number of items |
| `dtype` | the type of every item |

**Cell: shape, size and type**

```python
import numpy as np

scores = np.array([[70, 85, 90],
                   [60, 75, 80]])

print(scores.shape)
print(scores.ndim)
print(scores.size)
print(scores.dtype)

prices = np.array([4.5, 35, 59.99])
print(prices.dtype)
print(scores.astype(float))
```

> **REMEMBER**
> An array holds only one type. If you mix whole numbers and decimals, every number becomes a decimal.

> **TRY IT YOURSELF**
> Make `temps = np.array([[30, 32], [28, 35], [31, 29]])`. Print its shape, ndim, size and dtype. Then predict the dtype
> of `np.array([1, 2.5, 3])` and check it.

**Quick Check**

1. An array has 3 rows and 4 columns. What are its shape and size?
2. What does `astype(float)` do?

---

## 4. Indexing and Slicing

Counting starts at **0**. A minus sign counts from the end.

| Code | Meaning |
|---|---|
| `marks[0]` | the first item |
| `marks[-1]` | the last item |
| `marks[1:4]` | items 1, 2 and 3 (stops **before** 4) |
| `table[1, 2]` | row 1, column 2 |
| `table[:, 1]` | all rows, column 1 (the colon means "all") |
| `marks[marks >= 60]` | only the marks that are 60 or more |

**Cell: indexing and filtering**

```python
import numpy as np

marks = np.array([55, 72, 38, 91, 64])

print(marks[0])
print(marks[-1])
print(marks[1:4])
print(marks[::2])
print(marks >= 60)
print(marks[marks >= 60])

table = np.array([[70, 85, 90],
                  [60, 75, 80],
                  [50, 65, 95]])

print(table[1, 2])
print(table[0])
print(table[:, 1])
print(table[1:, :2])
```

> **LOOK FOR**
> `marks >= 60` gives True or False for each mark. Then the second line keeps only the True items.

> **WATCH OUT**
> A slice `1:4` stops before 4. Students often expect it to include 4.

> **TRY IT YOURSELF**
> With `marks = np.array([55, 72, 38, 91, 64])`, print the first three marks, the marks below 50, and every second mark.

**Quick Check**

1. What does `table[:, 1]` give?
2. What does `marks[marks >= 60]` return?

---

## 5. Maths on Whole Arrays

Maths works on every item at once:

- `prices * 2` multiplies every price by 2.
- `prices * quantities` multiplies matching positions: the first price by the first quantity, and so on.
- `prices > 30` gives True or False for every price.

**Cell: maths on arrays**

```python
import numpy as np

prices = np.array([4.50, 35.00, 59.99])
quantities = np.array([10, 2, 1])

print(prices * 2)
print(prices + 1)
print(prices * quantities)
print((prices * quantities).sum())
print(prices > 30)
```

> **LOOK FOR**
> `(prices * quantities).sum()` multiplies first, then adds everything: the total bill.

> **TRY IT YOURSELF**
> Take 10% off every price, then print the total after the discount.

**Quick Check**

1. What does `(prices * quantities).sum()` calculate?
2. What does `prices > 30` return?

---

## 6. Totals, Averages and the Axis

`sum`, `mean`, `max` and `min` work on the whole array. In a table, the **axis** tells NumPy which direction to work in.

> **REMEMBER**
> The axis you name disappears from the shape.
> - `axis=0` works **down the rows**, giving one result per **column**.
> - `axis=1` works **across the columns**, giving one result per **row**.

**Cell: totals and averages**

```python
import numpy as np

marks = np.array([[70, 85, 90],
                  [60, 75, 80],
                  [50, 65, 95]])

print(marks.sum())
print(marks.mean())
print(marks.max(), marks.min())
print(marks.sum(axis=0))
print(marks.mean(axis=1))
print(marks.argmax())
print(marks.argmax(axis=1))
```

> **LOOK FOR**
> `argmax()` gives the *position* of the biggest number. `max()` gives the number itself.

> **TRY IT YOURSELF**
> Using the `marks` table in this cell, print the average of each column and the total of each row.

**Quick Check**

1. What is the difference between `axis=0` and `axis=1`?
2. What does `argmax` return, compared with `max`?

---

## 7. Broadcasting

When a table and a smaller array are combined, NumPy repeats the smaller array to match the table. This is called
**broadcasting**.

Line up the shapes from the right. Each pair must match, or one of them must be 1.

**Cell: broadcasting**

```python
import numpy as np

marks = np.array([[70, 85, 90],
                  [60, 75, 80],
                  [50, 65, 95]])

bonus = np.array([5, 0, 10])
per_student = np.array([[1], [2], [3]])

print(marks + 5)
print(marks + bonus)
print(marks + per_student)
```

> **LOOK FOR**
> `marks + bonus` adds 5 to column 0, 0 to column 1 and 10 to column 2, in every row.

> **WATCH OUT**
> `(3,) + (4,)` fails. 3 and 4 do not match, and neither is 1.

> **TRY IT YOURSELF**
> Add the bonus `[1, 2, 3]` to every row of `marks`. Predict the first row before you run it.

**Quick Check**

1. Why can a table of shape (3, 3) combine with a shape (3,) array?

---

## 8. Practice Project: Marks Analyser

Five students, three subjects. Add a new code cell with the starter below and complete the six TODOs. Check each
line against the TODO that asks for it.

**Cell: starter**

```python
import numpy as np

subjects = ["Math", "Physics", "Python"]
marks = np.array([[72, 65, 88],
                  [45, 38, 52],
                  [90, 85, 95],
                  [60, 70, 55],
                  [33, 48, 40]])

# TODO 1: each student's average (one number per row), rounded to 1 decimal
# TODO 2: each subject's average (one number per column), rounded to 1 decimal
# TODO 3: the number (1 to 5) of the student with the highest average
# TODO 4: did each student score 40 or more in every subject? (True/False
#         per student). Then print how many students passed.
# TODO 5: the top mark in each subject, printed with the subject name
# TODO 6: add 5 grace marks to Physics only (maximum 100).
#         Print the Physics marks before and after.
```

> **TRY IT YOURSELF**
> Complete the TODOs one at a time. Run the cell after each one, and check the output matches what each TODO asks for.

> **Hints:** `mean(axis=1)`, `round(1)`, `argmax()`, `(marks >= 40).all(axis=1)`, `.sum()` counts True values,
> `zip(subjects, ...)`, `np.minimum(a, 100)`, `marks.copy()`.

---

## Errors You Will Meet

| Last line of the error | Usual cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'numpy'` | NumPy not installed, or the notebook uses another environment | run `uv add numpy` in the project, and select the `.venv` kernel |
| `ValueError: operands could not be broadcast together` | the shapes do not line up | print `.shape` of both arrays |
| `IndexError: index 5 is out of bounds` | the index is past the last item | valid indexes run from 0 to size minus 1 |
| `TypeError: can't multiply sequence by non-int of type 'float'` | list maths with a decimal | convert with `np.array(...)` |

---

## Reference Card

| You want to... | Write |
|---|---|
| Import NumPy | `import numpy as np` |
| Make an array | `np.array([1, 2, 3])`, `np.zeros((2, 3))`, `np.arange(0, 10, 2)` |
| Check an array | `a.shape`, `a.ndim`, `a.size`, `a.dtype` |
| Pick items | `a[0]`, `a[-1]`, `a[1:4]`, `t[1, 2]`, `t[:, 1]`, `a[a > 5]` |
| Totals | `a.sum()`, `a.mean()`, `a.max()`, `a.argmax()`, `t.sum(axis=0)` |
| Convert type | `a.astype(float)` |

---

## Knowledge Check

Answer in your own words. If you get stuck, go back to the section.

1. What is the difference between a list and a NumPy array?
2. What do `shape`, `ndim` and `size` tell you?
3. What does `arange(0, 10, 2)` stop before, and what does `linspace(0, 1, 5)` include?
4. In `table[1, 2]`, which row and which column?
5. What does `axis=0` mean in `sum(axis=0)`?
6. Why can `(3, 3) + (3,)` work but `(3,) + (4,)` fail?

> **GOLDEN RULE**
> Type the code yourself, make mistakes, read the error, and try again. That is how you become comfortable with NumPy.
