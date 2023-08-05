# VAT Package utilities

Utilities for publishing private packages

## Using
Install:
```
pip install vat-package-utils
```

## Developing
Install dev requirements:
```
pip install -r requirements-dev.txt
```

Build:
```
python setup.py sdist
```

Publish to PyPi:
```
twine upload -r pypi dist/vat-package-utils-*
```

For more on publishing to PyPi, see https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/.
