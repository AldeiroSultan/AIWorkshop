# Capstone Funding Tracker

A team dashboard for funding opportunities: which ones you're chasing, who is responsible, and what happens next. All data is fictional.

You'll use it in pairs in the AI skills workshop on 3 November. Before class, you only need to set it up.

## Before class

You need Python 3.11 or newer, Git, VS Code, and an AI chat extension for VS Code: **Claude Code** or **Codex**. Install it (or update it, if you already have it) and sign in.

Your AI reads the team's rules in [AGENTS.md](AGENTS.md) on its own.

1. **One person** makes your team's copy: click **Use this template** → **Create a new repository**. Make it public.
2. That person adds their partner: **Settings → Collaborators → Add people**. The partner accepts the invite from their email.
3. **Both of you** download it, then open the folder in VS Code (**File → Open Folder**):

   ```
   git clone <your team's repo URL>
   ```

4. Open your AI chat in VS Code and send this as your first message:

   ```
   Read README.md and set up this project for me. Only set it up: don't change any code. When it's done, start the app.
   ```

   Your AI may ask before it runs a command. Read what it wants to run, then allow it.

5. Open http://localhost:8000. If your page looks like the screenshot Tarik shared, you're done. See you in class!

## Setup steps

Your AI follows these. You can also run them yourself.

1. Make a virtual environment:

   ```
   python -m venv .venv
   ```

2. Turn it on:

   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
   - Mac: `source .venv/bin/activate`

3. Install and check:

   ```
   python -m pip install -r requirements.txt
   python check_setup.py
   ```

   Every line should say `[OK]`. If one says `[FIX]`, do what it says.

**Tips:** on a Mac, use `python3` if `python` doesn't work. If PowerShell says scripts are disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again.

## Run the app

```
python -m uvicorn app.main:app --reload
```

Then open http://localhost:8000

To start again with fresh data, stop the app, delete `data/opportunities.json`, and run it again.

## Run the tests

```
python -m pytest
```
