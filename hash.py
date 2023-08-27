import hashlib

def calculate_sha256_hash(image_path):
    try:
        # Open the image file in binary read mode
        with open(image_path, 'rb') as file:
            # Read the binary data of the image
            image_data = file.read()

            # Calculate the SHA-256 hash
            sha256_hash = hashlib.sha256(image_data).hexdigest()

        return sha256_hash

    except Exception as e:
        print("Error calculating SHA-256 hash:", str(e))
        return None

# Specify the path to your image file
image_path = '/Users/siddharthdeo/Downloads/yowsup-cli-2.0/pro2file.jpeg'

# Calculate the SHA-256 hash of the image
hash_value = calculate_sha256_hash(image_path)

if hash_value:
    print("SHA-256 Hash:", hash_value)
else:
    print("Failed to calculate the SHA-256 hash.")
