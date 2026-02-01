import { Request, Response } from "express";
import { incrementUsage } from "../../utils/incrementUsage";

/**
 * GET /api/judgments
 * Paid users – counts toward plan usage
 */
export async function listJudgments(req: Request, res: Response) {
  try {
    // Safety check (should already be ensured by authenticateJWT)
    if (!req.currentUser) {
      return res.status(401).json({ success: false });
    }

    // TEMP: replace with DB query later
    const data = [
      {
        id: "1",
        title: "Termination of Contract – Specific Relief Act",
        pol: "Termination of Contract",
        court: "Supreme Court",
        year: 2023,
        summary:
          "Termination must be lawful and comply with statutory requirements.",
      },
      {
        id: "2",
        title: "Specific Performance – Readiness & Willingness",
        pol: "Specific Performance",
        court: "Delhi High Court",
        year: 2022,
        summary:
          "Continuous readiness and willingness is mandatory for relief.",
      },
    ];

    // ✅ Increment usage ONCE per successful request
    await incrementUsage(req.currentUser._id, "judgmentsViewed");

    return res.json({
      success: true,
      data,
    });
  } catch (error) {
    console.error("[LIST JUDGMENTS]", error);
    return res.status(500).json({
      success: false,
      message: "Failed to fetch judgments",
    });
  }
}
