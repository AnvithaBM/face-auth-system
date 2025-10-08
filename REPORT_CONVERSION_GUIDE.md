# Project Report Conversion Guide

This guide explains how to convert the `PROJECT_REPORT.md` Markdown file to PDF format.

## Report Details

- **File:** PROJECT_REPORT.md
- **Size:** 4,315 lines
- **Estimated PDF Pages:** 70-75 pages
- **Format:** Markdown with LaTeX page breaks

## Conversion Methods

### Method 1: Using Pandoc (Recommended)

Pandoc is a universal document converter that produces high-quality PDFs.

#### Installation

**On macOS:**
```bash
brew install pandoc
brew install basictex  # For LaTeX support
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install pandoc
sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

**On Windows:**
- Download from: https://pandoc.org/installing.html
- Install MiKTeX: https://miktex.org/download

#### Conversion Command

**Basic Conversion:**
```bash
pandoc PROJECT_REPORT.md -o PROJECT_REPORT.pdf
```

**Advanced Conversion with Table of Contents:**
```bash
pandoc PROJECT_REPORT.md -o PROJECT_REPORT.pdf \
  --toc \
  --toc-depth=3 \
  --number-sections \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=report
```

**With Custom Styling:**
```bash
pandoc PROJECT_REPORT.md -o PROJECT_REPORT.pdf \
  --toc \
  --toc-depth=3 \
  --number-sections \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=report \
  -V colorlinks=true \
  -V linkcolor=blue \
  -V urlcolor=blue \
  --highlight-style=tango
```

### Method 2: Using VS Code

If you use Visual Studio Code:

1. Install the "Markdown PDF" extension
2. Open `PROJECT_REPORT.md`
3. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
4. Type "Markdown PDF: Export (pdf)"
5. Select PDF option

### Method 3: Using Typora

Typora is a WYSIWYG Markdown editor:

1. Download Typora from: https://typora.io/
2. Open `PROJECT_REPORT.md` in Typora
3. Go to File → Export → PDF
4. Configure settings:
   - Enable table of contents
   - Set margins to 1 inch
   - Choose font size 11pt
5. Click Export

### Method 4: Online Converters

Several online tools can convert Markdown to PDF:

**Recommended Online Tools:**

1. **Markdown to PDF** (https://www.markdowntopdf.com/)
   - Upload PROJECT_REPORT.md
   - Click Convert
   - Download PDF

2. **CloudConvert** (https://cloudconvert.com/md-to-pdf)
   - Upload file
   - Configure options
   - Convert and download

3. **Dillinger** (https://dillinger.io/)
   - Import PROJECT_REPORT.md
   - Export to PDF

**Note:** Online converters may have file size limits and might not handle all LaTeX commands.

### Method 5: Using Python (Advanced)

If you have Python with `markdown` and `pdfkit`:

```bash
pip install markdown pdfkit
```

Then create a conversion script:

```python
import markdown
import pdfkit

# Read markdown file
with open('PROJECT_REPORT.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert markdown to HTML
html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite', 'toc'])

# Add CSS styling
styled_html = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 1in; }}
        h1 {{ color: #333; page-break-before: always; }}
        code {{ background: #f4f4f4; padding: 2px 5px; }}
        pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

# Convert HTML to PDF
pdfkit.from_string(styled_html, 'PROJECT_REPORT.pdf')
```

## Report Structure

The report contains the following sections:

1. **Cover Page** - Title, author, institution, date
2. **Abstract** - Project summary (1 page)
3. **Acknowledgments** - Contributors and thanks (1-2 pages)
4. **Table of Contents** - Auto-generated (2-3 pages)
5. **Introduction** - Background and objectives (4 pages)
6. **Literature Review** - Face recognition technologies, hyperspectral data, CNNs (5 pages)
7. **System Analysis** - Problem definition, requirements, feasibility (5 pages)
8. **Design and Methodology** - Architecture, algorithms, database (8 pages)
9. **Implementation Details** - Code, technologies, deployment (12 pages)
10. **Results and Evaluation** - Testing, metrics, user feedback (8 pages)
11. **Conclusion** - Summary, limitations, future work (7 pages)
12. **References** - 40 IEEE-formatted citations (2 pages)
13. **Appendices** - Code listings, screenshots, diagrams (10 pages)

## Formatting Tips

### For Best PDF Output:

1. **Use Pandoc with LaTeX** for professional formatting
2. **Enable Table of Contents** for easy navigation
3. **Set appropriate margins** (1 inch recommended)
4. **Use 11pt or 12pt font** for readability
5. **Enable syntax highlighting** for code blocks
6. **Add page numbers** in footer

### Pandoc Template (Complete Example)

```bash
pandoc PROJECT_REPORT.md -o PROJECT_REPORT.pdf \
  --from markdown \
  --template eisvogel \
  --listings \
  --toc \
  --toc-depth=3 \
  --number-sections \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=report \
  -V colorlinks=true \
  -V linkcolor=blue \
  -V urlcolor=blue \
  -V toccolor=black \
  --highlight-style=tango \
  --pdf-engine=xelatex
```

**Note:** The `eisvogel` template provides beautiful formatting. Install it:
```bash
# Download template
wget https://raw.githubusercontent.com/Wandmalfarbe/pandoc-latex-template/master/eisvogel.tex

# Move to pandoc templates directory
mkdir -p ~/.pandoc/templates
mv eisvogel.tex ~/.pandoc/templates/
```

## Troubleshooting

### Common Issues:

**Issue: LaTeX not found**
- Solution: Install TeX distribution (MiKTeX, MacTeX, or TeX Live)

**Issue: Unicode errors**
- Solution: Use `--pdf-engine=xelatex` instead of default pdflatex

**Issue: Images not rendering**
- Solution: Ensure image paths are correct and accessible

**Issue: Code blocks not formatted**
- Solution: Use `--highlight-style=tango` or another style

**Issue: Table of contents not generating**
- Solution: Ensure `--toc` flag is used and headers are properly formatted

## Verification

After conversion, verify:

- [ ] All sections are present
- [ ] Table of contents is complete and clickable
- [ ] Code blocks are properly formatted
- [ ] Page numbers are present
- [ ] Images and diagrams are visible
- [ ] References are formatted correctly
- [ ] Total pages are between 50-75

## Academic Submission

For academic submission, ensure:

1. **Cover page** includes all required information
2. **Page numbers** start from introduction (not cover/TOC)
3. **Headers/Footers** contain chapter names
4. **Font** is Times New Roman or Arial (11-12pt)
5. **Line spacing** is 1.5 or double
6. **Margins** are 1 inch all around
7. **References** follow IEEE citation format

## Contact

For issues with the report content or structure, please refer to the project documentation or open an issue on the GitHub repository.

---

**Report Version:** 1.0  
**Last Updated:** January 2024  
**Maintained by:** Anvitha B M
