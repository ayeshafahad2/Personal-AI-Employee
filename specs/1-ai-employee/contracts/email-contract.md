# Email MCP Server Contract

## Overview
This contract defines the interface for the Email MCP server that enables Claude Code to send, draft, and search emails via Gmail API.

## Capabilities
The Email MCP server provides the following capabilities:
- Send emails with attachments
- Draft emails for later sending
- Search and read emails
- Manage email labels and categories

## Endpoints

### Send Email
**Endpoint**: `call send-email`
**Parameters**:
- `to` (string, required): Recipient email address
- `subject` (string, required): Email subject
- `body` (string, required): Email body content
- `cc` (string, optional): CC recipient email addresses
- `bcc` (string, optional): BCC recipient email addresses
- `attachments` (array of strings, optional): File paths to attach

**Response**:
- `success` (boolean): Whether the operation was successful
- `message_id` (string): ID of the sent email
- `error` (string, optional): Error message if operation failed

### Draft Email
**Endpoint**: `call draft-email`
**Parameters**:
- `to` (string, required): Recipient email address
- `subject` (string, required): Email subject
- `body` (string, required): Email body content
- `cc` (string, optional): CC recipient email addresses
- `bcc` (string, optional): BCC recipient email addresses

**Response**:
- `success` (boolean): Whether the draft was created successfully
- `draft_id` (string): ID of the created draft
- `error` (string, optional): Error message if operation failed

### Search Emails
**Endpoint**: `call search-emails`
**Parameters**:
- `query` (string, required): Search query string (e.g., "from:user@example.com is:unread")
- `max_results` (integer, optional): Maximum number of results to return (default: 10)

**Response**:
- `success` (boolean): Whether the search was successful
- `emails` (array of objects): Array of matching emails
  - `id` (string): Email ID
  - `subject` (string): Email subject
  - `from` (string): Sender
  - `date` (string): Date sent
  - `snippet` (string): Preview of email content
- `error` (string, optional): Error message if operation failed

### Read Email
**Endpoint**: `call read-email`
**Parameters**:
- `email_id` (string, required): ID of the email to read

**Response**:
- `success` (boolean): Whether the read was successful
- `email` (object): Email details
  - `id` (string): Email ID
  - `subject` (string): Email subject
  - `from` (string): Sender
  - `to` (string): Recipients
  - `date` (string): Date sent
  - `body` (string): Full email content
- `error` (string, optional): Error message if operation failed

## Error Handling
The server returns appropriate HTTP status codes and error messages for various failure conditions:
- 400 Bad Request: Invalid parameters
- 401 Unauthorized: Invalid or expired credentials
- 403 Forbidden: Insufficient permissions
- 429 Too Many Requests: Rate limit exceeded
- 500 Internal Server Error: Server-side error

## Security Considerations
- All API calls must be authenticated using OAuth2
- Credentials must be stored securely and not in plain text
- Rate limiting is enforced by the Gmail API
- All email content is treated as sensitive and logged appropriately