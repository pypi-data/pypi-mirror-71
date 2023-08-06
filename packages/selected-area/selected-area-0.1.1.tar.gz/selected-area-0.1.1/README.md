# Selected Area
[![Build Status](https://travis-ci.com/nedvedikd/selected-area.svg?branch=master)](https://travis-ci.com/nedvedikd/selected-area)
[![PyPI version](https://badge.fury.io/py/selected-area.svg)](https://badge.fury.io/py/selected-area)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/selected-area)

![nice image](https://i.postimg.cc/0QK43NMj/selected-area.png)

Calculates if plot/segment intersects the selected area.

## Installation

```bash
pip install selected-area
```

## Usage
```python
from selected_area import Segment, Point, SelectedArea

area = SelectedArea(Point(1, 2), Point(4,4))
segment = Segment(Point(2, 1.5), Point(4.5, 3.5))

if area.contains(segment):
    print('Segment was selected.')
else:
    print('Segment wasn\'t selected.')
```