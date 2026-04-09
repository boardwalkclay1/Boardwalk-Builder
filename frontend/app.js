const { useState, useEffect } = React;

const API_BASE = "http://localhost:8000";

function StudioApp() {
  const [theme, setTheme] = useState("gold");
  const [project, setProject] = useState("Laundry-Bubbles");
  const [goal, setGoal] = useState(
    "Build a full production-ready app with backend, frontend, DB, Cloudflare Worker, D1, KV, R2, Queues, and deployment."
  );
  const [stack, setStack] = useState("react-node");

  const [toggles, setToggles] = useState({
    allow_scaffold: true,
    allow_db: true,
    allow_api: true,
    allow_auth: true,
    allow_media: true,
    allow_cloudflare: true,
    allow_frontend: true,
    allow_service_worker: true,
    allow_deploy: true,
    allow_fix: true,
    allow_ai_apps: true,
  });

  const [agentEvents, setAgentEvents] = useState([]);
  const [agentRunning, setAgentRunning] = useState(false);

  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState("");
  const [fileLoading, setFileLoading] = useState(false);
  const [fileSaving, setFileSaving] = useState(false);

  const [githubUrl, setGithubUrl] = useState("");
  const [githubEvents, setGithubEvents] = useState([]);

  const [deployEvents, setDeployEvents] = useState([]);
  const [deploying, setDeploying] = useState(false);

  const [errorLog, setErrorLog] = useState("");
  const [errorFixEvents, setErrorFixEvents] = useState([]);
  const [fixingErrors, setFixingErrors] = useState(false);

  const [runMessages, setRunMessages] = useState([]);

  // THEME
  useEffect(() => {
    const body = document.body;
    body.classList.remove("theme-gold", "theme-red", "theme-white");
    if (theme === "gold") body.classList.add("theme-gold");
    if (theme === "red") body.classList.add("theme-red");
    if (theme === "white") body.classList.add("theme-white");
  }, [theme]);

  // HELPERS
  function pushAgentEvents(events) {
    setAgentEvents((prev) => [...prev, ...events]);
  }

  function pushGithubEvents(events) {
    setGithubEvents((prev) => [...prev, ...events]);
  }

  function pushDeployEvents(events) {
    setDeployEvents((prev) => [...prev, ...events]);
  }

  function pushRunMessage(msg) {
    setRunMessages((prev) => [...prev, msg]);
  }

  function pushErrorFixEvents(events) {
    setErrorFixEvents((prev) => [...prev, ...events]);
  }

  // API CALLS

  async function runAgent() {
    setAgentRunning(true);
    setAgentEvents([]);
    try {
      const payload = {
        project,
        goal,
        stack,
        ...toggles,
        mode: "full",
      };
      const res = await fetch(`${API_BASE}/api/agent/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      pushAgentEvents(data.events || []);
    } catch (err) {
      pushAgentEvents([
        { kind: "error", message: `Agent error: ${err.message || String(err)}` },
      ]);
    } finally {
      setAgentRunning(false);
      // refresh file tree after generation
      loadFiles();
    }
  }

  async function loadFiles() {
    if (!project) return;
    try {
      const res = await fetch(
        `${API_BASE}/api/files/list?project=${encodeURIComponent(project)}`
      );
      if (!res.ok) return;
      const data = await res.json();
      setFiles(data.items || []);
    } catch (err) {
      // ignore for now
    }
  }

  async function openFile(path) {
    setSelectedFile(path);
    setFileLoading(true);
    try {
      const res = await fetch(
        `${API_BASE}/api/files/read?project=${encodeURIComponent(
          project
        )}&path=${encodeURIComponent(path)}`
      );
      const data = await res.json();
      setFileContent(data.content || "");
    } catch (err) {
      setFileContent(`// Error loading file: ${err.message || String(err)}`);
    } finally {
      setFileLoading(false);
    }
  }

  async function saveFile() {
    if (!selectedFile) return;
    setFileSaving(true);
    try {
      await fetch(`${API_BASE}/api/files/write`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project,
          path: selectedFile,
          content: fileContent,
        }),
      });
    } catch (err) {
      // could show toast
    } finally {
      setFileSaving(false);
    }
  }

  async function runBackend() {
    try {
      await fetch(`${API_BASE}/api/run/backend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project }),
      });
      pushRunMessage("Backend dev server started (npm run dev).");
    } catch (err) {
      pushRunMessage(`Backend run error: ${err.message || String(err)}`);
    }
  }

  async function runFrontend() {
    try {
      await fetch(`${API_BASE}/api/run/frontend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project }),
      });
      pushRunMessage("Frontend dev server started (npm run dev).");
    } catch (err) {
      pushRunMessage(`Frontend run error: ${err.message || String(err)}`);
    }
  }

  async function deployWorker() {
    setDeploying(true);
    setDeployEvents([]);
    try {
      const res = await fetch(`${API_BASE}/api/cloudflare/deploy_worker`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project }),
      });
      const data = await res.json();
      pushDeployEvents(data.events || []);
      if (data.output) {
        pushDeployEvents([
          { kind: "system", message: "wrangler output captured in response." },
        ]);
      }
    } catch (err) {
      pushDeployEvents([
        { kind: "error", message: `Deploy error: ${err.message || String(err)}` },
      ]);
    } finally {
      setDeploying(false);
    }
  }

  async function cloneGithub() {
    if (!githubUrl.trim()) return;
    setGithubEvents([]);
    try {
      const res = await fetch(`${API_BASE}/api/github/clone`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project, repo_url: githubUrl.trim() }),
      });
      const data = await res.json();
      pushGithubEvents(data.events || []);
      // refresh file tree
      loadFiles();
    } catch (err) {
      pushGithubEvents([
        { kind: "error", message: `GitHub clone error: ${err.message || String(err)}` },
      ]);
    }
  }

  async function fixErrors() {
    if (!errorLog.trim()) return;
    setFixingErrors(true);
    setErrorFixEvents([]);
    try {
      const res = await fetch(`${API_BASE}/api/agent/fix_errors`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project, errors: errorLog }),
      });
      const data = await res.json();
      pushErrorFixEvents(data.events || []);
    } catch (err) {
      pushErrorFixEvents([
        { kind: "error", message: `Fix error: ${err.message || String(err)}` },
      ]);
    } finally {
      setFixingErrors(false);
    }
  }

  // INITIAL LOAD
  useEffect(() => {
    loadFiles();
  }, [project]);

  // UI HELPERS

  function toggleFlag(key) {
    setToggles((prev) => ({ ...prev, [key]: !prev[key] }));
  }

  function renderEvents(events) {
    return events.map((e, idx) => {
      const cls =
        e.kind === "system"
          ? "event-kind-system"
          : e.kind === "agent"
          ? "event-kind-agent"
          : e.kind === "error"
          ? "event-kind-error"
          : "";
      return (
        <div key={idx} className={`event-line ${cls}`}>
          [{e.kind?.toUpperCase?.() || "LOG"}] {e.message}
        </div>
      );
    });
  }

  function renderFileTree() {
    if (!files.length) {
      return <div className="file-tree-item">No files yet. Run the agent or clone a repo.</div>;
    }
    return files.map((item, idx) => {
      const isActive = selectedFile === item.path;
      return (
        <div
          key={idx}
          className={`file-tree-item ${isActive ? "active" : ""}`}
          onClick={() => item.type === "file" && openFile(item.path)}
        >
          <span className="file-tree-type">
            {item.type === "dir" ? "DIR" : "FILE"}
          </span>
          <span className="file-tree-path">{item.path}</span>
        </div>
      );
    });
  }

  return (
    <div className="studio-shell">
      {/* HEADER */}
      <header className="studio-header">
        <div className="studio-title-block">
          <div className="studio-logo" />
          <div className="studio-title-text">
            <h1>Boardwalk Studio</h1>
            <span>Autonomous Builder · IDE · Cloudflare Deployer</span>
          </div>
        </div>
        <div className="studio-header-right">
          <div className="theme-switcher">
            <span style={{ fontSize: 10, textTransform: "uppercase", letterSpacing: "0.12em" }}>
              Theme
            </span>
            <button
              className={`theme-pill ${theme === "gold" ? "active" : ""}`}
              onClick={() => setTheme("gold")}
            >
              Gold
            </button>
            <button
              className={`theme-pill ${theme === "red" ? "active" : ""}`}
              onClick={() => setTheme("red")}
            >
              Red
            </button>
            <button
              className={`theme-pill ${theme === "white" ? "active" : ""}`}
              onClick={() => setTheme("white")}
            >
              White
            </button>
          </div>
        </div>
      </header>

      {/* MAIN */}
      <main className="studio-main">
        {/* LEFT: PROJECT + AGENT */}
        <section className="studio-panel">
          <div className="studio-panel-header">
            <h2>Project · Agent</h2>
            <span>{project || "No project"}</span>
          </div>
          <div className="studio-panel-body">
            <div className="field-group">
              <div className="field-label">Project Name</div>
              <input
                className="input"
                value={project}
                onChange={(e) => setProject(e.target.value)}
                placeholder="e.g. Laundry-Bubbles"
              />
            </div>

            <div className="field-group">
              <div className="field-label">Goal</div>
              <textarea
                className="textarea"
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
              />
            </div>

            <div className="field-group">
              <div className="field-label">Stack</div>
              <select
                className="select"
                value={stack}
                onChange={(e) => setStack(e.target.value)}
              >
                <option value="react-node">React + Node</option>
                <option value="react-fastapi">React + FastAPI</option>
                <option value="svelte-worker">Svelte + Worker</option>
                <option value="next-node">Next.js + Node</option>
                <option value="vanilla-html">Vanilla HTML/CSS/JS</option>
              </select>
            </div>

            <div className="field-group">
              <div className="field-label">Capabilities</div>
              <div className="toggle-row">
                {Object.entries(toggles).map(([key, value]) => (
                  <button
                    key={key}
                    className={`toggle-chip ${value ? "active" : ""}`}
                    onClick={() => toggleFlag(key)}
                  >
                    {key.replace("allow_", "").replace(/_/g, " ")}
                  </button>
                ))}
              </div>
            </div>

            <div className="field-group" style={{ display: "flex", gap: 6 }}>
              <button
                className="btn btn-primary"
                onClick={runAgent}
                disabled={agentRunning || !project}
              >
                {agentRunning ? "Running Agent..." : "Run Autonomous Builder"}
              </button>
              <button className="btn btn-ghost" onClick={loadFiles}>
                Refresh Files
              </button>
            </div>

            <div className="events-log">{renderEvents(agentEvents)}</div>
          </div>
        </section>

        {/* CENTER: FILES + EDITOR */}
        <section className="studio-panel">
          <div className="studio-panel-header">
            <h2>Files · Editor</h2>
            <span>{selectedFile || "No file selected"}</span>
          </div>
          <div className="studio-panel-body">
            <div className="field-label">Project Files</div>
            <div className="file-tree">{renderFileTree()}</div>

            <div className="editor-area">
              <div className="editor-header">
                <div className="editor-filename">
                  {selectedFile ? selectedFile : "Select a file to edit"}
                </div>
                <div style={{ display: "flex", gap: 6 }}>
                  <button
                    className="btn btn-primary"
                    onClick={saveFile}
                    disabled={!selectedFile || fileSaving}
                  >
                    {fileSaving ? "Saving..." : "Save File"}
                  </button>
                </div>
              </div>
              <textarea
                className="editor-textarea"
                value={fileContent}
                onChange={(e) => setFileContent(e.target.value)}
                disabled={!selectedFile || fileLoading}
                placeholder={
                  selectedFile
                    ? fileLoading
                      ? "Loading..."
                      : ""
                    : "No file selected."
                }
              />
            </div>
          </div>
        </section>

        {/* RIGHT: RUN / DEPLOY / GITHUB / ERRORS */}
        <section className="studio-panel">
          <div className="studio-panel-header">
            <h2>Run · Deploy · GitHub · Errors</h2>
            <span>Control Surface</span>
          </div>
          <div className="studio-panel-body">
            <div className="run-grid">
              <div className="run-card">
                <div className="run-card-title">Run</div>
                <div className="run-card-body">
                  <button className="btn btn-primary" onClick={runBackend}>
                    ▶ Backend (npm run dev)
                  </button>
                  <button className="btn btn-primary" onClick={runFrontend}>
                    ▶ Frontend (npm run dev)
                  </button>
                  <button
                    className="btn btn-ghost"
                    onClick={() => window.open("http://localhost:5173", "_blank")}
                  >
                    Open App (5173)
                  </button>
                </div>
              </div>

              <div className="run-card">
                <div className="run-card-title">Cloudflare</div>
                <div className="run-card-body">
                  <button
                    className="btn btn-primary"
                    onClick={deployWorker}
                    disabled={deploying}
                  >
                    {deploying ? "Deploying Worker..." : "Deploy Worker (wrangler)"}
                  </button>
                  <button
                    className="btn btn-ghost"
                    onClick={() =>
                      pushDeployEvents([
                        {
                          kind: "system",
                          message:
                            "Pages + D1 + R2 deploy can be wired via Cloudflare REST API next.",
                        },
                      ])
                    }
                  >
                    Pages / D1 / R2 (notes)
                  </button>
                </div>
              </div>

              <div className="run-card">
                <div className="run-card-title">GitHub</div>
                <div className="run-card-body">
                  <input
                    className="small-input"
                    placeholder="https://github.com/user/repo.git"
                    value={githubUrl}
                    onChange={(e) => setGithubUrl(e.target.value)}
                  />
                  <button className="btn btn-primary" onClick={cloneGithub}>
                    Clone into Project
                  </button>
                </div>
              </div>

              <div className="run-card">
                <div className="run-card-title">Errors</div>
                <div className="run-card-body">
                  <textarea
                    className="textarea"
                    style={{ minHeight: 60 }}
                    placeholder="Paste error logs here..."
                    value={errorLog}
                    onChange={(e) => setErrorLog(e.target.value)}
                  />
                  <button
                    className="btn btn-primary"
                    onClick={fixErrors}
                    disabled={fixingErrors}
                  >
                    {fixingErrors ? "Analyzing..." : "Analyze & Log Errors"}
                  </button>
                </div>
              </div>
            </div>

            <div style={{ display: "flex", gap: 6, marginTop: 6, height: "40%" }}>
              <div className="log-panel">
                <div className="field-label">Run Messages</div>
                {runMessages.map((m, i) => (
                  <div key={i} className="event-line">
                    {m}
                  </div>
                ))}
              </div>
              <div className="log-panel">
                <div className="field-label">Cloudflare Deploy</div>
                {renderEvents(deployEvents)}
              </div>
            </div>

            <div style={{ display: "flex", gap: 6, marginTop: 6, height: "30%" }}>
              <div className="log-panel">
                <div className="field-label">GitHub</div>
                {renderEvents(githubEvents)}
              </div>
              <div className="log-panel">
                <div className="field-label">Error Diagnostics</div>
                {renderEvents(errorFixEvents)}
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="studio-footer">
        <span>Boardwalk Studio · Local Autonomous Builder · Full Stack · Cloudflare Ready</span>
        <span>Project: {project || "none"}</span>
      </footer>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<StudioApp />);
