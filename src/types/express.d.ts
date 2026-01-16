import { PlanType } from "@/types/plan.types";

declare global {
  namespace Express {
    interface Request {
      user?: AuthUser;
      currentUser?: AuthUser;
    }

    interface AuthUser {
      _id: string;
      name: string;
      email: string;
      role: "user" | "admin" | "superadmin";

      plan: PlanType;
      planStatus: "active" | "inactive" | "expired";
      planExpiresAt: Date | null;

      usage: {
        downloads: number;
        aiRequests: number;
        judgmentsViewed: number;
      };

      grace: any;
      isVerified: boolean;
    }
  }
}

export {};
