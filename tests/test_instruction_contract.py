from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
TEMPLATE = (ROOT / "assets/agents-template.md").read_text(encoding="utf-8")
TEAM = (ROOT / "assets/team-rules-template.md").read_text(encoding="utf-8")
TEAM_OPEN = "<!-- active-stack:team-mode -->"
TEAM_CLOSE = "<!-- /active-stack:team-mode -->"


def team_section():
    match = re.search(r"(?ms)^### Reglas de equipo.*?(?=^#{2,3} |\Z)", SKILL)
    return match.group(0) if match else ""


class InstructionContractTests(unittest.TestCase):
    def test_project_guidance_works_without_sdd_or_registry(self):
        self.assertNotRegex(TEMPLATE, r"(?i)openspec|/opsx:|skill de propuesta")
        self.assertRegex(SKILL, r"(?im)^.*si (?:falta|no existe) el registro.*omit[ií]")
        self.assertIn("inventario de skills del cliente activo", SKILL)

    def test_destinations_and_project_rules_follow_approved_inputs(self):
        self.assertRegex(SKILL, r"(?im)^.*rutas .*plan confirmado")
        self.assertIn("si hay rutas faltantes y existentes", SKILL.lower())
        self.assertRegex(SKILL, r"(?i)STOP y esperá la respuesta")
        self.assertNotIn("~/.claude/", SKILL + TEMPLATE)

    def test_instruction_links_follow_each_destination_but_state_paths_use_root(self):
        for prefix in ("", "../"):
            with self.subTest(prefix=prefix):
                for source in ("knowledge-base/", "CHANGES.md", ".atl/skill-registry.md"):
                    self.assertIn(f"`{prefix}{source}`", SKILL)
        self.assertRegex(SKILL, r"(?im)^.*resolvé .*enlaces.*directorio.*archivo de instrucciones")
        self.assertRegex(SKILL, r"(?im)^.*`state\.agents\.files`.*relativas a la raíz")
        self.assertRegex(SKILL, r"(?im)^- .*`reuse`.*enlace")
        self.assertIn("destinos anidados", TEMPLATE)

    def test_existing_project_preserves_user_text_and_records_real_outputs(self):
        self.assertRegex(SKILL, r"(?im)^- .*`reuse`.*sin escribir")
        self.assertIn("<!-- active-stack:agent-instruction -->", SKILL)
        self.assertIn("<!-- /active-stack:agent-instruction -->", SKILL)
        self.assertRegex(SKILL, r"(?im)^.*snapshot.*antes de escribir")
        self.assertRegex(SKILL, r"(?im)^.*`state\.agents\.files`.*verificad")


class TeamRulesTests(unittest.TestCase):
    def test_team_block_has_its_own_markers_distinct_from_the_project_block(self):
        self.assertEqual(TEAM.count(TEAM_OPEN), 1)
        self.assertEqual(TEAM.count(TEAM_CLOSE), 1)
        self.assertLess(TEAM.index(TEAM_OPEN), TEAM.index(TEAM_CLOSE))
        self.assertNotIn("active-stack:agent-instruction", TEAM)
        for marker in (TEAM_OPEN, TEAM_CLOSE):
            self.assertIn(marker, team_section())

    def test_team_block_is_short_and_points_to_the_skill_for_detail(self):
        body = TEAM.split(TEAM_OPEN, 1)[1].split(TEAM_CLOSE, 1)[0].strip().splitlines()
        self.assertLessEqual(len(body), 25)
        self.assertIn("active-delivery", TEAM)
        self.assertIn(".active-stack/team.json", TEAM)
        self.assertIn("`<id>-slug`", TEAM)

    def test_team_block_carries_the_manual_fallback(self):
        self.assertRegex(TEAM, r"(?i)si la skill `active-delivery` no est[aá] disponible")
        self.assertIn("knowledge-base/entrega/<id>.md", TEAM)
        self.assertRegex(TEAM, r"(?i)nada directo a `main`")
        self.assertRegex(TEAM, r"(?i)solo con autorizaci[oó]n")

    def test_team_block_holds_no_names_accounts_or_credentials(self):
        self.assertNotRegex(TEAM, r"(?i)token|secret|password|bearer|ghp_|clickup_id")
        self.assertNotRegex(TEAM, r"\bAna\b|Integrante \d")

    def test_team_section_is_only_written_with_a_confirmed_team(self):
        section = team_section()
        self.assertRegex(section, r"(?i)solo .*equipo confirmado")
        self.assertRegex(section, r"(?i)sin equipo confirmado.*id[eé]ntic")
        self.assertRegex(section, r"(?i)no inventes (?:nombres|integrantes)")

    def test_team_section_is_idempotent_and_never_duplicates(self):
        section = team_section()
        self.assertRegex(section, r"(?i)reemplaz[aá].*una sola vez")
        self.assertRegex(section, r"(?i)marcadores (?:incompletos|repetidos).*conflicto")
        self.assertRegex(section, r"(?i)no dupliques")

    def test_team_section_keeps_other_managed_blocks_and_uses_a_snapshot(self):
        section = team_section()
        self.assertRegex(section, r"(?i)bloques administrados por otros arneses")
        self.assertRegex(section, r"(?i)snapshot.*antes de escribir")

    def test_team_rules_go_to_the_project_file_not_the_global_one(self):
        section = team_section()
        self.assertRegex(section, r"(?i)archivo de instrucciones del proyecto")
        self.assertRegex(section, r"(?i)nunca en el global")


if __name__ == "__main__":
    unittest.main()
