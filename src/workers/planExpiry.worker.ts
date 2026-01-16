import { handleExpiredPlans } from "@/services/planExpiry.service";

/**
 * Runs plan expiry check
 * Intended to be triggered periodically
 */
export async function planExpiryWorker(): Promise<void> {
  try {
    console.log("[PLAN-EXPIRY] Worker started");

    await handleExpiredPlans();

    console.log("[PLAN-EXPIRY] Worker completed");
  } catch (error) {
    console.error("[PLAN-EXPIRY] Worker failed:", error);
  }
}
