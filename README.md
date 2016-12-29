# Command

## Install

`pip install git+ssh://git@github.com/dduong42/Command.git`

## Example

```python
import json
import os
from collections import deque

from command import command, inverse_of


@command
def populate_file(context):
    filename = context['filename']
    count = context['count']

    with open(filename, 'r') as f:
        context.setdefault('old_content', [])
        context['old_content'].append(f.read())

    with open(filename, 'w') as f:
        for i in range(count):
            f.write('{}'.format(i))

    return context


@inverse_of(populate_file)
def restore_file(context):
    filename = context['filename']
    old_content = context['old_content'].pop()
    with open(filename, 'w') as f:
        f.write(old_content)

    return context


@command
def persist_context(context):
    context_filename = context['context_filename']
    with open(context_filename, 'w+') as f:
        f.write(json.dumps(context))
    return context


@inverse_of(persist_context)
def restore_context(context):
    context_filename = context['context_filename']
    with open(context_filename) as f:
        new_context = f.read()
    os.unlink(context_filename)

    context.update(json.loads(new_context))
    return context


two_populate = populate_file >> populate_file >> persist_context
two_populate({'filename': 'file.txt', 'count': 10,
              'context_filename': 'context.json'})
two_populate.inverse({'context_filename': 'context.json'})
```
