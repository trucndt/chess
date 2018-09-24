# Dependencies
* python-chess (https://github.com/niklasf/python-chess)
* graphviz (https://github.com/xflr6/graphviz)

Can be installed using **pip**:
```
pip install python-chess graphviz 
```

# Parameters
Source code: **diagram.py**

You can change address to the input .pgn file by changing the variable **INPUTFILE** at _line 6_ 

The first and last moves to be appeared in the output diagram are defined by the variables START and END at _line 4_ and _5_, respectively.

The output file will be named as **'diagram-' + INPUTFILE** . If you wish to change this name format, it will be on _line 78_

# Run
```
$ python3 diagram.py
```

I also output to the command line the graph in [DOT](https://www.graphviz.org/doc/info/lang.html) language which can be used to change the output diagram easily.
