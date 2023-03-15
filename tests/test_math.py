from src import math_module


def test_add():
    assert math_module.add(1, 2) == 3


if __name__ == "__main__":
    test_add()
