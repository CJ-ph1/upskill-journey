import os                                  # ❌ Ruff: unused import (F401)
import sys                                 # ❌ Ruff: unused import (F401)
from typing import List


def add( a:int,b:int )->int:return a-b     # ❌ Black: bad spacing  ❌ logic bug (subtraction in `add`)


def greet(name):                            # ❌ MyPy (strict): missing annotations
    msg = "hello, " + name
    extra = 42                              # ❌ Ruff: unused variable (F841)
    return msg


def total(prices: List[float]) -> float:    # ❌ Ruff (UP006): use built-in `list[float]` on py3.9+
    return sum(prices)


# Demonstration of a type error MyPy will catch
result: int = add("1", "2")                 # ❌ MyPy: str passed where int expected
print(result)
