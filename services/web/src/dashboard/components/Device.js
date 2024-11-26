import * as React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";

import { ToggleRequest } from "./proto/device_pb";

export default class Device extends React.Component {
  constructor({ device, client }) {
    super();
    this.device = device;
    this.client = client;
  }

  toggle() {
    let request = new ToggleRequest();
    request.setIdsList([this.device.id]);

    console.log(request.toObject());

    this.client.toggle(request, [], (err, response) => {
      if (err) {
        console.error(err);
      }
    });
  }

  render() {
    return (
      <Card variant="outlined" sx={{ width: "100%" }}>
        <CardContent>
          Device {this.device.id}
          <Button variant="outlined" onClick={() => this.toggle()}>
            Toggle
          </Button>
        </CardContent>
      </Card>
    );
  }
}
