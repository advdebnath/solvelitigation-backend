export type PlanType = "free" | "simple" | "premium";
export type PlanStatus = "active" | "expired" | "inactive";

export interface IUser {
  _id: string;
  name: string;
  email: string;
  role: "user" | "admin" | "superadmin";

  plan: PlanType;
  planStatus: PlanStatus;
  planExpiresAt: Date | null;

  usage: {
    downloads: number;
    aiRequests: number;
    judgmentsViewed: number;
  };

  grace: {
    downloads: number;
    aiRequests: number;
    judgmentsViewed: number;
  };

  isVerified: boolean;
  isDeleted: boolean;
}
