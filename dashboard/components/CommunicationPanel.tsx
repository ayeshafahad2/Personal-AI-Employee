import React from 'react';

interface CommunicationItem {
  id: number;
  from: string;
  subject?: string;
  message?: string;
  time: string;
  read: boolean;
}

interface Communications {
  emails: CommunicationItem[];
  whatsapp: CommunicationItem[];
}

interface CommunicationPanelProps {
  communications: Communications;
}

const CommunicationPanel = ({ communications }: CommunicationPanelProps) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="px-6 py-5 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Communications</h2>
        <p className="mt-1 text-sm text-gray-500">Recent messages from Gmail and WhatsApp</p>
      </div>
      
      <div className="p-6">
        <h3 className="text-md font-medium text-gray-900 mb-3 flex items-center">
          <span className="mr-2">📧</span> Recent Emails
        </h3>
        <div className="space-y-3">
          {communications.emails.map((email) => (
            <div 
              key={email.id} 
              className={`p-3 rounded-lg border ${email.read ? 'border-gray-200 bg-white' : 'border-blue-200 bg-blue-50'}`}
            >
              <div className="flex justify-between">
                <p className="text-sm font-medium text-gray-900 truncate">{email.from}</p>
                <span className="text-xs text-gray-500">{email.time}</span>
              </div>
              <p className="text-sm text-gray-600 truncate">{email.subject}</p>
              {!email.read && (
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mt-1">
                  Unread
                </span>
              )}
            </div>
          ))}
        </div>
        
        <h3 className="text-md font-medium text-gray-900 mt-6 mb-3 flex items-center">
          <span className="mr-2">💬</span> WhatsApp Messages
        </h3>
        <div className="space-y-3">
          {communications.whatsapp.map((message) => (
            <div 
              key={message.id} 
              className={`p-3 rounded-lg border ${message.read ? 'border-gray-200 bg-white' : 'border-green-200 bg-green-50'}`}
            >
              <div className="flex justify-between">
                <p className="text-sm font-medium text-gray-900 truncate">{message.from}</p>
                <span className="text-xs text-gray-500">{message.time}</span>
              </div>
              <p className="text-sm text-gray-600 truncate">{message.message}</p>
              {!message.read && (
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 mt-1">
                  Unread
                </span>
              )}
            </div>
          ))}
        </div>
      </div>
      
      <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
        <button className="text-sm font-medium text-blue-600 hover:text-blue-800">
          View all communications →
        </button>
      </div>
    </div>
  );
};

export default CommunicationPanel;