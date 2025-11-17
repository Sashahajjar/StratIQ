'use client'

import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { motion } from 'framer-motion'

interface SWOTMatrixProps {
  industry: string | null
  company: string | null
}

export default function SWOTMatrix({ industry, company }: SWOTMatrixProps) {
  const { data: strategy, isLoading } = useQuery({
    queryKey: ['strategy', 'swot', industry, company],
    queryFn: () => api.getStrategy({ industry, company, analysis_type: 'swot' }),
    enabled: !!(industry || company),
  })

  if (!industry && !company) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-white rounded-lg shadow-md p-6 border border-gray-100"
      >
        <h3 className="text-lg font-semibold mb-4">SWOT Analysis</h3>
        <div className="text-center text-gray-500 py-12">
          Select an industry or company to generate SWOT analysis
        </div>
      </motion.div>
    )
  }

  const swotData = strategy?.content || {}

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-sm p-6"
    >
      <h3 className="text-lg font-semibold mb-4">SWOT Analysis</h3>
      {isLoading ? (
        <div className="text-center py-12 text-gray-500">Generating SWOT...</div>
      ) : (
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 bg-accent/10 rounded-lg border border-accent/20">
            <h4 className="font-semibold text-accent mb-2">Strengths</h4>
            <ul className="list-disc list-inside text-sm text-navy-dark space-y-1">
              {(swotData.strengths || []).map((item: string, index: number) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>
          <div className="p-4 bg-red-50/50 rounded-lg border border-red-200/30">
            <h4 className="font-semibold text-red-700 mb-2">Weaknesses</h4>
            <ul className="list-disc list-inside text-sm text-navy-dark space-y-1">
              {(swotData.weaknesses || []).map((item: string, index: number) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>
          <div className="p-4 bg-green-light/10 rounded-lg border border-green-light/20">
            <h4 className="font-semibold text-green-dark mb-2">Opportunities</h4>
            <ul className="list-disc list-inside text-sm text-navy-dark space-y-1">
              {(swotData.opportunities || []).map((item: string, index: number) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>
          <div className="p-4 bg-orange-50/50 rounded-lg border border-orange-200/30">
            <h4 className="font-semibold text-orange-700 mb-2">Threats</h4>
            <ul className="list-disc list-inside text-sm text-navy-dark space-y-1">
              {(swotData.threats || []).map((item: string, index: number) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </motion.div>
  )
}

