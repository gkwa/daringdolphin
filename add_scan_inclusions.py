#!/usr/bin/env python3
"""Add scan_inclusions to .zed/settings.json if they don't already exist."""

import argparse
import json
import logging
import pathlib


def setup_logging(verbosity: int) -> None:
    """Configure logging based on verbosity level."""
    if verbosity == 0:
        level = logging.WARNING
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


def load_json_file(file_path: pathlib.Path) -> dict[str, object]:
    """Load and parse a JSON file."""
    with file_path.open(encoding="utf-8") as f:
        return json.load(f)


def save_json_file(file_path: pathlib.Path, data: dict[str, object]) -> None:
    """Save data to a JSON file with pretty formatting."""
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        _ = f.write("\n")


def add_scan_inclusions(settings_path: pathlib.Path, new_inclusions: list[str]) -> bool:
    """
    Add new scan inclusions to settings.json if they don't already exist.

    Returns True if any changes were made, False otherwise.
    """
    settings = load_json_file(settings_path)

    existing_inclusions = settings.get("file_scan_inclusions", [])
    if not isinstance(existing_inclusions, list):
        existing_inclusions = []

    modified = False

    for inclusion in new_inclusions:
        if inclusion not in existing_inclusions:
            existing_inclusions.append(inclusion)
            modified = True
            logging.info("Added: %s", inclusion)
        else:
            logging.debug("Already exists: %s", inclusion)

    if modified:
        settings["file_scan_inclusions"] = existing_inclusions
        save_json_file(settings_path, settings)
        logging.info("Updated %s", settings_path)
        return True
    logging.debug("No changes needed")
    return False


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Add scan inclusions to .zed/settings.json"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v for INFO, -vv for DEBUG)",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()
    setup_logging(args.verbose)

    settings_path = pathlib.Path(".zed/settings.json")

    if not settings_path.exists():
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        initial_settings: dict[str, object] = {}
        save_json_file(settings_path, initial_settings)
        logging.info("Created %s", settings_path)

    new_inclusions = [
        "**/.nearwait.yml",
    ]

    _ = add_scan_inclusions(settings_path, new_inclusions)


if __name__ == "__main__":
    main()
