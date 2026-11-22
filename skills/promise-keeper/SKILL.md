---
name: "promise-keeper"
description: "Track promises the user made, requests waiting on them and replies they're waiting on. Use for 'what's needed from me', 'waiting on others', 'done this week', 'anything urgent'."
---

# Promise Keeper

Find the things the user said they would do, in their own words, and track them until they're done. The point is to catch promises they never wrote down anywhere: "I'll send that Friday", "let me check and get back to you", "I can take that one".

It tracks three kinds of item:
- **Promises**: things the user said they'd do.
- **Asked of you**: requests or questions other people sent the user that the user hasn't answered or done yet.
- **Waiting on others**: things the user is owed, such as a reply to their question or something someone promised them.

## 0. Work out which view the user wants

Match the user's words to a view. Every view rescans first (steps 1–6) so the ledger is current, then reports only that view (step 7).

| The user says something like | View | What to show |
|---|---|---|
| "run promise keeper", "what did I promise", "loose ends" | **Full** | Everything, in the order of step 7 |
| "what's needed from me", "what do I owe people", "my to-dos" | **Needed from me** | Open Promises plus open Asked of you, overdue first |
| "waiting on others", "who owes me", "who hasn't replied" | **Waiting on others** | Open Waiting items, longest silence first |
| "what's done", "done in the last 7 days", "what did I close this week" | **Done in last N days** | Items whose status became done in the last N days, newest first. If no N is given, use 7 |
| "anything urgent", "what's on fire", "what needs me today" | **Urgent** | Only items that meet the urgency rules in step 3c |

If the user combines views ("what's needed from me and anything urgent"), show each as its own section. If a request doesn't fit any view, show the Full view.

A number in the request sets the window for that view: "done in the last 3 days" means N = 3, and "waiting more than 2 weeks" means show only Waiting items quiet for 14 days or more.

## 1. Pick the time window

- First run: the last 14 days, unless the user names a different range.
- Later runs: from the date of the last scan, as recorded in the ledger (step 6), with a 1-day overlap.

## 2. Gather the user's own words

Use whatever is connected. Only messages the user wrote, or lines spoken by the user in a transcript, count as promises.

- **Email** (Gmail, Outlook): sent messages in the window, for Promises and Waiting on others. Also the inbox in the window, for Asked of you: messages from real people addressed to the user. Skip newsletters, promotions, automated senders (no-reply addresses, notification systems) and mailing lists unless a person in them asks the user something directly. Keep the sender or recipient, subject, date and a link to each.
- **Slack / Teams**: messages from the user in DMs, group DMs and channels.
- **Meeting notes / transcripts** (Google Drive, Notion, Granola, Otter, Zoom and so on): the user's lines, plus any action items assigned to the user by name.
- **Calendar**: only for context. Meeting titles and attendees help work out who a promise was made to.

If no source is connected, search the connector registry for the user's email and chat apps and suggest them. Meanwhile, offer to scan text the user pastes in.

Save the raw messages to a working file and process them in code or in batches. Don't page hundreds of messages through the conversation.

## 3. Find commitments

A commitment is the user, in the first person, agreeing to do something for someone.

**Count:**
- Explicit with a date: "I'll send the deck by Friday", "will have it to you EOD".
- Explicit without a date: "I'll intro you to Sam", "I'll look into it".
- Soft but real: "let me check and get back to you", "I'll circle back", "leave it with me", "I can take that", "on it".
- Accepted asks: someone asks "can you review this?" and the user replies "sure" / "yes" / "will do". The promise is the other person's request.
- Action items assigned to the user in meeting notes.

**Don't count:**
- Pleasantries with no real task, like "let's grab coffee sometime" or "happy to help anytime". If one looks half real, include it at low confidence.
- Conditional or hypothetical offers that never got a yes: "if you want, I could..." with no reply.
- Promises other people made to the user, and questions the user asked that got no reply. These go in **Waiting on others** (step 3b), not in Promises.
- Things the user finished in the same message.

For each one, record:
- **What**: a short task in the imperative, e.g. "Send Q3 deck to Priya".
- **To whom**: person and channel.
- **Quote**: the user's exact words, kept short.
- **Made on**: the message date.
- **Due**: see step 4.
- **Source link**.
- **Confidence**: high / medium / low.

## 3a. Find requests asked of the user

An Asked of you item is a message from someone else that asks the user to do, decide, answer or send something, where the thread shows no reply or action from the user afterwards.

**Count:** direct questions ("Is this the same role?", "Are you open to relocation?"), requests ("please send your resume", "can you review this"), decisions waiting on the user, and forms or steps marked required.

**Don't count:** questions answered later in the thread, rhetorical lines ("let me know if you have any questions"), and automated reminders unless a person is waiting behind them.

Record the same fields as a promise, with **From** in place of To, and the asker's words as the quote. Due date: a date the asker gave, else 2 business days after the message, marked *inferred*.

If the user later replies in a way that answers or delivers it, mark it done. If the user says yes to it, it becomes a Promise.

## 3b. Find what the user is waiting on

A Waiting on others item is either:
- the user's own message that asks a question or for an update, where the newest message in the thread is still the user's, or
- someone else promising the user something ("I'll reach out to HR", "I'll confirm shortly") with no sign they did it.

Record who, what the user is waiting for, the date of the user's last message (or of the other person's promise), and a link. Show **days quiet** as today minus that date. Count how many times the user has followed up in that thread.

Mark it **Replied** once the other person responds. If the user has followed up 3 or more times with no answer, say so, so the user can decide whether to keep chasing.

## 3c. Urgency rules

An open item is **urgent** if any of these is true:
- It's overdue, or due today or tomorrow.
- The message asking for it says urgent, ASAP, EOD, "by end of day", "today", "time-sensitive", "deadline" or similar, and it's still open.
- Someone has followed up on it at least once ("just following up", "bumping this", "any update?"). Being chased makes it urgent.
- It's tied to an event in the next 48 hours, such as a meeting, interview, call or flight, and something has to happen before it.

Waiting on others items are never urgent by themselves. Include one only if the user is blocked on it before an event in the next 48 hours.

In the Urgent view, give each item a one-line reason: "overdue 59 days", "due tonight", "he followed up twice", "interview tomorrow at 2pm".

## 4. Work out due dates

Resolve every date relative to the date the message was **sent**, not today.

- "Today" / "EOD": that day. "Tomorrow": the next day.
- A weekday ("Friday"): the next such day after the sent date.
- "This week": that Friday. "Next week": the Friday of the following week. "Early next week": the Tuesday.
- "End of month": the last business day of that month.
- "ASAP" / "shortly" / "get back to you": 2 business days after the sent date. Mark it *inferred*.
- No time at all: 5 business days after the sent date, marked *inferred*, unless the context sets a deadline, such as a meeting where the item is needed.

Always show whether a date was **stated** or **inferred**.

## 5. Check whether each one is already done

Before listing a promise as open, look for evidence it was kept:
- A later message in the same thread or to the same person that delivers it: an attachment, a link, "here you go", or the answer itself.
- The other person thanking the user for it.
- The user saying it's done.

If the evidence is clear, mark it **done** and record the date the evidence appeared as **Closed on**. If it's only likely, mark it **probably done – confirm?** Never drop an item silently.

When the user confirms an item or marks it done in the ledger, set Closed on to that day unless the evidence shows an earlier date. The Done in last N days view goes by Closed on.

## 6. Keep the running ledger

The list must last between runs.

- Before making a new list, look for an existing one. Search the user's artifacts for "Promise Keeper". Update that one instead of starting over.
- Where to keep it, in order of preference: a **Tasks** artifact (owner = the user, status, due date), then a **Sheets** artifact, then a `promise-keeper.md` file sent to the user.
- In a Sheets ledger, use three tabs:
  - **Promises**: What · To · Due · Stated/Inferred · Status (open / probably done / done / dropped) · Made on · Closed on · Quote · Link · Confidence.
  - **Asked of you**: What · From · Due · Stated/Inferred · Status (open / done / declined) · Asked on · Closed on · Their words · Link · Urgent (yes/no, with reason).
  - **Waiting on others**: Who · Waiting for · Since · Days quiet (a formula: today minus Since) · Follow-ups sent · Status (waiting / replied / dropped) · Closed on · Link.
- In a Tasks artifact or a markdown file, keep the same fields, with a Type field (Promise / Asked of you / Waiting) in place of the tabs.
- If an existing ledger is missing any of these tabs or columns, add them without disturbing the user's rows.
- Record the date of this scan in the ledger so the next run knows where to start.
- Merge duplicates. The same promise repeated ("still on it!") is one item. Use the later due date if the user changed it.
- Keep the user's manual edits. If they marked an item done or dropped, don't reopen it.

## 7. Report back

Show only the view the user asked for (step 0). Head the reply with the view's name, the scan date and the window, e.g. "**Needed from you** · Nov 22 · scanned Aug 24 – Nov 22". If a view has nothing in it, say so in one line, such as "Nothing urgent right now."

The **Full** view is short and ordered by urgency:

1. **Overdue**: each with how many days late and to whom.
2. **Due today / tomorrow**.
3. **Due this week**.
4. **No firm date**: inferred dates, oldest first.
5. **Probably done – confirm?**: one line each.
6. **Asked of you**: open requests from others, oldest first.
7. **Waiting on others**: longest silence first, with days quiet and follow-ups sent.

The other views use the same item format (what, who, due or days quiet, the quote kept short, a link):
- **Needed from me**: Promises and Asked of you together, grouped by overdue, due today or tomorrow, this week, then no firm date.
- **Waiting on others**: one line each. Flag any with 3 or more follow-ups.
- **Done in last N days**: one line each with its Closed on date, plus the count, e.g. "5 closed in the last 7 days".
- **Urgent**: one line each with its reason (step 3c), most pressing first.

End with counts, e.g. "12 open, 3 overdue, 5 closed since last scan", and a link to the ledger.

## 8. Help close the loop

For each overdue or due-today item, offer one of these:
- **Deliver**: draft the reply that sends what was promised, if Claude can produce it.
- **Renegotiate**: a short, honest message moving the date ("Running behind on the deck, can I get it to you Tuesday?").
- **Release**: a polite note handing it back if the user won't do it.

Draft only. **Never send a message, post in Slack or change someone's calendar without the user's explicit OK for that specific message.**

## 9. Offer to run it automatically

After the first run, offer once to set up a scheduled task, for example every weekday at 8:30am, that rescans, updates the ledger and reports only what's overdue or due today. Use the session's scheduling tools and call it a "scheduled task".

## Ground rules

- Read-only by default. Scanning never changes anything in the user's apps.
- Quote briefly. Don't copy whole messages into the ledger.
- When unsure whether something is a promise, include it at low confidence rather than miss it. The user can drop it in one click, but a missed promise is the thing this skill exists to prevent.