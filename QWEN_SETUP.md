# Qwen Integration Guide

This guide explains how to configure and use **Qwen** (通义千问) as the AI reasoning engine for your Personal AI Employee.

## Overview

The system supports two AI backends:
1. **Qwen API** (DashScope) - Cloud-based API
2. **Claude Code CLI** - Local command-line tool

By default, the system is configured to use **Qwen**.

## Quick Start with Qwen

### Step 1: Get Qwen API Key

1. Go to [Alibaba Cloud DashScope](https://dashscope.console.aliyun.com/)
2. Sign in or create an account
3. Navigate to **API Keys** section
4. Create a new API key (DashScope API Key)
5. Copy the API key

### Step 2: Configure .env

Open `.env` and update:

```env
# Set AI command to 'qwen'
AI_COMMAND=qwen

# Your Qwen API key
DASHSCOPE_API_KEY=sk-your-actual-api-key-here

# Model selection (optional)
QWEN_MODEL=qwen-max
```

### Step 3: Test Qwen Integration

```bash
# Test the orchestrator
python orchestrator.py --process --vault AI_Employee_Vault
```

## Available Qwen Models

| Model | Description | Best For |
|-------|-------------|----------|
| `qwen-max` | Most powerful | Complex reasoning, planning |
| `qwen-plus` | Balanced | General tasks |
| `qwen-turbo` | Fast & cheap | Simple tasks |
| `qwen-long` | Long context | Document analysis |

Update model in `.env`:
```env
QWEN_MODEL=qwen-max
```

## Configuration Options

### .env Variables

```env
# AI Assistant Selection
AI_COMMAND=qwen                    # 'qwen' for API, 'claude' for CLI

# Qwen API Configuration
DASHSCOPE_API_KEY=sk-xxxxx         # Your DashScope API key
QWEN_MODEL=qwen-max                # Model to use
ALIBABA_CLOUD_API_KEY=             # Alternative credential
```

### Orchestrator Configuration

The orchestrator automatically detects the AI command:

```python
# In orchestrator.py
if self.claude_cmd.lower() == 'qwen':
    # Use Qwen API
    result = self._run_qwen_api(prompt)
else:
    # Use CLI command
    result = subprocess.run([self.claude_cmd, '--prompt', prompt], ...)
```

## API Endpoints

### DashScope (International)
```
https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
```

### DashScope (China)
```
https://dashscope.aliyun.com/api/v1/services/aigc/text-generation/generation
```

The system uses the international endpoint by default. To use the China endpoint, add to `.env`:

```env
DASHSCOPE_ENDPOINT=https://dashscope.aliyun.com/api/v1/services/aigc/text-generation/generation
```

## Pricing (as of 2026)

| Model | Input (per 1K tokens) | Output (per 1K tokens) |
|-------|----------------------|------------------------|
| qwen-max | ~$0.04 | ~$0.12 |
| qwen-plus | ~$0.008 | ~$0.02 |
| qwen-turbo | ~$0.002 | ~$0.006 |

**Note:** Prices vary by region. Check [DashScope pricing](https://www.aliyun.com/price/product) for current rates.

## Using Qwen with the AI Employee

### Process Needs_Action Folder

```bash
# Process with Qwen
python orchestrator.py --process --vault AI_Employee_Vault
```

### Run Autonomous Loop

```bash
# Ralph Wiggum loop with Qwen
python ralph_wiggum.py "Process all files in Needs_Action" \
  --vault AI_Employee_Vault \
  --max-iterations 5
```

### Generate CEO Briefing

```bash
python orchestrator.py --briefing --vault AI_Employee_Vault
```

## Troubleshooting

### Error: "DASHSCOPE_API_KEY not set"

**Solution:** Add to `.env`:
```env
DASHSCOPE_API_KEY=sk-your-key-here
```

### Error: "Invalid API key"

**Solution:**
1. Verify API key in DashScope console
2. Ensure no extra spaces in `.env`
3. Restart Python process

### Error: "Model not found"

**Solution:** Change model in `.env`:
```env
QWEN_MODEL=qwen-plus
```

### Slow Response Times

**Solution:** Use faster model:
```env
QWEN_MODEL=qwen-turbo
```

## Switching Between Qwen and Claude

### Use Qwen
```env
AI_COMMAND=qwen
DASHSCOPE_API_KEY=sk-xxxxx
```

### Use Claude Code CLI
```env
AI_COMMAND=claude
```

## Example: Email Processing with Qwen

1. **Gmail Watcher** detects new email → creates `Needs_Action/EMAIL_xxx.md`
2. **Orchestrator** picks up file → creates `Plans/PLAN_xxx.md`
3. **Qwen API** processes the action:
   - Reads email content
   - Follows plan steps
   - Creates approval request if needed
   - Executes actions via MCP servers
4. **HITL Processor** handles approved actions
5. Files moved to `Done/`

## MCP Servers with Qwen

MCP servers work the same way regardless of AI backend:

- **Email MCP**: `send_email`, `draft_email`, `search_emails`
- **Browser MCP**: `navigate`, `click`, `fill`, `screenshot`
- **LinkedIn MCP**: `publish_post`, `publish_from_file`

Qwen can call these tools just like Claude would.

## Performance Tips

1. **Use qwen-turbo** for simple tasks (file moves, basic classification)
2. **Use qwen-max** for complex reasoning (planning, approval decisions)
3. **Set max_tokens** appropriately to control costs
4. **Cache common responses** in Company_Handbook.md

## Security Notes

- **Never commit `.env`** - Contains API keys
- **Rotate API keys** monthly
- **Monitor usage** in DashScope console
- **Set spending limits** in Alibaba Cloud

## Additional Resources

- [DashScope Documentation](https://help.aliyun.com/zh/dashscope/)
- [Qwen Model Overview](https://help.aliyun.com/zh/dashscope/developer-reference/model-overview)
- [Alibaba Cloud Console](https://dashscope.console.aliyun.com/)

---

**Ready to use Qwen with your AI Employee!**

Run: `python orchestrator.py --process` to start processing with Qwen.
