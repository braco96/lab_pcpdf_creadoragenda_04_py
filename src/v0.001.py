#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a daily agenda PDF from 'today' until Dec 31 of the current year.
- One page per day.
- Big centered header at the top: 'Jueves 28 Agosto 2025' (Spanish).
- Math-style grid background (light gray).
- Top margin to keep the grid from crossing the header.

Author: braco96
License: MIT
"""

from __future__ import annotations

import os
from datetime import datetime, date, timedelta
from typing import Optional

# PDF generation
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Timezone (Python 3.9+). Falls back to local date if zoneinfo is not available.
try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None  # type: ignore


# ------------------------------ Configuration ---------------------------------

SPANISH_WEEKDAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
SPANISH_MONTHS = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

FALLBACK_FONT = "Helvetica"
FONT_CANDIDATES = [
    ("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ("FreeSans",  "/usr/share/fonts/truetype/freefont/FreeSans.ttf"),
    ("Arial",     "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"),
    ("Arial",     "Arial.ttf"),
]


# ------------------------------- Font Handling --------------------------------

def register_readable_font() -> str:
    """Try to register a Unicode-capable font (accents support)."""
    for name, path in FONT_CANDIDATES:
        try:
            if os.path.exists(path):
                pdfmetrics.registerFont(TTFont(name, path))
                return name
        except Exception:
            continue
    return FALLBACK_FONT


# ------------------------------ Date Utilities --------------------------------

def today_europe_paris() -> date:
    """Get today's date in the Europe/Paris timezone."""
    if ZoneInfo is not None:
        tz = ZoneInfo("Europe/Paris")
        return datetime.now(tz).date()
    return date.today()


def end_of_year(d: date) -> date:
    """Return Dec 31 for the given date's year."""
    return date(d.year, 12, 31)


def format_date_spanish(d: date) -> str:
    """Format date as 'Jueves 28 Agosto 2025' in Spanish."""
    weekday = SPANISH_WEEKDAYS[d.weekday()]
    month = SPANISH_MONTHS[d.month - 1]
    return f"{weekday} {d.day} {month} {d.year}"


# ------------------------------- PDF Drawing ----------------------------------

def draw_grid(cnv: canvas.Canvas, page_w: float, page_h: float, spacing: int = 20, top_margin: int = 100) -> None:
    """Draw math-style light gray grid, leaving margin for the header."""
    cnv.setLineWidth(0.2)
    cnv.setStrokeColorRGB(0.85, 0.85, 0.85)

    # Vertical lines
    x = 0
    while x <= page_w:
        cnv.line(x, 0, x, page_h)
        x += spacing

    # Horizontal lines (stop before header)
    y = 0
    stop_y = page_h - top_margin
    while y <= stop_y:
        cnv.line(0, y, page_w, y)
        y += spacing


def draw_centered_text_top(cnv: canvas.Canvas, text: str, page_w: float, page_h: float,
                           font_name: str, font_size: int, top_offset: int = 70) -> None:
    """Draw centered header text."""
    cnv.setFont(font_name, font_size)
    text_w = cnv.stringWidth(text, font_name, font_size)
    cnv.drawString((page_w - text_w) / 2.0, page_h - top_offset, text)


def draw_page_number(cnv: canvas.Canvas, page_w: float, font_name: str, number: int,
                     font_size: int = 10, bottom_margin: int = 20) -> None:
    """Draw centered page number."""
    label = f"{number}"
    cnv.setFont(font_name, font_size)
    text_w = cnv.stringWidth(label, font_name, font_size)
    cnv.drawString((page_w - text_w) / 2.0, bottom_margin, label)


# --------------------------------- Pipeline -----------------------------------

def build_agenda_pdf(output_path: str,
                     start_date: Optional[date] = None,
                     spacing: int = 20,
                     header_font_size: int = 40,
                     include_page_numbers: bool = True,
                     top_margin: int = 100) -> None:
    """Create the agenda PDF."""
    start = start_date or today_europe_paris()
    end = end_of_year(start)

    font_name = register_readable_font()
    cnv = canvas.Canvas(output_path, pagesize=A4)
    page_w, page_h = A4

    page_num = 1
    current = start
    while current <= end:
        draw_grid(cnv, page_w, page_h, spacing=spacing, top_margin=top_margin)

        header_text = format_date_spanish(current)
        draw_centered_text_top(cnv, header_text, page_w, page_h,
                               font_name=font_name, font_size=header_font_size,
                               top_offset=top_margin - 30)

        if include_page_numbers:
            draw_page_number(cnv, page_w, font_name, page_num)

        cnv.showPage()
        page_num += 1
        current += timedelta(days=1)

    cnv.save()
    print(f"[DONE] Agenda saved to {output_path}")


# ------------------------------------ MAIN ------------------------------------

if __name__ == "__main__":
    # Run directly with default settings
    build_agenda_pdf(
        output_path="Agenda_2025.pdf",   # default output
        start_date=None,                 # defaults to 'today'
        spacing=20,                      # grid spacing
        header_font_size=40,             # title size
        include_page_numbers=True,       # add page numbers
        top_margin=100                   # margin for header
    )
