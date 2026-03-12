import { UploadZone } from "@/components/documents/UploadZone";
import { DocList } from "@/components/documents/DocList";

export default function DocumentsPage() {
  return (
    <div className="flex flex-col gap-6 p-6">
      <h1 className="text-2xl font-semibold">Documents</h1>
      <UploadZone />
      <DocList />
    </div>
  );
}
