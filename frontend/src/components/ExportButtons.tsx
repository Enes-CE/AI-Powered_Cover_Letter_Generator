import React from 'react';
import { Download, FileText, FileDown } from 'lucide-react';

interface ExportButtonsProps {
  coverLetter: string;
  jobTitle: string;
  companyName: string;
  isExporting: boolean;
  onExportPdf: () => void;
  onExportDocx: () => void;
}

export const ExportButtons: React.FC<ExportButtonsProps> = ({
  coverLetter,
  jobTitle,
  companyName,
  isExporting,
  onExportPdf,
  onExportDocx
}) => {
  return (
    <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
      <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
        <FileDown className="h-5 w-5 mr-2 text-blue-600" />
        Export Cover Letter
      </h4>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {/* PDF Export Button */}
        <button 
          onClick={onExportPdf}
          disabled={isExporting}
          className="group relative flex items-center justify-center px-4 py-3 bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white font-medium rounded-lg transition-all duration-200 shadow-md hover:shadow-lg disabled:shadow-sm"
        >
          {isExporting ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              <span>Exporting PDF...</span>
            </>
          ) : (
            <>
              <FileText className="h-5 w-5 mr-2 group-hover:scale-110 transition-transform" />
              <span>Download as PDF</span>
            </>
          )}
        </button>

        {/* DOCX Export Button */}
        <button 
          onClick={onExportDocx}
          disabled={isExporting}
          className="group relative flex items-center justify-center px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium rounded-lg transition-all duration-200 shadow-md hover:shadow-lg disabled:shadow-sm"
        >
          {isExporting ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              <span>Exporting DOCX...</span>
            </>
          ) : (
            <>
              <Download className="h-5 w-5 mr-2 group-hover:scale-110 transition-transform" />
              <span>Download as DOCX</span>
            </>
          )}
        </button>
      </div>

      {/* Export Info */}
      <div className="mt-3 text-xs text-gray-600">
        <p>• PDF: Professional format, ready to print</p>
        <p>• DOCX: Editable format for Microsoft Word</p>
      </div>
    </div>
  );
};
