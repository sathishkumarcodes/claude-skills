# no-ai-slop skill

Edits drafts into sharper, more human writing while keeping the writer's
voice, or flags AI-slop patterns without rewriting. It never adds facts:
where a sentence needs a number, source, or example the draft doesn't have,
it leaves a marker like `[source?]` and lists it for you.

Claude picks this skill automatically when you ask it to tighten a draft or
check whether something reads as AI. You can also invoke it as `/no-ai-slop`.

## Files

- `SKILL.md`: the editing rules and workflow.
- `eval.md`: the checklist Claude runs on its own edit before returning it.

## Install

```sh
./scripts/package.sh no-ai-slop
```

Upload `dist/no-ai-slop.zip` in Claude under Customize > Skills → **+** →
**Create skill** → **Upload a skill**. No connector needed.

## Examples

| Request | What happens |
| --- | --- |
| `Make this less AI-sounding: <draft>` | Edited draft + What changed + any `[source?]`-style markers |
| `Tighten this LinkedIn post, keep my tone: <draft>` | Minimal edit that keeps your voice |
| `Does this read as AI? Don't rewrite it. <draft>` | Table of patterns found, with quotes and fixes |
| `Audit this blog post for slop` | Same detect report |
| `Edit this short story, but only fix the AI tics` | Fiction mode: keeps metaphor, fragments, and endings |
| `Clean up this 3,000-word essay` | Asks whether you want the full draft or edits by section |

## What it leaves alone

Quotes, code, citations, names, numbers, data, legal or regulated wording,
and technical uses of words on its cut list ("robust standard errors").
