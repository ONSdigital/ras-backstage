import logging
import os
import unittest

from structlog import wrap_logger
from testfixtures import log_capture

from ras_backstage.logger_config import logger_initial_config


class TestLoggerConfig(unittest.TestCase):

    @log_capture()
    def test_success(self, l):
        os.environ['JSON_INDENT_LOGGING'] = '1'
        logger_initial_config(service_name='ras-backstage')
        logger = wrap_logger(logging.getLogger())
        logger.error('Test')
        message = l.records[0].msg

        message_contents = '{\n "event": "Test",\n "level": "error",\n "service": "ras-backstage"'
        self.assertIn(message_contents, message)

    @log_capture()
    def test_indent_type_error(self, l):
        os.environ['JSON_INDENT_LOGGING'] = 'abc'
        logger_initial_config(service_name='ras-backstage')
        logger = wrap_logger(logging.getLogger())
        logger.error('Test')
        message = l.records[0].msg
        self.assertIn('{"event": "Test", "level": "error", "service": "ras-backstage"', message)

    @log_capture()
    def test_indent_value_error(self, l):
        logger_initial_config(service_name='ras-backstage')
        logger = wrap_logger(logging.getLogger())
        logger.error('Test')
        message = l.records[0].msg
        self.assertIn('{"event": "Test", "level": "error", "service": "ras-backstage"', message)
