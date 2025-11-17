'use client'

import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { api } from '@/lib/api'
import { useEffect, useState } from 'react'

interface KPICardsProps {
  industry: string | null
  company: string | null
}

export default function KPICards({ industry, company }: KPICardsProps) {
  const [kpis, setKPIs] = useState({
    growthRate: 0,
    fundingVolume: 0,
    marketSize: 0,
  })

  const { data: marketData } = useQuery({
    queryKey: ['market', industry, company],
    queryFn: () => api.getMarketData({ industry, company }),
    enabled: !!(industry || company),
  })

  useEffect(() => {
    if (marketData?.metrics) {
      setKPIs({
        growthRate: marketData.metrics.growth_rate || 0,
        fundingVolume: marketData.metrics.funding_volume || 0,
        marketSize: marketData.metrics.market_size || 0,
      })
    } else if (!industry && !company) {
      // Reset KPIs when no selection
      setKPIs({
        growthRate: 0,
        fundingVolume: 0,
        marketSize: 0,
      })
    }
  }, [marketData, industry, company])

  const cards = [
    {
      label: 'Growth Rate',
      value: `${kpis.growthRate.toFixed(1)}%`,
      icon: '📈',
    },
    {
      label: 'Funding Volume',
      value: `$${(kpis.fundingVolume / 1000000).toFixed(1)}M`,
      icon: '💰',
    },
    {
      label: 'Market Size',
      value: `$${(kpis.marketSize / 1000000000).toFixed(1)}B`,
      icon: '🌐',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {cards.map((card, index) => (
        <motion.div
          key={`${card.label}-${industry}-${company}`}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="bg-white rounded-lg shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow"
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-2xl">{card.icon}</span>
            <span className="text-sm text-gray-600">{card.label}</span>
          </div>
          <motion.div
            key={`${card.value}-${industry}-${company}`}
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.3 }}
            className="text-3xl font-bold text-primary"
          >
            {card.value}
          </motion.div>
        </motion.div>
      ))}
    </div>
  )
}

