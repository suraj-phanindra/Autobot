import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Analytics</h1>
      <Card>
        <CardHeader>
          <CardTitle>Search Analytics</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Query volume, popular searches, and response time charts will appear
            here.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
