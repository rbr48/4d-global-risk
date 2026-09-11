"""
4D-MGRFF Dissertation Monograph Export Engine
Compiles thesis/DISSERTATION_MASTER_MANUSCRIPT.md into:
1. An interactive academic HTML monograph with MathJax 3 rendering.
2. A publication-grade PDF monograph using headless Microsoft Edge.
"""

import os
import re
import subprocess
import sys
from pathlib import Path
import markdown


ROOT_DIR = Path(__file__).resolve().parent.parent
THESIS_DIR = ROOT_DIR / "thesis"
RESULTS_DIR = ROOT_DIR / "results"
MANUSCRIPT_MD = THESIS_DIR / "DISSERTATION_MASTER_MANUSCRIPT.md"
OUTPUT_HTML = THESIS_DIR / "DISSERTATION_MONOGRAPH.html"
OUTPUT_PDF = THESIS_DIR / "DISSERTATION_MONOGRAPH.pdf"

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]


CSS_STYLES = """
:root {
  --primary-color: #1a2a3a;
  --text-color: #2b2b2b;
  --bg-color: #ffffff;
  --accent-color: #0d47a1;
  --border-color: #d1d5db;
  --table-header-bg: #f3f4f6;
  --code-bg: #f8fafc;
  --font-serif: 'Crimson Pro', 'Georgia', 'Cambria', serif;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
}

@page {
  size: letter;
  margin: 1in 0.85in 1in 0.85in;
  @bottom-right {
    content: counter(page);
    font-family: var(--font-sans);
    font-size: 9pt;
    color: #6b7280;
  }
}

body {
  font-family: var(--font-serif);
  font-size: 11pt;
  line-height: 1.65;
  color: var(--text-color);
  background: var(--bg-color);
  max-width: 860px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-sans);
  color: var(--primary-color);
  font-weight: 700;
  line-height: 1.25;
  page-break-after: avoid;
}

h1 {
  font-size: 24pt;
  border-bottom: 2px solid var(--accent-color);
  padding-bottom: 0.35rem;
  margin-top: 3rem;
  margin-bottom: 1.5rem;
}

h2 {
  font-size: 16pt;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.25rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

h3 {
  font-size: 13pt;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

h4 {
  font-size: 11pt;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #4b5563;
}

p {
  margin: 0.85rem 0;
  text-align: justify;
}

/* Callout / Quotes */
blockquote {
  border-left: 4px solid var(--accent-color);
  background: #f0f4f8;
  padding: 0.8rem 1.2rem;
  margin: 1.2rem 0;
  font-style: normal;
  border-radius: 0 6px 6px 0;
}

blockquote p {
  margin: 0.4rem 0;
}

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  font-family: var(--font-sans);
  font-size: 9.5pt;
  line-height: 1.45;
  page-break-inside: avoid;
}

th, td {
  padding: 8px 10px;
  border: 1px solid var(--border-color);
  text-align: left;
}

th {
  background-color: var(--table-header-bg);
  font-weight: 600;
  color: var(--primary-color);
}

tr:nth-child(even) td {
  background-color: #fafbfc;
}

/* Code & Preformatted */
code {
  font-family: var(--font-mono);
  font-size: 9pt;
  background: var(--code-bg);
  padding: 0.15rem 0.35rem;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
}

pre {
  background: var(--code-bg);
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 1rem;
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: 8.5pt;
  line-height: 1.4;
  page-break-inside: avoid;
}

pre code {
  background: transparent;
  padding: 0;
  border: none;
}

/* Embedded Figures */
figure {
  margin: 2rem auto;
  text-align: center;
  page-break-inside: avoid;
}

figure img {
  max-width: 95%;
  height: auto;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

figcaption {
  font-family: var(--font-sans);
  font-size: 9pt;
  color: #4b5563;
  margin-top: 0.6rem;
  font-style: italic;
}

/* Cover / Header section */
.monograph-cover {
  text-align: center;
  padding: 4rem 1rem 3rem 1rem;
  border-bottom: 3px double var(--accent-color);
  margin-bottom: 3rem;
  page-break-after: always;
}

.monograph-cover h1 {
  border: none;
  font-size: 28pt;
  margin-bottom: 1rem;
}

.monograph-cover .subtitle {
  font-family: var(--font-sans);
  font-size: 14pt;
  color: #4b5563;
  margin-bottom: 2rem;
}

.monograph-cover .meta {
  font-family: var(--font-sans);
  font-size: 11pt;
  color: #1f2937;
  line-height: 1.8;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  font-family: var(--font-sans);
  font-size: 8.5pt;
  font-weight: 600;
  border-radius: 9999px;
  background: #e0e7ff;
  color: #3730a3;
  margin-bottom: 1rem;
}

/* Horizontal Rules */
hr {
  border: 0;
  height: 1px;
  background: #e5e7eb;
  margin: 2.5rem 0;
}

/* Print optimizations */
@media print {
  body {
    max-width: 100%;
    padding: 0;
    font-size: 10pt;
  }
  h1 {
    page-break-before: always;
  }
  .monograph-cover h1 {
    page-break-before: avoid;
  }
}
"""


def protect_math_blocks(md_text: str):
    """
    Extracts $$...$$ and $...$ math blocks, replacing them with safe unique tokens
    so markdown parsing does not mangle subscripts, asterisks, or underscores.
    """
    display_blocks = []
    inline_blocks = []

    def disp_repl(match):
        idx = len(display_blocks)
        display_blocks.append(match.group(0))
        return f"%%MATH_DISP_{idx}%%"

    def inl_repl(match):
        idx = len(inline_blocks)
        inline_blocks.append(match.group(0))
        return f"%%MATH_INL_{idx}%%"

    # Display math: $$...$$
    protected = re.sub(r"\$\$(.*?)\$\$", disp_repl, md_text, flags=re.DOTALL)

    # Inline math: $...$ (avoiding double dollars)
    protected = re.sub(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", inl_repl, protected)

    return protected, display_blocks, inline_blocks


def restore_math_blocks(html_text: str, display_blocks, inline_blocks):
    """Restores the preserved math expressions into the generated HTML."""
    for idx, block in enumerate(display_blocks):
        html_text = html_text.replace(f"%%MATH_DISP_{idx}%%", block)
    for idx, block in enumerate(inline_blocks):
        html_text = html_text.replace(f"%%MATH_INL_{idx}%%", block)
    return html_text


def embed_visual_figures(html_text: str) -> str:
    """
    Converts '(See results/figures/figure_*.png)' lines into full HTML figure elements.
    """
    pattern = re.compile(r"\(See\s+(results/figures/([^\)]+\.png))\)")

    def fig_repl(match):
        rel_path = match.group(1)
        filename = match.group(2)
        clean_title = filename.replace(".png", "").replace("_", " ").title()
        
        # Absolute path for headless browser rendering
        abs_path = (ROOT_DIR / rel_path).resolve().as_uri()
        return (
            f'<figure>'
            f'<img src="{abs_path}" alt="{clean_title}" />'
            f'<figcaption>Figure: {clean_title} (Source: {rel_path})</figcaption>'
            f'</figure>'
        )

    return pattern.sub(fig_repl, html_text)


def compile_html():
    """Compiles markdown manuscript into standalone HTML monograph."""
    if not MANUSCRIPT_MD.exists():
        raise FileNotFoundError(f"Manuscript not found at: {MANUSCRIPT_MD}")

    with open(MANUSCRIPT_MD, "r", encoding="utf-8") as f:
        content = f.read()

    # Protect math expressions before markdown parsing
    protected_md, disp_math, inl_math = protect_math_blocks(content)

    # Parse markdown with tables and code extensions
    body_html = markdown.markdown(
        protected_md,
        extensions=["tables", "fenced_code", "toc"]
    )

    # Restore math blocks
    body_html = restore_math_blocks(body_html, disp_math, inl_math)

    # Embed visual figures
    body_html = embed_visual_figures(body_html)

    # Assemble complete HTML5 document with MathJax 3
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>4D-MGRFF: Doctoral Dissertation Monograph</title>
  
  <!-- MathJax 3 Configuration -->
  <script>
  window.MathJax = {{
    tex: {{
      inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
      displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
      processEscapes: true
    }},
    options: {{
      skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
    }}
  }};
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

  <style>
  {CSS_STYLES}
  </style>
</head>
<body>

  <div class="monograph-cover">
    <span class="badge">Verified Doctoral Research Monograph</span>
    <h1>Four-Dimensional Probabilistic Framework for Modelling the Evolution, Interaction, and Propagation of Multidisciplinary Global Risks (4D-MGRFF)</h1>
    <div class="subtitle">A Dynamic State-Space and Econometric System for Multi-Horizon Systemic Risk Forecasting</div>
    <div class="meta">
      <strong>Author:</strong> Izhaan Intellect Research<br>
      <strong>Framework Version:</strong> 1.0.0 (Audited & Reconciled)<br>
      <strong>Empirical Baseline:</strong> Federal Reserve Bank of St. Louis (FRED) Panel (43,707 Records)<br>
      <strong>Date of Compilation:</strong> September 2026
    </div>
  </div>

  <div class="monograph-body">
    {body_html}
  </div>

</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"[OK] Generated HTML monograph: {OUTPUT_HTML} ({len(full_html):,} bytes)")
    return OUTPUT_HTML


def compile_pdf():
    """Renders HTML monograph to PDF using headless Edge/Chrome."""
    html_file = compile_html()

    edge_path = None
    for cand in EDGE_CANDIDATES:
        if os.path.exists(cand):
            edge_path = cand
            break

    if not edge_path:
        print("[WARN] No headless browser (Edge/Chrome) found. PDF compilation skipped.")
        print(f"       You can view and print the HTML monograph at: {html_file}")
        return None

    print(f"[INFO] Using headless browser: {edge_path}")
    print(f"[INFO] Rendering PDF (allowing 8s for MathJax equation typesetting)...")

    file_uri = html_file.resolve().as_uri()

    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=8000",
        "--no-pdf-header-footer",
        f"--print-to-pdf={OUTPUT_PDF}",
        file_uri,
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and OUTPUT_PDF.exists() and OUTPUT_PDF.stat().st_size > 1000:
        pdf_size_mb = OUTPUT_PDF.stat().st_size / (1024 * 1024)
        print(f"[SUCCESS] Compiled PDF Monograph: {OUTPUT_PDF} ({pdf_size_mb:.2f} MB)")
        return OUTPUT_PDF
    else:
        print(f"[WARN] Headless PDF export failed or produced empty file: {res.stderr}")
        return None


if __name__ == "__main__":
    compile_pdf()
