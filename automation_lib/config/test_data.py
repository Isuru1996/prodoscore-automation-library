import json
from pathlib import Path


class TestDataLoader:
    """Loads test data from a JSON file."""

    __test__ = False

    def __init__(self, data_file):
        """Initialize TestDataLoader."""
        data_path = Path(data_file)
        if not data_path.exists():
            raise FileNotFoundError(f"Test data file not found: {data_path}")
        with open(data_path, "r") as f:
            self.data = json.load(f)

    def get(self, test_name=None, key=None, default=None):
        """Retrieve test data for a given test name and key."""
        test_data = self.data if test_name is None else self.data.get(test_name, {})
        if key:
            return test_data.get(key, default)
        return test_data or default
