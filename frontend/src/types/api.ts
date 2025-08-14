// API Response Types

export interface User {
  id: number;
  username: string;
  email?: string;
  full_name?: string;
  disabled: boolean;
  created_at: string;
  updated_at?: string;
}

export interface GitHubRepositoryInfo {
  id: number;
  name: string;
  full_name: string;
  description?: string;
  html_url: string;
  clone_url: string;
  language?: string;
  languages?: string[];
  topics?: string[];
  stars: number;
  forks: number;
  watchers: number;
  open_issues: number;
  size?: number;
  created_at?: string;
  updated_at?: string;
  readme_preview?: string;
  default_branch?: string;
  license?: string;
  archived: boolean;
  fork: boolean;
  private: boolean;
}

export interface SearchRequest {
  query: string;
  limit?: number;
}

export interface SearchResponse {
  query: string;
  search_type: string;
  repositories: GitHubRepositoryInfo[];
  ai_prerequisites?: string[];
  total_count: number;
}

export interface LearningStepDetail {
  step: number;
  title: string;
  description: string;
  duration: string;
  resources: string[];
  exercises: string[];
  completed: boolean;
}

export interface CodingExercise {
  id: string;
  title: string;
  description: string;
  difficulty: string;
  code_template: string;
  solution: string;
  hints: string[];
  validation_rules: string[];
  expected_output?: string;
  test_cases: any[];
  blanks?: Array<{
    placeholder: string;
    correct_answer: string;
    hint: string;
  }>;
}

export interface EnhancedLearningStepDetail extends LearningStepDetail {
  coding_exercises: CodingExercise[];
  exercises_completed: number;
  total_exercises: number;
}

export interface GeneratedLearningPlan {
  title: string;
  description: string;
  difficulty_level: string;
  estimated_duration: string;
  learning_steps: EnhancedLearningStepDetail[];
  prerequisites: string[];
  learning_objectives: string[];
  technologies_covered: string[];
}

export interface GeneratePlanRequest {
  repository_id?: number;
  repository_url?: string;
  repository_info?: GitHubRepositoryInfo;
}

export interface GeneratePlanResponse {
  success: boolean;
  learning_plan?: GeneratedLearningPlan;
  repository_info?: GitHubRepositoryInfo;
  error_message?: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface UserCreate {
  username: string;
  password: string;
  email?: string;
  full_name?: string;
}

export interface CodingExerciseSubmission {
  exercise_id: string;
  user_code: string;
  step_number: number;
}

export interface CodingExerciseValidation {
  exercise_id: string;
  is_correct: boolean;
  feedback: string;
  hints: string[];
  score: number;
  execution_result?: string;
  error_message?: string;
}
