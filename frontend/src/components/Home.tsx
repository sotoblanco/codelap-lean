import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { GitHubRepositoryInfo, SearchRequest, GeneratedLearningPlan } from '../types/api';
import apiService from '../services/api';
import RepositoryCard from './RepositoryCard';
import LearningPlanModal from './LearningPlanModal';
import { getSavedPlansForUser, savePlanForUser } from '../utils/storage';

const Home: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [repositories, setRepositories] = useState<GitHubRepositoryInfo[]>([]);
  const [selectedRepository, setSelectedRepository] = useState<GitHubRepositoryInfo | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [savedPlans, setSavedPlans] = useState<GeneratedLearningPlan[]>([]);

  // Load saved plans for the current user on mount/auth change
  useEffect(() => {
    if (user?.id) {
      const plans = getSavedPlansForUser(user.id);
      setSavedPlans(plans);
    } else {
      setSavedPlans([]);
    }
  }, [user?.id]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setRepositories([]);

    try {
      const searchRequest: SearchRequest = {
        query: query.trim(),
        limit: 10,
      };

      const response = await apiService.searchRepositories(searchRequest);
      setRepositories(response.repositories);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to search repositories');
    } finally {
      setLoading(false);
    }
  };

  const handleRepositorySelect = (repository: GitHubRepositoryInfo) => {
    setSelectedRepository(repository);
    setIsModalOpen(true);
  };

  const handleApprovePlan = (learningPlan: GeneratedLearningPlan) => {
    if (!user?.id) return;
    const updated = savePlanForUser(user.id, learningPlan);
    setSavedPlans(updated);
    alert('Learning plan approved and saved!');
  };

  const handleViewRoadmap = (learningPlan: GeneratedLearningPlan) => {
    navigate('/roadmap', { state: { learningPlan } });
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">CodeLap Lean</h1>
              <p className="text-sm text-gray-600">AI-Powered Learning Plan Generator</p>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                Welcome, {user?.full_name || user?.username}!
              </span>
              <button
                onClick={handleLogout}
                className="text-sm text-gray-600 hover:text-gray-900"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Section */}
        <div className="mb-8">
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Search GitHub Repositories
            </h2>
            <form onSubmit={handleSearch} className="flex space-x-4">
              <div className="flex-1">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Enter GitHub URL or search term (e.g., 'machine learning', 'https://github.com/tiangolo/fastapi')"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
              <button
                type="submit"
                disabled={loading || !query.trim()}
                className="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Searching...' : 'Search'}
              </button>
            </form>
            
            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
                <p className="text-red-600">{error}</p>
              </div>
            )}
          </div>
        </div>

        {/* Results Section */}
        {repositories.length > 0 && (
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">
                Search Results ({repositories.length} repositories)
              </h2>
              <p className="text-sm text-gray-600">
                Click on a repository to generate a learning plan
              </p>
            </div>
            
            <div className="space-y-4">
              {repositories.map((repository) => (
                <RepositoryCard
                  key={repository.id}
                  repository={repository}
                  onSelect={handleRepositorySelect}
                  isSelected={selectedRepository?.id === repository.id}
                />
              ))}
            </div>
          </div>
        )}

        {/* Saved Plans Section */}
        {savedPlans.length > 0 && (
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Saved Learning Plans ({savedPlans.length})
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {savedPlans.map((plan, index) => (
                <div key={index} className="bg-white rounded-lg shadow-sm border p-4">
                  <h3 className="font-semibold text-gray-900 mb-2">{plan.title}</h3>
                  <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                    {plan.description}
                  </p>
                  <div className="flex items-center justify-between text-sm mb-3">
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded">
                      {plan.difficulty_level}
                    </span>
                    <span className="text-gray-500">{plan.estimated_duration}</span>
                  </div>
                  <button
                    onClick={() => handleViewRoadmap(plan)}
                    className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors text-sm"
                  >
                    View Roadmap
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && repositories.length === 0 && savedPlans.length === 0 && (
          <div className="text-center py-12">
            <div className="mx-auto w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-4">
              <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Search for repositories
            </h3>
            <p className="text-gray-600">
              Enter a GitHub URL or search term to find repositories and generate learning plans.
            </p>
          </div>
        )}
      </div>

      {/* Learning Plan Modal */}
      <LearningPlanModal
        repository={selectedRepository}
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedRepository(null);
        }}
        onApprove={handleApprovePlan}
      />
    </div>
  );
};

export default Home;
