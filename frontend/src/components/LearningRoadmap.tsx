import React from 'react';
import { GeneratedLearningPlan, LearningStepDetail } from '../types/api';

interface LearningRoadmapProps {
  learningPlan: GeneratedLearningPlan;
  onStepClick: (step: LearningStepDetail) => void;
}

const LearningRoadmap: React.FC<LearningRoadmapProps> = ({ learningPlan, onStepClick }) => {
  const handleStepClick = (step: LearningStepDetail) => {
    onStepClick(step);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'beginner':
        return 'bg-green-100 text-green-800';
      case 'intermediate':
        return 'bg-yellow-100 text-yellow-800';
      case 'advanced':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Plan Header */}
      <div className="bg-white rounded-lg shadow-sm border p-6 mb-8">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {learningPlan.title}
            </h1>
            <p className="text-gray-600 text-lg mb-4">
              {learningPlan.description}
            </p>
          </div>
          <div className="flex flex-col items-end space-y-2">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(learningPlan.difficulty_level)}`}>
              {learningPlan.difficulty_level}
            </span>
            <span className="text-sm text-gray-500">
              {learningPlan.estimated_duration}
            </span>
          </div>
        </div>

        {/* Prerequisites */}
        {learningPlan.prerequisites.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Prerequisites</h3>
            <div className="flex flex-wrap gap-2">
              {learningPlan.prerequisites.map((prereq, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                >
                  {prereq}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Learning Objectives */}
        {learningPlan.learning_objectives.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Learning Objectives</h3>
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
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Technologies Covered</h3>
            <div className="flex flex-wrap gap-2">
              {learningPlan.technologies_covered.map((tech, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm"
                >
                  {tech}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Learning Steps Roadmap */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Learning Roadmap</h2>
        
        <div className="space-y-4">
          {learningPlan.learning_steps.map((step, index) => (
            <div
              key={step.step}
              className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md ${
                step.completed
                  ? 'border-green-500 bg-green-50'
                  : 'border-gray-200 bg-white hover:border-blue-300'
              }`}
              onClick={() => handleStepClick(step)}
            >
              <div className="flex items-start space-x-4">
                {/* Step Number */}
                <div className={`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold ${
                  step.completed
                    ? 'bg-green-500 text-white'
                    : 'bg-blue-100 text-blue-600'
                }`}>
                  {step.completed ? '✓' : step.step}
                </div>

                {/* Step Content */}
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {step.title}
                    </h3>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-500">
                        {step.duration}
                      </span>
                      {step.completed && (
                        <span className="text-green-600 text-sm font-medium">
                          Completed
                        </span>
                      )}
                    </div>
                  </div>
                  
                  <p className="text-gray-600 mb-3">
                    {step.description}
                  </p>

                  {/* Resources and Exercises Preview */}
                  <div className="flex flex-wrap gap-2 text-sm">
                    {step.resources.length > 0 && (
                      <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded">
                        {step.resources.length} resource{step.resources.length !== 1 ? 's' : ''}
                      </span>
                    )}
                    {step.exercises.length > 0 && (
                      <span className="px-2 py-1 bg-orange-50 text-orange-700 rounded">
                        {step.exercises.length} exercise{step.exercises.length !== 1 ? 's' : ''}
                      </span>
                    )}
                  </div>
                </div>

                {/* Arrow Icon */}
                <div className="flex-shrink-0 text-gray-400">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Progress Summary */}
        <div className="mt-8 pt-6 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Progress</h3>
              <p className="text-sm text-gray-600">
                {learningPlan.learning_steps.filter(step => step.completed).length} of {learningPlan.learning_steps.length} steps completed
              </p>
            </div>
            <div className="w-32 bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{
                  width: `${(learningPlan.learning_steps.filter(step => step.completed).length / learningPlan.learning_steps.length) * 100}%`
                }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LearningRoadmap;
