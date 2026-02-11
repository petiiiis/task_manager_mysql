import os

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")

DB_NAME = "task_manager"
TEST_DB_NAME = "task_manager_test"