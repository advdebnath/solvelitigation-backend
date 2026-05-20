"use client";

import { useState } from "react";
import axios from "axios";
import Tabs from "@/components/Tabs";

export default function Dashboard() {
  const [query, setQuery] = useState("");
  const [text, setText] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // =========================================
  // 🔥 HANDLE FILE UPLOAD
  // =========================================
  const handleFileUpload = async (e: any) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const content = await file.text();
    setText(content);
  };

  // =========================================
  // 🔥 HANDLE SUBMIT
  // =========================================
  const handleSubmit = async () => {
    if (!query.trim() || !text.trim()) {
      alert("Please enter both query and document text");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/draft-petition",
        {
          query,
          text,
        }
      );

      setResult(res.data);
    } catch (err: any) {
      console.error(err);
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  // =========================================
  // 🔥 RESET
  // =========================================
  const handleReset = () => {
    setQuery("");
    setText("");
    setResult(null);
  };

  // =========================================
  // 🔥 UI
  // =========================================
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-6xl mx-auto bg-white p-6 rounded shadow">

        {/* HEADER */}
        <h1 className="text-2xl font-bold mb-4">
          ⚖️ SolveLitigation AI Dashboard
        </h1>

        {/* FILE UPLOAD */}
        <div className="mb-4">
          <label className="font-semibold">Upload Document:</label>
          <input
            type="file"
            onChange={handleFileUpload}
            className="block mt-2"
          />
        </div>

        {/* TEXT INPUT */}
        <textarea
          className="w-full border p-3 mb-4 rounded"
          rows={6}
          placeholder="Paste document text here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        {/* QUERY INPUT */}
        <input
          type="text"
          className="w-full border p-3 mb-4 rounded"
          placeholder="Enter legal issue (e.g. interpretation of statute)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        {/* BUTTONS */}
        <div className="flex gap-3 mb-6">
          <button
            onClick={handleSubmit}
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            {loading ? "Processing..." : "Analyze Case"}
          </button>

          <button
            onClick={handleReset}
            className="bg-gray-500 text-white px-4 py-2 rounded"
          >
            Reset
          </button>
        </div>

        {/* LOADING */}
        {loading && (
          <div className="text-blue-600 font-semibold">
            ⏳ Processing legal analysis...
          </div>
        )}

        {/* RESULTS */}
        {result && (
          <div>
            <h2 className="text-xl font-semibold mb-3">
              📊 Analysis Result
            </h2>

            <Tabs result={result} />
          </div>
        )}
      </div>
    </div>
  );
}
