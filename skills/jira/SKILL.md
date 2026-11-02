---
name: jira
description: >-
  Create, edit, comment on, assign, transition, link, log time on, search, and
  verify Jira issues, manage sprint membership, break features into stories,
  and summarize epic or sprint progress, through the Atlassian MCP server. Use
  when the user asks to file, update, move, plan, or look up Jira work.
disable-model-invocation: true
metadata:
  model-tier: simple
---

# Jira

Manage Jira issues through the Atlassian MCP server. Change an issue only in
the way the user asked, and report a change as done only after reading it
back.

**Tool names.** The tools are named `atlassian_*` below, but the connector
may expose them with a prefix (for example `mcp__Atlassian__getJiraIssue`).
Match on the part after the prefix. If a tool named here doesn't exist, look
for the closest equivalent. If there is none, tell the user that this
connector can't do that action and, where it helps, give them the browse URL
to do it themselves in Jira.

**Configuration.** If environment variables are readable, check them before
asking the user: `JIRA_BASE_URL` (or `ATLASSIAN_BASE_URL`) for the site, such
as `example.atlassian.net`; `JIRA_DEFAULT_PROJECT` (or `JIRA_DEFAULT_SPACE`,
`JIRA_PROJECT`) for the project key; and `JIRA_DEFAULT_ISSUE_TYPE`, which
defaults to `Task`. Strip trailing slashes. The bare hostname is the
`cloudId`; browse URLs are `https://<hostname>/browse/<KEY>`. If the
environment can't be read or the variables are unset, move straight on to the
API lookups below; don't stop to explain that they're missing.

**Reading links and keys.** From a pasted Jira URL, take the hostname as the
site and the issue key from `/browse/<KEY>`, from a `selectedIssue=<KEY>`
query parameter, or from the last path segment that matches
`[A-Z][A-Z0-9_]+-\d+`. A board or backlog URL (`/jira/software/projects/<KEY>/boards/<id>`)
gives the project key and board ID. A bare key such as `PROJ-123` in the
message is an existing issue. A link with no instruction ("edit this") means
fetch the issue, show its summary, status, and assignee, and ask what to
change.

**Limits.** Never delete issues, sprints, or comments, even when asked; give
the browse URL so the user can do it in Jira. Never change workflows, boards,
permissions, or project settings.

## Steps

1. **Pick the operation:** create (a new issue, or requirements with no issue
   key), edit (an existing issue's fields), comment (adding findings, an
   update, or a note), assign, transition (a status change such as "start" or
   "close"), link (relating two issues), log work, sprint (adding issues to,
   moving them between, or removing them from a sprint), breakdown (turning a
   feature into several stories), bulk (the same change to several issues),
   search, or summarize (progress on an epic, sprint, or issue). "Update
   PROJ-123 with what we found" is a comment unless the user says to change
   the description or a field. If it could be create or edit, or edit or
   comment, ask before changing anything. Several operations in one request
   are fine; do them in the order given. Done when you know the operations.

2. **Resolve the site.** Use the hostname from a URL the user gave or from
   `JIRA_BASE_URL`. Otherwise call `atlassian_getAccessibleAtlassianResources`,
   and ask which site if it returns several and none matches the environment.
   Done when you have a `cloudId`.

3. **Resolve the project and type** (for create and breakdown). Take the
   project from the prompt, issue key, or URL, then the environment, then
   `atlassian_getVisibleJiraProjects` and the user. Take the type from the
   prompt (Bug, Story, Epic, Spike, Sub-task, or a custom type such as
   Feature), then `JIRA_DEFAULT_ISSUE_TYPE`, then `Task`, and check it exists
   with `atlassian_getJiraProjectIssueTypesMetadata`; if it doesn't, offer
   the project's valid types. Done when you have the project key and the
   type's `id`.

4. **Read the field metadata** (for create, breakdown, sprint changes, and
   edits that touch custom fields). Call
   `atlassian_getJiraIssueTypeMetaWithFields` with `cloudId`,
   `projectIdOrKey`, `issueTypeId`, and `requiredFieldsOnly: false`, since
   `true` hides optional custom fields. From the result, record:
   - **Required fields.** Every field with `required: true` that has no
     default value. Fill them from the prompt where you can; ask the user for
     the rest in one question, listing the allowed values for select fields.
     Don't call create while a required field is missing.
   - **Acceptance Criteria.** A field whose name matches "Acceptance
     Criteria", case-insensitively. Note its `customfield_*` key and its
     schema: a `schema.type` of `doc`, or a `textarea` with the rich-text
     renderer, takes Atlassian Document Format (ADF); a plain `string`
     takes a plain string. If you can't tell, send a plain string, and send
     ADF only if Jira rejects it.
   - **Story points.** A field named "Story Points" or "Story point
     estimate", case-insensitively (a number).
   - **Sprint.** A field named "Sprint" (schema custom type ending in
     `gh-sprint`).
   - **Parent / Epic link.** Whether the type uses `parent` (team-managed and
     current company-managed projects) or an `Epic Link` custom field (older
     company-managed projects).

   For a fetched issue, the `names` map from `atlassian_getJiraIssue` also
   shows field names. If discovery fails, treat the optional fields as absent
   and let the create call report any missing required fields. Done when you
   know which of these fields exist and their keys.

5. **Resolve named things.** Users often name things instead of giving keys.
   - **An epic or feature by title** ("the Reporting feature"): search
     `project = "<KEY>" AND issuetype in (Epic, Feature) AND summary ~ "<words>" AND statusCategory != Done`
     (drop `Feature` if the project has no such type). One match: use it and
     name it in your reply. Several: list key, summary, and status, and ask.
     None: say so and offer to create the epic.
   - **A sprint by name or position** ("Sprint 42", "the current sprint",
     "next sprint"): search
     `project = "<KEY>" AND sprint = "<name>"` (or `sprint in openSprints()`,
     or `sprint in futureSprints()`) with `fields` set to the Sprint field and
     `maxResults` of 5, and read the sprint objects on the results: each has
     an `id`, `name`, and `state` (`active`, `future`, `closed`). If several
     open sprints exist (several boards), list them and ask. If no issue is
     in the sprint yet, so the search can't reveal its ID, ask the user for
     the sprint ID (shown in the sprint's board URL or report) or to add one
     issue to it in Jira first.
   - **A person** is resolved under Assign in step 7.

   Done when every named item has a key or ID, or the user has been asked.

6. **Check for duplicates** before creating (including each story in a
   breakdown). Pick two to four distinctive keywords from the summary, strip
   double quotes and backslashes from them, and search with
   `atlassian_searchJiraIssuesUsingJql`:
   `project = "<KEY>" AND text ~ "<keywords>" ORDER BY statusCategory ASC, updated DESC`.
   Request `summary`, `status`, and `assignee`, with `maxResults` of 10. If
   anything matches, show each match's key, summary, and status, with open
   issues first, and ask whether to create anyway, comment on a match
   instead, or stop. Done when none match, or the user has chosen.

7. **Make the change:**
   - **Create** with `atlassian_createJiraIssue`, passing `cloudId`,
     `projectKey`, `issueTypeName`, `summary`, `description`,
     `contentFormat: "markdown"`, and, as needed, `assignee_account_id` and
     `additional_fields` for required fields, custom fields, labels,
     components, priority (`{"priority": {"name": "High"}}`), due date
     (`{"duedate": "YYYY-MM-DD"}`), story points
     (`{"<story_points_id>": 3}`), and the parent. Set the parent as
     `{"parent": {"key": "PROJ-1"}}`, or for an older company-managed project
     as `{"<epic_link_customfield_id>": "PROJ-1"}`. A Sub-task must have a
     parent; ask for one if the user didn't give it. To put the new issue in
     a sprint, create it first, then do a sprint change.
   - **Edit:** fetch the issue with only the fields you need (omit `fields`
     for the defaults, and never use `["*all"]`, which floods the context
     with custom fields). Keep existing text and fields unless asked to
     overwrite them. To add to the description, fetch it with
     `contentFormat: "markdown"` (or the tool's equivalent) so you get
     Markdown rather than ADF, merge your change into that text, and write
     the whole description back with `contentFormat: "markdown"`. Never write
     a Markdown fragment over an ADF description, because that drops the rest
     of it. Labels are a list: to add one, fetch the current labels and send
     the full list. Call `atlassian_editJiraIssue` with standard and
     `customfield_*` fields in `fields`, and `null` to clear one.
   - **Comment** with `atlassian_addCommentToJiraIssue`, passing `cloudId`,
     `issueIdOrKey`, `commentBody` in Markdown, and
     `contentFormat: "markdown"` if the tool accepts it. Write the comment
     from what the user said or the work in this conversation; lead with the
     finding or decision, then the supporting detail.
   - **Assign:** for "me", get the `account_id` from
     `atlassian_atlassianUserInfo`. For anyone else, resolve it with
     `atlassian_lookupJiraAccountId`. If that returns more than one active
     user, show their display names and emails (where visible) and ask which
     one; never pick the first match. If it returns none, say so and ask for
     an email or the exact display name. Pass `assignee_account_id` on
     create, or `{"fields": {"assignee": {"accountId": "<id>"}}}` on edit;
     `{"assignee": null}` unassigns.
   - **Transition:** never guess a transition ID. Call
     `atlassian_getTransitionsForJiraIssue` with `expand: "transitions.fields"`
     so each transition lists the fields its screen needs. Match the target
     status by transition name or by `to.name`. If the transition has
     required fields, fill them from the prompt (for example
     `{"resolution": {"name": "Done"}}`); otherwise ask, offering the allowed
     values. Call `atlassian_transitionJiraIssue` with
     `{"transition": {"id": "<id>"}}` plus `fields` for those values. If the
     status isn't reachable from the current one, show the available
     transition names and where each leads.
   - **Link** two issues ("PROJ-1 blocks PROJ-2", "relates to", "duplicates",
     "clones"). Get the link types from `atlassian_getIssueLinkTypes` and
     match the user's phrase to a type's `outward` or `inward` description:
     the issue the user names first is the outward issue when the phrase
     matches `outward` ("blocks"), and the inward issue when it matches
     `inward` ("is blocked by"). Create it with `atlassian_createIssueLink`,
     passing the type name and both keys. If the connector has no link tool,
     say so and give both browse URLs.
   - **Log work** with `atlassian_addWorklogToJiraIssue`, passing
     `timeSpent` in Jira format (`2h 30m`, `1d`), an optional `started`
     timestamp if the user gave a date ("yesterday" means that date at 09:00
     in the user's time zone), and an optional comment. Convert "an hour and
     a half" to `1h 30m`.
   - **Sprint:** with the Sprint field key from step 4 and the sprint ID
     from step 5, call `atlassian_editJiraIssue` with
     `{"fields": {"<sprint_field_id>": <sprint_id>}}` (a number, not a
     list) to add or move an issue, or `null` to send it back to the
     backlog. Only active and future sprints accept issues; for a closed
     sprint, say so and offer the active or next one. Sub-tasks follow their
     parent's sprint, so move the parent instead and say so.
   - **Breakdown** of a feature into stories ("break PROJ-50 into stories",
     "create stories for the reporting feature: PDF, CSV, email"): fetch the
     epic's summary and description. If the user listed the stories, use
     those; otherwise draft three to eight stories from the epic, each a
     thin, independently shippable slice with its own summary (benefit
     first), a short description in the feature template, and acceptance
     criteria. Show the full list as a numbered preview and ask the user to
     confirm, remove, or edit items before creating any. Then create each one
     under the epic, checking duplicates as in step 6, and report all the new
     keys together.
   - **Bulk** changes ("close all done bugs in PAY", "move these five to
     next sprint", "assign every unassigned story in Sprint 42 to me"): find
     the issues with a JQL search (or take the listed keys), show them as a
     list with key, summary, and current value of the field being changed,
     and state the change. Ask for confirmation before changing anything,
     even if the request sounded certain. Change at most 25 issues per
     request; if more match, say how many and ask the user to narrow it or
     confirm a second batch. Apply the changes one issue at a time, keep
     going if one fails, and report which succeeded and which failed and why.
   - **Search:** translate the request into JQL. Default to the resolved
     project, add `statusCategory != Done` unless the user asked about closed
     or all issues or asked about a sprint, use `assignee = currentUser()` for
     "my", and end with `ORDER BY updated DESC` unless another order was asked
     for. Quote values that contain spaces, and escape double quotes inside
     them. Useful forms: `sprint in openSprints()`, `sprint = "Sprint 42"`,
     `parent = PROJ-50` (or `"Epic Link" = PROJ-50`),
     `updated >= -7d`, `created >= startOfWeek()`, `duedate < now()`,
     `assignee is EMPTY`, `priority in (High, Highest)`. Call
     `atlassian_searchJiraIssuesUsingJql` with `fields` set to `summary`,
     `status`, `assignee`, `priority`, and `updated` (plus story points for
     sprint and epic searches), and `maxResults` of 20 unless the user asked
     for more. Show the JQL you ran, then one line per issue: key (linked to
     its browse URL), summary, status, assignee. For sprint searches, group
     the lines by status category (To Do, In Progress, Done). Say how many
     matched in total if there are more than you showed. If the JQL is
     rejected, fix it using the error message and retry once.
   - **Summarize** progress on an epic, sprint, or issue (read-only). For an
     epic, search its children; for a sprint, search the sprint; include
     done issues. Report: total issues and story points, how many are done,
     in progress, and to do (with points if the field exists), what's
     blocked (issues with a "blocked" status, a blocked flag or label, or an
     open "is blocked by" link), what's unassigned, and anything overdue.
     Lead with one sentence on overall state ("14 of 22 stories done, 3
     blocked"). For a single issue, summarize its description, latest
     comments, linked issues, and status history if available, in a few
     lines.

   Done when the calls succeed. If one fails, report Jira's error message in
   plain words. For a missing required field, ask for it and retry; for a
   permission error, say which action was refused and stop.

8. **Verify and report.** Search and summarize need no read-back. For every
   change, call `atlassian_getJiraIssue` with just the changed fields plus
   `status` and `assignee` (for a comment, check that the new comment
   appears with `fields: ["comment"]`, or that the add-comment call returned
   its ID; for a link, check `issuelinks`; for work logged, check the
   worklog call returned an ID). If an edit call already returned the
   updated issue with those fields, you may use that instead. For bulk
   changes and breakdowns, verify each issue and report them as a list.
   Done when the read-back matches and you've reported each key, browse
   URL, assignee, and status. If it doesn't match, say what differs; don't
   report success.

## Writing issues

**Summary.** State the consequence or benefit, not the mechanics, which go
under Approach: someone glancing at the board should see what improves
without opening the issue. For a bug, state the broken behavior and who it
hits. Keep it under about 80 characters.

```txt
BAD:  Add caching layer
GOOD: Eliminate redundant auth lookups to cut p99 latency

BAD:  Fix login bug
GOOD: SSO users are logged out after every deploy
```

**Description,** in Markdown. Use the feature template for Task, Story, Epic,
Feature, and Spike, and the bug template for Bug. Leave out a section only if
there's nothing true to put in it; don't invent repro steps, environments,
or numbers.

Feature template:

````md
## Problem

Current pain, risk, or missing capability.

## Goal

Target outcome for users or maintainers.

## Approach

- Implementation boundaries and constraints.
- What will not change.

## Outcome

Practical benefit in one short paragraph.
````

Bug template:

````md
## Summary

What's broken, who it affects, and how badly.

## Steps to Reproduce

1. First step.
2. Second step.

## Expected Behavior

What should happen.

## Actual Behavior

What happens instead, with error messages or logs.

## Environment

Version, browser or OS, account type, or anything else that narrows it down.
````

For a Spike, make the Goal the question to answer and the Outcome the
decision it enables, and add a timebox if the user gave one.

**Acceptance criteria.** Write them as testable statements, one behavior
each ("Exporting 10,000 rows completes in under 30 seconds"), not tasks
("Write export code"). With a custom field, put them there and not in the
description, in the format step 4 found. For a plain-text field, pass a
string with one criterion per line, each starting with `- `. For a rich-text
field, pass ADF: in `additional_fields` on create, or in `fields` on edit, as
`{"<customfield_id>": <adf>}`. Without a custom field, add an
`## Acceptance Criteria` section to the end of the description.

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [{ "type": "text", "text": "First criterion" }]
            }
          ]
        }
      ]
    }
  ]
}
```
