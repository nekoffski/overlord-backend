
from typing import List
from overlord import proto

from .service import Service


class StatisticsProxy(object):
    def __init__(self, services: List[Service]):
        self.services = services

    def get_service_statistics(self) -> List[proto.ServiceStatistics]:
        return [
            service.get_statistics() for service in self.services
        ]
