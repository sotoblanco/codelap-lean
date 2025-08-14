import React, { useState } from 'react';
import { GitHubRepositoryInfo, GeneratedLearningPlan } from '../types/api';
import apiService from '../services/api';

interface LearningPlanModalProps {
  repository: GitHubRepositoryInfo | null;
  isOpen: boolean;
  onClose: () => void;
  onApprove: (learningPlan: GeneratedLearningPlan) => void;
}

const LearningPlanModal: React.FC<LearningPlanModalProps> = ({
  repository,
  isOpen,
  onClose,
  onApprove,
}) => {
  const [learningPlan, setLearningPlan] = useState<GeneratedLearningPlan | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const generatePlan = async () => {
    if (!repository) return;

    setLoading(true);
    setError('');

    try {
      const response = await apiService.generateLearningPlan({
        repository_info: repository,
      });

      if (response.success && response.learning_plan) {
        setLearningPlan(response.learning_plan);
      } else {
        setError(response.error_message || 'Failed to generate learning plan');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate learning plan');
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = () => {
    if (learningPlan) {
      onApprove(learningPlan);
      onClose();
    }
  };

  if (!isOpen || !repository) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              Learning Plan for {repository.full_name}
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {!learningPlan && !loading && (
            <div className="text-center py-8">
              <p className="text-gray-600 mb-4">
                Generate an AI-powered learning plan for this repository
              </p>
              <button
                onClick={generatePlan}
                className="bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700 transition-colors"
              >
                Generate Learning Plan
              </button>
            </div>
          )}

          {loading && (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Generating learning plan...</p>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
              <p className="text-red-600">{error}</p>
              <button
                onClick={generatePlan}
                className="mt-2 text-red-600 hover:text-red-800 underline"
              >
                Try again
              </button>
            </div>
          )}

          {learningPlan && (
            <div className="space-y-6">
              {/* Plan Overview */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-lg font-semibold mb-2">{learningPlan.title}</h3>
                <p className="text-gray-600 mb-3">{learningPlan.description}</p>
                <div className="flex items-center space-x-4 text-sm">
                  <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded">
                    {learningPlan.difficulty_level}
                  </span>
                  <span className="text-gray-500">
                    Estimated duration: {learningPlan.estimated_duration}
                  </span>
                </div>
              </div>

              {/* Prerequisites */}
              {learningPlan.prerequisites.length > 0 && (
                <div>
                  <h4 className="text-lg font-semibold mb-3">Prerequisites</h4>
                  <ul className="list-disc list-inside space-y-1 text-gray-600">
                    {learningPlan.prerequisites.map((prereq, index) => (
                      <li key={index}>{prereq}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Learning Objectives */}
              {learningPlan.learning_objectives.length > 0 && (
                <div>
                  <h4 className="text-lg font-semibold mb-3">Learning Objectives</h4>
                  <ul className="list-disc list-inside space-y-1 text-gray-600">
                    {learningPlan.learning_objectives.map((objective, index) => (
                      <li key={index}>{objective}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Technologies Covered */}
              {learningPlan.technologies_covered.length > 0 && (
                <div>
                  <h4 className="text-lg font-semibold mb-3">Technologies Covered</h4>
                  <div className="flex flex-wrap gap-2">
                    {learningPlan.technologies_covered.map((tech, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Learning Steps */}
              <div>
                <h4 className="text-lg font-semibold mb-3">Learning Steps</h4>
                <div className="space-y-4">
                  {learningPlan.learning_steps.map((step, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <div className="flex items-start space-x-3">
                        <div className="flex-shrink-0 w-8 h-8 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center text-sm font-semibold">
                          {step.step}
                        </div>
                        <div className="flex-1">
                          <h5 className="font-semibold text-gray-900 mb-1">
                            {step.title}
                          </h5>
                          <p className="text-gray-600 text-sm mb-2">
                            {step.description}
                          </p>
                          <div className="text-xs text-gray-500 mb-2">
                            Duration: {step.duration}
                          </div>
                          
                          {step.resources.length > 0 && (
                            <div className="mb-2">
                              <span className="text-xs font-medium text-gray-700">Resources:</span>
                              <ul className="list-disc list-inside text-xs text-gray-600 ml-2">
                                {step.resources.map((resource, idx) => (
                                  <li key={idx}>{resource}</li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {step.exercises.length > 0 && (
                            <div>
                              <span className="text-xs font-medium text-gray-700">Exercises:</span>
                              <ul className="list-disc list-inside text-xs text-gray-600 ml-2">
                                {step.exercises.map((exercise, idx) => (
                                  <li key={idx}>{exercise}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex justify-end space-x-3 pt-6 border-t">
                <button
                  onClick={onClose}
                  className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleApprove}
                  className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                >
                  Approve & Save
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LearningPlanModal;
