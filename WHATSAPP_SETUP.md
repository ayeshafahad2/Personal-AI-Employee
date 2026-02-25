# 📱 WhatsApp Setup Guide

## Your Configuration

```env
WHATSAPP_RECIPIENT_NUMBER=whatsapp:+923298374240
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
```

---

## 🚀 Two Ways to Send WhatsApp

### Option 1: Browser Automation (FREE - Works Now!) ✅

**No Twilio account needed!** Uses WhatsApp Web directly.

**Send message:**
```bash
python whatsapp_send_browser.py
```

**How it works:**
1. Opens Chrome with WhatsApp Web
2. You scan QR code (first time only)
3. Enter recipient number and message
4. WhatsApp opens with pre-filled message
5. Click send
6. Done!

**Pros:**
- ✅ Free
- ✅ No API setup
- ✅ Works immediately
- ✅ Uses your existing WhatsApp

**Cons:**
- Requires browser
- Manual send (click button)

---

### Option 2: Twilio API (Professional - Automated) ⏳

**Requires Twilio account and credentials.**

**Step 1: Get Twilio Credentials**

1. **Go to:** https://console.twilio.com/
2. **Sign up** (free trial available)
3. **Verify your phone number**
4. **Get credentials from dashboard:**
   - Account SID (starts with AC...)
   - Auth Token

**Step 2: Enable WhatsApp Sandbox**

1. In Twilio Console, go to **Messaging** → **Try it out** → **Send a WhatsApp message**
2. **Follow instructions:**
   - Send "join <code>" to +14155238886 on WhatsApp
   - You'll get a confirmation
3. **Copy your sandbox code**

**Step 3: Add to `.env`**

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
WHATSAPP_RECIPIENT_NUMBER=whatsapp:+923298374240
```

**Step 4: Send via API**

```bash
python whatsapp_notifier.py
```

**Pros:**
- ✅ Fully automated
- ✅ API-based
- ✅ No browser needed
- ✅ Production ready

**Cons:**
- Requires Twilio account
- Free trial then paid
- Setup time (10-15 minutes)

---

## 🎯 Recommended: Start with Browser (Free)

**For now, use browser automation:**

```bash
python whatsapp_send_browser.py
```

**It works immediately with no setup!**

Later, if you need automation:
- Sign up for Twilio
- Get credentials
- Add to `.env`
- Use API

---

## 📝 Your WhatsApp Number

**Recipient:** `+923298374240` (Pakistan)

**Formatted for WhatsApp:** `whatsapp:+923298374240`

---

## 🚀 Quick Test (Browser Method)

**Run now:**
```bash
python whatsapp_send_browser.py
```

**It will:**
1. Open Chrome
2. Load WhatsApp Web
3. Ask for number and message
4. Open chat with pre-filled message
5. You click send

**First time:** Scan QR code with your phone

**After that:** Session saved, works immediately

---

## 📖 Files Created

- `whatsapp_send_browser.py` - Browser-based sender
- `WHATSAPP_SETUP.md` - This guide

---

## 🔗 Twilio Resources

- **Sign Up:** https://console.twilio.com/
- **WhatsApp Docs:** https://www.twilio.com/docs/whatsapp
- **Pricing:** https://www.twilio.com/pricing/whatsapp

---

**Start with browser method - it's free and works now!** 🎉
