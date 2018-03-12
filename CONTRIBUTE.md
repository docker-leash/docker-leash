# Contribute

## Launch the Unit Tests

With [nose](//nose.readthedocs.io/)
(and it's [watch plugin](https://pypi.python.org/pypi/nose-watch)):
```sh
nosetests tests -v --with-watch --with-coverage --cover-package=docker_leash
```

Or without:
```sh
python -m unittest discover -s tests
```

## Compile the documentation

```sh
python setup.py build_sphinx
```
