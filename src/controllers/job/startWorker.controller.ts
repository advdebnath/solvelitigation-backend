import { processJobsSerially } from '@/workers';

export async function startJudgmentWorker() {
  await processJobsSerially();
}
