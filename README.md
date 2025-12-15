# Prodoscore Automation Library

A comprehensive automation library for Prodoscore application testing using Playwright, Pytest, and Page Object Model.

## Features

- ✅ Playwright Sync API integration
- ✅ Page Object Model (POM) architecture
- ✅ MySQL database client
- ✅ Browser and context management
- ✅ Logging utilities
- ✅ Configuration management
- ✅ Reusable helper functions
- ✅ Base page classes with common functionality

## Project Structure

```
automation_lib/
├── core/                       # Core framework components
│   ├── base_page.py           # Base page class for POM
│   ├── config.py              # Configuration management
│   ├── logger.py              # Logging utilities
│   └── utils.py               # Common utility functions
├── db/                         # Database utilities
│   ├── mysql_client.py        # MySQL database client
│   └── db_config.py           # Database configuration
├── playwright/                 # Playwright management
│   ├── browser_manager.py     # Browser lifecycle management
│   └── context_manager.py     # Context and page management
├── pages/                      # Page Object Models
├── helpers/                    # Helper utilities
└── listeners/                  # Test listeners and hooks
```

## Installation

This library is designed to be installed as a dependency in test projects:

### In your test project's `pyproject.toml`:

```toml
[project]
dependencies = [
    "prodoscore-automation-library",
]

[tool.uv.sources]
prodoscore-automation-library = { path = "../prodoscore-automation-library", editable = true }
```

Then run:
```bash
uv sync
```

## Usage Examples

### Basic Page Interaction

```python
from playwright.sync_api import Page
from automation_lib.core.base_page import BasePage

def test_example(page: Page):
    base_page = BasePage(page)
    base_page.navigate_to("https://example.com")
    
    # Check element visibility
    assert base_page.is_visible("h1")
    
    # Get text content
    title_text = base_page.get_text("h1")
    
    # Fill input field
    base_page.fill("#username", "testuser")
    
    # Click button
    base_page.click("#submit")
```

### Browser Management

```python
from automation_lib.playwright.browser_manager import BrowserManager

# Create browser manager
manager = BrowserManager(browser_type='chromium', headless=False)
browser = manager.launch()

# Use browser...

# Clean up
manager.close()
```

### Database Operations

```python
from automation_lib.db.mysql_client import MySQLClient

# Create database client
db = MySQLClient(
    host="localhost",
    database="testdb",
    user="root",
    password="password"
)

db.connect()

# Execute queries
results = db.execute_query("SELECT * FROM users WHERE id = %s", (1,))
user = db.fetch_one("SELECT * FROM users WHERE email = %s", ("test@example.com",))

# Execute updates
rows_affected = db.execute_update("UPDATE users SET status = %s WHERE id = %s", ("active", 1))

db.disconnect()
```

### Configuration Management

```python
from automation_lib.core.config import Config

# Load configuration from YAML
config = Config("path/to/config.yaml")

# Get configuration values
db_host = config.get("db.host")
timeout = config.get("browser.timeout", default=30000)

# Get from environment
api_key = config.get_env("API_KEY")
```

### Logging

```python
from automation_lib.core.logger import Logger

# Setup logger
logger = Logger.setup_logger(
    name="test_automation",
    log_file="logs/test.log",
    level=logging.INFO
)

logger.info("Test started")
logger.error("Test failed with error")
```

## Development

### Adding New Page Objects

Create page objects in `automation_lib/pages/`:

```python
from automation_lib.core.base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = "#username"
        self.password_input = "#password"
        self.login_button = "#login"
    
    def login(self, username: str, password: str):
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)
```

### Building the Library

```bash
# Sync dependencies
uv sync

# Run tests (if any)
uv run pytest

# Build distribution
uv build
```

## Dependencies

- playwright >= 1.57.0
- pytest >= 8.0.0
- pytest-playwright >= 0.7.2
- pytest-xdist >= 3.5.0
- allure-pytest >= 2.13.0
- pytest-html >= 4.1.0
- mysql-connector-python >= 8.3.0
- pyyaml >= 6.0.1

## Contributing

When adding new features to the library:

1. Follow the existing code structure
2. Add appropriate docstrings
3. Update this README if needed
4. Ensure backward compatibility with existing tests

## License

Internal use only - Prodoscore Inc.
