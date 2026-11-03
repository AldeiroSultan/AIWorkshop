"""Token tracker for your OpenCode chats about this project.

OpenCode stores every chat message in a local database, together with the token
counts the AI provider reported for it. This script reads those counts (it never
writes to the database) and prints them as tables:

  Read   the tokens the AI read before it answered: your message, the earlier
         messages, the files it opened, and the instructions it follows.
  Wrote  the tokens the AI wrote back, including its hidden reasoning tokens.

Run it from the project folder:

  python tools/token_tracker.py              # one row per chat, newest first
  python tools/token_tracker.py --turns      # message by message, newest chat
  python tools/token_tracker.py --turns --session ses_abc123
  python tools/token_tracker.py --all        # every project, not just this one

The numbers come from the provider, so a reply only shows up once it has
finished: token counts arrive at the end of each step.
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DATABASE_ENV_VAR = "OPENCODE_DB"
TOKEN_KEYS = ("fresh", "cache_read", "cache_write", "output", "reasoning")


def project_root():
    """The folder this script lives in, one level up."""
    return Path(__file__).resolve().parents[1]


def database_path():
    """Where OpenCode keeps its database, or the path you set yourself."""
    chosen = os.environ.get(DATABASE_ENV_VAR)
    if chosen:
        return Path(chosen)

    home = Path.home()
    shared = Path(os.environ.get("XDG_DATA_HOME") or home / ".local" / "share")
    candidates = [
        shared / "opencode" / "opencode.db",
        home / ".local" / "share" / "opencode" / "opencode.db",
        home / "AppData" / "Local" / "opencode" / "opencode.db",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def connect(path):
    """Open the database read-only, so this script can never change your chats."""
    if not Path(path).exists():
        raise SystemExit(
            f"No OpenCode database at {path}.\n"
            f"Chat with OpenCode once, or point {DATABASE_ENV_VAR} at that file."
        )
    connection = sqlite3.connect(f"file:{Path(path).as_posix()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def table_names(connection):
    """The tables in the database, so we can cope with older OpenCode versions."""
    rows = connection.execute("select name from sqlite_master where type = 'table'")
    return {row["name"] for row in rows}


def load_sessions(connection, tables):
    """Every chat OpenCode knows about, keyed by chat id.

    Older versions keep chats in `session`, newer ones in `session_v2`. The
    newer table is read last, so its row is the one you see.
    """
    sessions = {}
    for table in ("session", "session_v2"):
        if table not in tables:
            continue
        rows = connection.execute(
            f"select id, directory, title, time_updated from {table}"
        )
        for row in rows:
            sessions[row["id"]] = dict(row)
    return sessions


def is_inside_folder(directory, root):
    """True when a chat was started in this folder or a folder below it."""
    if not directory:
        return False
    try:
        Path(directory).resolve().relative_to(Path(root).resolve())
    except ValueError:
        return False
    return True


def load_messages(connection, tables, session_id):
    """One chat's messages, oldest first, each with its token counts."""
    if "session_message" in tables:
        rows = connection.execute(
            "select type, data, time_created from session_message "
            "where session_id = ? order by seq",
            (session_id,),
        ).fetchall()
        kind_is_a_column = True
    else:
        rows = connection.execute(
            "select data, time_created from message "
            "where session_id = ? order by time_created",
            (session_id,),
        ).fetchall()
        kind_is_a_column = False

    messages = []
    for row in rows:
        data = json.loads(row["data"])
        messages.append(
            {
                "kind": row["type"] if kind_is_a_column else data.get("role", ""),
                "time": row["time_created"],
                "text": message_text(data),
                "tokens": token_counts(data),
            }
        )
    return messages


def message_text(data):
    """The words someone typed, or an empty string when a message has none."""
    text = data.get("text")
    if not text:
        text = (data.get("metadata") or {}).get("displayText", "")
    return text or ""


def token_counts(data):
    """The provider's token report for one message, as plain numbers."""
    tokens = data.get("tokens") or {}
    cache = tokens.get("cache") or {}
    return {
        "fresh": tokens.get("input", 0) or 0,
        "cache_read": cache.get("read", 0) or 0,
        "cache_write": cache.get("write", 0) or 0,
        "output": tokens.get("output", 0) or 0,
        "reasoning": tokens.get("reasoning", 0) or 0,
    }


def empty_totals():
    """All the counters we add up, starting at zero."""
    totals = {key: 0 for key in TOKEN_KEYS}
    totals["steps"] = 0
    return totals


def add_totals(into, other):
    """Add one set of totals into another."""
    for key in TOKEN_KEYS:
        into[key] += other.get(key, 0)
    into["steps"] += other.get("steps", 0)


def add_tokens(totals, counts):
    """Count one finished AI message as a step of a turn."""
    add_totals(totals, counts)
    totals["steps"] += 1


def build_turns(messages):
    """Group messages into turns: one message you sent, plus the AI's replies."""
    turns = []
    for message in messages:
        if message["kind"] == "user":
            turn = {"time": message["time"], "text": message["text"]}
            turn.update(empty_totals())
            turns.append(turn)
        elif message["kind"] == "assistant" and turns:
            add_tokens(turns[-1], message["tokens"])
    return turns


def prompt_tokens(totals):
    """Everything the AI read: new tokens plus the ones it reused from cache."""
    return totals["fresh"] + totals["cache_read"] + totals["cache_write"]


def reply_tokens(totals):
    """Everything the AI wrote: the reply plus its hidden reasoning."""
    return totals["output"] + totals["reasoning"]


def total_tokens(totals):
    return prompt_tokens(totals) + reply_tokens(totals)


def shorten(text, limit):
    """Squash text onto one line and cut it to fit a table column."""
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def clock(milliseconds):
    return datetime.fromtimestamp(milliseconds / 1000).strftime("%Y-%m-%d %H:%M")


def print_table(headers, rows, text_columns):
    """Print a plain table; the first `text_columns` columns are left-aligned."""
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def as_line(cells):
        parts = []
        for index, cell in enumerate(cells):
            if index < text_columns:
                parts.append(cell.ljust(widths[index]))
            else:
                parts.append(cell.rjust(widths[index]))
        return "  ".join(parts)

    print(as_line(headers))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print(as_line(row))


def show_sessions(connection, tables, sessions):
    """One row per chat, newest first."""
    rows = []
    totals = empty_totals()

    newest_first = sorted(
        sessions.values(), key=lambda session: session["time_updated"] or 0, reverse=True
    )
    for session in newest_first:
        turns = build_turns(load_messages(connection, tables, session["id"]))
        chat = empty_totals()
        for turn in turns:
            add_totals(chat, turn)
        add_totals(totals, chat)

        rows.append(
            [
                session["id"][:16],
                shorten(session["title"] or "(untitled)", 26),
                f"{chat['steps']:,}",
                f"{prompt_tokens(chat):,}",
                f"{chat['cache_read']:,}",
                f"{chat['output']:,}",
                f"{chat['reasoning']:,}",
                f"{total_tokens(chat):,}",
            ]
        )

    print(f"Chats in {project_root()} (newest first)\n")
    print_table(
        ["Chat", "Title", "Steps", "Read", "Cached", "Wrote", "Reason", "Total"],
        rows,
        2,
    )
    print()
    print(
        f"{len(rows)} chats: {prompt_tokens(totals):,} tokens read, "
        f"{reply_tokens(totals):,} tokens written."
    )
    print("Add --turns to see one chat message by message.")


def show_turns(connection, tables, session):
    """One row per turn of one chat."""
    turns = build_turns(load_messages(connection, tables, session["id"]))

    print(session["title"] or "(untitled)")
    print(f"{session['id']}   {session['directory']}")
    if not turns:
        print("\nNo finished messages in this chat yet.")
        return

    rows = []
    totals = empty_totals()
    for number, turn in enumerate(turns, start=1):
        add_totals(totals, turn)
        rows.append(
            [
                f"{number}",
                clock(turn["time"]),
                shorten(turn["text"], 24),
                f"{prompt_tokens(turn):,}",
                f"{turn['fresh']:,}",
                f"{turn['cache_read']:,}",
                f"{turn['output']:,}",
                f"{turn['reasoning']:,}",
                f"{total_tokens(turn):,}",
            ]
        )

    print()
    print_table(
        ["#", "When", "You said", "Read", "Fresh", "Cached", "Wrote", "Reason", "Total"],
        rows,
        3,
    )
    print()
    print(
        f"All {len(turns)} turns: {prompt_tokens(totals):,} tokens read, "
        f"{reply_tokens(totals):,} tokens written."
    )
    print()
    print("Read    everything the AI read, including your message and the files it opened")
    print("Fresh   read for the first time; Cached was already stored, so it is cheaper")
    print("Wrote   the reply you received; Reason is hidden thinking inside that reply")
    print("Steps   one round of reading and writing; a turn that uses tools has several")


def pick_session(sessions, wanted):
    """The chat you asked for, or the one you used most recently."""
    if not wanted:
        return max(sessions.values(), key=lambda session: session["time_updated"] or 0)

    matches = [
        session for session_id, session in sessions.items() if session_id.startswith(wanted)
    ]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise SystemExit(f"No chat starts with {wanted}.")
    raise SystemExit(f"{len(matches)} chats start with {wanted}; type more of the id.")


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # odd characters must not crash the printout

    parser = argparse.ArgumentParser(
        description="Show how many tokens your OpenCode chats about this project used."
    )
    parser.add_argument(
        "--turns",
        action="store_true",
        help="list every message instead of one row per chat",
    )
    parser.add_argument(
        "--session",
        metavar="ID",
        help="chat to show with --turns (default: the newest one)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="include chats from every project, not just this folder",
    )
    parser.add_argument(
        "--db",
        metavar="PATH",
        help=f"database file (default: the {DATABASE_ENV_VAR} variable, then the usual OpenCode folder)",
    )
    args = parser.parse_args(argv)

    path = Path(args.db) if args.db else database_path()
    connection = connect(path)
    tables = table_names(connection)

    root = project_root()
    sessions = load_sessions(connection, tables)
    if not args.all:
        sessions = {
            session_id: session
            for session_id, session in sessions.items()
            if is_inside_folder(session["directory"], root)
        }

    if not sessions:
        print(f"No OpenCode chats found for {root}.")
        print("Start one from this folder, or run with --all to see every project.")
        return 1

    if args.turns:
        show_turns(connection, tables, pick_session(sessions, args.session))
    else:
        show_sessions(connection, tables, sessions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
