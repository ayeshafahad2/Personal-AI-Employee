# Personal AI Employee Dashboard

A professional, real-time dashboard for monitoring your Personal AI Employee system. Built with Next.js, Tailwind CSS, and TypeScript for a stunning, responsive user experience.

## Features

- **Real-time Monitoring**: Live updates of your AI employee's activities
- **Activity Feed**: Timeline of recent actions taken by your AI employee
- **Task Management**: View and manage pending tasks
- **Communication Hub**: Monitor Gmail and WhatsApp interactions
- **Approval Queue**: Handle sensitive actions requiring your approval
- **Performance Metrics**: Track system performance and efficiency
- **Responsive Design**: Works beautifully on all device sizes

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom animations
- **Language**: TypeScript
- **Icons**: Emoji-based for simplicity (can be replaced with SVG icons)

## Installation

1. Navigate to the dashboard directory:
   ```bash
   cd dashboard
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
dashboard/
├── app/
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── DashboardHeader.tsx
│   ├── StatsCards.tsx
│   ├── ActivityFeed.tsx
│   ├── TaskManager.tsx
│   ├── CommunicationPanel.tsx
│   └── ApprovalQueue.tsx
├── hooks/
│   └── useDashboardData.ts
├── styles/
│   └── globals.css
├── public/
├── package.json
└── README.md
```

## Dashboard Sections

### Header
- System status indicator
- Welcome message
- Operational status

### Statistics Cards
- Emails processed
- WhatsApp messages handled
- Tasks completed
- Pending approvals
- System uptime

### Activity Feed
- Chronological list of recent activities
- Color-coded priority levels
- Activity types (email, WhatsApp, task, approval)

### Task Manager
- Current tasks being processed
- Task status indicators
- Action buttons for each task

### Communication Panel
- Recent Gmail messages
- WhatsApp message previews
- Read/unread status indicators

### Approval Queue
- Actions requiring human approval
- Approval/rejection buttons
- Detailed request information

## Customization

You can customize the dashboard by:

1. Modifying the styling in `styles/globals.css`
2. Updating the components in the `components/` directory
3. Adjusting the data simulation in `hooks/useDashboardData.ts`

## Integration with Backend

The dashboard is currently using simulated data. To connect to your actual AI Employee system:

1. Update the `useDashboardData` hook to fetch from your backend API
2. Create API routes in `app/api/` to serve real data
3. Implement WebSocket connections for real-time updates

## Deployment

To build the application for production:

```bash
npm run build
```

Then run the production server:

```bash
npm start
```

## Environment Variables

If connecting to a backend API, you can add environment variables to a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:3001
```

## Contributing

Feel free to submit issues and enhancement requests! Contributions are welcome to improve the dashboard functionality and design.

## License

This project is licensed under the MIT License.