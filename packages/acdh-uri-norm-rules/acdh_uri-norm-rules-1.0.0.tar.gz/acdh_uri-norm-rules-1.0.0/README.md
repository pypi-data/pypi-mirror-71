# UriNormRules

Set of URI normalization rules used within the [ACDH-CD](https://www.oeaw.ac.at/acdh/).

Provides Python 3 and PHP bindings.

Rules are stored as a JSON in the `UriNormRules/rules.json` file.

# Installation

## Python

Using pip3:

```bash
pip install acdh_uri-norm-rules
```

## PHP

Using [composer](https://getcomposer.org/doc/00-intro.md):

```bash
composer require acdh-oeaw/uri-norm-rules
```

# Usage

## Python

```Python
from AcdhUriNormRules import *
print(AcdhUriNormRules.getRules())

```

## PHP

```php
require_once 'vendor/autoload.php';
print_r(acdhOeaw\UriNormRules::getRules());
```
