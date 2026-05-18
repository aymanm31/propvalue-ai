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

const FIELDS: {
  name: keyof FormData;
  label: string;
  placeholder: string;
  hint?: string;
}[] = [
  {
    name: "zip_code",
    label: "ZIP code",
    placeholder: "22030",
    hint: "5-digit ZIP code",
  },
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
    hint: "1–60 months",
  },
];

function validateForm(formData: FormData, images: File[]): string[] {
  const errors: string[] = [];

  if (!/^\d{5}$/.test(formData.zip_code)) {
    errors.push("ZIP code must be exactly 5 digits");
  }
  if (!formData.square_footage || parseFloat(formData.square_footage) <= 0) {
    errors.push("Square footage must be greater than 0");
  }
  if (!formData.purchase_price || parseFloat(formData.purchase_price) <= 0) {
    errors.push("Asking price must be greater than 0");
  }
  if (!formData.monthly_taxes || parseFloat(formData.monthly_taxes) < 0) {
    errors.push("Monthly taxes must be 0 or greater");
  }
  if (
    !formData.monthly_insurance ||
    parseFloat(formData.monthly_insurance) < 0
  ) {
    errors.push("Monthly insurance must be 0 or greater");
  }
  const months = parseInt(formData.rehab_duration_months);
  if (!months || months < 1 || months > 60) {
    errors.push("Rehab duration must be between 1 and 60 months");
  }
  if (images.length === 0) {
    errors.push("Please upload at least one listing photo");
  }
  if (images.length > 10) {
    errors.push("Maximum 10 photos allowed");
  }
  for (const img of images) {
    if (img.size > 4 * 1024 * 1024) {
      errors.push(`${img.name} is too large. Maximum 4MB per image.`);
    }
  }

  return errors;
}

export default function AnalysisForm({
  onSubmit,
  isLoading,
}: AnalysisFormProps) {
  const [formData, setFormData] = useState<FormData>(EMPTY_FORM);
  const [images, setImages] = useState<File[]>([]);
  const [validationErrors, setValidationErrors] = useState<string[]>([]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (validationErrors.length > 0) setValidationErrors([]);
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setImages(Array.from(e.target.files));
      if (validationErrors.length > 0) setValidationErrors([]);
    }
  };

  const handleSubmit = (e: React.MouseEvent) => {
    e.preventDefault();
    const errors = validateForm(formData, images);
    if (errors.length > 0) {
      setValidationErrors(errors);
      return;
    }
    setValidationErrors([]);
    onSubmit(formData, images);
  };

  return (
    <div className="space-y-5">
      {validationErrors.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm font-medium text-red-700 mb-2">
            Please fix the following:
          </p>
          <ul className="list-disc list-inside space-y-1">
            {validationErrors.map((err, i) => (
              <li key={i} className="text-sm text-red-600">
                {err}
              </li>
            ))}
          </ul>
        </div>
      )}

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
          {field.hint && (
            <p className="text-xs text-gray-400 mt-1">{field.hint}</p>
          )}
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
        <p className="text-xs text-gray-400 mt-1">
          {images.length > 0
            ? `${images.length} photo${images.length > 1 ? "s" : ""} selected`
            : "Upload up to 10 photos · Max 4MB each"}
        </p>
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
