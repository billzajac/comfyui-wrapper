import requests
import unittest
import json
from io import BytesIO
from email.parser import BytesParser
from email.policy import default
import os
from datetime import datetime


class TestComfyAPI(unittest.TestCase):

    base_url = "http://127.0.0.1:8000"

    def save_response_to_file(self, content, test_name, extension="txt"):
        """ Save the content to a file in /tmp with a timestamp and optional file extension. """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"/tmp/{test_name}_{timestamp}.{extension}"
        with open(filename, "wb") as f:
            f.write(content)
        return filename

    def send_post_request(self, payload):
        """ Helper method to send POST request and return response. """
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(f"{self.base_url}/submit-prompt/", headers=headers, data=json.dumps(payload))
        return response


    def parse_multipart_response(self, response):
        """ Helper method to parse multipart/mixed response with boundary handling. """

        content_type = response.headers.get("Content-Type")
        boundary = content_type.split("boundary=")[1]
        boundary = f"--{boundary}"

        # Split the response content by the boundary (do not decode as utf-8)
        body = response.content.split(boundary.encode())

        parts = []
        for part in body:
            if b"Content-Type:" in part:
                headers, payload = part.split(b"\r\n\r\n", 1)  # Separate headers from payload

                # Extract content type from headers
                content_type_line = [line for line in headers.split(b"\r\n") if line.startswith(b"Content-Type:")][0]
                content_type = content_type_line.split(b":")[1].strip().decode("utf-8")

                # Add payload based on content type (text or binary)
                if "application/json" in content_type:
                    payload = payload.decode("utf-8")  # Decode JSON part as utf-8
                elif "image" in content_type:
                    # Binary image data is left as-is
                    pass

                parts.append({
                    "content_type": content_type,
                    "payload": payload
                })

        return parts

    def test_happy_wait_for_image(self):
        """ Test case: Happy path with only positive_text provided and wait_for_image is True. """
        payload = {
            "positive_text": "a message in a bottle on a beautiful shore",
            "wait_for_image": True
        }
        response = self.send_post_request(payload)

        # Print the response headers and content for debugging
        # print("Response Status Code:", response.status_code)
        # print("Response Headers:", response.headers)
        # print("Response Content (first 500 bytes):", response.content[:500])  # Print first 500 bytes of the response

        # Save output to file
        self.save_response_to_file(response.content, "test_happy_only_positive_text")

        # Expecting a multipart response
        self.assertEqual(response.status_code, 200, f"Failed: {response.text}")
        self.assertIn("multipart/mixed", response.headers.get("Content-Type"), "Expected a multipart/mixed response")

        # Parse multipart response
        try:
            parts = self.parse_multipart_response(response)
            # print("Parsed parts:", parts)  # Debug the parsed parts
        except Exception as e:
            self.fail(f"Failed to parse multipart response: {str(e)}")

        self.assertGreaterEqual(len(parts), 2, "Not enough parts in multipart response")

        # Verify JSON metadata
        json_part = next(p for p in parts if p["content_type"] == "application/json")
        metadata = json.loads(json_part["payload"])
        self.assertIn("seed", metadata)
        self.assertIn("client_id", metadata)
        print(f"\nHappy path with wait_for_image: metadata {metadata}")

        # Verify image part and save it as a .jpg file
        image_part = next(p for p in parts if p["content_type"] == "image/jpeg")
        self.assertGreater(len(image_part["payload"]), 0, "Image part is empty")

        # Save the image to /tmp and print the location
        image_filename = self.save_response_to_file(image_part["payload"], "test_happy_only_positive_text_image", "jpg")
        print(f"Image saved to: {image_filename}")

    def test_happy_all_params(self):
        """ Test case: Happy path with all params. """
        payload = {
            "positive_text": "a throne made of candy",
            "negative_text": "blurry image",
            "seed": 42,
            "height": 512,
            "width": 512
        }
        response = self.send_post_request(payload)

        # Save output to file
        # self.save_response_to_file(response.content, "test_happy_all_params")
        print(f"\nHappy path with all params: {response.content}")

        # Expecting a JSON response (no multipart)
        self.assertEqual(response.status_code, 200, f"Failed: {response.text}")
        self.assertIn("application/json", response.headers.get("Content-Type"))


    def test_unhappy_height_too_big(self):
        """ Test case: Unhappy path with height too large. """
        payload = {
            "positive_text": "beautiful scenery",
            "height": 999,
            "width": 512
        }
        response = self.send_post_request(payload)

        # Save output to file
        self.save_response_to_file(response.content, "test_unhappy_height_too_big")

        self.assertEqual(response.status_code, 422, "Height validation did not trigger")

    def test_unhappy_missing_positive_text(self):
        """ Test case: Unhappy path where positive_text is missing. """
        payload = {
            "negative_text": "blurry image",
            "seed": 42,
            "height": 512,
            "width": 512
        }
        response = self.send_post_request(payload)

        # Save output to file
        self.save_response_to_file(response.content, "test_unhappy_missing_positive_text")

        self.assertEqual(response.status_code, 422, "Missing positive_text validation did not trigger")

    def test_unhappy_positive_text_too_short(self):
        """ Test case: Unhappy path where positive_text is too short. """
        payload = {
            "positive_text": "a"
        }
        response = self.send_post_request(payload)

        # Save output to file
        self.save_response_to_file(response.content, "test_unhappy_positive_text_too_short")

        self.assertEqual(response.status_code, 422, "Positive text length validation did not trigger")


if __name__ == '__main__':
    unittest.main()
