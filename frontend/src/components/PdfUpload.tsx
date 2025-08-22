import React from 'react';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';

interface PdfUploadProps {
  onFileSelect: (e: React.ChangeEvent<HTMLInputElement>) => void;
  isUploading: boolean;
  fileName?: string;
  error?: string | null;
}

export const PdfUpload: React.FC<PdfUploadProps> = ({
  onFileSelect,
  isUploading,
  fileName,
  error
}) => {
  return (
    <div className="mt-2">
      <div className="relative">
        <input
          type="file"
          accept="application/pdf"
          onChange={onFileSelect}
          disabled={isUploading}
          className="hidden"
          id="pdf-upload"
        />
        
        <label
          htmlFor="pdf-upload"
          className={`group relative flex flex-col items-center justify-center w-full h-24 border-2 border-dashed rounded-lg cursor-pointer transition-all duration-200 ${
            isUploading
              ? 'border-blue-300 bg-blue-50'
              : error
              ? 'border-red-300 bg-red-50 hover:border-red-400'
              : 'border-gray-300 bg-gray-50 hover:border-blue-400 hover:bg-blue-50'
          }`}
        >
          {isUploading ? (
            <>
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mb-2"></div>
              <span className="text-sm text-blue-600 font-medium">Processing PDF...</span>
            </>
          ) : fileName ? (
            <>
              <CheckCircle className="h-6 w-6 text-green-600 mb-2" />
              <span className="text-sm text-green-600 font-medium">{fileName}</span>
              <span className="text-xs text-gray-500">Click to change file</span>
            </>
          ) : (
            <>
              <Upload className="h-6 w-6 text-gray-400 group-hover:text-blue-600 mb-2 transition-colors" />
              <span className="text-sm text-gray-600 group-hover:text-blue-600 font-medium transition-colors">
                Upload CV as PDF
              </span>
              <span className="text-xs text-gray-500">or drag and drop</span>
            </>
          )}
        </label>
      </div>
      
      {error && (
        <div className="mt-2 flex items-center text-red-600 text-sm">
          <AlertCircle className="h-4 w-4 mr-1" />
          {error}
        </div>
      )}
      
      <p className="text-xs text-gray-500 mt-1">
        PDF yükleyin; metin otomatik doldurulur. Maksimum 10MB.
      </p>
    </div>
  );
};
