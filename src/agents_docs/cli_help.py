"""ANSI formatting and help emitter for agents-docs CLI."""

from __future__ import annotations

import argparse
import json
import sys


def emit_help_json(argv: list[str], parser: argparse.ArgumentParser, name: str = "agents-docs") -> None:
    """Emit machine-readable CLI specification as JSON, including subcommands."""
    actions = []
    commands = []
    for action in parser._actions:
        if action.dest == "help":
            continue
        if isinstance(action, argparse._SubParsersAction):
            helps = {}
            for choice in getattr(action, "_choices_actions", []):
                helps[choice.dest] = choice.help or ""
            for cmd, sub in action.choices.items():
                commands.append({
                    "name": cmd,
                    "help": helps.get(cmd) or (sub.description or ""),
                })
            continue
        actions.append({
            "dest": action.dest,
            "option_strings": action.option_strings,
            "help": action.help or "",
            "default": str(action.default) if action.default is not None else None,
            "required": action.required,
        })
    payload = {
        "command": name,
        "description": parser.description or "",
        "arguments": actions,
        "commands": commands,
    }
    print(json.dumps(payload, indent=2))
