#!/usr/bin/env python3
"""Return the computer's current local date for task document generation."""

from __future__ import annotations

import json
from datetime import datetime


def main() -> None:
    now = datetime.now().astimezone()
    print(
        json.dumps(
            {
                "filename_date": now.strftime("%y%m%d"),
                "document_date": now.strftime("%Y-%m-%d"),
                "generated_at": now.isoformat(timespec="seconds"),
            },
            ensure_ascii=True,
        )
    )


if __name__ == "__main__":
    main()
