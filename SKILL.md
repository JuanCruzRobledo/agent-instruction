---
name: agents-md-generator
description: >
  Genera el AGENTS.md / CLAUDE.md canónico del proyecto a partir de la KB y el roadmap:
  stack tecnológico, referencia a knowledge-base/, skills disponibles por agente,
  roadmap de changes (CHANGES.md) y las reglas duras del proyecto. Fire-and-forget, sin preguntas.
  Trigger: cuando el usuario pide crear/generar/actualizar AGENTS.md o CLAUDE.md, "armar las reglas del proyecto",
  "instrucciones para los agentes", "generar claude.md", o tras correr kb-creator + roadmap-generator.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Generar el `AGENTS.md` (+ symlink/copia `CLAUDE.md`) que todo agente lee al entrar al repo.
- Consolidar en un solo archivo: stack, KB, skills por agente, roadmap y reglas duras.
- Refrescar las instrucciones del proyecto tras cambios en la KB o en `CHANGES.md`.

**Don't use when:**
- No existe `knowledge-base/` (corré `kb-creator` primero).
- El usuario quiere editar UNA regla puntual (sugerí editar el `AGENTS.md` existente en su lugar).
- Se busca configurar comportamiento automático del harness (eso son hooks en `settings.json`, no AGENTS.md).

## Critical Patterns

### Pre-checks (si falla, NO generes y avisá)

| Check | Si falla |
|-------|----------|
| `knowledge-base/` existe en raíz | "Falta la KB. Corré `kb-creator` primero." |
| `knowledge-base/02_descripcion_general.md` existe | "KB incompleta. Corré `kb-creator`." |
| `CHANGES.md` existe en raíz | Generá igual, pero omití la sección Roadmap y avisá: "Sin CHANGES.md — corré `roadmap-generator` para incluir el roadmap." |

### Output — ubicación

Generá **`AGENTS.md` en la raíz** y un **`CLAUDE.md` en la raíz** con el mismo contenido (copia, no referencia: muchos harness leen uno u otro). Nunca dentro de `.claude/` ni `openspec/`.

### Input — qué leer

1. `knowledge-base/02_descripcion_general.md` → stack tecnológico (copiá la tabla).
2. `knowledge-base/README.md` → nombre del proyecto + resumen ejecutivo.
3. `CHANGES.md` → camino crítico, fases y primer change (resumen, NO el detalle completo).
4. `.atl/skill-registry.md` (si existe) → **fuente de verdad de las skills disponibles** (nombres + triggers + paths). Es lo que genera `skill-registry`; leelo de ahí, no re-escanees. *Fallback* si no existe: escaneá `.claude/skills/` + `~/.claude/skills/`. En ambos casos, agrupá las skills por rol de agente.
5. `knowledge-base/10_preguntas_abiertas.md` → flag de inconsistencias Alta a resolver antes de codear.

### Las 7 reglas duras (SIEMPRE presentes, textual)

El AGENTS.md DEBE incluir esta sección literal — son contrato, no sugerencias:

1. **No buildear automático** — nunca correr build/compile sin pedido explícito del usuario.
2. **No commitear sin pedido explícito** — git add/commit/push solo cuando el usuario lo pide.
3. **Conventional Commits sin `Co-Authored-By`** — `tipo(scope): mensaje`; jamás atribución a IA.
4. **Tests sin mocks de DB** — usar base real/contenedor de test; mockear la DB invalida el test.
5. **Pydantic schemas con `extra='forbid'`** — rechazar campos no declarados.
6. **snake_case en Python** — funciones, variables, columnas, módulos.
7. **PascalCase en componentes React** — y los archivos de componente.

### Skills por agente

Mapeá las skills detectadas a los roles de agente del proyecto. Estructura sugerida:

| Agente | Rol | Skills que carga |
|--------|-----|------------------|
| Backend Core | FastAPI/SQLModel/UoW | `fastapi-templates`, `python-testing-patterns`, `postgresql-table-design` |
| Backend Aux | Servicios/integraciones | `api-security-best-practices`, `test-driven-development` |
| Frontend | React/Zustand/TanStack | `typescript-advanced-types`, `tailwind-design-system`, `playwright-best-practices` |
| Orquestación | OPSX/SDD | `kb-creator`, `roadmap-generator`, `agents-md-generator` |

Adaptá las filas a las skills realmente presentes en el repo. No inventes skills que no existen.

**DRY — no copies los compact rules acá.** El `AGENTS.md`/`CLAUDE.md` solo mapea skill→rol (decisión de arquitectura, versionada). Los compact rules de cada skill viven SOLO en `.atl/skill-registry.md` (no versionado); el orquestador los resuelve en runtime. Debajo de la tabla, agregá esta línea textual de referencia:

> Los compact rules de cada skill los resuelve el orquestador desde `.atl/skill-registry.md` (generado por `skill-registry`; no versionado — no está en el repo).

## Code Examples

Ver la plantilla completa en [assets/agents-template.md](assets/agents-template.md). Estructura de primer nivel (no quitar secciones):

```markdown
# {Proyecto} — Instrucciones para Agentes
## Stack Tecnológico        → tabla desde KB 02
## Base de Conocimiento     → links a knowledge-base/*.md
## Skills Disponibles       → tabla skill→rol (desde el registry) + línea de referencia a `.atl/skill-registry.md` para los compact rules
## Roadmap de Changes       → resumen de CHANGES.md + primer change
## Reglas Duras (no negociables)  → las 7 reglas, textual
## Flujo de Trabajo         → KB → CHANGES → /opsx:propose → archive
```

## Commands

```bash
# Fuente de verdad de skills: el registry (si existe). Fallback: escaneo directo.
test -f .atl/skill-registry.md && cat .atl/skill-registry.md || ls .claude/skills/ ~/.claude/skills/

# Verificar pre-checks
ls knowledge-base/ CHANGES.md

# Tras generar, validar que ambos archivos quedaron sincronizados
diff AGENTS.md CLAUDE.md && echo "OK: sincronizados"
```

## Resources

- **Templates**: ver [assets/agents-template.md](assets/agents-template.md) — plantilla completa de `AGENTS.md` con las 7 reglas duras y todas las secciones de contrato.
