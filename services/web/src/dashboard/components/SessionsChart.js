import * as React from "react";
import PropTypes from "prop-types";
import { useTheme } from "@mui/material/styles";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import { LineChart } from "@mui/x-charts/LineChart";

function AreaGradient({ color, id }) {
  return (
    <defs>
      <linearGradient id={id} x1="50%" y1="0%" x2="50%" y2="100%">
        <stop offset="0%" stopColor={color} stopOpacity={0.5} />
        <stop offset="100%" stopColor={color} stopOpacity={0} />
      </linearGradient>
    </defs>
  );
}

AreaGradient.propTypes = {
  color: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
};

export default function SessionsChart({ serviceName, running, data }) {
  const theme = useTheme();

  const colorPalette = [
    theme.palette.primary.light,
    theme.palette.primary.main,
    theme.palette.primary.dark,
  ];

  return (
    <Card variant="outlined" sx={{ width: "100%" }}>
      <CardContent>
        <Typography component="h2" variant="subtitle2" gutterBottom>
          {serviceName}
        </Typography>
        <Stack sx={{ justifyContent: "space-between" }}>
          <Stack
            direction="row"
            sx={{
              alignContent: { xs: "center", sm: "flex-start" },
              alignItems: "center",
              gap: 1,
            }}
          >
            <Typography variant="h4" component="p">
              {running ? "Up" : "Down"}
            </Typography>
          </Stack>
          <Typography variant="caption" sx={{ color: "text.secondary" }}>
            Latency (ms)
          </Typography>
        </Stack>
        <LineChart
          skipAnimation
          colors={colorPalette}
          bottomAxis={null}
          series={[
            {
              id: "direct",
              label: "Direct",
              showMark: false,
              curve: "linear",
              stack: "total",
              area: true,
              stackOrder: "ascending",
              data: running ? data : [],
            },
            // {
            //   id: "referral",
            //   label: "Referral",
            //   showMark: false,
            //   curve: "linear",
            //   stack: "total",
            //   area: true,
            //   stackOrder: "ascending",
            //   data: [
            //     500, 900, 700, 1400, 1100, 1700, 2300, 2000, 2600, 2900, 2300,
            //     3200, 3500, 3800, 4100, 4400, 2900, 4700, 5000, 5300, 5600,
            //     5900, 6200, 6500, 5600, 6800, 7100, 7400, 7700, 8000,
            //   ],
            // },
            // {
            //   id: "organic",
            //   label: "Organic",
            //   showMark: false,
            //   curve: "linear",
            //   stack: "total",
            //   stackOrder: "ascending",
            //   data: [
            //     1000, 1500, 1200, 1700, 1300, 2000, 2400, 2200, 2600, 2800,
            //     2500, 3000, 3400, 3700, 3200, 3900, 4100, 3500, 4300, 4500,
            //     4000, 4700, 5000, 5200, 4800, 5400, 5600, 5900, 6100, 6300,
            //   ],
            //   area: true,
            // },
          ]}
          height={250}
          margin={{ left: 50, right: 20, top: 20, bottom: 20 }}
          grid={{ horizontal: true }}
          sx={{
            "& .MuiAreaElement-series-organic": {
              fill: "url('#organic')",
            },
            "& .MuiAreaElement-series-referral": {
              fill: "url('#referral')",
            },
            "& .MuiAreaElement-series-direct": {
              fill: "url('#direct')",
            },
          }}
          slotProps={{
            legend: {
              hidden: true,
            },
          }}
        >
          <AreaGradient color={theme.palette.primary.dark} id="organic" />
          <AreaGradient color={theme.palette.primary.main} id="referral" />
          <AreaGradient color={theme.palette.primary.light} id="direct" />
        </LineChart>
      </CardContent>
    </Card>
  );
}
