import React from 'react';

interface Approval {
  id: number;
  type: string;
  amount?: string;
  recipient: string;
  subject?: string;
  status: string;
}

interface ApprovalQueueProps {
  approvals: Approval[];
}

const ApprovalQueue = ({ approvals }: ApprovalQueueProps) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="px-6 py-5 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Approval Queue</h2>
        <p className="mt-1 text-sm text-gray-500">Actions requiring your approval</p>
      </div>
      <div className="divide-y divide-gray-200">
        {approvals.map((approval) => (
          <div key={approval.id} className="px-6 py-4 hover:bg-gray-50 transition-colors duration-150">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-lg">📋</span>
              </div>
              <div className="ml-4 flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-gray-900">{approval.type} Request</p>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    approval.status === 'pending' 
                      ? 'bg-yellow-100 text-yellow-800' 
                      : approval.status === 'approved' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                  }`}>
                    {approval.status.charAt(0).toUpperCase() + approval.status.slice(1)}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mt-1">
                  {approval.amount ? `${approval.amount} to ${approval.recipient}` : `To: ${approval.recipient}`}
                  {approval.subject && ` - ${approval.subject}`}
                </p>
              </div>
            </div>
            <div className="mt-4 flex space-x-3">
              <button className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none">
                Approve
              </button>
              <button className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none">
                Reject
              </button>
              <button className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none">
                Details
              </button>
            </div>
          </div>
        ))}
      </div>
      <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
        <button className="text-sm font-medium text-blue-600 hover:text-blue-800">
          View all approvals →
        </button>
      </div>
    </div>
  );
};

export default ApprovalQueue;