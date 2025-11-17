'use client'

import { motion } from 'framer-motion'

export default function MetricsDefinitions() {
  const definitions = [
    {
      term: 'Growth Rate',
      definition: 'The annual percentage increase in market value, revenue, or market size for the industry or company.',
    },
    {
      term: 'Funding Volume',
      definition: 'Total amount of capital invested (in millions) through venture capital, private equity, or other funding sources.',
    },
    {
      term: 'Market Size',
      definition: 'The total addressable market value (in billions) representing the potential revenue opportunity for the industry.',
    },
    {
      term: 'Trend Analysis',
      definition: 'A 12-month forecast showing projected growth trajectory based on historical patterns and market data.',
    },
  ]

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-accent/5 rounded-lg shadow-md p-4 border border-accent/20"
    >
      <h4 className="text-sm font-semibold text-primary mb-3 flex items-center gap-2">
        <span className="text-accent">ℹ️</span>
        Metrics Definitions
      </h4>
      <div className="space-y-2">
        {definitions.map((item, index) => (
          <div key={index} className="text-xs">
            <span className="font-semibold text-navy-dark">{item.term}:</span>
            <span className="text-gray-600 ml-1">{item.definition}</span>
          </div>
        ))}
      </div>
    </motion.div>
  )
}


