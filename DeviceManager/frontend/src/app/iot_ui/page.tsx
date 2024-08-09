'use client'

import * as React from "react"
import { Label, Pie, PieChart, Area, AreaChart, CartesianGrid, XAxis } from "recharts"
import { TemperatureChart } from "../components/temperature-chart"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"

const chartConfig: ChartConfig = {
  temperature: {
    label: "Temperature",
    color: "hsl(var(--chart-1))",
  },
  pressure: {
    label: "Pressure",
    color: "hsl(var(--chart-2))",
  },
}

const getTemperatureColor = (temp: number) => {
  if (temp < 0) return "hsl(240, 100%, 50%)";
  if (temp < 20) return "hsl(120, 100%, 50%)";
  if (temp < 30) return "hsl(60, 100%, 50%)";
  return "hsl(0, 100%, 50%)";
};

const GaugeChart = ({ value, label, color, min, max }) => {
  const percentage = ((value - min) / (max - min)) * 100;
  const gaugeColor = label.includes("Temperature") ? getTemperatureColor(value) : color;
  
  const data = [
    { name: label, value: percentage, fill: gaugeColor },
    { name: "Remaining", value: 100 - percentage, fill: "hsl(var(--muted))" },
  ]

  return (
    <Card className="flex flex-col">
      <CardHeader className="items-center pb-0">
        <CardTitle>{label}</CardTitle>
      </CardHeader>
      <CardContent className="flex-1 pb-0">
        <ChartContainer
          config={chartConfig}
          className="mx-auto aspect-square max-h-[250px]"
        >
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              innerRadius={60}
              strokeWidth={5}
            >
              <Label
                content={({ viewBox }) => {
                  if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                    return (
                      <text
                        x={viewBox.cx}
                        y={viewBox.cy}
                        textAnchor="middle"
                        dominantBaseline="middle"
                      >
                        <tspan
                          x={viewBox.cx}
                          y={viewBox.cy}
                          className="fill-foreground text-3xl font-bold"
                        >
                          {value.toFixed(1)}
                        </tspan>
                        <tspan
                          x={viewBox.cx}
                          y={(viewBox.cy || 0) + 24}
                          className="fill-muted-foreground"
                        >
                          {label}
                        </tspan>
                      </text>
                    )
                  }
                }}
              />
            </Pie>
          </PieChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}


export default function IoTUI() {
  const [gauges, setGauges] = React.useState({
    temperature: 20,
    pressure: 1013,
  })

  const [timeSeriesData, setTimeSeriesData] = React.useState(() => {
    const now = Date.now();
    return Array.from({ length: 24 }, (_, i) => ({
      time: now - (23 - i) * 3600000, // Generate data for the last 24 hours
      temperature: 20 + Math.random() * 10 - 5, // Random temperature between 15 and 25
    }));
  });

  React.useEffect(() => {
    (window as any).updateGauges = (newValues: Partial<typeof gauges>) => {
      setGauges(prevGauges => ({ ...prevGauges, ...newValues }))
      setTimeSeriesData(prevData => [
        ...prevData.slice(-9),
        { time: Date.now(), ...newValues },
      ])
    }

    return () => {
      delete (window as any).updateGauges
    }
  }, [])

  return (
    <div className="p-4">
      <div className="grid grid-cols-2 gap-4 mb-4">
        <GaugeChart 
          value={gauges.temperature} 
          label="Temperature (°C)" 
          min={-20}
          max={50}
        />
        <GaugeChart 
          value={gauges.pressure} 
          label="Pressure (hPa)" 
          color={chartConfig.pressure.color} 
          min={950}
          max={1050}
        />
      </div>
      <TemperatureChart />
    </div>
  )
}
