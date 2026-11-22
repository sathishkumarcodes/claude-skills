"""Synthetic test data for the promise-keeper eval set.

Everyone here is invented. The user is Jamie Rivera <jamie@acme.example>.
"Today" for every case is Friday 2026-03-13; the default first-run window is
Feb 27 - Mar 13 (14 days).
"""

ME = "jamie@acme.example"


def m(frm, to, date, body, attachments=None, cc=None):
    msg = {"from": frm, "to": to, "date": date, "body": body}
    if cc:
        msg["cc"] = cc
    if attachments:
        msg["attachments"] = attachments
    return msg


# Each thread is annotated (in "_expect") for the eval author only; the
# annotations are stripped before the file is written for the runs.
THREADS = [
    {"id": "t01", "subject": "Q1 budget deck", "_expect": "PROMISE open, stated due Fri Mar 6, overdue 7 days",
     "messages": [
        m("priya@acme.example", ME, "2026-03-02T10:00:00-08:00", "Hi Jamie, can you share the Q1 budget deck before board prep?"),
        m(ME, "priya@acme.example", "2026-03-02T10:30:00-08:00", "Sure, I'll send it over by Friday."),
     ]},
    {"id": "t02", "subject": "Vendor contract clause 7", "_expect": "PROMISE open, soft, inferred due Mon Mar 16",
     "messages": [
        m("marcus@vendorco.example", ME, "2026-03-12T09:15:00-08:00", "Is clause 7 on liability OK with your legal team?"),
        m(ME, "marcus@vendorco.example", "2026-03-12T11:00:00-08:00", "Let me check with legal and get back to you."),
     ]},
    {"id": "t03", "subject": "Meeting your design team", "_expect": "PROMISE open, no time, inferred due Mon Mar 16",
     "messages": [
        m("dana@partner.example", ME, "2026-03-09T13:00:00-08:00", "Would love to meet your design team at some point."),
        m(ME, "dana@partner.example", "2026-03-09T14:00:00-08:00", "Happy to make the intro to the design team."),
     ]},
    {"id": "t04", "subject": "Notes from the sync", "_expect": "PROMISE done (notes attached Mar 4, thanked)",
     "messages": [
        m(ME, "omar@acme.example", "2026-03-03T16:00:00-08:00", "Good sync today. I'll send you the notes tomorrow."),
        m(ME, "omar@acme.example", "2026-03-04T09:00:00-08:00", "Here are the notes from yesterday's sync.", attachments=["sync-notes.pdf"]),
        m("omar@acme.example", ME, "2026-03-04T09:20:00-08:00", "Thanks!"),
     ]},
    {"id": "t05", "subject": "Offsite", "_expect": "PROMISE probably done (phone call, 'as discussed' next day)",
     "messages": [
        m("sam@acme.example", ME, "2026-03-11T10:00:00-08:00", "Can you call me about the offsite?"),
        m(ME, "sam@acme.example", "2026-03-11T10:05:00-08:00", "Will call you at 3 today."),
        m("sam@acme.example", ME, "2026-03-12T08:30:00-08:00", "Venue options attached, as discussed.", attachments=["venues.pdf"]),
     ]},
    {"id": "t06", "subject": "Great meeting you", "_expect": "PLEASANTRY: exclude or low confidence only",
     "messages": [
        m(ME, "lee@startup.example", "2026-02-27T17:00:00-08:00", "Great meeting you at the panel! Let's grab coffee sometime."),
     ]},
    {"id": "t07", "subject": "FAQ", "_expect": "CONDITIONAL offer, never accepted: exclude",
     "messages": [
        m(ME, "kim@acme.example", "2026-03-05T11:00:00-08:00", "If you want, I could draft the FAQ for the launch."),
     ]},
    {"id": "t08", "subject": "Hiring rubric", "_expect": "CONDITIONAL offer accepted: PROMISE open, inferred due ~Mar 12-13",
     "messages": [
        m(ME, "ravi@acme.example", "2026-03-05T15:00:00-08:00", "If helpful, I can put together the hiring rubric."),
        m("ravi@acme.example", ME, "2026-03-06T09:00:00-08:00", "Yes please, that would be great."),
     ]},
    {"id": "t09", "subject": "Onboarding doc review", "_expect": "ACCEPTED ASK: PROMISE open, stated due Wed Mar 11, overdue 2 days, chased -> urgent",
     "messages": [
        m("leo@acme.example", ME, "2026-03-10T09:00:00-08:00", "Can you review the onboarding doc by Wednesday?"),
        m(ME, "leo@acme.example", "2026-03-10T09:30:00-08:00", "Will do."),
        m("leo@acme.example", ME, "2026-03-13T08:45:00-08:00", "Just following up on the onboarding doc review?"),
     ]},
    {"id": "t10", "subject": "NDA", "_expect": "DONE IN SAME MESSAGE: exclude",
     "messages": [
        m(ME, "ana@law.example", "2026-03-09T12:00:00-08:00", "I've attached the signed NDA.", attachments=["nda-signed.pdf"]),
     ]},
    {"id": "t11", "subject": "Pricing sheet", "_expect": "PROMISE done; 'Friday' sent on Fri Feb 27 resolves to Fri Mar 6; delivered Mar 6",
     "messages": [
        m(ME, "ben@client.example", "2026-02-27T15:00:00-08:00", "I'll get you the pricing sheet Friday."),
        m(ME, "ben@client.example", "2026-03-06T10:00:00-08:00", "Pricing sheet attached.", attachments=["pricing.xlsx"]),
     ]},
    {"id": "t12", "subject": "Draft proposal", "_expect": "PROMISE open; 'next week' from Wed Mar 4 = Fri Mar 13; restated Mar 11 'by Monday' -> one item due Mon Mar 16",
     "messages": [
        m(ME, "chloe@client.example", "2026-03-04T14:00:00-08:00", "I'll have the draft proposal to you next week."),
        m(ME, "chloe@client.example", "2026-03-11T16:00:00-08:00", "Still on it, should have it to you by Monday."),
     ]},
    {"id": "t13", "subject": "Expenses", "_expect": "PROMISE open; 'end of month' from Mar 3 = Tue Mar 31",
     "messages": [
        m(ME, "finance@acme.example", "2026-03-03T10:00:00-08:00", "I'll submit my expense report by end of month."),
     ]},
    {"id": "t14", "subject": "Contract signature", "_expect": "WAITING: Jordan, last user msg Mar 10 (3 days quiet), 3 follow-ups -> flag",
     "messages": [
        m(ME, "jordan@client.example", "2026-02-27T11:00:00-08:00", "Could you sign the contract when you get a chance?", attachments=["contract.pdf"]),
        m(ME, "jordan@client.example", "2026-03-03T11:00:00-08:00", "Any update on the signature?"),
        m(ME, "jordan@client.example", "2026-03-06T11:00:00-08:00", "Following up on the contract."),
        m(ME, "jordan@client.example", "2026-03-10T11:00:00-08:00", "Just checking in on the signature."),
     ]},
    {"id": "t15", "subject": "Expense approval", "_expect": "WAITING: Alex promised approval by Wed Mar 4, since Mar 2 (11 days)",
     "messages": [
        m("alex@acme.example", ME, "2026-03-02T09:00:00-08:00", "I'll approve your expense by Wednesday."),
     ]},
    {"id": "t16", "subject": "Q4 numbers", "_expect": "ANSWERED question: not waiting",
     "messages": [
        m(ME, "nina@acme.example", "2026-03-05T10:00:00-08:00", "Do you have the Q4 numbers?"),
        m("nina@acme.example", ME, "2026-03-06T10:00:00-08:00", "Yes, attached.", attachments=["q4.xlsx"]),
     ]},
    {"id": "t17", "subject": "Headcount numbers", "_expect": "ASKED OF YOU, ASAP -> urgent",
     "messages": [
        m("grace@acme.example", ME, "2026-03-12T17:00:00-08:00", "Need the headcount numbers ASAP for the exec review."),
     ]},
    {"id": "t18", "subject": "Phone screen confirmed", "_expect": "ASKED OF YOU, event within 48h -> urgent",
     "messages": [
        m("tom@recruitco.example", ME, "2026-03-12T12:00:00-08:00", "Your phone screen is confirmed for tomorrow, Saturday March 14 at 10am. Please send your portfolio link beforehand."),
     ]},
    {"id": "t19", "subject": "Vendor survey notes", "_expect": "ASKED OF YOU, stated due next week (Fri Mar 20), NOT urgent",
     "messages": [
        m("hannah@acme.example", ME, "2026-03-12T10:00:00-08:00", "No rush, but could you share your notes on the vendor survey sometime next week?"),
     ]},
    {"id": "t20", "subject": "Room booking", "_expect": "ASKED and ANSWERED: exclude",
     "messages": [
        m("ivy@acme.example", ME, "2026-03-04T10:00:00-08:00", "Can you confirm the room booking for Thursday?"),
        m(ME, "ivy@acme.example", "2026-03-04T10:10:00-08:00", "Confirmed."),
     ]},
    {"id": "t21", "subject": "Thanks for the demo", "_expect": "RHETORICAL: exclude",
     "messages": [
        m("rep@tooling.example", ME, "2026-03-10T15:00:00-08:00", "Thanks for joining the demo. Let me know if you have any questions!"),
     ]},
    {"id": "t22", "subject": "Action required: confirm your email", "_expect": "AUTOMATED: skip",
     "messages": [
        m("no-reply@saasapp.example", ME, "2026-03-11T06:00:00-08:00", "Action required: please confirm your email address within 24 hours."),
     ]},
    {"id": "t23", "subject": "The Weekly Brief", "_expect": "NEWSLETTER: skip",
     "messages": [
        m("newsletter@industrynews.example", ME, "2026-03-12T07:00:00-08:00", "Can you spare 2 minutes for our reader survey? Reply today!"),
     ]},
    {"id": "t24", "subject": "Slides for Marcus", "_expect": "SOMEONE ELSE'S promise to someone else (user cc'd): exclude",
     "messages": [
        m("priya@acme.example", "marcus@vendorco.example", "2026-03-09T10:00:00-08:00", "I'll send Marcus the slides tomorrow.", cc=[ME]),
     ]},
]

STANDUP_NOTES = """# Team standup - Tuesday, March 10, 2026

Attendees: Jamie Rivera, Priya Shah, Omar Haddad

## Discussion
- Roadmap review slipped a week.
- Budget deck still in progress.

## Action items
- Jamie: update the roadmap doc by Thursday
- Priya: send the revised budget numbers to finance
- Omar: book the room for the quarterly review
"""
# Expected: Jamie's item -> PROMISE open, stated due Thu Mar 12, overdue 1 day.
# Priya's and Omar's items are not Jamie's.

# An existing ledger from a previous scan on Mar 6 (for later-run cases).
LEDGER_CSV = """Type,What,Who,Due,Stated/Inferred,Status,Made on,Closed on,Quote,Confidence
Promise,Send Priya the Q1 budget deck,Priya Shah,2026-03-06,Stated,Open,2026-03-02,,I'll send it over by Friday.,High
Promise,Get coffee with Lee,Lee,2026-03-06,Inferred,Dropped,2026-02-27,2026-03-06,Let's grab coffee sometime.,Low
Promise,Draft the launch FAQ for Kim,Kim,2026-03-12,Inferred,Dropped,2026-03-05,2026-03-06,I could draft the FAQ,Low
Promise,Send Ravi the vendor list,Ravi,2026-03-02,Stated,Done,2026-02-26,2026-03-02,I'll send the vendor list Monday.,High
Promise,Book the offsite venue,Sam,2026-03-05,Stated,Done,2026-03-01,2026-03-05,I'll book the venue by Thursday.,High
Promise,Get Ben the pricing sheet,Ben,2026-03-06,Stated,Done,2026-02-27,2026-03-06,I'll get you the pricing sheet Friday.,High
Promise,Update the team wiki,Omar,2026-03-10,Stated,Done,2026-03-06,2026-03-10,I'll update the wiki Tuesday.,High
Promise,Share the Q4 recap,Grace,2026-03-12,Stated,Done,2026-03-06,2026-03-12,I'll share the Q4 recap Thursday.,High
Waiting,Contract signature,Jordan,,,Waiting,2026-03-06,,Following up on the contract.,
Last scan,2026-03-06,,,,,,,,
"""

# A Telegram Desktop export (result.json shape). Jamie is user1234.
TELEGRAM = {
    "name": "Taylor",
    "type": "personal_chat",
    "id": 5551234,
    "messages": [
        {"id": 1, "type": "message", "date": "2026-03-11T19:00:00", "from": "Jamie Rivera", "from_id": "user1234",
         "text": "I'll send you the apartment checklist tonight"},
        {"id": 2, "type": "message", "date": "2026-03-11T19:05:00", "from": "Taylor", "from_id": "user9876",
         "text": "Perfect. I'll book the cabin for the 21st"},
        {"id": 3, "type": "message", "date": "2026-03-12T08:00:00", "from": "Taylor", "from_id": "user9876",
         "text": "Can you bring the speaker on Saturday?"},
        {"id": 4, "type": "message", "date": "2026-03-12T08:10:00", "from": "Jamie Rivera", "from_id": "user1234",
         "text": "Yep, will bring it"},
        {"id": 5, "type": "message", "date": "2026-03-12T08:11:00", "from": "Jamie Rivera", "from_id": "user1234",
         "text": "lol we should hang more"},
    ],
}
# Expected: checklist -> PROMISE open, due Mar 11, overdue 2 days.
# speaker -> PROMISE open, stated due Sat Mar 14.
# cabin -> WAITING on Taylor. "hang more" -> pleasantry.
