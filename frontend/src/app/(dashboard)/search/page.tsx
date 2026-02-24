import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function SearchPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Search</h1>
      <Card>
        <CardHeader>
          <CardTitle>Natural Language Search</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Ask questions about your inventory in natural language. The
            AI-powered search will find relevant vehicles and documents.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
