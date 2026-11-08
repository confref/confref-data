#!/usr/bin/env python3
"""cr: the generator framework (kg-commons 0018). Run ./cr --help for the commands."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from cr.cli import main  # noqa: E402

sys.exit(main())
