from enum import Enum


class Role(Enum):
    ADMIN = 'admin'
    READ_PROPERTIES = 'read-properties'
    WRITE_PROPERTIES = 'write-properties'
    REPORT_OCCURRENCES = 'report-occurrences'
    MANAGE_OCCURRENCES = 'manage-occurrences'
    WRITE_PROTOCOLS = 'write-protocols'
