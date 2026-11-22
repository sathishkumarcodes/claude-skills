# Promise Keeper eval set

14 test cases (89 checks) plus 20 trigger tests. All data is invented. The user is Jamie Rivera, and "today" is Friday, March 13, 2026, so due dates can be checked exactly.

## Test cases

| Case | What it tests | Checks |
|---|---|---|
| `combined-views` | Two separate sections, Needed from me and Urgent. | 3 |
| `custom-window-7-days` | Scans Mar 6-13 only and says so. Promises made in that window are listed; earlier ones are not. | 3 |
| `drafts-for-overdue` | Drafts for the overdue items (Priya's deck, Leo's review), using deliver, renegotiate or release approaches. Nothing is sent. | 5 |
| `full-report-from-mailbox` | A full report ordered by urgency. Open promises (Priya's deck, Leo's review, Ravi's rubric, Chloe's proposal, Marcus, Dana, the expense report) are found; kept ones (Omar's notes, Ben's pricing sheet) are marked done; pleasantries, unaccepted offers, same-message completions, other people's promises, automated mail and newsletters are left out. Asked-of-you and waiting-on-others sections appear. A ledger is written and a scheduled task is offered once. Nothing is sent. | 21 |
| `later-run-respects-ledger` | Rescans from about Mar 5 (last scan Mar 6 with a day of overlap), keeps the user's dropped and done items as they are, merges rather than duplicates, adds new items and records the new scan date. | 8 |
| `no-source-available` | No email, chat or notes are available, so it lists no promises, suggests connecting a source and offers to scan pasted or uploaded text. | 2 |
| `pasted-slack-text` | Works from the pasted text alone. The OKR draft is done; the hiring plan is open with an inferred due date of Mon Mar 16; Grace's budget numbers are a waiting item. | 4 |
| `resolves-due-dates` | Each promise's due date is resolved from the date the message was sent, and labeled stated or inferred. | 8 |
| `telegram-export` | Reads only Jamie's messages as promises: the overdue apartment checklist and bringing the speaker Saturday. Taylor's cabin booking is a waiting item. 'We should hang more' is a pleasantry. | 4 |
| `view-done-last-n-days` | Items closed Mar 8-13: the team wiki (Mar 10) and the Q4 recap (Mar 12), with closed-on dates and a count. Older closures are left out. | 6 |
| `view-needed-from-me` | Only the Needed from me view: Jamie's open promises plus open requests asked of Jamie, overdue first, including the standup action item. Waiting items and done items are left out. | 8 |
| `view-urgent` | Only urgent items, each with a one-line reason: the overdue Priya deck, Leo's review (overdue and chased), the overdue roadmap doc, Grace's ASAP request and Tom's portfolio before tomorrow's phone screen. Non-urgent and waiting items are left out. | 9 |
| `view-waiting-on-others` | Only the Waiting on others view: Alex (promised approval, quiet since Mar 2) then Jordan (unanswered, quiet since Mar 10, followed up 3 times), with days quiet. | 6 |
| `view-waiting-quiet-filter` | Waiting view filtered to items quiet 7+ days: Alex only. | 2 |

## Test data

- `mailbox.json`: 24 email threads, each built to test one rule (an overdue promise, a soft "get back to you", a promise already kept, a pleasantry, an offer nobody accepted, a request someone accepted, a task finished in the same email, a promise restated with a new date, someone else's promise, unanswered follow-ups, ASAP requests, an event in the next 48 hours, automated mail, a newsletter).
- `standup-2026-03-10.md`: meeting notes with action items for Jamie and for other people.
- `ledger.csv`: a list from an earlier scan (Mar 6), with items the user dropped and items closed on different dates.
- `result.json`: a Telegram Desktop export.
- `evals-answer-key.json`: what each thread should produce, for whoever reviews the runs.

## Trigger tests

`trigger-evals.json` has 10 requests that should turn the skill on and 10 look-alikes that shouldn't (a follow-up email, a to-do app, an email summary, a calendar check, a morning brief and so on). Use them with skill-creator's description optimizer.

## Running

- **In Claude:** ask "run the promise-keeper evals". Claude runs each case with and without the skill, grades the checks and opens a review page.
- **In Claude Code:** from this folder, run `claude plugin eval . --allow-tools Write,Edit,Bash --scaffold`. These are real, billed model runs.

## Latest results (iteration 1, Nov 22, 2026)

One run per case for each setup, graded against the same 89 checks.

| | With skill | Without skill |
|---|---|---|
| Checks passed | **88 / 89 (99%)** | 76 / 89 (86%) |
| Average time per run | 71 s | 32 s |
| Average tokens per run | ~61,000 | ~52,000 |

### By case

| Case | With skill | Without skill |
|---|---|---|
| `full-report-from-mailbox` | 21/21 | 17/21 |
| `resolves-due-dates` | 8/8 | 6/8 |
| `view-needed-from-me` | 8/8 | 6/8 |
| `view-waiting-on-others` | 6/6 | 4/6 |
| `view-waiting-quiet-filter` | 2/2 | 1/2 |
| `later-run-respects-ledger` | 8/8 | 7/8 |
| `pasted-slack-text` | 4/4 | 3/4 |
| `view-done-last-n-days` | 5/6 | 6/6 |
| `view-urgent` | 9/9 | 9/9 |
| `combined-views` | 3/3 | 3/3 |
| `custom-window-7-days` | 3/3 | 3/3 |
| `drafts-for-overdue` | 5/5 | 5/5 |
| `telegram-export` | 4/4 | 4/4 |
| `no-source-available` | 2/2 | 2/2 |

### Known issues in the skill

1. **Phone calls marked done too early.** The call with Sam was marked done because his next email said "as discussed" (3 runs). It should stay "probably done". This caused the one failed check, in `view-done-last-n-days`.
2. **Answered requests counted as promises.** Ivy's room booking (asked and answered) was counted as a closed promise.
3. **Sort order.** In the needed-from-me view, Grace's ASAP request and Ravi's rubric (due today, guessed date) were placed below items due weeks later. In the full report, the expense report due Mar 31 appeared under "this week".
4. **Off by one.** "Last 5 days" was read as Mar 8–13, which is 6 days counting both ends.
5. **Later scans can miss old items.** A rescan starts at the last scan date, so open items an earlier scan missed (Alex's approval, the expense report) are never picked up.

### Weak tests

Six cases pass with and without the skill, so they don't yet show what the skill adds: `view-urgent`, `combined-views`, `custom-window-7-days`, `drafts-for-overdue`, `telegram-export` and `no-source-available`. Checks to add:
- Ravi's rubric is due now.
- Chloe's proposal is not urgent.
- The NDA, the room booking and the promise Jamie was only cc'd on are left out.
- No ledger is created when there is no source.
- The test date is used, not the real date.
