# magic-kind

The MagicKind type is a simpler alternative to Enum types for groups of
related magic values when order is not important.

### Synopsis:

```
from magic_kind import MagicKind

class HttpCode(MagicKind):
    OK = 200
    NOT_FOUND = 404
    GATEWAY = 503
  
...

raise HttpException(HttpCode.NOT_FOUND, ...)
    
...

assert http_code in HttpCode

...

for http_code in HttpCode:
    http_code 
````

### Motivation

Think of the kind of things you might put in a constants.py file to make
sure you use the value consistently across your application. And then think
about the times such magic values were really just one of a number of
alternatives. For example they were all different Http Code values like:

```
HTTP_CODE_OK = 200
HTTP_CODE_NOT_FOUND = 404
HTTP_CODE_GATEWAY = 503
```

This is the kind of case that the the MagicKind type is made for. Instead
one would do this:

```
class HttpCode(MagicKind):
    OK = 200
    NOT_FOUND = 404
    GATEWAY = 503
```

The class itself provides some container object like functionality. It
allows you to iterate over it and get the values, and it allows you to use the
***in*** operator to check if a value you got somewhere else is in the Choices.

### But why not just use Enum instead?
Enumerated types have a similar but broader functionality where they are like
containers with special objects that know their relative order and have
attributes for their "name" and "value".

MagicKind types are instead like containers of the values themselves. This
makes dealing with them easier unless there is some special reason you are
interested in the order and attribute names as well as the values.

To illustrate the difference, let us suppose some user entered data is stored
as **some_string** and we wish to know if it is one of our kinds of soda:

```python
class Soda(str, Enum):
    ROOT_BEER = "root beer"
    COLA = "cola"
    
valid_soda_values = set([_.value for _ in Soda])

if some_string in valid_soda_values:
    print(f"{some_string} is a soda")
```
With MagicKind the basic elements are just the values "root beer" and "cola",
so we don't need to make a **valid_soda_values** set:

```python
class Soda(MagicKind):
    ROOT_BEER = "root beer"
    COLA = "cola"
    
if some_string in Soda:
    print(f"{some_string} is a soda")
```

### Usage Rules:
1. To be recognized as one of the choices, attribute names must be
       upper case identifiers that do not begin with an underscore. This
       is by design to allow other kinds of members to be added (methods
       for example, or other attributes that are not meant to be choices).
2. The values must be hashable (they are stored in a set internally). It
       is recommended that they are also immutable.
3. The upper case choice values should never be changed nor should they 
be replaced. Doing so will cause the internal metaclass data to be wrong and
 trouble will likely follow. If you want some non-constant class values, don't
 make them upper case, and they won't be seen as one of the magic value choices.
4. The following pre-existing non-choice members should not be overwritten:

| name | what it is already used for |
| --- | --- |
| **get_dict** | method that gets dict of magic value attribute names and values |
| **get_names** | method that gets set of magic value attribute names |
| **_choices_dict** | internal use by MetaMagicKind metaclass |
| **_choices_set** | internal use by MetaMagicKind metaclass |
| **_pydantic_validate** | along with **\_\_get_validators\_\_** provided to support use of MagicKind [in pydantic models](https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types) |

In addition, all \_\_special\_\_ variable names should only be overloaded if you know what you are doing.

### Works with Pydantic 
For those who wish to declare the MagicKind type in a
[pydantic model](https://pydantic-docs.helpmanual.io/usage/models/), MagicKind
has a validator method that behaves just as one expects (it will only accept
one of the "magic values" for the subclass).

### Acknowledgement
This package was originally developed at Rackspace Technology, which is releasing it
to the public under the Apache 2 open source license.
