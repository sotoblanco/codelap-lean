import React from 'react';
import { Link, NavLink } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLearningPlan } from '../contexts/LearningPlanContext';

const Navbar: React.FC = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const { currentPlan } = useLearningPlan();

  return (
    <nav className="bg-white border-b shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="h-14 flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <Link to={isAuthenticated ? '/' : '/login'} className="text-lg font-semibold text-gray-900">
              CodeLap Lean
            </Link>
            {isAuthenticated && (
              <div className="hidden md:flex items-center space-x-4">
                <NavLink
                  to="/"
                  className={({ isActive }) =>
                    `text-sm ${isActive ? 'text-indigo-600 font-medium' : 'text-gray-600 hover:text-gray-900'}`
                  }
                >
                  Home
                </NavLink>
                <NavLink
                  to={currentPlan ? '/roadmap' : '/'}
                  className={({ isActive }) =>
                    `text-sm ${isActive ? 'text-indigo-600 font-medium' : 'text-gray-600 hover:text-gray-900'} ${
                      currentPlan ? '' : 'opacity-50 cursor-not-allowed'
                    }`
                  }
                  onClick={(e) => {
                    if (!currentPlan) {
                      e.preventDefault();
                    }
                  }}
                >
                  Roadmap
                </NavLink>
              </div>
            )}
          </div>

          <div className="flex items-center space-x-4">
            {!isAuthenticated ? (
              <div className="flex items-center space-x-3">
                <NavLink
                  to="/login"
                  className={({ isActive }) =>
                    `text-sm ${isActive ? 'text-indigo-600 font-medium' : 'text-gray-600 hover:text-gray-900'}`
                  }
                >
                  Login
                </NavLink>
                <NavLink
                  to="/register"
                  className={({ isActive }) =>
                    `text-sm ${isActive ? 'text-indigo-600 font-medium' : 'text-gray-600 hover:text-gray-900'}`
                  }
                >
                  Register
                </NavLink>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <span className="hidden sm:inline text-sm text-gray-600">
                  {user?.full_name || user?.username}
                </span>
                <button
                  onClick={logout}
                  className="text-sm text-gray-600 hover:text-gray-900"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;


