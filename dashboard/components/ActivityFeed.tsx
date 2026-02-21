import React from 'react';

interface Activity {
  id: number;
  type: string;
  content: string;
  time: string;
  priority: string;
}

interface ActivityFeedProps {
  activities: Activity[];
}

const ActivityFeed = ({ activities }: ActivityFeedProps) => {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'email': return '📧';
      case 'whatsapp': return '💬';
      case 'task': return '✅';
      case 'approval': return '📋';
      default: return 'ℹ️';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="px-6 py-5 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Recent Activity</h2>
        <p className="mt-1 text-sm text-gray-500">Latest actions taken by your AI employee</p>
      </div>
      <div className="divide-y divide-gray-200">
        {activities.map((activity) => (
          <div key={activity.id} className="px-6 py-4 hover:bg-gray-50 transition-colors duration-150">
            <div className="flex items-start">
              <div className="flex-shrink-0 pt-0.5">
                <span className="text-xl">{getTypeIcon(activity.type)}</span>
              </div>
              <div className="ml-4 flex-1">
                <p className="text-sm font-medium text-gray-900">{activity.content}</p>
                <div className="mt-2 flex items-center justify-between">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(activity.priority)}`}>
                      {activity.priority}
                    </span>
                  </span>
                  <span className="text-xs text-gray-500">{activity.time}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
        <button className="text-sm font-medium text-blue-600 hover:text-blue-800">
          View all activity →
        </button>
      </div>
    </div>
  );
};

export default ActivityFeed;