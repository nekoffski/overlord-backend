import grpc

from overlord import proto


class StatisticsProvider(proto.StatisticsProviderServicer):
    def __init__(self, stats_proxy):
        self.stats_proxy = stats_proxy

    async def get_statistics(
        self,
        request: proto.GetStatisticsRequest,
        context: grpc.aio.ServicerContext,
    ) -> proto.GetStatisticsResponse:
        return proto.GetStatisticsResponse(services=self.stats_proxy.get_service_statistics())


def register_statistics_provider_service(server, stats_proxy):
    proto.add_StatisticsProviderServicer_to_server(
        StatisticsProvider(stats_proxy), server)
