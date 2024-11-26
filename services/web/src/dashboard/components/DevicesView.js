import * as React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid2";
import Device from "./Device";

import { DeviceGatewayClient } from "./proto/device-gateway_grpc_web_pb";
import { GetDevicesRequest } from "./proto/device_pb";

export default class DevicesView extends React.Component {
  state = {
    devices: [],
  };

  constructor() {
    super();
    this.deviceGatewayClient = new DeviceGatewayClient(
      "http://127.0.0.1:8080/"
    );
    this.fetchDevices();
  }

  fetchDevices() {
    this.deviceGatewayClient.get_devices(
      new GetDevicesRequest(),
      [],
      (err, response) => {
        if (err) {
          console.error(err);
        } else {
          let model = response.toObject();
          this.setState({
            devices: model.devicesList,
          });
        }
      }
    );
  }

  render() {
    return (
      <Box sx={{ width: "100%", maxWidth: { sm: "100%", md: "1700px" } }}>
        <Grid
          container
          spacing={2}
          columns={12}
          sx={{ mb: (theme) => theme.spacing(2) }}
        >
          {this.state.devices.map((device, _) => {
            return (
              <Grid size={{ xs: 6, md: 3 }}>
                <Device device={device} client={this.deviceGatewayClient} />
              </Grid>
            );
          })}
        </Grid>
      </Box>
    );
  }
}
