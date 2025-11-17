import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const api = {
  // Market data
  getMarketData: async (params: { industry?: string | null; company?: string | null }) => {
    const response = await apiClient.post('/api/market/', {
      industry: params.industry || undefined,
      company: params.company || undefined,
      timeframe: '1y',
    })
    return response.data
  },

  // Insights
  getInsights: async (params: { industry?: string | null; company?: string | null; data?: any }) => {
    const response = await apiClient.post('/api/insights/', {
      industry: params.industry || undefined,
      company: params.company || undefined,
      data: params.data || {},
    })
    return response.data
  },

  // Strategy
  getStrategy: async (params: {
    industry?: string | null
    company?: string | null
    analysis_type: string
  }) => {
    const response = await apiClient.post('/api/strategy/', {
      industry: params.industry || undefined,
      company: params.company || undefined,
      analysis_type: params.analysis_type,
    })
    return response.data
  },

  // Forecast
  getForecast: async (params: {
    metric: string
    data?: any[]
    periods?: number
    industry?: string | null
    company?: string | null
  }) => {
    const response = await apiClient.post('/api/forecast/', {
      metric: params.metric,
      data: params.data || [],
      periods: params.periods || 12,
      industry: params.industry || undefined,
      company: params.company || undefined,
    })
    return response.data
  },
}

