export type UploadCourtType = "SUPREME" | "HIGH" | "TRIBUNAL";

export interface UploadJobPayload {
  auditId: string;
  courtType: UploadCourtType;
  uploadedBy: string;
}
