import { Request, Response } from "express";

/**
 * GET /api/judgments
 * Public (paid users)
 */
export async function listJudgments(req: Request, res: Response) {
  try {
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

    res.json({ success: true, data });
  } catch (err) {
    res.status(500).json({ success: false });
  }
}
