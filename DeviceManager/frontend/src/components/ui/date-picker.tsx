import { useState } from "react"
import { Calendar as CalendarIcon, Clock } from "lucide-react"
import { format } from "date-fns"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import  TimePicker  from "@/components/ui/time-picker"

export default function DateTimePickerDemo({
  text,
  date,
  onDateChange,
  placeholder = "Pick date and time",
}) {
  const [tempDate, setTempDate] = useState(date)
  const [tempTime, setTempTime] = useState(date ? format(date, "HH:mm") : "00:00")

  const handleDateChange = (newDate) => {
    setTempDate(newDate)
  }

  const handleTimeChange = (newTime) => {
    setTempTime(newTime)
  }

  const handleOkClick = () => {
    if (tempDate) {
      const [hours, minutes] = tempTime.split(':')
      const newDateTime = new Date(tempDate)
      newDateTime.setHours(parseInt(hours, 10), parseInt(minutes, 10))
      onDateChange(newDateTime)
    }
  }

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant={"outline"}
          className={cn(
            "w-[280px] justify-between text-left font-normal",
            !date && "text-muted-foreground"
          )}
        >
          
          <CalendarIcon className="mr-2 h-4 w-4" />
          {date ?<span>{placeholder}: {format(date, "PPP HH:mm")}</span> : <span>{placeholder}</span>}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0">
        <Calendar
          mode="single"
          selected={tempDate}
          onSelect={handleDateChange}
          initialFocus
        />
      <div className="p-3 border-t flex justify-between items-center">
        <TimePicker value={tempTime} onChange={handleTimeChange} />
        <Button onClick={handleOkClick}>Set</Button>
      </div>

      </PopoverContent>
    </Popover>
  )
}
