from pynput.keyboard import Key, Listener, Controller, KeyCode
import json

def load_config(filename):
	try:
		with open(filename, "r") as f:
			return json.load(f)
	except Exception as e:
		print(f"Failed to load config: {str(e)}")
		return None

def validate_config(config):
	if not config:
		return False
	for pair_name, pair_data in config.items():
		if "keys" not in pair_data or "enabled" not in pair_data:
			print(f"Error in configuration schema: Pair {pair_name} must contain 'keys' and 'enabled' fields.")
			return False
		if len(pair_data["keys"]) != 2:
			print(f"Error in configuration: Pair {pair_name} must contain 2 key values in 'keys' field.")
			return False
	return True

class KeyboardManager:
	def __init__(self, config):
		self.config = config
		self.keyboard = Controller()
		self.pressed_buttons = set()

	def on_press(self, key):
		str_key = str(key).replace("'", "")
		for pair_data in self.config.values():
			if pair_data["enabled"] and str_key in pair_data["keys"]:
				self.pressed_buttons.add(key)
				str_other_key = [k for k in pair_data["keys"] if k != str_key][0]
				other_key = KeyCode.from_char(str_other_key)
				if other_key in self.pressed_buttons:
					self.release_key(other_key)

	def on_release(self, key):
		if key in self.pressed_buttons:
			print(f"key {key} released")
			self.pressed_buttons.remove(key)

	def release_key(self, key):
		self.keyboard.release(key)

	def press_key(self, key):
		self.keyboard.press(key)

if __name__ == "__main__":
	config = load_config("config.json")
	if validate_config(config):
		keyboard_manager = KeyboardManager(config)
		with Listener(on_press=keyboard_manager.on_press, on_release=keyboard_manager.on_release) as listener:
			listener.join()
