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
                "user_message": ('STRING', {'default': 'Check out my latest work!'}),
                "encrypted_file": (encrypted_files,),
            },
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "send_to_discord"

    def send_to_discord(self, path, user_message="", user_name="Default Username", encrypted_file=None):
        print("Starting send_to_discord function...")
        print(f"Path received: {path}")
        print(f"User message: {user_message}")
        print(f"User name: {user_name}")
        print(f"Encrypted file received: {encrypted_file}")

        if isinstance(path, tuple):
            path = path[1] if len(path) > 1 and isinstance(
                path[1], list) else path[0]

        print(f"Processed path: {path}")

        if not path:
            print("No paths provided to send to Discord.")
            return []

        files = []
        for p in path:
            if not p.endswith('.png'):  # PNG dosyalarını hariç tut
                with open(p, 'rb') as file:
                    files.append(
                        ('file', (os.path.basename(p), file.read(), 'application/octet-stream')))
        print(f"Files prepared for sending: {[f[0] for f in files]}")

        if encrypted_file:
            encrypted_file_path = Path(
                "custom_nodes/ComfyUI_sendDiscord") / encrypted_file
            if encrypted_file_path.exists() and encrypted_file_path.is_file():
                with open(encrypted_file_path, 'rb') as file:
                    files.append(
                        ('encrypted_file', (encrypted_file, file.read(), 'application/octet-stream')))
                print(f"Encrypted file added: {encrypted_file}")

        payload = {'user_name': user_name, 'user_message': user_message}

        try:
            response = requests.post(
                'https://urchin-app-brlyp.ondigitalocean.app/upload_files',
                files=files,
                data=payload
            )
            print(f"Response status code: {response.status_code}")
            if response.status_code == 200:
                print("Files sent successfully to Heroku")
                print(f"Response content: {response.json()}")
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
