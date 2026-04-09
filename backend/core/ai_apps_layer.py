import os
from typing import List
from .paths import project_root
from .utils import ensure_dir, write_file
from .agent import AgentEvent

def extend_with_ai_capabilities(project: str, goal: str, events: List[AgentEvent]) -> None:
    """
    This prepares the project to support:
    - music generation endpoints
    - video generation endpoints
    - image-to-comic / image-to-video transforms
    The actual model calls will be wired by you (e.g. to external APIs or local models).
    """
    backend_dir = os.path.join(project_root(project), "backend")
    ensure_dir(backend_dir)

    # Node-side AI routes stub
    write_file(
        os.path.join(backend_dir, "ai_routes.js"),
        """// AI routes stub: wire to your model providers (e.g. external APIs, local models)
const express = require("express");
const router = express.Router();

// POST /api/ai/music
router.post("/music", async (req, res) => {
  // TODO: call your music generation backend
  res.json({ ok: true, message: "Music generation stub. Wire to your model." });
});

// POST /api/ai/video
router.post("/video", async (req, res) => {
  // TODO: call your video generation backend
  res.json({ ok: true, message: "Video generation stub. Wire to your model." });
});

// POST /api/ai/image-to-comic
router.post("/image-to-comic", async (req, res) => {
  // TODO: call your image-to-comic backend
  res.json({ ok: true, message: "Image-to-comic stub. Wire to your model." });
});

// POST /api/ai/image-to-video
router.post("/image-to-video", async (req, res) => {
  // TODO: call your image-to-video backend
  res.json({ ok: true, message: "Image-to-video stub. Wire to your model." });
});

module.exports = router;
""",
    )

    # Note for wiring into server.js
    write_file(
        os.path.join(backend_dir, "ai_notes.md"),
        """# AI App Capabilities

This project is prepared for:

- Music generation
- Video generation
- Image → comic
- Image → video

Wire `ai_routes.js` into `server.js`:

```js
const aiRoutes = require("./ai_routes");
app.use("/api/ai", aiRoutes);
