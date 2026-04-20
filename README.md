# Fenwig5.github.io
This is my portfolio with projects in the following categories: [v1.0.0]
- software engineering
- web development
- machine learning
- data analysis
- cyber security
- server administration
- e-commerce

## DONE:
- [x] 
- [x] 
- [x] 
- [x] 
- [x] 

## IDEAS / TO DO:
- [ ] add all portfolio worthy stuff from college (especially UML)

- [ ] Make markdown previewer functional
- [ ] Make drum machine functional
- [ ] Make survey submittable and better
- [ ] add description overview of owl assist project

- [ ] Make an algorithms/engineering in action page/section
        pages to finish pomodoro clock
        javascript calculator
        javascript random quote machine
        javascript roman numeral converter
        javascript shift cipher
        javascript  temperature converter
        survey form
        java deadlock monitor
        python directory mapper?
        c employee pay system
        c++ rolodex
        psidemica.com (art portfolio, e-commerce shop, members hub)

- [ ] Make a data analysis page/section
        internet by country poster pdf
        particulate matter analysis pdf
        planaria analysis pdf
        solar wind analysis pdf
        pages to finish choropleth map
        pages to finish heat map
        pages to finish scatterplot graph
        pages to finish treemap diagram
        d3 bar chart?

- [ ] Make a machine learning page/section
        preprocessing experimentation for breast cancer classification
        python notebooks (decision trees, logistic regression, pca, kmeans)

- [ ] make a cyber security page/section
        python notebooks (key inversion, ciphertext to binary)
        java rc4ksa
        java symmetric encryption, decryption, and transmission
        java additive cipher
        java block cypher encrypt and decrypt

- [ ] make a section/page for shell/lab scripts
        bash user management
        setup docs for owncloud?
        setup doc for external mail routing?
        python music library management script?
        bash audio conversion scripts
        python batch rename
        python playlist map?
        bash executable file locator
        bash list concatenation
        bash file and directory renamer
        bash disk usage warning system
        python decode?

- [ ] make a setup script for arch linux
- [ ] store textbook files? (unlisted? legality?)
- [ ] remove code from education directories (and code archive?) after integrating

ANALYSIS

If it doesn’t answer:
“Would I hire this person based on this?”
…it shouldn’t be on your main site.

Top-tier (lead with these):
Psidemica (FULL STACK MONSTER)
    This is your crown jewel. It screams ownership + complexity.
    You built auth, APIs, e-commerce, admin tools?? Yeah—this goes first.
Owl Assist (real-world system + team experience)
    Has cloud, scraping, AI, collaboration
    This is your “I’ve worked on real systems” proof
Published Research (ML paper)
    Instant credibility bump
    Most devs don’t have this → leverage it hard

Mid-tier (good, but needs framing):
Data analysis posters + papers
Python notebooks (ML techniques)
Shell scripts (ONLY if grouped as tooling/automation)
C / C++ projects (if explained well)
These need context + story, not just “here’s code”.
Setup docs (turned into polished guides)

Low-tier
These are portfolio fillers, not differentiators:
Calculator
Temperature converter
Roman numeral converter
Shift cipher
Random quote machine
Survey form
Group them into a “Foundations / Early Projects” section

Suggested repo structure

/portfolio
  /apps
    /psidemica
    /owl-assist
    /hub-app (your React/.NET project)

  /data-ml
    /breast-cancer-research
    /data-analysis-projects
    /notebooks

  /engineering
    /c-pay-system
    /cpp-rolodex
    /java-projects

  /visualizations
    /d3-bar-chart (only if polished and solid, maybe interactive, relate to a data-ml project)
    /heatmap
    /scatterplot
    /treemap

  /tools
    /shell-automation
    /python-scripts

  /archive
    /freecodecamp-projects
      /calculator
      /roman-numeral
      /etc

  /assets
  index.html
  README.md

Ideal site structure (clean + professional)

🧭 NAVBAR
Home
Projects
Research
Experience
Contact

🏠 HOME (landing)
Short. Punchy.
Name + tagline
2–3 featured projects (cards)
Quick tech stack
Link to GitHub + LinkedIn

💻 PROJECTS PAGE (THIS IS THE MONEY PAGE)
🔥 Featured Projects
Psidemica
Owl Assist
Hub App (even if WIP)
Each gets:
Screenshot
Tech stack
2–3 bullet achievements
Link to repo + demo
🧠 Engineering Projects
C / C++ / Java work
Focus on:
problem solved
complexity
performance
📊 Data + ML
Research paper
Posters
Notebooks (summarized, not dumped)
🛠 Tools & Automation
Shell + Python scripts (grouped)
Present as:
“Automation Toolkit”
🧊 Foundations (collapsed section)
All your FCC-style apps go here.

📚 RESEARCH PAGE
You already have this mostly right—just clean layout.

💼 EXPERIENCE
This section is actually strong. Keep it.

Add THIS to every project:
Instead of:
“I made a calculator”
Do:
JavaScript Calculator
- Built dynamic expression parser using JS
- Implemented input validation and operator handling
- Designed responsive UI
Tech: JavaScript, HTML, CSS
👉 You’re selling thinking, not just output.

What you're missing (and should add ASAP)
These will dramatically boost your portfolio:
🚀 1. One MODERN stack project
You mentioned:
React + Tailwind + ASP.NET + Docker
👉 Finish even a small slice of this and feature it.
🚀 2. GitHub hygiene
Each major project should have:
clean README
screenshots
setup instructions
🚀 3. “Engineering thinking”
Add sections like:
“Challenges”
“Design decisions”
“Tradeoffs”
That’s what separates juniors from mid-level.

Separate Research page or not?
Short answer:
👉 Yes, but don’t duplicate content
Why:
“Projects” = engineering signal
“Research” = analytical depth signal
Recruiters and hiring managers mentally separate those.
How to do it cleanly:
Projects page
Show:
Psidemica
Owl Assist
Apps / engineering work
Include a small “Research highlights” section (1–2 items max)
Research page
Full breakdown:
Paper
Posters
Analysis work
ML experiments
👉 Think:
Projects = “I build systems”
Research = “I think deeply and analyze data”

How to include Java / C / C++ code
If you dump code on your site, you lose people immediately. Nobody is reading 500 lines of Java on a portfolio.
❌ Don’t:
Embed full files
Try to run everything in-browser
Treat your site like GitHub
✅ Do this instead (this is the winning pattern):
For each project:
1. Explain the problem
“Detect and prevent deadlocks in concurrent systems”
2. Show a small, meaningful snippet
// Example: detecting circular wait condition
if (visited.contains(thread)) {
    return true; // deadlock detected
}
3. Explain the thinking
Why this approach?
What’s the complexity?
What tradeoffs?
4. Link to repo
“Full implementation available on GitHub”

For your reuse goal (this is important)
You said:
“I want to reuse this logic later”
Good instinct. Do this:
Create a separate “code library” repo
/cs-snippets
  /algorithms
  /data-structures
  /concurrency
  /parsing
Keep it clean, reusable, documented
👉 Your portfolio = showcase
👉 That repo = your toolbox

Should your React app be public?
Yes. No hesitation.
Here’s the blunt truth:
Nobody cares if your idea is unique. They care if you can build.
What making it public signals:
You understand modern stack
You can structure a real app
You’re not hiding behind tutorials
What to avoid:
Messy commit history
Half-broken main branch
👉 If needed:
Clean it up
Add README
Then publish

Psidemica being private (this is normal)
You’re overthinking the “security risk” part a bit.
You’re not protecting nuclear launch codes—you’re protecting:
credentials
internal logic
vulnerabilities
✅ Safe to share:
Architecture
Features
Data flow
Screenshots
High-level logic
❌ Do NOT share:
API keys
Auth logic details
Database schema specifics (sensitive parts)
Anything exploitable
Pro move (do this):
Add a section:
“Technical Deep Dive (High-Level)”
Example:
- Custom authentication system using session-based validation
- Server-side validation for all user inputs
- Structured routing system for handling dynamic content
👉 Sounds detailed
👉 Reveals nothing dangerous