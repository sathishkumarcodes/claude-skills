"""Write the promise-keeper eval set as case folders (claude plugin eval layout)."""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
import fixtures as fx  # noqa: E402

SKILL = sys.argv[1]
EVALS = os.path.join(SKILL, "evals")

SETTINGS = """---
tags: [skill-creator, promise-keeper]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

"""

CTX = ("Today is Friday, March 13, 2026. I'm Jamie Rivera (jamie@acme.example). "
       "My email isn't connected in this session, so I exported it: mailbox.json has my "
       "inbox and sent mail from the last few weeks.")
CTX_NOTES = CTX + " standup-2026-03-10.md is my notes from Tuesday's standup."
CTX_LEDGER = CTX + " ledger.csv is my Promise Keeper list from the last scan."


def mailbox():
    return {"account": fx.ME, "threads": [{k: v for k, v in t.items() if not k.startswith("_")}
                                          for t in fx.THREADS]}


FILES = {
    "mailbox.json": lambda: json.dumps(mailbox(), indent=2),
    "standup-2026-03-10.md": lambda: fx.STANDUP_NOTES,
    "ledger.csv": lambda: fx.LEDGER_CSV,
    "result.json": lambda: json.dumps(fx.TELEGRAM, indent=2),
}

CASES = [
    {
        "name": "full-report-from-mailbox",
        "prompt": f"{CTX}\n\nRun promise keeper on my email.",
        "files": ["mailbox.json"],
        "outcome": "A full report ordered by urgency. Open promises (Priya's deck, Leo's review, Ravi's rubric, "
                   "Chloe's proposal, Marcus, Dana, the expense report) are found; kept ones (Omar's notes, Ben's "
                   "pricing sheet) are marked done; pleasantries, unaccepted offers, same-message completions, "
                   "other people's promises, automated mail and newsletters are left out. Asked-of-you and "
                   "waiting-on-others sections appear. A ledger is written and a scheduled task is offered once. "
                   "Nothing is sent.",
        "graders": [
            "The report lists sending Priya the Q1 budget deck as an open, overdue promise.",
            "The report gives the Priya deck a due date of Friday March 6, marked as stated, and says it is 7 days overdue.",
            "The report lists reviewing Leo's onboarding doc as an overdue promise due Wednesday March 11.",
            "The report lists putting together the hiring rubric for Ravi as an open promise.",
            "Sending Omar the sync notes is marked done, not listed as open.",
            "Getting Ben the pricing sheet is marked done, not listed as open.",
            "The signed NDA sent to Ana is not listed as an open promise.",
            "Drafting the FAQ for Kim is not listed as an open promise.",
            "Getting coffee with Lee is either left out or listed only at low confidence, never as overdue or high confidence.",
            "Priya's promise to send Marcus the slides is not listed as Jamie's promise or as something Jamie is waiting on.",
            "The report lists Alex's promised expense approval under waiting on others.",
            "The report lists Jordan's contract signature under waiting on others and notes that Jamie has followed up three or more times.",
            "Nina's Q4 numbers are not listed as something Jamie is waiting on.",
            "The report lists Grace's request for headcount numbers as a request asked of Jamie.",
            "The no-reply email confirmation and the newsletter survey are not listed as requests.",
            "Overdue items appear before items due today or later in the report.",
            "Each listed promise quotes Jamie's own words from the email.",
            "A ledger (a Sheet, a Tasks list or a promise-keeper.md file) is created holding the found items and the scan date March 13, 2026.",
            "The response offers to set up a recurring scheduled task.",
            "The response does not send any email or claim that one was sent.",
            "The report ends with counts of open and overdue items.",
        ],
    },
    {
        "name": "resolves-due-dates",
        "prompt": f"{CTX}\n\nRun promise keeper and give me every promise I made with its due date, and say whether "
                  "each date is one I gave or one you guessed.",
        "files": ["mailbox.json"],
        "outcome": "Each promise's due date is resolved from the date the message was sent, and labeled stated or inferred.",
        "graders": [
            "The Priya budget deck is due Friday March 6, 2026, labeled stated.",
            "Ben's pricing sheet ('Friday', written on Friday February 27) is given a due date of Friday March 6, not February 27.",
            "Chloe's draft proposal appears as one item, not two, with a due date of Monday March 16.",
            "The expense report is due Tuesday March 31, 2026, labeled stated.",
            "Getting back to Marcus about clause 7 is due Monday March 16, labeled inferred.",
            "The intro for Dana to the design team is due Monday March 16, labeled inferred.",
            "Leo's onboarding doc review is due Wednesday March 11, labeled stated.",
            "Every promise listed has its due date labeled as stated or inferred.",
        ],
    },
    {
        "name": "view-needed-from-me",
        "prompt": f"{CTX_NOTES}\n\nWhat's needed from me?",
        "files": ["mailbox.json", "standup-2026-03-10.md"],
        "outcome": "Only the Needed from me view: Jamie's open promises plus open requests asked of Jamie, overdue first, "
                   "including the standup action item. Waiting items and done items are left out.",
        "graders": [
            "The response presents a 'needed from you' view rather than the full report with every section.",
            "The response includes the Priya deck, Leo's review, Ravi's rubric and Chloe's proposal as things Jamie owes.",
            "The response includes Grace's headcount numbers, Tom's portfolio link and Hannah's vendor survey notes as requests asked of Jamie.",
            "The response includes updating the roadmap doc from the standup notes, due Thursday March 12.",
            "Priya's and Omar's standup action items are not listed as Jamie's.",
            "Alex's expense approval and Jordan's contract signature are not listed as things needed from Jamie.",
            "Sending Omar the notes and getting Ben the pricing sheet are not listed as open.",
            "Overdue items are listed before items that are not yet due.",
        ],
    },
    {
        "name": "view-waiting-on-others",
        "prompt": f"{CTX}\n\nWho am I waiting on?",
        "files": ["mailbox.json"],
        "outcome": "Only the Waiting on others view: Alex (promised approval, quiet since Mar 2) then Jordan "
                   "(unanswered, quiet since Mar 10, followed up 3 times), with days quiet.",
        "graders": [
            "The response lists Alex's expense approval and Jordan's contract signature.",
            "Alex is listed before Jordan.",
            "The response shows about 11 days quiet for Alex and about 3 days quiet for Jordan (within one day either way).",
            "The response flags that Jamie has followed up with Jordan three or more times.",
            "Nina is not listed.",
            "None of Jamie's own promises, such as the Priya deck, are listed as waiting items.",
        ],
    },
    {
        "name": "view-waiting-quiet-filter",
        "prompt": f"{CTX}\n\nWho's been quiet on me for more than a week?",
        "files": ["mailbox.json"],
        "outcome": "Waiting view filtered to items quiet 7+ days: Alex only.",
        "graders": [
            "The response lists Alex's expense approval.",
            "The response does not list Jordan, whose last message from Jamie was 3 days ago, as quiet for more than a week.",
        ],
    },
    {
        "name": "view-done-last-n-days",
        "prompt": f"{CTX_LEDGER}\n\nWhat did I get done in the last 5 days?",
        "files": ["mailbox.json", "ledger.csv"],
        "outcome": "Items closed Mar 8-13: the team wiki (Mar 10) and the Q4 recap (Mar 12), with closed-on dates and a count. "
                   "Older closures are left out.",
        "graders": [
            "The response includes updating the team wiki (closed March 10) and sharing the Q4 recap (closed March 12).",
            "The response does not include the vendor list (closed March 2), the offsite venue (March 5), the pricing sheet (March 6) or the notes to Omar (March 4).",
            "Each item listed shows the date it was closed.",
            "The response gives a count of items closed in the window.",
            "The Priya budget deck is not listed as done.",
            "If the call with Sam is mentioned, it is described as probably done or needing confirmation, not as confirmed done.",
        ],
    },
    {
        "name": "view-urgent",
        "prompt": f"{CTX_NOTES}\n\nAnything urgent?",
        "files": ["mailbox.json", "standup-2026-03-10.md"],
        "outcome": "Only urgent items, each with a one-line reason: the overdue Priya deck, Leo's review (overdue and "
                   "chased), the overdue roadmap doc, Grace's ASAP request and Tom's portfolio before tomorrow's "
                   "phone screen. Non-urgent and waiting items are left out.",
        "graders": [
            "The response includes the Priya budget deck with a reason saying it is overdue.",
            "The response includes Leo's onboarding doc review with a reason saying it is overdue or that Leo followed up.",
            "The response includes Grace's headcount numbers with a reason citing ASAP.",
            "The response includes sending Tom the portfolio link with a reason citing the phone screen tomorrow.",
            "The response includes updating the roadmap doc with a reason saying it is overdue.",
            "Hannah's vendor survey notes are not listed as urgent.",
            "The expense report due March 31 is not listed as urgent.",
            "Alex's approval and Jordan's signature are not listed as urgent.",
            "Every urgent item has a short reason.",
        ],
    },
    {
        "name": "combined-views",
        "prompt": f"{CTX}\n\nWhat's needed from me, and is anything urgent?",
        "files": ["mailbox.json"],
        "outcome": "Two separate sections, Needed from me and Urgent.",
        "graders": [
            "The response has a separate section for what's needed from Jamie and a separate section for urgent items.",
            "The urgent section includes Grace's headcount numbers and Tom's portfolio link.",
            "Hannah's vendor survey notes appear in the needed-from-me section but not in the urgent section.",
        ],
    },
    {
        "name": "custom-window-7-days",
        "prompt": f"{CTX}\n\nRun promise keeper for just the last 7 days.",
        "files": ["mailbox.json"],
        "outcome": "Scans Mar 6-13 only and says so. Promises made in that window are listed; earlier ones are not.",
        "graders": [
            "The response states that it scanned roughly March 6 to March 13.",
            "The response lists Leo's review, getting back to Marcus and the intro for Dana.",
            "The Priya deck (promised March 2) and the expense report (promised March 3) are not listed as found in this scan.",
        ],
    },
    {
        "name": "later-run-respects-ledger",
        "prompt": f"{CTX_LEDGER}\n\nRun promise keeper again and update my list.",
        "files": ["mailbox.json", "ledger.csv"],
        "outcome": "Rescans from about Mar 5 (last scan Mar 6 with a day of overlap), keeps the user's dropped and done "
                   "items as they are, merges rather than duplicates, adds new items and records the new scan date.",
        "graders": [
            "The response or ledger shows the scan started around March 5 or March 6, the last scan date, rather than a fresh 14-day window.",
            "Coffee with Lee is still marked dropped in the updated ledger.",
            "The FAQ for Kim is still marked dropped in the updated ledger.",
            "The Priya budget deck appears once in the updated ledger, still open.",
            "Ben's pricing sheet appears once in the updated ledger and is still done.",
            "The updated ledger adds new items found since the last scan, including Leo's onboarding doc review.",
            "Jordan's contract signature appears once in the updated ledger.",
            "The updated ledger records March 13, 2026 as the latest scan date.",
        ],
    },
    {
        "name": "telegram-export",
        "prompt": ("Today is Friday, March 13, 2026. I'm Jamie Rivera. Can you check my Telegram chat with Taylor "
                   "for anything I promised? I exported it from Telegram Desktop: result.json."),
        "files": ["result.json"],
        "outcome": "Reads only Jamie's messages as promises: the overdue apartment checklist and bringing the speaker "
                   "Saturday. Taylor's cabin booking is a waiting item. 'We should hang more' is a pleasantry.",
        "graders": [
            "The response lists sending Taylor the apartment checklist as an overdue promise (due March 11).",
            "The response lists bringing the speaker on Saturday March 14 as an open promise.",
            "Taylor's booking of the cabin is listed under waiting on others, not as Jamie's promise.",
            "'We should hang more' is left out or listed only at low confidence.",
        ],
    },
    {
        "name": "pasted-slack-text",
        "prompt": ("Today is Friday, March 13, 2026. Here's a Slack DM with my manager Grace from this week. "
                   "Anything I committed to?\n\n"
                   "[Mon 9:02] Grace: can you own the Q2 OKR draft?\n"
                   "[Mon 9:10] me: yep, I'll take it. will have a first pass by Wednesday\n"
                   "[Tue 14:30] Grace: also, I'll get you the budget numbers by Thursday\n"
                   "[Wed 17:45] me: OKR draft is in the shared folder\n"
                   "[Thu 11:00] Grace: thanks! can you also look at the hiring plan?\n"
                   "[Thu 11:05] me: let me take a look and circle back"),
        "files": [],
        "outcome": "Works from the pasted text alone. The OKR draft is done; the hiring plan is open with an inferred "
                   "due date of Mon Mar 16; Grace's budget numbers are a waiting item.",
        "graders": [
            "The Q2 OKR draft is marked done.",
            "Looking at the hiring plan is listed as open, with an inferred due date of Monday March 16.",
            "Grace's promised budget numbers are listed under waiting on others.",
            "The response answers from the pasted text without first requiring Jamie to connect an app.",
        ],
    },
    {
        "name": "no-source-available",
        "prompt": "Run promise keeper.",
        "files": [],
        "outcome": "No email, chat or notes are available, so it lists no promises, suggests connecting a source "
                   "and offers to scan pasted or uploaded text.",
        "graders": [
            "The response does not list any specific promises, people or due dates.",
            "The response suggests connecting an email or chat app, or pasting or uploading messages to scan.",
        ],
    },
    {
        "name": "drafts-for-overdue",
        "prompt": f"{CTX}\n\nDraft replies for anything I'm late on.",
        "files": ["mailbox.json"],
        "outcome": "Drafts for the overdue items (Priya's deck, Leo's review), using deliver, renegotiate or release "
                   "approaches. Nothing is sent.",
        "graders": [
            "The response drafts a message to Priya about the Q1 budget deck.",
            "The response drafts a message to Leo about the onboarding doc review.",
            "At least one draft asks for more time with a specific new date, or the response offers a deliver, renegotiate or release choice.",
            "The response presents the messages as drafts and does not send them or claim they were sent.",
            "No drafts are written for items already done, such as Omar's notes or Ben's pricing sheet.",
        ],
    },
]


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def slug(s):
    import re
    stop = {"the","response","includes","lists","report","is","are","a","an","as","with","s","it","its","and","or","of","to","listed","marked","each","every","that","for","be","in","on","has"}
    words = [w for w in re.sub(r"[^a-z0-9]+", " ", s.lower()).split() if w not in stop]
    return "-".join(words[:5])[:40].strip("-")


if os.path.exists(EVALS):
    shutil.rmtree(EVALS)

for c in CASES:
    d = os.path.join(EVALS, c["name"])
    prompt = c["prompt"]
    if c["files"]:
        prompt += "\n\nInput files: " + ", ".join(c["files"])
    write(os.path.join(d, "prompt.md"), SETTINGS + prompt + "\n")
    yaml = f'schema_version: "1.1"\nname: {c["name"]}\nexpected_outcome: |\n'
    yaml += "".join(f"  {line}\n" for line in c["outcome"].splitlines())
    if c["files"]:
        yaml += "context:\n  scaffold_script: place-files.sh\n"
        write(os.path.join(d, "place-files.sh"), '#!/usr/bin/env bash\nset -eu\ncp -R "$(dirname "$0")/files/." .\n')
        os.chmod(os.path.join(d, "place-files.sh"), 0o755)
        for fn in c["files"]:
            write(os.path.join(d, "files", fn), FILES[fn]())
    write(os.path.join(d, "case.yaml"), yaml)
    for i, g in enumerate(c["graders"], 1):
        write(os.path.join(d, "graders", f"{i:02d}-{slug(g)}.md"),
              f"---\ntype: llm\nfocus: trace\nweight: 1\n---\n\n{g}\n")

# Expected-answer key for whoever reviews runs (not read by the CLI).
key = {t["id"]: {"subject": t["subject"], "expected": t["_expect"]} for t in fx.THREADS}
write(os.path.join(SKILL, "evals-answer-key.json"), json.dumps(
    {"today": "2026-03-13 (Fri)", "user": fx.ME, "mailbox_threads": key,
     "standup": "Jamie: update the roadmap doc by Thursday -> open, due Thu Mar 12, overdue 1 day",
     "telegram": "checklist overdue (Mar 11); speaker due Sat Mar 14; cabin = waiting on Taylor; 'hang more' = pleasantry"},
    indent=2))

print(len(CASES), "cases,", sum(len(c["graders"]) for c in CASES), "graders")
