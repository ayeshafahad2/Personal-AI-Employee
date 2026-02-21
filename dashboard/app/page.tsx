'use client';

import dynamic from 'next/dynamic';
import { useDashboardData } from '../hooks/useDashboardData';

// Dynamically import components that might use browser APIs
const DashboardHeader = dynamic(() => import('../components/DashboardHeader'), { ssr: false });
const ActivityFeed = dynamic(() => import('../components/ActivityFeed'), { ssr: false });
const StatsCards = dynamic(() => import('../components/StatsCards'), { ssr: false });
const TaskManager = dynamic(() => import('../components/TaskManager'), { ssr: false });
const CommunicationPanel = dynamic(() => import('../components/CommunicationPanel'), { ssr: false });
const ApprovalQueue = dynamic(() => import('../components/ApprovalQueue'), { ssr: false });

export default function DashboardPage() {
  const { data: dashboardData, loading, error } = useDashboardData();

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Initializing AI Employee Dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          <div className="mx-auto bg-red-100 text-red-600 rounded-full w-16 h-16 flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-1">Connection Error</h3>
          <p className="text-gray-600 mb-4">Unable to connect to the AI Employee system. Please check your connection and try again.</p>
          <button 
            onClick={() => window.location.reload()}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">No dashboard data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Background decoration */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-48 -right-48 w-96 h-96 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full opacity-50 blur-3xl"></div>
        <div className="absolute -bottom-48 -left-48 w-96 h-96 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full opacity-50 blur-3xl"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <DashboardHeader />

        {/* Stats Cards */}
        <StatsCards stats={dashboardData.stats} />

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-8">
            {/* Activity Feed */}
            <ActivityFeed activities={dashboardData.recentActivity} />
            
            {/* Task Manager */}
            <TaskManager tasks={dashboardData.pendingTasks} />
          </div>

          {/* Right Column */}
          <div className="space-y-8">
            {/* Communication Panel */}
            <CommunicationPanel communications={dashboardData.communications} />
            
            {/* Approval Queue */}
            <ApprovalQueue approvals={dashboardData.approvals} />
          </div>
        </div>
      </div>
    </div>
  );
}