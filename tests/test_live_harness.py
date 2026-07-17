from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from harness.live_harness import AgentPoolSlot, AuthProfileCopyResult, OpenClawLiveHarness


class LiveHarnessTests(unittest.TestCase):
    def test_profile_isolation_populates_state_dir_config_path_and_dev_port(self) -> None:
        harness = OpenClawLiveHarness(openclaw_profile="dev")

        expected_state_dir = (Path.home() / ".openclaw-dev").resolve(strict=False)
        expected_config_path = (expected_state_dir / "openclaw.json").resolve(strict=False)

        self.assertEqual(harness.command_env["OPENCLAW_PROFILE"], "dev")
        self.assertEqual(harness.command_env["OPENCLAW_STATE_DIR"], str(expected_state_dir))
        self.assertEqual(harness.command_env["OPENCLAW_CONFIG_PATH"], str(expected_config_path))
        self.assertEqual(harness.command_env["OPENCLAW_GATEWAY_PORT"], "19001")

    def test_state_dir_isolation_keeps_explicit_state_dir(self) -> None:
        harness = OpenClawLiveHarness(openclaw_state_dir="/tmp/openclaw-bench-a")

        self.assertEqual(harness.command_env["OPENCLAW_STATE_DIR"], "/tmp/openclaw-bench-a")
        self.assertRegex(harness.command_env["OPENCLAW_PROFILE"], r"^bench-openclaw-bench-a-[0-9a-f]{10}$")

    def test_state_dir_isolation_derives_stable_profile_when_profile_not_explicit(self) -> None:
        harness_a = OpenClawLiveHarness(openclaw_state_dir="/tmp/openclaw-bench-a")
        harness_b = OpenClawLiveHarness(openclaw_state_dir="/tmp/openclaw-bench-a")
        expected_root = Path("/tmp/openclaw-bench-a").resolve(strict=False)

        self.assertEqual(harness_a.command_env["OPENCLAW_PROFILE"], harness_b.command_env["OPENCLAW_PROFILE"])
        self.assertEqual(harness_a.command_env["OPENCLAW_STATE_DIR"], "/tmp/openclaw-bench-a")
        self.assertEqual(harness_a.command_env["OPENCLAW_CONFIG_PATH"], str(expected_root / "openclaw.json"))

    def test_explicit_profile_wins_over_derived_isolation_profile(self) -> None:
        harness = OpenClawLiveHarness(
            openclaw_profile="bench-a",
            openclaw_state_dir="/tmp/openclaw-bench-a",
        )

        self.assertEqual(harness.command_env["OPENCLAW_PROFILE"], "bench-a")

    def test_config_path_isolation_derives_matching_state_dir_and_profile(self) -> None:
        harness = OpenClawLiveHarness(openclaw_config_path="/tmp/openclaw-bench-c/openclaw.json")
        expected_root = Path("/tmp/openclaw-bench-c").resolve(strict=False)

        self.assertEqual(harness.command_env["OPENCLAW_CONFIG_PATH"], "/tmp/openclaw-bench-c/openclaw.json")
        self.assertEqual(harness.command_env["OPENCLAW_STATE_DIR"], str(expected_root))
        self.assertRegex(harness.command_env["OPENCLAW_PROFILE"], r"^bench-openclaw-bench-c-[0-9a-f]{10}$")

    def test_auth_and_session_paths_use_configured_state_dir(self) -> None:
        harness = OpenClawLiveHarness(openclaw_state_dir="/tmp/openclaw-bench-a")
        expected_root = Path("/tmp/openclaw-bench-a").resolve(strict=False)

        self.assertEqual(
            harness._global_main_auth_profiles_path(),
            expected_root / "agents" / "main" / "agent" / "auth-profiles.json",
        )
        self.assertEqual(
            harness._agent_sessions_dir("agent-1"),
            expected_root / "agents" / "agent-1" / "sessions",
        )

    def test_ensure_isolated_state_seeded_copies_default_models_and_main_auth(self) -> None:
        with tempfile.TemporaryDirectory() as home_dir, tempfile.TemporaryDirectory() as target_dir:
            home_path = Path(home_dir)
            default_state_dir = home_path / ".openclaw"
            default_state_dir.mkdir(parents=True)
            (default_state_dir / "agents" / "main" / "agent").mkdir(parents=True)

            source_config = {
                "auth": {
                    "profiles": {
                        "zai:default": {"provider": "zai", "mode": "api_key"},
                    }
                },
                "models": {
                    "providers": {
                        "glm": {
                            "baseUrl": "https://example.invalid",
                            "models": [{"id": "GLM-5", "name": "GLM-5"}],
                        }
                    }
                },
                "agents": {
                    "defaults": {"maxConcurrent": 4},
                    "list": [{"id": "main"}, {"id": "legacy-agent"}],
                },
                "messages": {"ackReactionScope": "group-mentions"},
                "commands": {"native": "auto"},
            }
            (default_state_dir / "openclaw.json").write_text(json.dumps(source_config), encoding="utf-8")
            (default_state_dir / "agents" / "main" / "agent" / "auth-profiles.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "profiles": {
                            "zai:default": {"provider": "zai", "type": "api_key", "key": "zai-test-key"}
                        },
                        "lastGood": {"zai": "zai:default"},
                    }
                ),
                encoding="utf-8",
            )

            target_state_dir = Path(target_dir)
            target_config_path = target_state_dir / "openclaw.json"
            target_state_dir.mkdir(parents=True, exist_ok=True)
            target_config_path.write_text(
                json.dumps(
                    {
                        "agents": {
                            "defaults": {"maxConcurrent": 2},
                            "list": [{"id": "main"}],
                        },
                        "messages": {"ackReactionScope": "group-mentions"},
                        "commands": {"native": "auto"},
                    }
                ),
                encoding="utf-8",
            )

            harness = OpenClawLiveHarness(openclaw_state_dir=str(target_state_dir))
            harness.command_env["HOME"] = str(home_path)
            harness.command_env["OPENCLAW_HOME"] = str(home_path)

            harness._ensure_isolated_state_seeded()

            seeded_config = json.loads(target_config_path.read_text(encoding="utf-8"))
            self.assertIn("models", seeded_config)
            self.assertEqual(
                seeded_config["models"]["providers"]["glm"]["models"][0]["id"],
                "GLM-5",
            )
            self.assertEqual(seeded_config["auth"]["profiles"]["zai:default"]["provider"], "zai")
            self.assertEqual(seeded_config["agents"]["list"], [{"id": "main"}])
            self.assertEqual(seeded_config["agents"]["defaults"]["maxConcurrent"], 2)
            self.assertEqual(
                seeded_config["logging"]["file"],
                str((target_state_dir / "logs" / "openclaw.log").resolve(strict=False)),
            )

            target_auth_profiles = target_state_dir / "agents" / "main" / "agent" / "auth-profiles.json"
            self.assertTrue(target_auth_profiles.exists())
            copied_auth = json.loads(target_auth_profiles.read_text(encoding="utf-8"))
            self.assertEqual(copied_auth["profiles"]["zai:default"]["provider"], "zai")

    def test_ensure_isolated_state_seeded_adds_isolated_logging_file_when_config_is_already_complete(self) -> None:
        with tempfile.TemporaryDirectory() as target_dir:
            target_state_dir = Path(target_dir)
            target_config_path = target_state_dir / "openclaw.json"
            target_state_dir.mkdir(parents=True, exist_ok=True)
            target_config_path.write_text(
                json.dumps(
                    {
                        "auth": {"profiles": {"moonshot:default": {"provider": "moonshot", "mode": "api_key"}}},
                        "models": {"providers": {"moonshot": {"models": [{"id": "kimi-k2.6-preview"}]}}},
                        "agents": {"defaults": {}, "list": [{"id": "main"}]},
                    }
                ),
                encoding="utf-8",
            )

            harness = OpenClawLiveHarness(openclaw_state_dir=str(target_state_dir))

            harness._ensure_isolated_state_seeded()

            updated_config = json.loads(target_config_path.read_text(encoding="utf-8"))
            self.assertEqual(
                updated_config["logging"]["file"],
                str((target_state_dir / "logs" / "openclaw.log").resolve(strict=False)),
            )

    def test_ensure_isolated_state_seeded_sanitizes_stale_plugins_runtime_noise_and_cron_state(self) -> None:
        with tempfile.TemporaryDirectory() as target_dir:
            target_state_dir = Path(target_dir)
            target_config_path = target_state_dir / "openclaw.json"
            cron_runs_dir = target_state_dir / "cron" / "runs"
            cron_runs_dir.mkdir(parents=True, exist_ok=True)
            (target_state_dir / "cron" / "jobs.json").write_text('{"jobs":[{"id":"stale"}]}', encoding="utf-8")
            (cron_runs_dir / "stale.jsonl").write_text("old\n", encoding="utf-8")
            target_config_path.write_text(
                json.dumps(
                    {
                        "auth": {"profiles": {"moonshot:default": {"provider": "moonshot", "mode": "api_key"}}},
                        "models": {"providers": {"moonshot": {"models": [{"id": "kimi-k2.6-preview"}]}}},
                        "agents": {
                            "defaults": {"maxConcurrent": 4},
                            "list": [{"id": "main"}, {"id": "stale-agent"}],
                        },
                        "channels": {
                            "telegram": {"enabled": True},
                            "feishu": {"enabled": True},
                        },
                        "messages": {
                            "ackReactionScope": "group-mentions",
                            "logging": {},
                        },
                        "gateway": {"tailscale": {"mode": "serve", "resetOnExit": True}},
                        "hooks": {"internal": {"entries": {"command-logger": {"enabled": True}}}},
                        "plugins": {
                            "allow": ["telegram", "openclaw-lark", "cccontrol"],
                            "entries": {
                                "telegram": {"enabled": True},
                                "openclaw-lark": {"enabled": True},
                                "cccontrol": {"enabled": True},
                            },
                            "installs": {
                                "openclaw-lark": {"installPath": "/tmp/missing-openclaw-lark"},
                                "cccontrol": {"installPath": "/tmp/cccontrol"},
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )

            harness = OpenClawLiveHarness(openclaw_state_dir=str(target_state_dir))
            harness._ensure_isolated_state_seeded()

            updated_config = json.loads(target_config_path.read_text(encoding="utf-8"))
            self.assertEqual(updated_config["agents"]["list"], [{"id": "main"}])
            self.assertEqual(updated_config["plugins"]["allow"], ["telegram", "cccontrol"])
            self.assertNotIn("openclaw-lark", updated_config["plugins"]["entries"])
            self.assertNotIn("openclaw-lark", updated_config["plugins"]["installs"])
            self.assertFalse(updated_config["channels"]["feishu"]["enabled"])
            self.assertEqual(updated_config["messages"], {"ackReactionScope": "group-mentions"})
            self.assertEqual(updated_config["gateway"]["tailscale"]["mode"], "off")
            self.assertFalse(updated_config["hooks"]["internal"]["entries"]["command-logger"]["enabled"])
            self.assertFalse((target_state_dir / "cron" / "jobs.json").exists())
            self.assertFalse((cron_runs_dir / "stale.jsonl").exists())

    def test_sync_isolated_model_runtime_pins_primary_model_and_refreshes_provider_token(self) -> None:
        with tempfile.TemporaryDirectory() as home_dir, tempfile.TemporaryDirectory() as target_dir:
            home_path = Path(home_dir)
            target_state_dir = Path(target_dir)
            target_config_path = target_state_dir / "openclaw.json"
            target_auth_path = target_state_dir / "agents" / "main" / "agent" / "auth-profiles.json"
            target_auth_path.parent.mkdir(parents=True, exist_ok=True)
            target_config_path.write_text(
                json.dumps(
                    {
                        "auth": {"profiles": {}},
                        "models": {
                            "providers": {
                                "tencent-token-plan": {
                                    "apiKey": "sk-tp-new",
                                    "models": [{"id": "hunyuan-2.0-thinking"}],
                                }
                            }
                        },
                        "agents": {
                            "defaults": {
                                "model": {
                                    "primary": "tencent-token-plan/glm-5",
                                    "fallbacks": ["kimi/kimi-code", "volcengine-plan/ark-code-latest"],
                                },
                                "models": {"tencent-token-plan/glm-5": {}},
                            },
                            "list": [{"id": "main"}],
                        },
                    }
                ),
                encoding="utf-8",
            )
            target_auth_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "profiles": {
                            "tencent-token-plan:manual": {
                                "provider": "tencent-token-plan",
                                "type": "token",
                                "token": "sk-tp-old",
                            }
                        },
                        "lastGood": {"tencent-token-plan": "tencent-token-plan:manual"},
                        "usageStats": {
                            "tencent-token-plan:manual": {
                                "cooldownUntil": 123,
                                "errorCount": 2,
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            harness = OpenClawLiveHarness(openclaw_state_dir=str(target_state_dir))
            harness.command_env["HOME"] = str(home_path)
            harness.command_env["OPENCLAW_HOME"] = str(home_path)

            harness._sync_isolated_model_runtime("tencent-token-plan/hunyuan-2.0-thinking")

            updated_config = json.loads(target_config_path.read_text(encoding="utf-8"))
            self.assertEqual(
                updated_config["agents"]["defaults"]["model"]["primary"],
                "tencent-token-plan/hunyuan-2.0-thinking",
            )
            self.assertEqual(updated_config["agents"]["defaults"]["model"]["fallbacks"], [])
            self.assertIn(
                "tencent-token-plan/hunyuan-2.0-thinking",
                updated_config["agents"]["defaults"]["models"],
            )
            self.assertEqual(
                updated_config["auth"]["profiles"]["tencent-token-plan:manual"],
                {"provider": "tencent-token-plan", "mode": "token"},
            )

            updated_auth = json.loads(target_auth_path.read_text(encoding="utf-8"))
            self.assertEqual(
                updated_auth["profiles"]["tencent-token-plan:manual"]["token"],
                "sk-tp-new",
            )
            self.assertNotIn("usageStats", updated_auth)

    def test_sync_isolated_model_runtime_updates_zai_auth_profile_for_glm_alias(self) -> None:
        with tempfile.TemporaryDirectory() as home_dir, tempfile.TemporaryDirectory() as target_dir:
            home_path = Path(home_dir)
            target_state_dir = Path(target_dir)
            target_config_path = target_state_dir / "openclaw.json"
            target_auth_path = target_state_dir / "agents" / "main" / "agent" / "auth-profiles.json"
            target_auth_path.parent.mkdir(parents=True, exist_ok=True)
            target_config_path.write_text(
                json.dumps(
                    {
                        "auth": {"profiles": {}},
                        "models": {
                            "providers": {
                                "glm": {
                                    "apiKey": "glm-new-key",
                                    "models": [{"id": "GLM-5"}],
                                }
                            }
                        },
                        "agents": {
                            "defaults": {
                                "model": {"primary": "glm/GLM-4.7", "fallbacks": ["openai/gpt-4o"]},
                                "models": {},
                            },
                            "list": [{"id": "main"}],
                        },
                    }
                ),
                encoding="utf-8",
            )
            target_auth_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "profiles": {
                            "zai:default": {
                                "provider": "zai",
                                "type": "api_key",
                                "key": "glm-old-key",
                            }
                        },
                        "lastGood": {"zai": "zai:default"},
                    }
                ),
                encoding="utf-8",
            )

            harness = OpenClawLiveHarness(openclaw_state_dir=str(target_state_dir))
            harness.command_env["HOME"] = str(home_path)
            harness.command_env["OPENCLAW_HOME"] = str(home_path)

            harness._sync_isolated_model_runtime("glm/GLM-5")

            updated_config = json.loads(target_config_path.read_text(encoding="utf-8"))
            self.assertEqual(updated_config["agents"]["defaults"]["model"]["primary"], "glm/GLM-5")
            self.assertEqual(updated_config["agents"]["defaults"]["model"]["fallbacks"], [])
            self.assertEqual(
                updated_config["auth"]["profiles"]["zai:default"],
                {"provider": "zai", "mode": "api_key"},
            )

            updated_auth = json.loads(target_auth_path.read_text(encoding="utf-8"))
            self.assertEqual(updated_auth["profiles"]["zai:default"]["provider"], "zai")
            self.assertEqual(updated_auth["profiles"]["zai:default"]["key"], "glm-new-key")

    def test_sync_isolated_model_runtime_resolves_env_named_api_key_before_writing_auth_profile(self) -> None:
        with tempfile.TemporaryDirectory() as home_dir, tempfile.TemporaryDirectory() as target_dir:
            home_path = Path(home_dir)
            target_state_dir = Path(target_dir)
            target_config_path = target_state_dir / "openclaw.json"
            target_auth_path = target_state_dir / "agents" / "main" / "agent" / "auth-profiles.json"
            target_auth_path.parent.mkdir(parents=True, exist_ok=True)
            target_config_path.write_text(
                json.dumps(
                    {
                        "auth": {"profiles": {}},
                        "models": {
                            "providers": {
                                "deepseek": {
                                    "apiKey": "DEEPSEEK_API_KEY",
                                    "models": [{"id": "deepseek-v4-pro"}],
                                }
                            }
                        },
                        "agents": {
                            "defaults": {
                                "model": {"primary": "deepseek/deepseek-chat", "fallbacks": []},
                                "models": {},
                            },
                            "list": [{"id": "main"}],
                        },
                    }
                ),
                encoding="utf-8",
            )
            target_auth_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "profiles": {},
                        "lastGood": {},
                    }
                ),
                encoding="utf-8",
            )

            harness = OpenClawLiveHarness(openclaw_state_dir=str(target_state_dir))
            harness.command_env["HOME"] = str(home_path)
            harness.command_env["OPENCLAW_HOME"] = str(home_path)
            harness.command_env["DEEPSEEK_API_KEY"] = "sk-deepseek-live"

            harness._sync_isolated_model_runtime("deepseek/deepseek-v4-pro")

            updated_auth = json.loads(target_auth_path.read_text(encoding="utf-8"))
            self.assertEqual(updated_auth["profiles"]["deepseek:manual"]["provider"], "deepseek")
            self.assertEqual(updated_auth["profiles"]["deepseek:manual"]["key"], "sk-deepseek-live")

    def test_sync_isolated_model_runtime_bootstraps_missing_deepseek_provider_for_flash(self) -> None:
        with tempfile.TemporaryDirectory() as home_dir, tempfile.TemporaryDirectory() as target_dir:
            home_path = Path(home_dir)
            target_state_dir = Path(target_dir)
            target_config_path = target_state_dir / "openclaw.json"
            target_auth_path = target_state_dir / "agents" / "main" / "agent" / "auth-profiles.json"
            target_auth_path.parent.mkdir(parents=True, exist_ok=True)
            target_config_path.write_text(
                json.dumps(
                    {
                        "auth": {"profiles": {}},
                        "models": {
                            "providers": {
                                "glm": {
                                    "apiKey": "glm-test-key",
                                    "models": [{"id": "GLM-5"}],
                                }
                            }
                        },
                        "agents": {
                            "defaults": {
                                "model": {"primary": "glm/GLM-5", "fallbacks": []},
                                "models": {},
                            },
                            "list": [{"id": "main"}],
                        },
                    }
                ),
                encoding="utf-8",
            )
            target_auth_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "profiles": {},
                        "lastGood": {},
                    }
                ),
                encoding="utf-8",
            )

            harness = OpenClawLiveHarness(openclaw_state_dir=str(target_state_dir))
            harness.command_env["HOME"] = str(home_path)
            harness.command_env["OPENCLAW_HOME"] = str(home_path)
            harness.command_env["DEEPSEEK_API_KEY"] = "sk-deepseek-live"

            harness._sync_isolated_model_runtime("deepseek/deepseek-v4-flash")

            updated_config = json.loads(target_config_path.read_text(encoding="utf-8"))
            deepseek_provider = updated_config["models"]["providers"]["deepseek"]
            self.assertEqual(deepseek_provider["baseUrl"], "https://api.deepseek.com")
            self.assertEqual(deepseek_provider["apiKey"], "DEEPSEEK_API_KEY")
            self.assertEqual(
                [model["id"] for model in deepseek_provider["models"]],
                ["deepseek-v4-pro", "deepseek-v4-flash"],
            )

            updated_auth = json.loads(target_auth_path.read_text(encoding="utf-8"))
            self.assertEqual(updated_auth["profiles"]["deepseek:manual"]["provider"], "deepseek")
            self.assertEqual(updated_auth["profiles"]["deepseek:manual"]["key"], "sk-deepseek-live")

    def test_sync_isolated_model_runtime_seeds_codex_cli_backend(self) -> None:
        with tempfile.TemporaryDirectory() as home_dir, tempfile.TemporaryDirectory() as target_dir:
            home_path = Path(home_dir)
            target_state_dir = Path(target_dir)
            target_config_path = target_state_dir / "openclaw.json"
            target_config_path.write_text(
                json.dumps(
                    {
                        "agents": {
                            "defaults": {
                                "model": {"primary": "codex-cli/gpt-5.5", "fallbacks": []},
                                "models": {"codex-cli/gpt-5.5": {}},
                            },
                            "list": [{"id": "main"}],
                        },
                        "models": {"providers": {}},
                    }
                ),
                encoding="utf-8",
            )

            harness = OpenClawLiveHarness(openclaw_state_dir=str(target_state_dir))
            harness.command_env["HOME"] = str(home_path)
            harness.command_env["OPENCLAW_HOME"] = str(home_path)
            harness.command_env["PATH"] = "/tmp/codex-bin"

            with mock.patch("harness.live_harness.shutil.which", return_value="/tmp/codex-bin/codex"):
                harness._sync_isolated_model_runtime("codex-cli/gpt-5.4")

            updated_config = json.loads(target_config_path.read_text(encoding="utf-8"))
            defaults = updated_config["agents"]["defaults"]
            self.assertEqual(defaults["model"], {"primary": "codex-cli/gpt-5.4", "fallbacks": []})
            self.assertIn("codex-cli/gpt-5.4", defaults["models"])
            backend = defaults["cliBackends"]["codex-cli"]
            self.assertEqual(backend["command"], "/tmp/codex-bin/codex")
            self.assertEqual(backend["args"][:2], ["exec", "--json"])
            self.assertIn('model_reasoning_effort="xhigh"', backend["args"])
            self.assertEqual(backend["output"], "jsonl")
            self.assertEqual(backend["modelArg"], "--model")
            self.assertEqual(backend["sessionMode"], "none")
            self.assertEqual(backend["sessionIdFields"], ["thread_id"])
            self.assertEqual(backend["env"]["CODEX_HOME"], str(home_path / ".codex"))
            self.assertNotIn("resumeArgs", backend)

    def test_sync_isolated_model_runtime_seeds_qoder_cli_backend(self) -> None:
        with tempfile.TemporaryDirectory() as target_dir:
            target_state_dir = Path(target_dir)
            target_config_path = target_state_dir / "openclaw.json"
            target_config_path.write_text(
                json.dumps(
                    {
                        "agents": {
                            "defaults": {
                                "model": {"primary": "glm/GLM-5", "fallbacks": []},
                                "models": {"glm/GLM-5": {}},
                            },
                            "list": [{"id": "main"}],
                        },
                        "models": {"providers": {}},
                    }
                ),
                encoding="utf-8",
            )

            harness = OpenClawLiveHarness(openclaw_state_dir=str(target_state_dir))
            harness.command_env["PATH"] = "/tmp/qoder-bin"

            with mock.patch("harness.live_harness.shutil.which", return_value="/tmp/qoder-bin/qoderclicn"):
                harness._sync_isolated_model_runtime("qoder-cli/Qwen3.7-Max")

            updated_config = json.loads(target_config_path.read_text(encoding="utf-8"))
            defaults = updated_config["agents"]["defaults"]
            self.assertEqual(defaults["model"], {"primary": "qoder-cli/Qwen3.7-Max", "fallbacks": []})
            self.assertIn("qoder-cli/Qwen3.7-Max", defaults["models"])
            backend = defaults["cliBackends"]["qoder-cli"]
            self.assertEqual(backend["command"], "/tmp/qoder-bin/qoderclicn")
            self.assertEqual(backend["args"], ["-p", "-o", "json", "--permission-mode", "bypass_permissions"])
            self.assertEqual(backend["output"], "json")
            self.assertEqual(backend["modelArg"], "--model")
            self.assertEqual(backend["modelAliases"]["qwen3.7-max"], "Qwen3.7-Max")
            self.assertEqual(backend["sessionMode"], "none")
            self.assertEqual(backend["sessionIdFields"], ["session_id", "uuid"])
            self.assertFalse(backend["serialize"])
            self.assertEqual(
                backend["reliability"]["watchdog"]["fresh"]["noOutputTimeoutRatio"],
                0.95,
            )

    def test_sync_isolated_model_runtime_seeds_agy_backend(self) -> None:
        with tempfile.TemporaryDirectory() as target_dir:
            target_state_dir = Path(target_dir)
            target_config_path = target_state_dir / "openclaw.json"
            target_config_path.write_text(
                json.dumps(
                    {
                        "agents": {
                            "defaults": {
                                "model": {"primary": "glm/GLM-5", "fallbacks": []},
                                "models": {"glm/GLM-5": {}},
                            },
                            "list": [{"id": "main"}],
                        },
                        "models": {"providers": {}},
                    }
                ),
                encoding="utf-8",
            )

            harness = OpenClawLiveHarness(openclaw_state_dir=str(target_state_dir))
            harness.command_env["PATH"] = "/tmp/agy-bin"

            with mock.patch("harness.live_harness.shutil.which", return_value="/tmp/agy-bin/agy"):
                harness._sync_isolated_model_runtime("agy/Gemini 3.1 Pro (High)")

            updated_config = json.loads(target_config_path.read_text(encoding="utf-8"))
            defaults = updated_config["agents"]["defaults"]
            self.assertEqual(
                defaults["model"],
                {"primary": "agy/Gemini 3.1 Pro (High)", "fallbacks": []},
            )
            self.assertIn("agy/Gemini 3.1 Pro (High)", defaults["models"])
            backend = defaults["cliBackends"]["agy"]
            self.assertEqual(backend["command"], "/tmp/agy-bin/agy")
            self.assertEqual(
                backend["args"],
                ["--dangerously-skip-permissions", "--print-timeout", "40m", "--print"],
            )
            self.assertEqual(backend["output"], "text")
            self.assertNotIn("modelArg", backend)
            self.assertEqual(backend["sessionMode"], "none")
            self.assertEqual(
                backend["sessionIdFields"],
                ["conversation", "conversation_id", "conversationId"],
            )
            self.assertFalse(backend["serialize"])
            self.assertEqual(
                backend["reliability"]["watchdog"]["fresh"]["noOutputTimeoutRatio"],
                0.95,
            )

    def test_sync_isolated_agent_runtime_pins_agent_model_and_disables_fallbacks(self) -> None:
        with tempfile.TemporaryDirectory() as target_dir:
            target_state_dir = Path(target_dir)
            target_config_path = target_state_dir / "openclaw.json"
            target_config_path.write_text(
                json.dumps(
                    {
                        "agents": {
                            "defaults": {
                                "model": {
                                    "primary": "tencent-token-plan/glm-5",
                                    "fallbacks": ["kimi/kimi-code"],
                                }
                            },
                            "list": [
                                {"id": "main"},
                                {
                                    "id": "agent-1",
                                    "name": "agent-1",
                                    "workspace": "/tmp/workspace",
                                    "model": "tencent-token-plan/hunyuan-2.0-thinking",
                                },
                                {
                                    "id": "agent-2",
                                    "model": {
                                        "primary": "glm/GLM-5",
                                        "fallbacks": ["openai/gpt-4.1"],
                                    },
                                },
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )

            harness = OpenClawLiveHarness(openclaw_state_dir=str(target_state_dir))

            harness._sync_isolated_agent_runtime("agent-1", "tencent-token-plan/hunyuan-2.0-thinking")

            updated_config = json.loads(target_config_path.read_text(encoding="utf-8"))
            self.assertEqual(
                updated_config["agents"]["list"][1]["model"],
                {
                    "primary": "tencent-token-plan/hunyuan-2.0-thinking",
                    "fallbacks": [],
                },
            )
            self.assertEqual(
                updated_config["agents"]["list"][2]["model"],
                {
                    "primary": "glm/GLM-5",
                    "fallbacks": ["openai/gpt-4.1"],
                },
            )

    def test_ensure_agent_ready_retries_until_agent_appears(self) -> None:
        harness = OpenClawLiveHarness()
        first = mock.Mock(returncode=0, stdout='[]', stderr='')
        second = mock.Mock(returncode=0, stdout='[{"id":"ocb6-glm-glm-5-abc123"}]', stderr='')
        with mock.patch("harness.live_harness.subprocess.run", side_effect=[first, second]):
            state = harness._ensure_agent_ready("ocb6-glm-glm-5-abc123", max_wait_seconds=1.0)

        self.assertEqual(state["ensure_ready_phase"], "ready")
        self.assertEqual(state["agents_list_count"], 1)

    def test_ensure_agent_ready_matches_normalized_list_id_fields(self) -> None:
        harness = OpenClawLiveHarness()
        completed = mock.Mock(returncode=0, stdout='[{"agentId":"ocb6.glm.glm.5.abc123"}]', stderr='')
        with mock.patch("harness.live_harness.subprocess.run", return_value=completed):
            state = harness._ensure_agent_ready("ocb6-glm-glm-5-abc123", max_wait_seconds=0)

        self.assertEqual(state["ensure_ready_phase"], "ready")
        self.assertIn("ocb6.glm.glm.5.abc123", state["agents_list_ids_sample"])

    def test_ensure_agent_ready_requires_registry_even_when_sessions_dir_exists(self) -> None:
        harness = OpenClawLiveHarness()
        completed = mock.Mock(returncode=0, stdout='[]', stderr='')
        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_dir = Path(tmpdir) / "agents" / "ocb6-glm-glm-5-abc123" / "sessions"
            sessions_dir.mkdir(parents=True)
            with (
                mock.patch("harness.live_harness.subprocess.run", return_value=completed),
                mock.patch.object(harness, "_agent_sessions_dir", return_value=sessions_dir),
            ):
                with self.assertRaisesRegex(RuntimeError, "OpenClaw agent not ready"):
                    harness._ensure_agent_ready("ocb6-glm-glm-5-abc123", max_wait_seconds=0)

    def test_ensure_agent_ready_raises_when_registry_and_state_are_missing(self) -> None:
        harness = OpenClawLiveHarness()
        completed = mock.Mock(returncode=0, stdout='[]', stderr='')
        missing_dir = Path("/tmp/nonexistent-agent-sessions")
        with (
            mock.patch("harness.live_harness.subprocess.run", return_value=completed),
            mock.patch.object(harness, "_agent_sessions_dir", return_value=missing_dir),
        ):
            with self.assertRaisesRegex(RuntimeError, "OpenClaw agent not ready"):
                harness._ensure_agent_ready("ocb6-glm-glm-5-abc123", max_wait_seconds=0)

        harness = OpenClawLiveHarness()

        self.assertEqual(harness._auth_profile_providers_for_model("glm/GLM-5"), {"zai"})
        self.assertEqual(harness._auth_profile_providers_for_model("minimax/MiniMax-M2.7"), {"minimax"})
        self.assertEqual(harness._auth_profile_providers_for_model("codex-cli/gpt-5.5"), set())
        self.assertEqual(harness._auth_profile_providers_for_model("qoder-cli/Qwen3.7-Max"), set())
        self.assertEqual(harness._auth_profile_providers_for_model("agy/Gemini 3.1 Pro (High)"), set())

    def test_create_agent_copies_minimax_auth_profiles(self) -> None:
        harness = OpenClawLiveHarness()
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            completed = mock.Mock(returncode=0, stdout="", stderr="")
            copy_result = mock.Mock(reason="copied")
            with (
                mock.patch("harness.live_harness.subprocess.run", return_value=completed),
                mock.patch.object(harness, "_copy_auth_profiles", return_value=copy_result) as copy_auth,
                mock.patch.object(harness, "_sync_isolated_agent_runtime") as sync_agent_runtime,
            ):
                result = harness._create_agent("agent-1", "minimax/MiniMax-M2.7", workspace)

        self.assertIs(result, copy_result)
        sync_agent_runtime.assert_called_once_with("agent-1", "minimax/MiniMax-M2.7")
        copy_auth.assert_called_once_with("agent-1", providers={"minimax"})

    def test_create_agent_strips_openclaw_log_pollution_when_add_fails(self) -> None:
        harness = OpenClawLiveHarness()
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            completed = mock.Mock(
                returncode=1,
                stdout="",
                stderr=(
                    "[openclaw] log file size cap reached; suppressing writes file=/tmp/openclaw/openclaw-2026-04-14.log maxFileBytes=5242880\n"
                    "agent add failed"
                ),
            )
            with mock.patch("harness.live_harness.subprocess.run", side_effect=[mock.Mock(returncode=0, stdout="", stderr=""), completed]):
                with self.assertRaisesRegex(RuntimeError, "agent add failed"):
                    harness._create_agent("agent-1", "minimax/MiniMax-M2.7", workspace)

    def test_resolve_transcript_path_uses_sessions_metadata_when_requested_id_is_not_real_session_id(self) -> None:
        harness = OpenClawLiveHarness()
        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_dir = Path(tmpdir)
            (sessions_dir / "sessions.json").write_text(
                json.dumps(
                    {
                        "agent:test:main": {
                            "sessionId": "real-session-id",
                            "updatedAt": 200,
                        }
                    }
                ),
                encoding="utf-8",
            )
            transcript_path = sessions_dir / "real-session-id.jsonl"
            transcript_path.write_text('{"type":"message"}\n', encoding="utf-8")

            resolved = harness._resolve_transcript_path(sessions_dir, "requested-session-id")

        self.assertEqual(resolved, transcript_path)

    def test_resolve_transcript_path_falls_back_to_latest_transcript_file(self) -> None:
        harness = OpenClawLiveHarness()
        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_dir = Path(tmpdir)
            older = sessions_dir / "older.jsonl"
            newer = sessions_dir / "newer.jsonl"
            older.write_text('{"type":"message"}\n', encoding="utf-8")
            newer.write_text('{"type":"message"}\n', encoding="utf-8")
            older.touch()
            newer.touch()

            resolved = harness._resolve_transcript_path(sessions_dir, "missing-session-id")

        self.assertEqual(resolved, newer)

    def test_wait_and_load_transcript_returns_early_without_session_artifacts(self) -> None:
        harness = OpenClawLiveHarness()
        with (
            mock.patch.object(harness, "_session_artifacts_ready", return_value=False),
            mock.patch.object(harness, "_load_transcript") as load_transcript,
        ):
            transcript = harness._wait_and_load_transcript(
                "agent-id",
                "session-id",
                max_wait_seconds=12,
                startup_grace_seconds=0,
            )

        self.assertEqual(transcript, [])
        load_transcript.assert_not_called()

    def test_execute_turn_skips_transcript_wait_when_agent_creation_fails(self) -> None:
        harness = OpenClawLiveHarness()
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            with (
                mock.patch.object(harness, "_create_agent", side_effect=RuntimeError("agent add failed")),
                mock.patch.object(harness, "_wait_and_load_transcript") as wait_for_transcript,
            ):
                result = harness.execute_turn(
                    model="mock/default",
                    prompt="hello",
                    workspace_path=workspace,
                    timeout=1,
                )

        self.assertEqual(result.status, "error")
        self.assertEqual(result.error_detail, "agent add failed")
        wait_for_transcript.assert_not_called()

    def test_preflight_retries_after_timeout_then_succeeds(self) -> None:
        harness = OpenClawLiveHarness()
        completed = mock.Mock(returncode=0, stdout='[]', stderr='')
        with mock.patch(
            "harness.live_harness.subprocess.run",
            side_effect=[subprocess.TimeoutExpired(["openclaw", "agents", "list"], 45), completed],
        ):
            result = harness.preflight(timeout=45, max_attempts=2)

        self.assertTrue(result.ok)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("attempt=1 timeout_s=45", result.error_detail)

    def test_preflight_seeds_isolated_state_before_agents_list(self) -> None:
        harness = OpenClawLiveHarness(openclaw_state_dir="/tmp/openclaw-bench-a")
        completed = mock.Mock(returncode=0, stdout='[]', stderr='')
        with (
            mock.patch.object(harness, "_ensure_isolated_state_seeded") as ensure_seed,
            mock.patch("harness.live_harness.subprocess.run", return_value=completed),
        ):
            result = harness.preflight(timeout=45, max_attempts=1)

        self.assertTrue(result.ok)
        ensure_seed.assert_called_once()

    def test_preflight_reports_timeout_after_all_attempts(self) -> None:
        harness = OpenClawLiveHarness()
        with mock.patch(
            "harness.live_harness.subprocess.run",
            side_effect=[
                subprocess.TimeoutExpired(["openclaw", "agents", "list"], 45),
                subprocess.TimeoutExpired(["openclaw", "agents", "list"], 45),
            ],
        ):
            result = harness.preflight(timeout=45, max_attempts=2)

        self.assertFalse(result.ok)
        self.assertEqual(result.exit_code, -1)
        self.assertIn("OpenClaw live preflight timed out", result.error_detail)
        self.assertIn("attempt=2 timeout_s=45", result.error_detail)

    def test_preflight_bootstraps_gateway_after_agents_list_timeout(self) -> None:
        harness = OpenClawLiveHarness(openclaw_state_dir="/tmp/openclaw-bench-a", openclaw_gateway_port=19021)
        completed = mock.Mock(returncode=0, stdout="[]", stderr="")

        with (
            mock.patch(
                "harness.live_harness.subprocess.run",
                side_effect=[subprocess.TimeoutExpired(["openclaw", "agents", "list"], 45), completed],
            ),
            mock.patch.object(harness, "_ensure_gateway_ready", return_value=True) as ensure_gateway,
        ):
            result = harness.preflight(timeout=45, max_attempts=1)

        self.assertTrue(result.ok)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("gateway_bootstrap_after_timeout=ok", result.error_detail)
        self.assertIn("post_timeout_bootstrap_exit_code=0", result.error_detail)
        ensure_gateway.assert_called_once()

    def test_preflight_surfaces_cli_runtime_error(self) -> None:
        harness = OpenClawLiveHarness()
        completed = mock.Mock(returncode=1, stdout="", stderr="missing gaxios")
        with mock.patch("harness.live_harness.subprocess.run", return_value=completed):
            result = harness.preflight(timeout=1, max_attempts=1)

        self.assertFalse(result.ok)
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.error_detail, "missing gaxios")

    def test_preflight_bootstraps_gateway_for_isolated_instance_then_succeeds(self) -> None:
        harness = OpenClawLiveHarness(openclaw_state_dir="/tmp/openclaw-bench-a", openclaw_gateway_port=19021)
        failed = mock.Mock(
            returncode=1,
            stdout="",
            stderr="Failed to start CLI: gateway closed (1006 abnormal closure)",
        )
        succeeded = mock.Mock(returncode=0, stdout="[]", stderr="")
        with (
            mock.patch("harness.live_harness.subprocess.run", side_effect=[failed, succeeded]),
            mock.patch.object(harness, "_ensure_gateway_ready", return_value=True) as ensure_gateway,
        ):
            result = harness.preflight(timeout=5, max_attempts=1)

        self.assertTrue(result.ok)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("gateway_bootstrap=ok", result.error_detail)
        ensure_gateway.assert_called_once()

    def test_ensure_gateway_ready_tolerates_agents_list_timeout_during_startup(self) -> None:
        harness = OpenClawLiveHarness(openclaw_state_dir="/tmp/openclaw-bench-a", openclaw_gateway_port=19021)
        proc = mock.Mock()
        proc.poll.return_value = None
        completed = mock.Mock(returncode=0, stdout="[]", stderr="")

        with (
            mock.patch("harness.live_harness.subprocess.Popen", return_value=proc),
            mock.patch(
                "harness.live_harness.subprocess.run",
                side_effect=[subprocess.TimeoutExpired(["openclaw", "agents", "list"], 5), completed],
            ),
            mock.patch("harness.live_harness.time.sleep"),
        ):
            self.assertTrue(harness._ensure_gateway_ready(startup_timeout=10))

    def test_close_terminates_bootstrapped_gateway_process(self) -> None:
        harness = OpenClawLiveHarness(openclaw_state_dir="/tmp/openclaw-bench-a", openclaw_gateway_port=19021)
        proc = mock.Mock()
        proc.poll.return_value = None
        harness._gateway_process = proc

        with mock.patch.object(harness, "_kill_process_group") as kill_process_group:
            harness.close()

        kill_process_group.assert_called_once_with(proc)
        self.assertIsNone(harness._gateway_process)

    def test_communicate_with_heartbeat_emits_progress_message(self) -> None:
        messages: list[str] = []
        harness = OpenClawLiveHarness(progress_callback=messages.append, progress_interval_seconds=1)
        proc = mock.Mock()
        proc.args = ["openclaw", "agent"]
        proc.communicate.side_effect = [
            subprocess.TimeoutExpired(proc.args, 1),
            ('{"result": {}}', ""),
        ]

        stdout, stderr = harness._communicate_with_heartbeat(proc, timeout=2, agent_id="agent-1")

        self.assertEqual(stdout, '{"result": {}}')
        self.assertEqual(stderr, "")
        self.assertTrue(any("live-heartbeat agent=agent-1" in message for message in messages))

    def test_execute_turn_creates_fresh_agent_in_pooled_worker_and_copies_outputs_back(self) -> None:
        harness = OpenClawLiveHarness(agent_pool_size=1, cleanup_agents=True)
        completed_stdout = '{"result": {"meta": {"agentMeta": {"sessionId": "real-session-id"}}}}'
        proc = mock.Mock()
        proc.returncode = 0
        transcript = [
            {
                "type": "message",
                "message": {
                    "role": "assistant",
                    "content": [{"type": "text", "text": "done"}],
                    "usage": {"input": 10, "output": 5, "totalTokens": 15},
                },
            }
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            original_workspace = Path(tmpdir) / "original"
            pool_workspace = Path(tmpdir) / "pool"
            original_workspace.mkdir()
            pool_workspace.mkdir()
            (original_workspace / "seed.txt").write_text("seed\n", encoding="utf-8")
            slot = AgentPoolSlot(
                slot_id="worker-1",
                workspace_path=pool_workspace,
            )
            harness._agent_pool_model = "codex-cli/gpt-5.4"
            harness._agent_pool_slots = [slot]
            harness._agent_pool_queue.put(slot)

            def complete_turn(*_args: object, **_kwargs: object) -> tuple[str, str]:
                (pool_workspace / "answer.txt").write_text("done\n", encoding="utf-8")
                return completed_stdout, ""

            def delete_agent_after_copyback(_agent_id: str) -> None:
                self.assertTrue((original_workspace / "answer.txt").exists())
                shutil.rmtree(pool_workspace)

            with (
                mock.patch.object(
                    harness,
                    "_create_agent",
                    return_value=AuthProfileCopyResult(source_exists=True, requested_providers={"codex"}),
                ) as create_agent,
                mock.patch.object(harness, "_ensure_agent_ready", return_value={"ensure_ready_phase": "ready"}),
                mock.patch.object(harness, "_delete_agent", side_effect=delete_agent_after_copyback) as delete_agent,
                mock.patch("harness.live_harness.subprocess.Popen", return_value=proc) as popen,
                mock.patch.object(harness, "_communicate_with_heartbeat", side_effect=complete_turn),
                mock.patch.object(harness, "_wait_and_load_transcript", return_value=transcript),
            ):
                result = harness.execute_turn(
                    model="codex-cli/gpt-5.4",
                    prompt="hello",
                    workspace_path=original_workspace,
                    timeout=1,
                    expected_workspace_files=["seed.txt"],
                )
                output_text = (original_workspace / "answer.txt").read_text(encoding="utf-8")

            create_agent.assert_called_once()
            created_agent_id, created_model, created_workspace = create_agent.call_args.args
            self.assertEqual(result.status, "success")
            self.assertEqual(result.agent_id, created_agent_id)
            self.assertEqual(created_model, "codex-cli/gpt-5.4")
            self.assertEqual(created_workspace, pool_workspace)
            self.assertRegex(result.agent_id, r"^ocb6-codex-cli-gpt-5-4-[0-9a-f]{12}$")
            delete_agent.assert_called_once_with(result.agent_id)
            self.assertEqual(popen.call_args.kwargs["cwd"], str(pool_workspace))
            command = popen.call_args.args[0]
            self.assertIn(result.agent_id, command)
            self.assertIn("--session-id", command)
            self.assertEqual(output_text, "done\n")

    def test_execute_turn_converts_empty_success_trace_to_error(self) -> None:
        harness = OpenClawLiveHarness()
        completed_stdout = '{"result": {"meta": {"agentMeta": {"sessionId": "real-session-id"}}}}'
        proc = mock.Mock()
        proc.returncode = 0
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            with (
                mock.patch.object(
                    harness,
                    "_create_agent",
                    return_value=mock.Mock(requested_providers={"zai"}, to_dict=lambda: {"reason": "copied"}),
                ),
                mock.patch.object(harness, "_ensure_agent_ready"),
                mock.patch("harness.live_harness.subprocess.Popen", return_value=proc),
                mock.patch.object(harness, "_communicate_with_heartbeat", return_value=(completed_stdout, "")),
                mock.patch.object(harness, "_wait_and_load_transcript", return_value=[]),
            ):
                result = harness.execute_turn(
                    model="glm/GLM-5",
                    prompt="hello",
                    workspace_path=workspace,
                    timeout=1,
                )

        self.assertEqual(result.status, "error")
        self.assertEqual(result.error_detail, "empty live transcript/tool trace")
        self.assertNotEqual(result.exit_code, 0)

    def test_execute_turn_accepts_stderr_payload_when_transcript_is_missing(self) -> None:
        harness = OpenClawLiveHarness()
        completed_stderr = """
Gateway agent failed; falling back to embedded
{
  "payloads": [
    {"text": "done", "mediaUrl": null}
  ],
  "meta": {
    "durationMs": 1234,
    "agentMeta": {
      "sessionId": "real-session-id",
      "usage": {"input": 10, "output": 5, "cacheRead": 3}
    }
  }
}
"""
        proc = mock.Mock()
        proc.returncode = 0
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            with (
                mock.patch.object(
                    harness,
                    "_create_agent",
                    return_value=mock.Mock(requested_providers=set(), to_dict=lambda: {"reason": "copied"}),
                ),
                mock.patch.object(harness, "_ensure_agent_ready", return_value={"ensure_ready_phase": "ready"}),
                mock.patch("harness.live_harness.subprocess.Popen", return_value=proc),
                mock.patch.object(harness, "_communicate_with_heartbeat", return_value=("", completed_stderr)),
                mock.patch.object(harness, "_wait_and_load_transcript", return_value=[]),
            ):
                result = harness.execute_turn(
                    model="codex-cli/gpt-5.5",
                    prompt="hello",
                    workspace_path=workspace,
                    timeout=1,
                )

        self.assertEqual(result.status, "success")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.session_id, "real-session-id")
        self.assertEqual(result.trace["events"], [{"type": "assistant_message", "text": "done", "seq": 0}])
        self.assertEqual(result.trace["metrics"]["input_tokens"], 10)
        self.assertEqual(result.trace["metrics"]["output_tokens"], 5)
        self.assertEqual(result.trace["metrics"]["cache_read_tokens"], 3)

        harness = OpenClawLiveHarness()
        completed_stdout = '{"result": {"meta": {"agentMeta": {"sessionId": "real-session-id"}}}}'
        proc = mock.Mock()
        proc.returncode = 0
        transcript = [
            {
                "type": "message",
                "message": {
                    "role": "assistant",
                    "content": [],
                    "stopReason": "error",
                    "errorMessage": "No API key for provider: glm",
                    "usage": {"input": 0, "output": 0, "totalTokens": 0},
                },
            }
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            with (
                mock.patch.object(harness, "_create_agent"),
                mock.patch.object(harness, "_ensure_agent_ready"),
                mock.patch("harness.live_harness.subprocess.Popen", return_value=proc),
                mock.patch.object(harness, "_communicate_with_heartbeat", return_value=(completed_stdout, "")),
                mock.patch.object(harness, "_wait_and_load_transcript", return_value=transcript),
            ):
                result = harness.execute_turn(
                    model="glm/GLM-5",
                    prompt="hello",
                    workspace_path=workspace,
                    timeout=1,
                )

        self.assertEqual(result.status, "error")
        self.assertNotEqual(result.exit_code, 0)
        self.assertEqual(result.error_detail, "No API key for provider: glm")

    def test_execute_turn_recreates_agent_once_on_unknown_agent_id(self) -> None:
        harness = OpenClawLiveHarness()
        proc_first = mock.Mock()
        proc_first.returncode = 1
        proc_second = mock.Mock()
        proc_second.returncode = 0
        payload_success = '{"result": {"meta": {"agentMeta": {"sessionId": "real-session-id"}}, "payloads": [{"text": "done", "usage": {"input": 10, "output": 5, "total": 15}}]}}'
        transcript = [
            {
                "type": "message",
                "message": {
                    "role": "assistant",
                    "content": [{"type": "text", "text": "done"}],
                    "usage": {"input": 10, "output": 5, "totalTokens": 15},
                },
            }
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            with (
                mock.patch.object(harness, "_create_agent") as create_agent,
                mock.patch.object(harness, "_ensure_agent_ready"),
                mock.patch("harness.live_harness.subprocess.Popen", side_effect=[proc_first, proc_second]),
                mock.patch.object(harness, "_communicate_with_heartbeat", side_effect=[('{"error":"Unknown agent id \\\"agent-1\\\""}', "Unknown agent id \"agent-1\""), (payload_success, "")]),
                mock.patch.object(harness, "_wait_and_load_transcript", return_value=transcript),
            ):
                result = harness.execute_turn(
                    model="glm/GLM-5",
                    prompt="hello",
                    workspace_path=workspace,
                    timeout=1,
                )

        self.assertEqual(create_agent.call_count, 2)
        self.assertEqual(result.status, "success")
        self.assertEqual(result.exit_code, 0)

    def test_execute_turn_repairs_missing_workspace_files_after_agent_create(self) -> None:
        harness = OpenClawLiveHarness()
        completed_stdout = '{"result": {"meta": {"agentMeta": {"sessionId": "real-session-id"}}}}'
        proc = mock.Mock()
        proc.returncode = 0
        transcript = [
            {
                "type": "message",
                "message": {
                    "role": "assistant",
                    "content": [{"type": "text", "text": "done"}],
                    "usage": {"input": 10, "output": 5, "totalTokens": 15},
                },
            }
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            seeded = workspace / "seed.txt"
            seeded.write_text("seeded\n", encoding="utf-8")

            def create_agent(*_args: object, **_kwargs: object) -> mock.Mock:
                seeded.unlink()
                return mock.Mock(
                    requested_providers={"zai"},
                    to_dict=lambda: {"reason": "copied"},
                )

            def repair_workspace(target_workspace: Path) -> None:
                (target_workspace / "seed.txt").write_text("seeded\n", encoding="utf-8")

            with (
                mock.patch.object(harness, "_create_agent", side_effect=create_agent),
                mock.patch.object(harness, "_ensure_agent_ready", return_value={"ensure_ready_phase": "ready"}),
                mock.patch("harness.live_harness.subprocess.Popen", return_value=proc),
                mock.patch.object(harness, "_communicate_with_heartbeat", return_value=(completed_stdout, "")),
                mock.patch.object(harness, "_wait_and_load_transcript", return_value=transcript),
            ):
                result = harness.execute_turn(
                    model="glm/GLM-5",
                    prompt="hello",
                    workspace_path=workspace,
                    timeout=1,
                    expected_workspace_files=["seed.txt"],
                    repair_workspace=repair_workspace,
                )
            guard = result.trace["audit_state"]["live_runtime"]["workspace_guard"]
            self.assertTrue((workspace / "seed.txt").exists())
            self.assertEqual(len(guard["repair_attempts"]), 1)
            self.assertEqual(guard["repair_attempts"][0]["missing_before_restore"], ["seed.txt"])
            self.assertEqual(guard["repair_attempts"][0]["missing_after_restore"], [])
            self.assertTrue(guard["repair_attempts"][0]["repair_applied"])

    def test_execute_turn_normalizes_benign_terminated_exit_when_trace_is_complete(self) -> None:
        harness = OpenClawLiveHarness()
        completed_stdout = '{"result": {"meta": {"agentMeta": {"sessionId": "real-session-id"}}}}'
        proc = mock.Mock()
        proc.returncode = 1
        transcript = [
            {
                "type": "message",
                "message": {
                    "role": "assistant",
                    "content": [{"type": "text", "text": "done"}],
                    "usage": {"input": 10, "output": 5, "totalTokens": 15},
                },
            }
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            with (
                mock.patch.object(
                    harness,
                    "_create_agent",
                    return_value=mock.Mock(requested_providers={"zai"}, to_dict=lambda: {"reason": "copied"}),
                ),
                mock.patch.object(harness, "_ensure_agent_ready", return_value={"ensure_ready_phase": "ready"}),
                mock.patch("harness.live_harness.subprocess.Popen", return_value=proc),
                mock.patch.object(harness, "_communicate_with_heartbeat", return_value=(completed_stdout, "terminated")),
                mock.patch.object(harness, "_wait_and_load_transcript", return_value=transcript),
            ):
                result = harness.execute_turn(
                    model="glm/GLM-5",
                    prompt="hello",
                    workspace_path=workspace,
                    timeout=1,
                )

        self.assertEqual(result.status, "success")
        self.assertEqual(result.exit_code, 0)

    def test_build_error_detail_ignores_openclaw_log_size_cap_pollution(self) -> None:
        harness = OpenClawLiveHarness()

        detail = harness._build_error_detail(
            status="error",
            exit_code=1,
            stderr="[openclaw] log file size cap reached; suppressing writes file=/tmp/openclaw/openclaw-2026-04-14.log maxFileBytes=5242880\n",
            stdout="",
            payload=None,
        )

        self.assertEqual(detail, "OpenClaw agent exited with code 1")

    def test_clean_openclaw_command_streams_preserves_real_stderr_after_pollution(self) -> None:
        harness = OpenClawLiveHarness()

        stdout, stderr = harness._clean_openclaw_command_streams(
            '{"result": {}}',
            "[openclaw] log file size cap reached; suppressing writes file=/tmp/openclaw/openclaw-2026-04-14.log maxFileBytes=5242880\nreal failure",
        )

        self.assertEqual(stdout, '{"result": {}}')
        self.assertEqual(stderr, "real failure")

    def test_run_agents_list_strips_openclaw_log_pollution_from_stderr(self) -> None:
        harness = OpenClawLiveHarness()
        completed = mock.Mock(
            returncode=0,
            stdout='[{"id": "agent-1"}]',
            stderr="[openclaw] log file size cap reached; suppressing writes file=/tmp/openclaw/openclaw-2026-04-15.log maxFileBytes=5242880\n",
        )

        with mock.patch("harness.live_harness.subprocess.run", return_value=completed):
            exit_code, stdout, stderr, payload = harness._run_agents_list()

        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout, '[{"id": "agent-1"}]')
        self.assertEqual(stderr, "")
        self.assertEqual(payload, [{"id": "agent-1"}])

    def test_payload_usage_merges_multiple_common_locations(self) -> None:
        harness = OpenClawLiveHarness()
        payload = {
            "result": {
                "meta": {
                    "usage": {"prompt_tokens": "100", "completion_tokens": "20"},
                    "agentMeta": {
                        "lastCallUsage": {"cacheRead": 30, "cacheWrite": 40, "total": 190}
                    },
                }
            }
        }

        usage = harness._payload_usage(payload)

        self.assertEqual(usage["input"], 100)
        self.assertEqual(usage["output"], 20)
        self.assertEqual(usage["cacheRead"], 30)
        self.assertEqual(usage["cacheWrite"], 40)
        self.assertEqual(usage["total"], 190)

    def test_merge_stdout_payload_backfills_metrics_without_overwriting_larger_transcript_values(self) -> None:
        harness = OpenClawLiveHarness()
        trace = {
            "events": [{"type": "assistant_message", "text": "done", "seq": 0}],
            "metrics": {
                "input_tokens": 150,
                "output_tokens": 25,
                "cache_read_tokens": 0,
                "cache_write_tokens": 0,
                "total_tokens": 175,
            },
        }
        payload = {
            "result": {
                "meta": {
                    "agentMeta": {
                        "usage": {"input": 120, "output": 30, "total": 150},
                        "lastCallUsage": {"cacheRead": 10, "cacheWrite": 5},
                    }
                }
            }
        }

        harness._merge_stdout_payload(trace, payload)

        self.assertEqual(trace["metrics"]["input_tokens"], 150)
        self.assertEqual(trace["metrics"]["output_tokens"], 30)
        self.assertEqual(trace["metrics"]["cache_read_tokens"], 10)
        self.assertEqual(trace["metrics"]["cache_write_tokens"], 5)
        self.assertEqual(trace["metrics"]["total_tokens"], 175)

    def test_execute_turn_passes_session_metadata_into_trace_normalization(self) -> None:
        harness = OpenClawLiveHarness()
        completed_stdout = '{"result": {"meta": {"agentMeta": {"sessionId": "real-session-id"}}}}'
        proc = mock.Mock()
        proc.returncode = 0
        transcript = [
            {
                "type": "message",
                "message": {
                    "role": "assistant",
                    "content": [{"type": "text", "text": "done"}],
                    "usage": {"input": 0, "output": 0, "totalTokens": 0},
                },
            }
        ]
        session_metadata = {"systemPromptReport": {"systemPrompt": {"chars": 1234}}}

        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            with (
                mock.patch.object(harness, "_create_agent"),
                mock.patch.object(harness, "_ensure_agent_ready", return_value={"ensure_ready_phase": "ready"}),
                mock.patch("harness.live_harness.subprocess.Popen", return_value=proc),
                mock.patch.object(harness, "_communicate_with_heartbeat", return_value=(completed_stdout, "")),
                mock.patch.object(harness, "_wait_and_load_transcript", return_value=transcript),
                mock.patch.object(harness, "_load_session_metadata", return_value=session_metadata),
                mock.patch(
                    "harness.live_harness.normalize_trace",
                    return_value={"events": [{"type": "assistant_message", "text": "done", "seq": 0}], "metrics": {}, "audit_state": {}},
                ) as normalize,
            ):
                result = harness.execute_turn(
                    model="glm/GLM-5",
                    prompt="hello",
                    workspace_path=workspace,
                    timeout=1,
                )

        self.assertEqual(result.status, "success")
        normalize.assert_called_once_with(transcript, session_metadata=session_metadata)


class TargetAgentModeTests(unittest.TestCase):
    """Target-agent mode (fork/target-main): reuse an existing agent (main/颖姗)
    instead of creating a throwaway one. Safety invariants under test:
    never _create_agent, never _delete_agent on the target, never wipe the
    target workspace, never pool."""

    def test_target_mode_reuses_target_agent_id_and_skips_creation(self) -> None:
        harness = OpenClawLiveHarness(target_agent="main")
        completed_stdout = '{"result": {"meta": {"agentMeta": {"sessionId": "real-session-id"}}}}'
        proc = mock.Mock()
        proc.returncode = 0
        transcript = [
            {
                "type": "message",
                "message": {
                    "role": "assistant",
                    "content": [{"type": "text", "text": "done"}],
                    "usage": {"input": 10, "output": 5, "totalTokens": 15},
                },
            }
        ]
        run_calls: list[list[str]] = []

        def capture_run(args, **_kwargs: object) -> mock.Mock:
            run_calls.append(list(args))
            return mock.Mock(returncode=0, stdout="[]", stderr="")

        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            with (
                mock.patch.object(harness, "_create_agent") as create_agent,
                mock.patch.object(harness, "_delete_agent") as delete_agent,
                mock.patch.object(
                    harness, "_ensure_agent_ready", return_value={"ensure_ready_phase": "ready"}
                ),
                mock.patch("harness.live_harness.subprocess.run", side_effect=capture_run),
                mock.patch("harness.live_harness.subprocess.Popen", return_value=proc) as popen,
                mock.patch.object(
                    harness, "_communicate_with_heartbeat", return_value=(completed_stdout, "")
                ),
                mock.patch.object(harness, "_wait_and_load_transcript", return_value=transcript),
            ):
                result = harness.execute_turn(
                    model="minimax/MiniMax-M3",
                    prompt="hello",
                    workspace_path=workspace,
                    timeout=1,
                )

            self.assertEqual(result.status, "success")
            self.assertEqual(result.agent_id, "main")
            create_agent.assert_not_called()
            delete_agent.assert_not_called()
            # No `agents delete`/`agents add` subprocess may target the agent id.
            for args in run_calls:
                self.assertNotIn("delete", args)
                self.assertNotIn("add", args)
            command = popen.call_args.args[0]
            self.assertIn("main", command)
            # The agent id is the target, not a generated ocb6-<model>-<uuid> id.
            agent_index = command.index("--agent")
            self.assertEqual(command[agent_index + 1], "main")

    def test_target_mode_skips_unknown_agent_recreate(self) -> None:
        harness = OpenClawLiveHarness(target_agent="main")
        proc = mock.Mock()
        proc.returncode = 0
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            with (
                mock.patch.object(harness, "_create_agent") as create_agent,
                mock.patch.object(harness, "_delete_agent"),
                mock.patch.object(
                    harness, "_ensure_agent_ready", return_value={"ensure_ready_phase": "ready"}
                ),
                mock.patch.object(harness, "_is_unknown_agent_error", return_value=True),
                mock.patch("harness.live_harness.subprocess.Popen", return_value=proc) as popen,
                mock.patch.object(
                    harness, "_communicate_with_heartbeat", return_value=('{"result": {}}', "")
                ),
                mock.patch.object(harness, "_wait_and_load_transcript", return_value=[]),
            ):
                harness.execute_turn(
                    model="minimax/MiniMax-M3",
                    prompt="hello",
                    workspace_path=workspace,
                    timeout=1,
                )

            # Target mode must not try to (re)create the agent even when an
            # unknown-agent error is observed: _create_agent force-deletes first.
            create_agent.assert_not_called()
            self.assertEqual(popen.call_count, 1)

    def test_target_mode_never_uses_agent_pool(self) -> None:
        harness = OpenClawLiveHarness(target_agent="main", agent_pool_size=2, cleanup_agents=True)
        proc = mock.Mock()
        proc.returncode = 0
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            with (
                mock.patch.object(harness, "_acquire_agent_pool_slot") as acquire_slot,
                mock.patch.object(harness, "_create_agent"),
                mock.patch.object(harness, "_delete_agent"),
                mock.patch.object(
                    harness, "_ensure_agent_ready", return_value={"ensure_ready_phase": "ready"}
                ),
                mock.patch("harness.live_harness.subprocess.Popen", return_value=proc),
                mock.patch.object(
                    harness, "_communicate_with_heartbeat", return_value=('{"result": {}}', "")
                ),
                mock.patch.object(harness, "_wait_and_load_transcript", return_value=[]),
            ):
                result = harness.execute_turn(
                    model="minimax/MiniMax-M3",
                    prompt="hello",
                    workspace_path=workspace,
                    timeout=1,
                )

            acquire_slot.assert_not_called()
            self.assertEqual(result.agent_id, "main")

    def test_target_mode_delete_agent_never_deletes_target(self) -> None:
        harness = OpenClawLiveHarness(target_agent="main")
        with mock.patch.object(harness, "_delete_agent") as delete:
            harness.delete_agent("main")
            delete.assert_not_called()
            # Throwaway agents (probe/pool) still clean up normally.
            harness.delete_agent("ocb6-minimax-minimax-m3-probe")
            delete.assert_called_once_with("ocb6-minimax-minimax-m3-probe")

    def test_target_mode_replace_workspace_contents_stages_without_wiping(self) -> None:
        harness = OpenClawLiveHarness(target_agent="main")
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            target = root / "yingshan"
            target.mkdir()
            (target / "SOUL.md").write_text("soul", encoding="utf-8")
            (target / "skills").mkdir()
            (target / "skills" / "keep.md").write_text("keep", encoding="utf-8")

            source = root / "seed"
            (source / "materials").mkdir(parents=True)
            (source / "materials" / "paper.txt").write_text("paper", encoding="utf-8")

            harness._replace_workspace_contents(source, target)

            # Siblings preserved.
            self.assertEqual((target / "SOUL.md").read_text(encoding="utf-8"), "soul")
            self.assertTrue((target / "skills" / "keep.md").exists())
            # Fixtures staged into expected subpaths.
            self.assertEqual((target / "materials" / "paper.txt").read_text(encoding="utf-8"), "paper")

    def test_non_target_mode_replace_workspace_contents_wipes_target(self) -> None:
        harness = OpenClawLiveHarness()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            target = root / "worker"
            target.mkdir()
            (target / "stale.txt").write_text("stale", encoding="utf-8")

            source = root / "seed"
            source.mkdir()
            (source / "fresh.txt").write_text("fresh", encoding="utf-8")

            harness._replace_workspace_contents(source, target)

            self.assertFalse((target / "stale.txt").exists())
            self.assertEqual((target / "fresh.txt").read_text(encoding="utf-8"), "fresh")

    def test_read_primary_model_reads_agents_defaults_model_primary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            harness = OpenClawLiveHarness(openclaw_state_dir=tmpdir)
            config_path = harness._config_path()
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(
                json.dumps(
                    {"agents": {"defaults": {"model": {"primary": "minimax/MiniMax-M3"}}}}
                ),
                encoding="utf-8",
            )
            self.assertEqual(harness.read_primary_model(), "minimax/MiniMax-M3")

    def test_read_primary_model_returns_none_when_key_absent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            harness = OpenClawLiveHarness(openclaw_state_dir=tmpdir)
            self.assertIsNone(harness.read_primary_model())


if __name__ == "__main__":
    unittest.main()
