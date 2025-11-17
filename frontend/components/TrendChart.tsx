'use client'

import { useQuery } from '@tanstack/react-query'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { api } from '@/lib/api'
import { motion } from 'framer-motion'

interface TrendChartProps {
  industry: string | null
  company: string | null
}

export default function TrendChart({ industry, company }: TrendChartProps) {
  const { data: forecastData, isLoading } = useQuery({
    queryKey: ['forecast', industry, company],
    queryFn: async () => {
      // Fetch real forecast data from API
      if (!industry && !company) return []
      
      try {
        const forecast = await api.getForecast({
          metric: 'growth',
          data: [],
          periods: 12,
          industry: industry || undefined,
          company: company || undefined,
        })
        
        // Transform forecast data for chart
        return forecast.forecast?.slice(0, 12).map((item: any, index: number) => ({
          month: index + 1,
          value: item.yhat || item.value || 0,
        })) || []
      } catch (error) {
        console.error('Error fetching forecast:', error)
        return []
      }
    },
    enabled: !!(industry || company),
  })

  if (!industry && !company) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-white rounded-lg shadow-md p-6 border border-gray-100"
      >
        <h3 className="text-lg font-semibold mb-4">Trend Analysis</h3>
        <div className="text-center text-gray-500 py-12">
          Select an industry or company to view trends
        </div>
      </motion.div>
    )
  }

  // Determine Y-axis label based on company vs industry
  const yAxisLabel = company ? 'Stock Price ($)' : 'Growth Index'

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-md p-6 border border-gray-100"
    >
      <h3 className="text-lg font-semibold mb-4">Trend Analysis</h3>
      {isLoading ? (
        <div className="text-center py-12 text-gray-500">Loading chart...</div>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={forecastData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="month" 
              label={{ value: 'Month', position: 'insideBottom', offset: -5, style: { textAnchor: 'middle' } }}
            />
            <YAxis 
              label={{ value: yAxisLabel, angle: -90, position: 'insideLeft', style: { textAnchor: 'middle' } }}
            />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="value"
              stroke="#1C8B3E"
              strokeWidth={2}
              dot={{ fill: '#1C8B3E', r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </motion.div>
  )
}

