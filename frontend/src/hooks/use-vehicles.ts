import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'
import type {
  Vehicle,
  VehicleCreate,
  VehicleUpdate,
  PaginatedResponse,
} from '@/lib/types'

interface VehicleListParams {
  page?: number
  page_size?: number
  make?: string
  model?: string
  year?: number
  status?: string
}

export function useVehicles(params: VehicleListParams = {}) {
  return useQuery({
    queryKey: ['vehicles', params],
    queryFn: () =>
      apiClient.get<PaginatedResponse<Vehicle>>('/vehicles', {
        params: params as Record<
          string,
          string | number | boolean | undefined
        >,
      }),
  })
}

export function useVehicle(id: string) {
  return useQuery({
    queryKey: ['vehicles', id],
    queryFn: () => apiClient.get<Vehicle>(`/vehicles/${id}`),
    enabled: !!id,
  })
}

export function useCreateVehicle() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: VehicleCreate) =>
      apiClient.post<Vehicle>('/vehicles', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vehicles'] })
    },
  })
}

export function useUpdateVehicle() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: VehicleUpdate }) =>
      apiClient.patch<Vehicle>(`/vehicles/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vehicles'] })
    },
  })
}

export function useDeleteVehicle() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => apiClient.delete(`/vehicles/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vehicles'] })
    },
  })
}

export function useDecodeVin() {
  return useMutation({
    mutationFn: (vin: string) =>
      apiClient.post<Vehicle>('/vehicles/decode-vin', { vin }),
  })
}
