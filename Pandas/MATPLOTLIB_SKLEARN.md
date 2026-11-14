# Matplotlib and scikit-learn
## Student Notes

*Charts first, then a first machine learning model*

---

## What Are Matplotlib and scikit-learn?

**Matplotlib** is Python's main plotting library. It draws charts: bars, lines, histograms and scatter plots. Pandas can
draw charts too, and uses Matplotlib underneath. A table of 891 passengers is hard to read. A bar chart shows the pattern
in one look. Charts help you check your data before you model it, and explain your results to other people.

- A **plot** is drawn on axes. `plt.title`, `plt.xlabel` and `plt.ylabel` label it.
- `plt.show()` displays the chart. In a notebook, it appears under the cell.

**scikit-learn** (imported as `sklearn`) is Python's main library for classic machine learning. It gives you ready-made
models (such as decision trees), tools to split and prepare data, and ways to measure results. Every model follows the
same pattern: `fit` to learn from examples, and `predict` to answer new questions.

A model is only useful if it does better than a simple guess. That is why every model in this lecture is compared with a
**baseline** and measured by its **accuracy**.

> **REMEMBER**
> Plot first, then model. A chart often shows what a model will find before you train it.

---

## How to Use These Notes

Follow the same rules as the pandas notes: type each cell yourself, predict the result, then run it.

> **GOLDEN RULE**
> Do not copy and paste. Predict each result before you run the cell.

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
| 1 | Bar charts | draw a chart from a pandas result, with labels |
| 2 | Histograms | see how a number column is spread |
| 3 | Your first classifier | train, test and measure a decision tree |
| 4 | Practical | compare groups on a chart, then change the model |

---

## Setup

You need the pandas notes first. They load the data into the variable `df`, and this lecture uses it.

Add the two packages to the same project, `pandas_lab`:

```bash
uv add matplotlib scikit-learn
```

Use the same notebook, `pandas_lab.ipynb`, in `src/pandas_lab`. Run the pandas cells first, then the cells below, in
order. The data file stays in `src/pandas_lab/data/titanic.csv`.

> **WATCH OUT**
> If you see `NameError: name 'df' is not defined`, you skipped the pandas cells. Run them first.

---

## 1. Bar Charts

A bar chart compares one value per group. `rates` holds the survival rate for each class, so the chart compares them.

**Cell: bar chart**

```python
import matplotlib.pyplot as plt

rates = df.groupby("Pclass")["Survived"].mean()
rates.plot(kind="bar", title="Survival rate by class")
plt.ylabel("Survival rate")
plt.xticks(rotation=0)
plt.show()
```

**What each function and method does**

| Call | What it does |
|---|---|
| `rates.plot(kind="bar", title=...)` | draws a bar chart of `rates`, with a title. `kind` chooses the chart type |
| `plt.ylabel("Survival rate")` | labels the vertical axis |
| `plt.xticks(rotation=0)` | keeps the class labels horizontal |
| `plt.show()` | displays the chart. In a notebook it appears under the cell |

> **LOOK FOR**
> The first class has the tallest bar: about 0.63. Passengers in first class were most likely to survive.

> **TRY IT YOURSELF**
> 1. Draw the survival rate by `Sex` as a bar chart, with a title and a label on the vertical axis. *Expected: female about 0.74, male about 0.19.*
> 2. Draw the number of passengers in each class as a bar chart. *Expected: third class has the most, 491.*

**Quick Check**

1. What does `kind="bar"` do?
2. What does `plt.show()` do in a notebook?

---

## 2. Histograms

A **histogram** shows how a number column is spread. It cuts the values into ranges (bins) and counts how many fall in each.

**Cell: histogram**

```python
df["Age"].plot(kind="hist", bins=20, title="Passenger ages")
plt.xlabel("Age")
plt.show()
```

**What each function and method does**

| Call | What it does |
|---|---|
| `df["Age"].plot(kind="hist", bins=20, ...)` | counts the ages in 20 equal ranges and draws one bar per range |
| `plt.xlabel("Age")` | labels the horizontal axis |

> **LOOK FOR**
> The tallest bar is about ages 20 to 24, with 98 passengers. Most passengers were young adults.

> **WATCH OUT**
> `bins` changes the picture. Try 5 and 50 and see how the shape changes, but the counts are the same data.

> **TRY IT YOURSELF**
> 1. Draw the histogram with `bins=10`. Which range has the most passengers now?
> 2. Draw a histogram of `Fare` with `bins=30`. Most fares are low, so what do you notice about the few very high fares?

**Quick Check**

1. What does a histogram count?
2. What does `bins` control?

---

## 3. Your First Classifier

A **classifier** learns from examples and then predicts a category. This one predicts whether a passenger survived, from
their class, sex, age and fare.

Every model follows four steps:

1. **Choose features** (the inputs) and the **target** (the answer to predict).
2. **Split** the rows into training rows and test rows.
3. **Fit** the model on the training rows.
4. **Predict** on the test rows and measure the **accuracy**.

**Cell: classifier**

```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

features = pd.DataFrame({
    "Pclass": df["Pclass"],
    "Female": (df["Sex"] == "female").astype(int),
    "Age": df["Age"],
    "Fare": df["Fare"],
})
target = df["Survived"]
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.25, random_state=42)
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print("accuracy:", round(accuracy_score(y_test, predictions), 3))
print("baseline (always predict 'did not survive'):", round((y_test == 0).mean(), 3))
```

**What each function and method does**

| Call | What it does |
|---|---|
| `pd.DataFrame({...})` | builds a table of features from the columns you choose |
| `(df["Sex"] == "female").astype(int)` | turns True/False into 1/0, because the model needs numbers |
| `train_test_split(features, target, test_size=0.25, random_state=42)` | splits the rows: 75% for training, 25% for testing. `random_state` makes the split repeatable |
| `DecisionTreeClassifier(max_depth=3, random_state=42)` | creates a model that makes decisions by asking yes/no questions. `max_depth` limits how many questions in a row |
| `model.fit(X_train, y_train)` | learns from the training rows |
| `model.predict(X_test)` | predicts 0 or 1 for each test row |
| `accuracy_score(y_test, predictions)` | the fraction of predictions that were correct |

> **LOOK FOR**
> The accuracy is about 0.80. The baseline, always predicting "did not survive", is about 0.60. The model beats the guess.

> **REMEMBER**
> Never test a model on the rows it trained on. The test rows check whether it learned something general.

> **WATCH OUT**
> A model needs numbers. Text columns such as `Sex` must be converted first, as `Female` is above.

> **TRY IT YOURSELF**
> 1. Change `max_depth` to 1, 2, 3, 5 and 8, one at a time. Write down each accuracy. *Expected: 0.785, 0.776, 0.803, 0.803, 0.780.* Which depth is best?
> 2. Remove `Fare` from `features` and train again with `max_depth=3`. *Expected: 0.798.* Did the model get worse?
> 3. Train with only the `Female` column. *Expected: 0.785.* How close is one feature to the full model?

**Quick Check**

1. What is the target in this example?
2. Why do we split the data before training?
3. Why is the baseline needed?

---

## 4. Practical: Compare Groups, Then Change the Model

**Cell: survival by class and sex**

```python
by_class_sex = df.groupby(["Pclass", "Sex"])["Survived"].mean().unstack()
by_class_sex.plot(kind="bar", title="Survival rate by class and sex")
plt.ylabel("Survival rate")
plt.xticks(rotation=0)
plt.show()
```

**What each function and method does**

| Call | What it does |
|---|---|
| `df.groupby(["Pclass", "Sex"])["Survived"].mean()` | survival rate for each class and sex pair |
| `.unstack()` | moves `Sex` from the rows into the columns, so each class has one row |
| `by_class_sex.plot(kind="bar", ...)` | draws one bar per sex inside each class |

> **LOOK FOR**
> Women in first class survived at 0.97, and men in third class at 0.14. Sex matters a lot, and class matters too.

**Cell: add a family feature**

```python
df["Family"] = df["SibSp"] + df["Parch"] + 1
features["Family"] = df["Family"]
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.25, random_state=42)
model = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X_train, y_train)
print("accuracy with Family:", round(accuracy_score(y_test, model.predict(X_test)), 3))
```

> **TRY IT YOURSELF**
> 1. Run the practical cell. *Expected: 0.807, slightly better than 0.803.*
> 2. Set `max_depth=4` and then `max_depth=2` for the model with `Family`. *Expected: 0.812 and 0.776.* Which setting would you choose, and why?
> 3. Draw a bar chart of survival rate by `Family` size. *Expected: family size 1 gives 0.304, sizes 2 to 4 give 0.55 to 0.72.*

---

## Errors You Will Meet

| Last line of the error | Usual cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'sklearn'` | scikit-learn is not installed | run `uv add scikit-learn` |
| `ModuleNotFoundError: No module named 'matplotlib'` | matplotlib is not installed | run `uv add matplotlib` |
| `NameError: name 'df' is not defined` | the pandas cells were not run first | run the pandas notes cells, then this lecture |
| `ValueError: could not convert string to float: 'male'` | a text column was given to the model | convert it to numbers first, as `Female` does |

---

## Reference Card

| You want to... | Write |
|---|---|
| Bar chart from a result | `s.plot(kind="bar", title="...")` |
| Histogram of a column | `df["Age"].plot(kind="hist", bins=20)` |
| Label the axes | `plt.xlabel("...")`, `plt.ylabel("...")` |
| Show the chart | `plt.show()` |
| Split into train and test | `train_test_split(X, y, test_size=0.25, random_state=42)` |
| Create a model | `DecisionTreeClassifier(max_depth=3, random_state=42)` |
| Learn and predict | `model.fit(X_train, y_train)`, `model.predict(X_test)` |
| Measure accuracy | `accuracy_score(y_test, predictions)` |

---

## Knowledge Check

Answer in your own words. If you get stuck, go back to the section.

1. What does Matplotlib do, and why do we draw charts before modelling?
2. What is scikit-learn for, in one sentence?
3. What is the difference between `fit` and `predict`?
4. Why do we need a baseline to judge a model's accuracy?
5. Why do we set `random_state`?

> **GOLDEN RULE**
> Predict, run, read the result, and try a change. A model is only as good as the question you ask it.
