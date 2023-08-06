# fitting2d

a library for performing two-dimensional curve-fitting.

## Install

```
pip install . # within this repository
```

Presumably, it can be also installed from PyPI:

```
pip install fitting2d
```

## Usage

For more detailed documentation, visit our [documentation page](https://fitting2d.readthedocs.io/en/latest/).

### Classes

Currently, it has only two types of fitting procedures as classes:

- `Ellipse`
- `Circle`
- `Parabola`

Both classes are built as `namedtuple`s.

You can also extend the library by adding the `FittingMixin` mix-in class
to your shape class (built as a `namedtuple`).

### Performing fitting

To perform the fitting procedure, run e.g.

```python
# xp and yp consisting of x- and y- coordinates as arrays
model = Ellipse.fit(xp, yp)
```

### Drawing the fitted shapes

Both classes have the `draw` method making use the parameter-based representation:

```python
# t being the coordinate parameter
xp, yp = model.draw(t)
```

The nature of the parameter `t` above depends on the fitted shape.
Some tips are in the docstring for the `draw` method.

## License

Copyright (c) 2020 Keisuke Sehara, the MIT License
