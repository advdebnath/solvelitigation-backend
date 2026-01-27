// src/routes/pricing.routes.ts
import { Router } from "express";

const router = Router();

const plans = [
  {
    id: "simple",
    name: "Simple",
    price: 0,
    features: [
      "View judgments",
      "Basic search",
      "Limited downloads",
    ],
  },
  {
    id: "premium",
    name: "Premium",
    price: 999,
    features: [
      "Unlimited judgments",
      "Advanced search",
      "AI tools",
    ],
  },
];

/**
 * GET /api/pricing
 */
router.get("/", (_req, res) => {
  res.json(plans);
});

/**
 * GET /api/pricing/plans
 */
router.get("/plans", (_req, res) => {
  res.json({ plans });
});

export default router;
