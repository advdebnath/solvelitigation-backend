import { Router } from "express";

import Judgment from "../models/judgment.model";

const router = Router();

// =====================================================
// 🔥 REVIEW QUEUE
// =====================================================

router.get(

  "/queue",

  async (req: any, res) => {

    try {

      if (

        !req.user ||

        req.user.role !== "superadmin"

      ) {

        return res.status(403).json({

          success: false,

          message: "Unauthorized"
        });
      }

      const data =
        await Judgment.find({

          $or: [

            {
              reviewStatus:
                "PENDING"
            },

            {
              reviewStatus:
                "REVIEW_REQUIRED"
            },

            {
              documentQuality:
                "LOW_QUALITY"
            }
          ]
        })

        .select({

          caseNumber: 1,

          category: 1,

          headnote: 1,

          acts: 1,

          sections: 1,

          documentQuality: 1,

          reviewStatus: 1,

          isPublished: 1,

          createdAt: 1
        })

        .sort({

          createdAt: -1
        })

        .limit(200);

      res.json({

        success: true,

        total:
          data.length,

        data
      });

    } catch (err) {

      console.error(
        "❌ Review Queue Error:",
        err
      );

      res.status(500).json({

        success: false,

        message:
          "Failed to fetch review queue"
      });
    }
  }
);

// =====================================================
// 🔥 APPROVE JUDGMENT
// =====================================================

router.post(

  "/approve/:id",

  async (req: any, res) => {

    try {

      if (

        !req.user ||

        req.user.role !== "superadmin"

      ) {

        return res.status(403).json({

          success: false
        });
      }

      await Judgment.findByIdAndUpdate(

        req.params.id,

        {

          reviewStatus:
            "APPROVED",

          documentQuality:
            "HIGH_QUALITY",

          isPublished:
            true,

          reviewedBy:
            req.user._id,

          reviewedAt:
            new Date()
        }
      );

      res.json({

        success: true
      });

    } catch (err) {

      console.error(
        "❌ Approve Error:",
        err
      );

      res.status(500).json({

        success: false
      });
    }
  }
);

// =====================================================
// 🔥 REJECT JUDGMENT
// =====================================================

router.post(

  "/reject/:id",

  async (req: any, res) => {

    try {

      if (

        !req.user ||

        req.user.role !== "superadmin"

      ) {

        return res.status(403).json({

          success: false
        });
      }

      await Judgment.findByIdAndUpdate(

        req.params.id,

        {

          reviewStatus:
            "REJECTED",

          documentQuality:
            "REJECTED",

          isPublished:
            false,

          reviewedBy:
            req.user._id,

          reviewedAt:
            new Date()
        }
      );

      res.json({

        success: true
      });

    } catch (err) {

      console.error(
        "❌ Reject Error:",
        err
      );

      res.status(500).json({

        success: false
      });
    }
  }
);

export default router;
