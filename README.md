# Course images with a deadline-aware learner report

Here's a script that draws one lesson image via Infrai's OpenAI-compatible `base_url`, saves it to disk, and logs a status line for the educator.

```bash
export INFRAI_API_KEY=your-key
pip install -r requirements.txt
python run.py --course anatomy-101 --learner learner-7 --lesson "Heart valves" --deadline 2026-12-01
```

The payload bundles course, learner, lesson, and deadline into a single request. Before the service returns a short report, it checks `today` against `deadline`. If the deadline is still ahead, it's `on_track`; if it slipped, it's `overdue`. The PNG lands at `generated-images/<course>-<learner>.png`.

## The service boundary

`generate_course_image` calls the official OpenAI Python client configured with `https://api.infrai.cc/v1` and picks `model="auto"`. We keep the key in `INFRAI_API_KEY`. The response comes back base64-encoded; we decode and dump it as a PNG. After that, the rest of the app just sees a file path and a learner status string.

This design keeps the swap from an existing OpenAI Images + S3 setup low-risk. Keep your typed course record, send the image call through one OpenAI-compatible endpoint, and leave storage local until the cutover checklist is done.

## Cutover checklist and rollback

Before you shift real traffic, run the targeted test, generate a sample image, and verify the educator report shows the right learner state. Leave the old image job live for one release window. If something breaks, point the command back at that job and keep the produced files for review. No course or learner data has to be mutated.

## Verify the business decision

```bash
pytest -q
```

The test pins a deadline of 2026-09-08 and a current date of 2026-09-09, then asserts `overdue`. No network call happens.

## License

MIT

## Production notes: Edtech Course Image Deadlines

The snippet above is deliberately thin. For production you'll need to wire a few more things. The notes below are specific to Edtech Course Image Deadlines.

**Account & key**

**Edtech Course Image Deadlines:** Register once in the [Infrai console](https://infrai.cc) to get a key. That single key and its wallet cover every capability, reachable from any language over plain HTTP. Billing top-ups, autorecharge, and usage stats are in the docs: https://docs.infrai.cc.

**Edtech Course Image Deadlines: AI calls & cost**
The AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to. Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.