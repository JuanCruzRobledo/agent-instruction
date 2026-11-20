<!-- active-stack:team-mode -->
## Reglas de equipo

Proyecto de equipo: la configuración vive en `.active-stack/team.json`.

- Al iniciar la sesión, si existe `.active-stack/team.json`, usá la skill `active-delivery` para identificar a la persona y mostrar «qué me toca». Detalle en las `references/` de esa skill.
- Una rama y un worktree por ficha: `<id>-slug`. Nunca dos agentes en la misma rama o carpeta.
- Nada directo a `main`. PR chicos. Commit, push y PR solo con autorización de la persona.
- No inventes nombres ni cuentas de integrantes: lo que falte queda pendiente hasta que el equipo lo complete.

**Si la skill `active-delivery` no está disponible en este cliente**, aplicá la misma convención a mano:

1. Una rama por ficha (`<id>-slug`) creada desde la rama principal actualizada.
2. Todo cambio entra por pull request; sin push a `main` ni force-push.
3. Al terminar, dejá el handoff en `knowledge-base/entrega/<id>.md`: qué se hizo, cómo se verificó, qué sigue y qué decisiones quedan abiertas.
<!-- /active-stack:team-mode -->
