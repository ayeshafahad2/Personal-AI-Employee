// Dashboard Configuration
export const DASHBOARD_CONFIG = {
  // API Configuration
  API_BASE_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001',
  
  // Refresh intervals (in milliseconds)
  STATS_REFRESH_INTERVAL: 30000, // 30 seconds
  ACTIVITY_FEED_REFRESH_INTERVAL: 10000, // 10 seconds
  COMMUNICATIONS_REFRESH_INTERVAL: 15000, // 15 seconds
  APPROVALS_REFRESH_INTERVAL: 20000, // 20 seconds
  
  // Dashboard settings
  MAX_ACTIVITY_ITEMS: 10,
  MAX_COMMUNICATION_ITEMS: 5,
  MAX_APPROVAL_ITEMS: 5,
  
  // Priority levels
  PRIORITY_LEVELS: {
    LOW: 'low',
    MEDIUM: 'medium',
    HIGH: 'high'
  },
  
  // Status types
  STATUS_TYPES: {
    PENDING: 'pending',
    IN_PROGRESS: 'in-progress',
    COMPLETED: 'completed',
    APPROVED: 'approved',
    REJECTED: 'rejected'
  },
  
  // Communication types
  COMMUNICATION_TYPES: {
    EMAIL: 'email',
    WHATSAPP: 'whatsapp',
    TASK: 'task',
    APPROVAL: 'approval'
  },
  
  // Theme settings
  THEME: {
    PRIMARY_COLOR: '#4F46E5', // indigo-600
    SECONDARY_COLOR: '#7C3AED', // violet-600
    BACKGROUND_GRADIENT: 'from-gray-50 to-gray-100',
    CARD_SHADOW: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  }
};

// Export individual settings for easier access
export const {
  API_BASE_URL,
  STATS_REFRESH_INTERVAL,
  ACTIVITY_FEED_REFRESH_INTERVAL,
  COMMUNICATIONS_REFRESH_INTERVAL,
  APPROVALS_REFRESH_INTERVAL,
  MAX_ACTIVITY_ITEMS,
  MAX_COMMUNICATION_ITEMS,
  MAX_APPROVAL_ITEMS,
  PRIORITY_LEVELS,
  STATUS_TYPES,
  COMMUNICATION_TYPES,
  THEME
} = DASHBOARD_CONFIG;