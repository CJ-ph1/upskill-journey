def add(a: int, b: int) -> int:
    return a + b


def greet(name: str) -> str:
    msg = "hello, " + name
    return msg


def total(prices: list[float]) -> float:
    return sum(prices)


result: int = add(1, 2)
print(result)
