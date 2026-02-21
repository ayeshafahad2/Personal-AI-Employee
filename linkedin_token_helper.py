#!/usr/bin/env python3
"""
LinkedIn Access Token Helper
Simulates the token exchange process to help you understand how to get your access token
"""
import json

def simulate_token_exchange():
    """
    Simulates the token exchange process
    """
    print("=" * 80)
    print("LINKEDIN ACCESS TOKEN HELPER")
    print("=" * 80)
    print()
    print("This script simulates the token exchange process to help you understand")
    print("how to exchange your authorization code for an access token.")
    print()
    print("WHEN YOU VISIT THE AUTHORIZATION URL AND AUTHORIZE THE APP,")
    print("YOU'LL BE REDIRECTED TO SOMETHING LIKE:")
    print()
    print("https://localhost?code=AQTR...[LONG_CODE_STRING]...&state=linkedin_auth_state")
    print()
    print("THE 'CODE' PARAMETER IS WHAT YOU NEED FOR THE NEXT STEP.")
    print()
    print("TO EXCHANGE THIS CODE FOR AN ACCESS TOKEN, MAKE A POST REQUEST TO:")
    print("https://www.linkedin.com/oauth/v2/accessToken")
    print()
    print("WITH THESE PARAMETERS:")
    print("  - grant_type: authorization_code")
    print("  - code: [THE_CODE_FROM_THE_REDIRECT_URL]")
    print("  - redirect_uri: https://localhost")
    print("  - client_id: 7763qv2uyw7eao")
    print("  - client_secret: WPL_AP1.YOUR_LINKEDIN_SECRET_HERE")
    print()
    print("USING CURL, THE REQUEST LOOKS LIKE:")
    print()
    print("curl -X POST \\")
    print("  'https://www.linkedin.com/oauth/v2/accessToken' \\")
    print("  -H 'Content-Type: application/x-www-form-urlencoded' \\")
    print("  -d 'grant_type=authorization_code' \\")
    print("  -d 'code=[YOUR_AUTHORIZATION_CODE]' \\")
    print("  -d 'redirect_uri=https://localhost' \\")
    print("  -d 'client_id=7763qv2uyw7eao' \\")
    print("  -d 'client_secret=WPL_AP1.YOUR_LINKEDIN_SECRET_HERE'")
    print()
    print("A SUCCESSFUL RESPONSE WILL LOOK LIKE:")
    print()
    sample_response = {
        "access_token": "AQXd...[YOUR_ACTUAL_ACCESS_TOKEN]...",
        "expires_in": 5183999,
        "refresh_token": "AQTS...[REFRESH_TOKEN_IF_GRANTED]...",
        "refresh_token_expires_in": 5183999,
        "scope": "r_liteprofile w_member_social"
    }
    print(json.dumps(sample_response, indent=2))
    print()
    print("THE 'access_token' VALUE IS WHAT YOU NEED TO PUT IN YOUR .ENV FILE!")
    print()
    print("TIP: You can also use LinkedIn's OAuth 2.0 tools at:")
    print("     https://www.linkedin.com/developers/tools/oauth")
    print("     to exchange your code for an access token without using curl.")
    print()
    print("=" * 80)

def main():
    simulate_token_exchange()

if __name__ == "__main__":
    main()