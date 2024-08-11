'use client'

import * as React from "react"
import { Line, LineChart, CartesianGrid, XAxis, YAxis } from "recharts"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartConfig,
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import  DateTimePickerDemo  from "@/components/ui/date-picker"

const generateTemperatureData = (startDate: Date, days: number) => {
  const data = [];
  const endDate = new Date(startDate.getTime() + days * 24 * 60 * 60 * 1000);
  for (let currentDate = new Date(startDate); currentDate < endDate; currentDate.setSeconds(currentDate.getSeconds() + 5)) {
    data.push({
      date: currentDate.toISOString(),
      temperature: Math.round((Math.random() * 15 + 15) * 10) / 10,
    });
  }
  return data;
};

const chartData = generateTemperatureData(new Date('2024-08-11'), 1);

const chartConfig = {
  min: {
    label: "Min Temperature",
    color: "hsl(var(--chart-1))",
    gradient: "url(#gradientMin)",
  },
  max: {
    label: "Max Temperature",
    color: "hsl(var(--chart-2))",
    gradient: "url(#gradientMax)",
  },
  average: {
    label: "Average Temperature",
    color: "hsl(var(--chart-3))",
    gradient: "url(#gradientAvg)",
  },
} satisfies ChartConfig


export function TemperatureChart() {
  const [fromDate, setFromDate] = React.useState<Date>(() => {
    const date = new Date();
    date.setHours(date.getHours() - 24);
    return date;
  });
  const [toDate, setToDate] = React.useState<Date>(new Date());
  const [timeRange, setTimeRange] = React.useState("hourly");
  const [displayData, setDisplayData] = React.useState(chartData);
  const [minTemperature, setMinTemperature] = React.useState(-20);
  const [maxTemperature, setMaxTemperature] = React.useState(50);

  React.useEffect(() => {
    const intervalMap = {
      "1m": 60 * 1000,
      "5m": 5 * 60 * 1000,
      "15m": 15 * 60 * 1000,
      "30m": 30 * 60 * 1000,
      "hourly": 60 * 60 * 1000,
      "daily": 24 * 60 * 60 * 1000,
      "weekly": 7 * 24 * 60 * 60 * 1000,
      "monthly": 30 * 24 * 60 * 60 * 1000,
    };
    const interval = intervalMap[timeRange];
    
    let filteredData = chartData;
    const extendedFromDate = fromDate ? new Date(fromDate.getTime() - interval) : null;
    
    if (extendedFromDate && toDate) {
      filteredData = filteredData.filter(item => {
        const itemDate = new Date(item.date);
        return itemDate >= extendedFromDate && itemDate <= toDate;
      });
    } else if (extendedFromDate) {
      filteredData = filteredData.filter(item => {
        const itemDate = new Date(item.date);
        return itemDate >= extendedFromDate;
      });
    } else if (toDate) {
      filteredData = filteredData.filter(item => {
        const itemDate = new Date(item.date);
        return itemDate <= toDate;
      });
    }
    
    if (timeRange) {
      console.log(filteredData);
      
      const filteredStart = new Date(filteredData[0].date).getTime();
      const filteredEnd = new Date(filteredData[filteredData.length - 1].date).getTime();

      const extendedStart = new Date(filteredStart - interval);
      const aggregatedData = {};
      
      filteredData.forEach(item => {
        const date = new Date(item.date);
        const intervalKey = Math.floor((date.getTime() - extendedStart.getTime()) / interval) * interval + extendedStart.getTime();
        const displayDate = new Date(intervalKey + interval);

        if (!aggregatedData[intervalKey]) {
          aggregatedData[intervalKey] = { 
            date: displayDate, 
            min: Infinity, 
            max: -Infinity, 
            sum: 0, 
            count: 0 
          };
        }
        aggregatedData[intervalKey].min = Math.min(aggregatedData[intervalKey].min, item.temperature);
        aggregatedData[intervalKey].max = Math.max(aggregatedData[intervalKey].max, item.temperature);
        aggregatedData[intervalKey].sum += item.temperature;
        aggregatedData[intervalKey].count++;
      });
      
      filteredData = Object.values(aggregatedData).map(item => ({
        date: item.date,
        min: item.min,
        max: item.max,
        average: item.sum / item.count
      }));
      
      
    }

    const calculatedMinTemp = Math.floor(Math.min(...filteredData.map(item => 
      Math.min(item.min, item.max, item.average)
    ))) - 2.5;
    
    const calculatedMaxTemp = Math.ceil(Math.max(...filteredData.map(item =>
      Math.max(item.min, item.max, item.average)
    ))) + 2.5;

    console.log( filteredData)
    setMinTemperature(calculatedMinTemp);
    setMaxTemperature(calculatedMaxTemp);
    setDisplayData(filteredData);
  }, [fromDate, toDate, timeRange]);

  return (
    <Card>
      <CardHeader className="flex items-center gap-2 space-y-0 border-b py-5 lg:flex-row">
        <div className="grid flex-1 gap-1 text-center lg:text-left">
          <CardTitle>Temperature Chart - Interactive</CardTitle>
          <CardDescription>
            Showing temperature data for the selected period
          </CardDescription>
        </div>
        <div className="flex flex-col space-y-2 sm:flex-row sm:space-y-0 sm:space-x-2">
            <div className="w-full sm:w-auto">
              <DateTimePickerDemo
                date={fromDate}
                onDateChange={setFromDate}
                placeholder="From"
              />
            </div>
            <div className="w-full sm:w-auto">
              <DateTimePickerDemo
                date={toDate}
                onDateChange={setToDate}
                placeholder="  To"
              />
            </div>
          </div>

        <Select value={timeRange} onValueChange={setTimeRange}>
          <SelectTrigger
            className="w-[160px] rounded-lg lg:ml-auto"
            aria-label="Select a value"
          >
            <SelectValue placeholder="Select Interval" />
          </SelectTrigger>
          <SelectContent className="rounded-xl">
            <SelectItem value="1m" className="rounded-lg">1 Min</SelectItem>
            <SelectItem value="5m" className="rounded-lg">5 Mins</SelectItem>
            <SelectItem value="15m" className="rounded-lg">15 Mins</SelectItem>
            <SelectItem value="30m" className="rounded-lg">30 Mins</SelectItem>
            <SelectItem value="hourly" className="rounded-lg">Hourly</SelectItem>
            <SelectItem value="daily" className="rounded-lg">Daily</SelectItem>
            <SelectItem value="weekly" className="rounded-lg">Weekly</SelectItem>
            <SelectItem value="monthly" className="rounded-lg">Monthly</SelectItem>
          </SelectContent>
        </Select>
      </CardHeader>
      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <ChartContainer
          config={chartConfig}
          className="aspect-auto h-[250px] w-full"
        >
          <LineChart data={displayData}>
          <defs>
              <linearGradient id="gradientMin" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={chartConfig.min.color} stopOpacity={0.8}/>
                <stop offset="95%" stopColor={chartConfig.min.color} stopOpacity={0.1}/>
              </linearGradient>
              <linearGradient id="gradientMax" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={chartConfig.max.color} stopOpacity={0.8}/>
                <stop offset="95%" stopColor={chartConfig.max.color} stopOpacity={0.1}/>
              </linearGradient>
              <linearGradient id="gradientAvg" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={chartConfig.average.color} stopOpacity={0.8}/>
                <stop offset="95%" stopColor={chartConfig.average.color} stopOpacity={0.1}/>
              </linearGradient>
            </defs>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              minTickGap={32}
              tickFormatter={(value) => {
              
                const date = new Date(value);
                if (timeRange === "hourly" || timeRange === "5m") {
                  const spanMultipleDays = (toDate.getTime() - fromDate.getTime()) > 86400000;
                  if (spanMultipleDays) {
                    return date.toLocaleString("en-GB", {
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                      hour12: false
                    });
                  }
                  return date.toLocaleString("en-GB", {
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: false
                  });
                }
                return date.toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                });
              }}
            />
<YAxis 
  domain={[minTemperature, maxTemperature]}
  tickLine={false}
  axisLine={false}
  tickMargin={8}
  tickFormatter={(value) => `${value}°C`}
/>
<ChartTooltip
  content={({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const date = new Date(label);
      return (
        <div className="bg-gray-800 border border-gray-700 rounded-lg shadow-lg p-4">
          <p className="font-bold text-gray-200 mb-2">
            {date.toLocaleString("en-GB", {
              year: 'numeric',
              month: 'short',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit',
              hour12: false
            })}
          </p>
          {payload.map((entry, index) => (
            <div key={index} className="flex justify-between items-center mb-1">
              <span className="font-medium text-gray-300" style={{ color: entry.color }}>
                {entry.name}:
              </span>
              <span className="font-semibold text-gray-100">
                {`${entry.value.toFixed(1)}°C`}
              </span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  }}
/>


                       <Line
              type="monotone"
              dataKey="min"
              stroke={chartConfig.min.color}
              strokeWidth={2}
              dot={false}
              fill={chartConfig.min.gradient}
            />
            <Line
              type="monotone"
              dataKey="max"
              stroke={chartConfig.max.color}
              strokeWidth={2}
              dot={false}
              fill={chartConfig.max.gradient}
            />
            <Line
              type="monotone"
              dataKey="average"
              stroke={chartConfig.average.color}
              strokeWidth={2}
              dot={false}
              fill={chartConfig.average.gradient}
            />
            <ChartLegend content={<ChartLegendContent />} />
          </LineChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
