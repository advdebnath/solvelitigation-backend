import { PlanType, UsageKey } from "@/types/plan.types";

export const PLAN_LIMITS: Record<
  PlanType,
  {
    downloads: number;
    aiRequests: number;
    judgmentsViewed: number;
    grace: number;
  }
> = {
  free: {
    downloads: 5,
    aiRequests: 3,
    judgmentsViewed: 20,
    grace: 0,
  },
  simple: {
    downloads: 50,
    aiRequests: 30,
    judgmentsViewed: 200,
    grace: 5,
  },
  premium: {
    downloads: 500,
    aiRequests: 300,
    judgmentsViewed: 2000,
    grace: 20,
  },

enterprise: {
    downloads: 999999,
    aiRequests: 999999,
    judgmentsViewed: 999999,
    grace: 999999,
  },
};

