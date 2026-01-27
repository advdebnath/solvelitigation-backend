import { Request, Response } from "express";
import { User } from "@/models/user.model";

/**
 * GET /api/superadmin/users
 */
export const listUsers = async (req: Request, res: Response) => {
  const users = await User.find().select("-password");
  res.json(users);
};

/**
 * PATCH /api/superadmin/users/:id/block
 */
export const blockUser = async (req: Request, res: Response) => {
  await User.findByIdAndUpdate(req.params.id, { isBlocked: true });
  res.json({ success: true });
};

/**
 * PATCH /api/superadmin/users/:id/unblock
 */
export const unblockUser = async (req: Request, res: Response) => {
  await User.findByIdAndUpdate(req.params.id, { isBlocked: false });
  res.json({ success: true });
};

/**
 * PATCH /api/superadmin/users/:id/verify
 */
export const verifyUser = async (req: Request, res: Response) => {
  await User.findByIdAndUpdate(req.params.id, { isVerified: true });
  res.json({ success: true });
};

/**
 * PATCH /api/superadmin/users/:id/role
 */
export const updateUserRole = async (req: Request, res: Response) => {
  const { role } = req.body;
  await User.findByIdAndUpdate(req.params.id, { role });
  res.json({ success: true });
};
