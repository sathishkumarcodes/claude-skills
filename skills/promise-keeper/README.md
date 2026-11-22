# Promise Keeper

**Never forget a promise you made in an email.**

Promise Keeper is a Claude skill. It reads your sent mail, chats and meeting notes, finds every time you said you'd do something ("I'll send that Friday", "let me get back to you", "I can take that one"), and tracks each one until it's done. It also tracks two related things:

- **Asked of you**: requests and questions people sent you that you haven't answered yet.
- **Waiting on others**: replies and promised items that other people owe you.

Most to-do apps only track tasks you type in yourself. Promise Keeper catches the ones you agreed to in passing and then forgot.

---

## Quick start

1. **Install the skill.** Build the ZIP with `./scripts/package.sh promise-keeper` (or download it from the repo's Actions artifacts), then upload it in Claude under Customize > Skills. See the [repo README](../../README.md#installing-a-skill-in-claude) for the steps.
2. **Connect at least one source.** Gmail is the easiest place to start (see [Sources](#sources)).
3. **Ask for it** in any chat:

   ```
   Run promise keeper
   ```

The first run scans the last 14 days. After that, each run picks up from the last scan.

---

## What you can ask

| Say something like | View | What you get |
|---|---|---|
| "Run promise keeper", "Any loose ends?" | **Full** | Everything, ordered by urgency |
| "What's needed from me?", "What do I owe people?" | **Needed from me** | Your open promises plus unanswered requests, overdue first |
| "Who am I waiting on?", "Who hasn't replied?" | **Waiting on others** | People who owe you something, longest silence first |
| "What did I get done in the last 7 days?" | **Done in last N days** | Items closed in that window. Any number works; 7 if you don't say |
| "Anything urgent?", "What needs me today?" | **Urgent** | Only what's pressing, each with a one-line reason |

You can combine views ("What's needed from me and anything urgent?") and add filters:

```
Scan the last 90 days
Who's been quiet for more than 2 weeks?
What did I close in the last 3 days?
```

---

## Example report

> **Promise Keeper** · Mar 14 · scanned Mar 1 – Mar 14 · 4 open, 1 overdue
>
> **🔴 Overdue**
> - Send Priya the Q1 budget deck. You wrote *"I'll send it over by Friday"*. Due Mar 6 (stated) · **8 days late** · [open email]
>
> **🟠 Due today**
> - Get back to Marcus on the vendor contract. You wrote *"Let me check with legal and get back to you"*. Due Mar 14 (inferred) · [open thread]
>
> **🟡 This week**
> - Intro Dana to the design team. You wrote *"Happy to make the intro"*. Due Mar 17 (inferred) · [open message]
>
> **📥 Asked of you**
> - Review the onboarding doc, which Leo asked for on Mar 12 and has followed up on once · **urgent** · [open email]
>
> **✅ Probably done (confirm?)**
> - Call Sam back about the offsite. A phone call, so there's no email proof
>
> **⏳ Waiting on others**
> - Jordan (contract signature): 12 days · Alex (expense approval): 6 days (3 follow-ups sent)
>
> Want me to draft replies for the overdue items?

Every item shows your exact words, who it's with, the due date and a link back to the original message.

---

## How it works

1. **Scan.** It reads your sent messages to find promises and things you're waiting on, and your inbox to find requests addressed to you.
2. **Detect.** It picks out real commitments and skips pleasantries like "let's grab coffee sometime".
3. **Date.** It works out each due date from when the message was **sent**, so "Friday" means the Friday after that email. Each date is marked **stated** (you gave it) or **inferred** (a default was used).
4. **Verify.** It reads the rest of each thread for proof the item was done, such as an attachment, a confirmed meeting or a thank-you. Items with proof are marked done. If the proof is weaker, they're marked *probably done* for you to confirm.
5. **Record.** It updates a running list (the ledger) so nothing is lost between runs.
6. **Report.** It shows the view you asked for.
7. **Help close the loop.** For overdue items it offers draft replies (see [Drafting replies](#drafting-replies)).

### Default due dates

| Your words | Due |
|---|---|
| "today", "EOD" | That day |
| "tomorrow" | The next day |
| "Friday" | The next Friday after the message |
| "this week" | Friday of that week |
| "next week" | Friday of the following week |
| "end of month" | The last business day of that month |
| "ASAP", "shortly", "get back to you" | 2 business days later *(inferred)* |
| No time given | 5 business days later *(inferred)* |

### What counts as urgent

An open item is **urgent** if any of these is true:

- It's overdue, or due today or tomorrow.
- The request says *urgent*, *ASAP*, *EOD*, *today* or *deadline*.
- Someone has already followed up on it ("just following up", "any update?").
- It's tied to a meeting, interview or call in the next 48 hours.

Items you're waiting on from others only count as urgent if you're blocked on them before an event in the next 48 hours.

---

## The ledger

Promise Keeper keeps its running list as a **Claude Sheet** called **Promise Keeper** with three tabs:

| Tab | Columns |
|---|---|
| **Promises** | What · To · Due · Stated/Inferred · Status · Made on · Closed on · Your words · Link · Confidence |
| **Asked of you** | What · From · Due · Stated/Inferred · Status · Asked on · Closed on · Their words · Link · Urgent |
| **Waiting on others** | Who · Waiting for · Since · Days quiet · Follow-ups sent · Status · Closed on · Link |

- **Edit it freely.** Change a status, delete a row or add notes. Promise Keeper keeps your edits and never reopens an item you've marked done or dropped.
- **Days quiet** updates itself every day.
- You can **download** the sheet as an .xlsx or CSV file from its page.

If Sheets isn't available, it falls back to a Tasks list, then to a `promise-keeper.md` file.

---

## Sources

| Source | How to connect | Covers |
|---|---|---|
| **Gmail** | Gmail connector | Sent mail and inbox |
| **Outlook + Teams** | Microsoft 365 connector | Email and Teams chats |
| **Slack** | Slack connector | DMs, group DMs and channels |
| **Google Drive** | Google Drive connector | Meeting notes in Google Docs |
| **Meeting recorders** | Grain, Otter, Granola or Zoom, where a connector exists | Your lines and action items assigned to you |
| **Calendar** | Calendar connector | Context only: who a meeting was with, and what's coming up |
| **Telegram** | Export chats as JSON from Telegram Desktop (Settings → Advanced → Export Telegram data) and upload the file | Your messages |
| **Discord** | Request your data package (Settings → Data & Privacy) and upload it | Your messages |
| **Anything else** | Paste the text into the chat | Whatever you paste |

Connect apps from your claude.ai connector settings. If nothing is connected, Promise Keeper suggests connectors and offers to scan pasted text instead.

---

## Drafting replies

For each overdue or due-today item, Promise Keeper can draft one of three replies:

- **Deliver**: send what you promised, if Claude can put it together.
- **Renegotiate**: a short, honest note asking for more time ("Running behind on the deck, can I get it to you Tuesday?").
- **Release**: a polite note handing the task back if you won't do it.

Drafts are saved in your email app (for example, Gmail Drafts). **Nothing is ever sent without your explicit OK for that specific message.**

---

## Run it automatically

Ask Claude:

```
Run promise keeper every weekday at 8:30am
```

This creates a **scheduled task** that rescans each morning, updates the ledger and reports only what's urgent or due that day. You can change or delete it in your scheduled tasks at any time.

---

## Privacy and safety

- **Read-only by default.** Scanning never changes anything in your apps.
- **No sending.** Replies are only drafted; you send them.
- **Your words only.** Only messages you wrote count as your promises, and only messages addressed to you count as requests.
- **Short quotes.** The ledger keeps a short quote from each message, not the whole message.
- **Private ledger.** The Promise Keeper sheet is visible only to you unless you share it.

---

## Limits

- **Phone calls and in-person promises** aren't visible unless they show up in notes or a follow-up message. Promise Keeper marks these *probably done* rather than guessing.
- **Telegram and Discord** need a manual export. No connector can read personal chats or DMs.
- **Automated emails** (no-reply senders, notification systems) are skipped. Required steps buried in a scheduling email may still be flagged at low confidence.
- **Low-confidence items** are included on purpose. Dropping a false alarm takes one click; a missed promise is what this skill exists to prevent.

---

## Testing and evals

Promise Keeper comes with a test set in its `evals/` folder: **14 test cases with 89 pass/fail checks**, plus **20 trigger tests** in `trigger-evals.json`. All test data is invented. The test user is "Jamie," and the test date is fixed at Friday, March 13, 2026, so every due date and day count has one right answer.

### What's tested

| Area | Cases |
|---|---|
| Finding and filtering promises | `full-report-from-mailbox` |
| Due-date rules and stated/guessed labels | `resolves-due-dates` |
| The five views | `view-needed-from-me`, `view-waiting-on-others`, `view-waiting-quiet-filter`, `view-done-last-n-days`, `view-urgent`, `combined-views` |
| Scan windows and later runs | `custom-window-7-days`, `later-run-respects-ledger` |
| Other sources | `telegram-export`, `pasted-slack-text`, `no-source-available` |
| Drafting replies without sending | `drafts-for-overdue` |

The test data is a 24-thread mailbox (each thread tests one rule), standup notes, an earlier ledger and a Telegram export. `evals-answer-key.json` says what each thread should produce. To change the tests, edit `evals-src/fixtures.py` and `evals-src/build_evals.py`, then run `python3 evals-src/build_evals.py .` from this folder to rebuild `evals/`.

Full results from the latest run are in `eval-results/iteration-1/`. `results.html` shows each case's output with and without the skill, plus the scores. `benchmark.md` is the summary.

### Latest results (iteration 1)

Each case was run once with the skill and once without it, and graded against the same checks.

| | With skill | Without skill |
|---|---|---|
| Checks passed | **88 / 89 (99%)** | 76 / 89 (86%) |
| Average time per run | 71 seconds | 32 seconds |
| Average tokens per run | ~61,000 | ~52,000 |

**Where the skill made the difference:**
- Due dates worked out from the send date and labeled stated or guessed. Without the skill, soft promises got no date or a wrong one.
- Days quiet counted from the user's last follow-up, sorted longest silence first.
- Asking for one view returned only that view.
- Every promise quoted the user's own words, and overdue items came first.

**Known issues to fix:**
1. A promise kept by phone (only "as discussed" in a later email) was marked done instead of probably done. This was the one failed check.
2. A request that was asked and already answered was counted as a closed promise.
3. In the needed-from-me view, an ASAP item and an item due today were sorted below items due weeks later.
4. "Last 5 days" covered 6 days, because it counted both ends.
5. A later scan only looks back to the last scan date, so items an earlier scan missed are never picked up.

**Weak tests:** 6 cases (urgent, combined views, 7-day window, drafts, Telegram, no source) passed both with and without the skill, so they need stricter checks to show what the skill adds.

### Running the tests

- **In Claude:** ask "run the promise-keeper evals". Claude runs each case with and without the skill, grades the checks and builds a results page with two tabs: Outputs (side-by-side replies) and Benchmark (scores).
- **In Claude Code:** from the skill folder, run `claude plugin eval . --allow-tools Write,Edit,Bash --scaffold`. These are real, billed model runs.

---

## FAQ

**It flagged something that isn't really a promise.**
Set its status to *Dropped* in the ledger. It won't come back.

**It missed one.**
Tell Claude ("I also promised Sam the slides by Monday") and it will add the item to the ledger.

**How far back can it scan?**
As far back as you like ("scan the last 6 months"). Longer windows take longer to run.

**Can I use it for work and personal email together?**
Yes. Connect both accounts and it scans each one, noting which account every item came from.
