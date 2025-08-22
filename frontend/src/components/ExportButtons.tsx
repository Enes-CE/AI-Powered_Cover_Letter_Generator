import React from 'react';
import { Download, FileText, FileDown } from 'lucide-react';

interface ExportButtonsProps {
  isExporting: boolean;
  onExportPdf: () => void;
  onExportDocx: () => void;
}

export const ExportButtons: React.FC<ExportButtonsProps> = ({
  isExporting,
  onExportPdf,
  onExportDocx
}) => {
  return (
    <div className="flex space-x-3">
      {/* PDF Export Button */}
      <button 
        onClick={onExportPdf}
        disabled={isExporting}
        className="group relative flex items-center px-4 py-2 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 disabled:from-red-400 disabled:to-red-500 text-white font-medium rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl disabled:shadow-md transform hover:scale-105 disabled:transform-none"
      >
        {isExporting ? (
          <>
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
            <span>Exporting...</span>
          </>
        ) : (
          <>
            <FileText className="h-4 w-4 mr-2 group-hover:scale-110 transition-transform" />
            <span>PDF</span>
          </>
        )}
      </button>

      {/* DOCX Export Button */}
      <button 
        onClick={onExportDocx}
        disabled={isExporting}
        className="group relative flex items-center px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:from-blue-400 disabled:to-blue-500 text-white font-medium rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl disabled:shadow-md transform hover:scale-105 disabled:transform-none"
      >
        {isExporting ? (
          <>
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
            <span>Exporting...</span>
          </>
        ) : (
          <>
            <Download className="h-4 w-4 mr-2 group-hover:scale-110 transition-transform" />
            <span>DOCX</span>
          </>
        )}
      </button>
    </div>
  );
};
