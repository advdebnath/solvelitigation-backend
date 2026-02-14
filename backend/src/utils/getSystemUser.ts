import User from "../models/user.model";

export async function getSystemUserId() {
  const user = await User.findOne({ email: "system@solvelitigation.local" }).select("_id");
  if (!user) {
    throw new Error("SYSTEM user not found");
  }
  return user._id;
}
