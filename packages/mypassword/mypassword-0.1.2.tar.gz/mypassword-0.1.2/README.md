# MyPassword Package

## Installation
mypassword requires Python 3.* to work

```sh
$ pip install mypassword
```
or

```sh
$ pip3 install mypassword
```

## Password
### Default Use
```python
from mypassword import Password

password = Password()

print(password)          # Ex. print xvcpdudi
print(password.password) # Ex. print xvcpdudi
```

### Stronger passwords
There are 4 levels for the password strength level
1. Level One: Includes only lower case characters
2. Level Two: Includes lower and upper case characters
3. Level Three: Includes lower and upper case characters and digits
4. Level Four: Includes lower and upper case characters, digits and punctuation characters

If you need more security, you can specify the level in the creation of the object

```python
from mypassword import Password, PasswordLevel

password_level_one = Password()
password_level_two = Password(level=PasswordLevel.TWO)
password_level_three = Password(level=PasswordLevel.THREE)
password_level_four = Password(level=PasswordLevel.FOUR)

print(password_level_one)   # Ex. print amzvlepp  
print(password_level_two)   # Ex. print RbHnbpMa
print(password_level_three) # Ex. print 9hS7c1Tw
print(password_level_four)  # Ex. print l8:N7@.1
```

### Length
Additionally you can specify the password length, by default the length is 8

```python
from mypassword import Password, PasswordLevel

password_level_one = Password(length=16)
password_level_four = Password(length=32, level=PasswordLevel.FOUR)

print(password_level_one)   # Ex. print enxhyrpgwecyboyn  
print(password_level_four)  # Ex. print lX7a`DMN$e\09<i|0U93r6Lj7bg1m0Z/
```

## Pasworify
### Default use
```python
from mypassword import Passworify

my_string = 'my secure password'
passworify = Passworify(my_string)
passworify.parse()
print(passworify.password) # Ex. print My+SEcUR3!PASSw0rd
```

`passworify.parse()` converts the string into a `Password` instance. The object is in the attribute `passworify.password`