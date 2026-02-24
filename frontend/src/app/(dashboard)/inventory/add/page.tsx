import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

export default function AddVehiclePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Add Vehicle</h1>
      <Card>
        <CardHeader>
          <CardTitle>VIN Lookup</CardTitle>
          <CardDescription>
            Enter a VIN to automatically populate vehicle details from NHTSA.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">VIN lookup form coming soon.</p>
        </CardContent>
      </Card>
    </div>
  )
}
