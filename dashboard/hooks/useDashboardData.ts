import { useState, useEffect } from 'react';

interface DashboardData {
  stats: {
    emailsProcessed: number;
    whatsappMessages: number;
    tasksCompleted: number;
    pendingApprovals: number;
    uptime: string;
    systemStatus: string;
  };
  recentActivity: Array<{
    id: number;
    type: string;
    content: string;
    time: string;
    priority: string;
  }>;
  pendingTasks: Array<{
    id: number;
    title: string;
    status: string;
    type: string;
  }>;
  communications: {
    emails: Array<{
      id: number;
      from: string;
      subject: string;
      time: string;
      read: boolean;
    }>;
    whatsapp: Array<{
      id: number;
      from: string;
      message: string;
      time: string;
      read: boolean;
    }>;
  };
  approvals: Array<{
    id: number;
    type: string;
    amount?: string;
    recipient: string;
    subject?: string;
    status: string;
  }>;
}

export const useDashboardData = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/dashboard');
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result: DashboardData = await response.json();
        setData(result);
        setError(null);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError(err instanceof Error ? err.message : 'Failed to fetch dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Set up polling to update data periodically
    const interval = setInterval(fetchData, 15000); // Update every 15 seconds

    return () => {
      clearInterval(interval);
    };
  }, []);

  return { data, loading, error };
};