from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
TEMPLATE = (ROOT / "assets/agents-template.md").read_text(encoding="utf-8")


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


if __name__ == "__main__":
    unittest.main()
