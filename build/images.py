#!/usr/bin/env python3
"""P1 image pipeline. One command per accepted image; no per-batch code writing.

    python3 build/images.py status
    python3 build/images.py next [BATCH]          # prints the pending shots + prompts
    python3 build/images.py add SHOT_ID SRC_PATH  # crop, grade, encode, log, accept
    python3 build/images.py reject SHOT_ID "reason"
    python3 build/images.py og                    # derive the 1200x630 social cards
    python3 build/images.py verify                # budgets + missing files

Processing follows MASTER_PLAN.md §11.6: centre-crop to the shot ratio, downscale
to the final long edge, one shared grade (highlights -8, warmth +3, clarity -5,
grain 8%), export AVIF q55 + WebP q78, enforce the per-set byte budget.
"""
import json, math, os, random, sys

from PIL import Image, ImageEnhance, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "docs", "p1-manifest.json")
STATE = os.path.join(ROOT, "docs", "p1-state.json")
LOG = os.path.join(ROOT, "docs", "image-log.md")
IMGDIR = os.path.join(ROOT, "assets", "img")


def load_manifest():
    with open(MANIFEST) as f:
        return json.load(f)


def load_state():
    if os.path.exists(STATE):
        with open(STATE) as f:
            return json.load(f)
    m = load_manifest()
    return {"shots": {s["id"]: {"status": "pending", "attempts": 0} for s in m["shots"]}}


def save_state(st):
    with open(STATE, "w") as f:
        json.dump(st, f, indent=1, sort_keys=True)


def shot(m, shot_id):
    for s in m["shots"]:
        if s["id"] == shot_id:
            return s
    raise SystemExit(f"unknown shot id: {shot_id}")


# ---------------------------------------------------------------- processing
def centre_crop(im, ratio):
    rw, rh = (int(v) for v in ratio.split(":"))
    w, h = im.size
    target = rw / rh
    if target >= w / h:
        cw, ch = w, round(w / target)
    else:
        ch, cw = h, round(h * target)
    left, top = (w - cw) // 2, (h - ch) // 2
    return im.crop((left, top, left + cw, top + ch))


def grade(im, g):
    """One shared grade across the whole set (§11.6 step 2)."""
    # highlights: soft knee above ~70% luma, pulling the top end down
    pull = abs(g["highlights"]) / 100.0
    knee = 178
    lut = []
    for v in range(256):
        if v <= knee:
            lut.append(v)
        else:
            t = (v - knee) / (255 - knee)
            lut.append(round(knee + (255 - knee) * (t ** (1 + pull * 2))))
    im = im.point(lut * 3)

    # warmth: lift red, ease blue
    w = g["warmth"] / 100.0
    r, gr, b = im.split()
    r = r.point(lambda v: min(255, round(v * (1 + w))))
    b = b.point(lambda v: max(0, round(v * (1 - w))))
    im = Image.merge("RGB", (r, gr, b))

    # clarity negative: very slight softening of local contrast
    soft = im.filter(ImageFilter.GaussianBlur(radius=0.6))
    im = Image.blend(im, soft, abs(g["clarity"]) / 100.0)

    # fine grain, deterministic
    random.seed(1337)
    noise = Image.effect_noise(im.size, 22).convert("L")
    grain = Image.merge("RGB", (noise, noise, noise))
    im = Image.blend(im, grain, g["grain_pct"] / 100.0 * 0.22)
    return ImageEnhance.Contrast(im).enhance(1.02)


def encode(im, s, enc):
    os.makedirs(IMGDIR, exist_ok=True)
    out = {}
    for fmt, key, q in (("AVIF", "avif", enc["avif_q"]), ("WEBP", "webp", enc["webp_q"])):
        path = os.path.join(ROOT, s["files"][key])
        im.save(path, fmt, quality=q, method=6) if fmt == "WEBP" else im.save(path, fmt, quality=q)
        kb = os.path.getsize(path) / 1024
        # step quality down until the budget is met (AVIF budget; WebP allowed +40%)
        limit = s["budget_kb"] * (1.0 if key == "avif" else 1.4)
        while kb > limit and q > 30:
            q -= 6
            if fmt == "WEBP":
                im.save(path, fmt, quality=q, method=6)
            else:
                im.save(path, fmt, quality=q)
            kb = os.path.getsize(path) / 1024
        out[key] = {"path": s["files"][key], "kb": round(kb, 1), "q": q}
    return out


def add(shot_id, src):
    m, st = load_manifest(), load_state()
    s = shot(m, shot_id)
    im = Image.open(src).convert("RGB")
    im = centre_crop(im, s["ratio"])
    im = im.resize((s["width"], s["height"]), Image.LANCZOS)
    im = grade(im, m["grade"])
    files = encode(im, s, m["encode"])
    rec = st["shots"].setdefault(shot_id, {"attempts": 0})
    rec.update(status="accepted", attempts=rec.get("attempts", 0) + 1, files=files,
               width=s["width"], height=s["height"])
    save_state(st)
    log_prompt(s, files)
    over = [f for f in files.values() if f["kb"] > s["budget_kb"] * 1.4]
    print(f"{shot_id}: OK {s['width']}x{s['height']} "
          f"avif {files['avif']['kb']}KB q{files['avif']['q']} / webp {files['webp']['kb']}KB"
          f"{' OVER BUDGET' if over else ''}")


def reject(shot_id, reason):
    st = load_state()
    rec = st["shots"].setdefault(shot_id, {"attempts": 0})
    rec.update(status="pending", attempts=rec.get("attempts", 0) + 1,
               last_rejection=reason)
    save_state(st)
    print(f"{shot_id}: REJECTED ({reason}) — stays pending, retry in a later batch")


def log_prompt(s, files):
    head = "# P1 image log\n\nEvery accepted image, with the prompt that produced it, so the set can be extended consistently.\n"
    if not os.path.exists(LOG):
        with open(LOG, "w") as f:
            f.write(head)
    body = open(LOG).read()
    entry = (f"\n## {s['id']}\n\n"
             f"- Set: {s['set']} · ratio {s['ratio']} · {s['width']}x{s['height']}\n"
             f"- Files: `{files['avif']['path']}` ({files['avif']['kb']} KB), "
             f"`{files['webp']['path']}` ({files['webp']['kb']} KB)\n"
             f"- Alt: {s['alt']}\n"
             f"- Prompt: {s['prompt']}\n")
    marker = f"\n## {s['id']}\n"
    if marker in body:
        start = body.index(marker)
        end = body.find("\n## ", start + 1)
        body = body[:start] + entry + (body[end:] if end != -1 else "")
    else:
        body += entry
    with open(LOG, "w") as f:
        f.write(body)


def og():
    m, st = load_manifest(), load_state()
    made = 0
    for o in m["og"]:
        src = shot(m, o["source"])
        p = os.path.join(ROOT, src["files"]["webp"])
        if not os.path.exists(p):
            print(f"{o['id']}: skipped (source {o['source']} not accepted yet)")
            continue
        im = Image.open(p).convert("RGB")
        im = centre_crop(im, "1200:630").resize((1200, 630), Image.LANCZOS)
        out = f"assets/img/{o['id']}-1200.webp"
        im.save(os.path.join(ROOT, out), "WEBP", quality=80, method=6)
        # og:image points at the JPEG: LinkedIn and several other crawlers still do
        # not fetch WebP, and a silently broken share card is worse than 40 KB.
        jpg = f"assets/img/{o['id']}-1200.jpg"
        im.save(os.path.join(ROOT, jpg), "JPEG", quality=82, optimize=True, progressive=True)
        st.setdefault("og", {})[o["id"]] = {"path": out, "jpg": jpg, "source": o["source"]}
        made += 1
    save_state(st)
    print("og cards written:", made)


def verify():
    m, st = load_manifest(), load_state()
    problems = []
    for s in m["shots"]:
        rec = st["shots"].get(s["id"], {})
        if rec.get("status") != "accepted":
            continue
        for key in ("avif", "webp"):
            p = os.path.join(ROOT, s["files"][key])
            if not os.path.exists(p):
                problems.append(f"{s['id']}: missing {key}")
                continue
            kb = os.path.getsize(p) / 1024
            limit = s["budget_kb"] * (1.0 if key == "avif" else 1.4)
            if kb > limit:
                problems.append(f"{s['id']}: {key} {kb:.0f}KB over {limit:.0f}KB budget")
            with Image.open(p) as im:
                if im.size != (s["width"], s["height"]):
                    problems.append(f"{s['id']}: {key} is {im.size}, expected {(s['width'], s['height'])}")
    print("\n".join(problems) if problems else "verify: all accepted images pass")
    return 1 if problems else 0


def status():
    m, st = load_manifest(), load_state()
    done = [s for s in m["shots"] if st["shots"].get(s["id"], {}).get("status") == "accepted"]
    print(f"accepted {len(done)}/{len(m['shots'])}")
    by_batch = {}
    for s in m["shots"]:
        ok = st["shots"].get(s["id"], {}).get("status") == "accepted"
        b = by_batch.setdefault(s["batch"], [0, 0])
        b[0] += ok
        b[1] += 1
    for b in sorted(by_batch):
        d, t = by_batch[b]
        print(f"  batch {b:>2}: {d}/{t}{'  <- next' if d < t and all(by_batch[x][0] == by_batch[x][1] for x in sorted(by_batch) if x < b) else ''}")


def nxt(batch=None):
    m, st = load_manifest(), load_state()
    pend = [s for s in m["shots"] if st["shots"].get(s["id"], {}).get("status") != "accepted"]
    if batch:
        pend = [s for s in pend if s["batch"] == int(batch)]
    else:
        pend = [s for s in pend if s["batch"] == pend[0]["batch"]] if pend else []
    if not pend:
        print("nothing pending")
        return
    print(f"BATCH {pend[0]['batch']} — {len(pend)} shots\n")
    for s in pend:
        rec = st["shots"].get(s["id"], {})
        note = f"  [retry: {rec['last_rejection']}]" if rec.get("last_rejection") else ""
        print(f"### {s['id']}  ({s['gen_size']}, crop {s['ratio']} -> {s['width']}x{s['height']}){note}")
        print(s["prompt"])
        print()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "add":
        add(sys.argv[2], sys.argv[3])
    elif cmd == "reject":
        reject(sys.argv[2], " ".join(sys.argv[3:]) or "unspecified")
    elif cmd == "next":
        nxt(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "og":
        og()
    elif cmd == "verify":
        sys.exit(verify())
    else:
        status()
