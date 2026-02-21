import { NextResponse } from 'next/server';

// Mock data for the dashboard API
const mockDashboardData = {
  stats: {
    emailsProcessed: 24,
    whatsappMessages: 18,
    tasksCompleted: 12,
    pendingApprovals: 3,
    uptime: '99.8%',
    systemStatus: 'Operational'
  },
  recentActivity: [
    { id: 1, type: 'email', content: 'Important email from client received', time: '2 mins ago', priority: 'high' },
    { id: 2, type: 'whatsapp', content: 'Urgent message from supplier', time: '5 mins ago', priority: 'high' },
    { id: 3, type: 'task', content: 'Weekly report generated', time: '15 mins ago', priority: 'medium' },
    { id: 4, type: 'approval', content: 'Payment request awaiting approval', time: '22 mins ago', priority: 'high' },
    { id: 5, type: 'email', content: 'Meeting reminder processed', time: '30 mins ago', priority: 'low' },
  ],
  pendingTasks: [
    { id: 1, title: 'Respond to client inquiry', status: 'pending', type: 'email' },
    { id: 2, title: 'Schedule social media post', status: 'in-progress', type: 'social' },
    { id: 3, title: 'Process invoice approval', status: 'pending', type: 'finance' },
  ],
  communications: {
    emails: [
      { id: 1, from: 'client@example.com', subject: 'Project Update', time: '10:30 AM', read: false },
      { id: 2, from: 'supplier@business.com', subject: 'Order Confirmation', time: '9:15 AM', read: true },
    ],
    whatsapp: [
      { id: 1, from: '+1234567890', message: 'Can we schedule a call?', time: '11:45 AM', read: false },
      { id: 2, from: '+0987654321', message: 'Thanks for the info!', time: '8:30 AM', read: true },
    ]
  },
  approvals: [
    { id: 1, type: 'Payment', amount: '$1,250', recipient: 'Vendor Inc.', status: 'pending' },
    { id: 2, type: 'Email', recipient: 'client@example.com', subject: 'Contract Renewal', status: 'pending' },
  ]
};

export async function GET(request: Request) {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  return NextResponse.json(mockDashboardData);
}

// POST route to handle approval actions
export async function POST(request: Request) {
  const body = await request.json();
  
  // In a real implementation, this would process the approval action
  // For now, we'll just return a success response
  return NextResponse.json({
    success: true,
    message: `Action ${body.action} for item ${body.itemId} processed successfully`,
    data: body
  });
}