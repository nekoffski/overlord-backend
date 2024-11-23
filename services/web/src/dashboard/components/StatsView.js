import * as React from "react";
import Grid from "@mui/material/Grid2";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import SessionsChart from "./SessionsChart";

import { PingerClient } from "./proto/ping_grpc_web_pb";
import { PingRequest } from "./proto/ping_pb";
import { StatisticsProviderClient } from "./proto/stats_grpc_web_pb";
import { GetStatisticsRequest } from "./proto/stats_pb";

function toMillis(seconds, nanoseconds) {
  return Math.round(seconds * 1000 + nanoseconds / 1_000_000);
}

const maxLatencyElements = 250;

class ServiceInfo {
  name = "";
  requestLatencies = [];
  responseLatencies = [];

  constructor(name, requestLatencies, responseLatencies, isRunning) {
    this.name = name;
    this.requestLatencies = requestLatencies;
    this.responseLatencies = responseLatencies;
    this.isRunning = isRunning;
  }
}

class ApiInfo extends ServiceInfo {
  constructor() {
    super("API Gateway", [], [], false);
    this.invalidate();
  }

  invalidate() {
    this.isRunning = false;
    this.requestLatencies = Array(maxLatencyElements).fill(0);
    this.responseLatencies = Array(maxLatencyElements).fill(0);
  }
}

export default class StatsView extends React.Component {
  state = {
    api_gateway: new ApiInfo(),
    services: [],
  };

  constructor() {
    super();

    this.statsProvider = new StatisticsProviderClient("http://127.0.0.1:8080/");
    this.apiPinger = new PingerClient("http://127.0.0.1:8080/");
    this.pingApi();
    this.gatherStatistics();
  }

  gatherStatistics() {
    this.statsProvider.get_statistics(
      new GetStatisticsRequest(),
      [],
      (err, res) => {
        let services = [];

        if (err) {
          console.error(err);
        } else {
          let model = res.toObject();
          services = Array.from(model.servicesList, (service) => {
            return new ServiceInfo(
              service.name,
              service.requestLatenciesList,
              service.responseLatenciesList,
              service.isRunning
            );
          });
        }

        this.setState({
          services: services,
        });
        setTimeout(() => {
          this.gatherStatistics();
        }, 750);
      }
    );
  }

  pingApi() {
    const start = Date.now();
    let request = new PingRequest();

    this.apiPinger.ping(request, {}, (err, res) => {
      let server = this.state.api_gateway;

      if (err) {
        console.log(err);
        server.invalidate();
      } else {
        const timestamp = res.toObject().timestamp;
        const timestampMillis = toMillis(timestamp.seconds, timestamp.nanos);

        const requestDelay = timestampMillis - start;
        const responseDelay = Date.now() - timestampMillis;

        server.isRunning = true;
        server.requestLatencies.push(requestDelay);
        server.requestLatencies.shift();
        server.responseLatencies.push(responseDelay);
        server.responseLatencies.shift();
      }

      this.setState({
        api_gateway: server,
      });

      setTimeout(() => {
        this.pingApi();
      }, 750);
    });
  }

  render() {
    return (
      <Box sx={{ width: "100%", maxWidth: { sm: "100%", md: "1700px" } }}>
        {/* cards */}
        <Typography component="h2" variant="h6" sx={{ mb: 2 }}>
          System Metrics & Health
        </Typography>
        <Grid
          container
          spacing={2}
          columns={12}
          sx={{ mb: (theme) => theme.spacing(2) }}
        >
          <Grid size={{ xs: 6, md: 6 }}>
            <SessionsChart data={this.state.api_gateway} />
          </Grid>
          {this.state.services.map((service, _) => {
            return (
              <Grid size={{ xs: 6, md: 6 }}>
                <SessionsChart data={service} />
              </Grid>
            );
          })}
        </Grid>
      </Box>
    );
  }
}
