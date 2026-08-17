#!/usr/bin/env python3
"""
VENETA — guide diagrams (MASTER_PLAN §11.1, "Guides / diagrams", 6 @ 4:3).

Hand-built SVG rather than generated raster, because every one of these
diagrams needs legible lettering and dimension arithmetic, and §11.2 forbids
legible text in generated imagery. SVG also costs ~3 KB against the §14
image budget instead of ~120 KB, and stays sharp at any zoom.

Palette and faces are read from build/tokens.css by eye and hard-coded here as
literals, because an external <style> cannot follow an <img src="*.svg">.

Run: python3 build/diagrams.py
Writes: assets/img/diagram-*.svg
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D  # noqa: E402  -- MOUNT_DEPTH is declared once, in data.py

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")

W, H = 1400, 1050  # 4:3 per §11.1

CANVAS = "#F6F2EC"
SURFACE = "#FCFAF6"
SINK = "#EDE7DD"
LINE = "#DCD5C9"
INK = "#211C16"
INK70 = "#55503F"
INK45 = "#8A8371"
CLAY = "#8C5A38"
CLAY_SOFT = "#D8C0AC"
GLASS = "#E4EAE6"
SANS = "'Inter Tight','Inter',system-ui,sans-serif"


def head(title, desc):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">{title}</title><desc id="d">{desc}</desc>
<defs>
  <marker id="a" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
    <path d="M1 1 L11 6 L1 11 z" fill="{CLAY}"/>
  </marker>
  <marker id="ai" viewBox="0 0 12 12" refX="2" refY="6" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
    <path d="M11 1 L1 6 L11 11 z" fill="{CLAY}"/>
  </marker>
</defs>
<rect width="{W}" height="{H}" fill="{CANVAS}"/>"""


TAIL = "</svg>"


def label(x, y, s, size=31, fill=INK, weight=500, anchor="start", ls=0):
    return (f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{ls}">{s}</text>')


def eyebrow(s):
    return label(70, 92, s.upper(), size=25, fill=INK45, weight=600, ls=3.4)


def title(s):
    return label(70, 158, s, size=48, fill=INK, weight=600)


def dim(x1, y1, x2, y2, text, side="above", gap=16):
    """Clay dimension line with arrowheads at both ends and a centred label."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if side == "above":
        tx, ty, anchor = mx, my - gap, "middle"
    elif side == "below":
        tx, ty, anchor = mx, my + gap + 22, "middle"
    elif side == "left":
        tx, ty, anchor = mx - gap, my + 8, "end"
    else:
        tx, ty, anchor = mx + gap, my + 8, "start"
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CLAY}" '
            f'stroke-width="2.5" marker-start="url(#ai)" marker-end="url(#a)"/>'
            + label(tx, ty, text, size=30, fill=CLAY, weight=600, anchor=anchor))


def tick(x, y, vertical=False, length=26):
    if vertical:
        return (f'<line x1="{x - length/2}" y1="{y}" x2="{x + length/2}" y2="{y}" '
                f'stroke="{CLAY}" stroke-width="2"/>')
    return (f'<line x1="{x}" y1="{y - length/2}" x2="{x}" y2="{y + length/2}" '
            f'stroke="{CLAY}" stroke-width="2"/>')


def note(x, y, lines, size=29):
    out = ""
    for i, ln in enumerate(lines):
        out += label(x, y + i * 44, ln, size=size, fill=INK70, weight=400)
    return out


def rule(y, x1=70, x2=W - 70):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{LINE}" stroke-width="2"/>'


# --------------------------------------------------------------------------
# 1. Inside mount
# --------------------------------------------------------------------------
def inside_mount():
    s = head("Inside mount cross-section",
             "Cut-away view of a window opening with the shade headrail fitted "
             "inside the recess, dimensioned across the opening width and down "
             "the opening height.")
    s += eyebrow("Mount type 01") + title("Inside mount")
    # wall block
    ox, oy, ow, oh = 320, 280, 420, 540
    jamb = 62
    s += f'<rect x="{ox-jamb}" y="{oy-jamb}" width="{ow+jamb*2}" height="{oh+jamb*2}" fill="{SINK}" stroke="{LINE}" stroke-width="2"/>'
    s += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="{GLASS}" stroke="{INK45}" stroke-width="2"/>'
    # sash bar
    s += f'<line x1="{ox}" y1="{oy+oh/2}" x2="{ox+ow}" y2="{oy+oh/2}" stroke="{INK45}" stroke-width="6"/>'
    # headrail seated inside the opening
    s += f'<rect x="{ox+8}" y="{oy+8}" width="{ow-16}" height="52" fill="{INK}" rx="3"/>'
    # fabric, three-quarters down
    s += f'<rect x="{ox+16}" y="{oy+60}" width="{ow-32}" height="{oh*0.62}" fill="{CLAY_SOFT}" opacity=".92"/>'
    for i in range(1, 13):
        yy = oy + 60 + (oh * 0.62) * i / 13
        s += f'<line x1="{ox+16}" y1="{yy:.0f}" x2="{ox+ow-16}" y2="{yy:.0f}" stroke="{SURFACE}" stroke-width="1.5" opacity=".65"/>'
    s += f'<rect x="{ox+16}" y="{oy+60+oh*0.62:.0f}" width="{ow-32}" height="16" fill="{INK70}"/>'
    # width dimension inside the opening
    s += dim(ox, oy - 34, ox + ow, oy - 34, 'opening width', side="above")
    s += tick(ox, oy - 34) + tick(ox + ow, oy - 34)
    # depth callout
    s += dim(ox - 34, oy, ox - 34, oy + oh, 'opening height', side="left")
    s += tick(ox - 34, oy, vertical=True) + tick(ox - 34, oy + oh, vertical=True)
    s += rule(940)
    s += label(830, 320, 'Shade sits fully', size=28, weight=600)
    s += note(830, 366, ['inside the recess.',
                         'Order the exact',
                         'opening size, to the',
                         'nearest 1/8". The',
                         'factory takes the',
                         'deduction, not you.'])
    s += label(70, 990, 'Never subtract from an inside-mount width yourself.', size=29, fill=INK70)
    return s + TAIL


# --------------------------------------------------------------------------
# 2. Outside mount
# --------------------------------------------------------------------------
def outside_mount():
    s = head("Outside mount cross-section",
             "Front view of a window with the shade mounted on the wall above "
             "and beyond the opening, showing two inches of overlap on each "
             "side and three inches above the opening.")
    s += eyebrow("Mount type 02") + title("Outside mount")
    ox, oy, ow, oh = 320, 360, 400, 420
    jamb = 54
    s += f'<rect x="60" y="220" width="700" height="680" fill="{SINK}" opacity=".55"/>'
    s += f'<rect x="{ox-jamb}" y="{oy-jamb}" width="{ow+jamb*2}" height="{oh+jamb*2}" fill="{SINK}" stroke="{LINE}" stroke-width="2"/>'
    s += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="{GLASS}" stroke="{INK45}" stroke-width="2"/>'
    s += f'<line x1="{ox}" y1="{oy+oh/2}" x2="{ox+ow}" y2="{oy+oh/2}" stroke="{INK45}" stroke-width="6"/>'
    # shade overhanging the opening
    sx, sy = ox - 76, oy - 116
    sw = ow + 152
    s += f'<rect x="{sx}" y="{sy}" width="{sw}" height="54" fill="{INK}" rx="3"/>'
    s += f'<rect x="{sx+10}" y="{sy+54}" width="{sw-20}" height="250" fill="{CLAY_SOFT}" opacity=".9"/>'
    for i in range(1, 8):
        yy = sy + 54 + 250 * i / 8
        s += f'<line x1="{sx+10}" y1="{yy:.0f}" x2="{sx+sw-10}" y2="{yy:.0f}" stroke="{SURFACE}" stroke-width="1.5" opacity=".6"/>'
    s += f'<rect x="{sx+10}" y="{sy+304}" width="{sw-20}" height="16" fill="{INK70}"/>'
    # overlap dims
    s += f'<line x1="{ox}" y1="{oy-150}" x2="{ox}" y2="{oy+oh}" stroke="{INK45}" stroke-width="1.5" stroke-dasharray="6 8"/>'
    s += f'<line x1="{ox+ow}" y1="{oy-150}" x2="{ox+ow}" y2="{oy+oh}" stroke="{INK45}" stroke-width="1.5" stroke-dasharray="6 8"/>'
    s += dim(sx, oy + oh + 96, ox, oy + oh + 96, '2"', side="below")
    s += dim(ox + ow, oy + oh + 96, sx + sw, oy + oh + 96, '2"', side="below")
    s += dim(sx - 54, sy, sx - 54, oy, '3" above', side="left")
    s += rule(940)
    s += label(70, 990, 'Add 4" to width and 3" to height, then centre the brackets on the opening.', size=29, fill=INK70)
    s += label(840, 320, 'Use it when', size=28, weight=600)
    s += note(840, 366, ['depth is under 3/4",',
                          'the opening is out',
                          'of square by more',
                          'than 1/2", or you',
                          'want a taller,',
                          'softer window line.'])
    return s + TAIL


# --------------------------------------------------------------------------
# 3. Measure width in three places
# --------------------------------------------------------------------------
def measure_width():
    s = head("Measuring width in three places",
             "A window opening with three horizontal measurements taken at the "
             "top, middle and sill, and a note that the narrowest of the three "
             "is the one to record.")
    s += eyebrow("Step 02") + title("Width, three places")
    ox, oy, ow, oh = 250, 290, 440, 510
    jamb = 58
    s += f'<rect x="{ox-jamb}" y="{oy-jamb}" width="{ow+jamb*2}" height="{oh+jamb*2}" fill="{SINK}" stroke="{LINE}" stroke-width="2"/>'
    s += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="{GLASS}" stroke="{INK45}" stroke-width="2"/>'
    s += f'<line x1="{ox}" y1="{oy+oh/2}" x2="{ox+ow}" y2="{oy+oh/2}" stroke="{INK45}" stroke-width="6"/>'
    rows = [(oy + 52, '36 1/4"', False), (oy + oh / 2 - 46, '36 1/8"', False), (oy + oh - 56, '36"', True)]
    for yy, txt, narrow in rows:
        inset = 0 if not narrow else 14
        s += dim(ox + inset, yy, ox + ow - inset, yy, txt, side="above")
        s += tick(ox + inset, yy) + tick(ox + ow - inset, yy)
        if narrow:
            s += f'<circle cx="{ox+ow/2}" cy="{yy}" r="0" fill="none"/>'
            s += label(ox + ow / 2, yy + 54, 'narrowest — record this', size=28, fill=CLAY, weight=600, anchor="middle")
    s += label(ox - jamb - 16, oy + 60, 'top', size=28, fill=INK45, anchor="end")
    s += label(ox - jamb - 16, oy + oh / 2 - 38, 'middle', size=28, fill=INK45, anchor="end")
    s += label(ox - jamb - 16, oy + oh - 48, 'sill', size=28, fill=INK45, anchor="end")
    s += rule(940)
    s += label(70, 990, 'Steel tape only. Record to the nearest 1/8". Never round the width up.', size=29, fill=INK70)
    s += label(830, 320, 'Out of square?', size=28, weight=600)
    s += note(830, 366, ['If the three widths',
                          'differ by more than',
                          '1/2", switch to an',
                          'outside mount.'])
    return s + TAIL


# --------------------------------------------------------------------------
# 4. Measure height in three places
# --------------------------------------------------------------------------
def measure_height():
    s = head("Measuring height in three places",
             "A window opening with three vertical measurements taken at the "
             "left, centre and right, and a note that the longest of the three "
             "is the one to record.")
    s += eyebrow("Step 03") + title("Height, three places")
    ox, oy, ow, oh = 240, 300, 420, 450
    jamb = 56
    s += f'<rect x="{ox-jamb}" y="{oy-jamb}" width="{ow+jamb*2}" height="{oh+jamb*2}" fill="{SINK}" stroke="{LINE}" stroke-width="2"/>'
    s += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="{GLASS}" stroke="{INK45}" stroke-width="2"/>'
    s += f'<line x1="{ox}" y1="{oy+oh/2}" x2="{ox+ow}" y2="{oy+oh/2}" stroke="{INK45}" stroke-width="6"/>'
    cols = [(ox + 58, '48"', 'left', False), (ox + ow / 2, '48 1/8"', 'centre', False), (ox + ow - 58, '48 1/4"', 'right', True)]
    for xx, txt, name, longest in cols:
        s += (f'<line x1="{xx}" y1="{oy+10}" x2="{xx}" y2="{oy+oh-10}" stroke="{CLAY}" '
              f'stroke-width="2.5" marker-start="url(#ai)" marker-end="url(#a)"/>')
        s += tick(xx, oy + 10, vertical=True) + tick(xx, oy + oh - 10, vertical=True)
        s += label(xx, oy - jamb - 22, txt, size=29, fill=CLAY, weight=600, anchor="middle")
        s += label(xx, oy + oh + jamb + 44, name, size=28, fill=INK45, anchor="middle")
        if longest:
            s += label(xx, oy + oh + jamb + 82, 'longest', size=28, fill=CLAY, weight=600, anchor="middle")
    s += rule(940)
    s += label(70, 990, 'Measure from the top of the opening to the sill. Never round the height down.', size=29, fill=INK70)
    s += label(830, 320, 'Longest wins', size=28, weight=600)
    s += note(830, 366, ['Record the longest',
                         'of the three. On a',
                         'sloped sill, measure',
                         'to the highest point',
                         'of the slope.'])
    return s + TAIL


# --------------------------------------------------------------------------
# 5. Depth and clearance
# --------------------------------------------------------------------------
def depth_clearance():
    s = head("Window depth and headrail clearance",
             "Plan-view cut-away through a window jamb showing the flat depth "
             "available in front of the glass, the headrail sitting within it, "
             "and the flush-mount threshold.")
    s += eyebrow("Before you choose") + title("Depth and clearance")
    # plan view: wall in section, glass at back
    wx, wy, wh = 260, 300, 300
    s += f'<rect x="{wx}" y="{wy}" width="820" height="{wh}" fill="{SINK}" stroke="{LINE}" stroke-width="2"/>'
    # glass plane at the back of the recess
    s += f'<rect x="{wx+40}" y="{wy+40}" width="740" height="26" fill="{GLASS}" stroke="{INK45}" stroke-width="2"/>'
    s += label(wx + 40, wy + 20, 'glass', size=27, fill=INK45)
    # available flat depth
    s += f'<line x1="{wx+40}" y1="{wy+66}" x2="{wx+40}" y2="{wy+wh-40}" stroke="{INK45}" stroke-width="1.5" stroke-dasharray="6 8"/>'
    s += f'<line x1="{wx+780}" y1="{wy+66}" x2="{wx+780}" y2="{wy+wh-40}" stroke="{INK45}" stroke-width="1.5" stroke-dasharray="6 8"/>'
    # headrail in section
    s += dim(wx + 40, wy + 258, wx + 780, wy + 258, 'flat depth available', side="below")
    s += tick(wx + 40, wy + 258) + tick(wx + 780, wy + 258)
    s += f'<rect x="{wx+90}" y="{wy+96}" width="640" height="86" fill="{INK}" rx="4"/>'
    s += label(wx + 110, wy + 150, 'headrail', size=29, fill="#FCFAF6", weight=600)
    s += dim(wx + 90, wy + wh + 60, wx + 730, wy + wh + 60, 'headrail depth', side="below")
    s += tick(wx + 90, wy + wh + 60) + tick(wx + 730, wy + wh + 60)
    s += f'<line x1="{wx+90}" y1="{wy+182}" x2="{wx+90}" y2="{wy+wh+60}" stroke="{INK45}" stroke-width="1.5" stroke-dasharray="6 8"/>'
    s += f'<line x1="{wx+730}" y1="{wy+182}" x2="{wx+730}" y2="{wy+wh+60}" stroke="{INK45}" stroke-width="1.5" stroke-dasharray="6 8"/>'
    s += rule(780)
    yy = 840
    for d, _lbl, t in D.MOUNT_DEPTH:
        s += label(70, yy, d, size=27, fill=CLAY, weight=600)
        s += label(340, yy, t, size=29, fill=INK70)
        yy += 46
    return s + TAIL


# --------------------------------------------------------------------------
# 6. Bracket placement
# --------------------------------------------------------------------------
def bracket_placement():
    s = head("Bracket placement on the headrail",
             "Front view of a headrail showing end brackets set in from each "
             "end and an evenly spaced centre support, with the maximum "
             "unsupported span called out.")
    s += eyebrow("Installation") + title("Bracket placement")
    hx, hy, hw = 150, 380, 1100
    s += f'<rect x="{hx}" y="{hy}" width="{hw}" height="86" fill="{INK}" rx="4"/>'
    s += f'<rect x="{hx+14}" y="{hy+100}" width="{hw-28}" height="150" fill="{CLAY_SOFT}" opacity=".85"/>'
    for i in range(1, 5):
        yy = hy + 100 + 150 * i / 5
        s += f'<line x1="{hx+14}" y1="{yy:.0f}" x2="{hx+hw-14}" y2="{yy:.0f}" stroke="{SURFACE}" stroke-width="1.5" opacity=".6"/>'
    # brackets
    for bx in (hx + 60, hx + hw / 2 - 30, hx + hw - 120):
        s += f'<rect x="{bx}" y="{hy-58}" width="60" height="58" fill="none" stroke="{CLAY}" stroke-width="4"/>'
        s += f'<line x1="{bx+30}" y1="{hy-58}" x2="{bx+30}" y2="{hy+86}" stroke="{CLAY}" stroke-width="2" stroke-dasharray="6 7"/>'
    s += label(hx + 90, hy - 76, 'end', size=27, fill=CLAY, weight=600, anchor="middle")
    s += label(hx + hw / 2, hy - 76, 'centre support', size=27, fill=CLAY, weight=600, anchor="middle")
    s += label(hx + hw - 90, hy - 76, 'end', size=27, fill=CLAY, weight=600, anchor="middle")
    # dims
    s += dim(hx, hy + 300, hx + 90, hy + 300, '2" in', side="below")
    s += dim(hx + 90, hy + 300, hx + hw / 2, hy + 300, 'max 36"', side="below")
    s += dim(hx + hw / 2, hy + 300, hx + hw - 90, hy + 300, 'max 36"', side="below")
    s += dim(hx + hw - 90, hy + 300, hx + hw, hy + 300, '2" in', side="below")
    for xx in (hx, hx + 90, hx + hw / 2, hx + hw - 90, hx + hw):
        s += tick(xx, hy + 300)
    s += rule(800)
    s += label(70, 860, 'Set end brackets 2" in from each end. Add one support for every 36" of span.', size=29, fill=INK70)
    s += label(70, 906, 'Level the brackets to each other, not to the sill: old sills are rarely level.', size=29, fill=INK70)
    s += label(70, 972, 'Pilot-drill hardwood and plaster. Never anchor a headrail into drywall alone.', size=29, fill=INK70)
    return s + TAIL


DIAGRAMS = {
    "diagram-inside-mount": inside_mount,
    "diagram-outside-mount": outside_mount,
    "diagram-measure-width": measure_width,
    "diagram-measure-height": measure_height,
    "diagram-depth-clearance": depth_clearance,
    "diagram-bracket-placement": bracket_placement,
}

# alt text, consumed by build/pic.py so the pages and the diagrams cannot drift
ALT = {
    "diagram-inside-mount": "Diagram of an inside mount: the headrail sits inside the window recess, with the opening measured across its width and down its height.",
    "diagram-outside-mount": "Diagram of an outside mount: the shade is fixed to the wall with two inches of overlap each side and three inches above the opening.",
    "diagram-measure-width": "Diagram of a window with the width measured at the top, middle and sill, with the narrowest measurement marked as the one to record.",
    "diagram-measure-height": "Diagram of a window with the height measured at the left, centre and right, with the longest measurement marked as the one to record.",
    "diagram-depth-clearance": "Plan-view diagram of a window jamb showing the flat depth available in front of the glass and the headrail depth that has to fit inside it.",
    "diagram-bracket-placement": "Diagram of a headrail with end brackets set two inches in from each end and a centre support, with a maximum unsupported span of thirty-six inches.",
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        path = os.path.join(OUT, name + ".svg")
        svg = fn()
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"{name}.svg  {len(svg.encode('utf-8'))/1024:.1f} KB")


if __name__ == "__main__":
    main()
