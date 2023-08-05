# Ipo

Infix piping operator for Python. Iterator-native decluttering of your code.

## Demo

```python
from functools import partial as p
from ipo import ipo, head


# Ipo makes data flows much easier to follow.
ipo([5, 2, 3, 1, 4]) | sorted              | list | print  # [1, 2, 3, 4, 5]
ipo([5, 2, 3, 1, 4]) | p(head, 3)          | list | print  # [5, 2, 3]
ipo([5, 2, 3, 1, 4]) | sorted | p(head, 3) | list | print  # [1, 2, 3]
ipo([5, 2, 3, 1, 4]) | p(head, 3) | sorted | list | print  # [2, 3, 5]

# Much more readable than the original!
#   print(list(sorted(itertools.islice([5, 2, 3, 1, 4], 3))))
```

```python
from functools import partial as p
from itertools import starmap
from ipo import from_csv, skip, to_csv, before, write

# Ipo is ideally suited for working with CSV data.
ipo("""
#Voltage,Current
12,1
8,2
220,6
""".strip().split()) | from_csv | p(skip, 1) | \
	p(starmap, lambda v, a: (v, a, float(v) * float(a))) | \
	to_csv | p(before, ["#Voltage,Current,Power"]) | write
# #Voltage,Current,Power
# 12,1,12.0
# 8,2,16.0
# 220,6,1320.0
```

```python
from functools import partial as p
from ipo import read, write

# Most ipo chains that work over iterable data are lazy by default. You can load huge files,
# process them and write the results to another file.
with open("bigfile.txt") as f_in, open("processed.txt") as f_out:
	read(file=f_in) | p(map, some_preprocessing) | \
	p(map, some_advanced_function) | \
	p(map, some_formatting) | p(write, file=f_out)
```

## Inspiration

Inspired by but not based on

* https://pypi.org/project/pipe/
* https://arvindn.livejournal.com/68137.html

## Development
To create a virtualenv and install the dependencies in it:
```
tools/create_venv.py
```

Activate the virtualenv with `source venv/bin/activate`.

Important: make sure the virtualenv is activated when you are experimenting with `ipo`, otherwise
your global `ipo` installation may be used.
