"""MySQL database client for test automation."""

import logging
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Union, cast

from mysql.connector import Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from automation_lib.core import Logger
from automation_lib.core.exceptions import (
    DatabaseConnectionError,
    DatabasePoolError,
    DatabaseQueryError,
)

logger = Logger.get_logger("MySQLClient")


class MySQLClient:
    """MySQL database client wrapper with connection pooling and retry mechanism.

    Uses connection pooling for better performance and resource management.
    Can be used as a context manager for automatic connection/disconnection.

    Example:
        with MySQLClient(host="localhost", database="test", user="root", password="pass") as client:
            results = client.execute_query("SELECT * FROM users")
    """

    def __init__(
        self,
        host: str,
        database: str,
        user: str,
        password: str,
        port: int = 3306,
        pool_name: str = "mypool",
        pool_size: int = 5,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """Initialize MySQL client with connection pooling.

        Args:
            host: Database host
            database: Database name
            user: Database user
            password: Database password
            port: Database port
            pool_name: Name for the connection pool
            pool_size: Maximum number of connections in the pool
            max_retries: Maximum number of retry attempts for failed operations
            retry_delay: Delay in seconds between retry attempts
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.pool_name = pool_name
        self.pool_size = pool_size
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.pool: Optional[MySQLConnectionPool] = None
        self._is_connected = False

    def _create_retry_decorator(self):
        """Create a retry decorator with configured settings."""
        return retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=self.retry_delay, min=1, max=10),
            retry=retry_if_exception_type(
                (
                    DatabaseConnectionError,
                    DatabasePoolError,
                    DatabaseQueryError,
                )
            ),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True,
        )

    def __enter__(self):
        """Context manager entry - automatically connects to database pool."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - automatically disconnects from database."""
        self.disconnect()
        return False

    def connect(self) -> None:
        """Establish connection pool with retry mechanism using tenacity.

        Raises:
            DatabasePoolError: If connection pool creation fails
        """
        if self._is_connected:
            logger.info("Connection pool already created")
            return

        @self._create_retry_decorator()
        def _connect_pool():
            try:
                self.pool = MySQLConnectionPool(
                    pool_name=self.pool_name,
                    pool_size=self.pool_size,
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                )
                self._is_connected = True
                logger.info(
                    f"Connection pool '{self.pool_name}' created with size {self.pool_size}"
                )
            except Error as e:
                raise DatabasePoolError(
                    message=f"Failed to create connection pool '{self.pool_name}'",
                    details=str(e),
                )

        _connect_pool()

    def get_connection(
        self,
    ) -> Union[PooledMySQLConnection, MySQLConnectionAbstract]:
        """Get a connection from the pool.

        Returns:
            Pooled MySQL connection object

        Raises:
            DatabaseConnectionError: If no connection pool is available
        """
        if self.pool:
            return self.pool.get_connection()
        else:
            raise DatabaseConnectionError(
                host=self.host,
                database=self.database,
                message="No connection pool available",
                details="Call connect() first",
            )

    def disconnect(self) -> None:
        """Close database connection pool."""
        if not self._is_connected:
            return

        if self.pool:
            # Connection pool cleanup is handled automatically by mysql.connector
            logger.info(f"Connection pool '{self.pool_name}' cleanup initiated")

        self._is_connected = False
        self.pool = None

    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor from connection pool.

        Yields:
            Database cursor
        """
        connection = None
        cursor = None

        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            yield cursor
            connection.commit()
        except Error as e:
            if connection:
                connection.rollback()
            raise DatabaseQueryError(
                query="N/A",
                message=str(e),
                details=f"Error code: {e.errno}" if hasattr(e, "errno") else None,
            )
        finally:
            if cursor:
                cursor.close()
            # Return connection to pool
            if connection:
                connection.close()

    def execute_query(
        self, query: str, params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """Execute a SELECT query with retry mechanism using tenacity.

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            List of result rows as dictionaries
        """

        @self._create_retry_decorator()
        def _execute():
            try:
                with self.get_cursor() as cursor:
                    cursor.execute(query, params or ())
                    return cast(List[Dict[str, Any]], cursor.fetchall())
            except Error as e:
                raise DatabaseQueryError(
                    query=query,
                    message=str(e),
                    details=f"Error code: {e.errno}" if hasattr(e, "errno") else None,
                )

        return _execute()

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an INSERT, UPDATE, or DELETE query with retry mechanism using tenacity.

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            Number of affected rows
        """

        @self._create_retry_decorator()
        def _execute():
            try:
                with self.get_cursor() as cursor:
                    cursor.execute(query, params or ())
                    return cursor.rowcount
            except Error as e:
                raise DatabaseQueryError(
                    query=query,
                    message=str(e),
                    details=f"Error code: {e.errno}" if hasattr(e, "errno") else None,
                )

        return _execute()

    def fetch_one(
        self, query: str, params: Optional[tuple] = None
    ) -> Optional[Dict[str, Any]]:
        """Fetch a single row with retry mechanism using tenacity.

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            Single row as dictionary or None
        """

        @self._create_retry_decorator()
        def _execute():
            try:
                with self.get_cursor() as cursor:
                    cursor.execute(query, params or ())
                    return cast(Optional[Dict[str, Any]], cursor.fetchone())
            except Error as e:
                raise DatabaseQueryError(
                    query=query,
                    message=str(e),
                    details=f"Error code: {e.errno}" if hasattr(e, "errno") else None,
                )

        return _execute()

    def fetch_all(
        self, query: str, params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """Fetch all rows as a list of dictionaries with retry mechanism using tenacity."""

        @self._create_retry_decorator()
        def _execute():
            try:
                with self.get_cursor() as cursor:
                    cursor.execute(query, params or ())
                    return cast(List[Dict[str, Any]], cursor.fetchall())
            except Error as e:
                raise DatabaseQueryError(
                    query=query,
                    message=str(e),
                    details=f"Error code: {e.errno}" if hasattr(e, "errno") else None,
                )

        return _execute()

    def bulk_insert(self, query: str, params_list: List[tuple]) -> int:
        """Bulk insert using executemany. Returns number of inserted rows."""

        @self._create_retry_decorator()
        def _execute():
            try:
                with self.get_cursor() as cursor:
                    cursor.executemany(query, params_list)
                    return cursor.rowcount
            except Error as e:
                raise DatabaseQueryError(
                    query=query,
                    message=str(e),
                    details=f"Error code: {e.errno}" if hasattr(e, "errno") else None,
                )

        return _execute()

    def bulk_update(self, query: str, params_list: List[tuple]) -> int:
        """Bulk update using executemany. Returns number of affected rows."""

        @self._create_retry_decorator()
        def _execute():
            try:
                with self.get_cursor() as cursor:
                    cursor.executemany(query, params_list)
                    return cursor.rowcount
            except Error as e:
                raise DatabaseQueryError(
                    query=query,
                    message=str(e),
                    details=f"Error code: {e.errno}" if hasattr(e, "errno") else None,
                )

        return _execute()
