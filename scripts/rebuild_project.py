import subprocess
import sys


def run_command(command):
    print()
    print("=" * 70)
    print("RUNNING:", " ".join(command))
    print("=" * 70)

    result = subprocess.run(
        command,
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(
            f"Command failed with exit code "
            f"{result.returncode}"
        )


def main():
    run_command(
        [
            sys.executable,
            "scripts/run_pipeline.py",
        ]
    )

    run_command(
        [
            sys.executable,
            "scripts/export_customer_priority.py",
        ]
    )

    run_command(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
        ]
    )

    run_command(
        [
            sys.executable,
            "scripts/validate_business.py",
        ]
    )


if __name__ == "__main__":
    main()