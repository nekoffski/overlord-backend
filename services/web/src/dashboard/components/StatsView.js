import * as React from "react";
import Grid from "@mui/material/Grid2";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import SessionsChart from "./SessionsChart";

import { PingerClient } from "./proto/ping_grpc_web_pb";
import { PingRequest } from "./proto/ping_pb";

function toMillis(seconds, nanoseconds) {
  return Math.round(seconds * 1000 + nanoseconds / 1_000_000);
}

const maxLatencyElements = 250;

class ServerInfo {
  latencies = [];
  isRunning = false;

  constructor() {
    this.invalidate();
  }

  invalidate() {
    this.isRunning = false;
    this.latencies = Array(maxLatencyElements).fill(0);
  }
}

export default class StatsView extends React.Component {
  state = {
    api_gateway: new ServerInfo(),
    log_server: new ServerInfo(),
  };

  constructor() {
    super();

    this.apiPinger = new PingerClient("http://127.0.0.1:8080/");
    this.ping();
  }

  ping() {
    const now = Date.now();
    let request = new PingRequest();

    this.apiPinger.ping(request, {}, (err, res) => {
      let server = this.state.api_gateway;

      if (err) {
        console.log(err);
        server.invalidate();
      } else {
        const timestamp = res.toObject().timestamp;
        const timestampMillis = toMillis(timestamp.seconds, timestamp.nanos);
        const delay = timestampMillis - now;

        server.isRunning = true;
        server.latencies.push(delay);
        server.latencies.shift();
      }

      this.setState({
        api_gateway: server,
      });

      setTimeout(() => {
        this.ping();
      }, 500);
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
          <Grid size={{ xs: 12, md: 6 }}>
            <SessionsChart
              serviceName={"API Gateway"}
              running={this.state.api_gateway.isRunning}
              data={this.state.api_gateway.latencies}
            />
          </Grid>
          <Grid size={{ xs: 12, md: 6 }}>
            <SessionsChart
              serviceName={"Log Server"}
              running={this.state.log_server.isRunning}
              data={this.state.log_server.latencies}
            />
          </Grid>
        </Grid>
      </Box>
    );
  }
}
