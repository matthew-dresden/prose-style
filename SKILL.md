---
name: prose-style
description: Enforce a personal prose and document standard derived from pre-LLM US English. Use when drafting, editing, or reviewing prose or documentation.
metadata:
  version: "0.2.1"
  trigger: Writing or editing prose, documentation, comments, or reviewing text for AI patterns and punctuation violations
  author: Matthew Dresden
  derived-from: Hardik Pandya (https://hvpandya.com), stop-slop, MIT
---

# Prose Style

Write prose the way careful American writers wrote before text-generation
models existed, and keep documents in that same voice throughout.

## Core Rules

1. **Cut filler phrases.** Remove throat-clearing openers, emphasis crutches, and all adverbs. See [references/phrases.md](references/phrases.md).

2. **Break formulaic structures.** Avoid binary contrasts, negative listings, dramatic fragmentation, rhetorical setups, false agency. See [references/structures.md](references/structures.md).

3. **Use active voice.** Every sentence needs a human subject doing something. No passive constructions. No inanimate objects performing human actions ("the complaint becomes a fix").

4. **Be specific.** No vague declaratives ("The reasons are structural"). Name the specific thing. No lazy extremes ("every," "always," "never") doing vague work.

5. **Put the reader in the room.** No narrator-from-a-distance voice. "You" beats "People." Specifics beat abstractions.

6. **Vary rhythm.** Mix sentence lengths. Two items beat three. End paragraphs differently.

7. **Trust readers.** State facts directly. Skip softening, justification, hand-holding.

8. **Cut quotables.** If it sounds like a pull-quote, rewrite it.

9. **No dashes as punctuation.** No em dashes, no en dashes, and no double-hyphen "--" substitute. They are the most recognizable machine-writing tell alive today. Rewrite the sentence with the punctuation it calls for: a comma, a colon, a semicolon, parentheses, or a period. Never swap one dash for another; each replacement is a sentence-level rewrite, never a punctuation search-and-replace.

10. **Standard US English.** Grammar, punctuation, and spelling follow the conventions of careful American professional writing as practiced before text-generation models. This is a floor, not a stylistic personality: plain, correct, and specific.

## Documents

Documentation follows the same voice, plus three structural rules:

1. **Present state only.** Documents describe what a thing is and does now. No change history, no "previously," no "was / is now" tables. Changelogs carry history; prose carries the current state.

2. **Structure for scanning.** Headings in order, lists nested where items group naturally, code in fenced blocks. Indentation and nesting exist so a reader can skip to their depth.

3. **Progressive disclosure.** Lead with the fastest path to a working result. Link deeper material instead of inlining it, and make each drill-down destination worth the click: explanation, worked examples, and diagrams where they help.

## Quick Checks

Before delivering prose:

- Any adverbs? Kill them.
- Any passive voice? Find the actor, make them the subject.
- Inanimate thing doing a human verb ("the decision emerges")? Name the person.
- Sentence starts with a Wh- word? Restructure it.
- Any "here's what/this/that" throat-clearing? Cut to the point.
- Any "not X, it's Y" contrasts? State Y directly.
- Three consecutive sentences match length? Break one.
- Paragraph ends with punchy one-liner? Vary it.
- Em dash, en dash, or "--" anywhere in prose? Rewrite the sentence.
- Vague declarative ("The implications are significant")? Name the specific implication.
- Narrator-from-a-distance ("Nobody designed this")? Put the reader in the scene.
- Meta-joiners ("The rest of this essay...")? Delete. Let the essay move.
- Document describing what something "used to" be? Cut it to the present state.

## Scoring

Rate 1-10 on each dimension:

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human? |
| Density | Anything cuttable? |

Below 35/50: revise.

## Examples

See [references/examples.md](references/examples.md) for before/after transformations.

## Origin and license

Derived from [stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik
Pandya, MIT licensed. This fork is Apache 2.0; see [NOTICE](NOTICE) and
[LICENSE](LICENSE) for the upstream attribution the MIT license requires.
