import socket
import os

from loguru import logger as log

from . import cfg


class _LogServerStream(object):
    def __init__(self, addr):
        self.addr = addr
        self.socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def write(self, message: str):
        try:
            self.socket.sendto(message.encode('utf-8'), self.addr)
        except Exception as e:
            log.warning(
                "Could not send message to the log server - %s", str(e))


def setup_logger(service_name, host=cfg.LOG_SERVER_HOST, port=cfg.LOG_SERVER_LOGGER_PORT):
    log_server_stream = _LogServerStream((host, port))

    def formatter(record):
        record["extra"]["serialized"] = {
            'service': service_name,
            'ts': str(record['time']),
            'level': record['level'].name,
            'file': f'{record['file'].name}:{record['line']}',
            'exception': record['exception'],
            'message': record['message']

        }
        return "{extra[serialized]}\n"

    log.add(log_server_stream, level=cfg.LOG_LEVEL, format=formatter)
    log.info("log server addr: {}:{}, level: {}", host, port, cfg.LOG_LEVEL)
