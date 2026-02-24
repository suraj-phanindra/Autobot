import { useMutation } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'
import type { SearchRequest, SearchResponse } from '@/lib/types'

export function useSearch() {
  return useMutation({
    mutationFn: (data: SearchRequest) =>
      apiClient.post<SearchResponse>('/search', data),
  })
}
