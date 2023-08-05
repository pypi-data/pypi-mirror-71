# Basket Case
Basket case is a small, pure-Python swiss army knife for translating strings between case styles. I developed it because in my development work I often need to switch between string renderings: snake_case for Python, slug-names for document names, camelCase for a bunch of things, CONSTANT_NAMES for, well, constants, and Title Case for nice human readability.

I want to be able to move between these fluidly and reliably, and by using a single import statement.

```
import basket_case as bc

my_string = "a long name for a variable"
assert bc.slug(my_string)     == "a-long-name-for-a-variable"
assert bc.title(my_string)    == "A Long Name for a Variable"
assert bc.camel(my_string)    == "aLongNameForAVariable"
assert bc.snake(my_string)    == "a_long_name_for_a_variable"
assert bc.constant(my_String) == "A_LONG_NAME_FOR_A_VARIABLE"
```

## Installation

```
pip install basket-case
```

Python 3+ only; sorry not sorry.

## Usage



## Dependencies

Basket case wraps titlecase and python-slugify for their respective capabilities.

## Contributions

Please!
