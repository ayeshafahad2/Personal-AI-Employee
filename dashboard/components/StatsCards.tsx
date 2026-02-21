import React from 'react';

interface StatsProps {
  stats: {
    emailsProcessed: number;
    whatsappMessages: number;
    tasksCompleted: number;
    pendingApprovals: number;
    uptime: string;
    systemStatus: string;
  };
}

const StatsCards = ({ stats }: StatsProps) => {
  const statItems = [
    { name: 'Emails Processed', value: stats.emailsProcessed, icon: '✉️', change: '+12%' },
    { name: 'WhatsApp Messages', value: stats.whatsappMessages, icon: '💬', change: '+8%' },
    { name: 'Tasks Completed', value: stats.tasksCompleted, icon: '✅', change: '+15%' },
    { name: 'Pending Approvals', value: stats.pendingApprovals, icon: '📋', change: '-3%' },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      {statItems.map((item, index) => (
        <div 
          key={index} 
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200"
        >
          <div className="flex items-center">
            <div className="text-2xl">{item.icon}</div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{item.name}</p>
              <div className="flex items-baseline">
                <p className="text-2xl font-semibold text-gray-900">{item.value}</p>
                <p className="ml-2 text-sm font-medium text-green-500">{item.change}</p>
              </div>
            </div>
          </div>
        </div>
      ))}
      
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl shadow-sm border border-blue-100 p-6">
        <div className="flex items-center">
          <div className="text-2xl">⏱️</div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-600">System Uptime</p>
            <div className="flex items-baseline">
              <p className="text-2xl font-semibold text-blue-700">{stats.uptime}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatsCards;