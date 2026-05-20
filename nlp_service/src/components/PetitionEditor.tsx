"use client";

import dynamic from "next/dynamic";
import { useState } from "react";

// 🔥 Load Jodit only on client (IMPORTANT)
const JoditEditor = dynamic(() => import("jodit-react"), {
  ssr: false,
});

export default function PetitionEditor({ content }: any) {
  const [value, setValue] = useState(content || "");

  return (
    <div>
      <JoditEditor
        value={value}
        onChange={(newContent: string) => setValue(newContent)}
      />

      {/* OPTIONAL SAVE / COPY */}
      <div className="mt-3 flex gap-2">
        <button
          onClick={() => navigator.clipboard.writeText(value)}
          className="bg-green-500 text-white px-3 py-1 rounded"
        >
          Copy Edited Text
        </button>
      </div>
    </div>
  );
}
