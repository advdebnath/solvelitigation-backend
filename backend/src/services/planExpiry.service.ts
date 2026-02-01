import { User } from "../models/user.model";

/**
 * Downgrade expired plans to FREE
 */
export async function handleExpiredPlans(): Promise<void> {
  const now = new Date();

  const expiredUsers = await User.find({
    plan: { $ne: "free" },
    planStatus: "active",
    planExpiresAt: { $lt: now },
    isDeleted: false,
  }).select("_id plan planExpiresAt");

  if (expiredUsers.length === 0) {
    return;
  }

  const userIds = expiredUsers.map((u) => u._id);

  await User.updateMany(
    { _id: { $in: userIds } },
    {
      $set: {
        plan: "free",
        planStatus: "expired",
        planExpiresAt: null,
        usage: {
          downloads: 0,
          aiRequests: 0,
          judgmentsViewed: 0,
        },
        grace: {
          downloads: 0,
          aiRequests: 0,
          judgmentsViewed: 0,
        },
      },
    }
  );

  console.log(
    `[PLAN-EXPIRY] Downgraded ${userIds.length} expired users to FREE`
  );
}
