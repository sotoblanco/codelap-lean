import React, { createContext, useContext, useState, ReactNode } from 'react';
import { GeneratedLearningPlan, LearningStepDetail } from '../types/api';

interface LearningPlanContextType {
  currentPlan: GeneratedLearningPlan | null;
  setCurrentPlan: (plan: GeneratedLearningPlan) => void;
  completeStep: (stepNumber: number) => void;
  getStepCompletion: (stepNumber: number) => boolean;
  resetProgress: () => void;
}

const LearningPlanContext = createContext<LearningPlanContextType | undefined>(undefined);

export const useLearningPlan = () => {
  const context = useContext(LearningPlanContext);
  if (context === undefined) {
    throw new Error('useLearningPlan must be used within a LearningPlanProvider');
  }
  return context;
};

interface LearningPlanProviderProps {
  children: ReactNode;
}

export const LearningPlanProvider: React.FC<LearningPlanProviderProps> = ({ children }) => {
  const [currentPlan, setCurrentPlanState] = useState<GeneratedLearningPlan | null>(null);

  const setCurrentPlan = (plan: GeneratedLearningPlan) => {
    // Load completion status from localStorage
    const updatedSteps = plan.learning_steps.map(step => {
      const isCompleted = localStorage.getItem(`step_${step.step}_completed`) === 'true';
      return { ...step, completed: isCompleted };
    });
    
    setCurrentPlanState({
      ...plan,
      learning_steps: updatedSteps
    });
  };

  const completeStep = (stepNumber: number) => {
    if (!currentPlan) return;

    const updatedSteps = currentPlan.learning_steps.map(step => {
      if (step.step === stepNumber) {
        return { ...step, completed: true };
      }
      return step;
    });

    setCurrentPlanState({
      ...currentPlan,
      learning_steps: updatedSteps
    });

    // Save to localStorage
    localStorage.setItem(`step_${stepNumber}_completed`, 'true');
  };

  const getStepCompletion = (stepNumber: number): boolean => {
    return localStorage.getItem(`step_${stepNumber}_completed`) === 'true';
  };

  const resetProgress = () => {
    if (!currentPlan) return;

    // Clear all localStorage entries for this plan
    currentPlan.learning_steps.forEach(step => {
      localStorage.removeItem(`step_${step.step}_completed`);
      localStorage.removeItem(`step_${step.step}_code`);
    });

    // Reset the plan state
    const resetSteps = currentPlan.learning_steps.map(step => ({
      ...step,
      completed: false
    }));

    setCurrentPlanState({
      ...currentPlan,
      learning_steps: resetSteps
    });
  };

  const value: LearningPlanContextType = {
    currentPlan,
    setCurrentPlan,
    completeStep,
    getStepCompletion,
    resetProgress
  };

  return (
    <LearningPlanContext.Provider value={value}>
      {children}
    </LearningPlanContext.Provider>
  );
};
