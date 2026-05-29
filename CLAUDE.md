# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not an application** — it is a curated **Claude Code skills pack** for AI-assisted
video and animation production. The entire repository is `.claude/skills/`: a collection of
self-contained skills that give Claude domain expertise in Remotion, motion graphics, web
animation, and media processing. There is no `package.json`, build system, lint config, or test
suite at the root. The commit history calls this the "editor-pro-max" skill set.

"Developing in this codebase" therefore means **authoring and maintaining skills**, not building
or running an app. The skills themselves are *invoked* during other sessions to produce videos.

## The skills

| Skill | Purpose | Activation |
|-------|---------|------------|
| `remotion-best-practices` | Domain knowledge for writing Remotion (React-based video) code. Index `SKILL.md` points to ~40 focused `rules/*.md` files (animations, audio, charts, captions, 3D, fonts, etc.) | Loaded whenever working with Remotion code |
| `remotion-render` | Renders TSX/Remotion component code to MP4 via the inference.sh CLI (`infsh app run infsh/remotion-render`) | Code-to-video, programmatic video generation |
| `motion-designer` | Produces detailed scene-by-scene video *specifications* (timing, audio, SFX, transitions). Output feeds `remotion-best-practices` for implementation | "create a video", "spec out a video", motion graphics planning |
| `explainer-video-guide` | End-to-end explainer-video pipeline (script formulas, pacing, assembly) via inference.sh | Product demos, onboarding/tutorial videos |
| `awwwards-animations` | Premium web animation (GSAP/useGSAP, Motion, Anime.js, Lenis, Three.js, generative/algorithmic art). React-first, 60fps. References in `references/*.md` | Scroll experiences, page transitions, kinetic typography, generative art |
| `animated-component-libraries` | Pre-built animated React components (Magic UI, React Bits, shadcn/ui). Includes Python helper scripts | Landing pages, dashboards, pre-made animated UI |
| `ffmpeg` | Media processing recipes (convert, resize, compress, extract audio, prepare assets for Remotion) | Format conversion, media transforms |
| `playwright-mcp` | Live browser automation via the Playwright MCP server | Navigating/inspecting/screenshotting web UIs |

These skills are designed to compose: `motion-designer` (spec) → `remotion-best-practices`
(implement) → `remotion-render`/`ffmpeg` (render & post-process).

## Skill structure conventions

Every skill is a directory under `.claude/skills/<name>/` containing a `SKILL.md` with YAML
frontmatter. When authoring or editing skills, preserve these conventions — they are how Claude
discovers and loads skills:

- **`name`** (required): must match the directory name.
- **`description`** (required): the most important field. It is trigger-matched to decide when the
  skill loads, so it must be densely packed with concrete trigger phrases and tool/library names
  (see `awwwards-animations` and `remotion-render` for the established style). Vague descriptions
  mean the skill won't activate.
- **`allowed-tools`** (optional): restricts tools, e.g. `Bash(infsh *)` for the inference.sh skills.
- **`metadata`** (optional): `version`, `tags`, `mcp-server`.

**Progressive disclosure is the core pattern.** Keep `SKILL.md` short and use it as an index that
links to detail files which are loaded on demand. Two layouts are used:
- `rules/` — deep reference docs (`remotion-best-practices`, `motion-designer`).
- `references/` — supplementary catalogs/guides (`awwwards-animations`, `animated-component-libraries`).
Other subdirs: `scripts/` (executable helpers), `assets/` (sample/template files).

Link to detail files with relative paths (e.g. `[./rules/subtitles.md](./rules/subtitles.md)`) so
Claude loads them only when the specific task needs them.

## Commands

There is nothing to build, lint, or test in this repo. The commands that matter are the ones the
skills tell Claude to run when producing videos:

```bash
# Render Remotion TSX code to MP4 (remotion-render / explainer-video-guide)
infsh login
infsh app run infsh/remotion-render --input '{ "code": "...", "duration_seconds": 3, "fps": 30, "width": 1920, "height": 1080 }'

# Media processing (ffmpeg skill) — e.g. GIF → Remotion-compatible MP4
ffmpeg -i input.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" output.mp4

# Helper scripts in animated-component-libraries
.claude/skills/animated-component-libraries/scripts/component_importer.py --library magicui --component grid-pattern
.claude/skills/animated-component-libraries/scripts/props_generator.py --component shimmer-button --format typescript
```

The inference.sh skills require the `infsh` CLI (`Bash(infsh *)` is their only allowed tool).
`playwright-mcp` requires the Playwright MCP server and uses `mcp__playwright__*` tool calls
directly (never shelled out).

## Key conventions when working here

- **Editing a skill = editing Markdown/scripts under its directory.** Do not add app scaffolding,
  package manifests, or test harnesses at the root — that is not what this repo is.
- **Keep the index/detail split.** New domain knowledge goes in a `rules/`/`references/` file that
  the `SKILL.md` index links to, not inline in `SKILL.md`.
- **When adding a skill,** create `.claude/skills/<name>/SKILL.md` with a trigger-rich
  `description`, and mirror the frontmatter style of existing skills.
- **Remotion code targets the inference.sh renderer:** components `export default` a function and
  import only from `remotion` and `react` (see `remotion-render/SKILL.md` for the supported API
  surface). 60fps and even pixel dimensions are recurring hard requirements across the video skills.
- Commit messages in this repo are written in **Spanish** (e.g. "Instala skills de edición de
  video…"); match that style.
