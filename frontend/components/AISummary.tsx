'use client'

import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { motion } from 'framer-motion'

interface AISummaryProps {
  industry: string | null
  company: string | null
}

export default function AISummary({ industry, company }: AISummaryProps) {
  // First fetch market data to get metrics
  const { data: marketData } = useQuery({
    queryKey: ['market', industry, company],
    queryFn: () => api.getMarketData({ industry, company }),
    enabled: !!(industry || company),
  })

  // Then fetch insights with the actual metrics
  const { data: insights, isLoading } = useQuery({
    queryKey: ['insights', industry, company, marketData?.metrics],
    queryFn: () => api.getInsights({ 
      industry, 
      company, 
      data: marketData?.metrics || {} 
    }),
    enabled: !!(industry || company) && !!marketData,
  })

  if (!industry && !company) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-white rounded-lg shadow-md p-6 border border-gray-100"
      >
        <h3 className="text-lg font-semibold mb-4">Key Insights</h3>
        <div className="text-center text-gray-500 py-8">
          Select an industry or company to generate insights
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-sm p-6"
    >
      <h3 className="text-lg font-semibold mb-4">Key Insights</h3>
      {isLoading ? (
        <div className="text-center py-8 text-gray-500">Generating insights...</div>
      ) : (
        <div className="space-y-4">
            <p className="text-sm text-navy-dark leading-relaxed">
            {insights?.summary || 'No insights available'}
          </p>
          {insights?.key_takeaways && insights.key_takeaways.length > 0 && (
            <div className="mt-4">
              <h4 className="text-sm font-semibold mb-2">Key Takeaways:</h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-navy-dark">
                {insights.key_takeaways.map((takeaway: string, index: number) => (
                  <li key={index}>{takeaway}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </motion.div>
  )
}

