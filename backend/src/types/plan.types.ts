/**
 * Plan & Usage Types — single source of truth
 */

export type PlanType = "free" | "simple" | "premium" | "enterprise";

export type UsageKey =
  | "downloads"
  | "aiRequests"
  | "judgmentsViewed";

export interface UsageCounter {
  downloads: number;
  aiRequests: number;
  judgmentsViewed: number;
  lastViewedAt?: Date;
}

export interface GraceCounter {
  downloads: number;
  aiRequests: number;
  judgmentsViewed: number;
}
