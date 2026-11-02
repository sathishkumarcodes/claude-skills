# Claude Skills

A collection of custom skills for [Claude](https://claude.ai). Each skill is a
folder under `skills/` containing a `SKILL.md` with instructions Claude follows
when the skill is loaded.

## Skills

| Skill | Invoke with | What it does |
| --- | --- | --- |
| [jira](skills/jira/) | `/jira` | Create, edit, comment on, assign, transition, link, search and summarize Jira issues; manage sprints; break features into stories |
| [no-ai-slop](skills/no-ai-slop/) | automatic, or `/no-ai-slop` | Edit drafts into sharper, more human writing in the writer's own voice, or flag AI-slop patterns without rewriting |

## Installing a skill in Claude

1. Turn on code execution (Settings > Capabilities on Free/Pro/Max; on
   Team/Enterprise an owner enables it in Organization settings > Skills).
2. Build the ZIP for the skill you want:

   ```sh
   ./scripts/package.sh jira      # one skill → dist/jira.zip
   ./scripts/package.sh           # every skill
   ```

   Or download a ready-made ZIP from the latest run of the **Validate and
   package skills** workflow (Actions tab → run → Artifacts).
3. In Claude, go to Customize > Skills, click **+** → **Create skill** →
   **Upload a skill**, and choose the ZIP.
4. Make sure the skill's toggle is on.

Some skills need a connector too; each skill's README says which.

To update a skill, delete the old one in Claude and upload the new ZIP.

## Adding a new skill

1. Copy the template: `cp -r templates/skill skills/<name>`
2. Edit `skills/<name>/SKILL.md`. The folder name must match the `name` in the
   frontmatter (lowercase letters, numbers and hyphens).
3. Fill in `skills/<name>/README.md` with setup and example requests.
4. Run `./scripts/package.sh <name>` to check it and build the ZIP.
5. Add a row to the table above.

## Layout

```
skills/<name>/SKILL.md     the skill itself (what Claude reads)
skills/<name>/README.md    setup and examples (for people; not uploaded)
templates/skill/           starting point for new skills
scripts/package.sh         validates and zips skills into dist/
```
