# Un worktree es el proyecto de su repositorio

- **Origen:** SoftwareFactory, 2026-10-29. El control «un proyecto por sesión» bloqueaba a los subagentes en sus worktrees (`.claude/worktrees/agent-…`): los tomaba por otro proyecto.
- **Decisión:** un worktree de git cuenta como el proyecto de su repositorio. Se reconoce por su `.git`, un archivo `gitdir: <repo>/.git/worktrees/<n>`. Así el subagente escribe en su worktree, y el worktree de otro proyecto sigue bloqueado.
- **Aplicada en:** metodología, 2 («Un proyecto por sesión»); mod, `control.ts`; Cómo funciona el panel («Qué controla»); Cómo funciona la Software Factory.
