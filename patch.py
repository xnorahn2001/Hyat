import re
import os

filepath = '/Users/norahalnaif/Desktop/Hyat/Hyat.html'
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update logo to image
logo_pattern = r'<svg width="40" height="24" viewBox="0 0 130 72" fill="none">.*?</svg>\s*<div>\s*<div class="logo-text">حياة</div>\s*<span class="logo-sub">HYAT</span>\s*</div>'
new_logo = r'<img src="hayat logo -06.png" style="height: 36px; object-fit: contain;" alt="Hyat Logo" />'
html = re.sub(logo_pattern, new_logo, html, flags=re.DOTALL)

# 2. Add Lang Toggle button next to logo-wrap
logo_wrap_pattern = r'(<div class="logo-wrap"[^>]*>.*?<img src="hayat logo -06.png"[^>]*>)'
lang_html = r'''\1
        <div class="lang-switch" onclick="toggleLang(event)" style="cursor:pointer; display:flex; align-items:center; gap:6px; font-size:12px; font-weight:500; color:rgba(255,255,255,0.7); background:rgba(255,255,255,0.05); padding:6px 12px; border-radius:20px; border:1px solid rgba(255,255,255,0.1); margin-inline-start:12px; transition:0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
          <span class="lang-ind">EN</span>
        </div>'''
html = re.sub(logo_wrap_pattern, lang_html, html)

# Wrap them so flex space-between works correctly without splitting them
wrap_pattern = r'(<div class="logo-wrap"[^>]*>.*?<img src="hayat logo -06.png"[^>]*>\s*<div class="lang-switch".*?</div>)'
html = re.sub(wrap_pattern, r'<div style="display:flex;align-items:center;">\1</div>', html, flags=re.DOTALL)

# 3. CSS RTL to LTR alignments
html = html.replace('text-align: right;', 'text-align: start;')
html = html.replace('text-align: left;', 'text-align: end;')

old_after = r'\.opt\.sel::after\s*\{[^}]*\}'
new_after = r'''[dir="rtl"] .opt.sel::after {
      content: '✓'; position: absolute; left: 18px; top: 50%; transform: translateY(-50%); color: var(--coral); font-size: 16px;
    }
    [dir="ltr"] .opt.sel::after {
      content: '✓'; position: absolute; right: 18px; top: 50%; transform: translateY(-50%); color: var(--coral); font-size: 16px;
    }'''
html = re.sub(old_after, new_after, html)

# 4. Inject Translation script at the end of body
i18n_script = r'''
<script>
  let currentLang = 'ar';
  
  // English questions & profiles overrides
  const enQ_texts = [
    "How many hours did you sleep last night?",
    "When was the last time you took a full day off — no work, no messages?",
    "How do you rate your stress level right now?",
    "Your body sends you signals. Do you actually listen?",
    "Have you talked to anyone about your health and mood in the last 3 months?",
    "If your health was a metric in your company, how would it be right now?"
  ];
  const enQ_opts = [
    ["Less than 4 hours", "4–5 hours", "6 hours", "7 or more"],
    ["This week", "This month", "More than a month", "I honestly can't remember"],
    ["Low — I'm fine", "Manageable", "High — running on adrenaline", "Critical — reached the limit"],
    ["Yes — I check in daily", "Sometimes — when it gets loud", "Rarely — no time", "What signals? I'm numb"],
    ["Yes — therapist or coach", "Yes — close friend", "No — only to family", "No — and I won't"],
    ["Steady growth 📈", "Stagnant, no growth", "Declining — needs intervention", "Pre-revenue 😬"]
  ];
  const enP_labels = ["Critical Charge", "Low Charge", "Medium Charge", "Strong Charge"];
  const enP_titles = [
    "Your body is asking for help... <em>for a while.</em>",
    "You work. But <em>working isn't thriving.</em>",
    "Better than most. <em>Let's keep it that way.</em>",
    "You are a <em>rare breed.</em> Protect this."
  ];
  const enP_oneThing = [
    "Give yourself one honest conversation — no performance, no investor mask. <em>HYAT is that place.</em>",
    "10 mins personal review every week — private, honest, tracked. <em>From there HYAT starts.</em>",
    "Stay consistent. <em>HYAT helps you track your health before it becomes a crisis.</em>",
    "<em>Share this with your partner or team.</em> Culture starts with you."
  ];
  const enP_cards = [
    [
      {h: "Sleep debt is accumulating", p: "Consistently under 5hrs impairs decisions like alcohol. Your company pays the cognitive cost daily."},
      {h: "Running on adrenaline, not energy", p: "Adrenaline looks like productivity. But it's an emergency system — with a limit."},
      {h: "73% of founders are here", p: "The only difference: those who handle it early keep their company alive much longer."}
    ],
    [
      {h: "You are in a maintenance loop", p: "Everything works until one thing is added. One bad week is enough — and you know it."},
      {h: "Rest is strategy, not reward", p: "Founders who last 10 years don't rest less — they protect their rest differently."},
      {h: "Your body knows what you need", p: "You answered 'Sometimes' to signals. That 'sometimes' is the actual starting point."}
    ],
    [
      {h: "You have awareness — rare", p: "Most founders in the room answered worse. Attention alone puts you ahead."},
      {h: "Prevention is cheaper than recovery", p: "Burnout costs 3-6 months. You're not there yet — don't wait until you are."},
      {h: "Community is untapped", p: "Isolation is the silent multiplier. A place that understands chronic stress changes everything."}
    ],
    [
      {h: "You take basics seriously", p: "Sleep, boundaries, support — you have pillars. This is not common here at all."},
      {h: "One hard quarter erases this", p: "Scaling, funding, team crisis — habits erode fast. Systems before hard times is key."},
      {h: "You can model this for your team", p: "Founder health culture spreads down. If you protect yours, you normalize it for everyone."}
    ]
  ];

  // Static translations dictionary
  const dict = {
    "لوحة التحكم ↗": "Dashboard ↗",
    "← الرئيسية": "← Home",
    "اليوم العالمي للصحة · 7 أبريل": "World Health Day · Apr 7",
    "ما هي\nبطارية جسمك؟": "What is your\nbody battery?",
    "6 أسئلة صريحة، نتيجة فورية، بدون اسم ولا حساب. اكتشف أين تقف صحتك كمؤسس.": "6 honest questions, instant result, completely anonymous. Find out where your health stands as a founder.",
    "من المؤسسين يعانون\nالإرهاق بصمت": "of founders suffer\nsilent burnout",
    "فقط يطلبون\nأي دعم": "only ask for\nany support",
    "من فشل الشركات يبدأ\nبصحة المؤسس": "of startup failures begin\nwith founder's health",
    "ابدأ الاختبار ←": "Start Quiz →",
    "مجهول الهوية تماماً — اسمك لا يُجمع أبداً": "Completely anonymous — your name is never collected",
    "التالي ←": "Next →",
    "أظهر نتيجتي ←": "Show Result →",
    "مجهول الهوية — لا يتم جمع اسمك": "Anonymous — your name is not collected",
    "نتيجتك": "Your Result",
    "جاري الحساب…": "Calculating...",
    "الشيء الواحد الذي تفعله الآن": "The ONE thing to do now",
    "انضم لقائمة انتظار حياة ←": "Join HYAT waitlist →",
    "شارك نتيجتي": "Share my result",
    "أعيد الاختبار": "Retake Quiz",
    "لوحة تحكم حياة": "HYAT Dashboard",
    "أدخل الرمز السري للوصول لنتائج المشاركين": "Enter PIN to access results",
    "دخول ←": "Enter →",
    "الرمز الافتراضي: 1234": "Default PIN: 1234",
    "نتائج الجلسة": "Session Results",
    "آخر تحديث: الآن": "Last update: Now",
    "توزيع مستويات البطارية": "Battery Level Distribution",
    "تفصيل الإجابات لكل سؤال": "Answers Breakdown",
    "سجل المشاركين": "Participants Log",
    "إجمالي المشاركين": "Total Participants",
    "متوسط البطارية": "Avg Battery",
    "متوسط النقاط / 18": "Avg Score / 18",
    "الأكثر شيوعاً": "Most Common",
    "تحديث البيانات ↻": "Refresh Data ↻",
    "تصدير CSV": "Export CSV",
    "مسح كل البيانات": "Clear All Data",
    "لا يوجد مشاركون بعد.\nشارك الرابط وانتظر النتائج هنا.": "No participants yet.\nShare the link and wait for results."
  };

  function trDOM(node) {
    if (node.nodeType === 3) {
      let txt = node.nodeValue.trim();
      if (!txt) return;
      if (!node.originalTxt) node.originalTxt = txt;
      
      let baseTxt = node.originalTxt;
      
      // Dynamic replacements
      if (baseTxt.startsWith("سؤال ") && baseTxt.includes(" من ")) {
        if(currentLang === 'en') {
          node.nodeValue = baseTxt.replace("سؤال ", "Question ").replace(" من ", " of ");
        } else {
          node.nodeValue = baseTxt;
        }
        return;
      }

      if (currentLang === 'en' && dict[baseTxt]) {
        node.nodeValue = dict[baseTxt];
      } else if (currentLang === 'ar') {
        node.nodeValue = baseTxt;
      }
    } else {
      if(node.tagName === 'SCRIPT' || node.tagName === 'STYLE') return;
      for (let i = 0; i < node.childNodes.length; i++) {
        trDOM(node.childNodes[i]);
      }
    }
  }

  // Backup original Arrays
  const arQ_texts = Qs.map(q => q.text);
  const arQ_opts = Qs.map(q => [...q.opts]);
  const arP_labels = Profiles.map(p => p.label);
  const arP_titles = Profiles.map(p => p.title);
  const arP_oneThing = Profiles.map(p => p.oneThingTitle);
  const arP_cards = Profiles.map(p => p.cards.map(c => ({...c})));

  function toggleLang(e) {
    if(e) { e.preventDefault(); e.stopPropagation(); }
    currentLang = currentLang === 'ar' ? 'en' : 'ar';
    document.documentElement.lang = currentLang;
    document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
    document.querySelectorAll('.lang-ind').forEach(el => el.textContent = currentLang === 'ar' ? 'EN' : 'عربي');
    
    // Update data objects
    if(currentLang === 'en') {
      Qs.forEach((q, i) => { q.text = enQ_texts[i]; q.opts = [...enQ_opts[i]]; });
      Profiles.forEach((p, i) => { 
        p.label = enP_labels[i]; p.title = enP_titles[i]; p.oneThingTitle = enP_oneThing[i]; 
        p.cards.forEach((c, ci) => { c.h = enP_cards[i][ci].h; c.p = enP_cards[i][ci].p; });
      });
      // specific fixes for tags
      document.querySelector('.landing-tag').innerHTML = '<span class="tag-dot"></span> World Health Day · Apr 7';
      document.querySelector('.landing-h1').innerHTML = 'What is your<br><em>body battery?</em>';
      document.querySelector('.admin-title').innerHTML = 'Session <em>Results</em>';
    } else {
      Qs.forEach((q, i) => { q.text = arQ_texts[i]; q.opts = [...arQ_opts[i]]; });
      Profiles.forEach((p, i) => { 
        p.label = arP_labels[i]; p.title = arP_titles[i]; p.oneThingTitle = arP_oneThing[i]; 
        p.cards.forEach((c, ci) => { c.h = arP_cards[i][ci].h; c.p = arP_cards[i][ci].p; });
      });
      // specific fixes for tags
      document.querySelector('.landing-tag').innerHTML = '<span class="tag-dot"></span> اليوم العالمي للصحة · 7 أبريل';
      document.querySelector('.landing-h1').innerHTML = 'ما هي<br><em>بطارية جسمك؟</em>';
      document.querySelector('.admin-title').innerHTML = 'نتائج <em>الجلسة</em>';
    }

    trDOM(document.body);
    
    // Refresh current view
    if(document.getElementById('page-quiz').classList.contains('active')) renderQ();
    if(document.getElementById('page-admin').classList.contains('active')) refreshDash();
    if(document.getElementById('page-results').classList.contains('active')) showResults(); // will force recalculate and redraw with correct language
  }
</script>
</body>
'''
html = html.replace('</body>', i18n_script)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
print("Patch applied successfully.")
