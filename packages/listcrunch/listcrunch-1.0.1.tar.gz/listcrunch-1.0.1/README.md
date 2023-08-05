# ListCrunch

A simple human-readable way to compress redundant sequential data.

## Example

```python
from listcrunch import crunch

compressed_string = crunch([1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
# Returns '1:0-8;2:9', meaning 1 appears in indices 0-8 (inclusive),
# and 2 occurs at index 9.
```

To uncompress, use the `uncrunch` function.

```python
from listcrunch import uncrunch

uncrunch('50:0-1,3-4;3:2,5;60:6;70:7-8')
# Returns ['50', '50', '3', '50', '50', '3', '60', '70', '70']
```
