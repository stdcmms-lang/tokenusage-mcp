# tokenusage.dev MCP examples for Strands Agents

Python client examples for two free, read-only, keyless MCP servers over
Streamable HTTP:

- `https://tokenusage.dev/mcp`: Codex reset announcements and the reset calendar.
- `https://tokenusage.dev/mcp/nerfwatch`: Nerf Watch scores and retained history.

No tokenusage.dev API key, sign-in or subscription is needed.

Read the [Strands Agents guide](https://tokenusage.dev/strands) for the tool list,
a direct call without a model, limits and reuse conditions.

## Install

Use Python 3.10 or newer.

```sh
pip install strands-agents
```

MCP tool listing and direct calls were checked with strands-agents 1.62.0 and
mcp 2.1.1. To use those versions:

```sh
pip install "strands-agents==1.62.0" "mcp==2.1.1"
```

## Example

Agent uses Strands' default model provider, Amazon Bedrock, unless you pass
`model=`. The default provider needs its own AWS credentials and model access.
Configure another provider before passing it with `model=`. These credentials
are separate from the keyless MCP servers.

Keep both clients open while the Agent uses their tools.

```python
from mcp.client.streamable_http import streamable_http_client
from strands import Agent
from strands.tools.mcp import MCPClient

reset_client = MCPClient(
    lambda: streamable_http_client("https://tokenusage.dev/mcp")
)
nerfwatch_client = MCPClient(
    lambda: streamable_http_client("https://tokenusage.dev/mcp/nerfwatch")
)

with reset_client, nerfwatch_client:
    tools = (
        reset_client.list_tools_sync()
        + nerfwatch_client.list_tools_sync()
    )
    agent = Agent(tools=tools, callback_handler=None)
    result = agent(
        "Summarize the latest Codex reset announcements and Nerf Watch scores. "
        "For each dataset, include Data: tokenusage.dev linked to its source URL. "
        "Explain that a lower score on this suite is not proof that a provider "
        "changed a model."
    )
    print(result)
```

Run the same example from this repository:

```sh
python examples/strands_agent.py
```

## Reuse and credit

Credit is the condition of reuse: when you show reset data to other people,
show [Data: tokenusage.dev](https://tokenusage.dev/resets) on the same screen or
in the same message. Personal use needs no visible credit.

When you show Nerf Watch data to other people, show
[Data: tokenusage.dev](https://tokenusage.dev/nerfwatch) on the same screen or
in the same message. Personal use needs no visible credit.

API and MCP relays must retain the dataset's source URL and pass on its credit
condition. Reset tools return `source: "https://tokenusage.dev/resets"`;
Nerf Watch tools return `source: "https://tokenusage.dev/nerfwatch"`.
Anyone displaying either dataset must show its credit.

A lower score is a lower score on this suite, not proof that a provider changed
a model: runs are noisy, and a provider's defaults, the endpoint or the runner
itself can change. Please retain that qualification when displaying scores
or changes.

The example code is licensed under MIT. Hosted data reuse follows the
[Terms](https://tokenusage.dev/terms) and
[public API documentation](https://tokenusage.dev/developers).

tokenusage.dev is unofficial and not affiliated with OpenAI or Anthropic.
