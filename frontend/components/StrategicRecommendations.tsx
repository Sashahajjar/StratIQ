'use client'

import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { motion } from 'framer-motion'

interface StrategicRecommendationsProps {
  industry: string | null
  company: string | null
}

export default function StrategicRecommendations({
  industry,
  company,
}: StrategicRecommendationsProps) {
  const { data: strategy, isLoading } = useQuery({
    queryKey: ['strategy', 'growth', industry, company],
    queryFn: () => api.getStrategy({ industry, company, analysis_type: 'growth' }),
    enabled: !!(industry || company),
  })

  if (!industry && !company) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-white rounded-lg shadow-md p-6 border border-gray-100"
      >
        <h3 className="text-lg font-semibold mb-4">Strategic Recommendations</h3>
        <div className="text-center text-gray-500 py-8">
          Select an industry or company to view recommendations
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
      <h3 className="text-lg font-semibold mb-4">Strategic Recommendations</h3>
      {isLoading ? (
        <div className="text-center py-8 text-gray-500">Generating recommendations...</div>
      ) : (
        <ul className="space-y-3">
          {(strategy?.recommendations || []).map((rec: string, index: number) => (
            <motion.li
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-start space-x-2 text-sm text-navy-dark"
            >
              <span className="text-accent font-bold mt-1">•</span>
              <span>{rec}</span>
            </motion.li>
          ))}
        </ul>
      )}
    </motion.div>
  )
}

