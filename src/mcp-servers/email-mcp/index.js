/**
 * Email MCP Server for Personal AI Employee
 * Handles sending, drafting, and searching emails via Gmail API
 */

const { createClient, createServer } = require('@modelcontextprotocol/sdk');
const { google } = require('googleapis');

// Gmail API setup
const SCOPES = ['https://www.googleapis.com/auth/gmail'];
const TOKEN_PATH = 'token.json';

class EmailMCPServer {
  constructor() {
    this.server = createServer({
      name: 'email-mcp',
      version: '1.0.0'
    });
    
    this.setupEndpoints();
  }
  
  setupEndpoints() {
    // Send email endpoint
    this.server.addTool({
      name: 'send-email',
      description: 'Send an email via Gmail',
      inputSchema: {
        type: 'object',
        properties: {
          to: { type: 'string', description: 'Recipient email address' },
          subject: { type: 'string', description: 'Email subject' },
          body: { type: 'string', description: 'Email body content' },
          cc: { type: 'string', description: 'CC recipient email addresses (optional)' },
          bcc: { type: 'string', description: 'BCC recipient email addresses (optional)' },
          attachments: { 
            type: 'array', 
            items: { type: 'string' },
            description: 'File paths to attach (optional)'
          }
        },
        required: ['to', 'subject', 'body']
      }
    }, async ({ to, subject, body, cc, bcc, attachments }) => {
      try {
        const gmail = await this.getGmailService();
        
        // Create email message
        const email = this.createEmailMessage(to, subject, body, cc, bcc);
        
        // Send the email
        const res = await gmail.users.messages.send({
          userId: 'me',
          requestBody: {
            raw: Buffer.from(email).toString('base64')
          }
        });
        
        return {
          success: true,
          message_id: res.data.id,
          message: 'Email sent successfully'
        };
      } catch (error) {
        console.error('Error sending email:', error);
        return {
          success: false,
          error: error.message
        };
      }
    });
    
    // Draft email endpoint
    this.server.addTool({
      name: 'draft-email',
      description: 'Create a draft email in Gmail',
      inputSchema: {
        type: 'object',
        properties: {
          to: { type: 'string', description: 'Recipient email address' },
          subject: { type: 'string', description: 'Email subject' },
          body: { type: 'string', description: 'Email body content' },
          cc: { type: 'string', description: 'CC recipient email addresses (optional)' },
          bcc: { type: 'string', description: 'BCC recipient email addresses (optional)' }
        },
        required: ['to', 'subject', 'body']
      }
    }, async ({ to, subject, body, cc, bcc }) => {
      try {
        const gmail = await this.getGmailService();
        
        // Create email message
        const email = this.createEmailMessage(to, subject, body, cc, bcc);
        
        // Create the draft
        const res = await gmail.users.drafts.create({
          userId: 'me',
          requestBody: {
            message: {
              raw: Buffer.from(email).toString('base64')
            }
          }
        });
        
        return {
          success: true,
          draft_id: res.data.id,
          message: 'Draft created successfully'
        };
      } catch (error) {
        console.error('Error creating draft:', error);
        return {
          success: false,
          error: error.message
        };
      }
    });
    
    // Search emails endpoint
    this.server.addTool({
      name: 'search-emails',
      description: 'Search emails in Gmail',
      inputSchema: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'Search query string (e.g., "from:user@example.com is:unread")' },
          max_results: { type: 'number', description: 'Maximum number of results to return (default: 10)' }
        },
        required: ['query']
      }
    }, async ({ query, max_results = 10 }) => {
      try {
        const gmail = await this.getGmailService();
        
        // Search for emails
        const res = await gmail.users.messages.list({
          userId: 'me',
          q: query,
          maxResults: Math.min(max_results, 50) // Limit to 50 max
        });
        
        const messages = res.data.messages || [];
        const emailDetails = [];
        
        // Get details for each email (limit to first 10 to avoid too many API calls)
        for (const msg of messages.slice(0, 10)) {
          try {
            const emailRes = await gmail.users.messages.get({
              userId: 'me',
              id: msg.id
            });
            
            const headers = emailRes.data.payload.headers;
            const from = headers.find(h => h.name === 'From')?.value || 'Unknown';
            const subject = headers.find(h => h.name === 'Subject')?.value || 'No Subject';
            const date = headers.find(h => h.name === 'Date')?.value || 'Unknown';
            
            emailDetails.push({
              id: msg.id,
              subject: subject,
              from: from,
              date: date,
              snippet: emailRes.data.snippet
            });
          } catch (err) {
            console.error(`Error getting details for email ${msg.id}:`, err);
          }
        }
        
        return {
          success: true,
          emails: emailDetails,
          count: emailDetails.length
        };
      } catch (error) {
        console.error('Error searching emails:', error);
        return {
          success: false,
          error: error.message
        };
      }
    });
  }
  
  async getGmailService() {
    // Load client secrets from environment variables
    const clientId = process.env.GMAIL_CLIENT_ID;
    const clientSecret = process.env.GMAIL_CLIENT_SECRET;
    const redirectUri = process.env.GMAIL_REDIRECT_URI || 'http://localhost';
    
    if (!clientId || !clientSecret) {
      throw new Error('Missing Gmail API credentials in environment variables');
    }
    
    // Create OAuth2 client
    const oAuth2Client = new google.auth.OAuth2(
      clientId,
      clientSecret,
      redirectUri
    );
    
    // Check if we have previously stored a token
    try {
      const fs = require('fs');
      const token = fs.readFileSync(TOKEN_PATH);
      oAuth2Client.setCredentials(JSON.parse(token));
    } catch (error) {
      throw new Error('Could not load access token. Please authenticate first.');
    }
    
    return google.gmail({ version: 'v1', auth: oAuth2Client });
  }
  
  createEmailMessage(to, subject, body, cc, bcc) {
    let message = '';
    message += `To: ${to}\r\n`;
    message += `Subject: ${subject}\r\n`;
    if (cc) message += `Cc: ${cc}\r\n`;
    message += 'Content-Type: text/html\r\n';
    message += '\r\n';  // End of headers
    message += body;
    
    return message;
  }
  
  start() {
    console.log('Starting Email MCP Server...');
    this.server.listen({ port: 8080 });
    console.log('Email MCP Server listening on port 8080');
  }
}

// Start the server if this file is run directly
if (require.main === module) {
  const server = new EmailMCPServer();
  server.start();
}

module.exports = EmailMCPServer;