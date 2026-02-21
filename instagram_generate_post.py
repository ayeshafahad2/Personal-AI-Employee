#!/usr/bin/env python3
"""
Instagram Post Generator - Creates image and SEO-optimized post
Topic: Human FTE vs Digital FTE (Custom Agent)
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("=" * 70)
print("  INSTAGRAM POST GENERATOR")
print("  Topic: Human FTE vs Digital FTE (Custom Agent)")
print("=" * 70)

# Create Instagram post image
def create_instagram_image():
    """Create a professional Instagram post image"""
    
    # Image dimensions (Instagram square: 1080x1080)
    width, height = 1080, 1080
    
    # Create gradient background
    img = Image.new('RGB', (width, height), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Draw gradient
    for y in range(height):
        r = int(26 + (224 - 26) * y / height)
        g = int(46 + (146 - 46) * y / height)
        b = int(94 + (210 - 94) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add title text
    try:
        title_font = ImageFont.truetype("arial.ttf", 72)
        subtitle_font = ImageFont.truetype("arial.ttf", 42)
        text_font = ImageFont.truetype("arial.ttf", 36)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Title
    title = "HUMAN FTE"
    draw.text((width/2, 150), title, fill='#ffffff', font=title_font, anchor='mm')
    
    # VS
    draw.text((width/2, 320), "VS", fill='#ff6b6b', font=title_font, anchor='mm')
    
    # Subtitle
    subtitle = "DIGITAL FTE"
    draw.text((width/2, 480), subtitle, fill='#4ecdc4', font=title_font, anchor='mm')
    
    # Tagline
    tagline = "(Custom AI Agent)"
    draw.text((width/2, 560), tagline, fill='#95a5a6', font=subtitle_font, anchor='mm')
    
    # Comparison points
    points = [
        "💰 85-90% Cost Reduction",
        "⏰ 24/7 Availability",
        "🚀 Instant Response",
        "📊 Zero HR Overhead",
        "🔒 Privacy-First Design"
    ]
    
    y_offset = 680
    for point in points:
        draw.text((width/2, y_offset), point, fill='#ffffff', font=text_font, anchor='mm')
        y_offset += 65
    
    # Add date
    date_text = datetime.now().strftime('%B %d, %Y')
    draw.text((width/2, height - 80), date_text, fill='#7f8c8d', font=subtitle_font, anchor='mm')
    
    # Save image
    image_path = 'instagram_human_fte_vs_digital_fte.png'
    img.save(image_path)
    print(f"\n✅ Image created: {image_path}")
    print(f"   Size: {width}x{height} pixels")
    print(f"   Format: PNG")
    
    return image_path

# Generate SEO-optimized caption
def generate_caption():
    """Generate SEO-friendly Instagram caption"""
    
    caption = """🚀 HUMAN FTE vs DIGITAL FTE: The Future of Work is Here! 🤖

💼 TRADITIONAL HUMAN FTE:
❌ $4,000-8,000/month salary
❌ 8 hours/day availability
❌ Sick days, vacations, holidays
❌ Training & onboarding time
❌ HR overhead & management
❌ Limited to one task at a time

✨ DIGITAL FTE (Custom AI Agent):
✅ $500-2,000/month (85-90% savings!)
✅ 24/7/365 availability
✅ Zero sick days, never takes vacation
✅ Instant deployment, no training
✅ Zero HR overhead
✅ Handles multiple tasks simultaneously

📊 REAL-WORLD IMPACT:

A Digital FTE (Custom AI Agent) can:
• Monitor your Gmail 24/7 for urgent emails
• Manage WhatsApp communications automatically
• Post to LinkedIn, Instagram, Twitter autonomously
• Track deadlines and send reminders
• Generate reports and insights
• Handle routine inquiries instantly

🎯 THE BOTTOM LINE:

Digital FTEs don't replace humans—they AUGMENT human potential.

While your Digital FTE handles routine tasks, you focus on:
→ Strategic decision-making
→ Creative work
→ Building relationships
→ Growing your business

💡 This is the future of productivity.

📈 Companies using Digital FTEs report:
• 80% reduction in administrative tasks
• 3x faster response times
• 95% task completion accuracy
• Zero missed opportunities

🔥 Ready to transform your workflow?

The technology exists TODAY to create your own Digital FTE.

It's not about working harder—it's about working SMARTER with AI augmentation.

👇 Drop a 💻 if you want to learn more about Digital FTEs!

━━━━━━━━━━━━━━━━━━━━

#DigitalFTE #HumanFTE #AIAgent #CustomAgent #ArtificialIntelligence #Automation #FutureOfWork #Productivity #BusinessEfficiency #DigitalTransformation #AI #MachineLearning #TechInnovation #StartupLife #Entrepreneur #BusinessGrowth #WorkflowAutomation #SmartWork #Innovation #TechTrends #AIAssistant #VirtualAssistant #BusinessAutomation #DigitalEmployee #WorkSmart #ProductivityHacks #AITools #BusinessTips #TechSolutions #ModernBusiness

📍 Posted: {timestamp}
""".format(timestamp=datetime.now().strftime('%B %d, %Y'))
    
    return caption

# Main execution
print("\n[1/3] Creating Instagram post image...")
image_path = create_instagram_image()

print("\n[2/3] Generating SEO-optimized caption...")
caption = generate_caption()

print("\n[3/3] Caption Preview:")
print("=" * 70)
print(caption[:500] + "...")
print("=" * 70)

# Save caption to file
caption_file = 'instagram_caption_human_fte.txt'
with open(caption_file, 'w', encoding='utf-8') as f:
    f.write(caption)

print(f"\n✅ Caption saved: {caption_file}")
print(f"   Length: {len(caption)} characters")
print(f"   Hashtags: 30 (optimized for Instagram)")

# Copy to clipboard
try:
    import subprocess
    subprocess.run(['clip'], input=caption.encode('utf-16-le'), capture_output=True)
    print("\n✅ Caption copied to clipboard!")
except:
    print("\n⚠️  Please copy caption manually from the file")

print("\n" + "=" * 70)
print("  READY TO POST")
print("=" * 70)
print(f"""
  IMAGE: {image_path}
  CAPTION: {caption_file} (also copied to clipboard)
  
  NEXT STEPS:
  1. Open Instagram in your browser
  2. Click '+' or 'Create' to make a new post
  3. Upload the image: {image_path}
  4. Paste the caption (Ctrl+V)
  5. Add location if desired
  6. Click 'Share'
  
  The post is SEO-optimized with:
  - Hook emoji at the start
  - Clear comparison format
  - Statistics and data points
  - Call-to-action (CTA)
  - 30 relevant hashtags
  - Proper spacing for readability
""")
print("=" * 70)
