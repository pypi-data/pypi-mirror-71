# Thread Wrapper Class

<badges>[![version](https://img.shields.io/pypi/v/threadwrapper.svg)](https://pypi.org/project/threadwrapper/)
[![license](https://img.shields.io/pypi/l/threadwrapper.svg)](https://pypi.org/project/threadwrapper/)
[![pyversions](https://img.shields.io/pypi/pyversions/threadwrapper.svg)](https://pypi.org/project/threadwrapper/)  
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>Gather results from multiple threads seamlessly.</i>

# Hierarchy

```
threadwrapper
'---- ThreadWrapper()
    |---- add()
    '---- wait()
```

# Example

## python
```python
from threadwrapper import *
from omnitools import def_template
def a(b, c=None):
    return f"{b}, {c}"
tw = ThreadWrapper(threading.Semaphore(1))
result = {}
for i in range(10):
    # def_template(_def, *args, **kwargs)() is same as
    # _def(*args, **kwargs)
    tw.add(job=def_template(a, i**2, c=i**3), result=result, key=i)
tw.wait()
print(result)
# {0: '0, 0', 1: '1, 1', 2: '4, 8', 3: '9, 27', 4: '16, 64', 5: '25, 125', 6: '36, 216', 7: '49, 343', 8: '64, 512', 9: '81, 729'}
```
