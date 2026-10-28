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
