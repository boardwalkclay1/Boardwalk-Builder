import os
from typing import List
from .paths import project_root
from .utils import ensure_dir, write_file
from .agent import AgentEvent

def create_db_layer(project: str, events: List[AgentEvent]) -> None:
    db_dir = os.path.join(project_root(project), "db")
    ensure_dir(db_dir)
    write_file(
        os.path.join(db_dir, "schema.sql"),
        """-- Example schema; extend as needed
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  token TEXT NOT NULL,
  created_at TEXT NOT NULL,
  expires_at TEXT NOT NULL
);
""",
    )
    write_file(
        os.path.join(db_dir, "migrations.md"),
        "# Migrations\n\n- 0001_initial_users_sessions\n",
    )
    events.append(AgentEvent(kind="agent", message="Database schema and migrations stub created."))
