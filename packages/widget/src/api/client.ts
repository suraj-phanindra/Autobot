export interface QueryResponse {
  answer: string
  vehicles: {
    id: string
    year: number
    make: string
    model: string
    trim?: string
    price?: number
    mileage?: number
    exterior_color?: string
  }[]
  session_id: string
}

export interface WidgetConfig {
  primary_color: string
  logo_url?: string
  greeting: string
  dealership_name: string
}

export function widgetApi(baseUrl: string, apiKey: string) {
  const headers = {
    'Content-Type': 'application/json',
    'X-API-Key': apiKey,
  }

  return {
    async getConfig(): Promise<WidgetConfig> {
      const res = await fetch(`${baseUrl}/widget/config`, { headers })
      if (!res.ok) throw new Error('Failed to fetch widget config')
      return res.json()
    },

    async query(queryText: string, sessionId: string): Promise<QueryResponse> {
      const res = await fetch(`${baseUrl}/widget/query`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          query: queryText,
          session_id: sessionId,
        }),
      })
      if (!res.ok) {
        if (res.status === 429) throw new Error('Rate limit exceeded. Please wait a moment.')
        throw new Error('Failed to send query')
      }
      return res.json()
    },
  }
}
