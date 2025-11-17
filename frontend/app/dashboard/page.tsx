'use client'

import { useState } from 'react'
import Navigation from '@/components/Navigation'
import KPICards from '@/components/KPICards'
import TrendChart from '@/components/TrendChart'
import AISummary from '@/components/AISummary'
import SWOTMatrix from '@/components/SWOTMatrix'
import StrategicRecommendations from '@/components/StrategicRecommendations'
import MarketSearch from '@/components/MarketSearch'
import MetricsDefinitions from '@/components/MetricsDefinitions'

export default function DashboardPage() {
  const [selectedIndustry, setSelectedIndustry] = useState<string | null>(null)
  const [selectedCompany, setSelectedCompany] = useState<string | null>(null)

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-primary mb-2">
            Business Intelligence Dashboard
          </h1>
          <p className="text-navy-light">
            Analyze markets, detect opportunities, and generate strategic insights
          </p>
        </div>

        <MarketSearch
          onIndustrySelect={setSelectedIndustry}
          onCompanySelect={setSelectedCompany}
        />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
          <div className="lg:col-span-2 space-y-6">
            <KPICards
              key={`kpi-${selectedIndustry}-${selectedCompany}`}
              industry={selectedIndustry}
              company={selectedCompany}
            />
            <TrendChart
              key={`trend-${selectedIndustry}-${selectedCompany}`}
              industry={selectedIndustry}
              company={selectedCompany}
            />
            <SWOTMatrix
              key={`swot-${selectedIndustry}-${selectedCompany}`}
              industry={selectedIndustry}
              company={selectedCompany}
            />
          </div>

          <div className="space-y-6">
            <MetricsDefinitions />
            <AISummary
              key={`ai-${selectedIndustry}-${selectedCompany}`}
              industry={selectedIndustry}
              company={selectedCompany}
            />
            <StrategicRecommendations
              key={`rec-${selectedIndustry}-${selectedCompany}`}
              industry={selectedIndustry}
              company={selectedCompany}
            />
          </div>
        </div>
      </main>
    </div>
  )
}

