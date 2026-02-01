/**
 * One-time password reset using app bcrypt logic
 */
require("dotenv").config({
  path: "/var/www/solvelitigation/backend/.env.production",
});

const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");
const { User } = require("../dist/models/user.model");

async function run() {
  await mongoose.connect(process.env.MONGODB_URI);

  const email = "advdebnath66@gmail.com";
  const newPassword = "Admin@123";

  const hash = await bcrypt.hash(newPassword, 10);

  const res = await User.updateOne(
    { email },
    { $set: { password: hash } }
  );

  console.log("Password reset result:", res);
  process.exit(0);
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
