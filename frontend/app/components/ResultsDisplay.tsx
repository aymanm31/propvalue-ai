interface RoiAnalysis {
  roi_percentage: number;
  verdict: string;
  net_profit: number;
  total_investment: number;
  seventy_percent_rule_max_purchase: number;
  passes_70_percent_rule: boolean;
}

interface LineItem {
  room_type: string;
  condition_grade: string;
  midpoint_estimate: number;
}

interface RehabEstimate {
  line_items: LineItem[];
  recommended_budget: number;
}

interface MarketData {
  estimated_arv: number;
  median_price_per_sqft: number;
}

interface VisionAnalysis {
  overall_condition_grade: string;
  images_analyzed: number;
}

interface AnalysisResults {
  roi_analysis: RoiAnalysis;
  rehab_estimate: RehabEstimate;
  market_data: MarketData;
  vision_analysis: VisionAnalysis;
}

interface ResultsDisplayProps {
  results: AnalysisResults | null;
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
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
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Rehab estimate
        </h2>
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
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Market data
        </h2>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div>
            <p className="text-gray-500">Estimated ARV</p>
            <p className="font-semibold text-gray-900">
              ${market.estimated_arv.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-gray-500">Median price/sqft</p>
            <p className="font-semibold text-gray-900">
              ${market.median_price_per_sqft}
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
