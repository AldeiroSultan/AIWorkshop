import json
import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import token_tracker


def make_database(tmp_path):
    """A tiny stand-in for OpenCode's database."""
    path = tmp_path / "opencode.db"
    connection = sqlite3.connect(path)
    connection.executescript(
        """
        create table session (
            id text primary key,
            directory text,
            title text,
            time_updated integer
        );
        create table session_message (
            id text,
            session_id text,
            type text,
            seq integer,
            time_created integer,
            data text
        );
        """
    )
    connection.execute(
        "insert into session values (?, ?, ?, ?)",
        ("ses_test", str(tmp_path), "Test chat", 1000),
    )

    def add_message(seq, kind, text, tokens=None):
        data = {"text": text}
        if tokens:
            data["tokens"] = tokens
        connection.execute(
            "insert into session_message values (?, ?, ?, ?, ?, ?)",
            (f"msg_{seq}", "ses_test", kind, seq, seq * 1000, json.dumps(data)),
        )

    add_message(0, "user", "How many tokens did this cost?")
    add_message(
        1,
        "assistant",
        "",
        {"input": 1000, "output": 200, "reasoning": 50, "cache": {"read": 500, "write": 0}},
    )
    add_message(
        2,
        "assistant",
        "",
        {"input": 20, "output": 30, "reasoning": 0, "cache": {"read": 800, "write": 0}},
    )
    add_message(3, "user", "Thanks")
    connection.commit()
    connection.close()
    return path


def test_turns_add_up_the_numbers_the_provider_sent(tmp_path):
    connection = token_tracker.connect(make_database(tmp_path))
    tables = token_tracker.table_names(connection)

    turns = token_tracker.build_turns(
        token_tracker.load_messages(connection, tables, "ses_test")
    )

    assert len(turns) == 2
    first, second = turns

    # Two AI steps reply to the first message.
    assert first["steps"] == 2
    assert first["fresh"] == 1020
    assert first["cache_read"] == 1300
    assert first["output"] == 230
    assert first["reasoning"] == 50
    assert token_tracker.prompt_tokens(first) == 2320
    assert token_tracker.reply_tokens(first) == 280
    assert token_tracker.total_tokens(first) == 2600

    # The second message has no reply yet, so it counts as zero.
    assert second["steps"] == 0
    assert token_tracker.total_tokens(second) == 0


def test_database_is_opened_read_only(tmp_path):
    connection = token_tracker.connect(make_database(tmp_path))

    with pytest.raises(sqlite3.OperationalError):
        connection.execute("delete from session_message")


def test_missing_database_stops_with_a_helpful_message(tmp_path):
    with pytest.raises(SystemExit):
        token_tracker.connect(tmp_path / "nope.db")


def test_folders_are_matched_by_location(tmp_path):
    root = tmp_path / "project"

    assert token_tracker.is_inside_folder(str(root), root)
    assert token_tracker.is_inside_folder(str(root / "sub"), root)
    assert not token_tracker.is_inside_folder(str(tmp_path / "project-2"), root)
    assert not token_tracker.is_inside_folder("", root)


def test_newer_session_table_wins(tmp_path):
    path = make_database(tmp_path)
    connection = sqlite3.connect(path)
    connection.execute(
        "create table session_v2 ("
        "id text primary key, directory text, title text, time_updated integer)"
    )
    connection.execute(
        "insert into session_v2 values ('ses_test', '.', 'Newer title', 2000)"
    )
    connection.commit()
    connection.close()

    connection = token_tracker.connect(path)
    sessions = token_tracker.load_sessions(
        connection, token_tracker.table_names(connection)
    )

    assert sessions["ses_test"]["title"] == "Newer title"


def test_database_path_can_be_set_with_an_environment_variable(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENCODE_DB", str(tmp_path / "chosen.db"))

    assert token_tracker.database_path() == tmp_path / "chosen.db"
