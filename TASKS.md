# Your tasks

Save this file as `TASKS.md` in your project folder, next to `README.md`.

Work in pairs. Each of you builds Task 1 on your own, with AI. Use AI however you like. Then you compare, keep one version, and do Task 2 together.

Tarik plays your client. You can ask questions at any time.

## Task 1: Deadline colours

Make deadlines easy to see in the table:

- Late deadlines are red and say "Overdue".
- Deadlines in the next 7 days are yellow and say "Due in 3 days" (or however many days).
- A deadline today says "Due today".

**Files:** `static/deadlines.js` and `static/deadlines.css`

**Done when:** you can see the colours on the page, every label matches the rules above, and `python -m pytest` passes. Passing tests alone doesn't prove it works, so check the page too.

### Share your work

1. Make your own branch: `git switch -c task1-yourname` (for example `task1-maya`).
2. Build Task 1 with AI. Commit as you go.
3. Push: `git push -u origin task1-yourname`
4. Open a pull request on GitHub. Fill in the form.
5. Review each other's pull request, with AI's help. Talk about it: how did your two AIs solve it differently? Which do you prefer, and why?
6. Together, pick the better one and merge it. Close the other one with **Close pull request**. Don't merge both: they change the same files, so they would clash.
7. Both of you get the latest version: `git switch main`, then `git pull`.

## Task 2: Team notes (together)

Do this together, after you've merged one version of Task 1.

Each of you writes one line about how **you** solved Task 1. You both add it to the bottom of the same file, so GitHub will show a merge conflict. That's the point: you'll practise fixing one.

1. Both of you get the latest version: `git switch main`, then `git pull`.
2. Each of you makes your own branch: `git switch -c notes-yourname` (for example `notes-maya`).
3. Open `TEAM_NOTES.md` (not this file). At the bottom, add one line in your own words: what you asked your AI, and what you checked. Start it with your name. For example:

   ```markdown
   - **Maya:** I asked my AI to ... Then I checked ...
   ```

4. Commit, push, and open a pull request. Both of you. **Don't merge anything until both pull requests are open.**
5. Merge one pull request. The other one now says **This branch has conflicts**. Fix it together, using the steps below.

You can ask your AI to explain the conflict, but fix it yourselves.

**File:** `TEAM_NOTES.md`

**Done when:** both pull requests are merged, and `TEAM_NOTES.md` on GitHub shows both lines.

## When GitHub says "This branch has conflicts"

You both added a line to the bottom of `TEAM_NOTES.md`, so whoever merges second gets a conflict. Git can't choose which line to keep, so you choose.

1. On the pull request, click **Resolve conflicts**.
2. You'll see both lines between markers, something like this:

   ```
   <<<<<<< notes-sam
   - **Sam:** ...
   =======
   - **Maya:** ...
   >>>>>>> main
   ```

3. Keep both lines. Delete the three marker lines (`<<<<<<<`, `=======`, `>>>>>>>`).
4. Click **Mark as resolved**, then **Commit merge**.
5. Wait for the tests to pass, then merge the pull request.
6. Open `TEAM_NOTES.md` on GitHub. Check that both lines are there and no markers are left.
