import React from 'react';
import { GitHubRepositoryInfo } from '../types/api';

interface RepositoryCardProps {
  repository: GitHubRepositoryInfo;
  onSelect: (repository: GitHubRepositoryInfo) => void;
  isSelected?: boolean;
}

const RepositoryCard: React.FC<RepositoryCardProps> = ({
  repository,
  onSelect,
  isSelected = false,
}) => {
  return (
    <div
      className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md ${
        isSelected
          ? 'border-indigo-500 bg-indigo-50 shadow-md'
          : 'border-gray-200 bg-white hover:border-gray-300'
      }`}
      onClick={() => onSelect(repository)}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">
            {repository.full_name}
          </h3>
          {repository.description && (
            <p className="text-gray-600 text-sm mb-3 line-clamp-2">
              {repository.description}
            </p>
          )}
          
          <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
            {repository.language && (
              <span className="flex items-center">
                <span className="w-3 h-3 rounded-full bg-blue-500 mr-1"></span>
                {repository.language}
              </span>
            )}
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              {repository.stars.toLocaleString()}
            </span>
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
              {repository.forks.toLocaleString()}
            </span>
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              {repository.open_issues}
            </span>
          </div>

          {repository.topics && repository.topics.length > 0 && (
            <div className="flex flex-wrap gap-1 mb-3">
              {repository.topics.slice(0, 5).map((topic, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                >
                  {topic}
                </span>
              ))}
              {repository.topics.length > 5 && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                  +{repository.topics.length - 5} more
                </span>
              )}
            </div>
          )}

          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>
              Updated {repository.updated_at ? new Date(repository.updated_at).toLocaleDateString() : 'Unknown'}
            </span>
            <div className="flex items-center space-x-2">
              {repository.archived && (
                <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded">
                  Archived
                </span>
              )}
              {repository.fork && (
                <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded">
                  Fork
                </span>
              )}
            </div>
          </div>
        </div>

        <div className="ml-4">
          <button
            className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
              isSelected
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
            onClick={(e) => {
              e.stopPropagation();
              onSelect(repository);
            }}
          >
            {isSelected ? 'Selected' : 'Select'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default RepositoryCard;
