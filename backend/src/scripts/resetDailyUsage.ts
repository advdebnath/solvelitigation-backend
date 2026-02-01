import mongoose from "mongoose";
import { User } from "@/models/user.model";

const MONGO_URI = process.env.MONGO_URI;

async function resetDailyUsage() {
  if (!MONGO_URI) {
    console.error("❌ MONGO_URI not set");
    process.exit(1);
  }

  await mongoose.connect(MONGO_URI);

  await User.updateMany(
    {},
    {
      $set: {
        "usage.downloads": 0,
        "usage.aiRequests": 0,
        "usage.judgmentsViewed": 0,
        "usageMeta.judgmentsViewedAt": null,
      },
    }
  );

  console.log("✅ Daily usage reset completed");
  await mongoose.disconnect();
}

resetDailyUsage()
  .then(() => process.exit(0))
  .catch((err) => {
    console.error("❌ Daily usage reset failed", err);
    process.exit(1);
  });
