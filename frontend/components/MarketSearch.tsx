'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'

interface MarketSearchProps {
  onIndustrySelect: (industry: string | null) => void
  onCompanySelect: (company: string | null) => void
}

export default function MarketSearch({
  onIndustrySelect,
  onCompanySelect,
}: MarketSearchProps) {
  const [searchType, setSearchType] = useState<'industry' | 'company'>('industry')
  const [searchValue, setSearchValue] = useState('')

  const industries = [
    'Technology',
    'Healthcare',
    'Finance',
    'Retail',
    'Manufacturing',
    'Energy',
    'Education',
    'Real Estate',
    'Fashion',
  ]

  const companies = [
    { name: 'Apple', symbol: 'AAPL' },
    { name: 'Microsoft', symbol: 'MSFT' },
    { name: 'Google', symbol: 'GOOGL' },
    { name: 'Amazon', symbol: 'AMZN' },
    { name: 'Meta', symbol: 'META' },
    { name: 'Tesla', symbol: 'TSLA' },
    { name: 'NVIDIA', symbol: 'NVDA' },
    { name: 'Netflix', symbol: 'NFLX' },
    { name: 'Salesforce', symbol: 'CRM' },
    { name: 'Oracle', symbol: 'ORCL' },
    { name: 'IBM', symbol: 'IBM' },
    { name: 'Intel', symbol: 'INTC' },
    { name: 'Adobe', symbol: 'ADBE' },
    { name: 'PayPal', symbol: 'PYPL' },
    { name: 'Visa', symbol: 'V' },
    { name: 'Mastercard', symbol: 'MA' },
    { name: 'JPMorgan', symbol: 'JPM' },
    { name: 'Bank of America', symbol: 'BAC' },
    { name: 'Walmart', symbol: 'WMT' },
    { name: 'Target', symbol: 'TGT' },
    { name: 'Nike', symbol: 'NKE' },
    { name: 'Starbucks', symbol: 'SBUX' },
  ]

  const handleIndustryChange = (value: string) => {
    setSearchValue(value)
    // Automatically trigger search when industry is selected
    if (value) {
      onIndustrySelect(value)
      onCompanySelect(null)
    } else {
      onIndustrySelect(null)
      onCompanySelect(null)
    }
    // Clear search value when switching to company mode
    if (searchType === 'company') {
      setSearchValue('')
    }
  }

  const handleCompanyChange = (value: string) => {
    setSearchValue(value)
    // Trigger search on Enter key or when value changes significantly
    if (value.trim()) {
      onCompanySelect(value.trim())
      onIndustrySelect(null)
    } else {
      onCompanySelect(null)
      onIndustrySelect(null)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-md p-6 border border-gray-100"
    >
      <div className="flex flex-col md:flex-row gap-4">
        <div className="flex gap-2">
          <button
            onClick={() => {
              setSearchType('industry')
              setSearchValue('')
              onIndustrySelect(null)
              onCompanySelect(null)
            }}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              searchType === 'industry'
                ? 'bg-primary text-white shadow-md'
                : 'bg-gray-100 text-navy-dark hover:bg-gray-200'
            }`}
          >
            Industry
          </button>
          <button
            onClick={() => {
              setSearchType('company')
              setSearchValue('')
              onIndustrySelect(null)
              onCompanySelect(null)
            }}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              searchType === 'company'
                ? 'bg-primary text-white shadow-md'
                : 'bg-gray-100 text-navy-dark hover:bg-gray-200'
            }`}
          >
            Company
          </button>
        </div>

        {searchType === 'industry' ? (
          <select
            value={searchValue}
            onChange={(e) => handleIndustryChange(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-accent"
          >
            <option value="">Select an industry</option>
            {industries.map((industry) => (
              <option key={industry} value={industry}>
                {industry}
              </option>
            ))}
          </select>
        ) : (
          <select
            value={searchValue}
            onChange={(e) => handleCompanyChange(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-accent"
          >
            <option value="">Select a company</option>
            {companies.map((company) => (
              <option key={company.symbol} value={company.name}>
                {company.name} ({company.symbol})
              </option>
            ))}
          </select>
        )}
      </div>
    </motion.div>
  )
}

