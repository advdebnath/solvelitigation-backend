"use client";

import { useEffect, useState } from "react";

interface Stats {
  UPLOADED: number;
  PENDING: number;
  PROCESSING: number;
  COMPLETED: number;
  FAILED: number;
  PERMANENT_FAILURE: number;
  TOTAL: number;
}

export default function IngestionStatsCard() {
  const [stats, setStats] = useState<Stats | null>(null);

  const fetchStats = async () => {
    try {
      const res = await fetch("/api/admin/ingestions/stats", {
        cache: "no-store",
      });
      const data = await res.json();
      if (data.success) {
        setStats(data.data);
      }
    } catch (err) {
      console.error("Failed to fetch ingestion stats", err);
    }
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 10000);
    return () => clearInterval(interval);
  }, []);

  if (!stats) return <div>Loading ingestion stats...</div>;

  return (
    <div className="p-6 bg-white rounded-2xl shadow-md space-y-4">
      <h2 className="text-xl font-semibold">Live Ingestion Monitor</h2>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        <Stat label="Total" value={stats.TOTAL} />
        <Stat label="Completed" value={stats.COMPLETED} />
        <Stat label="Pending" value={stats.PENDING} />
        <Stat label="Processing" value={stats.PROCESSING} />
        <Stat
          label="Failed"
          value={stats.FAILED}
          highlight={stats.FAILED > 0}
        />
        <Stat
          label="Permanent Failure"
          value={stats.PERMANENT_FAILURE}
          highlight={stats.PERMANENT_FAILURE > 0}
        />
      </div>
    </div>
  );
}

function Stat({
  label,
  value,
  highlight = false,
}: {
  label: string;
  value: number;
  highlight?: boolean;
}) {
  return (
    <div
      className={`p-4 rounded-xl border ${
        highlight ? "border-red-500 bg-red-50" : "border-gray-200"
      }`}
    >
      <div className="text-sm text-gray-500">{label}</div>
      <div
        className={`text-2xl font-bold ${
          highlight ? "text-red-600" : "text-gray-800"
        }`}
      >
        {value}
      </div>
    </div>
  );
}
