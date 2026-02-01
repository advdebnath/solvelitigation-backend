import { User } from "@/models/user.model";
import { UsageKey } from "@/types/plan.types";

const USAGE_COOLDOWN_MINUTES = 15;

export async function incrementUsage(
  userId: string,
  key: UsageKey
): Promise<void> {
  const user = await User.findById(userId).select("usage usageMeta");

  if (!user) return;

  const now = new Date();

  // Handle judgmentsViewed cooldown
  if (key === "judgmentsViewed") {
    const u = user as any;
  const lastViewed = u.usageMeta?.judgmentsViewedAt;

    if (lastViewed) {
      const diffMinutes =
        (now.getTime() - lastViewed.getTime()) / (1000 * 60);

      if (diffMinutes < USAGE_COOLDOWN_MINUTES) {
        return; // ⛔ Skip increment
      }
    }

    u.usageMeta ??= {};
    u.usageMeta.judgmentsViewedAt = now;
  }

  // Increment usage safely
  user.usage[key] = (user.usage[key] ?? 0) + 1;
  await user.save();
}
