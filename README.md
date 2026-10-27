# Sarabo: Final Year Project Documentation

Everything for the final-year-project submission of **Sarabo**, a device-repair service platform for Bangladesh.
Author: Jahid Hasan (222-115-116, Batch 57 C). Supervisor: Shrabanti Chowdhury.

| File | What it is |
|---|---|
| **[Sarabo_Final_Report.pdf](Sarabo_Final_Report.pdf)** | Final report, compiled from `report/` (109 pages, Metropolitan University template; Chapter 7 is a screenshot walkthrough built by `report/make_walkthrough.py`) |
| `report/` | LaTeX source: `myThesis.tex` (main file), `tex/*.tex` (one file per chapter), `ref_file.bib`, `myStyle.sty`, `img/` |
| **[presentation/Sarabo_Presentation.pptx](presentation/Sarabo_Presentation.pptx)** | 16 slides (about 8 minutes) with short points, large text, zoomed screenshots and an ER diagram (slide 5); the speaker script is in each slide's notes |
| [presentation/script-5min.md](presentation/script-5min.md) · **[PDF](presentation/Sarabo_Script_5min.pdf)** | Slide script, exactly 5 minutes, written to be spoken (Rahim's story, timings, cut-if-late lines) |
| [presentation/script-full.md](presentation/script-full.md) · **[PDF](presentation/Sarabo_Script_Full.pdf)** | Long slide script (12-14 min), same slides and story, with bridge lines between slides |
| [presentation/demo-plan-5min.md](presentation/demo-plan-5min.md) · **[PDF](presentation/Sarabo_Demo_Plan_5min.pdf)** | 5-minute live demo plan: setup checklist, workflow diagram, what to click and say, fallbacks, likely questions |
| [presentation/demo-script.md](presentation/demo-script.md) | 5-minute live demo, timed, told as one real-life story (Rahim's cracked phone) |
| [presentation/demo-script-detailed.md](presentation/demo-script-detailed.md) | Longer demo (12-15 min): every role and feature, a fallback plan, and likely questions with short answers |
| **[presentation/Sarabo_Demo_Script.pdf](presentation/Sarabo_Demo_Script.pdf)** | Both demo scripts in one PDF (5-minute and detailed), from `presentation/demo-script.html` |
| **[presentation/Sarabo_Viva_QnA.pdf](presentation/Sarabo_Viva_QnA.pdf)** | Viva practice in Bangla/mixed: quick facts, code map (client file → API → route → controller → service) for every feature, and likely questions on design, gaps, edge cases, security, AI and testing; from `presentation/viva-qna.html` |
| `presentation/build_slides.py`, `make_crops.py` | Rebuild the PPTX: `python make_crops.py` (cuts the slide screenshots from `report/img/screens`), then `python build_slides.py` |
| [01-project-overview.md](01-project-overview.md) | What Sarabo is, its users, features, architecture and tech stack |
| [02-development-history.md](02-development-history.md) | How the project was built, phase by phase |
| [03-work-log.md](03-work-log.md) | Log of every fix and improvement from 11 Oct 2026; feeds Section 5.13 of the report |

## Rebuilding the report PDF

- **Overleaf:** upload the `report/` folder and compile `myThesis.tex` (pdfLaTeX or XeLaTeX, with BibTeX).
- **This PC:** run `tectonic -X compile myThesis.tex` inside `report/`, then copy `myThesis.pdf` to `Sarabo_Final_Report.pdf`.

Values that may change (submission date, test counts, names) are defined once at the top of `report/myThesis.tex`.

When a fix is made: add an entry to `03-work-log.md`, add a row to Table 5.3 in `report/tex/chapter5.tex`, then rebuild.
