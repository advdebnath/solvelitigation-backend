import { User } from "../models/user.model";

type UsageKey = "judgments" | "downloads" | "aiRequests";

export async function incrementUsage(
  userId: string,
  key: UsageKey,
  amount = 1
) {
  const update: Record<string, number> = {};
  update[`usage.${key}`] = amount;

  await User.updateOne(
    { _id: userId },
    { $inc: update }
  );
}
