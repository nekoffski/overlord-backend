import * as React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import { LogServerClient } from "./proto/log-server_grpc_web_pb";
import { GetLogsRequest } from "./proto/log-server_pb";

export default class LogsView extends React.Component {
  state = {
    logs: [],
  };

  constructor() {
    super();

    this.logServerClient = new LogServerClient("http://127.0.0.1:8080/");
    this.fetchLogs();
  }

  fetchLogs() {
    this.logServerClient.get_logs(new GetLogsRequest(), [], (err, response) => {
      if (err) {
        console.error(err);
      } else {
        let model = response.toObject();
        this.setState({
          logs: model.logsList,
        });
      }
    });
  }

  render() {
    return (
      <Box sx={{ width: "100%", maxWidth: { sm: "100%", md: "1700px" } }}>
        <Typography component="h2" variant="h6" sx={{ mb: 2 }}>
          System Logs
        </Typography>
        {this.state.logs.map((line) => (
          <p>{line}</p>
        ))}
      </Box>
    );
  }
}
