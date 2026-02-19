import { recoverStuckIngestions } from "../services/ingestionRecovery.service";

export function startWatchdog() {
  console.log("👀 Watchdog started");

  setInterval(async () => {
    try {
      await recoverStuckIngestions();
    } catch (err) {
      console.error("Watchdog error:", err);
    }
  }, 5 * 60 * 1000);
}
