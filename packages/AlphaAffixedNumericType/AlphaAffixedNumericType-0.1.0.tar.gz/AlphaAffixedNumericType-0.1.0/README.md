# AlphaAffixedNumericType (aant)
Python data type to support arithmetics on alphanumeric string

## Types of arithmetics supported
- Addition
    `aant + integer`
    \* NOTE: integer type must be on the right of addition operator

- Subtraction
    `aant - [integer|aant]`

## How to Use

```python
from AlphaAffixedNumericType import AlphaAffixedNumericType

aant = AlphaAffixedNumericType('A123')
print(aant + 1)  # prints 'A124' 
print(aant + 1000)  # prints 'A1123' 

aant += 10
print(aant.get_value()) # prints 'A133'

aant2 = AlphaAffixedNumericType('A123B')
aant3 = AlphaAffixedNumericType('A124B')
print(aant2 - aant3)  # prints -1 

print(aant2 - 200)  # raises 'NumericArithmeticException' - Numeric part of aant2 (123) is less than 200

aant4 = AlphaAffixedNumericType('A0001B')
print(aant4 + 1000)  # prints 'A1001B' 

```