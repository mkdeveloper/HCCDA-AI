# Week 5 Study Guide: Build a Mart API with FastAPI and SQLModel

*Agentic AI Course | FastAPI, SQLModel and Neon*

This week you build a small mart API: a server that stores products, lets clients create, read, change and delete them, and protects the stock with a sell route. You test everything in Swagger UI, the page FastAPI builds for you. Your data is stored in Neon, a cloud Postgres database, from the start.

All code in this guide is fully typed. Every function has parameter and return type hints, and you can check them with mypy (see Part 8).

## Routes

| Route | What it does | Success | Error |
|---|---|---|---|
| `POST /products` | create a product | 201 | 422 if the data is wrong |
| `GET /products` | list products | 200 | none |
| `GET /products/cheap` | list products at or below a price | 200 | 422 if the price is invalid |
| `GET /products/{product_id}` | read one product | 200 | 404 if it does not exist |
| `PATCH /products/{product_id}` | change name or price | 200 | 404 |
| `DELETE /products/{product_id}` | remove a product | 200 | 404 |
| `POST /products/{product_id}/sell?quantity=n` | reduce stock | 200 | 409 if not enough stock |

You build the `GET /products/cheap` route as a challenge in Part 6.

We install packages in stages. You only install a package in the part that first needs it, so you always know why it is in your project.

| Part | Install | Why |
|---|---|---|
| 1 | `fastapi[standard]` | the web framework and Swagger UI |
| 3 | `sqlmodel` | the table and data classes |
| 4 | `psycopg[binary]` | the Postgres driver, needed to talk to Neon |
| 4 | `python-dotenv` | reads your `.env` file so the address is loaded automatically |

## Setup

You already have uv and Python. Create the project with `uv init`. It creates the `src` layout shown below, so your code goes in the `src/mart_api` folder, not in the project root:

```bash
uv --version
uv init mart_api
cd mart_api
```

Project structure:

```text
mart_api/
├── pyproject.toml          settings, packages, and where the app is
├── README.md, .gitignore, .python-version
└── src/
    └── mart_api/           <- your code goes here
        ├── __init__.py     empty (uv put a placeholder here: delete it)
        ├── main.py         the routes (Parts 1, 5, 6, 7)
        ├── models.py       the product classes (Part 3)
        └── database.py     the connection (Part 4)
```

> **Note:** Keep the quotes when you type `"fastapi[standard]"` in Part 1. Some terminals read the square brackets as a pattern if the quotes are missing.

---

## Part 1: Your First FastAPI App

By the end of this part you can:

- Explain what a decorator does, using plain Python first.
- Explain each line of a small FastAPI app, including its imports.
- Start the server and test a route in Swagger UI.

### Concept

A decorator is a function that takes another function and returns a new one. The `@` line is a short way to write that step. Nothing in FastAPI is special here: it is Python you already know, applied to functions.

### Example: Step 1, the same idea without the `@` symbol

`decorator_intro.py`

```python
def shout(func):          # 1. takes a function as its input
    def wrapper():        # 2. a new function that wraps the old one
        result = func()   # 3. call the original function
        return result.upper()  # 4. change what it returns
    return wrapper        # 5. hand back the new function


def greet():
    return "hello"


greet = shout(greet)  # 6. replace greet with the wrapped version
print(greet())
```

Output:

```text
HELLO
```

Run it with `python decorator_intro.py`. It prints `HELLO`, although `greet` returns `"hello"`. Line 6 did the work: `shout` received `greet`, and the name `greet` now refers to the wrapper.

### Example: Step 2, the same thing with the `@` symbol

`decorator_at.py`

```python
def shout(func):
    def wrapper():
        return func().upper()
    return wrapper


@shout  # same as: wave = shout(wave)
def wave():
    return "bye"


print(wave())
```

Output:

```text
BYE
```

The `@shout` line sits directly above `def wave()`. It means the same as line 6 in Step 1. The `@` is syntax only, so the function is still a normal function.

### Example: Step 3, the pattern FastAPI uses

`@app.get("/")` looks like magic, but it does two simple things. It saves your function under a path, and it returns your function unchanged. Here is a tiny version of that idea:

`route_registry.py`

```python
routes = {}  # a place to remember the routes


def get(path):             # takes the path, returns a decorator
    def register(func):    # the decorator: takes the function
        routes[path] = func  # remember the function under its path
        return func          # give it back unchanged
    return register


@get("/")  # the path goes in parentheses, like @app.get("/")
def home():
    return {"message": "Hello, mart"}


print(routes)
print(routes["/"]())
```

Output:

```text
{'/': <function home at 0x7fab33bfcf40>}
{'message': 'Hello, mart'}
```

Real FastAPI does more work inside `register`: it reads your type hints and builds the documentation shown in Swagger UI. The idea is the same.

> **Tip:** A decorator with parentheses, like `@get("/")`, is a function that returns a decorator. That is why there are two levels: `get("/")` runs first, and its result is applied to `home`.

### Your turn

Change `shout` so that `wave` returns the text in capitals and ends with `!`. Predict the output before you run it.

### Checkpoint

1. In `greet = shout(greet)`, what does `shout` receive and what does it return?
2. Why does `@shout` above `def wave():` need no extra call like `wave = shout(wave)`?
3. In `@get("/")`, which runs first: `get("/")` or `register(home)`?

### How Python finds your code: imports

An import loads code from another file or package. Python looks in the folder where you start the program. That is why the commands in this guide always run from the `mart_api` folder.

| Line | What Python does |
|---|---|
| `import os` | loads the standard library module `os`, which ships with Python |
| `from fastapi import FastAPI` | loads the `fastapi` package from `.venv`, then takes out the name `FastAPI` |
| `from mart_api.models import Product` | loads `models.py` from the `mart_api` package and takes out the name `Product` |

Nothing here is automatic. FastAPI does not guess what you meant. The name you import is the name you use, and `uv add` only installs packages; it does not change your imports.

### Install FastAPI

```bash
uv add "fastapi[standard]"
```

Then add two lines at the end of `pyproject.toml`. They tell FastAPI where your app is. The format is the same `file:name` pattern you used for `[project.scripts]` in the uv guide. Here it means: the package `mart_api`, the file `main.py` inside it, and the variable `app`:

`pyproject.toml` (add this)

```toml
[tool.fastapi]
entrypoint = "mart_api.main:app"
```

### Example: your first app, `src/mart_api/main.py`

Delete the placeholder code in `src/mart_api/__init__.py`, leaving that file empty. Then create `main.py` inside `src/mart_api`, next to `__init__.py`, with this content:

`src/mart_api/main.py`

```python
from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Hello, mart"}
```

Open Swagger UI and run `GET /`. The response body is:

```json
{"message": "Hello, mart"}
```

| Line | What it does |
|---|---|
| `from fastapi import FastAPI` | loads the `FastAPI` class from the installed package |
| `app: FastAPI = FastAPI()` | creates one app object. It holds every route. `uv run` finds it by the name `app` |
| `@app.get("/")` | decorator: stores `home` as the handler for GET requests to `/` |
| `def home() -> dict[str, str]:` | the function that answers the request. The return type says it gives a dictionary of strings |
| `return {...}` | FastAPI turns this dictionary into JSON for the response |

Start the server. Leave this terminal open while you work:

```bash
uv run fastapi dev
```

FastAPI reads `[tool.fastapi]`, imports `main`, and takes the `app` object from it. The message `Application startup complete` means the server is ready.

### Test it in Swagger UI

1. Open `http://127.0.0.1:8000/docs` in your browser. This is Swagger UI.
2. Click the `GET /` row to open it.
3. Press **Try it out**, then **Execute**.
4. Read two parts of the answer: **Response code** (should be 200) and **Response body** (should show `{"message": "Hello, mart"}`).

### Your turn

Add a route `/about` that returns `{"shop": "My Mart"}`. Save `main.py`, wait for the server to reload, and check that Swagger UI shows both routes.

### Challenge

Add a route `/version` that returns two keys: `name` (your name) and `today` (the date as text).

### Checkpoint

1. Which line of `main.py` creates the object that `fastapi dev` serves?
2. What does `entrypoint = "mart_api.main:app"` tell FastAPI?
3. In Swagger UI, where do you read the status code of a response?

---

## Part 2: Type Hints Do the Checking

### Concept

A type hint such as `number: int` is not just a label. FastAPI reads it. It converts the text in the request to that type, and if the conversion fails, it sends back a 422 error without running your function.

### Example

Add to `main.py`, below `home`:

```python
@app.get("/double/{number}")
def double(number: int) -> dict[str, int]:
    return {"result": number * 2}
```

The `{number}` in the path must have the same name as the parameter. In Swagger UI, open `GET /double/{number}`, type `4`, and press **Execute**. The response body is `{"result": 8}`.

Now type `abc` instead of `4` and press **Execute** again. Swagger UI shows the Response code `422` and this response body:

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "number"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "abc"
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `type` | the kind of error (here: text that is not a whole number) |
| `loc` | where the bad value came from: `path` (the URL), `body` (JSON) or `query` |
| `msg` | a sentence for humans. Wording can vary between FastAPI versions and tools |
| `input` | the value that was refused |

> **Note:** Some tools show a friendlier message, but the underlying answer is the same JSON body. Trust the Response body field in Swagger UI. If the wording on your screen differs, check that the `loc` field names the same parameter.

> **Tip:** A 422 is good news. The check worked, and bad data never reached your code.

A third response you will meet is **405 Method Not Allowed**. That means the URL exists, but not with that method. For example, `GET /products/1/sell` returns 405, because the route is declared with `POST`.

### Your turn

Add `/square/{number}` returning `number * number`, with the same typed signature as `double`. Test `/square/7` and `/square/seven` in Swagger UI, and write down both status codes.

### Checkpoint

1. What does FastAPI do with the text `"4"` in `/double/4` before your function runs?
2. Which field in the 422 body tells you which parameter was wrong?
3. What status code means the URL exists but the method is wrong?

---

## Part 3: SQLModel, One Class With Two Jobs

### Concept

SQLModel combines Pydantic models (the checking you saw in Part 2) with the database layer, so one class can do both jobs. A class with `table=True` is a database table and a Python class: each object of it is one row.

Think of the `product` table as a spreadsheet. Each line in the spreadsheet is one row, and each row holds one product. A `Product` object is one of those lines, written as Python:

```python
pen = Product(name="Pen", price=1.5, stock=10)
session.add(pen)
session.commit()
```

After the commit, the database stores `pen` as one row:

| id | name | price | stock |
|----|------|-------|-------|
| 1  | Pen  | 1.5   | 10    |

Creating a second `Product`, such as a notebook, and saving it adds a second row. Each object is one row, and each row is one object.

Install it now. This is the first time the project needs it:

```bash
uv add sqlmodel
```

A table class alone should not be sent over the API. For example, a client must not choose the `id`. So we use several classes that share their fields:

| Class | Purpose | Fields |
|---|---|---|
| `ProductBase` | the fields every version shares | `name`, `price`, `stock` |
| `Product` | the table (`table=True`); the database fills in `id` | all of the above, plus `id` |
| `ProductCreate` | what a client sends to create a product | `name`, `price`, `stock` |
| `ProductPublic` | what the API returns (`id` always present) | all of the above, plus `id` |
| `ProductUpdate` | what a client sends to change a product | every field optional |

### Example

`src/mart_api/models.py`

```python
from sqlmodel import Field, SQLModel


class ProductBase(SQLModel):
    name: str = Field(index=True)
    price: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)


class Product(ProductBase, table=True):
    # the table: the database fills in id
    id: int | None = Field(default=None, primary_key=True)


class ProductCreate(ProductBase):
    # what the client sends to create a product
    pass


class ProductPublic(ProductBase):
    # what the API returns: id is always present
    id: int


class ProductUpdate(SQLModel):
    # every field optional: send only what changes
    name: str | None = None
    price: float | None = Field(default=None, gt=0)
```

| Line | What it does |
|---|---|
| `class ProductBase(SQLModel):` | a class that inherits the checking of SQLModel |
| `price: float = Field(gt=0)` | a float, and greater than zero. Otherwise 422 |
| `stock: int = Field(default=0, ge=0)` | an integer, zero or more. Missing means 0 |
| `class Product(ProductBase, table=True):` | inherits the fields, and makes a database table |
| `id: int \| None = Field(default=None, ...)` | `None` until the database gives an id |

### Checkpoint

1. What does `table=True` change about the class?
2. Why does `ProductCreate` have no `id` field?
3. Which class would a PATCH request use, and why does every field have a default?

---

## Part 4: Neon Postgres and Sessions

### Concept

Neon is a hosted Postgres database. Your app connects to it with an address (a connection string) that includes a username, a password, and the database name. You will do three things: create the database, give the address to the app, and write `database.py`.

| Part of the address | Meaning |
|---|---|
| `postgresql://` | the Postgres format. Neon gives you this form |
| `postgresql+psycopg://` | the same format with the driver named. SQLModel needs this form |
| `psycopg` | the driver (version 3) that talks to Postgres |
| `sslmode=require` | the connection is encrypted. Neon requires it, and its string has it |

### Step 1: create the database

1. Sign up at neon.com and create a project.
2. Open the project and press **Connect**. Copy the connection string. It starts with `postgresql://`.
3. Treat the string as a password. Never paste it into a shared file, a screenshot, or Git.

### Step 2: install the packages and create the `.env` file

Install the driver and the loader for `.env` files. This is the first time the project needs them:

```bash
uv add "psycopg[binary]" python-dotenv
```

The app reads the connection string from a `.env` file in the project root:

`.env`

```text
DATABASE_URL=postgresql://user:password@ep-xxxx.neon.tech/neondb?sslmode=require
```

### Step 3: write `database.py`

`src/mart_api/database.py`

```python
import os
from collections.abc import Iterator
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from . import models  # noqa: F401  registers the table classes with SQLModel


def make_url(raw: str) -> str:
    # Neon gives "postgresql://..."; SQLModel needs the driver named explicitly
    if raw.startswith("postgresql://"):
        return raw.replace("postgresql://", "postgresql+psycopg://", 1)
    return raw


load_dotenv()  # reads the .env file in the project root into the environment

raw_url: str | None = os.environ.get("DATABASE_URL")
if not raw_url:
    raise RuntimeError("Set DATABASE_URL to your Neon connection string first")

DATABASE_URL: str = make_url(raw_url)  # after the check above, raw_url is narrowed to str
engine = create_engine(DATABASE_URL, pool_recycle=300)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    # a generator: yields one Session, then closes it after the request
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
```

| Line | What it does |
|---|---|
| `from . import models` | loads `models.py`, which defines the table classes. This must happen before the tables are created (see Part 5) |
| `load_dotenv()` | copies the values from the `.env` file into the environment. Does nothing if the file is missing |
| `raw_url: str \| None = os.environ.get(...)` | reads the address. `get` returns `None` when the variable is missing, so the type says so |
| `if not raw_url: raise RuntimeError` | stops with a clear message if you forgot to set it. After this line, the type checker knows `raw_url` is a `str` |
| `engine = create_engine(...)` | made once, when the module loads. `pool_recycle=300` replaces any pooled connection older than 5 minutes, before Neon's idle scale-down can close it |
| `def get_session() -> Iterator[Session]:` | a generator function that yields one session. `Iterator[Session]` is the return type of a generator that yields sessions |
| `with Session(engine) as session:` | opens the session, and closes it when the block ends |
| `yield session` | hands the session to the caller, then pauses |
| `SessionDep = Annotated[...]` | a short name: "a `Session` that FastAPI gets from `get_session`" |

#### How `SessionDep` works

`SessionDep = Annotated[Session, Depends(get_session)]` is a shortcut that combines two ideas.

1. **`Annotated` attaches a note to a type.** `Annotated[X, Y]` means "this is type `X`, with the note `Y` attached." The type checker only sees `Session`. FastAPI reads the note, `Depends(get_session)`, and uses it to find where the value comes from. Writing the note once lets every route reuse it.

2. **A route asks for the dependency by type.** When a route has `session: SessionDep` in its signature, FastAPI sees the note and knows the session must come from `get_session`.

Then, for each request (not once at startup):

- FastAPI calls `get_session()`. The code before `yield` runs and opens the session.
- The value after `yield` is passed into the route's `session` parameter, so the route runs with a working session.
- When the route returns, FastAPI resumes `get_session` after its `yield`. The `with` block ends, and the session closes, even if the route raised an error.

You never call `get_session` or `close()` yourself. Without this pattern, every route would need its own `with Session(engine) as session:` block, and it would be easy to forget the cleanup. Routes also do not need to know how the session is created, which makes it possible to swap in a test database later with `app.dependency_overrides`.

> **Summary:** A route asks for `session: SessionDep`. FastAPI calls `get_session` for that request, passes in the session it yields, and closes it after the route ends. You write the route as if the session were already there.

> **Note:** `Annotated` and `Depends` are imports like any other. FastAPI only uses them because the route's signature names them.

> **Warning:** Never write the password into `database.py` or any other file. The `.env` file keeps it out of the code, and the `.gitignore` line keeps it out of Git.

### Checkpoint

1. What is the difference between an engine and a session?
2. What does `yield` do in `get_session`, and when does the session close?
3. Who calls `get_session` in the route `create_product(product: ProductCreate, session: SessionDep)`?
4. Why does the code print `postgresql+psycopg://` when you set `postgresql://`?

---

## Part 5: The App Creates Its Tables When It Starts

### Concept

A table class does not create a table by itself. The app has to ask the database when it starts. FastAPI does this with a lifespan function. The function is marked with `@asynccontextmanager`, a decorator from Python's standard library that works the same way as the decorators in Part 1. The code before `yield` runs at startup, and the code after `yield` runs at shutdown.

The type `AsyncIterator[None]` says the function is an async generator that yields nothing useful: it only marks the point where the app is running.

### Example

Replace `src/mart_api/main.py` with this skeleton. It has the lifespan and the app, but no routes yet:

`src/mart_api/main.py` (skeleton)

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from mart_api.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    create_db_and_tables()  # runs once, before the first request
    yield


app: FastAPI = FastAPI(title="Mart API", lifespan=lifespan)
```

Restart `uv run fastapi dev`. The table now exists in Neon. To check, open the SQL Editor in the Neon console and run:

```sql
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
```

You should see `product` in the result.

### Why `database.py` imports the models

`create_db_and_tables()` creates tables only for classes that have already been defined. A class with `table=True` is defined when Python loads its file. The lifespan runs after the app starts, so if nothing has loaded `models.py` by then, `Product` is never defined, and its table is silently skipped. No error is shown.

The line `from . import models` in `database.py` makes sure the model file is loaded whenever the database module is loaded. Keep it even after you add routes. Routes may change, but the tables should always be created.

If you want to see the effect, comment out that import, delete the `product` table in the Neon SQL Editor, and restart the server. The table will not come back. Uncomment the import and restart, and it will.

> **Note:** The older `@app.on_event("startup")` style still appears in some tutorials. FastAPI marks it deprecated, so this guide does not use it.

> **Warning:** The app creates a table only if it is missing. If you later change a model (for example add a field), the old table stays as it was. Run `DROP TABLE product;` in the Neon SQL Editor, then restart. This deletes every product, so do it only while you are learning.

### Checkpoint

1. When does `create_db_and_tables()` run?
2. Why does an existing table not change when you edit the model?

---

## Part 6: Create, Read, Update and Delete

### Concept

Every database app does four things: CRUD. HTTP has a method for each, and FastAPI has a decorator for each. You will add one route at a time to `main.py` and test each one in Swagger UI before moving on.

| CRUD | HTTP method | Decorator | Typical success |
|---|---|---|---|
| Create | POST | `@app.post` | 201 Created |
| Read | GET | `@app.get` | 200 OK |
| Update | PATCH | `@app.patch` | 200 OK |
| Delete | DELETE | `@app.delete` | 200 OK |

Before adding the routes, make the top of `main.py` look like this. These are all the names the routes below use. Replace the old import lines with this block:

`src/mart_api/main.py` (the top of the file)

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlmodel import col, select

from mart_api.database import SessionDep, create_db_and_tables
from mart_api.models import Product, ProductCreate, ProductPublic, ProductUpdate
```

> **Note:** Keep the `lifespan` function and the `app` line from Part 5, and add each route below them. Delete the `home` route from Part 1 and the `double` route from Part 2, because the mart API does not use them.

### 6a: Create a product

`main.py` (add below the lifespan)

```python
@app.post("/products", response_model=ProductPublic, status_code=201)
def create_product(product: ProductCreate, session: SessionDep) -> Product:
    db_product: Product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product
```

| Part | What it does |
|---|---|
| `product: ProductCreate` | the body the client sends. It cannot set `id` |
| `session: SessionDep` | FastAPI gives this route a session from `get_session` |
| `-> Product` | the function returns a table row |
| `Product.model_validate(...)` | turns the checked input into a table row |
| `session.add` / `commit` / `refresh` | save the row, then read back the `id` the database gave it |
| `response_model=ProductPublic` | controls the output: the answer always has an `id` |
| `status_code=201` | Swagger UI shows 201 Created on success |

> **Note:** The return annotation (`-> Product`) describes what the function really returns. The `response_model` decides what the client sees. Here the client sees a `ProductPublic`, which has the `id` filled in, so the two work together.

### Your turn

In Swagger UI, open `POST /products`, press **Try it out**, and send a notebook with price `4.5` and stock `50`. Expect 201 and an `id`. Then send price `-1` and read the 422 body.

### 6b: List products

`main.py` (add below `create_product`)

```python
@app.get("/products", response_model=list[ProductPublic])
def list_products(session: SessionDep) -> list[Product]:
    products = session.exec(select(Product)).all()
    return list(products)
```

This route has no query parameters. It returns every product in the table, so keep the table small while you test.

### 6c: Read one product

`main.py` (add below `list_products`)

```python
@app.get("/products/{product_id}", response_model=ProductPublic)
def get_product(product_id: int, session: SessionDep) -> Product:
    product: Product | None = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
```

`session.get` returns the row, or `None` when there is none. The type `Product | None` says exactly that, and the `if not product:` line turns the `None` case into a clear 404. Without it, the code would crash on the next line.

### 6d: Change a product

`main.py` (add below `get_product`)

```python
@app.patch("/products/{product_id}", response_model=ProductPublic)
def update_product(
    product_id: int,
    update: ProductUpdate,
    session: SessionDep,
) -> Product:
    product: Product | None = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.sqlmodel_update(update.model_dump(exclude_unset=True))
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
```

`exclude_unset=True` keeps only the fields the client actually sent. In Swagger UI, send `{"price": 5}` and the name stays the same.

> **Warning:** PATCH changes the fields you send. PUT means "replace the whole item". Mixing them up can erase fields the client did not mean to change.

### 6e: Delete a product

`main.py` (add below `update_product`)

```python
@app.delete("/products/{product_id}")
def delete_product(product_id: int, session: SessionDep) -> dict[str, bool]:
    product: Product | None = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {"ok": True}
```

### Challenge

Add `GET /products/cheap?max_price=` that lists products whose price is at most `max_price`. Put it **above** `/products/{product_id}`. Predict what happens to `/products/cheap` if you put it below, then test it.

A typed solution:

```python
@app.get("/products/cheap", response_model=list[ProductPublic])
def list_cheap_products(
    session: SessionDep,
    max_price: float,
) -> list[Product]:
    statement = select(Product).where(col(Product.price) <= max_price)
    return list(session.exec(statement).all())
```

> **Note:** `col(Product.price)` tells the type checker that `Product.price` is a database column, so `<=` builds a SQL condition instead of a plain Python boolean. Use `col()` whenever you compare a table field inside `where()`.

### Checkpoint

1. Which model class does POST use, and why not the table class?
2. What does `exclude_unset=True` do in the PATCH route?
3. Which line returns the 404, and what does Swagger UI show for it?

---

## Part 7: The Sell Route, Protecting the Stock

### Concept

This is the encapsulation idea from the OOP guide, applied to an API: stock goes down through one route, and that route checks the rule before it changes anything. `ProductUpdate` has no `stock` field, so PATCH cannot change stock at all.

### Example

`main.py` (add below `delete_product`)

```python
@app.post("/products/{product_id}/sell", response_model=ProductPublic)
def sell_product(
    product_id: int,
    session: SessionDep,
    quantity: int,
) -> Product:
    if quantity <= 0:
        raise HTTPException(status_code=422, detail="Quantity must be above zero")
    product: Product | None = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if quantity > product.stock:
        raise HTTPException(
            status_code=409,
            detail=f"Only {product.stock} of {product.name} left",
        )
    product.stock -= quantity
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
```

- `quantity: int` is a query parameter. FastAPI reads it from the URL, so `?quantity=3` sets it to 3.
- **409 Conflict** means the request is valid, but it conflicts with the stored state: not enough stock. Use 422 for bad input, and 409 for a rule that depends on the data.
- The check comes before the change, so a refused sale leaves the stock untouched.

### Your turn

Create a product with stock `5`. In Swagger UI, sell `3`, then sell `3` again. Write down both status codes and the message from the second one.

### Challenge

Add `POST /products/{product_id}/restock?quantity=` that adds stock and refuses zero or negative quantities. Hint: copy the sell route and change the operator.

### Checkpoint

1. Why must the check come before `product.stock -= quantity`?
2. What is the difference between a 422 and a 409 response?

---

## Part 8: Practice: Build It Again Alone

### Project

Close this guide and build the mart API in an empty folder. Use the checklist, and look back at a part only when a check fails.

1. `uv init mart_api`. Install `fastapi[standard]`, then add the `[tool.fastapi]` entrypoint at the end of `pyproject.toml`.
2. Empty the placeholder in `src/mart_api/__init__.py`, then create `main.py` with the home route. Start the server, and test it in Swagger UI.
3. Install `sqlmodel`. Write `src/mart_api/models.py` with five classes. Check that the file has no syntax errors.
4. Install `psycopg[binary]`. Write `src/mart_api/database.py`. Check that the file has no syntax errors.
5. Replace `main.py` with the lifespan skeleton. Start the server and find the `product` table in the Neon SQL Editor.
6. Add the five CRUD routes one at a time. Test each in Swagger UI before the next.
7. Add the sell route. Check that the 409 message is readable.
8. Create a product, stop the server, start it again, and read it back. It must still be there.

### Challenge: extensions (choose one)

- **Search:** `GET /products?name=` returns products whose name contains the text.
- **Restock:** the route from Part 7.
- **Category:** add `category: str` to `ProductBase`, drop the table in the Neon SQL Editor, and test in Swagger UI.

### Troubleshooting

| What you see | Likely cause | Fix |
|---|---|---|
| `RuntimeError: Set DATABASE_URL...` | `.env` missing, misnamed, in the wrong folder, or without a `DATABASE_URL=` line | fix the file in the project root, then retry |
| `ModuleNotFoundError: No module named 'sqlmodel'` | Part 3 install not done | run `uv add sqlmodel` |
| `ModuleNotFoundError: No module named 'psycopg'` | Part 4 install not done | run `uv add "psycopg[binary]"` |
| `ModuleNotFoundError: No module named 'mart_api'` | file is outside `src/mart_api`, or wrong folder | `cd mart_api`, and check the file is in `src/mart_api` |
| `Could not import module "main"` | entrypoint wrong, or wrong folder | check `entrypoint = "mart_api.main:app"` |
| `relation "product" does not exist` | lifespan did not run | check the server log at startup for errors |
| `password authentication failed` | old or wrong password | copy the connection string again from Neon |
| SSL error | `sslmode=require` missing | keep the whole string from Neon, unchanged |
| `ImportError: cannot import name 'Produc'` | misspelled name in an import line | match the spelling of the class in `models.py` |
| `ModuleNotFoundError: No module named 'mart_api.mdoels'` | misspelled file name in an import | the file is `models.py`; match it exactly |
| HTTP 405 Method Not Allowed | the route exists, but not for that method | check the decorator: `post`, `get`, `patch` or `delete` |
| HTTP 422 Unprocessable Entity | the request data is the wrong type or missing | read the `loc` and `msg` fields in the response body |
| HTTP 409 Conflict (sell route) | valid request, but not enough stock | this is correct behaviour; sell a smaller quantity |

### Reference card

| You want to... | Write |
|---|---|
| Create the app | `app: FastAPI = FastAPI(lifespan=lifespan)` |
| Make a route | `@app.get("/products/{product_id}")` |
| Read the body | `def create(product: ProductCreate) -> Product:` |
| Query parameter | `quantity: int` (FastAPI reads it from the URL) |
| Check a value | `Field(gt=0)`, `Field(ge=0)`, `Field(index=True)` |
| Get a session | `def route(session: SessionDep) -> ...:` |
| Get one row | `product: Product \| None = session.get(Product, product_id)` |
| Run a query | `session.exec(select(Product)).all()` |
| Compare a column | `where(col(Product.price) <= max_price)` |
| Save a new row | `session.add(x); session.commit(); session.refresh(x)` |
| Return 404 | `raise HTTPException(status_code=404, detail="...")` |
| Start the server | `uv run fastapi dev` |

---

## Checkpoint Answers

Try each checkpoint first, then compare. Your wording can differ; the idea should match.

**Part 1 (decorators)**

1. `shout` receives `greet` (a function) and returns `wrapper`, a new function.
2. It does not need it: `@shout` does that step. It means `wave = shout(wave)`.
3. `get("/")` runs first and returns `register`. Then `register(home)` runs.

**Part 1 (imports and first app)**

1. `app: FastAPI = FastAPI()`.
2. It tells FastAPI to load `mart_api/main.py` and use the variable `app` inside it.
3. In the **Response code** field of the response.

**Part 2**

1. It converts the text to an `int`, so the function receives the number `4`.
2. `loc` names the parameter (its location is `path`, `query` or `body`).
3. 405 Method Not Allowed.

**Part 3**

1. It makes the class a database table. Each object becomes one row.
2. The client must not choose the `id`; the database creates it.
3. `ProductUpdate`. Every field has a default so a PATCH can send only the fields it changes.

**Part 4**

1. The engine holds the connection and is made once. A session is one unit of work on top of it.
2. It hands the session out and pauses. The session closes when the request finishes.
3. FastAPI does, because of `Depends(get_session)` in `SessionDep`.
4. `make_url` changes the prefix to `postgresql+psycopg://`, which names the psycopg 3 driver for SQLModel.

**Part 5**

1. At startup, before the first request. The code after `yield` runs at shutdown.
2. SQLModel creates a table only when it is missing, so an existing table keeps its old columns.

**Part 6**

1. `ProductCreate`, because the client must not send an `id`. The table class is for the database.
2. It keeps only the fields the client sent, so missing fields are not overwritten.
3. The `if not product:` line returns 404; Swagger UI shows the code 404 and the detail text.

**Part 7**

1. So a refused sale leaves the stock unchanged.
2. 422 means the input is invalid. 409 means the input is valid, but the stored stock does not allow it.
