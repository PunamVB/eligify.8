import sqlite3

con = sqlite3.connect("opportunities.db")

# name, type, class_min, class_max, stream, state, gender, cost,
# deadline, official_link, note, last_verified
rows = [
    # ---------- School olympiads ----------
    (
        "Indian Olympiad Qualifier in Mathematics (IOQM)",
        "Olympiad", 11, 12,
        "Any", "All India", "Any",
        "Verify on official site",
        "Verify on official site",
        "",
        "Details to be verified on the official site.",
        "not verified",
    ),
    (
        "National Standard Examination in Physics (NSEP)",
        "Olympiad", 11, 12,
        "Science", "All India", "Any",
        "Verify on official site",
        "Verify on official site",
        "",
        "Details to be verified on the official site.",
        "not verified",
    ),
    (
        "Indian Computing Olympiad",
        "Olympiad", 11, 12,
        "Any", "All India", "Any",
        "Verify on official site",
        "Verify on official site",
        "",
        "Details to be verified on the official site.",
        "not verified",
    ),
    # ---------- UG / professional certificate programmes ----------
    (
        "IIT Bombay Certificate in Agentic AI for Working Professionals",
        "Certificate Course", "UG", "",
        "Any", "All India", "Any",
        "Paid (fee not shown on page)",
        "2026-10-15",
        "https://www.mygreatlearning.com/iit-bombay-agentic-ai",
        "5-month online certificate with weekly live sessions, curriculum by IIT Bombay faculty and offered through Great Learning. Covers agentic AI, MCP, RAG, multi-agent systems, CrewAI and LangGraph. Fee is only given after submitting the brochure form.",
        "2026-10-12",
    ),
    (
        "IIT Patna Certificate Programme in Generative AI for Professionals",
        "Certificate Course", "UG", "",
        "Any", "All India", "Any",
        "Rs 79,999 (EMI available)",
        "Verify on official site",
        "https://iitpatna.com/generative-ai-for-professionals",
        "6-month live online programme (Batch 9 open). Covers 30+ AI tools, AI agents, automation and AI web apps, with a capstone. No prior coding required. Optional paid 2-day campus immersion. No closing date shown on the page. Page says the fee rises to Rs 1,34,999 for the next batch.",
        "2026-10-12",
    ),
    (
        "Agentic AI Certification - Vishlesan i-Hub Foundation, IIT Patna (Techademy)",
        "Certificate Course", "UG", "",
        "Any", "All India", "Any",
        "Rs 74,999 to Rs 79,999 (EMI available)",
        "2026-10-17",
        "https://www.techademy.com/vishlesan-i-hub-iit-patna-agentic-ai",
        "26-week (6-month) live online programme for working professionals and graduates, run by Techademy. Covers AI agents, RAG, MCP, multi-agent systems and an enterprise capstone. Also gives a Microsoft certificate (Develop AI Agents on Azure). Fees are non-refundable. The page shows two different fee figures, so check before relying on it.",
        "2026-10-12",
    ),
    (
        "IIM Tiruchirappalli Executive Certification in Generative AI for Management Leaders",
        "Certificate Course", "UG", "",
        "Any", "All India", "Any",
        "Rs 1,30,000 + GST",
        "Verify on official site",
        "https://www.iimtrichy.ac.in/ecgaiml",
        "6-month live online certificate programme (Saturdays, 9:30 am to 12:45 pm), academic delivery and certificate by IIM Tiruchirappalli. Eligibility: bachelor's degree in any discipline and minimum 5 years of work experience. Ad says only 50 leaders are selected. Covers GenAI and agentic AI across HR, Marketing, Finance, Operations and Strategy, ending in a capstone. A certificate programme, not a degree or diploma. Page only says application closing soon.",
        "2026-10-12",
    ),
    (
        "Intellipaat x iHub DivyaSampark IIT Roorkee - AI & Data Science (student programme)",
        "Certificate Course", "UG", "",
        "Any", "All India", "Any",
        "Paid (fee not listed)",
        "Verify on official site",
        "",
        "Online programme with live classes by IIT faculty and industry experts, campus immersion at iHub IIT Roorkee, and internship assistance. Ad targets students before they graduate. Run by Intellipaat; certificate from iHub DivyaSampark, IIT Roorkee. Fee, duration, deadline and eligibility not confirmed. Add the exact programme link before publishing.",
        "2026-10-12",
    ),
    (
        "iHub Drishti IIT Jodhpur - Professional Certificate Program in Gen AI & Agentic AI",
        "Certificate Course", "UG", "",
        "Any", "All India", "Any",
        "Paid (fee not listed)",
        "Verify on official site",
        "",
        "Professional certificate programme from iHub Drishti, IIT Jodhpur, with a Microsoft certificate. Ad says: learn from IIT faculty and industry experts, 12 academic credits approved by AICTE and NSQF, alumni status of iHub Drishti IIT Jodhpur, and job assistance. Fee, duration, deadline and eligibility not confirmed. Add the exact programme link before publishing.",
        "2026-10-12",
    ),
    (
        "IIT Jammu Cybersecurity Program (LearnAI)",
        "Certificate Course", "UG", "",
        "Any", "All India", "Any",
        "Verify on official site",
        "Verify on official site",
        "https://learnai.in/iitjammu-cybersecurity",
        "Cybersecurity programme with IIT Jammu, listed on LearnAI. I could not open this page, so the type, fee, duration, deadline and eligibility are all unconfirmed. Check the page and update before publishing.",
        "2026-10-12",
    ),
    (
        "Confluentia 2026 Hackathon - RL Track (with 2une.ai)",
        "Hackathon", "UG", "",
        "Any", "Uttar Pradesh", "Any",
        "Verify on official site",
        "Verify on official site",
        "https://eventsplanning.ai/portal/confluentia/hackathon/",
        "48-hour reinforcement learning hackathon at Confluentia 2026, IIT (BHU) Varanasi, with 2une.ai (PW's initiative). Exclusive to IIT (BHU) students. Teams of up to 3. Problem statements drop on 23 October, with a mentoring session by PW on 24 October. Registration deadline, fee and prizes not found.",
        "2026-10-12",
    ),
    ]


added = updated = 0
for r in rows:
    found = con.execute("SELECT id FROM opportunities WHERE name = ?", (r[0],)).fetchone()
    if found:
        con.execute("""UPDATE opportunities SET
            type=?, class_min=?, class_max=?, stream=?, state=?, gender=?, cost=?,
            deadline=?, official_link=?, note=?, last_verified=?
            WHERE id=?""", r[1:] + (found[0],))
        updated += 1
    else:
        con.execute("""INSERT INTO opportunities
            (name,type,class_min,class_max,stream,state,gender,cost,
             deadline,official_link,note,last_verified)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", r)
        added += 1

con.commit()
con.close()
print(f"Added: {added}, Updated: {updated}")
