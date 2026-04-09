
---

### `backend/core/errors_layer.py`

```python
import os
from typing import List
from .paths import project_root
from .utils import ensure_dir, write_file
from .agent import AgentEvent

def analyze_and_fix_errors(project: str, errors: str, events: List[AgentEvent]) -> None:
    root = project_root(project)
    ensure_dir(root)
    write_file(os.path.join(root, "diagnostics.log"), errors)
    write_file(
        os.path.join(root, "diagnostics.md"),
        f"# Diagnostics for {project}\n\n```\n{errors}\n```\n\nNext steps:\n- Inspect diagnostics.log\n- Adjust code or configs accordingly.\n",
    )
    events.append(AgentEvent(kind="agent", message="Error log captured to diagnostics.log and diagnostics.md for this project."))
