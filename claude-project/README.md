# Setting up the claude.ai Project

1. In the Claude app / claude.ai, open **Projects → Create project**.
2. **Name:** `Vaidam LinkedIn Autopilot`
   **Description:** `Daily LinkedIn posts and carousels on Indian business compliance for Vaidam Consultancy LLP.`
3. **Set project instructions:** paste the whole of `PROJECT_INSTRUCTIONS.md`.
4. **Add files (project knowledge):** upload
   `CLAUDE.md`, `HANDOFF.md`, `hooks.json`, `example-post.txt`,
   `example-content.json`, `build_carousel.py`.
5. Start a chat in the project, e.g. "Write Monday's deadlines post".

A Project chat can research and draft, but it can't post to LinkedIn or run
on a schedule. Automatic daily posting runs through Claude Code (see HANDOFF.md).
