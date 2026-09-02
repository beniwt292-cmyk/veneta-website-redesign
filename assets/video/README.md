# Hero background video

Drop an encode in here and the homepage hero plays it over the still. Remove the
files and the hero silently returns to the photograph. Nothing else to change.

## Naming

The hero asks for `hero-home`. Both of these are optional; ship either or both:

    assets/video/hero-home.webm    AV1 or VP9
    assets/video/hero-home.mp4     H.264 High, the universal floor

Whichever file is smaller is listed first in the markup, so there is no need to
hand-tune the order.

The poster frame is reused from `assets/img/hero-home-1536.webp`, so the first
frame of the video must match that photograph's framing or the swap will visibly
jump.

## Encode targets

| Setting | Value | Why |
|---|---|---|
| Resolution | 1920x1080 | Upscaled by `object-fit:cover` past that; 4K is wasted on a darkened background |
| Duration | 4 to 6 seconds, plays once | The clip is not set to loop: it plays through once per pageview and rests on its final frame. No `loop` attribute in the markup, and the JS never restarts it, including when it scrolls back into view. |
| Frame rate | 24 or 25 fps | Matches the still photography's film look |
| Audio | none, stripped from the file | The element is muted and decorative; audio blocks autoplay on some browsers |
| Target size | under 2.5 MB mp4, under 1.8 MB webm | Above that the hero costs more than the rest of the page combined |

Content should be slow: a curtain drift, a shade lowering, light moving across a
floor. Anything with a cut or a camera move fights the headline. Because it only
plays once, trim to just the active motion, there is no benefit to a long hold
on a static final frame; the poster/last-frame does that job for free.

If the source footage is lower resolution than 1080p (true of most AI-generated
clips today), run it through a denoise + lanczos upscale + light sharpen pass
before the final encode rather than a plain scale. A plain upscale looks soft;
denoising first keeps the sharpen pass from amplifying compression noise:

    ffmpeg -i source.mp4 -t 5.4 \
      -vf "hqdn3d=1.2:1.0:6:6,scale=1920:1080:flags=lanczos:force_original_aspect_ratio=increase,crop=1920:1080,unsharp=5:5:0.6:5:5:0.0" \
      -an -c:v libx264 -profile:v high -crf 19 -preset slow -pix_fmt yuv420p \
      -movflags +faststart assets/video/hero-home.mp4

## Commands

    # H.264 fallback
    ffmpeg -i master.mov -an -vf "scale=1920:-2,fps=24" \
      -c:v libx264 -profile:v high -crf 25 -preset slow \
      -pix_fmt yuv420p -movflags +faststart assets/video/hero-home.mp4

    # AV1 (best ratio, needs a recent ffmpeg)
    ffmpeg -i master.mov -an -vf "scale=1920:-2,fps=24" \
      -c:v libsvtav1 -crf 38 -preset 6 assets/video/hero-home.webm

    # VP9 if libsvtav1 is unavailable
    ffmpeg -i master.mov -an -vf "scale=1920:-2,fps=24" \
      -c:v libvpx-vp9 -crf 34 -b:v 0 -row-mt 1 assets/video/hero-home.webm

Check the result: if the webm lands heavier than the mp4, drop it and ship the
mp4 alone rather than shipping a fallback that costs more than the floor.

`-movflags +faststart` matters: without it the moov atom sits at the end of the
file and playback waits for the whole download.

## Playback rules already handled in code

- Nothing downloads until `build/interactive.js` attaches the sources.
- Skipped entirely on `prefers-reduced-motion: reduce`, Save-Data and 2G.
- Paused when the hero scrolls out of view.
- A visible pause control appears once the first frame is decodable, which is
  what WCAG 2.2.2 requires for motion that runs longer than five seconds.
- The `<picture>` still is the LCP paint, so the video cannot regress that metric.

## Current file

`hero-home.mp4` / `hero-home.webm` in this folder are a placeholder: a slow
12-second push across the existing hero photograph, generated so the motion
treatment can be reviewed before real footage exists. Replace both with the shot
footage; the markup does not change.
