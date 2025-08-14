import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { GeneratedLearningPlan, LearningStepDetail } from '../types/api';
import LearningRoadmap from './LearningRoadmap';
import { useLearningPlan } from '../contexts/LearningPlanContext';

const RoadmapPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { learningPlan } = location.state as { learningPlan: GeneratedLearningPlan };
  const { setCurrentPlan, currentPlan, resetProgress } = useLearningPlan();

  // Set the current plan in context when component mounts
  useEffect(() => {
    setCurrentPlan(learningPlan);
  }, [learningPlan, setCurrentPlan]);

  const currentLearningPlan = currentPlan || learningPlan;

  const handleStepClick = (step: LearningStepDetail) => {
    const stepIndex = currentLearningPlan.learning_steps.findIndex(s => s.step === step.step);
    navigate(`/step/${step.step}`, {
      state: {
        step,
        learningPlan: currentLearningPlan,
        stepIndex
      }
    });
  };



  const handleBackToHome = () => {
    navigate('/');
  };

  const completedSteps = currentLearningPlan.learning_steps.filter(step => step.completed).length;
  const totalSteps = currentLearningPlan.learning_steps.length;
  const progressPercentage = (completedSteps / totalSteps) * 100;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-4">
            <div className="flex items-center space-x-4">
              <button
                onClick={handleBackToHome}
                className="text-gray-600 hover:text-gray-900"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">
                  Learning Roadmap
                </h1>
                <p className="text-sm text-gray-600">
                  {currentLearningPlan.title}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-600">Progress</p>
                <p className="text-lg font-semibold text-gray-900">
                  {completedSteps} / {totalSteps} steps
                </p>
              </div>
              <div className="w-24 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progressPercentage}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <LearningRoadmap 
        learningPlan={currentLearningPlan} 
        onStepClick={handleStepClick} 
      />

      {/* Quick Actions */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="flex flex-wrap gap-4">
            <button
              onClick={() => {
                const firstIncompleteStep = currentLearningPlan.learning_steps.find(step => !step.completed);
                if (firstIncompleteStep) {
                  const stepIndex = currentLearningPlan.learning_steps.findIndex(s => s.step === firstIncompleteStep.step);
                  navigate(`/step/${firstIncompleteStep.step}`, {
                    state: {
                      step: firstIncompleteStep,
                      learningPlan: currentLearningPlan,
                      stepIndex
                    }
                  });
                }
              }}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Continue Learning
            </button>
            <button
              onClick={() => {
                resetProgress();
              }}
              className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
            >
              Reset Progress
            </button>
            <button
              onClick={() => {
                // Export progress (you could implement this)
                const progressData = {
                  learningPlan: currentLearningPlan,
                  completedSteps: currentLearningPlan.learning_steps.filter(step => step.completed).map(step => step.step),
                  timestamp: new Date().toISOString()
                };
                const dataStr = JSON.stringify(progressData, null, 2);
                const dataBlob = new Blob([dataStr], { type: 'application/json' });
                const url = URL.createObjectURL(dataBlob);
                const link = document.createElement('a');
                link.href = url;
                link.download = `learning-progress-${currentLearningPlan.title.replace(/\s+/g, '-').toLowerCase()}.json`;
                link.click();
                URL.revokeObjectURL(url);
              }}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
            >
              Export Progress
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RoadmapPage;
