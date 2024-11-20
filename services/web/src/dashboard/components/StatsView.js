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
  requestLatencies = [];
  responseLatencies = [];
  name = "";

  isRunning = false;

  constructor(name) {
    this.name = name;
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
    api_gateway: new ServerInfo("API Gateway"),
    log_server: new ServerInfo("Log Server"),
  };

  constructor() {
    super();

    this.apiPinger = new PingerClient("http://127.0.0.1:8080/");
    this.ping();
  }

  ping() {
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
        this.ping();
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
          <Grid size={{ xs: 12, md: 6 }}>
            <SessionsChart data={this.state.api_gateway} />
          </Grid>
          <Grid size={{ xs: 12, md: 6 }}>
            <SessionsChart data={this.state.log_server} />
          </Grid>
        </Grid>
      </Box>
    );
  }
}
