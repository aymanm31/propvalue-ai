"use client";

import { useState } from "react";
import { FormData } from "../lib/api";

interface AnalysisFormProps {
  onSubmit: (formData: FormData, images: File[]) => void;
  isLoading: boolean;
}

const EMPTY_FORM: FormData = {
  zip_code: "",
  square_footage: "",
  purchase_price: "",
  monthly_taxes: "",
  monthly_insurance: "",
  rehab_duration_months: "",
};

const FIELDS: { name: keyof FormData; label: string; placeholder: string }[] = [
  { name: "zip_code", label: "ZIP code", placeholder: "22030" },
  { name: "square_footage", label: "Square footage", placeholder: "1800" },
  { name: "purchase_price", label: "Asking price ($)", placeholder: "320000" },
  { name: "monthly_taxes", label: "Monthly taxes ($)", placeholder: "400" },
  {
    name: "monthly_insurance",
    label: "Monthly insurance ($)",
    placeholder: "150",
  },
  {
    name: "rehab_duration_months",
    label: "Estimated rehab duration (months)",
    placeholder: "4",
  },
];

export default function AnalysisForm({
  onSubmit,
  isLoading,
}: AnalysisFormProps) {
  const [formData, setFormData] = useState<FormData>(EMPTY_FORM);
  const [images, setImages] = useState<File[]>([]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setImages(Array.from(e.target.files));
    }
  };

  const handleSubmit = (e: React.MouseEvent) => {
    e.preventDefault();
    onSubmit(formData, images);
  };

  return (
    <div className="space-y-5">
      {FIELDS.map((field) => (
        <div key={field.name}>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {field.label}
          </label>
          <input
            type="text"
            name={field.name}
            placeholder={field.placeholder}
            value={formData[field.name]}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      ))}

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Listing photos
        </label>
        <input
          type="file"
          accept="image/*"
          multiple
          onChange={handleImageChange}
          className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
        {images.length > 0 && (
          <p className="text-xs text-gray-400 mt-1">
            {images.length} photo{images.length > 1 ? "s" : ""} selected
          </p>
        )}
      </div>

      <button
        onClick={handleSubmit}
        disabled={isLoading}
        className="w-full bg-blue-600 text-white py-2.5 px-4 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? "Analyzing..." : "Analyze property"}
      </button>
    </div>
  );
}
