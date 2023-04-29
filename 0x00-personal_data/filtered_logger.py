#!/usr/bin/env python3
"""[filtered_logger Module]"""
from typing import List
import re
import logging
import mysql.connector
import os
PII_FIELDS = ("name", "phone", "password", "ssn", "email")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """[summary]

        Args:
            fields (List[str]): [description]
        """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """[summary]
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """[summary]

    Args:
        fields (List[str]): [representing all fields to obfuscate]
        redaction (str): [representing by what the field will be obfuscated]
        message (str): [representing the log line]
        separator (str): [ representing by which character is separating
        all fields in the log line]

    Returns:
        str: [the log message obfuscated:]
    """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}', f"{f}={redaction}{separator}",
                         message)
    return message


def get_logger() -> logging.Logger:
    """[summary]

    Returns:
        logging.Logger: [description]
    """
    log = logging.getLogger("user_data")
    log.setLevel(logging.INFO)
    log.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    log.addHandler(handler)
    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """[summary]

    Returns:
        mysql.connector.connection.MySQLConnection: [description]
    """
    user = os.getenv("PERSONAL_DATA_DB_USERNAME")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    host = os.getenv("PERSONAL_DATA_DB_HOST")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(host=host,
                                   database=database,
                                   user=user,
                                   password=password)


def main():
    """[summary]
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    values = cursor.fetchall()
    for value in values:
        message = f"name={value[0]}; email={value[1]}; phone={value[2]}; \
            ssn={value[3]} password={value[4]}; ip={value[5]}; \
                last_login={value[6]}; user_agent={value[7]};"
        log_record = logging.LogRecord("my_logger", logging.INFO, None, None,
                                       message, None, None)
        RedactingFormatter(PII_FIELDS).format(log_record)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
