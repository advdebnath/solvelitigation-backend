import mongoose from "mongoose";

const LegalOntology =
  mongoose.connection.collection(
    "legalontology"
  );

export async function getOntologyActs() {

  return await LegalOntology
    .find({
      ontologyType: "ACT",
      frequency: { $gte: 2 }
    })
    .sort({
      frequency: -1
    })
    .toArray();
}

export async function getOntologyPoints() {

  return await LegalOntology
    .find({
      ontologyType: "POINT_OF_LAW"
    })
    .sort({
      frequency: -1
    })
    .toArray();
}
