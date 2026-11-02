# Jira skill

Manage Jira through Claude: create, edit, comment on, assign, transition, link
and log work on issues; manage sprint membership; break features into stories;
search; and summarize epic or sprint progress. Every change is read back from
Jira before it's reported as done.

Invoke it explicitly with `/jira`; it never runs on its own.

## Requirements

- The **Atlassian** (Jira & Confluence) connector in Claude: Customize >
  Connectors → search "Atlassian" → Connect, then sign in.
- Edit rights in the Jira projects you'll use.
- Linking issues and logging work need those tools in your connector; if
  they're missing, Claude says so and gives you the issue link instead.

## Install

```sh
./scripts/package.sh jira
```

Upload `dist/jira.zip` in Claude under Customize > Skills → **+** →
**Create skill** → **Upload a skill**.

Optional environment variables, if your setup exposes them:
`JIRA_BASE_URL`, `JIRA_DEFAULT_PROJECT`, `JIRA_DEFAULT_ISSUE_TYPE`.

## Test it

1. `/jira what's assigned to me?`
2. `/jira show the current sprint for <PROJECT KEY>`
3. `/jira create a test task in <PROJECT KEY>: delete me`, then
   `/jira close <KEY> as Done`

## Examples

| Operation | Request |
| --- | --- |
| Create | `/jira file a bug: CSV export times out for files over 5MB` |
| Create | `/jira create a story in PAY: save a default payment method, high priority, 3 points` |
| Create | `/jira create a sub-task under PROJ-123: write migration script` |
| Create | `/jira turn what we just discussed into a ticket` |
| Feature | `/jira create a story under PROJ-50: export reports as PDF` |
| Feature | `/jira add a story to the Reporting feature: scheduled email reports` |
| Feature | `/jira break PROJ-50 into stories` |
| Feature | `/jira move PROJ-123 under PROJ-50` |
| Edit | `/jira https://yourco.atlassian.net/browse/PROJ-123 add an acceptance criterion: handles 10k rows` |
| Edit | `/jira PROJ-123 set priority to High and add label customer-reported` |
| Edit | `/jira rewrite PROJ-123's description to follow the template` |
| Comment | `/jira update PROJ-123 with what we found: the N+1 query causes the timeout` |
| Assign | `/jira assign PROJ-123 to Priya` |
| Status | `/jira start PROJ-123` |
| Status | `/jira close PROJ-88 as Done` |
| Status | `/jira what statuses can PROJ-123 move to?` |
| Sprint | `/jira add PROJ-123 to the current sprint` |
| Sprint | `/jira move PROJ-123 to next sprint` |
| Sprint | `/jira send PROJ-123 back to the backlog` |
| Sprint | `/jira show all stories in Sprint 42` |
| Link | `/jira PROJ-1 blocks PROJ-2` |
| Work log | `/jira log 2h 30m on PROJ-123 for code review` |
| Search | `/jira what's assigned to me?` |
| Search | `/jira show open bugs in PAY` |
| Search | `/jira high-priority issues updated this week` |
| Summary | `/jira how is the current sprint going?` |
| Summary | `/jira progress on PROJ-50` |
| Bulk | `/jira move all unfinished stories in Sprint 42 to next sprint` |
| Combined | `/jira create a bug for the export timeout, assign it to me, add it to the current sprint and start it` |

## Limits

Never deletes issues, sprints or comments; never changes workflows, boards,
permissions or project settings; changes at most 25 issues per request, always
after confirmation.
