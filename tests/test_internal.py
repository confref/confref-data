"""Internal datasets (decision 0023): their versions go to the internal store."""
import unittest
from pathlib import Path
from unittest import mock

from cr import catalog, config


class InternalStore(unittest.TestCase):
    def test_store_of(self):
        e = catalog.Entry(Path("pc.md"), {"slug": "pc", "internal": "committee members"}, "")
        p = catalog.Entry(Path("dblp.md"), {"slug": "dblp"}, "")
        self.assertEqual(e.internal, "committee members")
        self.assertIsNone(p.internal)
        cat = mock.Mock(entries={"pc": e, "dblp": p})
        cfg = config.Config({"store": "s", "internal_store": "i"}, None)
        with mock.patch.object(catalog, "Catalog", return_value=cat):
            self.assertEqual(cfg.store_of("pc"), (config.ROOT / "i").resolve())
            self.assertEqual(cfg.store_of("dblp"), (config.ROOT / "s").resolve())

    def test_not_configured(self):
        cfg = config.Config({"store": "s"}, None)
        cfg._internal = {"pc"}
        with self.assertRaises(config.ConfigError):
            cfg.store_of("pc")
        self.assertIsNone(cfg.store_of("pc", required=False))


if __name__ == "__main__":
    unittest.main()
