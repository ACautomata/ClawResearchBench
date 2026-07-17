from __future__ import annotations

import unittest

from harness.loader import custom_checks_root, load_scenario, scenarios_root


RESEARCH_ROOT = scenarios_root() / "research"

# Each deep grader owns its config shape. The manifest test asserts the keys a
# grader fail-fasts on, without coupling to grader internals.
GRADER_REQUIRED_KEYS = {
    "idea_generate_grader.py": (["keywords"], ["keywords", "forbidden_phrases"]),
    "paper_review_grader.py": (
        ["outputs", "keywords"],  # multi-output pipeline shape
        ["output", "must_contain", "must_not_contain", "fields"],  # single-output shape
    ),
}


def _config_matches_shape(config: dict, shapes) -> bool:
    return any(all(k in config for k in shape) for shape in shapes)


class ResearchManifestCoverageTests(unittest.TestCase):
    """Every research scenario must resolve to a real grader/standalone with the
    config its grader requires. Guards the migration's data integrity without
    coupling to grader internals.
    """

    def test_every_research_scenario_resolves_with_required_config(self) -> None:
        yaml_paths = sorted(RESEARCH_ROOT.glob("*.yaml"))
        self.assertGreater(len(yaml_paths), 0, "no research scenarios discovered")
        checks_root = custom_checks_root()
        for yaml_path in yaml_paths:
            with self.subTest(scenario=yaml_path.name):
                scenario = load_scenario(yaml_path)
                self.assertTrue(
                    scenario.custom_check, f"{yaml_path.name} has no custom_check"
                )
                target = (checks_root / scenario.custom_check).resolve()
                self.assertTrue(
                    target.exists(),
                    f"{yaml_path.name}: custom_check {scenario.custom_check!r} does not resolve",
                )
                grader_name = target.name
                if grader_name in GRADER_REQUIRED_KEYS:
                    config = scenario.custom_check_config
                    self.assertIsInstance(
                        config, dict, f"{yaml_path.name}: custom_check_config is not a dict"
                    )
                    self.assertGreater(
                        len(config), 0, f"{yaml_path.name}: empty custom_check_config for grader"
                    )
                    shapes = GRADER_REQUIRED_KEYS[grader_name]
                    self.assertTrue(
                        _config_matches_shape(config, shapes),
                        f"{yaml_path.name}: config {sorted(config)} matches none of {shapes}",
                    )


if __name__ == "__main__":
    unittest.main()
