# timed-functions

Decorator to print how long each decorated function takes to complete.

### How to use

```python
from timed_functions import timing

@timing
def say_hello(name):
    print(f"Hello {name}")
```

Output:

```python
Hello World
@timing - 'say_hello' function took 0.023 ms
```

### How to deploy

```
python3 -m pip install --user --upgrade setuptools wheel
python3 -m pip install --user --upgrade twine

rm -rf build dist timed_functions.egg-info
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```