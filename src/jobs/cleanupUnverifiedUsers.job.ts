import cron from "node-cron";
import { User } from "@/models/user.model";

/**
 * 🧹 Cleanup unverified users (SOFT DELETE)
 * Runs every day at 03:00 AM
 */
export const startCleanupUnverifiedUsersJob = () => {
  cron.schedule("0 3 * * *", async () => {
    try {
      const result = await User.updateMany(
        {
          isVerified: false,
          isDeleted: false,
          createdAt: { $lte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) },
        },
        {
          $set: {
            isDeleted: true,
            planStatus: "expired",
          },
        }
      );

      console.log(
        `[CRON] Cleanup unverified users → ${result.modifiedCount} users soft-deleted`
      );
    } catch (err) {
      console.error("[CRON] Cleanup failed:", err);
    }
  });

  console.log("[CRON] Cleanup unverified users job scheduled");
};
