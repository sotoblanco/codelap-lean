import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { useLearningPlan } from '../contexts/LearningPlanContext';
import { apiService } from '../services/api';
import { CodingExercise, CodingExerciseValidation } from '../types/api';
import FillInTheBlankEditor from './FillInTheBlankEditor';

interface StepPageProps {
  // Add any props if needed
}

const StepPage: React.FC<StepPageProps> = () => {
  const { stepNumber } = useParams<{ stepNumber: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { currentPlan, completeStep, getStepCompletion } = useLearningPlan();
  
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0);
  const [userCode, setUserCode] = useState('');
  const [validationResult, setValidationResult] = useState<CodingExerciseValidation | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showHints, setShowHints] = useState(false);
  const [completedExercises, setCompletedExercises] = useState<Set<string>>(new Set());

  const stepNum = parseInt(stepNumber || '1');
  
  // Try to get step from multiple sources
  let step = currentPlan?.learning_steps.find(s => s.step === stepNum);
  
  // If not found in context, try to get from location state
  if (!step && location.state?.step) {
    step = location.state.step;
  }
  
  // If still not found, try to get from location state learning plan
  if (!step && location.state?.learningPlan) {
    step = location.state.learningPlan.learning_steps.find((s: any) => s.step === stepNum);
  }
  
  const currentExercise = step?.coding_exercises?.[currentExerciseIndex];
  
  // Debug logging
  console.log('StepPage Debug:', {
    stepNumber,
    stepNum,
    hasCurrentPlan: !!currentPlan,
    currentPlanSteps: currentPlan?.learning_steps?.length,
    hasLocationState: !!location.state,
    locationStateStep: !!location.state?.step,
    locationStateLearningPlan: !!location.state?.learningPlan,
    foundStep: !!step,
    stepTitle: step?.title,
    hasCodingExercises: !!step?.coding_exercises,
    codingExercisesCount: step?.coding_exercises?.length,
    currentExercise: !!currentExercise
  });

  useEffect(() => {
    if (currentExercise) {
      // Load saved code for this exercise
      const savedCode = localStorage.getItem(`exercise_${currentExercise.id}`);
      if (savedCode) {
        setUserCode(savedCode);
      } else {
        setUserCode(currentExercise.code_template);
      }
    }
  }, [currentExercise]);

  const handleCodeChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newCode = e.target.value;
    setUserCode(newCode);
    
    // Auto-save code
    if (currentExercise) {
      localStorage.setItem(`exercise_${currentExercise.id}`, newCode);
    }
  };

  const handleSubmit = async () => {
    if (!currentExercise) return;

    setIsSubmitting(true);
    try {
      const submission = {
        exercise_id: currentExercise.id,
        user_code: userCode,
        step_number: stepNum
      };

      const result = await apiService.validateCode(submission);
      setValidationResult(result);

      if (result.is_correct) {
        setCompletedExercises(prev => new Set(Array.from(prev).concat(currentExercise.id)));
        
        // Move to next exercise or complete step
        if (currentExerciseIndex < (step?.coding_exercises.length || 0) - 1) {
          setCurrentExerciseIndex(prev => prev + 1);
          setValidationResult(null);
        } else {
          // All exercises completed for this step
          completeStep(stepNum);
        }
      }
    } catch (error) {
      console.error('Error validating code:', error);
      setValidationResult({
        exercise_id: currentExercise.id,
        is_correct: false,
        feedback: 'Error validating code. Please try again.',
        hints: [],
        score: 0,
        error_message: 'Network error'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNextExercise = () => {
    if (currentExerciseIndex < (step?.coding_exercises.length || 0) - 1) {
      setCurrentExerciseIndex(prev => prev + 1);
      setValidationResult(null);
      setShowHints(false);
    }
  };

  const handlePreviousExercise = () => {
    if (currentExerciseIndex > 0) {
      setCurrentExerciseIndex(prev => prev - 1);
      setValidationResult(null);
      setShowHints(false);
    }
  };

  const handleReset = () => {
    setUserCode(currentExercise?.code_template || '');
    setValidationResult(null);
    setShowHints(false);
  };

  const getProgressPercentage = () => {
    if (!hasCodingExercises) return 0;
    return (completedExercises.size / totalExercises) * 100;
  };

  if (!step) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Step not found</h1>
            <p className="text-gray-600 mb-4">
              Step {stepNum} could not be loaded. This might be because:
            </p>
            <ul className="text-gray-600 mb-6 text-left max-w-md mx-auto">
              <li>• No learning plan is currently active</li>
              <li>• The step doesn't exist in the current plan</li>
              <li>• There was an error loading the step data</li>
            </ul>
            <div className="space-x-4">
              <button
                onClick={() => navigate('/roadmap')}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Back to Roadmap
              </button>
              <button
                onClick={() => navigate('/')}
                className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
              >
                Go to Home
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Check if step has coding exercises
  const hasCodingExercises = step.coding_exercises && step.coding_exercises.length > 0;
  const totalExercises = hasCodingExercises ? step.coding_exercises.length : 0;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Step {step.step}: {step.title}
              </h1>
              <p className="text-gray-600 mt-1">{step.description}</p>
            </div>
            <div className="flex items-center space-x-4">
              {hasCodingExercises && (
                <div className="text-right">
                  <div className="text-sm text-gray-600">Progress</div>
                  <div className="text-lg font-semibold text-blue-600">
                    {completedExercises.size} / {totalExercises}
                  </div>
                </div>
              )}
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${getProgressPercentage()}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Panel - Introduction and Resources */}
          <div className="space-y-6">
            {/* Step Introduction */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Introduction</h2>
              <p className="text-gray-700 leading-relaxed">{step.description}</p>
              
              <div className="mt-6">
                <h3 className="text-lg font-medium text-gray-900 mb-3">Duration</h3>
                <p className="text-gray-600">{step.duration}</p>
              </div>
            </div>

            {/* Resources */}
            {step.resources.length > 0 && (
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-3">Resources</h3>
                <ul className="space-y-2">
                  {step.resources.map((resource, index) => (
                    <li key={index} className="flex items-center text-gray-700">
                      <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                      {resource}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Exercise Navigation */}
            {hasCodingExercises && (
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-3">Exercises</h3>
                <div className="space-y-2">
                  {step.coding_exercises.map((exercise, index) => (
                    <button
                      key={exercise.id}
                      onClick={() => setCurrentExerciseIndex(index)}
                      className={`w-full text-left p-3 rounded-lg border transition-colors ${
                        index === currentExerciseIndex
                          ? 'border-blue-500 bg-blue-50'
                          : completedExercises.has(exercise.id)
                          ? 'border-green-500 bg-green-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-medium text-gray-900">
                          Exercise {index + 1}: {exercise.title}
                        </span>
                        <div className="flex items-center space-x-2">
                          <span className={`text-sm px-2 py-1 rounded ${
                            exercise.difficulty === 'beginner' ? 'bg-green-100 text-green-800' :
                            exercise.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {exercise.difficulty}
                          </span>
                          {completedExercises.has(exercise.id) && (
                            <span className="text-green-600">✓</span>
                          )}
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right Panel - Coding Exercise */}
          <div className="space-y-6">
            {!hasCodingExercises ? (
              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-center">
                  <h2 className="text-xl font-semibold text-gray-900 mb-4">
                    No Coding Exercises Available
                  </h2>
                  <p className="text-gray-600 mb-4">
                    This step doesn't have any coding exercises yet. You can still review the learning materials and resources.
                  </p>
                  <div className="space-y-4">
                    <div className="bg-blue-50 rounded-lg p-4">
                      <h3 className="font-medium text-blue-900 mb-2">Duration</h3>
                      <p className="text-blue-700">{step.duration}</p>
                    </div>
                    {step.resources && step.resources.length > 0 && (
                      <div className="bg-green-50 rounded-lg p-4">
                        <h3 className="font-medium text-green-900 mb-2">Resources</h3>
                        <ul className="text-green-700 space-y-1">
                          {step.resources.map((resource, index) => (
                            <li key={index}>• {resource}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {step.exercises && step.exercises.length > 0 && (
                      <div className="bg-orange-50 rounded-lg p-4">
                        <h3 className="font-medium text-orange-900 mb-2">Exercises</h3>
                        <ul className="text-orange-700 space-y-1">
                          {step.exercises.map((exercise, index) => (
                            <li key={index}>• {exercise}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                  <div className="mt-6">
                    <button
                      onClick={() => completeStep(stepNum)}
                      className="bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700"
                    >
                      Mark as Complete
                    </button>
                  </div>
                </div>
              </div>
            ) : currentExercise && (
              <>
                {/* Exercise Header */}
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-semibold text-gray-900">
                      Exercise {currentExerciseIndex + 1}: {currentExercise.title}
                    </h2>
                    <span className={`text-sm px-3 py-1 rounded-full ${
                      currentExercise.difficulty === 'beginner' ? 'bg-green-100 text-green-800' :
                      currentExercise.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {currentExercise.difficulty}
                    </span>
                  </div>
                  
                  <p className="text-gray-700 mb-4">{currentExercise.description}</p>
                  
                  {currentExercise.expected_output && (
                    <div className="bg-gray-50 rounded-lg p-4 mb-4">
                      <h4 className="text-sm font-medium text-gray-900 mb-2">Expected Output:</h4>
                      <code className="text-sm text-gray-700 bg-white px-2 py-1 rounded">
                        {currentExercise.expected_output}
                      </code>
                    </div>
                  )}
                </div>

                {/* Code Editor */}
                <div className="bg-white rounded-lg shadow">
                  <div className="border-b px-6 py-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-medium text-gray-900">
                        {currentExercise.blanks && currentExercise.blanks.length > 0 
                          ? 'Fill-in-the-Blank Exercise' 
                          : 'Code Editor'
                        }
                      </h3>
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => setShowHints(!showHints)}
                          className="text-sm text-blue-600 hover:text-blue-700"
                        >
                          {showHints ? 'Hide' : 'Show'} Hints
                        </button>
                        <button
                          onClick={handleReset}
                          className="text-sm text-gray-600 hover:text-gray-700"
                        >
                          Reset
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  <div className="p-6">
                    {currentExercise.blanks && currentExercise.blanks.length > 0 ? (
                      <FillInTheBlankEditor
                        codeTemplate={currentExercise.code_template}
                        blanks={currentExercise.blanks}
                        onCodeChange={setUserCode}
                        userCode={userCode}
                        isSubmitting={isSubmitting}
                      />
                    ) : (
                      <textarea
                        value={userCode}
                        onChange={handleCodeChange}
                        className="w-full h-64 p-4 font-mono text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                        placeholder="Write your code here..."
                      />
                    )}
                  </div>
                  
                  {/* Hints */}
                  {showHints && currentExercise.hints.length > 0 && (
                    <div className="border-t bg-yellow-50 px-6 py-4">
                      <h4 className="text-sm font-medium text-gray-900 mb-2">Hints:</h4>
                      <ul className="space-y-1">
                        {currentExercise.hints.map((hint, index) => (
                          <li key={index} className="text-sm text-gray-700">
                            • {hint}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  {/* Validation Result */}
                  {validationResult && (
                    <div className={`border-t px-6 py-4 ${
                      validationResult.is_correct ? 'bg-green-50' : 'bg-red-50'
                    }`}>
                      <div className="flex items-center justify-between mb-2">
                        <h4 className={`text-sm font-medium ${
                          validationResult.is_correct ? 'text-green-900' : 'text-red-900'
                        }`}>
                          {validationResult.is_correct ? '✓ Correct!' : '✗ Try Again'}
                        </h4>
                        <span className={`text-sm px-2 py-1 rounded ${
                          validationResult.is_correct ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'
                        }`}>
                          Score: {validationResult.score}/100
                        </span>
                      </div>
                      <p className={`text-sm ${
                        validationResult.is_correct ? 'text-green-700' : 'text-red-700'
                      }`}>
                        {validationResult.feedback}
                      </p>
                      {validationResult.error_message && (
                        <div className="mt-2 p-2 bg-red-100 rounded">
                          <code className="text-xs text-red-800">{validationResult.error_message}</code>
                        </div>
                      )}
                      {validationResult.execution_result && (
                        <div className="mt-2 p-2 bg-gray-100 rounded">
                          <code className="text-xs text-gray-800">{validationResult.execution_result}</code>
                        </div>
                      )}
                    </div>
                  )}
                  
                  {/* Action Buttons */}
                  <div className="border-t px-6 py-4 bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div className="flex space-x-3">
                        <button
                          onClick={handlePreviousExercise}
                          disabled={currentExerciseIndex === 0}
                          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          Previous
                        </button>
                        <button
                          onClick={handleNextExercise}
                          disabled={currentExerciseIndex >= (step.coding_exercises.length - 1)}
                          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          Next
                        </button>
                      </div>
                      
                      <button
                        onClick={handleSubmit}
                        disabled={isSubmitting || !userCode.trim()}
                        className="px-6 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {isSubmitting ? 'Submitting...' : 'Submit Code'}
                      </button>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>

        {/* Bottom Navigation */}
        <div className="mt-8 flex items-center justify-between">
          <button
            onClick={() => navigate('/roadmap')}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            ← Back to Roadmap
          </button>
          
          <div className="flex space-x-3">
            <button
              onClick={() => navigate(`/step/${stepNum - 1}`)}
              disabled={stepNum <= 1}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous Step
            </button>
            <button
              onClick={() => navigate(`/step/${stepNum + 1}`)}
              disabled={!step || stepNum >= (currentPlan?.learning_steps.length || 0)}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next Step
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StepPage;
