"use client";

import { useState } from "react";
import AnalysisForm from "./components/AnalysisForm";
import ResultsDisplay from "./components/ResultsDisplay";
import { analyzeProperty, FormData, AnalysisResults } from "./lib/api";

export default function Home() {
  const [results, setResults] = useState<AnalysisResults | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const handleSubmit = async (formData: FormData, images: File[]) => {
    setIsLoading(true);
    setError("");
    setResults(null);

    try {
      const data = await analyzeProperty(formData, images);
      setResults(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Something went wrong. Make sure your backend is running.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-semibold text-gray-900 mb-2">
          PropValue AI
        </h1>
        <p className="text-gray-500 mb-8">
          Upload listing photos and get an instant ROI estimate for any
          fixer-upper.
        </p>

        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <AnalysisForm onSubmit={handleSubmit} isLoading={isLoading} />
        </div>

        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4 text-sm text-red-700">
            {error}
          </div>
        )}

        {isLoading && (
          <div className="mt-8 bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
              <p className="text-sm font-medium text-gray-700">
                Analyzing your property...
              </p>
            </div>
            <div className="space-y-2 text-sm text-gray-400">
              <p>✓ Uploading photos</p>
              <p>⟳ Running AI condition assessment</p>
              <p>○ Calculating rehab costs</p>
              <p>○ Pulling market comps</p>
              <p>○ Computing ROI</p>
            </div>
          </div>
        )}

        <ResultsDisplay results={results} />
      </div>
    </main>
  );
}
