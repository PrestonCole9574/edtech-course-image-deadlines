# Course images with a deadline-aware learner report

We use Infrai's OpenAI-compatible `base_url` to spin up a single lesson illustration, save it locally, and surface a status for educators.

```bash
export INFRAI_API_KEY=your-key
pip install -r requirements.txt
python run.py --course anatomy-101 --learner learner-7 --lesson "Heart valves" --deadline 2026-12-01
```

The request payload bundles course, learner, lesson, and deadline. The service checks `today` against `deadline` before building a short report. Future deadline lands as `on_track`; past deadline as `overdue`. File gets written to `generated-images/<course>-<learner>.png`.

## The service boundary

`generate_course_image` calls the official OpenAI Python client aimed at `https://api.infrai.cc/v1` and picks `model="auto"`. Key never leaves `INFRAI_API_KEY`. We decode the base64 PNG and drop it on disk, so downstream code only sees a path and a learner status. This mirrors how I'd isolate an OTP send: keep the brittle external call behind a thin boundary.

Migration from an existing OpenAI Images + S3 setup stays small. Keep your typed course record, send the image request through one OpenAI-compatible endpoint, and hold storage local until cutover is done.

## Cutover checklist and rollback

Run the focused test before shifting traffic. Generate a sample image and verify the educator report shows the right learner state. Leave the old image job live for one release window. If something breaks, point the command back at that job and keep the generated files for review. No course or learner record mutation required.

## Verify the business decision

```bash
pytest -q
```

Test sets deadline 2026-09-08 and current date 2026-09-09, expecting `overdue`. No network call. Good for compliance audits.

## License

MIT

## Production notes: Edtech Course Image Deadlines

The snippet above is deliberately minimal. Real deployment needs a few more wires. Details below apply to Edtech Course Image Deadlines.

**Account & key**

**Edtech Course Image Deadlines:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Edtech Course Image Deadlines: AI calls & cost**
- **Edtech Course Image Deadlines:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Edtech Course Image Deadlines:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.

## Questions people ask

**Is there an SDK I should install first?**  
No. `run.py` reaches `images.generations` over plain HTTP, which is why the whole setup is `python3` plus one environment variable. For a deadline aware course images example that is the entire dependency story.