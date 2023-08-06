# duck
A small Python package facilitating duck typing through attribute traverse utilities

This replaces try/except chains when trying to call different methods:
```python
from duckt import Duck, DuckCall

class Lion:
    def roar(self):
        return "roar!"

creature = Lion()
assert Duck(creature).attr_call(
    DuckCall("make_sound", ["woof"]), # tries to call creature.make_sound("woof")
    DuckCall("make_sound", ["buzz", 100]), # tries to call creature.buzz("buzz", 100)
    DuckCall("bark"), # creature.bark()
    DuckCall("roar"), # creature.roar()
    DuckCall("speak", ["Hello "], {"times": 3}) # creature.speak("Hello ", times=3)
) == "roar!"

 # returns the output of the first successfull call
# if none of the call attempts was successful then the last raised error will be thrown
```
**DuckCall** class is fully replacable here with any custom callable accepting single argument. This argument is the **Duck**-wrapped object, so you can implement custom attribute extracting and/or calling behavior here. **AttributeError**s and **TypeError**s thrown from this callable is handled by the **Duck** instance.


Simplified interface for property extraction:
```python
from duckt import Duck

class Person:
    full_name = "John Doe"

some_person = Person()
name = Duck(some_person).attr('first_name', 'name', 'full_name')
# name now is equal to the first present attribute
# otherwise AttributeError is thrown
```

You may also use **Duck** as wrapper to a callable:
```python
from duckt import Duck

def foo(some_string):
    print(some_string)

duck = Duck(foo)
duck.call(
    ["hello", "world"], # foo("hello", "world")
    ["hello world"],    # foo("hello world")
    [[], {"hello": "world"}]  # foo(hello="world")
)

```
That's it.
