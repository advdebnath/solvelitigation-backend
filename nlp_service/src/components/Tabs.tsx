"use client";

import { useState } from "react";
import PetitionEditor from "./PetitionEditor";

export default function Tabs({ result }: any) {
  const [tab, setTab] = useState("petition");

  const tabs = [
    { key: "petition", label: "📄 Petition" },
    { key: "advocate", label: "⚖️ Advocate" },
    { key: "judgment", label: "🏛️ Judgment" },
    { key: "outcome", label: "📊 Outcome" },
    { key: "strategy", label: "🧠 Strategy" },
  ];

  // =========================================
  // 🔥 COPY FUNCTION
  // =========================================
  const getContent = () => {
    if (!result) return "";

    switch (tab) {
      case "petition":
        return result.petition || "";
      case "advocate":
        return result.advocate || "";
      case "judgment":
        return result.judgment || "";
      case "outcome":
        return result.outcome?.text || "";
      case "strategy":
        return result.strategy?.text || "";
      default:
        return "";
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(getContent());
    alert("Copied to clipboard!");
  };

  // =========================================
  // 🔥 UI
  // =========================================
  return (
    <div className="mt-6">

      {/* TAB BUTTONS */}
      <div className="flex flex-wrap gap-2 mb-4">
        {tabs.map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`px-3 py-1 rounded border ${
              tab === t.key
                ? "bg-blue-600 text-white"
                : "bg-white hover:bg-gray-100"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* ACTION BAR */}
      <div className="flex justify-between items-center mb-2">
        <div className="font-semibold">
          {tabs.find((t) => t.key === tab)?.label}
        </div>

        <button
          onClick={handleCopy}
          className="bg-green-500 text-white px-3 py-1 rounded"
        >
          Copy
        </button>
      </div>

      {/* CONTENT BOX */}
      <div className="border rounded p-4 bg-gray-50 whitespace-pre-wrap h-[500px] overflow-y-auto">

        {/* PETITION */}
        {tab === "petition" && (
          <PetitionEditor content={result?.petition} />
        )}

        {/* ADVOCATE */}
        {tab === "advocate" && (
          <div>{result?.advocate || "No advocate analysis available"}</div>
        )}

        {/* JUDGMENT */}
        {tab === "judgment" && (
          <div>{result?.judgment || "No judgment generated"}</div>
        )}

        {/* OUTCOME */}
        {tab === "outcome" && (
          <div>
            {result?.outcome ? (
              <>
                <div className="mb-3 font-semibold text-lg">
                  Probability: {result.outcome.probability}%
                </div>

                <div className="mb-2">
                  Decision: {result.outcome.decision}
                </div>

                <div className="mb-2">
                  Confidence: {result.outcome.confidence}
                </div>

                <div className="mt-3 font-semibold">Reasons:</div>
                <ul className="list-disc ml-5">
                  {result.outcome.reasons?.map((r: any, i: number) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>

                <pre className="mt-3 whitespace-pre-wrap">
                  {result.outcome.text}
                </pre>
              </>
            ) : (
              "No outcome prediction available"
            )}
          </div>
        )}

        {/* STRATEGY */}
        {tab === "strategy" && (
          <div>
            {result?.strategy ? (
              <>
                <div className="mb-2 font-semibold">
                  Strength: {result.strategy.strength}
                </div>

                <div className="mb-2">
                  Strategy: {result.strategy.strategy}
                </div>

                <div className="mt-2 font-semibold">Steps:</div>
                <ul className="list-disc ml-5">
                  {result.strategy.steps?.map((s: any, i: number) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>

                <pre className="mt-3 whitespace-pre-wrap">
                  {result.strategy.text}
                </pre>
              </>
            ) : (
              "No strategy available"
            )}
          </div>
        )}

      </div>
    </div>
  );
}
