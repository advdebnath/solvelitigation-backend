// ============================================
// 🔥 LAW MAPPER (POINT → ACT + SECTION)
// ============================================

type Mapping = {
  act: string;
  sections: string[];
};

// 🔥 MASTER LEGAL MAP (EXPANDABLE)
const LAW_MAP: Record<string, Mapping> = {
  murder: {
    act: "Indian Penal Code",
    sections: ["Section 302 IPC"],
  },

  "attempt to murder": {
    act: "Indian Penal Code",
    sections: ["Section 307 IPC"],
  },

  evidence: {
    act: "Indian Evidence Act",
    sections: ["Section 101 Evidence Act"],
  },

  "circumstantial evidence": {
    act: "Indian Evidence Act",
    sections: ["Section 3 Evidence Act"],
  },

  fraud: {
    act: "Indian Penal Code",
    sections: ["Section 420 IPC"],
  },

  "breach of contract": {
    act: "Indian Contract Act",
    sections: ["Section 73 Contract Act"],
  },

  negligence: {
    act: "Law of Torts",
    sections: ["Negligence Principle"],
  },
};

// ============================================
// 🔥 MAIN FUNCTION
// ============================================

export const mapPointsToLaw = (points: string[] = []) => {
  const acts = new Set<string>();
  const sections = new Set<string>();
  const sectionActMap: Record<string, string> = {};

  points.forEach((point) => {
    const key = point.toLowerCase();

    if (LAW_MAP[key]) {
      const mapping = LAW_MAP[key];

      acts.add(mapping.act);

      mapping.sections.forEach((sec) => {
        sections.add(sec);
        sectionActMap[sec] = mapping.act;
      });
    }
  });

  return {
    acts: Array.from(acts),
    sections: Array.from(sections),
    sectionActMap,
  };
};
