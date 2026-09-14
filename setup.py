from __future__ import annotations

import getpass
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
ENV_FILE = ROOT / ".env"

REQUIRED_DIRECTORIES = [
    ROOT / "resume_system" / "experience_corpus",
]

DEPENDENCIES = [
    "openai",
    "pydantic",
    "python-dotenv",
    "discord.py",
    "requests",
    "beautifulsoup4",
    "python-docx",
]


def create_directories() -> None:
    print("\nCreating required directories...")

    for directory in REQUIRED_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory.relative_to(ROOT)}")


def create_virtual_environment() -> None:
    if VENV_DIR.exists():
        print("\nVirtual environment already exists.")
        return

    print("\nCreating virtual environment...")

    subprocess.run(
        [sys.executable, "-m", "venv", str(VENV_DIR)],
        check=True,
    )

    print("  ✓ .venv created")


def get_venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"

    return VENV_DIR / "bin" / "python"


def install_dependencies() -> None:
    python = get_venv_python()

    print("\nUpgrading pip...")

    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
        ],
        check=True,
    )

    print("\nInstalling dependencies...")

    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            *DEPENDENCIES,
        ],
        check=True,
    )

    print("  ✓ Dependencies installed")


def configure_environment() -> None:
    print("\nConfiguring API credentials...")

    if ENV_FILE.exists():
        answer = input(
            ".env already exists. Replace it? [y/N]: "
        ).strip().lower()

        if answer not in {"y", "yes"}:
            print("  ✓ Existing .env preserved")
            return

    openai_key = getpass.getpass(
        "OpenAI API key: "
    ).strip()

    discord_token = getpass.getpass(
        "Discord bot token: "
    ).strip()

    if not openai_key:
        raise ValueError(
            "OpenAI API key cannot be empty."
        )

    contents = (
        f"OPENAI_API_KEY={openai_key}\n"
        f"DISCORD_BOT_TOKEN={discord_token}\n"
    )

    ENV_FILE.write_text(
        contents,
        encoding="utf-8",
    )

    # Restrict permissions on Linux/macOS.
    if os.name != "nt":
        ENV_FILE.chmod(0o600)

    print("  ✓ .env created")


def print_next_steps() -> None:
    print("\n" + "=" * 60)
    print("Career Chameleon setup complete.")
    print("=" * 60)

    if os.name == "nt":
        print("\nActivate the virtual environment in PowerShell:")
        print(r"  .\.venv\Scripts\Activate.ps1")

        print("\nThen run:")
        print(r"  python -m resume_system.main")

    else:
        print("\nActivate the virtual environment:")
        print("  source .venv/bin/activate")

        print("\nThen run:")
        print("  python -m resume_system.main")

    print(
        "\nAdd professional evidence YAML files to:"
    )
    print(
        "  resume_system/experience_corpus/"
    )


def main() -> None:
    print("=" * 60)
    print("Career Chameleon Setup")
    print("=" * 60)

    try:
        create_directories()
        create_virtual_environment()
        install_dependencies()
        configure_environment()
        print_next_steps()

    except subprocess.CalledProcessError as exc:
        print(
            f"\nSetup failed while running a command: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)

    except Exception as exc:
        print(
            f"\nSetup failed: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()