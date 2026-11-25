<p align="center">
  <picture><source media="(prefers-color-scheme: dark)" srcset="site/img/logo-oscuro.svg"><img src="site/img/logo.svg" width="96" alt="SoftwareFactory"></picture>
</p>

<h1 align="center">A new mod for Claude Code</h1>

<p align="center">
  <b>Go fast with Claude Code. Stay in control. In the terminal and the desktop app.</b><br>
  A mod plugs into Claude Code and changes how it works, without switching tools. <b>SoftwareFactory</b> adds a live panel,<br>
  a task queue and a way of working, for people who build alone or with a small team: every request becomes a task<br>
  with its own subagent and branch, they all work in parallel, and nothing goes public without a privacy check.
</p>

<p align="center">
  🇬🇧 English · <a href="README.es.md">🇪🇸 Leer en castellano</a>
</p>

<p align="center">
  <a href="https://github.com/jumibot/SoftwareFactory/releases"><img alt="Latest release" src="https://img.shields.io/github/v/tag/jumibot/SoftwareFactory?label=release&color=f5c400"></a>
  <a href="LICENSE"><img alt="MIT licence" src="https://img.shields.io/badge/licence-MIT-f5c400"></a>
  <img alt="Windows, macOS, Linux" src="https://img.shields.io/badge/Windows%20%C2%B7%20macOS%20%C2%B7%20Linux-555">
</p>

<p align="center">
  <a href="#install"><b>Install in 2 commands</b></a> &nbsp;|&nbsp; <a href="https://jumibot.github.io/SoftwareFactory/"><b>Take the tour on the website</b></a>
</p>

<p align="center">
  <img src="site/img/panel-en.svg" width="560" alt="The SoftwareFactory panel in Claude Code: seven tasks in progress, each with its subagent, one ready to test, 38 queued with a Start button, 3 in review, 124 closed and 12 proposals">
</p>

## Install

Once per computer:

```bash
claude plugin marketplace add jumibot/SoftwareFactory
claude plugin install sf@softwarefactory --scope user
```

Then open Claude Code and ask *“Check the SF installation”*: Claude reviews the plugin and the requirements and fixes what is missing, with your OK. Open your project, go full screen with `/tui fullscreen` or open the desktop app, and press the button on the welcome screen.

**You need** Claude Code, git, the GitHub CLI signed in (`gh auth login`) and Python 3.9 or later. Installing `sf` brings its three dependencies on its own.

## Don’t wait. Orchestrate.

Every task gets its own subagent, working in the background on its own branch. While they work, you keep talking to Claude: ask for more, or test another task. You never wait for one to finish before starting the next.

- Several subagents in parallel, one per task.
- Each on its own branch: they never step on each other.
- The panel shows every step as it happens.

## Claude knows what you’re on. And doesn’t interrupt.

> 🅵🅾🅲🆄🆂 `Fix accents in the CSV export (T❹ ❼ )`
>
> Fixed: the export is now UTF-8 with BOM, so Excel opens ñ and é. Ready to test on its branch.
>
> (`ᴏꜰꜰ-ᴛᴏᴘɪᴄ` T❹ ❽ : dark mode ready to test ▶️)

Every answer starts with the task you are focused on. News from other tasks waits for the end of an answer, in one short line. An idea that comes up halfway goes to the queue, not into the conversation.

> **Not to produce more. To ask for less of your attention.** That is the goal of SoftwareFactory: one person runs many projects at once, building, researching, teaching and learning, and the factory keeps count so your head stays free.

## Publish without fear

Before anything goes up to a public repository, SoftwareFactory checks what is leaving: secrets and keys, e-mails, paths from your machine, your user and machine name, local files. **If it finds something, it stops: nothing is pushed.** When it is clean, RELEASE moves `develop` to `main`, tags the version and pushes it, with one button.

| Goes out | Stays home |
|---|---|
| ✓ your code, your docs, the changelog | ✕ tokens and keys (`ghp_…`, private keys, passwords in code) |
| ✓ the version tag (`v1.3.0`) on `main` | ✕ e-mails, your user and machine name, your home folder paths |
| ✓ what was already public, without asking again | ✕ `.env`, the local queue and Claude Code local settings |

Only what is new counts: what was already public is not flagged again, and what you accept is not asked twice.

## Your project, told as a story

The vision document doesn’t list features: it tells a story, with a named protagonist, a real problem, scenes and chapters, and every feature shown in action at the moment it changes something for someone. It reads like a book, in an e-reader that turns the page. Around it, the rest of the document has a cover, folding sections, cards and interactive diagrams in your project’s own colours, and prints on A4.

## Same Claude. A very different day.

| Claude Code on its own | With SoftwareFactory |
|---|---|
| You ask for five things. Three get lost in the scroll. | Every request lands in a queue the moment you say it. |
| Every change piles up on the branch you happen to be on. | Each task works on its own branch, with its own agent, all at once. |
| The to-do list lives in your head. | One panel shows what is running, waiting and done. |
| You push and hope nothing private slipped in. | Every release is checked for secrets and personal data. |
| Each project means setting things up again. | Any project is ready after a few questions. |

## What you get

**No idea gets lost.** Say it in the chat, in your own words. Before any work starts, it is in the queue as a task with its steps. TURBO hands Claude every task that does not need you.

**You decide. Claude does the work.** Each task gets its own agent and its own branch. Nothing touches your stable code until you have tested it and said OK. Start a queued task with one click (**Start**, in the panel); when it is ready, one click closes it into one clean commit.

**Everything at a glance, wherever you use Claude Code.** The same live panel beside the chat, in the terminal and in the desktop app; not in full screen, a small box above the prompt keeps the essentials. Close, discard or revert a task with a click. The same marks in the chat and in the panel: 🟢 working, 🔴 finished and waiting, ▶️ ready to test, 👀 in review, 🔒 closed.

**Your projects, as they are.** Bring in a project you already have, or start from an empty folder. A few questions as menus and it is ready, without moving or renaming your code. No GitHub repository yet? Onboarding creates one with your OK. After reloading the plugins, it carries on by itself.

**Nothing is taken for granted.** Every close says what changed, what was checked and what is pending. A subagent that hits a block says so; it never works around it.

**A method, if you want one.** Turn it on and Claude guides the project from vision and spec to code, in small vertical slices, keeps every decision on file with its reason and writes documents people actually read, with interactive diagrams.

| No idea gets lost | Publish without fear |
|:---:|:---:|
| <img src="site/img/request-en.svg" width="380" alt="You ask in the chat, Claude turns it into tasks 47 and 48, and a subagent works through the steps"> | <img src="site/img/publish-en.svg" width="380" alt="RELEASE reviews nine new commits, finds a personal path and blocks publishing until it is fixed"> |

Good to know: today the panel and the generated documents are in Spanish; Claude talks to you in your language.

<p align="center">
  <a href="https://jumibot.github.io/SoftwareFactory/"><b>See every feature on the website</b></a>
</p>

## More

- [Website](https://jumibot.github.io/SoftwareFactory/): the full tour, in English and Spanish.
- [The plugin](plugins/sf/README.md): what it contains and how it is published (in Spanish).
- [Development guide](DESARROLLO.md): for those working on SoftwareFactory itself (in Spanish).
- [Third-party licences](plugins/sf/LICENCIAS-DE-TERCEROS.md).

SoftwareFactory is free software under the [MIT licence](LICENSE).
