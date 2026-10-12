# prose-style

A skill for writing prose the way careful American writers wrote before
text-generation models existed: no AI tells, no dashes standing in for
punctuation, and documents that describe only the current state.

Derived from [stop-slop](https://github.com/hardikpandya/stop-slop) by
Hardik Pandya (MIT); this fork is Apache 2.0, with the upstream attribution
retained in [NOTICE](NOTICE).

## What this is

AI writing has patterns. Predictable phrases, structures, rhythms, and,
most recognizable of all, dashes standing in for punctuation. This skill
teaches an LLM to catch and remove them, then to rewrite the sentence with
the punctuation it actually calls for.

## Skill Structure

```text
prose-style/
├── SKILL.md              # Core instructions
├── references/
│   ├── phrases.md        # Phrases to remove
│   ├── structures.md     # Structural patterns to avoid
│   └── examples.md       # Before/after transformations
├── NOTICE                # Upstream attribution (MIT notice retained)
├── LICENSE               # Apache License 2.0
└── .github/workflows/    # CI: lint, spell, frontmatter, no-dash self-check
```

## Quick start

**Claude Code:** Add this folder as a skill.

**Claude Projects:** Upload `SKILL.md` and reference files to project knowledge.

**Custom instructions:** Copy core rules from `SKILL.md`.

**API calls:** Include `SKILL.md` in your system prompt. Reference files load on demand.

**opencode:** Place the folder under `~/.config/opencode/skills/`.

## What it catches

**Banned phrases:** throat-clearing openers, emphasis crutches, business
jargon, all adverbs, vague declaratives, meta-commentary. See
`references/phrases.md`.

**Structural clichés:** binary contrasts, negative listings, dramatic
fragmentation, rhetorical setups, false agency, narrator-from-a-distance
voice, passive voice. See `references/structures.md`.

**Sentence-level rules:** no Wh- sentence starters, no staccato
fragmentation, no lazy extremes, active voice required.

**Dashes as punctuation:** no em dashes, no en dashes, and no double-hyphen
substitute. Each violation is rewritten at the sentence level with standard
US English punctuation.

**Documents:** present state only, structured for scanning, with deeper
material linked rather than inlined.

## CI

This repository enforces its own rules on itself. The workflow lints the
markdown, spell-checks in US English, checks the skill frontmatter, and
fails on any prose em dash, en dash, or double-hyphen substitute in its
own files.

## Releases

Releases are fully automated. Every merge to main produces a semantic
version release with an updated changelog and version files.

1. Open a pull request with a conventional commit title. `feat` maps to a
   minor bump, `fix` and `chore` and their siblings map to patch, and a
   `!` suffix maps to major.
2. CI validates the title and runs lint, spell, prose, unit, and version
   immutability checks. Green CI enables automatic squash merge.
3. The merge triggers Main Validation, which validates main, calculates
   the next version from git tags, and opens an automated release pull
   request that bumps `pyproject.toml` and the `SKILL.md` frontmatter and
   prepends the changelog entry.
4. The release pull request merges on green CI. The merge creates the
   `vX.Y.Z` tag and the GitHub Release with the changelog entry as notes.

Version files (`pyproject.toml`, `SKILL.md`) are owned by the pipeline.
Manual edits to version lines are rejected in CI by the version
immutability check. The pipeline authenticates through the
`matthew-dresden-cicd` GitHub App; no personal access tokens appear in
any workflow. The App ID and private key live in AWS SSM Parameter
Store and the repository's Actions secrets.

## License

Apache License 2.0, with the upstream MIT notice retained in NOTICE. Use
freely, share widely, attribute upstream.
