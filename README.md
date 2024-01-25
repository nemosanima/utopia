# Utopia

WSGI framework with routing and middleware support.

## Install dependencies

poetry

```shell
poetry install
```

pip

```shell
pip install parse gunicorn
```

## Example

**example.py**:

```python
from src import Utopia

app = Utopia()


@app.router("/", methods=["GET"])
def read_root(request):
    return {"Hello": "World"}


@app.router("/items/{item_id}", methods=["GET"])
def read_item(request, item_id):
    return {"item_id": item_id}
```

Then run the application using Gunicorn:

```shell
$ gunicorn example:app
```