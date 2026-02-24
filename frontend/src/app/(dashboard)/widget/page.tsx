import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

export default function WidgetPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Widget</h1>
      <Card>
        <CardHeader>
          <CardTitle>Embeddable Chat Widget</CardTitle>
          <CardDescription>
            Add the AutoBot chat widget to your dealership website with a single
            script tag.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Widget customization and install code coming soon.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
