Concurrent.futures 101
================================
Overview of a handy python module
----------------------------------

Python usually gets a bad rep because "it's slow".  
While this might be generally true, there is nowadays
a plethora of tools and techniques that help with improving
python's speed.

`concurrent.futures` is a module of the standard
library that provides a high-level API for running
asynchronous code using threads or processes.

This tutorial makes a case for when it can come
in handy for things such as data processing or
web applications, while briefly
exploring better alternatives for specific use cases.

## Structure of the repo

All important files are in `/notebooks/`.
The slides are `cfintro.ipynb` and the visualization
notebook is `visualization.ipynb` (duh).
`quick-dask.ipynb` is a quick and not very well documented
demonstration of `dask distributed` on a local machine.

## To display the slides

```
jupyter-nbconvert ./notebooks/cf-intro.ipynb --to slides --post serve
```
