# -*- text -*-
# first non-comment line must be the short description:
POSIX-conformant command-line option parser (plus long options)

Use it like this:

    import pgetopt

    ovc, args = pgetopt.parse({
    # opt: (name,          type, default value, helptext[, arg name])
      "s": ("schmooze",    bool, 0,    "increase schmooziness"),
      "o": ("output_file", str,  None, "output file (or stdout)", "NAME"),
      "n": ("repetitions", int,  3,    "number of repetitions"),
      "d": ("debug",       str, [],    "debug topics", "DEBUG_TOPIC"),
    # keyword:        value
      "_arguments":   ["string_to_print", "..."],
      "_help_header": "print a string a number of times",
      "_help_footer": "This is just an example program.",
    })

On return, the option value container `ovc` has the following fields:  
    `ovc.schmooze`:    the number of `-s` options counted,  
    `ovc.output_file`: the parameter of `-o` or `--output-file`, or `None`  
    `ovc.repetitions`: the parameter of `-n` or `--repetitions`, or `3`  
    `ovc.debug`:       a list with all parameters given to `-d` or `--debug`  

Options `-h`, `--help`, `-?`, `--usage` are installed by default and
print a help message or a brief usage message, respectively.

`args` holds the remaining arguments behind the last option.

Call `help(pgetopt)` for details.  
More information at <https://git.w21.org/python_modules/pgetopt>

The full documentation for this version is at
<https://git.w21.org/python_modules/pgetopt/-/blob/v$__package_version$/README.md>

[ni@w21.org 2020-05-22]
