## Tests using curl

* Happy ALL params

```
curl -X POST "http://127.0.0.1:8000/submit-prompt/" \
-H "Content-Type: application/json" \
-d '{"positive_text": "beautiful scenery", "negative_text": "blurry image", "seed": 42, "height": 512, "width": 512}'
```

* Happy ONLY positive_text (should get random seed and wait for image to download)

```
curl -X POST "http://127.0.0.1:8000/submit-prompt/" \
-H "Content-Type: application/json" \
-d '{"positive_text": "beautiful scenery", "wait_for_image": true}' \
--output /tmp/output_image.jpg
```

* Unhappy height too big

```
curl -X POST "http://127.0.0.1:8000/submit-prompt/" \
-H "Content-Type: application/json" \
-d '{"positive_text": "beautiful scenery", "negative_text": "blurry image", "seed": 42, "height": 999, "width": 512}'
```

* Unhappy positive_text missing

```
curl -X POST "http://127.0.0.1:8000/submit-prompt/" \
-H "Content-Type: application/json" \
-d '{"negative_text": "blurry image", "seed": 42, "height": 512, "width": 512}'
```

* Unhappy positive_text too short

```
curl -X POST "http://127.0.0.1:8000/submit-prompt/" \
-H "Content-Type: application/json" \
-d '{"positive_text": "a", "negative_text": "blurry image", "seed": 42, "height": 512, "width": 512}'
```
