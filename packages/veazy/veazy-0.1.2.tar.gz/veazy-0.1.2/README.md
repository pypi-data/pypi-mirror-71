# Veazy
*Visualize your python code eazily*

`veazy` generates callgraphs for your python codebase by parsing the abstract syntax tree (its static, so it doesn't run your code).
Callgraphs can be convoluted, so `veazy` automagically determines a convenient complexity which you can then tweak. 

# Installation
`$ pip install veazy`

For `svg` output, you need graphviz:
`$ sudo apt install graphviz` or `conda install graphviz`.

We have tested this for unix. Will it work on Windows? We don't know!

# Usage 
`cd` into where your code lives. 
The (automatic) pruning requires the option `--root-file ROOT_FILE` (or`-r ROOT_FILE`), as in:

`veazy --root-file main.py`.

From there, you may set a relative depth with the `--complexity-offset` option (or `-c`). 
Absolute depths may be set with `--depth`. For maximum depth, do `-d -1` or `--all`. 
An example of `veazy` analysing itself:

`veazy -r main.py -c -3`
![](examples/c_minus_3.svg)

For exclusion purposes, you may specify the SRC to be included:
`veazy -r main.py tag_*.py`

## Other options
| **Option**                     | **Description** |
|--------------------------------|------|
|-r, --root-file PATH            | A top-level entry from where relative depth is determined. |
|-c, --complexity-offset INTEGER | To adjust the automatic depth. When depth is passed, this value is ignored. |
|-d, --depth INTEGER			 | Use an absolute depth. For -1, you get all, equal to the `--all` switch. |
|-a, --all 						 | Get the complete graph. It is not needed to specify a root file. |
|-o, --output-file PATH          | Write to this file. If None, svgs go to graph.svg. |
|-t, --output-type [dot\|svg]    | Output format. For svg, you need to have graphviz installed. |
|--launch, --no-launch           | Whether to open the resulting file with your default application. |
|--version                       | Show the version and exit. |
|--help                          | Help yourself and exit. |


# Thanks
The version of pyan3 used in Veazy is mirrored from https://github.com/Technologicat/pyan.

# [License](https://gitlab.com/janscholten/veazy/-/blob/master/LICENCE)
