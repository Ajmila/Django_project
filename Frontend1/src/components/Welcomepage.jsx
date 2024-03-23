// src/components/WelcomePage.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

const WelcomePage = () => {
 const navigate = useNavigate();

 const handleLoginRedirect = () => {
    navigate('/login');
 };

 return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Welcome to Our Application
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Please sign in to continue.
          </p>
        </div>
        <div>
          <button
            onClick={handleLoginRedirect}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Sign in
          </button>
        </div>
      </div>
    </div>
 );
};

export default WelcomePage;
