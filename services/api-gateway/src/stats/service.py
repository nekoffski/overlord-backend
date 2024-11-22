import time
import grpc

from overlord import proto
from overlord.log import log


MAX_LATENCIES = 250


def get_timestamp():
    return int(time.time_ns() / 1_000_000)


def to_millis(timestamp):
    return int(timestamp.seconds * 1000 + timestamp.nanos / 1_000_000)


class Service(object):
    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port

        self.reset()

    def reset(self):
        self.is_running = False
        self.request_latencies = [0] * MAX_LATENCIES
        self.response_latencies = [0] * MAX_LATENCIES

    async def ping(self):
        async with grpc.aio.insecure_channel(f"{self.host}:{self.port}") as channel:
            try:
                client = proto.PingerStub(channel)

                start = get_timestamp()
                response = await client.ping(proto.PingRequest())

                self.save_request_latency(
                    start=start, end=get_timestamp(), remote=to_millis(response.timestamp))
                self.is_running = True
            except grpc.aio.AioRpcError as error:
                log.warning("Could not ping {}/{}/{} - {}",
                            self.name, self.host, self.port, error.code())
                self.reset()

    def save_request_latency(self, start, end, remote):
        self.request_latencies.pop(0)
        self.request_latencies.append(int(remote - start))
        self.response_latencies.pop(0)
        self.response_latencies.append(int(end - remote))

    def get_statistics(self) -> proto.ServiceStatistics:
        return proto.ServiceStatistics(
            name=self.name,
            is_running=self.is_running,
            request_latencies=self.request_latencies,
            response_latencies=self.response_latencies
        )
