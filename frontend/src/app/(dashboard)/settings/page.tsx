import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Settings</h1>
      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Dealership Profile</CardTitle>
            <CardDescription>
              Manage your dealership information and branding.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Profile settings coming soon.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>API Keys</CardTitle>
            <CardDescription>
              Manage API keys for your widget integrations.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              API key management coming soon.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
