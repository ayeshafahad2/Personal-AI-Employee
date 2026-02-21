import React from 'react';

const DashboardHeader = () => {
  return (
    <div className="mb-8">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Employee Dashboard</h1>
          <p className="mt-2 text-sm text-gray-600">
            Your life and business on autopilot • Local-first, agent-driven, human-in-the-loop
          </p>
        </div>
        <div className="mt-4 md:mt-0 flex items-center space-x-4">
          <div className="flex items-center">
            <div className="w-3 h-3 rounded-full bg-green-500 mr-2 animate-pulse"></div>
            <span className="text-sm font-medium text-gray-700">Online</span>
          </div>
          <div className="bg-white px-4 py-2 rounded-lg shadow-sm border border-gray-200">
            <span className="text-sm font-medium text-gray-700">System Status: Operational</span>
          </div>
        </div>
      </div>
      
      <div className="mt-6 bg-gradient-to-r from-blue-600 to-indigo-700 rounded-xl p-6 text-white shadow-lg">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
          </div>
          <div className="ml-4">
            <h2 className="text-xl font-semibold">Personal AI Employee</h2>
            <p className="mt-1 text-blue-100">
              Proactively managing your personal and business affairs 24/7 • Last activity: Just now
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardHeader;