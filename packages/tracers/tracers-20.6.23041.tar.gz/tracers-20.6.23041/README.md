# Table of contents

- [Table of contents](#table-of-contents)
- [Project description](#project-description)
  * [Key Features](#key-features)
- [Quick Introduction](#quick-introduction)
- [Installation](#installation)
- [Examples](#examples)

# Project description

**Tracers** is an Open-Source **APM** (Application monitoring) project
that offers you zero overhead wrappers for profiling your code execution flow

```
🛈  Finished transaction: 332eeaef449841c48d5daf0d2a551fe8, 0.81 seconds

  #    Timestamp      %     Total    Nested Call Chain

     1     0.00s 100.0%     0.81s    ✓ async function_a()
     2     0.00s  12.4%     0.10s    ¦   ✓ async asyncio.tasks.sleep(delay, result=None, *, loop=None)
     3     0.10s  87.5%     0.71s    ¦   ✓ async function_b()
     4     0.10s  12.5%     0.10s    ¦   ¦   ✓ async asyncio.tasks.sleep(delay, result=None, *, loop=None)
     5     0.20s  25.0%     0.20s    ¦   ¦   ✓ async function_c()
     6     0.20s  12.5%     0.10s    ¦   ¦   ¦   ✓ async asyncio.tasks.sleep(delay, result=None, *, loop=None)
     7     0.30s  12.5%     0.10s    ¦   ¦   ¦   ✓ async function_d()
     8     0.30s  12.5%     0.10s    ¦   ¦   ¦   ¦   ✓ async asyncio.tasks.sleep(delay, result=None, *, loop=None)
     9     0.41s  12.5%     0.10s    ¦   ¦   ✓ async asyncio.tasks.sleep(delay, result=None, *, loop=None)
    10     0.51s  12.5%     0.10s    ¦   ¦   ✓ async function_d()
    11     0.51s  12.5%     0.10s    ¦   ¦   ¦   ✓ async asyncio.tasks.sleep(delay, result=None, *, loop=None)
    12     0.61s  12.4%     0.10s    ¦   ¦   ✓ async asyncio.tasks.sleep(delay, result=None, *, loop=None)
    13     0.71s  12.5%     0.10s    ¦   ¦   ✓ async function_e()
    14     0.71s  12.5%     0.10s    ¦   ¦   ¦   ✓ async asyncio.tasks.sleep(delay, result=None, *, loop=None)
```

## Key Features

- Handles **any callable** object, which includes **your own code**,
  **third party libraries**, and even the low-level **Python standard library**
- Handles [**async**](https://docs.python.org/3/library/asyncio.html) code
  **out-of-the box**, no config required
- Exposes a **high-level API**:
  - `@trace` decorator (which internally handles async/sync cases)
- It's **Thread-safe**, **Async-safe**, **Process-safe** and **Context-safe**
  - Accurate results in any scenario
  - No worries about leaking, bleeding, corrupting, or locking stuff into other
    code
- Introduces **zero overhead** in production!
  - The `@trace` decorator accepts a `do_trace` parameter
    that you can dynamically set to `True` of `False` to differentiate
    testing environments from production environments
- It's **easy to deploy**
  - Has no external dependencies
- Profiles without using dirty introspection stuff
  - The main code is just 50 lines long, pretty high level, go and read it :)

# Quick Introduction

Let's start with a very basic example:

```py
import time
from dateutil.parser import parse


def example():
    time.sleep(2.0)
    your_business_logic('Sat Oct 11')


def your_business_logic(date: str):
    parse(date)
    time.sleep(1.0)


example()
```

Tracing its flow and gathering profiling information is a matter of
decorating your functions:

```diff
--- a/examples/without_tracers.py
+++ b/examples/with_tracers.py
@@ -1,15 +1,18 @@
 import time
 from dateutil.parser import parse
+from tracers.function import trace


+@trace
 def example():
     time.sleep(2.0)
     your_business_logic('Sat Oct 11')


+@trace
 def your_business_logic(date: str):
     parse(date)
     time.sleep(1.0)


 example()
```

If you run it, all the functions you decorated will be traced
and you'll have metrics of the execution flow:

```
🛈  Finished transaction: ce72c9dbe3d64e4cb43714fb87738ac4, 3.00 seconds

  #    Timestamp      %     Total    Nested Call Chain

     1     0.00s 100.0%     3.00s    ✓ example()
     2     2.00s  33.4%     1.00s    ¦   ✓ your_business_logic(date: str)
```

From the output you can conclude:
- executing function *example* took a total of *3.0* seconds to complete
- function *example* represents *100%* of your code time
- function *example* called function: *your_business_logic*
- function *your_business_logic* took *1.0* seconds out of the *3.0* seconds
  the function *example* needed to complete
- function *your_business_logic* represents *33.4%* of your execution time
- There is *66.6%* of execution time
  that we've not instrumented... yet!

Tracing code is not limited to your own code.
You can trace any **callable object** including **third party packages**,
**Python's standard library**, and almost anything

The level of detail is up to you!


```diff
--- a/examples/with_tracers.py
+++ b/examples/with_detailed_tracers.py
@@ -1,18 +1,18 @@
 import time
 from dateutil.parser import parse
 from tracers.function import trace


 @trace
 def example():
-    time.sleep(2.0)
+    trace(time.sleep)(2.0)
     your_business_logic('Sat Oct 11')


 @trace
 def your_business_logic(date: str):
-    parse(date)
-    time.sleep(1.0)
+    trace(parse)(date)
+    trace(time.sleep)(1.0)


 example()
```

```
🛈  Finished transaction: 10b3878b12e647c1b326a9c55f954537, 3.00 seconds

  #    Timestamp      %     Total    Nested Call Chain

     1     0.00s 100.0%     3.00s    ✓ example()
     2     0.00s  66.6%     2.00s    ¦   ✓ time.sleep(...)
     3     2.00s  33.4%     1.00s    ¦   ✓ your_business_logic(date: str)
     4     2.00s   0.0%     0.00s    ¦   ¦   ✓ dateutil.parser._parser.parse(timestr, parserinfo=None, **kwargs)
     5     2.00s  33.3%     1.00s    ¦   ¦   ✓ time.sleep(...)
```

# Installation

We are hosted on **PyPI**: https://pypi.org/project/tracers

Just run: `pip install tracers`
or use the package manager you like the most

# Examples

Check them out in the
[examples](https://github.com/kamadorueda/tracers/tree/master/examples)
folder
