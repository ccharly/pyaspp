# pyaspp

> THIS IS NOT A PREPROCESSOR (like cpp) WRITTEN IN PYTHON!

This said, now we can talk about `pyaspp` for real!

`pyaspp` is a preprocessor that interprets `python` and generates `cpp` directives. It runs before the C preprocessor.

Here is a little example:
```cpp
#py= cpp.define('ONE_AND_ONE', 1 + 1)

#py a_python_value = ['py', 'thon'].join()
#py= cpp.define('PYTHON', a_python_value)
```

Lets preprocess it now:
```shell
python pyaspp.py example/main.cpp
```

This will give this output:
```cpp
#define ONE_AND_ONE 2

#define PYTHON python
```
