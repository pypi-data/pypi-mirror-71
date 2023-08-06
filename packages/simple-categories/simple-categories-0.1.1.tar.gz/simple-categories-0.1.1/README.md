Reads lines from a plaintext file, separated by categories.

To use use it, install the package and import on your project with

    import catlist

Then read a file with

    categories = catlist.catlist(file_name)

Category names are delimited by square brackets as the first and last
characters of the line.

Items in each category are just plain text, one item per line

Any lines before the first category will be assigned to 'uncategorized'

The format is simmilar to .ini files, only you don't have thei 'key'='value'
structure in the items.

Blank lines and lines that begin with '#' are ignored.

Example of a file:

```
# the following lines will be assigned to 'uncategorized`

Linux
Windows
MacOS

[Directories]
/home
/usr
/etc

# this line will be ignored

[Files]
README.md
module.py
```
