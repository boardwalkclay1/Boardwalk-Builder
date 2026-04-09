import os
from typing import List
from .paths import project_root, safe_name
from .utils import ensure_dir, write_file
from .agent import AgentEvent

def create_cloudflare_layer(project: str, events: List[AgentEvent]) -> None:
    cf_dir = os.path.join(project_root(project), "cloudflare")
    ensure_dir(cf_dir)
    write_file(
        os.path.join(cf_dir, "wrangler.toml"),
        f"""name = "{safe_name(project)}-worker"
main = "worker.js"
compatibility_date = "2024-04-08"

[[kv_namespaces]]
binding = "{safe_name(project).upper()}_KV"
id = "00000000000000000000000000000000"

[[d1_databases]]
binding = "{safe_name(project).upper()}_D1"
database_name = "{safe_name(project)}-db"
database_id = "00000000-0000-0000-0000-000000000000"

[[queues.producers]]
binding = "{safe_name(project).upper()}_QUEUE"
queue = "{safe_name(project)}-queue"

[triggers]
crons = ["0 * * * *"]
""",
    )
    write_file(
        os.path.join(cf_dir, "worker.js"),
        """export default {
  async fetch(request, env, ctx) {
    return new Response("Cloudflare Worker for app", {
      status: 200,
      headers: { "content-type": "text/plain" }
    });
  },

  async queue(batch, env, ctx) {
    for (const msg of batch.messages) {
      console.log("Queue message", msg.body);
    }
  },

  async scheduled(event, env, ctx) {
    console.log("Cron trigger", event.cron);
  }
};
""",
    )
    events.append(AgentEvent(kind="agent", message="Cloudflare Worker + KV + D1 + Queue + Cron config created."))
