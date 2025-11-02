import random
from fastmcp import FastMCP

app = FastMCP(name="example", version="1.0.0")

@app.tool()
def roll_dice(sides: int = 1) -> list[int]:
    """Roll a dice with a given number of sides"""
    return [random.randint(1, sides) for _ in range(sides)]

@app.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

if __name__ == "__main__":
    app.run()