import { Upload } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function DocumentsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Documents</h1>
        <Button>
          <Upload className="mr-2 h-4 w-4" />
          Upload
        </Button>
      </div>
      <div className="rounded-lg border bg-card p-12 text-center">
        <p className="text-muted-foreground">
          No documents uploaded yet. Upload Carfax reports, spec sheets, or
          dealer notes.
        </p>
      </div>
    </div>
  )
}
