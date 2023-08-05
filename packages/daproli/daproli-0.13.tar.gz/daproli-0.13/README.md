# daproli [![PyPI version](https://badge.fury.io/py/daproli.svg)](https://pypi.org/project/daproli/) [![Downloads](https://pepy.tech/badge/daproli)](https://pepy.tech/project/daproli)
A small data processing library that attempts to make data transformation more declarative.

## Installation

You can install daproli with PyPi:
`python -m pip install daproli`

## Examples

Let's first import daproli.

```python3
>>> import daproli as dp
```

The library provides basic data transformation methods.

```python3
>>> names = ['John', 'Susan', 'Mike']
>>> numbers = [i for i in range(10)]
>>>
>>> even_numbers = [0, 2, 4, 6, 8]
>>> odd_numbers = [1, 3, 5, 7, 9]
>>>
>>> dp.map(lambda n : n.lower(), names)
['john', 'susan', 'mike']
>>>
>>> dp.filter(lambda n : len(n) % 2 == 0, names)
['John', 'Mike']
>>> 
>>> dp.split(lambda x : x % 2 == 0, numbers)
[[1, 3, 5, 7, 9], [0, 2, 4, 6, 8]]
>>> 
>>> dp.expand(lambda x : (x, x**2), numbers)
[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]]
>>> 
>>> dp.combine(lambda x, y : (x,y), even_numbers, odd_numbers)
[(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
>>> 
>>> dp.join(lambda x, y : y-x == 3, even_numbers, odd_numbers)
[(0, 3), (2, 5), (4, 7), (6, 9)]
```

Additionally, it provides a data transformation pipeline framework.

```python3
>>> dp.Pipeline(
        dp.Splitter(lambda x: x % 2 == 1),
        dp.Multi(
            dp.Mapper(lambda x: x * 2),
            dp.Mapper(lambda x: x * 3),
        ),
        dp.Joiner(lambda x1, x2: (x1 + x2) % 5 == 0),
        dp.Filter(lambda x: sum(x) < 30),
        dp.Manipulator(sorted),
    ).transform(numbers)
[(0, 15), (4, 21), (12, 3), (16, 9)]
```

You can find more examples <a href="https://github.com/ermshaua/daproli/tree/master/daproli/examples">here</a>. 
