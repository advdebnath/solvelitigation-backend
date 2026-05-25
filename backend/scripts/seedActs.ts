import mongoose from "mongoose";
import ActMaster from "../src/models/actMaster.model";

const MONGO_URI = "mongodb://127.0.0.1:27017/solvelitigation";

async function seed() {
  await mongoose.connect(MONGO_URI);

  await ActMaster.deleteMany({});

  await ActMaster.insertMany([
    {
      canonicalName: "Indian Contract Act, 1872",
      aliases: ["contract act", "indian contract act"],
    },
    {
      canonicalName: "Arbitration and Conciliation Act, 1996",
      aliases: ["arbitration act", "conciliation act", "arbitration act 1996"],
    },
    {
      canonicalName: "Code of Civil Procedure, 1908",
      aliases: ["cpc", "civil procedure code"],
    },
    {
      canonicalName: "Code of Criminal Procedure, 1973",
      aliases: ["crpc", "criminal procedure code"],
    },
    {
      canonicalName: "Negotiable Instruments Act, 1881",
      aliases: ["ni act", "negotiable instruments act"],
    },
  ]);

  console.log("✅ Act Master Seeded");
  process.exit();
}

seed();
