# endless-sky-parse

A working, tested Python conversion of the C++ parser for Endless Sky DataFiles

## How to install

```console
$ pip install endless-sky-parse
```

## How to use

```python
from endless_sky.datafile import DataFile

f = DataFile("/usr/share/games/endless-sky/data/human/ships.txt")
it = f.root.filter(["ship", "Blackbird"])
ship = next(it)
ship.children[0]
# DataNode(tokens=['sprite', 'ship/blackbird'], children=[])
next(ship.filter_first("description")).tokens[1][:80]
# 'The Tarazed Blackbird is a high-class passenger transport, designed to move larg'
```


## Development


```console
$ python -m venv venv && . venv/bin/activate
$ pip install -r dev_requirements.txt
```

Run tests with

```console
$ python setup.py test
```

