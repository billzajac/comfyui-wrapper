import re

# Read the multipart response from the file
with open("/tmp/output_response.txt", "rb") as f:
    content = f.read()

# Split the response by the boundary
boundary = "--boundary"
parts = content.split(boundary.encode())

# Extract the metadata (JSON) part
metadata_part = [part for part in parts if b"Content-Type: application/json" in part][0]
metadata = re.search(b"{.*}", metadata_part).group(0).decode("utf-8")
print("Metadata:", metadata)

# Extract the image part
image_part = [part for part in parts if b"Content-Type: image/jpeg" in part][0]
image_data = image_part.split(b"\r\n\r\n", 1)[1].rstrip(b"\r\n--")
with open("/tmp/output_image.jpg", "wb") as f:
    f.write(image_data)

print("Image saved to /tmp/output_image.jpg")
