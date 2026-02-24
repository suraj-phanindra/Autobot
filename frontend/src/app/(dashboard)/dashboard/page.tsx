import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Car, FileText, Search, TrendingUp } from 'lucide-react'

export default function DashboardPage() {
  const stats = [
    {
      title: 'Total Vehicles',
      value: '\u2014',
      icon: Car,
      description: 'Active inventory',
    },
    {
      title: 'Documents',
      value: '\u2014',
      icon: FileText,
      description: 'Processed documents',
    },
    {
      title: 'Searches Today',
      value: '\u2014',
      icon: Search,
      description: 'Queries processed',
    },
    {
      title: 'Avg Response Time',
      value: '\u2014',
      icon: TrendingUp,
      description: 'Search latency',
    },
  ]

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.title}
              </CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">
                {stat.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
