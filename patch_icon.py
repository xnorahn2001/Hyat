import re

filepath = '/Users/norahalnaif/Desktop/Hyat/Hyat.html'
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the Lang Toggle injection
old_img = r'<img src="hayat logo -06.png" style="height: 36px; object-fit: contain;" alt="Hyat Logo" />'
lang_btn = r'''<img src="hayat logo -06.png" style="height: 36px; object-fit: contain;" alt="Hyat Logo" />
        <div class="lang-switch" onclick="toggleLang(event)" style="cursor:pointer; display:flex; align-items:center; gap:6px; font-size:12px; font-weight:500; color:rgba(255,255,255,0.7); background:rgba(255,255,255,0.05); padding:6px 12px; border-radius:20px; border:1px solid rgba(255,255,255,0.1); margin-inline-start:12px; transition:0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
          <span class="lang-ind">EN</span>
        </div>'''
html = html.replace(old_img, lang_btn)

# Make sure logo-wrap is flex to keep items inline
wrap_old = r'<div class="logo-wrap" onclick="goTo(\'page-landing\')">'
wrap_new = r'<div class="logo-wrap" onclick="goTo(\'page-landing\')" style="display:flex;align-items:center;">'
html = html.replace(wrap_old, wrap_new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
print("Language switch icon injected.")
