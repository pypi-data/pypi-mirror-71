# utilless
Useless library if you have time for puzzles, a useful one if you don't

## Quickstart
Install using pip: `pip install utilless`  
and import package into your script, v.g.  
`from utilless.comma import commaspace`
`print(commaspace(['Hello', 'world!']))`

## Module comma
Manipulates iterables and gets results with commas

iterable: any element that has __ iter __ method, like
list, tuple, set, dict or even str.

* justcomma(iterable)

`>>> justcomma(['apples', 'bananas', 'tofu', 'cats'])`  
`'apples,bananas,tofu,cats'`


* commaspace(iterable)

`>>> commaspace(['apples', 'bananas', 'tofu', 'cats'])`  
`'apples, bananas, tofu, cats'`

* commaand(iterable)

`>>> commaand(['apples', 'bananas', 'tofu', 'cats'])`  
`'apples, bananas, tofu, and cats'`

or commaand(iterable, str)  
`>>> commaand(['apples', 'bananas', 'tofu', 'cats'], ' & ')`  
`'apples, bananas, tofu & cats'`

## Module dot
Manipulates iterables and gets results with dots

* justdot(iterable)

`>>> justdot(['apples', 'bananas', 'tofu', 'cats'])`  
`'apples,bananas,tofu,cats'`

## Module iseven
Infamous function. Learn how to use modulo (%)

* iseven(int)

`>>> iseven(1)`  
`False`
`>>> iseven(42)`  
`True`

## Module isodd 
See module iseven 

* isodd(int)

`>>> isodd(1)`  
`True`
`>>> isodd(42)`  
`False`