# Twilio Free Trial Setup Guide

This guide will help you set up a **free Twilio trial account** to send WhatsApp notifications when LinkedIn posts are published.

## 🎁 Free Trial Benefits

- **$15 USD credit** (no credit card required for signup)
- Enough for ~100+ WhatsApp messages during testing
- Full access to Twilio WhatsApp API

## 📋 Step-by-Step Setup

### Step 1: Create Twilio Account

1. Go to [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Fill in the registration form:
   - Email address
   - Phone number (for verification)
   - Company name (optional)
   - Use case: Select "Testing/Learning"
3. Verify your email and phone number
4. Complete the CAPTCHA

### Step 2: Activate WhatsApp Sandbox

1. After login, go to **Console Dashboard**
2. In the left sidebar, click **Messaging** → **Try it out** → **Send a WhatsApp message**
3. Or go directly to: [https://console.twilio.com/us1/develop/sandbox/whatsapp](https://console.twilio.com/us1/develop/sandbox/whatsapp)
4. You'll see the **WhatsApp Sandbox** settings:
   - **Sandbox Number**: e.g., `+1 415 523 8886`
   - **Sandbox Code**: e.g., `journal-xxxx`

### Step 3: Connect Your WhatsApp

1. On your phone, open WhatsApp
2. Send a message to the sandbox number:
   - Message format: `join <your-sandbox-code>`
   - Example: `join journal-abc123`
3. You'll receive a confirmation message

### Step 4: Get Your Credentials

1. Go to **Console Dashboard**: [https://console.twilio.com/](https://console.twilio.com/)
2. Find your credentials on the main page:
   - **Account SID**: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **Auth Token**: Click "Show" to reveal

### Step 5: Configure Your .env File

Open `.env` file and update:

```env
# Twilio WhatsApp Credentials
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
WHATSAPP_RECIPIENT_NUMBER=whatsapp:+923298374240
```

**Important Notes:**
- `TWILIO_WHATSAPP_NUMBER`: Use the sandbox number with `whatsapp:` prefix
- `WHATSAPP_RECIPIENT_NUMBER`: Your number (+923298374240) with `whatsapp:` prefix
- Both numbers must be registered with the sandbox

### Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 7: Test the Integration

```bash
# Test all connections
python auto_post_manager.py --test

# Send a test WhatsApp message only
python whatsapp_notifier.py
```

## 🚀 Using the Automation

### Publish a Demo Post

```bash
python auto_post_manager.py
```

This will:
1. ✅ Publish a post to LinkedIn
2. ✅ Send you a WhatsApp notification with the post URL

### Custom Post

```bash
# Post custom text
python auto_post_manager.py --post "Your custom post content here"

# Post from file
python auto_post_manager.py --file my_post.txt
```

### Test Mode (No Posting)

```bash
python auto_post_manager.py --test
```

## ⚠️ Trial Limitations

| Feature | Free Trial | Production |
|---------|-----------|------------|
| Credit | $15 USD | Pay-as-you-go |
| WhatsApp Messages | ~100+ | $0.005/message |
| Sandbox Number | Yes | Your own number |
| Recipients | Only verified numbers | Any WhatsApp user |

### To Upgrade to Production:

1. Verify your business in Twilio Console
2. Register your own WhatsApp number
3. Submit WhatsApp template messages for approval
4. Upgrade account (add payment method)

## 🔧 Troubleshooting

### Error: "Invalid credentials"
- Double-check Account SID and Auth Token in `.env`
- Ensure no extra spaces in values

### Error: "To number not whitelisted"
- In free trial, only verified numbers can receive messages
- Add your number in Twilio Console → Verified Senders

### Error: "Sandbox not joined"
- Send `join <code>` to the sandbox number from your WhatsApp
- Wait for confirmation message

### LinkedIn Post Fails
- Check `LINKEDIN_ACCESS_TOKEN` in `.env`
- Token may have expired - regenerate from LinkedIn Developer Portal

## 📞 Support

- Twilio Docs: [https://www.twilio.com/docs/whatsapp](https://www.twilio.com/docs/whatsapp)
- Twilio Support: [https://support.twilio.com/](https://support.twilio.com/)
- LinkedIn API: [https://learn.microsoft.com/en-us/linkedin/](https://learn.microsoft.com/en-us/linkedin/)

## 🎯 Next Steps

1. ✅ Complete Twilio setup
2. ✅ Test with `python auto_post_manager.py --test`
3. ✅ Run demo post: `python auto_post_manager.py`
4. ✅ Check your WhatsApp for notification!

---

**Your WhatsApp number (+923298374240) is already configured as the recipient.** Just complete the Twilio setup and you're ready to go!
