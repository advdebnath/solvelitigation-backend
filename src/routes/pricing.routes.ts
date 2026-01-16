import { Router } from "express";
import { authenticateJWT } from "@/middlewares/auth.middleware";
import { User } from "@/models/user.model";

const router = Router();

const plans = [
  {
    id: "simple",
    planCode: "simple",
    name: "Simple",
    price: 499,
    currency: "INR",
    interval: "monthly",
    features: ["Judgment search", "Basic filters", "Limited downloads"],
  },
  {
    id: "premium",
    planCode: "premium",
    name: "Premium",
    price: 999,
    currency: "INR",
    interval: "monthly",
    features: [
      "Unlimited judgment search",
      "Advanced filters",
      "AI-generated headnotes",
      "Unlimited downloads",
    ],
  },
];

router.get("/", (_req, res) => {
  res.json({ success: true, data: plans });
});

router.post("/upgrade", authenticateJWT, async (req, res) => {
  try {
    if (!res.locals.userId) {
      return res.status(401).json({ success: false, message: "Unauthorized" });
    }

    const { planCode } = req.body;

    if (!["simple", "premium"].includes(planCode)) {
      return res.status(400).json({
        success: false,
        message: "Invalid plan code",
      });
    }

    const user = await User.findById(res.locals.userId);

    if (!user) {
      return res.status(404).json({
        success: false,
        message: "User not found",
      });
    }

    if (user.plan === planCode) {
      return res.status(400).json({
        success: false,
        message: "Already on this plan",
      });
    }

    user.plan = planCode;
    user.planStatus = "active";
    user.planStartedAt = new Date();

    await user.save();

    res.json({
      success: true,
      message: `Upgraded to ${planCode}`,
      plan: planCode,
    });
  } catch (err) {
    console.error("[PRICING]", err);
    res.status(500).json({
      success: false,
      message: "Upgrade failed",
    });
  }
});

export default router;
