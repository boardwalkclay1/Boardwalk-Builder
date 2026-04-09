import os
from typing import List
from .paths import project_root
from .utils import ensure_dir, write_file
from .agent import AgentEvent

def create_auth_layer(project: str, events: List[AgentEvent]) -> None:
    backend_dir = os.path.join(project_root(project), "backend")
    ensure_dir(backend_dir)
    write_file(
        os.path.join(backend_dir, "auth.js"),
        """// Basic auth helpers (to be wired into routes)
const crypto = require("crypto");

function hashPassword(password) {
  return crypto.createHash("sha256").update(password).digest("hex");
}

function generateToken() {
  return crypto.randomBytes(32).toString("hex");
}

module.exports = { hashPassword, generateToken };
""",
    )
    events.append(AgentEvent(kind="agent", message="Auth helper module created (hashing + token generation)."))
