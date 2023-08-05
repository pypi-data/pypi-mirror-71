# EResponse
This is a simple package to form json response easily.

## Usage

```python
from eresponse import new_success_message, new_error_message

def example():
    try:
        res = {
            "key": 1
        }
        return new_success_message("Success text", test=res)
    except Exception as e:
        return new_error_message("Error text")
```

What it looks like in response

### Success
```json
{
  "ok": true,
  "message": "Success text",
  "test": {
    "key": 1
  }
}

```

### Error
```json
{
  "ok": false,
  "error": "Error text"
}
```

