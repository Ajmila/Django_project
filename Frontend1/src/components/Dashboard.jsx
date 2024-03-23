// src/components/Dashboard.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();
  const [showConfirm, setShowConfirm] = useState(false);

  const handleViewClass = () => {
    navigate('/class');
  };

  const handleTakeAttendance = () => {
    navigate('/attendance');
  };

  const handleLogout = () => {
    setShowConfirm(true);
  };

  const confirmLogout = () => {
    setShowConfirm(false);
    navigate('/login');
  };

  const cancelLogout = () => {
    setShowConfirm(false);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="absolute top-0 right-0 m-4">
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Logout
        </button>
      </div>
      <div className="max-w-md w-full space-y-8">
        <h2 className="text-center text-3xl font-extrabold text-gray-900">Dashboard</h2>
        <div className="flex justify-center space-x-4">
          <button
            onClick={handleViewClass}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            View Class
          </button>
          <button
            onClick={handleTakeAttendance}
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Take Attendance
          </button>
        </div>
      </div>
      {showConfirm && (
        <div className="fixed inset-0 flex items-center justify-center z-50">
          <div className="bg-white p-4 rounded shadow">
            <p>Do you want to log out?</p>
            <div className="flex justify-end space-x-4 mt-4">
              <button
                onClick={confirmLogout}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Yes
              </button>
              <button
                onClick={cancelLogout}
                className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-700"
              >
                No
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
