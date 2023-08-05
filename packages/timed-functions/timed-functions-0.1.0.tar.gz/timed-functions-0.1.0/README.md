# timed-functions

Decorator to print how long each decorated function takes to complete.

### Example

```python
@timing
def say_hello(name):
    print(f"Hello {name}")
```

Output:

```python
Hello World
@timing - 'say_hello' function took 0.023 ms
```