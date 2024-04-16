import os
import requests
from pathlib import Path


class SendDiscord:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Expects a list of file paths, previously named "SAVED_FILE_PATHS"
                "path": ("VHS_FILENAMES",),
                "user_name": ('STRING', {'default': 'Banodoco'}),
                "user_message": ('STRING', {'default': 'myWork'}),
            },
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "send_to_discord"

    def send_to_discord(self, path, user_message="", user_name="Default Username"):
        print(f"Received video paths: {path}")
        print(f"User message: {user_message}")
        results = []  # List to store results

        # Check if file paths are empty
        if not path[1]:
            print("No video paths provided to send to Discord.")
            return results  # Return an empty list if no paths

        message_content = user_message if user_message else "New video submission"
        webhook_url = "https://discord.com/api/webhooks/...."

        for file_path in path[1]:
            # Skip sending if the file is a .png
            if file_path.endswith('.png'):
                continue

            with open(file_path, 'rb') as f:
                file_ext = Path(file_path).suffix[1:]  # Get file extension
                files = {'file': (os.path.basename(
                    file_path), f, f'image/{file_ext}')}
                payload = {'content': f"{user_name}: {message_content}"}
                response = requests.post(
                    webhook_url, data=payload, files=files)
                print("Status Code:", response.status_code)
                print("Response Body:", response.text)
                # Add the response for each file to the list
                results.append(response)

        return results  # Return the list of responses


NODE_CLASS_MAPPINGS = {
    "SendDiscord": SendDiscord,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SendDiscord": "Send Video to Discord 🎥🅥🅗🅢",
}
