import * as React from "react";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid2";
import Typography from "@mui/material/Typography";
import Card from "@mui/material/Card";
import Stack from "@mui/material/Stack";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Checkbox from "@mui/material/Checkbox";
import { Wheel, ShadeSlider } from "@uiw/react-color";

import { DeviceGatewayClient } from "./proto/device-gateway_grpc_web_pb";
import {
  GetDevicesRequest,
  ToggleRequest,
  SetHsvRequest,
} from "./proto/device_pb";

class Device extends React.Component {
  state = {
    hsva: { h: 214, s: 43, v: 90, a: 1 },
    selected: false,
  };

  constructor({ device, toggle, setColor, onSelect, isMultiOption }) {
    super();
    this.device = device;
    this.toggle = toggle;
    this.setColor = setColor;
    this.onSelect = onSelect;
    this.isMultiOption = isMultiOption;
  }

  render() {
    return (
      <Card variant="outlined" sx={{ width: "100%" }}>
        <CardContent>
          <Typography component="h3" variant="h7" sx={{ mb: 2 }}>
            {!this.isMultiOption && (
              <Checkbox
                checked={this.state.selected}
                onChange={() => {
                  const newState = !this.state.selected;
                  this.setState({
                    selected: newState,
                  });
                  this.onSelect(newState);
                }}
                inputProps={{ "aria-label": "controlled" }}
              />
            )}
            {this.isMultiOption ? "Selected" : `Device #${this.device.id}`}
            <Typography
              component="h3"
              variant="h7"
              style={{ marginLeft: 20, marginTop: 20 }}
              sx={{ mb: 2 }}
            >
              <Wheel
                color={this.state.hsva}
                onChange={(color) => {
                  this.setState({
                    hsva: {
                      h: Math.round(color.hsva.h),
                      s: Math.round(color.hsva.s),
                      v: this.state.hsva.v,
                      a: this.state.hsva.a,
                    },
                  });
                }}
              />
              <ShadeSlider
                hsva={this.state.hsva}
                style={{ width: 200, marginTop: 20 }}
                onChange={(newShade) => {
                  this.setState({
                    hsva: {
                      h: this.state.hsva.h,
                      s: this.state.hsva.s,
                      v: Math.round(newShade.v),
                      a: this.state.hsva.a,
                    },
                  });
                }}
              />
            </Typography>
          </Typography>

          <Stack direction="row" sx={{ gap: 1 }}>
            <Button variant="outlined" onClick={this.toggle}>
              Toggle
            </Button>
            <Button
              variant="outlined"
              onClick={() => {
                this.setColor(this.state.hsva);
              }}
            >
              Set Color
            </Button>
          </Stack>
        </CardContent>
      </Card>
    );
  }
}

export default class DevicesView extends React.Component {
  state = {
    devices: {},
    selected: [],
  };

  constructor() {
    super();
    this.client = new DeviceGatewayClient("http://127.0.0.1:8080/");
    this.fetchDevices();
  }

  fetchDevices() {
    this.client.get_devices(new GetDevicesRequest(), [], (err, response) => {
      if (err) {
        console.error(err);
      } else {
        let model = response.toObject();
        this.setState({
          devices: Object.fromEntries(
            model.devicesList.map((device) => [
              device.id,
              {
                id: device.id,
              },
            ])
          ),
        });
      }
      // setTimeout(() => this.fetchDevices(), 1000);
    });
  }

  setColor(ids, hsva) {
    this.client.set_hsv(
      new SetHsvRequest(hsva)
        .setH(hsva.h)
        .setS(hsva.s)
        .setV(hsva.v)
        .setIdsList(ids),
      [],
      (err, _) => {
        if (err) {
          console.error(err);
        }
      }
    );
  }

  toggle(ids) {
    this.client.toggle(new ToggleRequest().setIdsList(ids), [], (err, _) => {
      if (err) {
        console.error(err);
      }
    });
  }

  onSelect(id, state) {
    let selected = this.state.selected;
    if (state) selected.push(id);
    else selected.splice(selected.indexOf(id), 1);
    this.setState({
      selected: selected,
    });
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
          {Object.keys(this.state.devices).map((id, _) => {
            let device = this.state.devices[id];
            return (
              <Grid size={{ xs: 3, md: 3 }}>
                <Device
                  device={device}
                  toggle={() => this.toggle([id])}
                  setColor={(color) => this.setColor([id], color)}
                  onSelect={(state) => this.onSelect(parseInt(id), state)}
                  isMultiOption={false}
                />
              </Grid>
            );
          })}
          {this.state.selected.length > 0 && (
            <Grid size={{ xs: 3, md: 3 }}>
              <Device
                toggle={() => this.toggle(this.state.selected)}
                setColor={(color) => this.setColor(this.state.selected, color)}
                isMultiOption={true}
              />
            </Grid>
          )}
        </Grid>
      </Box>
    );
  }
}
