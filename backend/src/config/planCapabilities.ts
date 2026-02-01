export type PlanKey = "free" | "simple" | "premium" | "enterprise";

export type PlanCapabilities = {
  judgmentsPerDay: number | "unlimited";
  downloadsPerDay: number | "unlimited";
  aiRequestsPerDay: number | "unlimited";

  features: {
    aiTools: boolean;
    advancedSearch: boolean;
    bulkDownload: boolean;
  };
};

export const PLAN_CAPABILITIES: Record<PlanKey, PlanCapabilities> = {
  free: {
    judgmentsPerDay: 2,
    downloadsPerDay: 0,
    aiRequestsPerDay: 0,
    features: {
      aiTools: false,
      advancedSearch: false,
      bulkDownload: false,
    },
  },

  simple: {
    judgmentsPerDay: 10,
    downloadsPerDay: 3,
    aiRequestsPerDay: 0,
    features: {
      aiTools: false,
      advancedSearch: true,
      bulkDownload: false,
    },
  },

  premium: {
    judgmentsPerDay: "unlimited",
    downloadsPerDay: "unlimited",
    aiRequestsPerDay: 50,
    features: {
      aiTools: true,
      advancedSearch: true,
      bulkDownload: true,
    },
  },

  enterprise: {
    judgmentsPerDay: "unlimited",
    downloadsPerDay: "unlimited",
    aiRequestsPerDay: "unlimited",
    features: {
      aiTools: true,
      advancedSearch: true,
      bulkDownload: true,
    },
  },
};
