import React from 'react';

interface Task {
  id: number;
  title: string;
  status: string;
  type: string;
}

interface TaskManagerProps {
  tasks: Task[];
}

const TaskManager = ({ tasks }: TaskManagerProps) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'in-progress': return 'bg-blue-100 text-blue-800';
      case 'completed': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'email': return '📧';
      case 'social': return '📱';
      case 'finance': return '💰';
      default: return '📝';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="px-6 py-5 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Task Manager</h2>
        <p className="mt-1 text-sm text-gray-500">Current tasks being processed by your AI employee</p>
      </div>
      <div className="divide-y divide-gray-200">
        {tasks.map((task) => (
          <div key={task.id} className="px-6 py-4 hover:bg-gray-50 transition-colors duration-150">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-lg">{getTypeIcon(task.type)}</span>
              </div>
              <div className="ml-4 flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">{task.title}</p>
                <div className="mt-1 flex items-center">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(task.status)}`}>
                    {task.status.replace('-', ' ')}
                  </span>
                </div>
              </div>
              <div className="flex space-x-2">
                <button className="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded-full shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none">
                  View
                </button>
                <button className="inline-flex items-center px-3 py-1 border border-gray-300 text-xs font-medium rounded-full shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none">
                  Details
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
        <button className="text-sm font-medium text-blue-600 hover:text-blue-800">
          View all tasks →
        </button>
      </div>
    </div>
  );
};

export default TaskManager;