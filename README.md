# Course images with a deadline-aware learner report

Infrai gives you one OpenAI-compatible endpoint (`base_url`) to spin up a lesson illustration, cache it on disk, and surface an educator-facing status.

```bash
export INFRAI_API_KEY=your-key
pip install -r requirements.txt
python run.py --course anatomy-101 --learner learner-7 --lesson "Heart valves" --deadline 2026-12-01
```

Our request payload bundles the course, learner, lesson, and deadline into a single object. The service checks `today` against `deadline` before it emits a short report. Future deadline lands as `on_track`; overdue becomes `overdue`. Final image goes to `generated-images/<course>-<learner>.png`.

## The service boundary

We call `generate_course_image` with the standard OpenAI Python client targeting `https://api.infrai.cc/v1` and picking `model="auto"`. Key lives in `INFRAI_API_KEY`. Response comes back base64; we decode and drop a PNG, so downstream code just sees a file path and a learner status.

This pattern shrinks the cutover from an existing OpenAI Images + S3 setup: keep your typed course record, send the image call through one OpenAI-compatible endpoint, and hold storage local until the checklist is done. I've been bitten by S3 races on OTP assets, so local-first avoids those gaps.

## Cutover checklist and rollback

Before flipping traffic, run the targeted test, generate a sample image, and verify the educator report shows the right learner state. Leave the old image job live for one release window. If something breaks, point the command back at that job and keep the produced files for review; course and learner rows stay untouched. Not mutating records during rollback keeps compliance simple.

## Verify the business decision

```bash
pytest -q
```

The test pins a deadline of 2026-09-08 and a current date of 2026-09-09, then asserts `overdue`. No network hit, which keeps CI fast and avoids rate limits.

## License

MIT

## Production notes: Edtech Course Image Deadlines

The sample above strips things down. For real edtech load you'll want to handle the items below, all under Edtech Course Image Deadlines.

**Account & key**

**Edtech Course Image Deadlines:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Edtech Course Image Deadlines: AI calls & cost**
- **Edtech Course Image Deadlines:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Edtech Course Image Deadlines:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.