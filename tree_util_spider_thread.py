"""
This script lets you generate snap shots of your Drive folder structure.
You need Python 3.6 or higher to run this script.

Inspired by: [class - representation of files and folder-tree of Google Drive folder using Python API - Stack Overflow](https://stackoverflow.com/questions/48112412/representation-of-files-and-folder-tree-of-google-drive-folder-using-python-api)
Help with ChatGPT: https://chatgpt.com/c/67b0e93c-c474-8004-8740-e4bbb98486d1

"""

print("\n\n	🌳 Tree Spider - Directory Snapshot Tool\n\n")
print("		⏳ Initializing...\n")
# Colored emojis
colored_check = "\033[32m✅\033[0m"
colored_x = "\033[31m❌\033[0m"
colored_stop = "\033[31m🛑\033[0m"
colored_warn = "\033[93m⚠️\033[0m"
colored_bulb = "\033[36m💡\033[0m"
colored_no_entry = "\033[31m⛔\033[0m"
colored_question = "\033[1m❓\033[0m"
colored_arrow_right = "\033[33m🡆\033[0m"
colored_exclamation = "\033[31m❗\033[0m"



# Color ANSI codes
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BOLD = "\033[1m"
BOLD_ORANGE = "\033[1;33m"
BOLD_CYAN = "\033[1;36m"
GREY = "\033[90m"

def colored_emoji_test():
	""" Test all defined emojis are working. """
	print(f"{colored_check} {colored_x} {colored_stop} {colored_warn} {colored_bulb} {colored_no_entry} {colored_question} {colored_arrow_right} {colored_exclamation}")
	print("See if the emojis are working...")
	print(f"If they are, remove colored_emoji_test() from {__file__}...")
	exit()

error_logs = []
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from datetime import datetime
from functools import partial
from getpass import getpass
import concurrent.futures
from tqdm import tqdm
from sys import exit
import subprocess
import threading
import mimetypes
import itertools
import traceback
import platform
import humanize
import logging
import shutil
import random
import psutil
import math
import json
import time
import stat
import sys
import bz2
import re
import os
try: # Google Magika, Python 3.12 - 3.8	
	from magika import Magika
	import pathlib
	m = Magika()
except Exception as m:
	logging.debug("Magika not found, using mimetypes/magic instead")

if os.name == "nt":  # Windows only, get volume label
	import ctypes
	import ctypes.wintypes

	def get_volume_label(drive_letter):
		"""
		Retrieves the volume label of the specified drive letter on Windows.

		Args:
			drive_letter: A single character string representing the drive letter (e.g., 'C').

		Returns:
			The volume label of the drive as a string, or None if the volume label is not available.
		"""

		volume_name = ctypes.create_unicode_buffer(1024)
		file_system = ctypes.create_unicode_buffer(1024)

		ctypes.windll.kernel32.GetVolumeInformationW(
			f"{drive_letter}:\\",
			volume_name,
			ctypes.sizeof(volume_name),
			None,
			None,
			None,
			file_system,
			ctypes.sizeof(file_system)
		)
		
		return volume_name.value if volume_name.value else None

logging.basicConfig(format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

try:
	import keyboard
except ModuleNotFoundError as m: # Keyboard, optional
	print(f"{colored_warn}{YELLOW}[{type(m).__name__}]{RESET}: {m} - keyboard module not found.")
	print(f"{colored_bulb} Install with: `{GREY}pip install keyboard{RESET}`")

try:
	import magic
except ModuleNotFoundError as m:
	print(f"{colored_warn}{YELLOW}[{type(m).__name__}]{RESET}: {m} - MIME types will be detected using file extensions.")
	print("But you can install python-magic-bin to speed up the process.")
	if os.name == "nt":  # Windows
		print(f"{colored_bulb} Install with: `{GREY}pip install python-magic-bin{RESET}`")
	else:  # Linux
		print(f"{colored_bulb} Install with the following command:\n 1. `{GREY}sudo apt install python3-magic{RESET}`\n 2. `{GREY}pip install python-magic{RESET}`")

except Exception as i:
	print(f"{colored_warn} {YELLOW}[{type(i).__name__}]{RESET}: {i}; Check your Magic installation.\n")
	error_logs.append({"name": "magic", "type": str(type(i).__name__), "desc": str(i)})

if "magic" in sys.modules:
	try:# Test if magic is working
		magic.from_buffer(b"", mime=True)
	except Exception as m:
		print(f"{colored_warn} {YELLOW}[{type(m).__name__}]{RESET}: {m}; Magic installed but Magic is not working properly.\n")
		error_logs.append({"name": "magic", "type": str(type(m).__name__), "desc": str(m)})


class Spinner:
	def __init__(self, wait=0.05, show_timer=True, timer_delay=2, char="ascii", done_message=" "):
		"""
		Initialize a Spinner object with customizable animation and timer settings.

		Parameters:
			wait (float, optional): The delay between each animation frame in seconds. Defaults to 0.1.
			show_timer (bool, optional): Whether to display a timer alongside the animation. Defaults to True.
			timer_delay (int, optional): The delay in seconds before the timer starts displaying. Defaults to 2.
			char (str, optional): The character set to use for the animation. Options include "braille", "braille2", "fragment", "shade", "normal", "squish", "trigram", "trigram2", "emoji_arrows", "emoji_hourglass", "emoji_clock", and "ascii". Defaults to "ascii".
			done_message (str, optional): The message to display when the animation is stopped. Defaults to " ".

		Returns:
			None
		"""
		
		# Spinner animation frames
		if char == "braille":
			symbols = ["⠋", "⠙", "⠸", "⠴", "⠦", "⠇"]
		elif char == "braille2":
			symbols = ["⠋⠀", "⠉⠁", "⠈⠃", "⠀⠇", "⠠⠆", "⠤⠄", "⠦⠀", "⠇⠀"]
		elif char == "fragment":
			symbols = ["█","▖","▗","▘","▙","▚","▛","▜","▝","▞","▟"]
			random.shuffle(symbols)
		elif char == "shade":
			symbols = ["█", "▓", "▒", "░", "▒", "▓"]
		elif char == "normal":
			symbols = [ "◞","◡", "◟","◜","◠","◝"]
			symbols = ["◞", "◟","◜","◝"]
		elif char == "squish":
			symbols = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "█","▉","▊","▋","▌","▍","▎","▏"," "]
		elif char == "trigram":
			symbols = ["☰", "☱" ,"☲", "☴", "☶", "☵" ,"☳" ,"☷","☳", "☵","☶","☴","☲","☱","☰"]
		elif char == "trigram2":
			symbols = ["☰", "☱","☳","☷", "☶","☴","☰"]
		elif char == "emoji_arrows":
			symbols = ["⬆️","↗️","➡️","↘️","⬇️","↙️","⬅️","↖️"]
		elif char == "emoji_hourglass":
			symbols = ["⏳", "⏳", "⏳","⏳", "⌛", "⌛", "⌛", "⌛"]
		elif char == "emoji_clock":
			symbols = ["🕐","🕜","🕑","🕝","🕒","🕞","🕓","🕟","🕔","🕠","🕕","🕡","🕖","🕢","🕗","🕣","🕘","🕤","🕙","🕥","🕚","🕦","🕛","🕧"]
		elif char == "emoji_moon":
			symbols = ["🌑","🌒","🌓","🌔","🌕","🌖","🌗","🌘"]
		elif char == "emoji_moon2":
			symbols = ["🌚","🌒","🌓","🌔", "🌝","🌖","🌗","🌘"]
		elif char == "emoji_globe":
			symbols = ["🌍","🌍","🌍","🌍","🌎","🌎","🌎","🌎","🌏","🌏","🌏","🌏",]
		else: # char == "ascii"
			symbols = ['|', '/', '-', '\\']
		
		self.spinner_cycle = itertools.cycle(symbols)
		self.wait = wait
		self.show_timer = show_timer
		self.timer_delay = timer_delay
		self.running = False
		self.done_message = done_message
		self.thread = None

	def spin(self):
		"""Spinner animation running in a separate thread."""
		while self.running:
			elapsed = time.time() - start_spinner
			if elapsed < self.timer_delay or not self.show_timer:
				time_print = ""
			else:
				time_print = f" ({format_duration(elapsed)})"
			
			sys.stdout.write(f'\r{next(self.spinner_cycle)}' + time_print)  # Overwrite previous character
			sys.stdout.flush()
			time.sleep(self.wait)

	def start(self):
		"""Start the spinner thread."""
		if not self.running:
			global start_spinner
			start_spinner = time.time()
			self.running = True
			self.thread = threading.Thread(target=self.spin, daemon=True)  # Daemon thread stops when main exits
			self.thread.start()

	def stop(self):
		"""Stop the spinner and clear the line."""
		self.running = False
		if self.thread:
			self.thread.join()  # Ensure the thread stops
		sys.stdout.write(f'\r{self.done_message}\n')  # Print completion message
		sys.stdout.flush()

init_spinner = Spinner()
init_spinner.start()

from inputimeout import inputimeout, TimeoutOccurred

def timed_choice(question, timeout=10, default=False):
	# Function to ask a yes/no question with a timeout
	# If y == return True else return False
	try:
		answer = inputimeout(prompt=f"{question} (yes/no) [Default: {default}]\n", timeout=timeout)
		if answer.lower() == 'y' or answer.lower() == 'yes':
			return True
		else:
			return False
	except TimeoutOccurred:
		print('\nTimed out! Using default response.')
		return default

# Example usage

def seconds_to_datetime(seconds, ispath=False):
	"""Convert a Unix timestamp in seconds to a human-readable string.

	Parameters:
		seconds (int): The Unix timestamp in seconds.
		ispath (bool): If True, the string will be formatted as a filename-safe date string ("%Y-%m-%d_%H%M%S"). Otherwise, it will be a readable date string ("%Y-%m-%d %H:%M:%S.%f").

	Returns:
		str: The formatted date string.
	"""
	
	
	pattern = "%Y-%m-%d_%H%M%S" if ispath else "%Y-%m-%d %H:%M:%S.%f"
	return str(datetime.fromtimestamp(math.fabs(seconds)).strftime(pattern))


def format_duration(seconds):

	"""Format a duration in seconds to a human-readable string.

	The output string will be in the format "HH:MM:SS.MMM", or "DDd HH:MM:SS.MMM" if the duration is longer than a day.

	Parameters:
		seconds (int): The duration in seconds.

	Returns:
		str: The formatted duration string.)
	"""
	days, remainder = divmod(seconds, 86400)  # 86400 seconds in a day
	hours, remainder = divmod(remainder, 3600)
	minutes, remainder = divmod(remainder, 60)
	seconds, milliseconds = divmod(remainder, 1)  # Get milliseconds
	milliseconds = int(milliseconds * 1000)  # Convert to ms

	time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"

	if days > 0:
		return f"{int(days)}d {time_str}"
	return time_str

def get_size_of(obj):
	"""Convert a variable to a string and return its byte size."""
	return len(str(obj).encode('utf-8'))  # Convert to string, then get byte length



def plural(value, plural="s", non_plural=""):
	"""
	Returns the appropriate pluralization suffix based on the given value.

	Parameters:
		value (int): The number to determine singular or plural form.
		plural (str, optional): The suffix to use for plural form. Defaults to "s".
		non_plural (str, optional): The suffix to use for singular form. Defaults to an empty string.

	Returns:
		str: The appropriate suffix based on the value.
	
	Example:
		>>> plural(1)
		''
		>>> plural(2)
		's'
		>>> plural(1, 'es', '')
		''
		>>> plural(3, 'es', '')
		'es'
	"""
	return non_plural if value == 1 else plural



def shorten_string(string, max_length=20, placeholder="...", keep_filename=False):
	"""
	Shorten a string if it is longer than a specified maximum length.

	If the string is longer than the maximum length, a placeholder string is
	inserted in the middle of the string. If the string is a path, the
	placeholder string is inserted in the middle of the path, and the
	filename is left intact.

	Args:
		string (str): The string to shorten.
		max_length (int): The maximum length of the string. Defaults to 20.
		placeholder (str): The placeholder string to insert into the middle
			of the string. Defaults to "...".
		keep_filename (bool): Whether to keep the filename intact. Defaults to
			False.

	Returns:
		str: The shortened string.
	"""
	try:
		if len(str(string)) <= round(max_length):
			return string
		if keep_filename:
			head, tail = os.path.split(string)  # Get directory and filename
			half_len = (round(max_length) - len(tail) - len(placeholder)) // 2
			return head[:half_len] + placeholder + head[-half_len:] + "/" + tail
		else:
			half_len = (round(max_length) - len(placeholder)) // 2
			return string[:half_len] + placeholder + string[-half_len:]
	except Exception as e:
		return string



def input_or_exit(prompt, exit_message=f"{colored_stop} Exiting..."):
	"""Read input from the user with a prompt, and exit with a message if CTRL+C is pressed.

	Args:
		prompt (str): The prompt string to display to the user.
		exit_message (str, optional): The message to print when exiting. Defaults to f"{colored_stop} Exiting...".

	Returns:
		str: The input string entered by the user.
	"""
	try:
		return input(prompt)
	except KeyboardInterrupt:
		print(exit_message)
		exit()


def get_filesystem_type_cross_platform(path):
	"""Detects filesystem type for a given path on Windows/Linux/macOS."""
	partitions = psutil.disk_partitions()
	for partition in partitions:
		if path.startswith(partition.mountpoint):
			return partition
	return "Unknown"

def spinner_demo(wait=5):
	spinner = Spinner(char="emoji_arrows")
	spinner.start() # small spinner animation, but works well
	time.sleep(wait)
	spinner.stop()
	# Task completed

def clear_screen():
	"""
	Clears the console screen and moves the cursor to the top left corner.

	This function works on both Windows and Unix-like systems (including macOS and Linux).
	"""
	os.system('cls' if os.name == 'nt' else 'clear')

def title(title):
	"""
	Sets the console window title to the specified string.

	This function changes the title of the console window to the given `title`
	string. It is compatible with both Windows and Unix-like systems
	(including macOS and Linux).

	Args:
		title (str): The title to set for the console window.
	"""
	title = title.replace('&', '^&')  # Escape double quotes
	os.system(f'title {title}' if os.name == 'nt' else f'echo "\033]0;{title}\007"')

def get_partition_from_path(path):
	"""Returns the mount point or drive for a given path."""
	for partition in psutil.disk_partitions():
		if path.startswith(partition.mountpoint):
			return partition  # e.g., "C:\", "/dev/sda1"
	return ["Unknown","Unknown","Unknown","Unknown"]

def bz2_load_to_json(input_bz2):
	"""
	Converts a compressed bz2 file to a JSON content.

	Args:
		input_bz2 (str): The path to the input bz2 file.
	"""
	with open(input_bz2, 'rb') as f_in:
		return json.loads(bz2.decompress(f_in.read()).decode('utf-8'))


# Function to wait for 10 seconds or until a key is pressed
def timeout(timeout=10, nobreak=False, key='Enter'):
	"""
	Wait for a specified timeout or until a key is pressed.

	Parameters:
		timeout (int): The number of seconds to wait. A value of -1 means to wait indefinitely for a key press.
		nobreak (bool): If True, ignore key press except for CTRL+C. Default is False.
		key (str): The key to wait for. Default is 'Enter'.
	
	Returns:
		None
	"""
	if nobreak: # If nobreak is True, ignore key press except for CTRL+C
		ToExit = "press CTRL+C to quit ..."
	else: # If nobreak is False, wait for key press
		ToExit = f"press {key} to continue ..."
	if timeout == -1: # If timeout is -1, wait indefinitely for a key press
		# print("Waiting indefinitely for a key press...")
		print(ToExit[0].upper() + ToExit[1:])
		while True:
			try:
				if not nobreak:
					if keyboard.is_pressed(hotkey=key):
						# print("Key pressed, continuing...")
						return
			except KeyboardInterrupt:
				return
	elif timeout < -1: # If timeout is a negative number, log an error and return
		raise ValueError('Invalid value for timeout specified. Valid range is -1 to ∞.')
	else: # If timeout is a positive number, wait for the specified timeout
		start_time = time.time()
		while round(time.time() - start_time) < timeout:
			try:
				if not nobreak: # If nobreak is False, wait for key press
					if keyboard.is_pressed(hotkey=key):
						# print("Key pressed, continuing...")
						return
				time.sleep(0.1)  # Sleep for a short time to avoid high CPU usage
				sys.stdout.write(f"\rWaiting for  {round(timeout - (time.time() - start_time))} seconds, {ToExit}")
				sys.stdout.flush()
			except KeyboardInterrupt:
				return
		return
		# print("Timeout reached, continuing...")


def pause(wait_message="Press Enter to continue...:", exit_message=""):

	"""
	Pauses the program execution until the user presses Enter.

	This function displays a message prompting the user to press the Enter key
	to continue. If the user presses CTRL+C, it exits the program with an optional
	exit message.

	Args:
		wait_message (str, optional): The message to display while waiting for user input. Defaults to "Press Enter to continue...:".
		exit_message (str, optional): The message to display when exiting due to a KeyboardInterrupt. Defaults to an empty string.
	"""

	try:
		getpass(wait_message)
	except KeyboardInterrupt:
		print(exit_message)
		exit()

def get_file_icon(filename, mime_type):
	"""
		Get a file icon based on its extension and/or MIME type.

		This function takes a filename and/or MIME type as input and returns a
		corresponding icon. If no matching icon is found, it returns " " (a
		folder icon) if the MIME type is "folder", or " " (a document icon)
		otherwise.

		Parameters:
			filename (str): The name of the file to get an icon for.
			mime_type (str): The MIME type of the file to get an icon for.

		Returns:
			str: A string representing the icon for the given file.
	"""

	# Priority is up to down
	# Search by extension, not postfix
	icons_extension = {
		".safetensors": "🧠",
		".onnx": "🧠",
		".ckpt": "🏋️",
		".lnk": "🔗",
		".url": "🌐",
		".exe": "🚀",
		".pth": "🧠",
		".log": "🧾",
		".srt": "💬",
		".dll": "🧩",
		".sys": "🛠️",
		".ini": "🔧",
		#".sub": "💬",
	}

	for extension, icon in icons_extension.items():
		if extension.lower() == os.path.splitext(filename)[-1].lower():
			return icon


	# Search by Prefix
	icons_prefix = {
		"README": "📖",
		"LICENSE": "🪪",
		"INSTALL": "📝",
		"CHANGELOG": "📅",
		"CONTRIBUTING": "🤝",
		"CODE_OF_CONDUCT": "🚦",
		"CONTRIBUTORS": "🪪",
		"SECURITY": "🔒",
		"TODO": "📋",
		"SUPPORT": "📞",
		"NOTES": "📝",
		"requirements": "🐍",
	}

	for prefix, icon in icons_prefix.items():
		if filename.lower().startswith(prefix.lower()):
			return icon

	# Whole match
	icons_whole = {
		".gitignore": "➖",
		".dockerignore": "➖",
		".nomedia": "➖",
		".npmignore": "➖",
		".gitattributes": "🔧",
		".editorconfig": "🔩",
		".prettierrc":"📏",
		".eslintrc":"📏",
		".stylelintrc":"📏",
		"dockerfile": "🐳",
		"dockerignore": "➖",
		"docker-compose.yml": "🐳",
		"docker-compose.	yaml": "🐳",
		"DockerFile": "🐳",
		"Pipfile": "🐍",
		"package.json": "📦",
		"package-lock.json": "📦",
		"desktop.ini": "🏷️",
		"Makefile": "🔨",
		"Jenkinsfile": "🏗️",
		"package.json": "📦",
		".DS_Store": "🏷️",
		"yarn.lock": "🔒",
		"config.json": "🔧",
		"database.sqlite": "🗄️",
		"jest.config.js": "🃏",
		"log.txt":"📜",
		"error.log":"❌",
		".nvmrc":"🏗️",
		".babelrc":"🏗️",
		".gitmodules":"📦",
		"CMakeLists.txt":"🏗️",
	}

	for whole, icon in icons_whole.items():
		if filename.lower() == whole.lower():
			return icon

	# MIME types; icon will be applied up to down, so place longer MIME types first and also you can find duplicates easier.
	icons = {

		# Images
		"image/vnd.microsoft.icon": "📌",
		"image/svg+xml": "📐",
		"image/x-icon": "📌",
		"image/heic": "📷",
		"image/heif": "📷",
		"image/jpeg": "📷",
		"image/gif": "🎞️",
		"image/xcf": "🖌️",


		# Video
		"video/vnd.dlna.mpeg-tts": "📹",
		"video/x-sgi-movie": "📹",
		"video/x-matroska": "🎥",
		"video/quicktime": "🎥",
		"video/x-msvideo": "🎞️",
		"application/ogg": "🎬",
		"video/x-flv": "🎬",
		"video/webm": "🎞️",
		"video/mpeg": "📹",
		"video/3gp": "📼",
		"video/mp4": "🎬",
		"video/ogg": "🎞️",

		# Audio
		"application/vnd.rn-realmedia": "🎙️",
		"audio/x-pn-realaudio": "🎙️",
		"application/x-cdf": "💿",
		"audio/x-aiff": "🎧",
		"audio/x-midi": "🎹",
		"audio/basic": "🎵",
		"audio/x-wav": "🔉",
		"audio/x-aac": "🎧",
		"audio/3gpp2": "🎙️",
		"audio/mpeg": "🎵",
		"audio/opus": "🎤",
		"audio/3gpp": "🎙️",
		"audio/webm": "🎤",
		"audio/midi": "🎹",
		"audio/mid": "🎹",
		"audio/3gp": "🎙️",
		"audio/ogg": "🔉",
		"audio/wav": "🔉",
		"audio/aac": "🎧",
		"audio/mp4": "🎧",

		# Documents
		"text/tab-separated-values": "📊",
		"application/x-yaml": "📑",
		"application/x-httpd-php": "🌐",
		"application/x-mhtml": "🌐",
		"application/pdf": "📕",
		"application/xml": "📑",
		"application/rtf": "📝",
		"text/markdown": "📝",
		"text/richtext": "📝",
		"text/x-setext": "📜",
		"text/x-vcard": "📇",
		"text/x-sgml": "📜",
		"text/plain": "📄",
		"text/x-rst": "📜",
		"text/plain": "📝",
		"text/html": "🌐",
		"text/xml": "📑",
		"text/vtt": "💬",
		"text/n3": "📖",

		# Microsoft Office
		"application/vnd.ms-powerpoint": "📽️",
		"application/vnd.ms-excel": "📊",
		"application/vnd.visio": "📊",
		"application/msword": "📑",

		# Microsoft Office Open XML
		"application/vnd.openxmlformats-officedocument.presentationml.presentation": "📽️",
		"application/vnd.openxmlformats-officedocument.wordprocessingml.document": "📑",
		"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "📊",


		# OpenDocument
		"application/vnd.oasis.opendocument.graphics-template": "🖌️",
		"application/vnd.oasis.opendocument.presentation": "📽️",
		"application/vnd.oasis.opendocument.spreadsheet": "📊",
		"application/vnd.oasis.opendocument.graphics": "🖼️",
		"application/vnd.oasis.opendocument.formula": "🧮",
		"application/vnd.oasis.opendocument.image": "🖼️",
		"application/vnd.oasis.opendocument.chart": "📈",
		"application/vnd.oasis.opendocument.text": "📑",
		"application/oda": "📑",


		# Scripts
		"application/vnd.mozilla.xul+xml": "🦊",
		"application/x-iso9660-image": "💿",
		"application/x-shellscript": "🐚",
		"application/manifest+json": "📑",
		"application/javascript": "📜",
		"application/ecmascript": "📜",
		"application/x-ruby": "💎",
		"application/x-perl": "🐪",
		"application/x-php": "🐘",
		"application/x-tar": "🗃️",
		"application/x-msi": "📦",
		"application/x-apk": "📱",
		"application/x-deb": "🐧",
		"application/x-rpm": "📦",
		"application/x-cab": "🗄️",
		"application/json": "📑",
		"application/x-xz": "🗜️",

		"text/x-shellscript": "🐚",
		"text/x-msdos-batch": "🛞",
		"text/javascript": "⚡",
		"text/x-python": "🐍",
		"text/x-perl": "🐫",
		"text/x-ruby": "💎",
		"text/x-java": "☕",
		"text/x-rust": "🦀",
		"text/x-c++": "🔵",
		"text/x-php": "🐘",
		"text/x-go": "🐹",
		"text/css": "✨",
		"text/csv": "📊",
		"text/xml": "📑",
		"text/x-c": "🔵",


		# Models

		# Fonts
		"application/vnd.ms-fontobject": "🔤",
		"application/vnd.font-fontforge-sfd": "🔤",
		"font/woff2": "🔠",
		"font/woff": "🔠",


		# Applications

		# archives
		"application/x-python-bytecode": "🐍",
		"application/x-zip-compressed": "🗜️",
		"application/x-rar-compressed": "🗜️",
		"application/x-7z-compressed": "🗜️",
		"application/java-archive": "☕",
		"application/x-compressed": "🗜️",
		"application/vnd.rar": "🗜️",
		"application/x-bzip2": "🗜️",
		"application/x-lzip": "🗜️",
		"application/x-lzma": "🗜️",
		"application/x-gzip": "🗜️",
		"application/x-bzip": "🗜️",
		"application/x-tar": "📦",
		"application/x-xar": "🗜️",
		"application/gzip": "🗜️",
		"application/zip": "🗜️",




		# shell
		"application/vnd.microsoft.portable-executable": "🚀",
		"application/x-ms-dos-executable": "🔨",
		"application/x-msdownload": "🚀",
		"application/x-executable": "🛞",
		"application/x-dosexec": "📟",


		# Miscellaneous
		"application/vnd.google-earth.kml+xml": "🗺️",
		"application/windows-library+xml": "📚",
		"application/x-shockwave-flash": "⚡",
		"application/vnd.apple.mpegurl": "📻",
		"application/x-pn-realaudio": "🎧",
		"application/x-python-code": "🐍",
		"application/x-wais-source": "🌐",
		"application/x-ms-shortcut": "🔗",
		"application/x-troff-man": "📖",
		"application/pkcs7-mime": "🔐",
		"application/x-mswinurl": "🌐",
		"application/postscript": "🖌️",
		"application/x-troff-me": "📜",
		"application/x-troff-ms": "📜",
		"application/x-dos-exec": "🚀",
		"application/n-triples": "📊",
		"application/x-sqlite3": "🗃️",
		"application/x-sv4cpio": "📦",
		"application/x-texinfo": "📖",
		"application/x-netcdf": "🌐",
		"application/x-pkcs12": "🔒",
		"application/x-sv4crc": "📦",
		"application/n-quads": "📊",
		"application/x-bcpio": "📦",
		"application/x-latex": "📜",
		"application/x-troff": "📜",
		"application/x-ustar": "📦",
		"application/x-gtar": "📦",
		"application/x-cpio": "📦",
		"application/x-hdf5": "💾",
		"application/x-shar": "📦",
		"application/x-csh": "🐚",
		"application/x-dvi": "📜",
		"application/x-mif": "📄",
		"application/x-hdf": "💾",
		"application/x-tar": "📦",
		"application/x-tcl": "📜",
		"application/x-tex": "📜",
		"application/x-sh": "🐚",
		"application/trig": "📊",
		"application/wasm": "⚙️",

		"application/octet-stream": "💾",
		"message/rfc822": "✉️",
		"inode/x-empty": "🫙",


		# Fallback
		"application": "💼",
		"message": "✉️",
		"video": "🎬",
		"image": "🖼️",
		"audio": "🎵",
		"inode": "❓",
		"model": "🏗️",
		"font": "🔤",
		"text": "📄",

		# Unknown
		"Unknown": "❓",

		# Error
		"OSError": f"{RED}❌{RESET}"
	}
	for key, icon in icons.items():
		if mime_type and key.strip().lower() in mime_type.strip().lower():
			return icon

	# Regex Search, added soon

	# If no icon was found, return a default icon
	return "📃"

def get_folder_icon(path):

	"""
	Returns an emoji icon for the given folder name/path.

	Args:
		path: The folder name/path to get the icon for.

	Returns:
		A string containing an emoji icon representing the folder, or "📁" if no icon was found.
	"""
	folder_name = path.split('/')[-1].split('\\')[-1]
	if folder_name == '':
		folder_name = path.split('/')[-2].split('\\')[-1]

	icons = {
		"System Volume Information": "💽",

		# Windows / Android
		"Alarms": "⏰",
		"Android": "🤖",
		"Android": "📱",
		"Audiobooks": "🔉",
		"Desktop": "🖥️",
		"DCIM": "📸",
		"Downloads": "📥",
		"Download": "📥",
		"Documents": "📄",
		"Document": "📄",
		"Movies": "🎥",
		"Movie": "🎥",
		"Music": "🎵",
		"Notifications": "🔔",
		"Pictures": "🖼️",
		"Picture": "🖼️",
		"Podcasts": "🎧",
		"Recordings": "🎤",
		"Recording": "🎤",
		"Ringtones": "📞",
		"Videos": "🎬",
		"Video": "🎬",

		# Unix-like
		"bin": "📦",
		"boot": "🏁",
		"dev": "🔌",
		"etc": "🛞",
		"home": "🏠",
		"lib": "📚",
		"media": "💾",
		"mnt": "🖴",
		"opt": "🏗",
		"proc": "📊",
		"root": "👑",
		"run": "🚀",
		"sbin": "🛠",
		"srv": "🌐",
		"sys": "🖧",
		"tmp": "🧹",
		"usr": "🖥",
		"var": "📜",

		# MacOS
		"Applications": "📱",
		"Library": "📚",
		"Data": "📦",
		"Volumes": "🖴",
		"private": "🔒",
		"System": "🏢",
		"Network": "🌐",
		
		# Windows
		"$Recycle.Bin": "♻️",
		".thumbnails": "📌",
		"3D Objects": "🧊",
		"Administrative Tools": "🔧",
		"AppData": "📚",
		"Camera Roll": "📸",
		"Captures": "🎥",
		"Contacts": "👥",
		"Cookies": "🍪",
		"Common Files": "📦",
		"Documents and Settings": "🏚️",
		"Favorites": "🩷",
		"Fonts": "🔤",
		"FileHistory": "🕰️",
		"Program Files": "💻",
		"Program Files (x86)": "💻",
		"ProgramData": "📦",
		"Windows": "🪟",
		"Windows.old": "🧹",
		"Links": "🔗",
		"Local Settings": "🪛",
		"Libraries": "📚",
		"My Documents": "📄",
		"My Pictures": "🖼️",
		"My Music": "🎵",
		"My Videos": "🎬",
		"Media": "🔉",
		"NetHood": "📡",
		"OneDrive": "☁️",
		"Offline Web Pages": "🌐",
		"Programs": "💻",
		"PrintHood": "🖨️",
		"Saved Games": "🎮",
		"Searches": "🔎",
		"Recent": "👀",
		"Recovery": "🛡",
		"System32": "🏛️",
		"Screenshots": "📸",
		"StartUp": "🚀",
		"SendTo": "📤",
		"Start Menu": "🪟",
		"Templates": "🎭",
		"Temp": "❄️",
		"Users": "🏠",


		# Cloud Storage
		"Dropbox": "📦",
		"Google Drive": "🚘",

		# Projects
		"__pycache__": "🐍",
		".env": "🌱",
		".github": "🐱",
		".git": "📓",
		".history": "🕰️",
		".lib": "📚",
		".temp": "❄️",
		".venv": "🏞️",
		".vscode": "🆚",
		"assets": "📦",
		"build": "🏗️",
		"configs": "🔧",
		"cache": "🧹",
		"docs": "📄",
		"dist": "🎁",
		"font": "🔤",
		"fonts": "🔤",
		"git": "📓",
		"history": "🕰️",
		"include": "➕",
		"icon": "📌",
		"icons": "📌",
		"javascript": "⚡",
		"js": "⚡",
		"locales": "🗣️",
		"log": "🧾",
		"logs": "🧾",
		"lang": "🗣️",
		"langs": "🗣️",
		"models": "🧠",
		"node_modules": "🐢",
		"notebook": "📓",
		"notebooks": "📓",
		"python": "🐍",
		"rust": "®️",
		"src": "📜",
		"script": "📜",
		"scripts": "📜",
		"test": "🧪",
		"tests": "🧪",
		"text": "📝",
		"texts": "📝",
		"textures": "🎨",
		"uploads": "📤",
		"util": "🛠",
		"venv": "🏞️",
		"workflows":"🤖"


	}
	for key, icon in icons.items():
		if folder_name.lower() == key.lower():
			return icon
	return "📁"

def get_mime_type(file_path, max_size, force_magic, use_magika):  # Limit MIME detection for files <= 10MB
	"""
	Get mime type of a file. If the file size is greater than 10MB, the mime type is determined by the file extension.
	If the file size is less than 10MB, the mime type is determined by the file extension first, if the mime type is unknown or common, use magic to detect the mime type deeply.

	Args:
		file_path (str): Path to the file
		max_size (int, optional): Limit of file size to use magic for deep search. Defaults to 1 * 1024 * 1024 (10MB)

	Returns:
		str: Mime type of the file
	"""
	global magic_scanned
	try:
		# First, get mime type by extension
		mime = mimetypes.guess_type(file_path)[0]
		# if file size is greater than threshold, never use magic to prevent disk overload
		if max_size > os.path.getsize(file_path): 
			# If mime type is unknown or common, use magic for deep search
			if (mime == None or mime == '' or mime == "application/octet-stream" or mime == "text/plain") or force_magic: # If mime type is too common, or forced to use magic
				try:
					if use_magika and "magika" in sys.modules: # If using magika
						mime = m.identify_path(pathlib.Path(file_path)).output.mime_type
						if use_magika:
							magic_scanned += 1
					elif use_magika and "magic" in sys.modules: # If not using magika
						mime = magic.from_file(file_path, mime=True)
						if not use_magika:
							magic_scanned += 1
				except Exception as e: # if magic failed, return mimetypes: last resort
					magic_scanned -= 1
					logging.debug(f"{colored_warn} {e}")
					mime = mimetypes.guess_type(file_path)[0]
					logging.debug(f"{colored_warn} falling back: {e}; {mime}")
				if mime == None or mime == '': # if magic failed, return mimetypes: last resort
					mime = mimetypes.guess_type(file_path)[0]

		logging.debug(f"{file_path} mime detail searched: {mime}")
		if mime == None or mime == '':
			return "Unknown"
		else:
			return mime
	except Exception as x:
		logging.warning(x)
		return f"[{type(x).__name__}]: {x}"
def get_file_attributes(file_path):
	"""Get attributes of a file."""
	attributes = []
	try:
		file_stat = os.stat(file_path)
		if file_stat.st_file_attributes & stat.FILE_ATTRIBUTE_ARCHIVE:
			attributes.append("Archive")
		if file_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN:
			attributes.append("Hidden")
		if file_stat.st_file_attributes & stat.FILE_ATTRIBUTE_READONLY:
			attributes.append("Read-only")
		if file_stat.st_file_attributes & stat.FILE_ATTRIBUTE_SYSTEM:
			attributes.append("System")
		if file_stat.st_file_attributes & stat.FILE_ATTRIBUTE_COMPRESSED:
			attributes.append("Compressed")
		if file_stat.st_file_attributes & stat.FILE_ATTRIBUTE_ENCRYPTED:
			attributes.append("Encrypted")
	except AttributeError:
		pass  # Attributes not available on some OS
	except Exception as e:
		error_logs.append({"name": file_path, "type": str(type(e).__name__), "desc": str(e)})
		pass
	return attributes

def update_progress(total_files, use_magika):
	"""Updates the progress bar in a thread-safe way."""
	global progress
	with progress_lock:
		progress += total_files
		progress_bar.update(total_files)
		progress_bar.set_description(f"🕷️ | {'🪄 Magika' if use_magika else '🔮 Magic'}: {magic_scanned} | 📏 Total: {humanize.naturalsize(sum_size, binary=True)}")


def get_folder_structure_threaded(path, progress_bar=None, error_logs=None, no_attributes=False, max_workers=10, magic_max_size=1 * 1024 * 1024, force_magic=False, use_magika=False):
	"""Scans a directory structure efficiently with threading and shows progress."""
	global progress, sum_size
	tree = []
	total_size = 0
	scanned_files = 0
	scanned_folders = 0
	denied_folders = 0

	try:
		entries = list(os.scandir(path))
	except Exception as e:
		denied_folders += 1
		if error_logs is not None:
			error_logs.append({"name": path, "type":str(type(e).__name__), "desc": str(e)})
			sys.stdout.write(f"\n")
			if logger.isEnabledFor(logging.DEBUG):
				traceback.print_exc(file=sys.stdout)
			logging.debug(e)
			if "PermissionError" in type(e).__name__:
				logging.warning(f"{colored_no_entry} Permission denied: '{GREY}{path}{RESET}'")
			elif "OSError" in type(e).__name__:
				logging.warning(f"🚫 Access error: '{GREY}{path}{RESET}'")
			elif "FileNotFoundError" in type(e).__name__:
				logging.warning(f"❔ File not found: '{GREY}{path}{RESET}'")
			elif "IsADirectoryError" in type(e).__name__: # Skip junctions
					logging.warning(f"🛤️ Junction skipped: '{GREY}{path}{RESET}'")
			elif "NotADirectoryError" in type(e).__name__:
				logging.warning(f"🚧 Not a directory: '{GREY}{path}{RESET}'")
			elif "FileExistsError" in type(e).__name__: # Skip symbolic links
				logging.warning(f"🔗 Symbolic link skipped: '{GREY}{path}{RESET}'")
			else:
				logging.warning(f"{colored_x} Error: '{GREY}{path}{RESET}' due to {e}")

			tree.append({
				"name": os.path.basename(path), # Folder name
				"path": path,
				"type": "folder", # whether it is 'folder' or 'file'
				"size": 0, # folder size in bytes
				"attr": get_file_attributes(path) if not no_attributes else None, # folder attributes
				"mtime": os.path.getmtime(path), # folder modification time
				"ctime": os.path.getctime(path), # folder creation time
				"atime": os.path.getatime(path), # folder access time
				"files": 0, # number of files
				"folders": 0, # number of subfolders
				"access_denied": type(e).__name__, # whether access is denied
				"children": [], # folder structure
			})
		return tree, 0, 0, 0, 1


	future_results = []
	with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
		for entry in entries:
			entry_name = entry.name  # Store entry name to prevent race conditions
			entry_path = entry.path 
			entry_stat = entry.stat(follow_symlinks=False)
			if entry.is_symlink():
				tree.append({
					"name": entry_name, 
					"path": entry_path, 
					"type": "symlink",
					"target": os.readlink(entry_path), 
					"attr": get_file_attributes(entry.path) if not no_attributes else None,
					"size": 0,
					"mtime": entry_stat.st_mtime,
					"ctime": entry_stat.st_ctime,
					"atime": entry_stat.st_atime,
				})
			elif entry.is_file(follow_symlinks=False):
				try:
					file_stat = entry.stat()
					file_size = file_stat.st_size
					sum_size += file_size
					mime_type = get_mime_type(entry_path, magic_max_size, force_magic, use_magika)
					tree.append({
						"name": entry_name,
						"path": entry_path,
						"type": "file",
						"mime": mime_type,
						"size": file_size, 
						"attr": get_file_attributes(entry.path) if not no_attributes else None,
						"mtime": file_stat.st_mtime,
						"ctime": file_stat.st_ctime, 
						"atime": file_stat.st_atime,
					})
				except Exception as e:
					error_logs.append({"name": path, "type": str(type(e).__name__), "desc": str(e)})
					if args.verbose:
						traceback.print_exc(file=sys.stdout)
					logging.warning(e)
					tree.append({
						"name": entry_name,
						"path": entry_path,
						"type": "file",
						"mime": str(type(e).__name__),
						"size": 0, 
						"attr": get_file_attributes(entry.path) if not no_attributes else None,
						"mtime": 0,
						"ctime": 0, 
						"atime": 0,
					})
				total_size += file_size
				scanned_files += 1
			elif entry.is_dir(follow_symlinks=False):
				future = executor.submit(get_folder_structure_threaded, entry_path, progress_bar, error_logs, no_attributes, max_workers, magic_max_size, force_magic, use_magika)
				future_results.append((future, entry_name, entry_path))  # Store folder name & path safely
				scanned_folders += 1

		# Update progress
		update_progress(scanned_files, use_magika)

		for future, folder_name, folder_path in future_results:
			try:
				children, child_size, child_files, child_folders, denied_folders	 = future.result()
				total_size += child_size
				scanned_files += child_files
				scanned_folders += child_folders
				entry_stat = entry.stat(follow_symlinks=False)
				tree.append({
					"name": folder_name, 
					"path": folder_path, 
					"type": "folder",
					"size": child_size, 
					"attr": get_file_attributes(folder_path) if not no_attributes else None,
					"mtime": entry_stat.st_mtime,
					"ctime": entry_stat.st_ctime,
					"atime": entry_stat.st_atime,
					"files": child_files,
					"folders": child_folders, 
					"access_denied": False,
					"children": children,
				})
			except Exception as e:
				error_logs.append({"name": path, "type":str(type(e).__name__), "desc": str(e)})
				sys.stdout.write(f"\n")
				if args.verbose:
					traceback.print_exc(file=sys.stdout)
				logging.debug(e)
				if "PermissionError" in type(e).__name__:
					logging.warning(f"{colored_no_entry} Permission denied: '{GREY}{path}{RESET}'")
				elif "OSError" in type(e).__name__:
					logging.warning(f"🚫 Access error: '{GREY}{path}{RESET}'")
				elif "FileNotFoundError" in type(e).__name__:
					logging.warning(f"❔ File not found: '{GREY}{path}{RESET}'")
				elif "IsADirectoryError" in type(e).__name__: # Skip junctions
					logging.warning(f"🛤️ Junction skipped: '{GREY}{path}{RESET}'")
				elif "NotADirectoryError" in type(e).__name__:
					logging.warning(f"🚧 Not a directory: '{GREY}{path}{RESET}'")
				elif "FileExistsError" in type(e).__name__: # Skip symbolic links
					logging.warning(f"🔗 Symbolic link skipped: '{GREY}{path}{RESET}'")
				else:
					logging.warning(f"{colored_x} Error: '{GREY}{path}{RESET}' due to {e}")

				tree.append({
					"name": folder_name, # Folder name
					"path": folder_path,
					"type": "folder", # whether it is 'folder' or 'file'
					"size": 0, # folder size in bytes
					"attr": get_file_attributes(folder_path) if not no_attributes else None, # folder attributes
					"mtime": entry_stat.st_mtime, # folder modification time
					"ctime": entry_stat.st_ctime, # folder creation time
					"atime": entry_stat.st_atime, # folder access time
					"files": 0, # number of files
					"folders": 0, # number of subfolders
					"access_denied": type(e).__name__, # whether access is denied
					"children": [], # folder structure
				})

	return tree, total_size, scanned_files, scanned_folders, denied_folders

def get_folder_structure(path, progress_bar=None, error_logs=None, no_attributes=False, magic_max_size = 1 * 1024 * 1024, force_magic=False, use_magika=False):
	"""
	Get the folder structure of a given path.

	Args:
		path (str): The path to get the folder structure of.
		progress_bar (tqdm.tqdm): The progress bar to update.

	Returns:
		A tuple containing the folder structure, the total size of the folder, the number of files in the folder, and the number of subfolders in the folder.
	"""
	tree = []
	total_size = 0
	global scanned_folders, scanned_files, sum_size, denied_folders

	entries = list(os.scandir(path))
	for entry in entries:
		if progress_bar:
			progress_bar.update(1)
			dyn_tqdm.set_description(f"🕵️ | {'🪄 Magika' if use_magika else '🔮 Magic'}: {magic_scanned} | 📏 Total: {humanize.naturalsize(sum_size, binary=True)} ")
			
			attributes = get_file_attributes(entry.path) if not no_attributes else None
			'''if entry.is_junction(): # path is a junction
				tree.append({
					"name": entry.name, # Junction name
					"path": entry.path,
					"type": "junction", # whether it is 'folder' or 'file'
					"attr": get_file_attributes(entry.path), # junction attributes
					"size": 0, # junction size in bytes
					"mtime": entry.stat(follow_symlinks=False).st_mtime, # junction modification time
					"ctime": entry.stat(follow_symlinks=False).st_ctime, # junction creation time
					"atime": entry.stat(follow_symlinks=False).st_atime, # junction access time
				})'''
			
			if entry.is_symlink(): # path is a symbolic link
				tree.append({
					"name": entry.name, # Symbolic link name
					"path": entry.path,
					"type": "symlink", # whether it is 'folder' or 'file'
					"target": os.readlink(entry.path),
					"attr": attributes, # symbolic link attributes
					"size": 0, # symbolic link size in bytes
					"mtime": entry.stat(follow_symlinks=False).st_mtime, # symbolic link modification time
					"ctime": entry.stat(follow_symlinks=False).st_ctime, # symbolic link creation time
					"atime": entry.stat(follow_symlinks=False).st_atime, # symbolic link access time
				})
			elif entry.is_dir(follow_symlinks=False): # path is a directory
				try:
					children, child_size, child_files, child_folders, denied_folders = get_folder_structure(entry.path, progress_bar, magic_max_size=magic_max_size, force_magic=force_magic, use_magika=use_magika)
					scanned_folders += 1
					total_size += child_size
					tree.append({
						"name": entry.name, # Folder name
						"path": entry.path,
						"type": "folder", # whether it is 'folder' or 'file'
						"size": child_size, # folder size in bytes
						"attr": attributes, # folder attributes
						"mtime": entry.stat(follow_symlinks=False).st_mtime, # folder modification time
						"ctime": entry.stat(follow_symlinks=False).st_ctime, # folder creation time
						"atime": entry.stat(follow_symlinks=False).st_atime, # folder access time
						"files": child_files, # number of files
						"folders": child_folders, # number of subfolders
						"access_denied": False, # whether access is denied
						"children": children, # folder structure
					})
				except Exception as e:
					denied_folders += 1
					error_logs.append({"name": path, "type":str(type(e).__name__), "desc": str(e)})
					sys.stdout.write(f"\n")
					if logger.isEnabledFor(logging.DEBUG):
						traceback.print_exc(file=sys.stdout)
					logging.debug(e)
					if "PermissionError" in type(e).__name__:
						logging.warning(f"{colored_no_entry} Permission denied: '{GREY}{path}{RESET}'")
					elif "OSError" in type(e).__name__:
						logging.warning(f"{colored_no_entry} Access error: '{GREY}{path}{RESET}'")
					elif "FileNotFoundError" in type(e).__name__:
						logging.warning(f"❔ File not found: '{GREY}{path}{RESET}'")
					elif "IsADirectoryError" in type(e).__name__: # Skip junctions
						logging.warning(f"🛤️ Junction skipped: '{GREY}{path}{RESET}'")
					elif "NotADirectoryError" in type(e).__name__:
						logging.warning(f"🚧 Not a directory: '{GREY}{path}{RESET}'")
					elif "FileExistsError" in type(e).__name__: # Skip symbolic links
						logging.warning(f"🔗 Symbolic link skipped: '{GREY}{path}{RESET}'")
					else:
						logging.warning(f"{colored_x} Error: '{GREY}{path}{RESET}' due to {e}")

					tree.append({
						"name": entry.name, # Folder name
						"path": entry.path,
						"type": "folder", # whether it is 'folder' or 'file'
						"size": 0, # folder size in bytes
						"attr": attributes, # folder attributes
						"mtime": entry.stat(follow_symlinks=False).st_mtime, # folder modification time
						"ctime": entry.stat(follow_symlinks=False).st_ctime, # folder creation time
						"atime": entry.stat(follow_symlinks=False).st_atime, # folder access time
						"files": 0, # number of files
						"folders": 0, # number of subfolders
						"access_denied": type(e).__name__, # whether access is denied
						"children": [], # folder structure
					})
					pass  # Skip folders where permission is denied


			elif entry.is_file(follow_symlinks=False): # path is a file
				try:
					file_size = entry.stat().st_size
					total_size += file_size	
					# mime_type, _ = mimetyp	es.guess_type(entry.path)
					mime_type = get_mime_type(entry.path, magic_max_size, force_magic, use_magika)
					
					tree.append({
						"name": entry.name, # File name
						"path": entry.path,
						"type": "file", # whether it is 'folder' or 'file'
						"mime": mime_type, # mime type
						"size": file_size, # file size in bytes
						"attr": attributes, # file attributes
						"mtime": entry.stat().st_mtime, # last modified time
						"ctime": entry.stat().st_ctime, # creation time
						"atime": entry.stat().st_atime, # last accessed time
					})
				except Exception as e:
					error_logs.append({"name": path, "type": str(type(e).__name__), "desc": str(e)})
					if args.verbose:
						traceback.print_exc(file=sys.stdout)
					logging.warning(e)
					tree.append({
						"name": entry.name,
						"path": entry.path,
						"type": "file",
						"mime": str(type(e).__name__),
						"size": 0, 
						"attr": get_file_attributes(entry.path) if not no_attributes else None,
						"mtime": 0,
						"ctime": 0, 
						"atime": 0,
					})
				scanned_files += 1
				total_size += file_size
				sum_size += file_size
	return tree, total_size, scanned_files, scanned_folders, denied_folders

def save_json_tree(path_to_scan, output_file="folder_structure.json.bz2", simulate=False, no_attributes=False, magic_max_size=1 * 1024 * 1024, use_threads=False, force_magic=False, no_estimates=False, use_magika=False):

	"""
	Save the folder structure of a given path as a compressed JSON file.

	This function scans the specified directory path, gathers its folder structure,
	and saves it as a compressed JSON file with metadata such as the total size,
	number of files, and number of folders. The user can choose to simulate the save
	operation without writing the file.

	Args:
		path (str): The directory path to scan and save the structure from.
		output_file (str, optional): The output file path for the compressed JSON.
			Defaults to "folder_structure.json.bz2".
		simulate (bool, optional): If True, simulates the save operation without
			writing the file. Defaults to False.

	Raises:
		KeyboardInterrupt: If the operation is interrupted by the user.
	"""

	start_time = time.time()
	absolute_path = os.path.abspath(path_to_scan)
	# total_items = sum([len(files) + len(dirs) for _, dirs, files in tqdm(os.walk(path_to_scan), desc="🥷 Scanning Directories", unit=" dir", smoothing=1.0)])
	# Calculate total items

	def count_items_in_directory(directory):
		"""Count total items (files and subdirectories) in a directory."""
		try:
			return len(os.listdir(directory))  # Count files and subdirectories
		except PermissionError:
			return 0  # Skip directories we don't have permission to access
		except FileNotFoundError:
			return 0  # Skip directories that don't exist

	def count_items_concurrently(base_directory):
		"""Count items in a directory and subdirectories using threads."""
		total_items = 0
		dyn_tqdm_walk = tqdm(os.walk(base_directory),desc="🐍 Calculate total items", unit=" dirs", smoothing=1.0)
		with ThreadPoolExecutor() as executor:
			# Get a list of subdirectories and files
			timeStart_walk = time.time()
			for dirpath, _, _ in dyn_tqdm_walk:
				future = executor.submit(count_items_in_directory, dirpath)
				total_items += future.result()  # Wait for result and add to total
				search_rate = f"{(total_items / (time.time() - timeStart_walk)):.2f}"
				dyn_tqdm_walk.set_description(f"🐍 Calculate total items | 📃 {total_items} files | {'⚡' if float(search_rate) > 20000 else '🚀' if float(search_rate) > 10000 else '🔥'} {search_rate} files/s")

		return total_items

	if not no_estimates:
		if False: #use_threads:
			total_items = count_items_concurrently(path_to_scan)
		else:
			print("🥷 Calculating total items...")
			dyn_tqdm_walk = tqdm(os.walk(path_to_scan),desc="🥷 Calculate total items", unit=" dirs", smoothing=1.0)
			total_items = []
			dirs_count = 0
			files_count = 0
			search_rate = 0
			avg_dir = 0
			timeStart_walk = time.time()
			for _, _, files in dyn_tqdm_walk:
				dyn_tqdm_walk.set_description(f"🥷 | 📊 {avg_dir:.1f} files/dir | 📃 {files_count} files | {'⚡' if float(search_rate) > 20000 else '☄️' if float(search_rate) > 10000 else '🚀' if float(search_rate) > 5000 else '🔥' if float(search_rate) > 2000 else '❄️' if float(search_rate) > 1000 else '⛄'} {search_rate} files/s")
				dirs_count += 1
				for _ in files:
					files_count += 1
					try:
						search_rate = f"{(files_count / (time.time() - timeStart_walk)):.2f}"
						avg_dir = files_count / dirs_count
					except ZeroDivisionError:
						search_rate = 0
						avg_dir = 0
			
			total_items = dirs_count + files_count
	else:
		total_items = 0	

	global dyn_tqdm, scanned_files, scanned_folders, sum_size, denied_folders
	scanned_files = 0
	scanned_folders = 0
	denied_folders = 0
	sum_size = 0
	try:
		if use_threads:
			title(f"🕸️ Scanning... - Tree Spider")
			print("🕷️ Scanning files...")
			print("🧵 Using threads... (Progress bar may not work properly)")
			global progress, progress_lock, progress_bar
			progress_lock = threading.Lock()
			progress = 0
			with tqdm(total=total_items, desc="🕷️ Scanning files...", unit="files") as progress_bar:
				structure, total_size, scanned_files, scanned_folders, denied_folders = get_folder_structure_threaded(path_to_scan, progress_bar=progress_bar, error_logs=error_logs, no_attributes=no_attributes, magic_max_size=magic_max_size, force_magic=force_magic, use_magika=use_magika)
		else:
			title(f"📈 Scanning... - Tree Spider")
			print("🕵️ Scanning files...")
			dyn_tqdm = tqdm(total=total_items,  unit=" files", smoothing=1.0)
			with dyn_tqdm as progress_bar:
				structure, total_size, scanned_files, scanned_folders, denied_folders = get_folder_structure(path_to_scan, progress_bar=progress_bar, error_logs=error_logs, no_attributes=no_attributes, magic_max_size=magic_max_size, force_magic=force_magic, use_magika=use_magika)
	except KeyboardInterrupt:
		print(f"{colored_stop} Aborted.")
		exit(0)
	end_time = time.time()

	print(f"\n📋 Results\n")
	print(f" 📄 Total Files: {humanize.intcomma(scanned_files)} | 📂 Total Folders: {humanize.intcomma(scanned_folders)} | 📏 Total Size: {humanize.naturalsize(total_size, binary=True)}")
	print(f" ⏱️ Time Taken: {format_duration(end_time - start_time)}\n")

	title(f"📝 Enter a note - Tree Spider")
	if not args.simulate and timed_choice("📝 Enter a note for the report? ", 10, False):
			# not a command, so input prompts is pilcrow
			try:
				user_note = input("¶ ")
			except KeyboardInterrupt:
				user_note = ""
	else:
		user_note = ""
		print("⏭️ Skipped. You can edit the note later.")

	try:
		partition = get_partition_from_path(absolute_path).fstype
	except Exception as p:
		error_logs.append({"name":"partition", "type":str(type(p).__name__), "desc": str(p)})
		partition = str(type(p).__name__)
	
	data = { # metadata
		"user_note": user_note,
		"error_logs": error_logs,
		"original_path": absolute_path,
		"start_time": start_time,
		"end_time": end_time,
		"partition": partition,
		"total_size": total_size,
		"scanned_files": scanned_files,
		"scanned_folders": scanned_folders,
		"denied_folders": denied_folders,
		"magic_max_size": magic_max_size,
		"use_magika": use_magika,
		"force_magic": force_magic,
		"magic_scanned": magic_scanned,
		"computer_name": platform.node(),
		"system_name": platform.system(),
		"system_ver": platform.version(),
		"machine_type": platform.machine(),
		"machine_arch": platform.architecture()[0],
		"disk_usage": shutil.disk_usage(path_to_scan),
		"root_mtime": os.path.getmtime(path_to_scan),
		"root_ctime": os.path.getctime(path_to_scan),
		"root_atime": os.path.getatime(path_to_scan),
		"root_attr": get_file_attributes(path_to_scan),
		"threaded": use_threads,
		"structure": structure,
	}

	if simulate:
		print(f"⏭️ Skipping writing file...")
	else:	
		title(f"🗜️ Compressing JSON... - Tree Spider")
		print(f"\n🗜️ Compressing JSON...")
		spinner = Spinner()
		spinner.start() # small spinner animation, but works well
		try:
			compressed_data = bz2.compress(json.dumps(data, indent=4).encode('utf-8'))
			with open(output_file, 'wb') as f_out:
				f_out.write(compressed_data)
		except KeyboardInterrupt:
			print(f"{colored_stop} Interrupted by user.")
		finally:
			spinner.stop()
			print(f"📦 JSON has compressed by {round(os.path.getsize(output_file) / get_size_of(data) * 100, 2)} % | {humanize.naturalsize(get_size_of(data), binary=True)} ({humanize.intcomma(get_size_of(data))} bytes) -> {humanize.naturalsize(os.path.getsize(output_file), binary=True)} ({humanize.intcomma(os.path.getsize(output_file))} bytes) ")
	
	return end_time - start_time # return time taken
def get_top_n_largest_files(node, n, files=None):
	""" Get the top n largest files in a directory tree."""
	if files == None:
		files = []
	for item in node:
		if item["type"] == "file" or item["type"] == "symlink" or item["type"] == "junction":
			files.append(item)
		elif item["type"] == "folder":
			get_top_n_largest_files(item["children"], n, files)
	return sorted(files, key=lambda x: x["size"], reverse=True)[:n]

def get_top_n_large_folders(node, n, folders=None):	
	""" Get the top n largest folders in a directory tree."""
	if folders == None:
		folders = []
	
	for item in node:
		if item["type"] == "folder":
			folders.append(item)
			get_top_n_large_folders(item["children"], n, folders)
		elif item["type"] == "file" or item["type"] == "symlink" or item["type"] == "junction":
			pass
	return sorted(folders, key=lambda x: x["size"], reverse=True)[:n]

def get_top_n_recent_files(node, n, files=None, mode="new", key="mtime"):
	""" Get the top n recent files in a directory tree."""
	if files == None:
		files = []
	for item in node:
		if item["type"] == "file" or item["type"] == "symlink" or item["type"] == "junction":
			files.append(item)
		elif item["type"] == "folder":
			get_top_n_recent_files(item["children"], n, files, mode, key)
	if mode == "new":
		return sorted(files, key=lambda x: x[key], reverse=True)[:n]
	elif mode == "old":
		return sorted(files, key=lambda x: x[key])[:n]
	else:
		return sorted(files, key=lambda x: x[key], reverse=True)[:n]

def search_empty_folders(node, results=None):
	""" Search for empty folders in a directory tree."""
	if results == None:
		results = []
	for item in node:
		if item["type"] == "folder" and len(item["children"]) == 0:
			results.append(item)
		if item["type"] == "folder": # recursive
			search_empty_folders(item["children"], results)
	return results

def search_files(node, query, results=None):
	""" Search for files in a directory tree."""
	if results == None:
		results = []
	for item in node:
		if query.lower() in item["name"].lower():
			results.append(item)
		if item["type"] == "folder": # recursive
			search_files(item["children"], query, results)
	return results

def search_files_regex(node, query, results=None):
	""" Search for files in a directory tree."""
	if results == None:
		results = []
	for item in node:
		if re.search(query, item["name"]):
			results.append(item)
		if item["type"] == "folder": # recursive
			search_files_regex(item["children"], query, results)
	return results

def search_duplicates(node, file_map=None):
	"""Search for duplicate files in a directory tree based on name and size."""
	if file_map is None:
		file_map = defaultdict(list)  # Dictionary to store files by (name, size)
	
	for item in node:
		if item["type"] == "file":
			key = (item["name"], item["size"])
			file_map[key].append(item)
		elif item["type"] == "folder":  # Recursive call for subdirectories
			search_duplicates(item["children"], file_map)
	
	# Return only duplicate files (i.e., keys with more than one entry)
	return {k: v for k, v in file_map.items() if len(v) > 1}


def get_most_common_file_extensions(node, mode="freq", extensions=None, total_size=None, total_files=None):
	""" Get the top frequent extensions and sizes in a directory tree."""
	if extensions is None:
		extensions = {} # store extensions
	if total_size is None:
		total_size = sum([item["size"] for item in node if item["type"] == "file"])
	if total_files is None:
		total_files = len([item for item in node if item["type"] == "file"])
	
	for item in node:
		if item["type"] == "file":
			extension = os.path.splitext(item["name"])[1]
			size = item["size"]
			# Append extension (frequency, sizes), sum sizes
			if extension in extensions:
				# increment frequency, add size, calculate percentage
				extensions[extension] = (extensions[extension][0] + 1), (extensions[extension][1] + size), (extensions[extension][1] / total_size), (extensions[extension][0] / total_files)
			else:
				extensions[extension] = (1, size, (size / total_size), (1 / total_files))
		elif item["type"] == "folder": # recursive search for files
			get_most_common_file_extensions(item["children"], mode, extensions, total_size, total_files)
	# Sort by frequency or size
	if mode == "name":
		return sorted(extensions.items(), key=lambda x: x[0])
	elif mode == "size":
		return sorted(extensions.items(), key=lambda x: x[1][1], reverse=True)
	elif mode == "freq":
		return sorted(extensions.items(), key=lambda x: x[1][0], reverse=True)
	else:
		return sorted(extensions.items(), key=lambda x: x[1][0], reverse=True)
	return extensions



def set_nth_list(lst, index, value):
	""" Set the value at the nth index in a list, expanding the list if needed.

	Args:
		lst (list): The list to modify.
		index (int): The index at which to place the value.
		value: The value to store at the specified index.

	Returns:
		None
	"""
	if index >= len(lst):
		lst.extend([None] * (index - len(lst) + 1))  # Expand list with None
	lst[index] = value  # Now it's safe to assign

def convert_markdown_with_external_css(md_text):
	"""
	Convert Markdown text to styled HTML with an external CSS.

	This function takes a Markdown text string as input and converts it to HTML. 
	The resulting HTML includes a style block to apply basic styling to tables, 
	headers, and other elements.

	Args:
		md_text (str): The Markdown text to be converted.

	Returns:
		str: The HTML representation of the Markdown text with applied styling.
	"""

	body = markdown.markdown(md_text, extensions=['tables'])
	style = """table {\n	border-collapse: collapse;\n	width: 100%;\n	will-change: transform;\n}\n
th, td {\n	border: 1px solid black;\n	padding: 8px;\n	text-align: left;\n}\n
th {\n	background-color: #f2f2f2;\n}"""
	styled_html = f"""<!DOCTYPE html>\n<meta charset="utf-8">\n<html>\n<head>\n<style>\n{style}\n</style>\n</head>\n<body>\n{body}\n</body>\n</html>"""
	return styled_html

def repl_str_for_path(path):
	""" Replace characters that cannot be used in a path."""
	return re.sub(r'[<>:"/\\|?*]', '_', path)


def save_result_as_markdown(result, output_file="result.md", query=""):
	""" Save a search result as a markdown file."""
	totalsize = sum([item['size'] for item in result])
	write_lines = []
	write_lines.append(f"# Search Result for '{query}'\n")
	write_lines.append(f"## Information\n")
	write_lines.append(f"| Item | Value |")
	write_lines.append(f"|------|-------|")
	write_lines.append(f"| 🔎 Search Query | {query} |")
	write_lines.append(f"| 📑 Report File | {json_file} |")
	write_lines.append(f"| 📈 Total Size | {humanize.naturalsize(totalsize, binary=True)} ({humanize.intcomma(totalsize)} byte{plural(totalsize)}) |")
	write_lines.append(f"| 📃 Total Files | {len(result)} |")
	write_lines.append(f"| 📂 Total Folders | {len([item for item in result if item['type'] == 'folder'])} |")
	write_lines.append(f"| 🔗 Total Links | {len([item for item in result if item['type'] == 'symlink'])} |")
	write_lines.append(f"| 📊 Total Items | {len(result)} |")
	
	write_lines.append(f"## Files\n")
	write_lines.append(f"| # | Name | Size | MIME | Path | Date Modified | Date Created | Date Accessed |")
	write_lines.append(f"|---|------|------|------|------|---------------|--------------|---------------|")
	for index, item in enumerate(result):
		write_lines.append(f"| {index + 1} | {item['name']} | {humanize.naturalsize(item['size'], binary=True)} | {item.get('mime', 'N/A')} | {item['path']} | {seconds_to_datetime(item['mtime'])} | {seconds_to_datetime(item['ctime'])} | {seconds_to_datetime(item['atime'])} |")
	
	# Write to file
	output_file = repl_str_for_path(output_file)
	with open(output_file, "w") as f:
		f.writelines("\n".join(write_lines))

def browse_json_tree(json_file):

	"""
	Open a JSON file that was created by the Tree Spider and browse
	through the structure with a text-based interface.

	Args:
		json_file (str): The path to the JSON file to open and browse.
	"""
	global error_message
	error_message = ""

	global dir_count, file_count
	dir_count = 0
	file_count = 0
	if not os.path.exists(json_file):
		raise FileNotFoundError(f"JSON file not found: {json_file}")

	title(f"⏳ Loading JSON... - Tree Spider")

	spinner = Spinner(char="emoji_moon2")
	spinner.start() # small spinner animation, but works well
	try:
		data = bz2_load_to_json(json_file)
		
		print("\n🧐 Parsing...")

		
		structure = data["structure"] # The most important part of the data

	except KeyboardInterrupt:
			print(f"{colored_stop} Interrupted by user.")
	finally:
		spinner.stop()
	
	# set last opened json
	config["tree_util"] = {"last_opened_json": json_file}
	with open(config_file, "w") as conf:
		config.write(conf)

	def decimal_bytes_to_bits(size, intcomma=False):
		"""
		Convert a decimal byte size to a string with both bytes and bits.

		Args:
			size (int or float): The size to convert.
			intcomma (bool, optional): If True, use humanize.intcomma to format the byte size with commas. Defaults to False.

		Returns:
			str: A string in the format "X byte(s) + Y bit(s)" if there are bits, otherwise "X byte(s)".
		"""
		if intcomma:
			byte = humanize.intcomma(int(size)) # math.floor(size)
		else:
			byte = int(size)
		bits = int((size - int(size))*8)
		return f"{byte} byte{plural(size)} + {bits} bit{plural(bits)}" if bits > 0 else f"{byte} byte{plural(size)}"
	
	def generate_report(data):
		""" Generate a report from the data.  """
		# Retrieve Report Info

		global original_path, disk_total, total_size
		report_size = len(str(data))
		report_bz2_size = os.path.getsize(json_file)
		disk_total = data.get('disk_usage')[0]
		disk_free = data.get('disk_usage')[2]
		disk_used = data.get('disk_usage')[1]
		disk_free_percentage = disk_free / disk_total * 100
		disk_used_percentage = disk_used / disk_total * 100
		partition_filesystem = data.get('partition')
		original_path = data.get("original_path").replace("\\", "/")
		elapsed_seconds = data.get('end_time') - data.get('start_time')
		total_size = data.get('total_size')
		try:
			average_size = disk_total / data.get('scanned_files')
		except ZeroDivisionError:
			average_size = 0

		# Generate Report
		global report_info
		report_info = []
		report_info.append(f"\n	🏷️ Report Info for {json_file}\n")
		report_info.append(f" Item			Value")
		report_info.append(f" ----			-----")
		report_info.append(f" 📅 Datetime:		{seconds_to_datetime(data.get('start_time'))} - {seconds_to_datetime(data.get('end_time'))}")
		report_info.append(f" ⏱️ Elapsed Time:	{format_duration(elapsed_seconds)}	({elapsed_seconds:.2f} second{plural(round(elapsed_seconds,1))})")
		report_info.append(f" 📑 Report Size:	{humanize.naturalsize(report_size, binary=True)}	({humanize.intcomma(report_size)} byte{plural(report_size)})")
		report_info.append(f" 🗜️ Compressed Size:	{humanize.naturalsize(report_bz2_size, binary=True)}	({humanize.intcomma(report_bz2_size)} byte{plural(report_bz2_size)})	[{report_bz2_size / report_size * 100:.2f} %]\n")
		report_info.append(f" 📍 Original Path:	{original_path}")
		report_info.append(f" 🖥️ Computer Name:	{data.get('computer_name')}")
		report_info.append(f" 🛰️ System Name:	{data.get('system_name')} {data.get('system_ver')} {data.get('machine_arch')}")
		report_info.append(f" 🏗️ Machine Type:	{data.get('machine_type')}\n")
		report_info.append(f" 🗃️ Disk Filesystem:	{partition_filesystem}")
		report_info.append(f" 💽 Disk Total:		{humanize.naturalsize(disk_total, binary=True)}	({humanize.intcomma(disk_total)} byte{plural(disk_total)})")
		report_info.append(f" 🈵 Disk Used:		{humanize.naturalsize(disk_used, binary=True)}	({humanize.intcomma(disk_used)} byte{plural(disk_used)})	[{disk_used_percentage:.2f} %]")
		report_info.append(f" 🈳 Disk Free:		{humanize.naturalsize(disk_free, binary=True)}	({humanize.intcomma(disk_free)} byte{plural(disk_free)})	[{disk_free_percentage:.2f} %]\n")
		report_info.append(f" 🔮 Magic max size:	{humanize.naturalsize(data.get('magic_max_size', 0), binary=True)}	({humanize.intcomma(data.get('magic_max_size'))} byte{plural(data.get('magic_max_size'))}) {'[Forced]' if data.get('force_magic') else ''}")
		try:
			report_info.append(f" 🕵️ Magic scanned:	{humanize.intcomma(data.get('magic_scanned'))} file{plural(data.get('magic_scanned'))}	[{data.get('magic_scanned') / data.get('scanned_files') * 100:.2f} %]\n")
		except Exception as z:
			report_info.append(f" 🕵️ Magic scanned:	{humanize.intcomma(data.get('magic_scanned'))} file{plural(data.get('magic_scanned'))}	[{type(z).__name__} %]\n")
		report_info.append(f" 📊 Scanned Items:	\033[1m{humanize.intcomma(data.get('scanned_folders'))}{RESET} folder{plural(data.get('scanned_folders'))}, \033[1m{humanize.intcomma(data.get('scanned_files'))}{RESET} file{plural(data.get('scanned_files'))}")
		report_info.append(f" 📦 Scanned Size:	\033[1m{humanize.naturalsize(data.get('total_size'), binary=True)}{RESET} ({humanize.intcomma(data.get('total_size'))} byte{plural(data.get('total_size'))})")
		report_info.append(f" 🈲 Denied Folders:	{humanize.intcomma(data.get('denied_folders'))} folder{plural(data.get('denied_folders'))}\n")
		report_info.append(f" ➗ Average Size:	\033[1m{humanize.naturalsize(average_size, binary=True)}{RESET} ({decimal_bytes_to_bits(average_size, True)})" )
		report_info.append(f" 🗃️ Average files/dir:	{round(data.get('scanned_files') / data.get('scanned_folders'), 1) } file{plural(data.get('scanned_files') / data.get('scanned_folders'))}")
		report_info.append(f" 🚀 Search Speed:	\033[1m{data.get('scanned_files') / elapsed_seconds:.2f}{RESET} files/s\n")
		report_info.append(f" 🧵 Threaded:		{data.get('threaded')}")
		report_info.append(f" 📝 User Note:	{data.get('user_note')}")
		report_info = ("\n").join(report_info)
		# print(report_info, "\n")

		global error_report
		if data["error_logs"]:
			error_report = []
			for idx, error in enumerate(data["error_logs"], start=1):
				log = error.get('desc')
				if log == None:
					log = error.get('error')
				if error.get('type') == 'PermissionError':
					error_report.append(f"{idx}.	{colored_no_entry} {log}")
				elif error.get('type') == 'OSError':
					error_report.append(f"{idx}.	🚫 {log}")
				elif error.get('type') == 'FileNotFoundError':
					error_report.append(f"{idx}.	❔ {log}")
				elif error.get('type') == 'IsADirectoryError':
					error_report.append(f"{idx}.	🛤️ {log}")
				elif error.get('type') == 'NotADirectoryError':
					error_report.append(f"{idx}.	🚧 {log}")
				elif error.get('type') == 'FileExistsError':
					error_report.append(f"{idx}.	🔗 {log}")
				elif error.get('type') == 'ModuleNotFoundError':
					error_report.append(f"{idx}.	📦 {log}")
				elif error.get('type') == 'ImportError':
					error_report.append(f"{idx}.	🎣 {log}")
				elif error.get('type') == 'KeyError':
					error_report.append(f"{idx}.	🗝️ {log}")
				elif error.get('type') == 'IndexError':
					error_report.append(f"{idx}.	📇 {log}")
				elif error.get('type') == 'ValueError':
					error_report.append(f"{idx}.	🔢 {log}")
				elif error.get('type') == 'TypeError':
					error_report.append(f"{idx}.	🧩 {log}")
				elif error.get('type') == 'UnicodeDecodeError':
					error_report.append(f"{idx}.	🔣 {log}")
				elif error.get('type') == 'NotImplementedError':
					error_report.append(f"{idx}.	🤷 {log}")
				elif error.get('type') == 'ZeroDivisionError':
					error_report.append(f"{idx}.	➗ {log}")
				elif error.get('type') == 'AttributeError':
					error_report.append(f"{idx}.	🪄 {log}")
				elif error.get('type') == 'NameError':
					error_report.append(f"{idx}.	📛 {log}")
				elif error.get('type') == 'FileNotFoundError':
					error_report.append(f"{idx}.	❔ {log}")
				elif error.get('type') == 'SyntaxError':
					error_report.append(f"{idx}.	🔤 {log}")
				else:
					error_report.append(f"{idx}.	{colored_x} {log}")
			error_report = "\n".join(error_report)
		else:
			error_report = f" {colored_check} No errors found."

	generate_report(data)
	def sort_entries(entries, key):
		"""Sort a list of entries based on a key."""
		global error_message
		try:
			return sorted(entries, key=lambda x: x.get(key, "") if key in ["mime", "attr"] else x.get(key, 0))
		except Exception as k:
			error_message = f"{colored_warn} {k}"
			return entries

	def preview_file(file_path, lines=10): # if lines <= 0, show all
		print(f"\n{GREY}--- File Preview ---{RESET}")
		with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
			iters = itertools.cycle([None]) if lines <= 0 else range(lines)
			try:
				for _ in iters:  # Show first 10 lines
					line = file.readline()
					print(line)
					if not line:
						break
				print(f"{GREY}--- End of Preview ---{RESET}\n")
			except KeyboardInterrupt:
				print(f"{GREY}--- End of Preview ---{RESET}\n")

				print(f"🚧 Stopped at line {iters.stop}.")
			except Exception as e:
				print(f"{colored_warn} {YELLOW}[{type(e).__name__}]{RESET}: {e}.")
		print("\n")

	# Properties for root directory
	global depth_dir_info	
	depth_dir_info = [{
		"name": "<rootdir>",
		"type": "folder",
		"path": original_path,
		"size": data.get("total_size"),
		"attr": data.get("root_attr"),
		"mtime": data.get("root_mtime"),
		"ctime": data.get("root_ctime"),
		"atime": data.get("root_atime"),
		"files": data.get("scanned_files"),
		"folders": data.get("scanned_folders"),
		"access_denied": False
	}]
	def navigate(node, path="/", navigation_mode="browse", selected=None):
		"""Navigate through a directory tree."""
		depth = len(path.split("/")) - 2

		def print_cd(path="/", file="", emoji=None):# Get terminal width
			""" Print the current directory."""
			if emoji == None:
				if navigation_mode == "browse":
					emoji = "🌳"
				elif navigation_mode == "search":
					emoji = "🔍"
				elif navigation_mode == "top_files":
					emoji = "🥇"
				elif navigation_mode == "top_folders":
					emoji = "🏆"
				else:
					emoji = "📂"
			logging.debug(f"{depth_dir_info}\n🪜 Depth: {depth}\n")
			# return (f"	📂 Current Directory: {path}\n" + "-" * shutil.get_terminal_size().columns + "\n")
			breadcrumbs_arrow = ' > '
			backslash = '\\'
			return (f"	{emoji}{shorten_string(path+file,shutil.get_terminal_size().columns * 1 / 2).replace('/', breadcrumbs_arrow).replace(backslash, breadcrumbs_arrow)}\n" + "-" * shutil.get_terminal_size().columns + "\n")

		def print_dir(path="/", depth=0):
			""" Print a directory."""
			dir_count = 0
			file_count = 0
			print_list = []
			print_list.append("#	   Size		Name")
			print_list.append("-	   ----		----")
			print_list.append(f"[`]	⤴  {BOLD}{humanize.naturalsize(depth_dir_info[depth]['size'], binary=True)}	\033[1m../{RESET}")
			if depth_dir_info[depth]["access_denied"]:
				print_list.append(f"\n	{colored_no_entry} Access denied: {depth_dir_info[depth]['access_denied']}")

			for i, item in enumerate(node):
				# If the file is hidden, show in grey
				if item["name"].startswith(".") or item["attr"].count("Hidden") > 0:
					grey_start = GREY
					grey_end = RESET
				else:
					grey_start = ""
					grey_end = ""
				if item["type"] == "junction":
					dir_count += 1
					print_list.append(f"{grey_start}[{i}]	🛤️{BOLD} {humanize.naturalsize(item['size'], binary=True)}	{shorten_string(item['name'], shutil.get_terminal_size().columns * 1 / 2, '…')}/{RESET}{grey_end}")
				elif item["type"] == "symlink":
					dir_count += 1
					print_list.append(f"{grey_start}[{i}]	🌀{BOLD} {humanize.naturalsize(item['size'], binary=True)}	{shorten_string(item['name'], shutil.get_terminal_size().columns * 1 / 2, '…')}/{RESET}{grey_end}")
				elif item["type"] == "folder":
					dir_count += 1
					print_list.append(f"{grey_start}[{i}]	{get_folder_icon(item['name'])}{BOLD} {humanize.naturalsize(item['size'], binary=True)}	{shorten_string(item['name'], shutil.get_terminal_size().columns * 1 / 2, '…')}/{RESET}{grey_end}")
				else:
					file_count += 1
					print_list.append(f"{grey_start}[{i}]	{get_file_icon(item['name'], item['mime'])} {humanize.naturalsize(item['size'], binary=True)}	{shorten_string(item['name'], shutil.get_terminal_size().columns * 1 / 2, '…')}{grey_end}")
			print_list.append(f"\n	📁 Directories: {dir_count} | 📃 Files: {file_count}")
			return print_list
		def print_file_info(selected):
			""" Print information about a file."""
			try:
				now = time.time()
				print(print_cd(path, selected.get('name')))
				print(f"{get_file_icon(selected.get('name'), selected.get('mime'))} File Information:\n")
				print(f" 📛 Name:	{selected.get('name')}\n")
				print(f" 👣 Location:	{os.path.dirname(selected.get('path'))}")
				print(f" 🗂️ MIME Type:	{selected.get('mime')}\n")
				print(f" 📏 Size:	{humanize.naturalsize(selected.get('size'), binary=True)}	({humanize.intcomma(selected.get('size'))} byte{'s' if selected.get('size') != 1 else ''})")
				print(f" 📅 Created:	{seconds_to_datetime(selected.get('ctime', 0))}	[{humanize.naturaltime(now - selected.get('ctime', 0))}]")
				print(f" 📝 Modified:	{seconds_to_datetime(selected.get('mtime', 0))}	[{humanize.naturaltime(now - selected.get('mtime', 0))}]")
				print(f" 👀 Accessed:	{seconds_to_datetime(selected.get('atime', 0))}	[{humanize.naturaltime(now - selected.get('atime', 0))}]\n")
				print(f" 🪄 Attributes:	{', '.join(selected.get('attr'))}\n")
			except KeyError as e:
				logging.warning(f"{colored_warn} Unknown key: {e}")

		def print_dir_info(dir_info):
			""" Print information about a directory."""
			try:
				now = time.time()
				print(print_cd(path))
				print(f"{get_folder_icon(path)} Directory Information: {path}\n")
				print(f" 👣 Location:		{dir_info.get('path')}\n")
				print(f" 📃 Files: 		{humanize.intcomma(dir_info.get('files'))}")
				print(f" 📁 Folders: 		{humanize.intcomma(dir_info.get('folders'))}")
				print(f" 🗂️ Total Items: 	{humanize.intcomma(dir_info.get('files') + dir_info.get('folders'))}\n")
				print(f" 📏 Total Size: 	{humanize.naturalsize(dir_info.get('size'), binary=True)}	({humanize.intcomma(dir_info.get('size'))} byte{plural(dir_info.get('size'))})")
				try:
					print(f" ➗ Average Size: 	{humanize.naturalsize(round(dir_info.get('size') / dir_info.get('files'),3), binary=True)}	({decimal_bytes_to_bits(dir_info.get('size') / dir_info.get('files'), True)})\n")
				except ZeroDivisionError as z:
					print(f" ➗ Average Size: 	[{type(z).__name__}]\n")
				print(f" 📅 Created:		{seconds_to_datetime(dir_info.get('ctime', 0))}	[{humanize.naturaltime(now - dir_info.get('ctime', 0))}]")
				print(f" 📝 Modified:		{seconds_to_datetime(dir_info.get('mtime', 0))}	[{humanize.naturaltime(now - dir_info.get('mtime', 0))}]")
				print(f" 👀 Accessed:		{seconds_to_datetime(dir_info.get('atime', 0))}	[{humanize.naturaltime(now - dir_info.get('atime', 0))}]\n")

				print(f" 🪄 Attributes:		{', '.join(dir_info.get('attr'))}\n")

			except KeyError as e:
				logging.warning(f"{colored_warn} Unknown key: {e}")

		def print_link_info(link_info):
			try:
				now = time.time()
				print(print_cd(path, selected.get('name')))
				print(f"{'🌀' if selected.get('type') == 'symlink' else '🛤️'} File Information:\n")
				print(f" 📛 Name:	{selected.get('name')}\n")
				print(f" 👣 Location:	{os.path.dirname(selected.get('path'))}")
				print(f" 🎯 Target:	{link_info.get('target')}\n")
				print(f" 📏 Size:	{humanize.naturalsize(selected.get('size'), binary=True)}	({humanize.intcomma(selected.get('size'))} byte{'s' if selected.get('size') != 1 else ''})")
				print(f" 📅 Created:	{seconds_to_datetime(selected.get('ctime'))}	[{humanize.naturaltime(now - link_info.get('ctime', 0))}]")
				print(f" 📝 Modified:	{seconds_to_datetime(selected.get('mtime'))}	[{humanize.naturaltime(now - link_info.get('mtime', 0))}]")
				print(f" 👀 Accessed:	{seconds_to_datetime(selected.get('atime'))}	[{humanize.naturaltime(now - link_info.get('atime', 0))}]\n")
				print(f" 🪄 Attributes:	{', '.join(selected.get('attr'))}\n")
			except KeyError as e:
				logging.warning(f"{colored_warn} Unknown key: {e}")

		def search_result(results, query, sort_by="size", emoji="🔍"):
			results_list = []
			def print_results(results, results_list=None):
				if results_list == None:
					results_list = []
				if not results:
					print(f"{colored_no_entry} No results found.")
					return
				if sort_by == "size":
					for i, item in enumerate(results, start=1):
						if item["type"] == "folder" or item["type"] == "symlink" or item["type"] == "junction":
							results_list.append(f"[{i}]	{get_folder_icon(item['name'])} {humanize.naturalsize(item['size'], binary=True)}	{shorten_string(item['name'], shutil.get_terminal_size().columns * 1 / 3)}")
						elif item["type"] == "file":
							results_list.append(f"[{i}]	{get_file_icon(item['name'], item['mime'])} {humanize.naturalsize(item['size'], binary=True)}	{shorten_string(item['name'], shutil.get_terminal_size().columns * 1 / 2)}")
				elif sort_by == "mtime":
					for i, item in enumerate(results, start=1):
						if item["type"] == "folder" or item["type"] == "symlink" or item["type"] == "junction":
							results_list.append(f"[{i}]	{get_folder_icon(item['name'])} {seconds_to_datetime(item['mtime'])}	{shorten_string(item['name'], shutil.get_terminal_size().columns * 1 / 3)}")
						elif item["type"] == "file":
							results_list.append(f"[{i}]	{get_file_icon(item['name'], item['mime'])} {seconds_to_datetime(item['mtime'])}	{shorten_string(item['name'], shutil.get_terminal_size().columns * 1 / 2)}")
				elif sort_by == "ctime":
					for i, item in enumerate(results, start=1):
						if item["type"] == "folder" or item["type"] == "symlink" or item["type"] == "junction":
							results_list.append(f"[{i}]	{get_folder_icon(item['name'])} {seconds_to_datetime(item['ctime'])}	{shorten_string(item['name'], shutil.get_terminal_size().columns * 1 / 3)}")
						elif item["type"] == "file":
							results_list.append(f"[{i}]	{get_file_icon(item['name'], item['mime'])} {seconds_to_datetime(item['ctime'])}	{shorten_string(item['name'], shutil.get_terminal_size().columns * 1 / 2)}")
				elif sort_by == "atime":
					for i, item in enumerate(results, start=1):
						if item["type"] == "folder" or item["type"] == "symlink" or item["type"] == "junction":
							results_list.append(f"[{i}]	{get_folder_icon(item['name'])} {seconds_to_datetime(item['atime'])}	{shorten_string(item['name'], shutil.get_terminal_size().columns * 1 / 3)}")
						elif item["type"] == "file":
							results_list.append(f"[{i}]	{get_file_icon(item['name'], item['mime'])} {seconds_to_datetime(item['atime'])}	{shorten_string(item['name'], shutil.get_terminal_size().columns * 1 / 2)}")
				return results_list
			while True:
				clear_screen()
				title(f"🔎 Results for {query} - Tree Spider")
				print(print_cd(path, emoji))
				print(f"\n	🎯 Search Results for {query} - {len(results)} matched\n")
				if sort_by == "size":
					print("#	   Size		Name	")
					print("-	   ----		----	")
				elif sort_by == "mtime":
					print("#	   Mtime		Name	")
					print("-	   ----		----	")
				elif sort_by == "ctime":
					print("#	   Ctime		Name	")
					print("-	   ----		----	")
				elif sort_by == "atime":
					print("#	   Atime		Name	")
					print("-	   ----		----	")
				print("\n".join(print_results(results)))
				print("\n📍 Enter the number to navigate, '/back' or .. to go back, '/save' to save as markdown.")
				try:
					choice = input("\n>>> ").strip().lower()
				except KeyboardInterrupt:
					print(f"{colored_stop} Exiting...")
					return
				if choice == "":
					continue
				elif choice == "/back" or choice == "..":
					break
				elif choice == "/save":
					print(f"\n📝 Saving search results as markdown...")
					output_file = f"{scan_log_dir}/tree_util_search_result_{query}.md"
					spinner = Spinner()
					spinner.start()
					try:
						save_result_as_markdown(results, output_file=output_file, query=query)
					except KeyboardInterrupt:
						print(f"{colored_stop} Exiting...")
						return
					finally:
						spinner.stop()
						print(f"\n{colored_check} Saved search results as markdown: {output_file}\n")
					pause()
				elif choice.isdigit() and 0 < int(choice) <= len(results):
					selected = results[int(choice) - 1]
					clear_screen()
					if selected["type"] == "folder" or selected["type"] == "symlink" or selected["type"] == "junction":
						set_nth_list(depth_dir_info, depth+1, 
					{
						"name": selected.get("name"),
						"path": selected.get("path"),
						"type": selected.get("type"),
						"size": selected.get("size"),
						"attr": selected.get("attr"),
						"ctime": selected.get("ctime"),
						"mtime": selected.get("mtime"),
						"atime": selected.get("atime"),
						"files": selected.get("files"),
						"folders": selected.get("folders"),
						"access_denied": selected.get("access_denied")
					}
					)
						navigate(selected["children"], path + selected["name"] + "/", navigation_mode="search")
					elif selected["type"] == "file":
						title(f"🍎 {selected['name']} - Tree Spider")
						print_file_info(selected)
						pause(exit_message=f"{colored_stop} Exiting...")
				
		def open_file(choice, node):
			if choice.isdigit() and 0 <= int(choice) < len(node):
				run_path = node[int(choice)]["path"].replace('/', '\\')
				cmd = ["start", '""', f'"{run_path}"'] if os.name == "nt" else ['xdg-open', f'"{node[int(choice)]["path"]}"']
				print(f'🚀 Opening selected file with ... `{GREY}{" ".join(cmd)}{RESET}`')
				# run other file
				spinner = Spinner()
				spinner.start()
				try:
					os.system(" ".join(cmd))
				except KeyboardInterrupt:
					print(f"{colored_stop} Exiting...")
					return
				except Exception as e:
					error_message = (f"{colored_warn} Error: {e}")

				spinner.stop()
			else:
				error_message = (f"{colored_warn} Error: Invalid number: {choice}")
				clear_screen()

		def edit_report_user_note():
			title("📝 Edit Notes - Tree Spider")
			print(print_cd(path))
			print(report_info, "\n")

			print("\n	📝 Edit Notes (CTRL+C to discard)\n")
			
			edit_user_note = input("\n¶ ").strip()
			if not edit_user_note == "":
				data["user_note"] = edit_user_note

				title(f"🗜️ Compressing JSON... - Tree Spider")
				print(f"\n🗜️ Updating JSON...")
				spinner = Spinner()
				spinner.start() # small spinner animation, but works well
				try:
					compressed_data = bz2.compress(json.dumps(data, indent=4).encode('utf-8'))
					with open(json_file, 'wb') as f_out:
						f_out.write(compressed_data)
				except KeyboardInterrupt:
					print(f"{colored_stop} Interrupted by user.")
					return
				finally:
					spinner.stop()
					generate_report(data)
					print(f"\n{colored_check} Updated json: {json_file}\n")
					pause()

		# Sort by name by default
		node = sort_entries(node, "name")
		selected = None

		valid_sort_keys = ["name", "size", "mime", "ctime", "mtime", "atime", "attr"]
		valid_sort_keys_desc = ["Name", "Size", "MIME Type", "Created Time", "Modified Time", "Accessed Time", "Attributes"]
		valid_ext_keys = ["name", "freq", "size"]
		valid_ext_keys_desc = ["Name", "Frequency", "Size"]

		while True:
			global error_message

			clear_screen()

			title(f"🌳 { path.split('/')[-2] if not path == '/' else path} - Tree Spider")


			print(print_cd(path))
			print("\n".join(print_dir(path, depth)))
		
			# print(f"🌲 Depth: {depth}")
			print(f"\n📍 Enter the navigation number, '{GREY}..{RESET}' to return, '{GREY}/help{RESET}', '{GREY}/h{RESET}' or '{GREY}/?{RESET}' for help.")

					
			# Display an error message
			if not error_message == "":
				print(error_message)
				error_message = ""
			try: # user input
				choice = input("\n>>> ").strip().lower()
			except KeyboardInterrupt as k:
				print(k)
				if depth == 0:
					print(f"{colored_stop} Exiting...")
				depth_dir_info.pop()
				return
			if choice == ".." or choice == "/back" or choice == "`":
				# print(f"🔙 Going back..." if not depth==0 else print(f"{colored_stop} Exiting..."))
				depth_dir_info.pop()
				return

			elif choice == "/help" or choice == "/h" or choice == "/?":
				clear_screen()
				title("💡 Help - Tree Spider")
				print(print_cd(path))
				print("\n💡 Command List\n")
				print(" [NUMBER]	🪜 Navigates to the specified file or directory ")
				print(" CTRL + C	🛑 Returns to the previous directory or exits the program if you are in the root directory.\n")
				print(" /help /h /?	💡 Displays this help message\n")
				print(" .. /back	🔙 Returns to the previous directory")
				print(" /dir /d	📂 Displays the properties of the current directory")
				print(" /dup /u	🪞 Displays duplicate files in the current directory")
				print(" /empty /ed	🗑️ Displays empty directories in the current directory")
				print(" /error /e	🚨 Displays error message logs from the snapshot report")
				print(" /exit /quit /q	🚪 Quits this program")
				print(" /ext /x [%s]\n" % ", ".join(valid_ext_keys), "		📎 Displays the most common file extensions in scanned files.\n")
				print(" /info /i	📋 Displays snapshot report information")
				print(" /note /n	📝 Edits and saves the user note of the report")
				print(" /peek /p NUMBER (LINES)\n		👀 Previews file for specified lines (default lines = 20, set 0 to show all data)")
				print(" /recent /r (COUNT)\n		🕰️ Displays the most recently modified files in the current directory")
				print(" /regex /re	🧩 Searches for files or folders using a regular expression")
				print(" /search /find /f STRING\n 		🔎 Searches for files or folders by name")
				print(" /sort /s [%s]\n" % ", ".join(valid_sort_keys), "		📊 Sorts the current directory by a specific key")
				print(" /run /o NUMBER	🚀 Opens/runs file in system default program")
				print(" /top /t (COUNT)🥇 Displays the top largest file sizes in scanned files. (default count = 10)\n")
				print(" /topf /tf (COUNT)\n		🏆 Displays the top largest folders in scanned files. (default count = 10)\n")
				print(" /tree /t	🌲 Displays the directory tree of the current directory")
				try:
					pause(exit_message=f"{colored_stop} Exiting...")
				except KeyboardInterrupt:
					return
			# Exit the program
			elif choice == "/exit" or choice == "/quit" or choice == "/q":
				print(f"{colored_stop} Exiting...")
				exit(0)
				prise()

			# Show scanning info
			elif choice == "/info" or choice == "/i":
				clear_screen()
				title("📋 Report info - Tree Spider")
				print(print_cd(path))

				print(report_info, "\n\n")
				if total_size > disk_total:
					print("* Note: The scanned size may be bigger than the total disk size. This is because of on-demand cloud storage services.\n")
				pause(exit_message=f"{colored_stop} Exiting...")

			elif choice == "/error" or choice == "/e":
				clear_screen()
				title("🚨 Error logs - Tree Spider")
				print(print_cd(path))
				print("\n	🚨 Error Report\n")
				print(error_report, "\n")
				pause(exit_message=f"{colored_stop} Exiting...")

			elif choice == "/note" or choice == "/n":
				clear_screen()
				try:
					edit_report_user_note()
				except KeyboardInterrupt:
					print(f"{colored_stop} Interrupted by user.")
					return
			# Back to the previous directory

			# Display the most common file extensions

			elif choice == "/ext" or choice == "/x":
				error_message = (f"{colored_bulb} Usage: /ext {', '.join(valid_ext_keys)}")
			elif choice.startswith("/ext ") or choice.startswith("/x "):
				_, key = choice.split(" ", 1)
				
				if key in valid_ext_keys:
					print("📎 Finding most common file extensions...")
					spinner = Spinner()
					spinner.start()
					try:
						result = get_most_common_file_extensions(node, key, None, total_size=data.get("total_size"), total_files=data.get("scanned_files"))
					except KeyboardInterrupt:
						print(f"{colored_stop} Exiting...")
						return
					finally:
						spinner.stop()
					clear_screen()
					title("📎 Most Common File Extensions - Tree Spider")
					print(print_cd(path, emoji="📎"))
					print("\n	📎 Most Common File Extensions\n")
					print("#	Ext.	Count	% Count	Size	% size")
					print("-	----	-----	-------	----	------")
					for i, item in enumerate(result, start=1):
						print(f"{i}.	{item[0]}	{item[1][0]}	{item[1][3] * 100:.2f} %	{humanize.naturalsize(item[1][1], binary=True)}	{item[1][2] * 100:.2f} %")
					print("\n")
					pause(exit_message=f"{colored_stop} Exiting...")
				else:
					error_message = (f"{colored_warn} Error: Invalid sorting key: {key}")	
				
			# Open a file
			elif choice == "/peek" or choice == "/p":
				error_message = (f"{colored_bulb} Usage: /peek NUMBER (LINES)")
			elif choice.startswith("/peek ") or choice.startswith("/p "):
				# /peek 0 22 - preview 0th file for 22 lines (lines is optional)
				if len(choice.split(" ")) == 3:
					_, n, l = choice.split(" ", 3)
					try:
						l = int(l)
					except ValueError:
						error_message = (f"{colored_warn} Error: Invalid line number: {l}")
						continue
				elif len(choice.split(" ")) == 2:
					_, n = choice.split(" ", 2)
					l = 10
				else:
					error_message = (f"{colored_warn} Error: Got too many arguments ({len(choice.split(' '))-1}). Please enter /preview NAME [LINES]")
					continue
				if n.isdigit() and 0 <= int(n) < len(node):
					selected = node[int(n)]
					if selected["type"] == "file":# and selected.get("mime", "").startswith("text")
						if not "text" in selected.get("mime", ""):
							print(f"{colored_warn} Selected file is not recognized as a text file. ({selected['mime']})")
							print("Proceeding may cause your terminal to break. Proceed? ([y]es/[n]o)\n")
							choice = input_or_exit(">>> ", f"{colored_stop} Exiting...").lower()
							if not choice == "y" or choice == "yes":
								continue
						clear_screen()
						title(f"👀 Previewing {selected['name']} - Tree Spider")
						print(print_cd(path))
						print(f"👀 Previewing: {selected['name']}\n")
						
						try:
							preview_file(selected["path"], l)
							pause()
						except KeyboardInterrupt:
							print(f"{colored_stop} Exiting...")
							return
						except Exception as e:
							error_message = (f"{colored_warn} Error: {e}")
					else:
						error_message = (f"{colored_warn} Error: Selected item is not a file")
				else:
					error_message = (f"{colored_warn} Error: Invalid file number: {n}")
			# Sort the directory
			elif choice == "/sort" or choice == "/s":
				error_message = (f"{colored_bulb} Usage: /sort [{', '.join(valid_sort_keys)}]")
			elif choice.startswith("/sort ") or choice.startswith("/s "):
				key = choice.split(" ")[1]
				if key not in ["size", "name", "ctime", "mtime", "atime", "mime"]:
					error_message = (f"{colored_warn} Error: Invalid sorting key: {key}")
				else:
					print(f"📊 Sorting list by {[valid_ext_keys_desc]}...")
					node[:] = sort_entries(node, key)

			# Search for a file or folder
			elif choice == "/search" or choice == "/find" or choice == "/f":
				error_message = (f"{colored_bulb} Usage: /search STRING")
			elif choice.startswith("/search ") or choice.startswith("/find ") or choice.startswith("/f "):
				_, query = choice.split(" ", 1)
				print("🔎 Searching...")
				spinner = Spinner()
				spinner.start()
				try:
					results = search_files(structure, query)
				except KeyboardInterrupt:
					print(f"{colored_stop} Exiting...")
					return
				spinner.stop()
				
				if len(results) > 0:
					search_result(results, query, emoji="🔎")
				else:
					error_message = (f"{colored_exclamation} No results found for '{query}'")
			# Search for a file or folder using a regular expression
			elif choice == "/regex" or choice == "/re":
				error_message = (f"{colored_bulb} Usage: /regex REGEX")
			elif choice.startswith("/regex ") or choice.startswith("/re "):
				_, regex = choice.split(" ", 1)
				regex = " ".join(regex.split())
				print("🧩 Searching...")
				spinner = Spinner()
				spinner.start()
				try:
					results = search_files_regex(structure, regex)
				except KeyboardInterrupt:
					print(f"{colored_stop} Exiting...")
					return
				spinner.stop()
				
				if len(results) > 0:
					search_result(results, regex, emoji="🧩")
				else:
					error_message = (f"{colored_exclamation} No results found for '{regex}'")
			# Show empty directories
			elif choice == "/empty" or choice == "/ed":
				title("🗑️ Empty directories - Tree Spider")
				
				print("🗑️ Searching...")
				spinner = Spinner()
				spinner.start()
				try:
					files = search_empty_folders(node)
				except KeyboardInterrupt:
					print(f"{colored_stop} Exiting...")
					return
				finally:
					spinner.stop()

				if len(files) > 0:
					search_result(files, "Empty directories", emoji="🗑️")
				else:
					error_message = (f"{colored_check} No empty directories found.")
			# Show duplicate files
			elif choice == "/dup" or choice == "/u":
				title("🪞 Duplicate files - Tree Spider")
				
				print("🪞 Searching...")
				spinner = Spinner()
				spinner.start()
				try:
					files = search_duplicates(node)
				except KeyboardInterrupt:
					print(f"{colored_stop} Exiting...")
					return
				finally:
					spinner.stop()

				if len(files) > 0:
					search_result(files, "Duplicate files", emoji="🪞", sort_by="name")
				else:
					error_message = (f"{colored_check} No duplicate files found.")
			# Show directory info
			elif choice == "/dir" or choice == "/d":
				clear_screen()
				title("🪵 Directory info - Tree Spider")
				print_dir_info(depth_dir_info[depth])
				pause(exit_message=f"{colored_stop} Exiting...")
			# Show recent files
			elif choice == "/recent" or choice == "/r" or choice.startswith("/recent ") or choice.startswith("/r "):
				if choice.startswith("/recent ") or choice.startswith("/r "):
					_, n = choice.split(" ", 1)
				else:
					n = "10"
				if not n.isdigit():
					error_message = (f"{colored_warn} Error: Invalid number: {n}")
				else:
					n = int(n)
					title("🕰️ Recent files - Tree Spider")
					print("🕰️ Searching...")
					spinner = Spinner(char="fragment")
					spinner.start()
					try:
						files = get_top_n_recent_files(node, n)
					except KeyboardInterrupt:
						print(f"{colored_stop} Exiting...")
						return
					finally:
						spinner.stop()
					if len(files) > 0:
						search_result(files, f"Recent files ({n})", sort_by="mtime", emoji="🕒")
					else:
						error_message = (f"{colored_exclamation} No results found for '{n}'")

			# Show top n largest folders in json
			if choice == "/topf" or choice == "/tf" or choice.startswith("/topf ") or choice.startswith("/tf "):
				if choice.startswith("/topf ") or choice.startswith("/tf "):
					_, n = choice.split(" ", 1)
				else:
					n = "10"
				if not n.isdigit():
					error_message = (f"{colored_warn} Error: Invalid number: {n}")
				else:
					print("🏆 Searching...")
					n = int(n)
					spinner = Spinner(char="fragment")
					spinner.start()
					try:
						files = get_top_n_large_folders(node, n)
					except KeyboardInterrupt:
						print(f"{colored_stop} Exiting...")
						return
					finally:
						spinner.stop()
					if len(files) > 0:
						search_result(files, f"Top {n} Largest Folders", sort_by="size", emoji="🏆")
					else:
						error_message = (f"{colored_exclamation} No results found for '{n}'")
			# Show top n largest files in json
			if choice == "/top" or choice == "/t" or choice.startswith("/top ") or choice.startswith("/t "):
				if choice.startswith("/top ") or choice.startswith("/t "):
					_, n = choice.split(" ", 1)
				else:
					n = "10"
				if not n.isdigit():
					error_message = (f"{colored_warn} Error: Invalid number: {n}")
				else:
					print("🥇 Searching...")
					n = int(n)
					spinner = Spinner(char="fragment")
					spinner.start()
					try:
						files = get_top_n_largest_files(node, n)
					except KeyboardInterrupt:
						print(f"{colored_stop} Exiting...")
						return
					finally:
						spinner.stop()
					if len(files) > 0:
						search_result(files, f"Top {n} Largest Files", sort_by="size", emoji="🥇")
					else:
						error_message = (f"{colored_exclamation} No results found for '{n}'")
			elif choice == "/run" or choice == "/o":
				# open current directory
				cmd = ['start','""', f"\"{depth_dir_info[-1]['path']}\""] if os.name == "nt" else ['xdg-open', f'"{original_path[:-1]}{path}"']
				print(f'🚀 Opening current directory with explorer... `{GREY}{" ".join(cmd)}{RESET}`')
				spinner = Spinner()
				spinner.start()
				try:
					os.system(" ".join(cmd))
				except KeyboardInterrupt:
					print(f"{colored_stop} Exiting...")
					return
				except Exception as e:
					error_message = (f"{colored_warn} Error: {e}")
				spinner.stop()
				clear_screen()
			elif choice.startswith("/run ") or choice.startswith("/o "):
				_, choice = choice.split(" ", 1)
				open_file(choice, node)
			# Number navigation
			elif choice.isdigit() and 0 <= int(choice) < len(node):
				selected = node[int(choice)]
				if selected["type"] == "folder":
					set_nth_list(depth_dir_info, depth+1, 
					{
						"name": selected.get("name"),
						"path": selected.get("path"),
						"type": selected.get("type"),
						"size": selected.get("size"),
						"attr": selected.get("attr"),
						"ctime": selected.get("ctime"),
						"mtime": selected.get("mtime"),
						"atime": selected.get("atime"),
						"files": selected.get("files"),
						"folders": selected.get("folders"),
						"access_denied": selected.get("access_denied")
					}
					)
					navigate(selected["children"], path + selected["name"] + "/")
				elif selected["type"] in ["file", "junction", "symlink"]:
					clear_screen()
					title(f"🍎 {selected['name']} - Tree Spider")
					if selected["type"] in ["junction", "symlink"]:
						print_link_info(selected)
					else:
						print_file_info(selected)
					pause(exit_message=f"{colored_stop} Exiting...")
			elif choice.isnumeric() or choice.isdigit() and (int(choice) < 0 or int(choice) >= len(node)):
				error_message = f"{colored_warn} Invalid choice: {choice}"

	navigate(structure)



def naturalsize_to_int(value):
	"""
	Convert a human-readable file size string into an integer representing bytes.

	Supports both decimal (SI) and binary (IEC) prefixes:

	- SI (Base 10): "k" (10³), "m" (10⁶), "g" (10⁹), "t" (10¹²), "p" (10¹⁵), etc.
	- IEC (Base 2): "ki" (2¹⁰), "mi" (2²⁰), "gi" (2³⁰), "ti" (2⁴⁰), etc.

	Parameters:
		value (str | int): The size string (e.g., "10M", "5Gi", "2.5T") or an integer.

	Returns:
		int: The equivalent size in bytes.

	Example:
		>>> naturalsize_to_int("10M")
		10000000
		>>> naturalsize_to_int("5Gi")
		5368709120
		>>> naturalsize_to_int("123")
		123
	"""
	value = str(value).lower().replace(",", "").strip()  # Normalize input

	if value.endswith("k"):
		return int(value[:-1]) * 10**3
	elif value.endswith("m"):
		return int(value[:-1]) * 10**6
	elif value.endswith("g"):
		return int(value[:-1]) * 10**9
	elif value.endswith("t"):
		return int(value[:-1]) * 10**12
	elif value.endswith("p"):
		return int(value[:-1]) * 10**15
	elif value.endswith("e"):
		return int(value[:-1]) * 10**18
	elif value.endswith("z"):
		return int(value[:-1]) * 10**21
	elif value.endswith("y"):
		return int(value[:-1]) * 10**24
	elif value.endswith("r"):
		return int(value[:-1]) * 10**27
	elif value.endswith("q"):
		return int(value[:-1]) * 10**30

	elif value.endswith("ki"):
		return int(value[:-2]) * 2**10
	elif value.endswith("mi"):
		return int(value[:-2]) * 2**20
	elif value.endswith("gi"):
		return int(value[:-2]) * 2**30
	elif value.endswith("ti"):
		return int(value[:-2]) * 2**40
	elif value.endswith("pi"):
		return int(value[:-2]) * 2**50
	elif value.endswith("ei"):
		return int(value[:-2]) * 2**60
	elif value.endswith("zi"):
		return int(value[:-2]) * 2**70
	elif value.endswith("yi"):
		return int(value[:-2]) * 2**80
	elif value.endswith("ri"):
		return int(value[:-2]) * 2**90
	elif value.endswith("qi"):
		return int(value[:-2]) * 2**100

	else:
		return int(value)  # If no suffix, treat as raw integer

def get_deepest_folder(path):
	"""Get the name of the deepest folder in a path."""
	path = os.path.abspath(path)  # Get absolute path
	parts = path.rstrip(os.sep).split(os.sep)  # Split into parts

	if os.name == "nt":  # Windows
		label = get_volume_label(path[:1])
		return parts[-1] if len(parts) > 1 else label if not label == None else path[:1]  # Drive letter if root
	else:  # Linux/macOS
		return parts[-1] if len(parts) > 1 else "root"

def todo(message):
	"""
	Returns a formatted string with a green-colored reminder message.

	Parameters:
		message (str): The reminder message to be formatted.

	Returns:
		str: A formatted string with the reminder message.
	"""
	return(f"\033[32m📌 [Reminder]\033[0m - {message}\n")

def main(args):
	global magic_max_size, directory, json_file, scan_log_dir
	magic_max_size = naturalsize_to_int(args.threshold)
	directory = None
	json_file = None
	scan_log_dir = "./logs"
	if not os.path.exists(scan_log_dir):
		os.mkdir(scan_log_dir)

	if os.path.exists(config_file):
		try:
			config.read(config_file)
			last_opened_json = config.get("tree_util", "last_opened_json")
		except UnicodeDecodeError:
			os.remove(config_file)
			last_opened_json = ""

	else:
		last_opened_json = ""

	no_attributes = args.no_attributes

	global action, threaded, gui_enabled, main_menu_enabled, error_message, open_after_scan, force_magic, use_magika
	threaded = args.threads
	gui_enabled = args.gui
	open_after_scan = args.explore
	error_message = ""
	force_magic = args.force_magic
	try:
		use_magika = args.use_magika
	except AttributeError:
		use_magika = False

	def main_menu():
		global action, threaded, directory, gui_enabled, main_menu_enabled, magic_max_size, json_file, error_message, open_after_scan, force_magic, use_magika
		main_menu_enabled = True
		while True:
			clear_screen()
			json_file = ''
			directory = ''
			print("\n📍 Enter commands to begin:\n")
			print(" 🖥️ Main commands\n")
			print(f"  📂 Scan a directory:	'{GREY}scan{RESET}', '{GREY}s{RESET}'")
			print(f"  📜 Explore JSON:	'{GREY}browse{RESET}', '{GREY}b{RESET}'")
			if last_opened_json:
				print(f"  🗓️ Last opened JSON:	'{GREY}last{RESET}', '{GREY}l{RESET}'")
			print("\n 🔧 Scan Settings\n")
			print(f"  📏 Magic max size [{humanize.naturalsize(magic_max_size, binary=True)}]:	'{GREY}magic{RESET}', '{GREY}m{RESET}'")
			if "magika" in sys.modules:
				print(f"  🪄 Use magika [{use_magika}]:	'{GREY}magika{RESET}', '{GREY}k{RESET}'")
			else:
				print(f"  {GREY}🪄 Use magika [Unavailable]:	'magika', 'k'{RESET}")
			print(f"  🔮 Force magic [{force_magic}]:	'{GREY}force{RESET}', '{GREY}f{RESET}'")
			print(f"  🧵 Threads [{threaded}]:		'{GREY}threads{RESET}', '{GREY}t{RESET}'")
			print(f"  🖱️ GUI filedialog [{gui_enabled}]:	'{GREY}gui{RESET}', '{GREY}g{RESET}'")
			print(f"  ⛏️ Open after scan [{open_after_scan}]:	'{GREY}explore{RESET}', '{GREY}e{RESET}'")
			print("\n 🐍 Debug\n")
			print(f"  ⌨️ Edit this file:	'{GREY}edit{RESET}', '{GREY}d{RESET}'")
			print(f"  ✨ Reload this file:	'{GREY}reload{RESET}', '{GREY}r{RESET}'")
			print(f"  🎚️ Verbosity [{logging.getLevelName(logger.getEffectiveLevel())}]:	'{GREY}verbose{RESET}', '{GREY}v{RESET}'")
			print(f"\n 🚪 Exit:		'{GREY}exit{RESET}', '{GREY}quit{RESET}', '{GREY}q{RESET}', {GREY}CTRL+C{RESET}\n")
			# Display an error message
			if not error_message == "":
				print(error_message)
				error_message = ""
			action = input_or_exit(">>> ").lower().strip()

			if action == "browse" or action == 'b':
				browse_mode()
			elif action == 'scan' or action == 's':
				scan_mode()
			elif action == 'last' or action == 'l':
				open_last_opened()
			elif action == "magic" or action == "m":
			
				print("Set mime threshold:")
				print(f"Current: {humanize.naturalsize(magic_max_size, binary=True)} ({humanize.intcomma(magic_max_size)} byte{plural(magic_max_size)})")

				while True:
					try:
						magic_max_size = naturalsize_to_int(input_or_exit(">>> "))
						error_message = (f"📏 New threshold: {humanize.naturalsize(magic_max_size, binary=True)} ({humanize.intcomma(magic_max_size)} byte{plural(magic_max_size)})")
						break
					except ValueError:
						error_message = (f"{colored_warn} Invalid input. Please enter a number.")

			elif action == "magika" or action == "k":
				if "magika" in sys.modules:
					use_magika = not use_magika
					error_message = (f"🪄 Use magika {'enabled' if use_magika else 'disabled'}")
				else:
					error_message = (f"🪄 To install magika, run `{GREY}pip install magika{RESET}`. Requires Python 3.8 - 3.12. ")
			elif action == "t" or action == "threads":
				threaded = not threaded
				error_message = (f"🧵 Threads {'enabled' if threaded else 'disabled'}")
			elif action == "g" or action == "gui":
				gui_enabled = not gui_enabled
				error_message = (f"🖱️ GUI {'enabled' if gui_enabled else 'disabled'}")
			elif action == "f" or action == "force":
				force_magic = not force_magic
				error_message = (f"🧵 Force magic {'enabled' if force_magic else 'disabled'}")
			elif action == "e" or action == "explore":
				open_after_scan = not open_after_scan
				error_message = (f"⛏️ Open after scan {'enabled' if open_after_scan else 'disabled'}")
			elif action == "d" or action == "edit":
				cmd = ["code", os.path.realpath(__file__)]
				error_message = (f"📝 Editing this file... `{GREY}{' '.join(cmd)}{RESET}`")
				os.system(" ".join(cmd))
			elif action == "v" or action == "verbose":
				if logger.getEffectiveLevel() == logging.DEBUG:
					logger.setLevel(logging.INFO)
					error_message = (f"🎚️ Verbosity set to INFO")
				else:
					logger.setLevel(logging.DEBUG)
					error_message = (f"🎚️ Verbosity set to DEBUG")
			elif action == "r" or action == "reload":
				exec(open(__file__).read())
			elif action == "exit" or action == "quit" or action == "q" or action == "..":
				print(f"{colored_stop} Exiting...")
				exit()
			elif not action:
				if main_menu_enabled == True:
					main_menu()
				else:
					logging.error(error_message)
					exit(1)
				
			else:
				error_message = (f"{colored_warn} Invalid action. Please enter 'scan' or 'browse'.")
				if main_menu_enabled == True:
					main_menu()
				else:
					logging.error(error_message)
					exit(1)
	
	def scan_mode():
		global directory, error_message
		if not directory or directory == '':
			if gui_enabled:
				root = Tk()
				root.withdraw()
				root.attributes("-topmost", True)
				print("📂 Select the scan directory:")
				directory = filedialog.askdirectory(title="Select Scan Directory", initialdir=os.getcwd())
				root.destroy()
				print(f" '{directory}'")
			else:
				print("📂 Enter the scan directory path: ")
				directory = input_or_exit(">>> ")
			if not directory:
				error_message = (f"{colored_warn} No directory path provided.")
				if main_menu_enabled:
					main_menu()
				else:
					logging.error(error_message)
					exit(1)
			elif not os.path.isdir(directory):
				error_message = (f"{colored_warn} Invalid directory path: '{directory}'")
				directory = ''
				if main_menu_enabled:
					main_menu()
				else:
					logging.error(error_message)
					exit(1)

		if args.output:
			output_file = args.output
		else:
			default_output_file = f"{get_deepest_folder(directory)[:50]}_{seconds_to_datetime(time.time(), True)}.structure.json.bz2"

			if not args.simulate:
				if gui_enabled: # Set save location
					root = Tk()
					root.withdraw()
					root.attributes("-topmost", True)
					print("💾 Select the output file path:")
					output_file = filedialog.asksaveasfilename(defaultextension=".json.bz2", initialdir=scan_log_dir, initialfile=default_output_file, filetypes=[("BZip2 JSON File", "*.json.bz2")])
					root.destroy()
					if not output_file:
						print(f"{colored_warn} No output file path provided.")
						if main_menu_enabled:
							main_menu()
						else:
							exit(1)
					print(f" '{output_file}'")
				else:
					print("💾 Enter the output file path: ")
					output_file = input_or_exit(">>> ").strip()
					if not output_file:
						output_file = scan_log_dir +"/"+ default_output_file
						logging.warning(f"{colored_warn} No output file path provided. Defaulting to '{output_file}'")
					elif output_file.endswith(".json"):
						output_file += ".bz2"
					elif not output_file.endswith(".json.bz2"):
						output_file += ".json.bz2"

					if os.path.exists(output_file):
						print(f"{colored_warn} Output file already exists: '{output_file}' - overwrite? ([y]es/[n]o)\n")
						while True:
							overwrite = input_or_exit(">>> ").lower().strip()
							if overwrite in ["y", "yes"]:
								break
							elif overwrite in ["n", "no"]:
								output_file = default_output_file
								print(f"📌 Using default output file: '{output_file}'")
								break
							else:
								print(f"{colored_warn} Invalid input. Please enter 'yes' or 'no'.")
		global magic_scanned
		magic_scanned = 0
		print(f"⚖️ Magic MIME detection threshold: {humanize.naturalsize(magic_max_size, binary=True)} {'[FORCED]' if force_magic else ''}")
		print(f"{colored_bulb} If scanning takes too long, consider using a lower threshold.")
		print(f'📌 Running command: `{GREY}python3 {os.path.abspath(__file__)} -s "{directory}" -t {magic_max_size}{" -m" if args.simulate else ""}{" -th" if threaded else ""}{" -a" if no_attributes else ""}{" -f" if force_magic else ""}{" -e" if args.explore else ""}{" -k" if use_magika else ""} -o "{os.path.abspath(output_file)}"{" --no-estimates" if args.no_estimates else ""} {RESET}`\n')

		time_taken = save_json_tree(directory, output_file=output_file, simulate=args.simulate, no_attributes=no_attributes, magic_max_size=magic_max_size, use_threads=threaded, force_magic=force_magic, no_estimates=args.no_estimates, use_magika=use_magika)
		sys.stdout.write("\n")
		title(f"✅ Task Complete - Tree Spider")
		if args.simulate:
			logging.info(f"{colored_check} Simulation complete!")
		else:
			logging.info(f"{colored_check} Folder structure saved to '{output_file}'")
			print(f'{colored_bulb} You can open output file with `{GREY}python3 "{os.path.abspath(__file__)}" -b "{os.path.abspath(output_file)}"{RESET}`')
		if gui_enabled:
			root = Tk()
			root.withdraw()
			root.attributes("-topmost", True)

			if args.simulate:
				messagebox.showinfo("Success", f"Simulation complete!")
			else:
				messagebox.showinfo("Success", f"Folder structure saved to '{output_file}'\nElapsed time: {format_duration(time_taken)}")
			root.destroy()
		else:
			pause()
		if open_after_scan:
			browse_json_tree(output_file)
	def browse_mode():
		global json_file, error_message
		if not json_file:
			if gui_enabled:
				root = Tk()
				root.withdraw()
				root.attributes("-topmost", True)
				print("📂 Select the BZip2 JSON file to browse:")
				json_file = filedialog.askopenfilename(title="Select BZip2 JSON File", filetypes=[("JSON File", "*.json.bz2")],initialdir=scan_log_dir, defaultextension=".json.bz2")
				root.destroy()
				
				if not json_file or json_file =='':
					error_message = (f"{colored_warn} No JSON file path provided.")
					if main_menu_enabled:
						main_menu()
					else:
						logging.error(error_message)
						exit(1)
				
			else:
				
				def print_files(directory):
					print (f"\n📂 Scan log directory: {directory}\n")

					# Get all files with their creation timestamps and sizes
					files = [(f, os.path.getctime(os.path.join(directory, f)), os.path.getsize(os.path.join(directory, f))) 
						for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

					# Sort by creation time (oldest to newest)
					files.sort(key=lambda x: x[1])

					# Print the files with their creation time and size
					for file, ctime, size in files:
						if file.endswith(".json.bz2"):
							if directory == '.':
								print(f" {file}	({humanize.naturalsize(size,binary=True)})	[{humanize.naturaltime(time.time() - ctime)}]")
							else:
								print(f" {directory}/{file}	({humanize.naturalsize(size,binary=True)})	[{humanize.naturaltime(time.time() - ctime)}]")
					
				print_files(".")
				print_files(scan_log_dir)
				
				print("\n📂 Enter the JSON file path: ")
				json_file = input_or_exit(">>> ").strip()
				if not json_file or json_file =='':
					error_message = (f"{colored_warn} No JSON file path provided.")
					if main_menu_enabled:
						main_menu()
					else:
						logging.error(error_message)
						exit(1)
				
				if os.path.isfile(json_file+'.bz2'):
					json_file = json_file+'.bz2'
				elif os.path.isfile(json_file+'.json.bz2'):
					json_file = json_file+'.json.bz2'
				elif not os.path.isfile(json_file):
					error_message = (f"{colored_warn} Invalid JSON file path: '{json_file}'")
					if gui_enabled:
						root = Tk()
						root.withdraw()
						root.attributes("-topmost", True)
						messagebox.showerror("Error", f"Invalid JSON file path: '{json_file}'")
						root.destroy()
					
					if main_menu_enabled:
						main_menu()
					else:
						logging.error(error_message)
						exit(1)
		print("\n📜 Loading JSON file: ", json_file)
		browse_json_tree(json_file)
		if main_menu_enabled:
			main_menu()
		else:
			exit(0)
	def open_last_opened():
		global error_message, json_file
		if os.path.exists(config_file):
			try:
				config.read(config_file)
				last_opened_json = config.get("tree_util", "last_opened_json")
			except UnicodeDecodeError:
				os.remove(config_file)
				last_opened_json = ""

		else:
			last_opened_json = ""
		
		if not last_opened_json:
			error_message = (f"{colored_warn} Last opened JSON file not found: {last_opened_json}")
			if main_menu_enabled:
				main_menu()
			else:
				logging.error(error_message)
				exit(1)
		elif os.path.exists(last_opened_json):
			json_file = last_opened_json
			print(f"\n📜 Opening last opened JSON file:  {json_file}")
			browse_json_tree(json_file)
		else:
			error_message = (f"{colored_warn} Last opened JSON file not found: {last_opened_json}")
			if main_menu_enabled:
				main_menu()
			else:
				logging.error(error_message)
				exit(1)
	main_menu_enabled = False
	if args.scan:
		action = "scan"
		directory = args.scan
		scan_mode()
	elif args.browse:
		action = "browse"
		json_file = args.browse
		browse_mode()
	elif args.last:
		action = 'last'
		open_last_opened()
	else:
		main_menu()
	


# print(todo("Todo: Compress json file to reduce size. (e.g. gzip, brotli, zstd)"))
# print(todo("Fix tqdm progress bar information - scanned total size"))
# print(todo("Todo: Regex search for setting icon"))
# print(todo("Fix: command /d - dir info"))
# print(todo("Fix: PermissionError not stored on threaded mode"))
# print(todo("Fix: IndexError (depth_dir_info) when opening folder on search results	"))


init_spinner.stop()

if __name__ == "__main__":
	import argparse
	import configparser
	try:
		from tkinter import filedialog, messagebox, Tk
	except Exception as i:
		print(f"{colored_warn} {YELLOW}[{type(i).__name__}]{RESET}: {i} - GUI not available.")
		
	title("🌳 Tree Spider")
	
	config = configparser.ConfigParser()
	config_file = os.path.join(os.path.dirname(__name__), 'tree_util_config.ini')

	parser = argparse.ArgumentParser(description="🌳 Tree Spider - A tool to create snapshots of directory structures and explore them.",epilog="Usage: python3 tree_util.py -s /path/to/directory -o /path/to/output.json.bz2")

	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("-b", "--browse", type=str, help="Explore a structured JSON file. Specify the JSON file path.")
	mode.add_argument("-s", "--scan", type=str, help="Scan and create a structured JSON file. Specify the scan directory path.")
	parser.add_argument("-o", "--output", type=str, help="Specify the path for the BZip2 compressed output. If not specified, the output is saved in the current directory with a datetime. can be used with '-s'.")
	parser.add_argument("-t", "--threshold", type=str, default=naturalsize_to_int("10Mi"), help="Specify the threshold in bytes for enabling deep file type scanning (e.g. 50K, 10Mi, 100 etc.). If the file size is greater than the value, the MIME type is first detected by the mimetypes module (which detects by extension), then if the MIME type is unknown or too common (e.g. text/plain), the magic module is used for deep MIME type detection. Set value to 0 to disable deep file type scanning which makes the script faster. can be used with '-s'.")
	parser.add_argument("-g", "--gui", action="store_true", help="Open the GUI file selection to choose a directory (it's easier this way).")
	parser.add_argument("-m", "--simulate", action="store_true", help="Simulate the scan process, rather than actually writing the JSON file. This is useful for testing purposes.")
	parser.add_argument("-e", "--explore", action="store_true", help="Explore a structured JSON file soon after it's created.")
	parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
	parser.add_argument("-th", "--threads", action="store_true", help="Optimize the script by using threads to scan directories.")
	parser.add_argument("-l", "--last", action="store_true", help="Open last opened JSON file.")
	parser.add_argument("-f", "--force-magic", action="store_true", help="Force deep MIME type detection under the threshold. (Disable extension detection, slower).")
	parser.add_argument("-a","--no-attributes", action="store_true", help="Do not include file attributes in the JSON file.")
	parser.add_argument("--no-estimates", action="store_true", help="Do not estimate total files and directories.")
	parser.add_argument("-k", "--use-magika", action="store_true", help="Use Google Magika for even deeper MIME type detection. (Slowest, but can detect more types.)")
	args = parser.parse_args()

	if not "magika" in sys.modules and args.use_magika:
		raise Exception("Magika is not installed. Install it with: pip install magika")


	if args.verbose:
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.INFO)
	if args.gui and not "tkinter" in sys.modules:
		gui_enabled = True
	else:
		gui_enabled = False


	if len(error_logs) > 0:
		try:
			timeout()
			input()
		except: # On some systems, keyboard module requires root permission
			pause("Press Enter to continue...")
	main(args)