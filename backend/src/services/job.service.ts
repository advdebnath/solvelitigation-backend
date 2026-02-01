import { Job } from "../models/job.model";

export const enqueueJob = async (data: {
  type: string;
  payload: any;
}) => {
  return await Job.create({
    type: data.type,
    payload: data.payload,
    status: "PENDING",
  });
};
