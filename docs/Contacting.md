# All your JS to Python contacting is here.
To create a function in [@api.py](api.py), create a function IN the `API` class, and do something like
```python
class API:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        print(f"Calling from Pyder's Python. Hello, {self.name}!")
```

Obviously, you can organize the code to something like
```text
src
| backend
| | utils
| | | print.py
| | api.py
```
And then import it to something like
```python
import src.backend.utils.print as print

class API:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        print.log(f"Calling from Pyder's Python. Hello, {self.name}!")
```

## To actually call the script.
For Typescript, in the root of `src` folder or in `./src/types/pywebview.d.ts`, paste this in.
```typescript
interface PyWebviewAPI {
  greet?: (name: string) => string;
  getOS?: () => string;
}

declare global {
  interface Window {
    pywebview: {
      api: PyWebviewAPI;
    };
  }
}

export {};
```

For javascript, it's reccomended to put it in `./src/utils/pyder`.
```javascript
const pywebview = window.pywebview || {};
const pyAPI = pywebview.api || {};

export function pyder<T = unknown>(
  method: PyMethodName,
  args: any[] = []
): T | undefined {
  try {
    const api = window.pywebview?.api;
    if (!api) {
      console.warn("PyWebView isn't ready yet.");
      return undefined;
    }

    const fn = api[method] as ((...a: any[]) => T) | undefined;
    if (!fn) {
      console.warn(`Python method "${String(method)}" not found.`);
      return undefined;
    }

    return fn(...args);
  } catch (err) {
    console.error(`Failed to call Pyder to "${String(method)}`, err);
    return undefined;
  }
}

export { callPython };
```

### To use the code,
```typescript
// if you're using javascript, you'd have to import it.
import { pyder } from './utils/pyder';

const pyAPI = window.pywebview?.api // optional, but makes the code cleaner!

return (
  <>
    <button
      onClick={() => {
        pyder('greet', ["World!"]);
      }}
    >
      Call Python
    </button>
  </>
)
```
This is only used for JSX or TSX. Framework will vary on how to call them.
