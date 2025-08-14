import axios from 'axios';
import {
  SearchRequest,
  SearchResponse,
  GeneratePlanRequest,
  GeneratePlanResponse,
  UserLogin,
  UserCreate,
  Token,
  User,
  CodingExerciseSubmission,
  CodingExerciseValidation
} from '../types/api';

class ApiService {
  private baseURL: string;

  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    
    // Add request interceptor to include auth token
    axios.interceptors.request.use(
      (config: any) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error: any) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle auth errors
    axios.interceptors.response.use(
      (response: any) => response,
      (error: any) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication methods
  async login(credentials: UserLogin): Promise<Token> {
    const response = await axios.post<Token>(`${this.baseURL}/login`, credentials);
    return response.data;
  }

  async register(userData: UserCreate): Promise<User> {
    const response = await axios.post<User>(`${this.baseURL}/register`, userData);
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await axios.get<User>(`${this.baseURL}/users/me`);
    return response.data;
  }

  // Repository search methods
  async searchRepositories(searchRequest: SearchRequest): Promise<SearchResponse> {
    const response = await axios.post<SearchResponse>(`${this.baseURL}/search-repo`, searchRequest);
    return response.data;
  }

  // Learning plan generation methods
  async generateLearningPlan(request: GeneratePlanRequest): Promise<GeneratePlanResponse> {
    const response = await axios.post<GeneratePlanResponse>(`${this.baseURL}/generate-plan`, request);
    return response.data;
  }

  // Code validation methods
  async validateCode(submission: CodingExerciseSubmission): Promise<CodingExerciseValidation> {
    const response = await axios.post<CodingExerciseValidation>(`${this.baseURL}/validate-code`, submission);
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await axios.get<{ status: string }>(`${this.baseURL}/health`);
    return response.data;
  }

  // Utility methods
  setToken(token: string) {
    localStorage.setItem('token', token);
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  removeToken() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}

export const apiService = new ApiService();
export default apiService;
