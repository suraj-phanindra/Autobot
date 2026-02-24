import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

export default async function VehicleDetailPage({
  params,
}: {
  params: Promise<{ vehicleId: string }>
}) {
  const { vehicleId } = await params

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Vehicle Details</h1>
      <p className="text-muted-foreground">Vehicle ID: {vehicleId}</p>
      <Tabs defaultValue="specs">
        <TabsList>
          <TabsTrigger value="specs">Specs</TabsTrigger>
          <TabsTrigger value="history">History</TabsTrigger>
          <TabsTrigger value="documents">Documents</TabsTrigger>
          <TabsTrigger value="activity">Activity</TabsTrigger>
        </TabsList>
        <TabsContent value="specs" className="rounded-lg border bg-card p-6">
          <p className="text-muted-foreground">
            Vehicle specifications will appear here.
          </p>
        </TabsContent>
        <TabsContent
          value="history"
          className="rounded-lg border bg-card p-6"
        >
          <p className="text-muted-foreground">
            Vehicle history will appear here.
          </p>
        </TabsContent>
        <TabsContent
          value="documents"
          className="rounded-lg border bg-card p-6"
        >
          <p className="text-muted-foreground">
            Associated documents will appear here.
          </p>
        </TabsContent>
        <TabsContent
          value="activity"
          className="rounded-lg border bg-card p-6"
        >
          <p className="text-muted-foreground">
            Search activity will appear here.
          </p>
        </TabsContent>
      </Tabs>
    </div>
  )
}
