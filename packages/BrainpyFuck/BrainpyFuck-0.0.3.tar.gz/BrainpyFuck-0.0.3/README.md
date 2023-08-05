# BrainFuckInterpreter
### standard usage:
```python
from brainFuckInterpreter import BrainF
```
easily get outputs:

```python
for msg in BrainF('yourcodehere'):
    print(msg)  #msg is what the '.' outputs
```
or use a comprehension
```python
meg=[i for i in BrainF('yourcodehere') if i]
```
#### attributes
in the iterator called ```BrainF```:
```python
def __init__(self,code,*,print_memory=True, input_func=None, print_func=None)
```
<ul>
    <li>print_memory => bool</li>
    <li>input_func => function fot input</li>
    <li>print_func => function for printing memory(is not needed when print_memory is set to False)</li>
</ul>

### PrettyPrint!!!
```python
from brainFuckInterpreter import prettyprint
```
```python
prettyprint(ur list representing memory to print, the index of cell (aka element) u want to emphasize)
```


