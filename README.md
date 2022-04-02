# Dependencies

Graphviz 2.42.2 https://graphviz.org/download/

Python 3.9

Python libraries:
* python-chess 1.9.0 (https://github.com/niklasf/python-chess)
* graphviz 0.19.1 (https://github.com/xflr6/graphviz)
* Can be installed using **pip**: `$ pip install chess graphviz`


# Usage
Main source: **diagram.py**

```
$ python3 diagram.py input
```
- `input`: path to the .pgn file
- For example: `$ python3 diagram.py Nimzo-4-Bg5.pgn`

By default, the program draws from the 4th move to the 18th move. To change this, specify the command-line arguments as follows:
```
$ python3 diagram.py -s START -e END input
```
- `START`: the first move
- `END`: the last move
- For example: `$ python3 diagram.py -s 3 -e 19 Nimzo-4-Bg5.pgn`

To print full usage:
```
$ python3 diagram.py --help
```

```
usage: diagram.py [-h] [-s START] [-e END] input

Draw moves from a PGN file

positional arguments:
  input                 Input pgn file

optional arguments:
  -h, --help            show this help message and exit
  -s START, --start START
                        First move
  -e END, --end END     Last move
```

# Output

A `diagram-<input>.gv.pdf` file storing the output diagram, and a `diagram-<input>.gv.dot` file storing the diagram in [DOT](https://www.graphviz.org/doc/info/lang.html) language.
