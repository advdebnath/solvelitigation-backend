const { MongoClient } = require("mongodb");

(async () => {
  const client = new MongoClient("mongodb://127.0.0.1:27017");

  try {
    await client.connect();
    const db = client.db("solvelitigation");

    const THIRTY_DAYS = 30 * 24 * 60 * 60 * 1000;
    const now = new Date();

    /* ===============================
       1️⃣ Expire old subscriptions
       =============================== */
    const expireResult = await db.collection("subscriptions").updateMany(
      {
        status: "active",
        startedAt: { $lte: new Date(now.getTime() - THIRTY_DAYS) }
      },
      {
        $set: {
          status: "expired",
          endedAt: now
        }
      }
    );

    /* ===============================
       2️⃣ Find active subscribers
       =============================== */
    const activeUserIds = await db
      .collection("subscriptions")
      .distinct("userId", { status: "active" });

    /* ===============================
       3️⃣ Downgrade users
       =============================== */
    const downgradeResult = await db.collection("users").updateMany(
      {
        planStatus: "active",
        _id: { $nin: activeUserIds }
      },
      {
        $set: {
          planStatus: "expired",
          plan: "free"
        }
      }
    );

    console.log("✅ Subscription expiry job completed");
    console.log("Expired subscriptions:", expireResult.modifiedCount);
    console.log("Downgraded users:", downgradeResult.modifiedCount);

  } catch (err) {
    console.error("❌ Subscription expiry job failed", err);
  } finally {
    await client.close();
  }
})();
