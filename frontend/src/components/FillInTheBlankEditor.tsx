import React, { useState, useEffect, ReactElement } from 'react';

interface Blank {
  placeholder: string;
  correct_answer: string;
  hint: string;
}

interface FillInTheBlankEditorProps {
  codeTemplate: string;
  blanks: Blank[];
  onCodeChange: (code: string) => void;
  userCode: string;
  isSubmitting: boolean;
}

const FillInTheBlankEditor: React.FC<FillInTheBlankEditorProps> = ({
  codeTemplate,
  blanks,
  onCodeChange,
  userCode,
  isSubmitting
}) => {
  const [blankAnswers, setBlankAnswers] = useState<Record<string, string>>({});
  const [showHints, setShowHints] = useState<Record<string, boolean>>({});

  // Initialize blank answers from user code or template
  useEffect(() => {
    const answers: Record<string, string> = {};
    blanks.forEach(blank => {
      answers[blank.placeholder] = '';
    });
    setBlankAnswers(answers);
  }, [blanks]);

  // Update user code when blank answers change
  useEffect(() => {
    let updatedCode = codeTemplate;
    blanks.forEach(blank => {
      const answer = blankAnswers[blank.placeholder] || blank.placeholder;
      updatedCode = updatedCode.replace(new RegExp(blank.placeholder, 'g'), answer);
    });
    onCodeChange(updatedCode);
  }, [blankAnswers, codeTemplate, blanks, onCodeChange]);

  const handleBlankChange = (placeholder: string, value: string) => {
    setBlankAnswers(prev => ({
      ...prev,
      [placeholder]: value
    }));
  };

  const toggleHint = (placeholder: string) => {
    setShowHints(prev => ({
      ...prev,
      [placeholder]: !prev[placeholder]
    }));
  };

  const getBlankHint = (placeholder: string) => {
    const blank = blanks.find(b => b.placeholder === placeholder);
    return blank?.hint || '';
  };

  const renderCodeWithBlanks = () => {
    const lines = codeTemplate.split('\n');
    const renderedLines: ReactElement[] = [];

    lines.forEach((line, lineIndex) => {
      const lineElements: ReactElement[] = [];
      let currentLine = line;

      // Find all blanks in this line
      const lineBlanks = blanks.filter(blank => line.includes(blank.placeholder));
      
      lineBlanks.forEach((blank, blankInLineIndex) => {
        const parts = currentLine.split(blank.placeholder);
        
        if (parts.length > 1) {
          // Add text before the blank
          if (parts[0]) {
            lineElements.push(
              <span key={`text-${lineIndex}-${blankInLineIndex}`} className="text-gray-300">
                {parts[0]}
              </span>
            );
          }
          
          // Add the blank input
          lineElements.push(
            <span key={`blank-${lineIndex}-${blankInLineIndex}`} className="inline-block relative">
              <input
                type="text"
                value={blankAnswers[blank.placeholder] || ''}
                onChange={(e) => handleBlankChange(blank.placeholder, e.target.value)}
                placeholder={blank.placeholder}
                disabled={isSubmitting}
                className="inline-block min-w-24 px-2 py-1 mx-1 text-sm border-2 border-blue-400 rounded-md focus:border-blue-500 focus:outline-none bg-blue-50 text-gray-900 placeholder-gray-500 disabled:opacity-50 font-mono"
              />
              <button
                type="button"
                onClick={() => toggleHint(blank.placeholder)}
                disabled={isSubmitting}
                className="ml-1 text-xs text-blue-400 hover:text-blue-300 disabled:opacity-50"
                title="Show hint"
              >
                💡
              </button>
              {showHints[blank.placeholder] && (
                <div className="absolute z-10 mt-1 p-2 bg-yellow-100 border border-yellow-300 rounded-md text-xs text-gray-700 max-w-xs shadow-lg">
                  {getBlankHint(blank.placeholder)}
                </div>
              )}
            </span>
          );
          
          // Update current line to continue processing
          currentLine = parts.slice(1).join(blank.placeholder);
        }
      });
      
      // Add remaining text after all blanks
      if (currentLine) {
        lineElements.push(
          <span key={`text-end-${lineIndex}`} className="text-gray-300">
            {currentLine}
          </span>
        );
      }
      
      // Add line number and content
      renderedLines.push(
        <div key={`line-${lineIndex}`} className="flex items-start">
          <span className="text-gray-500 text-xs mr-4 select-none w-8 text-right">
            {lineIndex + 1}
          </span>
          <div className="flex-1 flex flex-wrap items-center">
            {lineElements}
          </div>
        </div>
      );
    });

    return renderedLines;
  };

  return (
    <div className="relative">
      {/* Code Editor */}
      <div className="bg-gray-900 text-gray-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
        <div className="space-y-1">
          {renderCodeWithBlanks()}
        </div>
      </div>
      
      {/* Blank Status Panel */}
      <div className="mt-4 p-4 bg-gray-50 rounded-lg border">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-sm font-medium text-gray-900">Fill in the blanks:</h4>
          <span className="text-xs text-gray-500">
            {blanks.length} blank{blanks.length !== 1 ? 's' : ''} to complete
          </span>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {blanks.map((blank, index) => (
            <div key={index} className="flex items-center space-x-2 p-2 bg-white rounded border">
              <span className="text-xs text-gray-600 w-6 font-medium">#{index + 1}</span>
              <input
                type="text"
                value={blankAnswers[blank.placeholder] || ''}
                onChange={(e) => handleBlankChange(blank.placeholder, e.target.value)}
                placeholder={blank.placeholder}
                disabled={isSubmitting}
                className="flex-1 px-2 py-1 text-sm border border-gray-300 rounded focus:border-blue-500 focus:outline-none disabled:opacity-50"
              />
              <button
                type="button"
                onClick={() => toggleHint(blank.placeholder)}
                disabled={isSubmitting}
                className="text-xs text-blue-600 hover:text-blue-700 disabled:opacity-50 p-1"
                title="Show hint"
              >
                💡
              </button>
            </div>
          ))}
        </div>
        
        {/* Hints Panel */}
        {Object.values(showHints).some(Boolean) && (
          <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
            <h5 className="text-sm font-medium text-yellow-900 mb-2 flex items-center">
              <span className="mr-2">💡</span>
              Hints:
            </h5>
            <ul className="space-y-2">
              {blanks.map((blank, index) => (
                showHints[blank.placeholder] && (
                  <li key={index} className="text-sm text-yellow-800 flex items-start">
                    <span className="font-medium mr-2">Blank {index + 1}:</span>
                    <span>{blank.hint}</span>
                  </li>
                )
              ))}
            </ul>
          </div>
        )}
        
        {/* Progress Indicator */}
        <div className="mt-3 pt-3 border-t border-gray-200">
          <div className="flex items-center justify-between text-xs text-gray-600">
            <span>Progress:</span>
            <span>
              {Object.values(blankAnswers).filter(answer => answer.trim() !== '').length} / {blanks.length} filled
            </span>
          </div>
          <div className="mt-1 w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{
                width: `${(Object.values(blankAnswers).filter(answer => answer.trim() !== '').length / blanks.length) * 100}%`
              }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FillInTheBlankEditor;
