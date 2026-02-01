import { planExpiryWorker } from "@/workers";

/**
 * Job entry for plan expiry
 */
export async function planExpiryJob(): Promise<void> {
  await planExpiryWorker();
}
