[CPython source code](https://github.com/python/cpython)

[Python grammer](https://github.com/python/cpython/blob/main/Grammar)

[Python objects](https://github.com/python/cpython/tree/main/Objects)


[CPython 3.6 walkthrough](https://leanpub.com/insidethepythonvirtualmachine/read)
CPython 3.11s new specializing, adaptive interpreter:
https://www.youtube.com/watch?v=shQtrn1v7sQ&ab_channel=PyConUS
https://www.youtube.com/watch?v=shQtrn1v7sQ&ab_channel=PyConUS


Understand the AST of the code:

```python
import ast, inspect, pprint

pprint.pprint(
    ast.dump(
        ast.parse(
            inspect.getsource(some_function)
        )
    )
)
```

Understand the bytecode:

```python
import dis
dis.dis(some_function)
```