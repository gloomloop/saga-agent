"""
A FastMCP server for the SAGA Engine Server.

This server provides a tool-based interface for an LLM agent to interact
with the Go-based game engine.

Run with: python saga_mcp.py <session_id>
"""

from __future__ import annotations

import json
import sys
from typing import Dict, Any, Optional

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SAGA Engine ServerMCP")

# ────────────────────────────────────────────────────────────────────────────────
# Configuration
# ────────────────────────────────────────────────────────────────────────────────
GO_SERVER_URL = "http://localhost:8080"

# Get session ID from command line argument
if len(sys.argv) != 2:
    print("Usage: python saga_mcp.py <session_id>")
    sys.exit(1)

SESSION_ID = sys.argv[1]


# ────────────────────────────────────────────────────────────────────────────────
# Helper Function to Interact with the Go Server
# ────────────────────────────────────────────────────────────────────────────────
def _call_game_api(endpoint: str, payload: Optional[Dict[str, Any]] = {}) -> Dict[str, Any]:
    """
    Sends a request to the Go game server and returns the JSON response.

    Parameters
    ----------
    endpoint : str
        The API endpoint to call (e.g., "/observe").
    payload : Dict[str, Any], optional
        The JSON payload to send with the request.

    Returns
    -------
    Dict[str, Any]
        The JSON response from the server.
    """
    url = f"{GO_SERVER_URL}/api/v1/sessions/{SESSION_ID}{endpoint}"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    return response.json()


# ────────────────────────────────────────────────────────────────────────────────
# 👀 Observe Tool
# ────────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def observe() -> Dict[str, Any]:
    """
    Observe the current room.

    Example
    -------
    ```json
    {
        "tool": "observe",
        "args": {}
    }
    ```
    """
    return _call_game_api("/observe")


# ────────────────────────────────────────────────────────────────────────────────
# 🔍 Inspect Tool
# ────────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def inspect(target_name: str) -> Dict[str, Any]:
    """
    Inspect a specific entity in the current room.
    Supports items and doors.

    Example
    -------
    ```json
    {
        "tool": "inspect",
        "args": {"target_name": "chest"}
    }
    ```
    """
    return _call_game_api("/inspect", {"target_name": target_name})


# ────────────────────────────────────────────────────────────────────────────────
# 🔓 Uncover Tool
# ────────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def uncover(target_name: str) -> Dict[str, Any]:
    """
    Look under or move aside to reveal something hidden.

    Example
    -------
    ```json
    {
        "tool": "uncover",
        "args": {"target_name": "pile of leaves"}
    }
    ```
    """
    return _call_game_api("/uncover", {"target_name": target_name})


# ────────────────────────────────────────────────────────────────────────────────
# 🔑 Unlock Tool
# ────────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def unlock(key_or_code: str, target_name: str) -> Dict[str, Any]:
    """
    Unlock a door or container using a key (by name) or code.

    Example
    -------
    ```json
    {
        "tool": "unlock",
        "args": {"key_or_code": "1234", "target_name": "safe"}
    }
    ```
    """
    return _call_game_api("/unlock", {"key_or_code": key_or_code, "target_name": target_name})


# ────────────────────────────────────────────────────────────────────────────────
# 🔎 Search Tool
# ────────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def search(target_name: str) -> Dict[str, Any]:
    """
    Search inside a container for hidden items.
    Does not actually take an item.

    Example
    -------
    ```json
    {
        "tool": "search",
        "args": {"target_name": "drawer"}
    }
    ```
    """
    return _call_game_api("/search", {"target_name": target_name})


# ────────────────────────────────────────────────────────────────────────────────
# 📦 Take Tool
# ────────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def take(target_name: str) -> Dict[str, Any]:
    """
    Pick up an item and add it to your inventory.
    Only keys, weapons, ammo boxes, health items and items marked as portable can be taken.

    Example
    -------
    ```json
    {
        "tool": "take",
        "args": {"target_name": "rusty crowbar"}
    }
    ```
    """
    return _call_game_api("/take", {"target_name": target_name})


# ────────────────────────────────────────────────────────────────────────────────
# 🎒 Inventory Tool
# ────────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def inventory() -> Dict[str, Any]:
    """
    Check your current inventory and ammunition.

    Example
    -------
    ```json
    {
        "tool": "inventory",
        "args": {}
    }
    ```
    """
    return _call_game_api("/inventory")


# ────────────────────────────────────────────────────────────────────────────────
# 💊 Heal Tool
# ────────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def heal(health_item_name: str) -> Dict[str, Any]:
    """
    Use a health item from your inventory to restore health.

    Example
    -------
    ```json
    {
        "tool": "heal",
        "args": {"health_item_name": "gauze bandage"}
    }
    ```
    """
    return _call_game_api("/heal", {"health_item_name": health_item_name})


# ────────────────────────────────────────────────────────────────────────────────
# 🚪 Traverse Tool
# ────────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def traverse(door_or_direction: str) -> Dict[str, Any]:
    """
    Move to a different room. Supports both door names and relative directions.

    Example
    -------
    ```json
    {
        "tool": "traverse",
        "args": {"door_or_direction": "front door"}
    }
    ```
    """
    return _call_game_api("/traverse", {"door_or_direction": door_or_direction})


# ────────────────────────────────────────────────────────────────────────────────
# ⚔️ Battle Tool
# ────────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def battle(weapon_name: str = "fists") -> Dict[str, Any]:
    """
    Attack an enemy using a weapon from your inventory.
    Defaults to hand-to-hand combat if no weapon is provided.

    Example
    -------
    ```json
    {
        "tool": "battle",
        "args": {"weapon_name": "sword"}
    }
    ```
    """
    return _call_game_api("/battle", {"weapon_name": weapon_name})


# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"🚀 Starting SAGA Engine Server MCP Server for session {SESSION_ID}...")
    print("Agent can now use: observe, inspect, uncover, unlock, search, take, inventory, heal, traverse, battle")
    mcp.run()  # Runs with stdio transport by default
