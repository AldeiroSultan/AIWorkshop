# Part 2: Fix the rules

Work together with your partner.

Your AI did exactly what `AGENTS.md` told it. Some of those rules were wrong, and nobody checked them. Now you'll fix the rules and see how your AI's answer changes.

## Fix the rules file

1. Read `AGENTS.md` together. For each rule, ask: is it true? Did anyone check it with the client? Ask Tarik, your client, about anything you're not sure of.
2. Fix the wrong rules. Write exactly what you mean, so your AI doesn't have to guess.
3. Start a **new chat** with your AI, so it reads your new rules. Ask it to do Task 1 again.
4. Check your AI's work with different cases, not just the tests that already pass:
   - a deadline today, tomorrow and yesterday
   - a row that's already Submitted, Successful or Unsuccessful

   Look at the page for the rows you have. Ask your AI to add tests for the rest, then run `python -m pytest`.
5. Talk about it: what changed between your AI's first answer and this one? Why?

When you're happy with it, share it the same way as Task 1: branch, pull request, review, merge.

## If you have time: make it yours

Pick one small improvement you'd like in the app, and build it with your AI. For example, a filter by owner, or the total amount at the top of the page. Check it the same way: look at the page, not just the tests.
