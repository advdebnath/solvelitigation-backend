import { Router } from "express";
import {
  listUsers,
  blockUser,
  unblockUser,
  verifyUser,
  updateUserRole,
} from "../../controllers/superadmin/users.controller";

import {
  authenticateJWT,
  requireSuperAdmin,
} from "../../middlewares/auth.middleware";

const router = Router();

// 🔐 Superadmin-only protection
router.use(authenticateJWT, requireSuperAdmin);

// 👥 User management
router.get("/", listUsers);
router.patch("/:id/block", blockUser);
router.patch("/:id/unblock", unblockUser);
router.patch("/:id/verify", verifyUser);
router.patch("/:id/role", updateUserRole);

export default router;
