# LinkedIn Watcher Setup and Usage Guide

## Overview
The LinkedIn Watcher is a component of the Personal AI Employee that monitors LinkedIn for important messages, posts, and networking opportunities, creating action files in the `Needs_Action` folder for processing.

## Prerequisites
- Python 3.8+
- LinkedIn API access (requires approval from LinkedIn)

## Setup

### 1. Obtain Access Token
To use the LinkedIn API, you need to obtain an access token. Follow these steps:

1. First, verify the redirect URI registered with your LinkedIn application:
   - Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
   - Navigate to your application
   - Check the "Authorized Redirect URLs" section
   - Make sure the URL matches exactly what you'll use below

2. Visit the OAuth 2.0 authorization URL (replace with your app's values):
   ```
   https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=7763qv2uyw7eao&redirect_uri=https://localhost&state=RANDOM_STATE_STRING&scope=r_liteprofile%20w_member_social
   ```
   
   OR if you prefer to use your other registered redirect URI:
   ```
   https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=7763qv2uyw7eao&redirect_uri=https://localhost:3000/callback&state=RANDOM_STATE_STRING&scope=r_liteprofile%20w_member_social
   ```

3. Log in to your LinkedIn account and authorize your application
4. You'll be redirected to your redirect URI with an authorization code in the URL
5. Copy the 'code' parameter from the URL (the value after 'code=' and before '&')
6. Exchange the authorization code for an access token using the token endpoint

### 2. Install Dependencies
Make sure you have the required Python packages installed:
```bash
pip install -r requirements.txt
```

### 3. Prepare Your Vault Directory
Ensure your AI Employee Vault directory is set up with the proper structure:
```
AI_Employee_Vault/
├── Needs_Action/
├── Logs/
└── ...
```

## Configuration

### Environment Variables
Your LinkedIn credentials are already configured in the `.env` file:
```
LINKEDIN_CLIENT_ID=7763qv2uyw7eao
LINKEDIN_CLIENT_SECRET=WPL_AP1.YOUR_LINKEDIN_SECRET_HERE
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token_here
LINKEDIN_REFRESH_TOKEN=your_linkedin_refresh_token_here
LINKEDIN_REDIRECT_URI=http://localhost
```

Replace `your_linkedin_access_token_here` with your actual access token.

### Manual Token Refresh (if needed)
If your access token expires, you can refresh it using the refresh token:
```python
from src.watchers.linkedin_watcher import LinkedInWatcher

watcher = LinkedInWatcher('/path/to/vault')
new_token = watcher._refresh_access_token()
```

## Usage

### Run the LinkedIn Watcher Continuously
The LinkedIn watcher runs automatically as part of the main orchestrator:
```bash
python src/orchestrator/orchestrator.py
```

### Test the Connection
You can test the LinkedIn connection separately:
```bash
python -c "
from src.watchers.linkedin_watcher import LinkedInWatcher
from pathlib import Path

vault_path = Path.home() / 'Documents' / 'AI_Employee_Vault'
watcher = LinkedInWatcher(str(vault_path))
updates = watcher.check_for_updates()
print(f'Found {len(updates)} updates')
"
```

## Configuration
The LinkedIn watcher monitors for posts and messages containing these keywords by default:
- urgent
- asap
- important
- meeting
- opportunity
- collaboration
- proposal
- contract
- offer
- interview
- position
- job
- hiring
- business
- partnership
- investment
- funding
- pitch
- networking

## Important Notes
1. **LinkedIn API Terms of Service**: Be aware of LinkedIn's API terms of service and usage limits. Misuse may result in your application being restricted.

2. **Rate Limits**: LinkedIn API has rate limits. The watcher is configured to check every 5 minutes to stay within reasonable limits.

3. **Permissions**: Your LinkedIn application must be approved by LinkedIn for the specific permissions you request. Some permissions require LinkedIn's review process.

4. **Access Tokens**: Access tokens have expiration times. Make sure to implement proper token refresh mechanisms.

## Troubleshooting
- If the watcher reports authentication errors, verify your access token is valid
- If you receive permission errors, check that your LinkedIn application has the required scopes
- Check the log file at `[VAULT_PATH]/Logs/watcher.log` for detailed error information
- For API-related issues, consult the [LinkedIn API documentation](https://docs.microsoft.com/en-us/linkedin/)