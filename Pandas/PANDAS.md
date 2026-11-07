# Pandas for Data Analysis
## Student Notes

*Tables of data: loading, cleaning, summarising and using them for AI*

---

## What Is Pandas, and Why Use It?

**Pandas** is a Python library for working with tables of data. Its main object is the **DataFrame**: rows and named
columns, similar to a spreadsheet, but you control it with code.

Pandas is used because real data is messy. Before any analysis or AI model, you usually need to:

- **load** the data from a file (CSV, Excel, a database),
- **look** at it to see what is there,
- **select and filter** the rows and columns you care about,
- **fix** missing or wrong values,
- **summarise** it, for example average survival rate per class.

Pandas does all of these with short, readable commands, and it works fast on large tables. Most data work in Python
starts here, and the cleaned table is what goes into a model later.

> **REMEMBER**
> A DataFrame is a table. A **column** is one kind of information (such as `Age`). A **row** is one record (such as
> one passenger).

---

## How to Use These Notes

These are notes, not a list of commands. In every section you read a short explanation, type the code yourself,
and look at what happens. If your result is not what the notes describe, read the step again.

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
| 1 | Loading data | read a CSV file into a DataFrame |
| 2 | Looking at data | read types, column information and summaries |
| 3 | Selecting | pick columns and rows with `[]`, `loc` and `iloc` |
| 4 | Filtering | keep only the rows that match a condition |
| 5 | Missing values | find, fill and remove missing data |
| 6 | Grouping | calculate results for each group |
| 7 | Excel files | save to and read from `.xlsx` |
| 8 | Practical | clean, transform and analyse the Titanic data |

---

## Setup

Do this once. Run each command in a terminal:

```bash
uv init pandas_lab
cd pandas_lab
uv add numpy pandas openpyxl
uv add --dev ipykernel
```

**Dataset.** The notes use the Titanic passenger list. Download `titanic.csv` from this link and save it in a `data` folder inside `pandas_lab`:

https://github.com/datasciencedojo/datasets/blob/master/titanic.csv

Create a notebook named `pandas_lab.ipynb` in the `pandas_lab` folder and open it in VS Code. When VS Code asks for a
kernel, select the project's **`.venv`** Python environment.

**One notebook, all the code.** Each code block in these notes is one cell. Run each cell with **Shift + Enter**, in
order. The paths in the cells (`data/titanic.csv`) work when the notebook sits in the `pandas_lab` folder.

> **LOOK FOR**
> The file `data/titanic.csv` should be there before you start. If you see `FileNotFoundError`, check the path.

---

## 1. Loading Data

A **DataFrame** is a table: rows and named columns. `pd.read_csv` loads a CSV file into a DataFrame. `head()` shows the
first five rows.

**Cell: loading**

```python
import pandas as pd

df = pd.read_csv("data/titanic.csv")
print(df.shape)
print(df.columns.tolist())
df.head()
```

**What each function and method does**

| Call | What it does |
|---|---|
| `pd.read_csv(path)` | reads a CSV file and builds a DataFrame from it |
| `df.head()` | shows the first 5 rows (pass a number to change it, e.g. `head(10)`) |
| `df.shape` | a pair (rows, columns) telling you how big the table is |
| `df.columns.tolist()` | `df.columns` holds the column names; `tolist()` turns them into a normal Python list |
| `df.tail()` | shows the last 5 rows |

> **LOOK FOR**
> `(891, 12)` means 891 rows and 12 columns. Each row is one passenger.

> **TRY IT YOURSELF**
> 1. Print the last five rows with `df.tail()`.
> 2. How many passengers are there? Use `len(df)`. *Expected: 891.*
> 3. Load only the first 100 rows with `pd.read_csv("data/titanic.csv", nrows=100)`. What is its shape? *Expected: (100, 12).*
> 4. Print the column names and count them. *Expected: 12 names, starting with `PassengerId`.*

**Quick Check**

1. What does `df.shape` return?
2. What does `head()` show, and how many rows by default?

---

## 2. Looking at the Data

Three methods tell you what you have before you analyse it:

| Method | What it shows |
|---|---|
| `df.dtypes` | the type of each column |
| `df.info()` | how many values each column has, and the types |
| `df.describe()` | summary statistics for the number columns |

**Cell: looking**

```python
print(df.dtypes)
df.info()
df.describe()
```

**What each function and method does**

| Call | What it does |
|---|---|
| `df.dtypes` | shows the type of each column: `int64` (whole numbers), `float64` (decimals), `str` (text) |
| `df.info()` | prints the number of non-missing values per column, the types, and the memory used |
| `df.describe()` | summary statistics for number columns: count, mean, std (spread), min, quartiles, max |

> **LOOK FOR**
> `Age` has 714 values, not 891. Some ages are missing. Part 5 deals with this.

> **WATCH OUT**
> `describe()` only summarises number columns. Text columns such as `Name` are left out.

> **TRY IT YOURSELF**
> 1. Find the average `Fare` from `describe()`. *Expected: about 32.2.*
> 2. Which columns have missing values? *Expected: `Age` (177), `Cabin` (687) and `Embarked` (2).* Hint: `df.isna().sum()`.
> 3. How many passengers survived? *Expected: 342.* Hint: `df["Survived"].sum()` adds the 1s.

**Quick Check**

1. What is the difference between `dtypes` and `info()`?
2. Why does `Age` show fewer non-null values than the other columns?

---

## 3. Selecting Columns and Rows

| Code | Meaning |
|---|---|
| `df["Name"]` | one column, as a Series |
| `df[["Name", "Sex"]]` | several columns, as a DataFrame (note the double brackets) |
| `df.loc[0, "Name"]` | row with label 0, column `Name` |
| `df.iloc[0:3, 0:4]` | rows 0 to 2 and columns 0 to 3, by position |

**Cell: selecting**

```python
df["Name"].head(3)
df[["Name", "Sex", "Age"]].head(3)
df.loc[0, ["Name", "Survived"]]
df.iloc[0:3, 0:4]
```

**What each function and method does**

| Call | What it does |
|---|---|
| `df["Name"]` | selects one column; the result is a Series (a single column) |
| `df[["Name", "Sex", "Age"]]` | selects several columns; the result is a DataFrame (a table) |
| `df.loc[0, ["Name", "Survived"]]` | selects by **label**: row label 0, the named columns |
| `df.iloc[0:3, 0:4]` | selects by **position**: rows 0 to 2, columns 0 to 3. The stop number is excluded |

> **REMEMBER**
> `loc` uses **names** (labels). `iloc` uses **positions**. Both count from 0, but `iloc` stops before the end.

> **WATCH OUT**
> `df["Name", "Sex"]` with one set of brackets fails. Use `df[["Name", "Sex"]]`.

> **TRY IT YOURSELF**
> 1. Print the `Sex` and `Age` of the first five passengers.
> 2. Print the name of the passenger in row 10. *Expected: Sandstrom, Miss. Marguerite Rut.*
> 3. Print `Name`, `Ticket` and `Fare` for the first three passengers, using `loc` with a list of column names.

**Quick Check**

1. What is the difference between `loc` and `iloc`?
2. What does `df[["Name"]]` return compared with `df["Name"]`?

---

## 4. Filtering Rows

A condition such as `df["Sex"] == "female"` gives True or False for every row. Put it inside `df[...]` to keep only
the True rows.

When you combine conditions, use `&` (and), `|` (or), and brackets around each condition.

**Cell: filtering**

```python
women = df[df["Sex"] == "female"]
print(len(women))
first_class = df[df["Pclass"] == 1]
print(len(first_class))
rich_women = df[(df["Sex"] == "female") & (df["Fare"] > 100)]
print(rich_women[["Name", "Fare"]])
```

**What each function and method does**

| Call | What it does |
|---|---|
| `df["Sex"] == "female"` | compares every row; the result is True or False for each row |
| `len(women)` | counts the rows in the filtered table |
| `( ) & ( )` | combines two conditions: `&` means both must be True |
| `df[condition]` | keeps only the rows where the condition is True |

> **WATCH OUT**
> Use `&` and `|` for filters, not `and` and `or`. Each condition must be in brackets:
> `(df["Sex"] == "female") & (df["Fare"] > 100)`.

> **TRY IT YOURSELF**
> 1. Count the children (`Age` below 12). *Expected: 68.* Hint: `(df["Age"] < 12).sum()`.
> 2. Count the third-class passengers who survived. *Expected: 119.* Use `&` with two brackets.
> 3. Count the first-class passengers over 60. *Expected: 14.*

**Quick Check**

1. What does `df[df["Pclass"] == 1]` return?
2. Why are the brackets needed around each condition?

---

## 5. Missing Values

A missing value is shown as `NaN` (not a number). Three methods handle them:

| Method | What it does |
|---|---|
| `isna()` | True for each missing value |
| `fillna(value)` | replaces missing values with a value you choose |
| `dropna()` | removes rows that have missing values |

**Cell: missing values**

```python
print(df.isna().sum())
print(df["Age"].isna().mean().round(3))
df["Age"] = df["Age"].fillna(df["Age"].median())
print(df["Age"].isna().sum())
df_small = df.dropna(subset=["Embarked"])
print(len(df_small))
```

**What each function and method does**

| Call | What it does |
|---|---|
| `df.isna()` | True for every missing value (`NaN`), False otherwise |
| `df.isna().sum()` | counts the True values per column, so it counts the missing values |
| `df["Age"].isna().mean()` | the mean of True/False values is the fraction missing (0.199 means about 20%) |
| `df["Age"].median()` | the middle value when the ages are sorted |
| `df["Age"].fillna(value)` | returns a copy where every missing value is replaced with `value` |
| `df.dropna(subset=["Embarked"])` | removes rows where `Embarked` is missing; other rows are kept |

> **LOOK FOR**
> `Age` had 177 missing values. After filling with the median, none are left.

> **REMEMBER**
> The median is the middle value when sorted. It is less affected by extreme values than the mean.

> **TRY IT YOURSELF**
> 1. Fill the missing `Cabin` values with `"Unknown"`, then count the missing values again. *Expected: 0.*
> 2. Two passengers have no `Embarked` port. Fill them with the most common port, `df["Embarked"].mode()[0]`. The most common port is `S`.
> 3. How many rows are left after you remove rows with a missing `Age`? *Expected: 714.* Hint: `dropna(subset=["Age"])`, then `len()`.

**Quick Check**

1. What does `df.isna().sum()` count?
2. What is the difference between `fillna` and `dropna`?

---

## 6. Grouping and Summarising

`groupby` splits the table into groups, then calculates something for each group. This is the pandas version of the
NumPy `axis` idea from the NumPy notes.

**Cell: grouping**

```python
print(df.groupby("Sex")["Survived"].mean().round(3))
print(df.groupby("Pclass")["Survived"].mean().round(3))
print(df.groupby(["Pclass", "Sex"])["Survived"].mean().round(3))
print(df.groupby("Pclass")["Fare"].agg(["count", "mean", "max"]).round(2))
```

**What each function and method does**

| Call | What it does |
|---|---|
| `df.groupby("Sex")` | splits the rows into one group per sex |
| `["Survived"].mean()` | averages Survived within each group. Survived is 1 or 0, so the mean is the survival rate |
| `df.groupby(["Pclass", "Sex"])` | groups by two columns at once: each class and sex combination |
| `.agg(["count", "mean", "max"])` | calculates several statistics for each group in one step |
| `.round(2)` | rounds the numbers to 2 decimal places |

> **LOOK FOR**
> Women survived at a much higher rate than men: about 74% against 19%.

> **REMEMBER**
> `groupby(...)["Survived"].mean()` gives the survival rate, because Survived is 1 for yes and 0 for no.

> **TRY IT YOURSELF**
> 1. Find the average `Age` for each `Embarked` port. *Expected: C 30.8, Q 28.1, S 29.4.* Pandas skips missing values in `mean()`.
> 2. Find the survival rate for each `SibSp` value (siblings or spouses aboard). *Expected: 0 gives 0.345, 1 gives 0.536.* Which value has the highest rate?
> 3. Find the highest `Fare` in each class with `groupby("Pclass")["Fare"].max()`. *Expected: first class 512.33.*

**Quick Check**

1. What does `groupby("Pclass")["Fare"].mean()` return?
2. What does `agg(["count", "mean", "max"])` add to the result?

---

## 7. Excel Files

pandas can save a DataFrame to an Excel file with `to_excel`, and read it back with `read_excel`. Excel needs the
`openpyxl` package, which you installed in the setup step.

**Cell: Excel**

```python
summary = df.groupby("Pclass")["Survived"].mean().round(3).reset_index()
summary.to_excel("data/survival_by_class.xlsx", index=False)
back = pd.read_excel("data/survival_by_class.xlsx")
print(back)
```

**What each function and method does**

| Call | What it does |
|---|---|
| `summary.to_excel(path, index=False)` | writes the table to an Excel file. `index=False` leaves out the row numbers |
| `.reset_index()` | turns the group names from the index back into a normal column |
| `pd.read_excel(path)` | reads an Excel file back into a DataFrame |

> **LOOK FOR**
> `index=False` stops pandas writing the row numbers as an extra column.

> **WATCH OUT**
> `read_excel` needs `openpyxl`. If you see `ImportError`, run `uv add openpyxl` in the project.

> **TRY IT YOURSELF**
> 1. Save the average `Fare` for each class to `data/fare_by_class.xlsx`, then read it back.
> 2. Save the table of women only (`df[df["Sex"] == "female"]`) to `data/women.xlsx`. Read it back and count the rows. *Expected: 314.*

**Quick Check**

1. What does `index=False` do?
2. Which package does pandas need for Excel files?

---

## 8. Practical: Clean, Transform and Analyse

This part combines the earlier parts. You will create new columns, group them, and calculate statistics with NumPy.

**Cell: practical**

```python
import numpy as np

ages = df["Age"].to_numpy()
print("mean age:", round(ages.mean(), 2), "| median:", np.median(ages).round(2), "| std:", ages.std().round(2))
df["Family"] = df["SibSp"] + df["Parch"] + 1
print(df.groupby("Family")["Survived"].agg(["count", "mean"]).round(3))
df["AgeGroup"] = pd.cut(df["Age"], bins=[0, 12, 18, 60, 100], labels=["child", "teen", "adult", "senior"])
print(df.groupby("AgeGroup", observed=True)["Survived"].mean().round(3))
```

**What each function and method does**

| Call | What it does |
|---|---|
| `df["Age"].to_numpy()` | converts a pandas column into a NumPy array, so NumPy functions can use it |
| `np.median(ages)` | NumPy's median, the same idea as in Part 5 |
| `ages.std()` | standard deviation: how spread out the values are |
| `df["SibSp"] + df["Parch"] + 1` | adds the columns row by row, to get the family size including the passenger |
| `pd.cut(values, bins, labels)` | sorts each number into a named range (bin) |
| `groupby("AgeGroup", observed=True)` | groups by the bins, and skips bins with no rows |

> **LOOK FOR**
> Passengers travelling alone (family size 1) had the lowest survival rate among the common family sizes.

> **TRY IT YOURSELF**
> 1. Create a column `Adult` that is True when `Age` is 18 or more. Find the survival rate for adults and for children. *Expected: adults 0.381, under 18 0.390.*
> 2. Create a column `Alone` that is True when `Family` is 1. Find the survival rate for `Alone` True and False.
> 3. Find the number of passengers and the survival rate for each `Pclass` and `Sex` pair. Which group has the highest rate? *Expected: first-class women, 0.968.*

> **TRY IT YOURSELF (challenge)**
> Find which `AgeGroup` has the highest survival rate, and write one sentence explaining why you think that is.

---

## Errors You Will Meet

| Last line of the error | Usual cause | Fix |
|---|---|---|
| `KeyError: 'Survivd'` | a column name is misspelled | check `df.columns.tolist()` for the exact name |
| `FileNotFoundError: No such file or directory: 'data/titanik.csv'` | the file name or folder is wrong | check the path, and that the notebook is in `pandas_lab` |
| `ValueError: The truth value of a Series is ambiguous` | `and` was used instead of `&` | use `&` with brackets around each condition |
| `ImportError` when reading Excel | openpyxl is not installed | run `uv add openpyxl` |

---

## Reference Card

| You want to... | Write |
|---|---|
| Load a CSV | `df = pd.read_csv("data/titanic.csv")` |
| See the first rows | `df.head()` |
| Check the shape | `df.shape` |
| Pick a column | `df["Name"]` |
| Pick by name or position | `df.loc[row, "col"]`, `df.iloc[row, col]` |
| Filter rows | `df[(df["Sex"] == "female") & (df["Age"] > 18)]` |
| Count missing values | `df.isna().sum()` |
| Fill missing values | `df["Age"] = df["Age"].fillna(df["Age"].median())` |
| Group and average | `df.groupby("Pclass")["Survived"].mean()` |
| Save to Excel | `df.to_excel("data/out.xlsx", index=False)` |
| Read Excel | `pd.read_excel("data/out.xlsx")` |

---

## Knowledge Check

Answer in your own words. If you get stuck, go back to the section.

1. What is a DataFrame, and what does one row represent in the Titanic data?
2. What is the difference between `loc` and `iloc`?
3. Why must each condition be in brackets when you combine them with `&`?
4. What does `groupby` do, in one sentence?

> **GOLDEN RULE**
> Type the code yourself, make mistakes, read the error, and try again. That is how you become comfortable with pandas.
