import { redisClient } from "../config/redis";

export const invalidateJudgmentCache = async () => {
  try {
    const filterKey = "judgment:filters";

    // Delete filter cache
    await redisClient.del(filterKey);

    // Delete paginated list caches
    const listKeys = await redisClient.keys("judgments:list:*");

    if (listKeys.length > 0) {
      await redisClient.del(listKeys);
    }

    console.log("🧹 Judgment cache invalidated");
  } catch (error) {
    console.error("❌ Cache invalidation error:", error);
  }
};
