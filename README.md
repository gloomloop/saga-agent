# SAGA Engine Agent

SAGA (Structured Adventure Game Agent) Engine Agent is an interactive storytelling LLM agent that communicates with a game state server via tool-calling. It is part of the SAGA Engine, along with the [SAGA Engine Server](https://github.com/gloomloop/saga-server).

## Background

The idea is to combine the narrative generation capabilities of LLMs with the structure of a traditional text-based puzzle game.

An LLM agent is given a curated set of tools for interacting with a purpose-built text adventure game server. In a REPL-like loop, the agent describes the current state of the game, waits for player input, maps that input to a tool call and reports the response, while remaining in-character.

## Demo
Below is an example gameplay transcript, using a thin MCP (Model Context Protocol) server wrapper around the game server API and an off-the-shelf MCP client, [MCPHost](https://github.com/mark3labs/mcphost). The model is GPT-4o (likely overkill). The game definition JSON can be found [here](https://github.com/gloomloop/saga-server/blob/main/internal/testdata/demo.yaml).


🧑 <span style="color: #1E90FF;"><strong>user:</strong> where am i</span>

🛠️ <span style="color: #DAA520;"><strong>tool call:</strong> saga-engine-server__observe {}</span>

🤖 <span style="color: #20B2AA;"><strong>assistant:</strong> You find yourself in a dilapidated waiting room, the air thick with dust and a sense of abandonment. Shadows dance across the peeling wallpaper, and the atmosphere is heavy with an eerie silence. In the middle of the floor, a tattered grey hoodie lies, as if discarded in haste. It seems to be hiding something beneath it.

Nearby, an unopened energy drink sits, a small beacon of life in this forsaken place. It might offer some rejuvenation if needed.

To the west stands a metal stairwell door, locked and foreboding, its purpose concealed by a key lock. To the north, an office door invites investigation, while to the east, a storage room door waits to be explored. Each path promises its own secrets and dangers.</span>

🧑 <span style="color: #1E90FF;"><strong>user:</strong> inspect the drink</span>

🛠️ <span style="color: #DAA520;"><strong>tool call:</strong> saga-engine-server__inspect {"target_name":"energy drink"}</span>

🤖 <span style="color: #20B2AA;"><strong>assistant:</strong> The energy drink is labeled "NRG-9001," promising to "unleash your inner beast." It's unopened and seems to be in good condition, offering a burst of energy and possibly a vital boost to your health. It might be wise to take it with you, should you need some revitalization in the near future.</span>

🧑 <span style="color: #1E90FF;"><strong>user:</strong> take it</span>

🛠️ <span style="color: #DAA520;"><strong>tool call:</strong> saga-engine-server__take {"target_name":"energy drink"}</span>

🤖 <span style="color: #20B2AA;"><strong>assistant:</strong> You carefully pick up the energy drink, feeling its cold, metallic surface in your hand. Now safely in your possession, it promises a surge of vitality when you need it most. The room remains silent, waiting for your next move.</span>