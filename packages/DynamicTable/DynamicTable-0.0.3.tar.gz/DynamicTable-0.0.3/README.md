# DynamicTable

Install using pip:

```bash
pip install DynamicTable
```

Extra documentation:

https://pypi.org/project/DynamicTable/
 
HOW TO USE:
```python
from DynamicTable import DynamicTable
header = ['Epoch','Progress','loss_labels']
formatters = {'Epoch':'{:03d}', 'Progress':'%$', 'loss_labels':'{:3f}'}
progress_table = DynamicTable(header, formatters)
import sys, time
### Print header
sys.stdout.write(progress_table.header)
sys.stdout.flush()
for i in range(5):
    time.sleep(1)
    for b in range(100):
        time.sleep(.01)
        vals = {'Epoch': i, 'Progress': b/99, 'loss_labels': 100*np.random.randn()}
        line = progress_table.update_line(vals, append = b == 99)
        if b != 99:
            sys.stdout.write(line + '\r')
        else:
            sys.stdout.write(line + '\n')
### Print bottom of the table
sys.stdout.write(progress_table.bottom_border + '\n')
```