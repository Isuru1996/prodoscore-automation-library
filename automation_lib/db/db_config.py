"""Database configuration utilities."""

from typing import Any, Dict


class DBConfig:
    """Database configuration manager."""

    @staticmethod
    def get_mysql_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """Get MySQL configuration.

        Args:
            config: Configuration dictionary

        Returns:
            MySQL connection parameters
        """
        return {
            "host": config.get("db", {}).get("host", "localhost"),
            "database": config.get("db", {}).get("database", ""),
            "user": config.get("db", {}).get("user", "root"),
            "password": config.get("db", {}).get("password", ""),
            "port": config.get("db", {}).get("port", 3306),
            "pool_size": config.get("db", {}).get("pool_size", 10),
        }
