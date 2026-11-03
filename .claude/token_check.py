"""Token checker hook for Claude Code (standard library only).

Called by two hooks (see settings.local.json):
  UserPromptSubmit -> shows the estimated tokens of the message you just sent
  Stop             -> shows the real tokens used by Claude's reply

Claude Code sends a JSON object on stdin. We print JSON with a
"systemMessage", which Claude Code shows to the user.
"""
import json
import sys


def read_transcript(path):
    """Return every line of the transcript file as a dict."""
    rows = []
    with open(path) as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except ValueError:
                pass  # skip a broken line
    return rows


def is_user_prompt(row):
    """True for a message the user typed (not a tool result)."""
    if row.get("type") != "user":
        return False
    content = row.get("message", {}).get("content")
    if isinstance(content, str):
        return True
    return any(part.get("type") == "text" for part in content or [])


def reply_usage(rows):
    """Add up the usage of the assistant entries after the last user prompt."""
    start = 0
    for i, row in enumerate(rows):
        if is_user_prompt(row):
            start = i

    # One reply can be written to the file several times; keep the last copy.
    by_id = {}
    for row in rows[start:]:
        if row.get("type") == "assistant":
            message = row.get("message", {})
            by_id[message.get("id", row.get("uuid"))] = message.get("usage", {})

    usages = list(by_id.values())
    total_out = sum(u.get("output_tokens", 0) for u in usages)
    last = usages[-1] if usages else {}
    context = (
        last.get("input_tokens", 0)
        + last.get("cache_read_input_tokens", 0)
        + last.get("cache_creation_input_tokens", 0)
    )
    return total_out, context, len(usages)


def main():
    data = json.load(sys.stdin)
    event = data.get("hook_event_name")

    if event == "UserPromptSubmit":
        # There is no free exact tokenizer, so estimate: about 4 characters per token.
        estimate = max(1, len(data.get("prompt", "")) // 4)
        text = f"Token check - your message: ~{estimate} tokens (estimate)"
    elif event == "Stop":
        out_tokens, context, calls = reply_usage(read_transcript(data["transcript_path"]))
        text = (
            f"Token check - my reply: {out_tokens} output tokens "
            f"({calls} model calls) | context size now: {context} tokens"
        )
    else:
        return

    print(json.dumps({"systemMessage": text}))


main()
