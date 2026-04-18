from groq import Groq
import gradio as gr
import datetime
import os

client = None

def set_client(api_key):
    global client
    if api_key.strip():
        client = Groq(api_key=api_key.strip())
        return "✅ API Key set! App ready to use."
    return "⚠️ Please enter a valid API key."

def check_client():
    return client is not None

def generate_linkedin_post(topic, tone, length, language, audience, include_cta):
    if not check_client():
        return "⚠️ Please enter your Groq API key first!", "", ""

    length_map = {
        "Short (< 300 chars)": "Keep it under 300 characters, punchy and direct",
        "Medium (300-700 chars)": "Keep it between 300-700 characters",
        "Long (700+ chars)": "Write a detailed post of 700+ characters"
    }
    lang_map = {
        "English": "Write in professional English",
        "Hinglish": "Write in Hinglish (mix of Hindi and English)",
        "Urdu": "Write in Roman Urdu script"
    }
    cta = "End with a strong Call To Action." if include_cta else ""

    prompt = f"""Generate 3 different LinkedIn post variations.

Topic: {topic}
Tone: {tone}
Length: {length_map[length]}
Audience: {audience}
Language: {lang_map[language]}
{cta}

Rules:
- Use emojis smartly
- Add relevant hashtags at end
- Each variation must feel different in style

Format EXACTLY like:
--- VARIATION 1 ---
[post]

--- VARIATION 2 ---
[post]

--- VARIATION 3 ---
[post]"""

    try:
        msg = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        result = msg.choices[0].message.content

        if topic.strip():
            entry = f"📌 {topic[:50]} | {tone} | {language} | {datetime.datetime.now().strftime('%H:%M')}"
            post_history.insert(0, entry)
            if len(post_history) > 5:
                post_history.pop()

        variations = result.split("--- VARIATION")
        char_info = ""
        for i, v in enumerate(variations[1:], 1):
            text = v.split("---")[-1].strip() if "---" in v else v.strip()
            bar = "█" * min(int(len(text) / 20), 30)
            char_info += f"Variation {i}: {len(text)} chars  {bar}\n"

        history_text = "\n".join(post_history) if post_history else "No history yet."
        return result, char_info, history_text

    except Exception as e:
        return f"ERROR: {str(e)}", "", ""


def score_post(post_text):
    if not check_client():
        return "⚠️ Please enter your Groq API key first!"
    if not post_text.strip():
        return "⚠️ Please paste a post to score."

    prompt = f"""You are a LinkedIn content expert. Analyze this post and give a detailed review.

POST:
{post_text}

Give your response in this EXACT format:

OVERALL SCORE: [X/10]

BREAKDOWN:
- Hook Strength: [X/10] — [one line reason]
- Readability: [X/10] — [one line reason]
- Engagement Potential: [X/10] — [one line reason]
- Hashtag Quality: [X/10] — [one line reason]
- Call To Action: [X/10] — [one line reason]

WHAT'S GOOD:
[2-3 bullet points]

IMPROVEMENTS NEEDED:
[2-3 bullet points]

IMPROVED VERSION:
[Rewrite the post making it better]"""

    try:
        msg = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.choices[0].message.content
    except Exception as e:
        return f"ERROR: {str(e)}"


def generate_hashtags(topic, industry, goal):
    if not check_client():
        return "⚠️ Please enter your Groq API key first!"

    prompt = f"""Generate the best LinkedIn hashtags for this topic.

Topic: {topic}
Industry: {industry}
Goal: {goal}

Format EXACTLY like:

🔥 TOP 5 POWER HASHTAGS (highest reach):
#tag1 #tag2 #tag3 #tag4 #tag5

🎯 NICHE HASHTAGS (targeted audience):
#tag1 #tag2 #tag3 #tag4 #tag5

📈 TRENDING HASHTAGS (currently popular):
#tag1 #tag2 #tag3 #tag4 #tag5

💡 COPY-PASTE COMBO (best mix for your post):
#tag1 #tag2 #tag3 #tag4 #tag5 #tag6 #tag7 #tag8

PRO TIP: [one actionable tip about using hashtags]"""

    try:
        msg = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.choices[0].message.content
    except Exception as e:
        return f"ERROR: {str(e)}"


def generate_bio(name, role, skills, experience, goal, tone):
    if not check_client():
        return "⚠️ Please enter your Groq API key first!"

    prompt = f"""Write 3 variations of a powerful LinkedIn bio/headline+summary.

Name: {name}
Current Role: {role}
Top Skills: {skills}
Experience: {experience} years
Career Goal: {goal}
Tone: {tone}

Format EXACTLY like:

--- BIO VARIATION 1 ---
HEADLINE: [catchy headline under 220 chars]
SUMMARY:
[3-4 line professional summary]

--- BIO VARIATION 2 ---
HEADLINE: [different style headline]
SUMMARY:
[3-4 line summary different approach]

--- BIO VARIATION 3 ---
HEADLINE: [creative headline]
SUMMARY:
[3-4 line summary storytelling style]"""

    try:
        msg = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.choices[0].message.content
    except Exception as e:
        return f"ERROR: {str(e)}"


def get_best_time(audience, timezone, goal):
    if not check_client():
        return "⚠️ Please enter your Groq API key first!"

    prompt = f"""You are a LinkedIn algorithm expert. Give the best posting schedule.

Target Audience: {audience}
Timezone: {timezone}
Goal: {goal}

Format EXACTLY like:

📅 BEST DAYS TO POST:
[ranked list with reason]

⏰ BEST TIME SLOTS:
[Morning slot] — [why]
[Afternoon slot] — [why]
[Evening slot] — [why]

❌ WORST TIMES TO POST:
[list with reasons]

📊 WEEKLY SCHEDULE:
Monday: [time] — [content type]
Tuesday: [time] — [content type]
Wednesday: [time] — [content type]
Thursday: [time] — [content type]
Friday: [time] — [content type]
Saturday: [time] — [content type]
Sunday: [time] — [content type]

💡 ALGORITHM TIP:
[one powerful insight]"""

    try:
        msg = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.choices[0].message.content
    except Exception as e:
        return f"ERROR: {str(e)}"


def generate_content_ideas(industry, role, frequency):
    if not check_client():
        return "⚠️ Please enter your Groq API key first!"

    prompt = f"""Generate a full LinkedIn content strategy.

Industry: {industry}
Role: {role}
Posting Frequency: {frequency} posts per week

Format EXACTLY like:

🗓️ 30-DAY CONTENT CALENDAR:

WEEK 1:
- Post 1: [topic] | Type: [Story/Tips/Poll/Question] | Hook: [first line]
- Post 2: [topic] | Type: [Story/Tips/Poll/Question] | Hook: [first line]
- Post 3: [topic] | Type: [Story/Tips/Poll/Question] | Hook: [first line]

WEEK 2:
- Post 1: [topic] | Type: [...] | Hook: [...]
- Post 2: [topic] | Type: [...] | Hook: [...]
- Post 3: [topic] | Type: [...] | Hook: [...]

WEEK 3:
- Post 1: [topic] | Type: [...] | Hook: [...]
- Post 2: [topic] | Type: [...] | Hook: [...]
- Post 3: [topic] | Type: [...] | Hook: [...]

WEEK 4:
- Post 1: [topic] | Type: [...] | Hook: [...]
- Post 2: [topic] | Type: [...] | Hook: [...]
- Post 3: [topic] | Type: [...] | Hook: [...]

🔥 VIRAL CONTENT FORMULAS:
[3 proven formulas with examples]

📌 CONTENT PILLARS:
[4-5 content pillars for your profile]"""

    try:
        msg = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.choices[0].message.content
    except Exception as e:
        return f"ERROR: {str(e)}"


# ─────────────────────────────────────────
# UI
# ─────────────────────────────────────────
post_history = []

css = """
body { font-family: 'Segoe UI', sans-serif; background: #f3f6f9; }
.gradio-container { max-width: 1100px !important; margin: auto !important; }
footer { display: none !important; }
.header-box {
    background: linear-gradient(135deg, #0077B5 0%, #004182 100%);
    padding: 32px 24px; border-radius: 16px;
    text-align: center; margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(0,119,181,0.3);
}
.header-box h1 { color: white !important; font-size: 2.2em; margin: 0; }
.header-box p  { color: #cce8f4; margin: 8px 0 0 0; }
.stats-row { display: flex; gap: 12px; margin-bottom: 20px; }
.stat-card {
    flex: 1; background: white; border-radius: 12px;
    padding: 16px; text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border-top: 3px solid #0077B5;
}
.stat-card .num { font-size: 1.8em; font-weight: 700; color: #0077B5; }
.stat-card .lbl { font-size: 0.78em; color: #666; margin-top: 2px; }
.gr-button-primary {
    background: linear-gradient(135deg, #0077B5, #005f8e) !important;
    border: none !important; color: white !important;
    font-weight: 700 !important; border-radius: 10px !important;
    box-shadow: 0 4px 15px rgba(0,119,181,0.3) !important;
}
.tips-box {
    background: #e8f4fd; border-left: 4px solid #0077B5;
    border-radius: 0 10px 10px 0; padding: 12px 16px;
    margin-top: 8px; font-size: 0.88em; color: #004182;
}
"""

with gr.Blocks(css=css, theme=gr.themes.Soft(
    primary_hue="blue",
    neutral_hue="slate",
    font=gr.themes.GoogleFont("Inter")
)) as demo:

    gr.HTML("""
    <div class="header-box">
        <h1>💼 LinkedIn Growth Suite</h1>
        <p>AI-Powered Post Generator • Scorer • Hashtags • Bio • Schedule • Content Calendar</p>
    </div>
    <div class="stats-row">
        <div class="stat-card"><div class="num">6</div><div class="lbl">AI Tools</div></div>
        <div class="stat-card"><div class="num">3</div><div class="lbl">Post Variations</div></div>
        <div class="stat-card"><div class="num">∞</div><div class="lbl">Content Ideas</div></div>
        <div class="stat-card"><div class="num">3</div><div class="lbl">Languages</div></div>
    </div>
    """)

    # API KEY SECTION
    gr.HTML("""
    <div style="background:#fff3cd; border-left:4px solid #ffc107;
    padding:12px 16px; border-radius:0 10px 10px 0; margin-bottom:16px;">
    ⚠️ <b>Important:</b> You need a free Groq API key to use this app.
    Get it free at <a href="https://console.groq.com" target="_blank">console.groq.com</a>
    </div>
    """)
    with gr.Row():
        api_input = gr.Textbox(label="🔑 Enter Your Groq API Key", placeholder="gsk_...", type="password", scale=3)
        api_btn = gr.Button("Set API Key", variant="primary", scale=1)
        api_status = gr.Textbox(label="Status", scale=2, interactive=False)
    api_btn.click(set_client, [api_input], [api_status])

    with gr.Tabs():

        with gr.TabItem("✍️ Post Generator"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📋 Post Settings")
                    topic_in = gr.Textbox(label="Topic / Idea", placeholder="e.g., AI in workplace, my first job rejection...", lines=3)
                    with gr.Row():
                        tone_in = gr.Dropdown(["Professional","Casual","Inspirational","Educational","Storytelling","Humorous"], label="Tone", value="Professional")
                        lang_in = gr.Dropdown(["English","Hinglish","Urdu"], label="Language", value="English")
                    with gr.Row():
                        len_in = gr.Dropdown(["Short (< 300 chars)","Medium (300-700 chars)","Long (700+ chars)"], label="Length", value="Medium (300-700 chars)")
                        aud_in = gr.Dropdown(["General Professionals","Students & Freshers","Entrepreneurs","Tech Community","HR & Recruiters"], label="Audience", value="General Professionals")
                    cta_in = gr.Checkbox(label="✅ Include Call-To-Action", value=True)
                    with gr.Row():
                        gen_btn = gr.Button("🚀 Generate 3 Variations", variant="primary", scale=2)
                        clr_btn = gr.Button("🗑️ Clear", scale=1)
                    gr.HTML('<div class="tips-box">💡 <b>Pro Tip:</b> "Storytelling" tone gets 3x more engagement. Be specific with your topic.</div>')
                with gr.Column(scale=1):
                    gr.Markdown("### 📝 Generated Posts")
                    post_out = gr.Textbox(label="3 Variations (editable)", lines=18, interactive=True)
                    char_out = gr.Textbox(label="📊 Character Count", lines=3, interactive=False)
                    gr.Markdown("#### 🕘 Recent History")
                    hist_out = gr.Textbox(label="Last 5 Topics", lines=5, interactive=False)
            gr.Examples(
                examples=[
                    ["AI transforming workplace productivity","Professional","Medium (300-700 chars)","English","Tech Community",True],
                    ["My first job rejection taught me everything","Storytelling","Long (700+ chars)","English","Students & Freshers",True],
                    ["Career growth tips for freshers","Inspirational","Medium (300-700 chars)","Hinglish","Students & Freshers",True],
                ],
                inputs=[topic_in, tone_in, len_in, lang_in, aud_in, cta_in]
            )
            gen_btn.click(generate_linkedin_post, [topic_in,tone_in,len_in,lang_in,aud_in,cta_in], [post_out,char_out,hist_out])
            clr_btn.click(lambda: ("","",""), [], [post_out,char_out,topic_in])

        with gr.TabItem("⭐ Post Scorer"):
            gr.Markdown("### Paste any LinkedIn post — AI will score it and suggest improvements")
            with gr.Row():
                with gr.Column():
                    score_in = gr.Textbox(label="Paste Your Post Here", lines=10)
                    score_btn = gr.Button("🔍 Analyze & Score", variant="primary")
                with gr.Column():
                    score_out = gr.Textbox(label="📊 AI Analysis", lines=20, interactive=False)
            score_btn.click(score_post, [score_in], [score_out])

        with gr.TabItem("# Hashtag Generator"):
            gr.Markdown("### Generate perfect hashtags for maximum reach")
            with gr.Row():
                with gr.Column():
                    htag_topic = gr.Textbox(label="Post Topic", placeholder="e.g., machine learning, remote work")
                    htag_industry = gr.Dropdown(["Technology","Marketing","Finance","Healthcare","Education","HR","Entrepreneurship","Design","Sales","Other"], label="Industry", value="Technology")
                    htag_goal = gr.Dropdown(["Grow followers","Get job offers","Generate leads","Build personal brand","Network with professionals"], label="Goal", value="Build personal brand")
                    htag_btn = gr.Button("# Generate Hashtags", variant="primary")
                with gr.Column():
                    htag_out = gr.Textbox(label="Your Hashtag Strategy", lines=18, interactive=True)
            htag_btn.click(generate_hashtags, [htag_topic,htag_industry,htag_goal], [htag_out])

        with gr.TabItem("👤 Bio Generator"):
            gr.Markdown("### Create a powerful LinkedIn headline + summary")
            with gr.Row():
                with gr.Column():
                    bio_name = gr.Textbox(label="Your Name", placeholder="e.g., Sameen Fatima")
                    bio_role = gr.Textbox(label="Current Role", placeholder="e.g., CS Student | Aspiring ML Engineer")
                    bio_skills = gr.Textbox(label="Top Skills", placeholder="e.g., Python, Machine Learning, Blockchain")
                    bio_exp = gr.Slider(0, 20, value=1, step=1, label="Years of Experience")
                    bio_goal = gr.Textbox(label="Career Goal", placeholder="e.g., Land a job at a top tech company")
                    bio_tone = gr.Dropdown(["Professional","Creative","Ambitious","Humble & Inspiring"], label="Tone", value="Professional")
                    bio_btn = gr.Button("✨ Generate Bio", variant="primary")
                with gr.Column():
                    bio_out = gr.Textbox(label="3 Bio Variations", lines=22, interactive=True)
            bio_btn.click(generate_bio, [bio_name,bio_role,bio_skills,bio_exp,bio_goal,bio_tone], [bio_out])

        with gr.TabItem("⏰ Best Time to Post"):
            gr.Markdown("### Find optimal posting schedule for your audience")
            with gr.Row():
                with gr.Column():
                    time_aud = gr.Dropdown(["General Professionals","Students","Entrepreneurs","Tech Professionals","Recruiters & HR"], label="Target Audience", value="General Professionals")
                    time_tz = gr.Dropdown(["Pakistan Standard Time (PKT)","India Standard Time (IST)","Gulf Standard Time (GST)","UTC","US Eastern Time","US Pacific Time"], label="Timezone", value="Pakistan Standard Time (PKT)")
                    time_goal = gr.Dropdown(["Maximize views","Get more connections","Generate leads","Job hunting","Thought leadership"], label="Goal", value="Maximize views")
                    time_btn = gr.Button("📅 Get My Schedule", variant="primary")
                with gr.Column():
                    time_out = gr.Textbox(label="Your Personalized Schedule", lines=22, interactive=False)
            time_btn.click(get_best_time, [time_aud,time_tz,time_goal], [time_out])

        with gr.TabItem("📅 Content Calendar"):
            gr.Markdown("### Get a full 30-day LinkedIn content strategy")
            with gr.Row():
                with gr.Column():
                    cal_industry = gr.Textbox(label="Your Industry", placeholder="e.g., Software Engineering, Digital Marketing")
                    cal_role = gr.Textbox(label="Your Role", placeholder="e.g., CS Student, Software Developer")
                    cal_freq = gr.Slider(1, 7, value=3, step=1, label="Posts Per Week")
                    cal_btn = gr.Button("📅 Generate 30-Day Calendar", variant="primary")
                    gr.HTML('<div class="tips-box">💡 <b>Consistency beats virality.</b> 3 posts/week for 3 months beats 1 viral post.</div>')
                with gr.Column():
                    cal_out = gr.Textbox(label="Your 30-Day Content Plan", lines=22, interactive=True)
            cal_btn.click(generate_content_ideas, [cal_industry,cal_role,cal_freq], [cal_out])

    gr.HTML("""
    <div style="text-align:center; padding:20px; color:#666; font-size:0.85em; margin-top:16px;">
        Built with ❤️ using Groq AI + Gradio &nbsp;|&nbsp; LinkedIn Growth Suite v2.0
    </div>
    """)

demo.launch()
