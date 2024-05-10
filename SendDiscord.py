from pathlib import Path
import os
import requests


class SendDiscord:
    @classmethod
    def INPUT_TYPES(cls):
        encrypted_file_path = Path("custom_nodes/ComfyUI_sendDiscord")
        encrypted_files = sorted(
            [f.name for f in encrypted_file_path.glob("*.enc") if f.is_file()])

        return {
            "required": {
                "path": ("VHS_FILENAMES",),
                "user_name": ('STRING', {'default': 'Banodoco'}),
                "user_message": ('STRING', {'default': 'Check out my latest work!'}),
                # Adding encrypted file selection, assume it's passed as a filename string
                "encrypted_file": (encrypted_files,),
            },
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "send_to_discord"

    def send_to_discord(self, path, user_message="", user_name="Default Username", encrypted_file=None):
        # Handle path input tuple from ComfyUI
        if isinstance(path, tuple):
            path = path[1] if len(path) > 1 and isinstance(
                path[1], list) else []

        if not path:
            print("No video paths provided to send to Discord.")
            return []

        # Preparing to send files to Heroku
        files = [('file', (os.path.basename(p), open(p, 'rb'),
                  'application/octet-stream')) for p in path]

        # Include encrypted file if provided
        if encrypted_file:
            encrypted_file_path = Path(
                "custom_nodes/ComfyUI_sendDiscord") / encrypted_file
            if encrypted_file_path.exists() and encrypted_file_path.is_file():
                files.append(('encrypted_file', (encrypted_file, open(
                    encrypted_file_path, 'rb'), 'application/octet-stream')))

        payload = {
            'user_name': user_name,
            'user_message': user_message,
        }

        try:
            response = requests.post(
                'https://banodoco-942cd408d2cc.herokuapp.com/upload_files',
                files=files,
                data=payload
            )
            if response.status_code == 200:
                print("Files sent successfully to Heroku")
                print(response.json())
                return [response.json()]
            else:
                print("Failed to send files, status code:", response.status_code)
                return []
        except requests.exceptions.RequestException as e:
            print("Failed to send files due to an error:", str(e))
            return []


NODE_CLASS_MAPPINGS = {
    "SendDiscord": SendDiscord,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SendDiscord": "Send Video to Discord 🎥🅥🅗🅢",
}
