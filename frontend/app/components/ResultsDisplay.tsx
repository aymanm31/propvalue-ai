"use client";

import { useState } from "react";
import {
  AnalysisResults,
  LineItem,
  OverImprovementResult,
  downloadReport,
} from "../lib/api";

interface ResultsDisplayProps {
  results: AnalysisResults | null;
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  const [isDownloading, setIsDownloading] = useState(false);

  if (!results) return null;

  const roi = results.roi_analysis;
  const rehab = results.rehab_estimate;
  const market = results.market_data;
  const vision = results.vision_analysis;

  const roiColor =
    roi.roi_percentage >= 15
      ? "text-green-600"
      : roi.roi_percentage >= 0
        ? "text-yellow-600"
        : "text-red-600";

  return (
    <div className="space-y-6 mt-8">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-900">
          Analysis results
        </h2>
        <button
          onClick={async () => {
            setIsDownloading(true);
            try {
              await downloadReport(results);
            } catch {
              alert("Failed to generate report. Please try again.");
            } finally {
              setIsDownloading(false);
            }
          }}
          disabled={isDownloading}
          className="text-sm bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          {isDownloading ? "Generating..." : "Download PDF report"}
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          ROI summary
        </h2>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-xs text-gray-500 mb-1">ROI</p>
            <p className={`text-2xl font-semibold ${roiColor}`}>
              {roi.roi_percentage.toFixed(1)}%
            </p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-xs text-gray-500 mb-1">Verdict</p>
            <p className="text-sm font-medium text-gray-800">{roi.verdict}</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-xs text-gray-500 mb-1">Net profit</p>
            <p className="text-lg font-semibold text-gray-900">
              ${roi.net_profit.toLocaleString()}
            </p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-xs text-gray-500 mb-1">Total investment</p>
            <p className="text-lg font-semibold text-gray-900">
              ${roi.total_investment.toLocaleString()}
            </p>
          </div>
        </div>
      </div>

      {results.over_improvement.alert_count > 0 && (
        <div className="bg-amber-50 rounded-xl border border-amber-200 p-6">
          <h2 className="text-lg font-semibold text-amber-800 mb-3">
            Over-improvement warnings
          </h2>
          <div className="space-y-2">
            {results.over_improvement.alerts.map((alert: string, i: number) => (
              <div key={i} className="flex gap-3 text-sm text-amber-700">
                <span className="flex-shrink-0">⚠️</span>
                <p>{alert}</p>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t border-amber-200 grid grid-cols-2 gap-3 text-sm">
            <div>
              <p className="text-amber-600">Neighborhood ceiling</p>
              <p className="font-semibold text-amber-800">
                $
                {results.over_improvement.neighborhood_ceiling.toLocaleString()}
              </p>
            </div>
            <div>
              <p className="text-amber-600">ARV as % of ceiling</p>
              <p className="font-semibold text-amber-800">
                {results.over_improvement.arv_to_ceiling_ratio}%
              </p>
            </div>
            <div>
              <p className="text-amber-600">Recommended max rehab</p>
              <p className="font-semibold text-amber-800">
                $
                {results.over_improvement.recommended_max_rehab.toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Property condition
        </h2>
        <p className="text-sm text-gray-600">
          Overall grade:{" "}
          <span className="font-semibold">
            {vision.overall_condition_grade}
          </span>{" "}
          · {vision.images_analyzed} photo
          {vision.images_analyzed > 1 ? "s" : ""} analyzed
        </p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-1">
          Rehab estimate
        </h2>
        <p className="text-xs text-gray-400 mb-4">
          Local labor multiplier: {results.rehab_estimate.labor_multiplier}x
          national average
        </p>
        <div className="space-y-2">
          {rehab.line_items.map((item: LineItem, i: number) => (
            <div key={i} className="flex justify-between text-sm">
              <span className="text-gray-600 capitalize">
                {item.room_type.replace("_", " ")} ({item.condition_grade})
              </span>
              <span className="font-medium text-gray-900">
                ${item.midpoint_estimate.toLocaleString()}
              </span>
            </div>
          ))}
          <div className="border-t border-gray-100 pt-2 mt-2 flex justify-between text-sm font-semibold">
            <span>Recommended budget (incl. 15% contingency)</span>
            <span>${rehab.recommended_budget.toLocaleString()}</span>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-1">
          Market data
        </h2>
        <p className="text-xs text-gray-400 mb-4">
          Based on {market.comps_used} comparable ZIP codes · Confidence:{" "}
          <span
            className={
              market.arv_confidence === "high"
                ? "text-green-600 font-medium"
                : market.arv_confidence === "medium"
                  ? "text-yellow-600 font-medium"
                  : "text-red-600 font-medium"
            }
          >
            {market.arv_confidence}
          </span>
        </p>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div>
            <p className="text-gray-500">Estimated ARV</p>
            <p className="font-semibold text-gray-900">
              ${market.arv_estimate.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-gray-500">ARV range</p>
            <p className="font-semibold text-gray-900">
              ${market.arv_low.toLocaleString()} – $
              {market.arv_high.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-gray-500">Avg price / sqft</p>
            <p className="font-semibold text-gray-900">
              ${market.avg_price_per_sqft}
            </p>
          </div>
          <div>
            <p className="text-gray-500">Days on market</p>
            <p className="font-semibold text-gray-900">
              {market.primary_market.days_on_market} days
            </p>
          </div>
          <div>
            <p className="text-gray-500">70% rule max purchase</p>
            <p className="font-semibold text-gray-900">
              ${roi.seventy_percent_rule_max_purchase.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-gray-500">Passes 70% rule</p>
            <p
              className={`font-semibold ${roi.passes_70_percent_rule ? "text-green-600" : "text-red-600"}`}
            >
              {roi.passes_70_percent_rule ? "Yes" : "No"}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
