import { GeneratedLearningPlan } from '../types/api';

const buildUserPlansKey = (userId: number): string => `saved_plans_user_${userId}`;

export const getSavedPlansForUser = (userId: number): GeneratedLearningPlan[] => {
  try {
    const raw = localStorage.getItem(buildUserPlansKey(userId));
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    console.error('Failed to parse saved plans from storage:', error);
    return [];
  }
};

export const setSavedPlansForUser = (userId: number, plans: GeneratedLearningPlan[]): void => {
  try {
    localStorage.setItem(buildUserPlansKey(userId), JSON.stringify(plans));
  } catch (error) {
    console.error('Failed to save plans to storage:', error);
  }
};

export const savePlanForUser = (userId: number, plan: GeneratedLearningPlan): GeneratedLearningPlan[] => {
  const existing = getSavedPlansForUser(userId);
  // Avoid duplicates by title; fall back to object equality if needed
  const alreadyExists = existing.some(p => p.title === plan.title);
  const updated = alreadyExists ? existing : [...existing, plan];
  setSavedPlansForUser(userId, updated);
  return updated;
};


