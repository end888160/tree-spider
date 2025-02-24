"""
This script lets you generate snap shots of your Drive folder structure.
You need Python 3.6 or higher to run this script.

Inspired by: [class - representation of files and folder-tree of Google Drive folder using Python API - Stack Overflow](https://stackoverflow.com/questions/48112412/representation-of-files-and-folder-tree-of-google-drive-folder-using-python-api)
Help with ChatGPT: https://chatgpt.com/c/67b0e93c-c474-8004-8740-e4bbb98486d1

"""



# Color ANSI codes
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
CYAN = "\033[36m"
ORANGE = "\033[38;5;208m"
WHITE = "\033[37m"
BOLD = "\033[1m"
BOLD_ORANGE = "\033[1;33m"
BOLD_CYAN = "\033[1;36m"
GREY = "\033[90m"
UNDERLINE = "\033[4m"

program_name = "Tree Spider"
print(f"\n\n{GREEN}	🌳 {program_name}{RESET} - {ORANGE}Directory Snapshot Tool{RESET}\n\n")
print("		⏳ Initializing...\n")

import threading
import itertools
import time
import sys

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
class Spinner:
	def __init__(self, wait=1/10, show_timer=True, timer_delay=2, char="ascii", done_message=" "):
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
			symbols = ["🌚","🌒","🌓","🌔","🌝","🌖","🌗","🌘"]
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


# Colored emojis
colored_check = "\033[32m✅\033[0m"
colored_x = "\033[31m❌\033[0m"
colored_stop = "\033[31m🛑\033[0m"
colored_warn = "\033[93m⚠️\033[0m"
colored_bulb = "\033[36m💡\033[0m"
colored_no_entry = "\033[31m⛔\033[0m"
colored_question = "\033[1m❓\033[0m"
colored_exclamation = "\033[31m❗\033[0m"
colored_prohibited = "\033[38;5;208m🚫\033[0m"


error_logs = []
from inputimeout import inputimeout, TimeoutOccurred
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from datetime import datetime
from getpass import getpass
import concurrent.futures
from tqdm import tqdm
from sys import exit
import subprocess
import mimetypes
import traceback
import tempfile
import markdown
import platform
import humanize
import logging
import shutil
import random
import psutil
import heapq
import math
import json
import stat
import bz2
import re
import io
import os

logging.basicConfig(format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

try:
	import orjson
except ImportError:
	logging.debug("orjson not found, using json instead")
	print(f"{colored_bulb} You can install orjson to to speed up parsing: `{GREY}pip install orjson{RESET}`")

if os.name == "nt":  # Windows only, get volume label
	import ctypes
	import ctypes.wintypes
def get_volume_label(path: str = "/") -> str:
	"""Get the Volume Label (name) of a drive in a cross-platform way.
	
	Args:
		path (str): The path or drive letter to check (default: root "/").
	
	Returns:
		str: The volume label or None if not found.
	"""

	system = platform.system()
	path = os.path.abspath(path).split(os.sep)[0] + os.sep
	try:
		if system == "Windows":
			volume_name = ctypes.create_unicode_buffer(1024)
			file_system = ctypes.create_unicode_buffer(1024)

			ctypes.windll.kernel32.GetVolumeInformationW(
				f"{path}",
				volume_name,
				ctypes.sizeof(volume_name),
				None,
				None,
				None,
				file_system,
				ctypes.sizeof(file_system)
			)

			return volume_name.value if volume_name.value else path[:1]


		elif system == "Linux":
			output = subprocess.check_output(f"lsblk -no LABEL {path}", shell=True, text=True)
			return output.strip() if output else None

		elif system == "Darwin":  # macOS
			output = subprocess.check_output(f"diskutil info {path} | grep 'Volume Name'", shell=True, text=True)
			match = re.search(r"Volume Name:\s+(.+)", output)
			return match.group(1).strip() if match else None

	except subprocess.CalledProcessError:
		return None  # Command failed

	return None  # Unsupported OS or no result

def get_volume_serial_number(path: str = "/") -> str:
	"""Get the Volume Serial Number (VSN) of a drive in a cross-platform way.
	
	Args:
		path (str): The path or drive letter to check (default: root "/").
	
	Returns:
		str: The volume serial number or None if not found.
	"""

	system = platform.system()
	path = os.path.abspath(path).split(os.sep)[0] + os.sep
	try:
		if system == "Windows":
			drive = os.path.splitdrive(path)[0]
			output = subprocess.check_output(f"vol {drive}", shell=True, text=True)
			match = re.search(r"Serial Number is ([\w-]+)", output)
			return match.group(1) if match else None

		elif system == "Linux":
			output = subprocess.check_output(f"lsblk -no UUID {path}", shell=True, text=True)
			return output.strip() if output else None

		elif system == "Darwin":  # macOS
			output = subprocess.check_output(f"diskutil info {path} | grep 'Volume UUID'", shell=True, text=True)
			match = re.search(r"Volume UUID:\s+([\w-]+)", output)
			return match.group(1) if match else None

	except subprocess.CalledProcessError:
		return None  # Command failed
	except Exception as e:
		return (f"[{type(e).__name__}]")

	return None  # Unsupported OS or no result


try:
	import keyboard
except ModuleNotFoundError as m: # Keyboard, optional
	print(f"{colored_warn}{YELLOW}[{type(m).__name__}]{RESET}: {m} - keyboard module (optional) not found.")
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



try: # Google Magika, Python 3.12 - 3.8
	from magika import Magika
	m = Magika()
except Exception as m:
	logging.debug("Magika not found, using mimetypes/magic instead")

if "magika" in sys.modules:
	try: # Test if magika is working
		magika = Magika()
		magika.identify_bytes(content="")
	except Exception as m:
		print(f"{colored_warn} {YELLOW}[{type(m).__name__}]{RESET}: {m}; Magika installed but Magika is not working properly.\n")
		error_logs.append({"name": "magika", "type": str(type(m).__name__), "desc": str(m)})


def timed_choice(question, timeout=10, default=False, timeout_message="\nTimed out! Using default response."):
	# Function to ask a yes/no question with a timeout
	# If y == return True else return False
	try:
		answer = inputimeout(prompt=f"{question} ({UNDERLINE}y{RESET}es/{UNDERLINE}n{RESET}o) [Default: {default}]\n>>> ", timeout=timeout)
		if answer.lower() == 'y' or answer.lower() == 'yes':
			return True
		else:
			return False
	except TimeoutOccurred:
		print(timeout_message)
		return default
	except KeyboardInterrupt:
		print(timeout_message)
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



def shorten_string(string, max_length=20, placeholder="...", keep_filename=False, omit_position='start'):

	"""
	Shortens a given string by replacing parts of it with a placeholder string.

	Parameters:
		string (str): The string to shorten.
		max_length (int, optional): The maximum length of the shortened string. Defaults to 20.
		placeholder (str, optional): The placeholder string to use. Defaults to "...".
		keep_filename (bool, optional): Whether to keep the filename intact. Defaults to False.
		omit_position (str, optional): Where to omit the placeholder string. Options are "start", "end", or "middle". Defaults to "start".

	Returns:
		str: The shortened string.

	Example:
		>>> shorten_string("a" * 30)
		'...aaaaaaaaaaaaaaaaaaaaaaaa'
		>>> shorten_string("a" * 30, keep_filename=True)
		'.../a' * 30
	"""
	if omit_position not in ['start', 'end', 'middle']:
		raise ValueError("omit_position must be 'start', 'end', or 'middle'")
	try:
		if len(str(string)) <= round(max_length):
			return string
		if keep_filename:
			if omit_position == 'start': # omit from start
				return placeholder + "/" + string[-(round(max_length) - len(placeholder)):]
			elif omit_position == 'end': # omit from end
				return string[:round(max_length) - len(placeholder)] + placeholder
			else: # omit middle
				head, tail = os.path.split(string)  # Get directory and filename
				half_len = (round(max_length) - len(tail) - len(placeholder)) // 2
				return head[:half_len] + placeholder + head[-half_len:] + "/" + tail
		else:
			if omit_position == 'start': # omit from start
				return placeholder + string[-(round(max_length) - len(placeholder)):]
			elif omit_position == 'end': # omit from end
				return string[:round(max_length) - len(placeholder)] + placeholder
			else: # omit middle
				half_len = (round(max_length) - len(placeholder)) // 2
				return string[:half_len] + placeholder + string[-half_len:]
	except Exception as e:
		return string

def input_or_exit(prompt, exit_message=f"{colored_stop} Exiting..."):
	""" Prompts the user for input and exits the program if the user presses CTRL+C. """
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

def clear_screen():
	""" Clears the console screen and moves the cursor to the top left corner. """
	os.system('cls' if os.name == 'nt' else 'clear')

def title_console(title):
	""" Sets the title of the console window. """

	if os.name == 'nt': # Windows command prompt
		title = re.sub(r'([&<^%>|])', r'^\1', title)
	else: # Unix-like command prompt
		title = re.sub(r'($"\'*|&;<>#)', r'\\\1', title)
	os.system(f'title {title}' if os.name == 'nt' else f'echo "\033]0;{title}\007"')

def get_partition_from_path(path):
	"""Returns the mount point or drive for a given path."""
	for partition in psutil.disk_partitions():
		if path.startswith(partition.mountpoint):
			return partition  # e.g., "C:\", "/dev/sda1"
	return ["Unknown","Unknown","Unknown","Unknown"]


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
	""" Pauses the program until the user presses Enter. """
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
		".babelrc":"🏗️",
		".DS_Store": "🏷️",
		".dockerignore": "➖",
		".editorconfig": "🔩",
		".eslintrc":"📏",
		".gitattributes": "🔧",
		".gitignore": "➖",
		".gitmodules":"📦",
		".nvmrc":"🏗️",
		".nomedia": "➖",
		".npmignore": "➖",
		".prettierrc":"📏",
		".stylelintrc":"📏",
		"CMakeLists.txt":"🏗️",
		"config.json": "🔧",
		"dockerfile": "🐳",
		"dockerignore": "➖",
		"docker-compose.yml": "🐳",
		"docker-compose.	yaml": "🐳",
		"desktop.ini": "🏷️",
		"database.sqlite": "🗄️",
		"DockerFile": "🐳",
		"error.log":"🚨",
		"jest.config.js": "🃏",
		"Jenkinsfile": "🏗️",
		"log.txt":"📜",
		"Makefile": "🔨",
		"Pipfile": "🐍",
		"package.json": "📦",
		"package-lock.json": "📦",
		"package.json": "📦",
		"yarn.lock": "🔒",
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
		"image/webp": "📸",
		"image/gif": "🎞️",
		"image/xcf": "🖌️",
		"image/RW2": "🏞️",
		"image/PTX": "🏞️",
		"image/RAW": "🏞️",


		# Video
		"video/vnd.dlna.mpeg-tts": "📹",
		"video/x-sgi-movie": "📹",
		"video/x-matroska": "🎥",
		"video/quicktime": "🎬",
		"video/x-msvideo": "🎞️",
		"application/ogg": "🎬",
		"video/x-flv": "🎬",
		"video/webm": "🎥",
		"video/mpeg": "📹",
		"video/3gp": "📼",
		"video/mp4": "🎬",
		"video/ogg": "🎞️",

		# Audio
		"application/vnd.rn-realmedia": "🎙️",
		"application/vnd.apple.mpegurl": "📻",
		"application/x-pn-realaudio": "🎧",
		"application/vnd.ms-wpl": "🎶",
		"audio/x-pn-realaudio": "🎙️",
		"audio/vnd.dlna.adts": "🎧",
		"application/x-cdf": "💿",
		"audio/x-mpegurl": "📻",
		"audio/x-aiff": "🎧",
		"audio/x-midi": "🎹",
		"audio/basic": "🔉",
		"audio/x-wav": "🔉",
		"audio/x-aac": "🎧",
		"audio/3gpp2": "🎙️",
		"audio/mpeg": "🎵",
		"audio/opus": "🎤",
		"audio/3gpp": "🎙️",
		"audio/webm": "🎤",
		"audio/midi": "🎹",
		"audio/mid": "🎹",
		"audio/spx": "🎤",
		"audio/3gp": "🎙️",
		"audio/ogg": "🔉",
		"audio/wav": "🔉",
		"audio/aac": "🎧",
		"audio/mp4": "🎧",

		# Documents
		"application/vnd.ms-xpsdocument": "📝",
		"text/tab-separated-values": "📊",
		"application/x-mimearchive": "🌐",
		"application/x-mswebsite": "🌐",
		"application/x-httpd-php": "🌐",
		"application/xaml+xml": "📑",
		"application/x-mhtml": "🌐",
		"application/x-yaml": "📑",
		"application/pdf": "📕",
		"application/xml": "📑",
		"application/rtf": "📝",
		"application/hta": "🌐",
		"text/markdown": "📝",
		"text/richtext": "📝",
		"text/x-setext": "📜",
		"text/x-vcard": "📇",
		"text/x-sgml": "📜",
		"text/plain": "📄",
		"text/x-rst": "📜",
		"text/plain": "🗒️",
		"text/x-po": "📜",
		"text/html": "🌐",
		"text/xml": "📑",
		"text/vtt": "💬",
		"text/n3": "📖",

		# Microsoft Office
		"application/vnd.ms-officetheme": "🎨",
		"application/vnd.ms-powerpoint": "📽️",
		"application/vnd.ms-excel": "📊",
		"application/vnd.visio": "📊",
		"application/msword": "📘",
		"application/CDFV2": "📘",

		# Microsoft Office Open XML
		"application/vnd.openxmlformats-officedocument.presentationml.presentation": "📽️",
		"application/vnd.openxmlformats-officedocument.presentationml.template": "📽️",
		"application/vnd.openxmlformats-officedocument.wordprocessingml.template": "📘",
		"application/vnd.openxmlformats-officedocument.wordprocessingml.document": "📘",
		"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "📊",
		"application/vnd.ms-word.template.macroEnabled.12": "📘",
		"application/x-msaccess": "🗃️",
		"application/msonenote": "📔",
		"application/msaccess": "🗃️",

		# OpenDocument
		"application/vnd.oasis.opendocument.graphics-template": "🖌️",
		"application/vnd.oasis.opendocument.presentation": "📽️",
		"application/vnd.oasis.opendocument.spreadsheet": "📊",
		"application/vnd.oasis.opendocument.graphics": "🖼️",
		"application/vnd.oasis.opendocument.formula": "🧮",
		"application/vnd.oasis.opendocument.image": "🖼️",
		"application/vnd.oasis.opendocument.chart": "📈",
		"application/vnd.oasis.opendocument.text": "📘",
		"application/oda": "📘",


		# Scripts
		"application/vnd.mozilla.xul+xml": "🦊",
		"application/x-iso9660-image": "💿",
		"application/x-shellscript": "🐚",
		"application/x-java-applet": "☕",
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

		"application/x-powershell": "🚀",
		"text/x-shellscript": "🐚",
		"text/x-msdos-batch": "⚙️",
		"text/javascript": "⚡",
		"text/x-python": "🐍",
		"text/x-perl": "🐫",
		"text/x-ruby": "💎",
		"text/x-java": "☕",
		"text/x-rust": "🦀",
		"text/x-c++": "🔵",
		"text/x-php": "🐘",
		"text/x-go": "🐹",
		"text/css": "🎨",
		"text/csv": "📊",
		"text/xml": "📑",
		"text/x-c": "🔵",


		# Models

		# Fonts
		"application/vnd.font-fontforge-sfd": "🔤",
		"application/vnd.ms-fontobject": "🔤",
		"application/vnd.ms-opentype": "🔤",
		"application/font-sfnt": "🔤",
		"font/woff2": "🔠",
		"font/woff": "🔠",


		# Applications

		# archives
		"application/vnd.android.package-archive": "📱",
		"application/vnd.ms-cab-compressed": "🗄️",
		"application/x-ms-compress-szd": "🗜️",
		"application/x-python-bytecode": "🐍",
		"application/x-apple-diskimage": "📀",
		"application/x-zip-compressed": "🗜️",
		"application/x-rar-compressed": "🗜️",
		"application/x-lzh-compressed": "🗜️",
		"application/x-7z-compressed": "🗜️",
		"application/java-archive": "☕",
		"application/x-compressed": "🗜️",
		"application/x-compress": "🗜️",
		"application/x-archive": "📦",
		"application/vnd.rar": "🗜️",
		"application/x-bzip2": "🗜️",
		"application/x-lzip": "🗜️",
		"application/x-lzma": "🗜️",
		"application/x-gzip": "🗜️",
		"application/x-bzip": "🗜️",
		"application/x-rar": "🗜️",
		"application/x-tar": "📦",
		"application/x-xar": "🗜️",
		"application/x-xz": "🗜️",
		"application/gzip": "🗜️",
		"application/zlib": "🗜️",
		"application/zip": "🗜️",




		# shell
		"application/vnd.microsoft.portable-executable": "🚀",
		"application/x-ms-dos-executable": "🔨",
		"application/x-msdownload": "🚀",
		"application/x-executable": "🛞",
		"application/x-dosexec": "📟",


		# Miscellaneous
		"application/vnd.google-earth.kml+xml": "🗺️",
		"application/vnd.debian.binary-package": "📦",
		"application/vnd.ms-pki.certstore": "🔏",
		"application/windows-library+xml": "📚",
		"application/x-shockwave-flash": "⚡",
		"application/x-bytecode.python": "🐍",
		"application/vnd.ms-pki.seccat": "🔏",
		"application/vnd.tcpdump.pcap":"📡",
		"application/x-java-keystore": "🔐",
		"application/x-x509-ca-cert": "🔏",
		"application/x-python-code": "🐍",
		"application/x-wais-source": "🌐",
		"application/x-ms-shortcut": "🔗",
		"application/x-mach-binary": "🚀",
		"application/x-bittorrent": "📥",
		"application/x-troff-man": "📖",
		"application/x-dosdriver": "🪛",
		"application/pkcs7-mime": "🔐",
		"application/x-mswinurl": "🌐",
		"application/postscript": "🖌️",
		"application/x-terminfo": "🔧",
		"application/x-troff-me": "📜",
		"application/x-troff-ms": "📜",
		"application/x-dos-exec": "🚀",
		"application/x-pem-file": "🔑",
		"application/n-triples": "📊",
		"application/x-sqlite3": "🗃️",
		"application/x-sv4cpio": "📦",
		"application/x-texinfo": "📖",
		"application/x-netcdf": "🌐",
		"application/x-mach-o": "🚀",
		"application/pkix-crl": "🔏",
		"application/x-pkcs12": "🔑",
		"application/x-sv4crc": "📦",
		"application/x-ms-pdb": "🔨",
		"application/n-quads": "📊",
		"application/x-plist": "📑",
		"application/x-bcpio": "📦",
		"application/winhelp": "📖",
		"application/x-latex": "📜",
		"application/x-troff": "📜",
		"application/x-ustar": "📦",
		"application/x-gtar": "📦",
		"application/x-cpio": "📦",
		"application/winhlp": "📖",
		"application/x-hdf5": "💾",
		"application/x-coff": "🚀",
		"application/x-shar": "📦",
		"application/x-csh": "🐚",
		"application/x-dbt": "🗃️",
		"application/x-dvi": "📜",
		"application/x-mif": "📄",
		"application/x-hdf": "💾",
		"application/x-tar": "📦",
		"application/x-tcl": "📜",
		"application/x-tex": "📜",
		"application/x-sql": "🗃️",
		"application/x-sh": "🐚",
		"application/trig": "📊",
		"application/wasm": "⚙️",
		"application/efi": "🛰️",
		"application/chm": "📖",

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
		"OSError": "❗"
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

	# Define a dictionary of folder names and their corresponding icons

	# Whole match
	icons_whole = {

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
		"Application Data": "📚",
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
	}

	for key, value in icons_whole.items():
		if key.lower() == folder_name.lower():
			return value



	# Search for a specific icon by regex
	icons_regex = {
		# "pattern": "icon",

		# General
		r"FOUND.\d\d\d": "🪦",

		# Project-specific
		"__pycache__": "🐍",
		"assets?": "📦",
		"apps?": "📱",
		"admin": "👑",
		"archive": "🏛️",
		"audio": "🎵",
		"build": "🏗️",
		"class": "📚",
		"classes": "📚",
		"configs?": "🔧",
		"console": "🪛",
		"content": "🗄️",
		"container": "📦",
		"css": "🎨",
		"data": "📦",
		"cache": "🧹",
		"custom": "🖋️",
		"docs": "📄",
		"dist": "🎁",
		"database": "🗄️",
		"debug": "🐞",
		"docker": "🐳",
		"dump": "💾",
		"env": "🔬",
		"environment": "🔬",
		"errors?": "🚨",
		"events?": "🔔",
		"examples?": "🧪",
		"exports?": "📤",
		"favicon": "📌",
		"fonts?": "🔤",
		"functions?": "🪛",
		"git": "📓",
		"github": "🐱",
		"gitlab": "🦊",
		"global": "🌐",
		"helpers?": "🪛",
		"hooks?": "🪛",
		"history": "🕰️",
		"i18n": "🗣️",
		"images?": "🖼️",
		"img": "🖼️",
		"imports?": "📥",
		"interfaces?": "🪛",
		"js": "⚡",
		"json": "📜",
		"libs?": "📚",
		"locale": "🗣️",
		"include": "➕",
		"icons?": "📌",
		"javascript": "⚡",
		"json": "📜",
		"js": "⚡",
		"locales?": "🗣️",
		"lib": "📚",
		"logs?": "🧾",
		"langs?": "🗣️",
		"models?": "🧠",
		"mail": "✉️",
		"markdown": "📝",
		"media": "🎥",
		"modules?": "🪛",
		"node_modules": "🐢",
		"notebooks?": "📓",
		"python": "🐍",
		"packages?": "📦",
		"pdf": "📕",
		"plugins?": "🧩",
		"powershell": "🪛",
		"private": "🔒",
		"projects?": "🛠️",
		"public": "🌐",
		"python": "🐍",
		"repositor(y|ies)": "📓",
		"resources?": "📦",
		"reviews?": "👁️‍🗨️",
		"robots?": "🤖",
		"routes?": "🚗",
		"rules?": "☑️",
		"secure": "🔒",
		"rust": "🦀",
		"src": "📜",
		"servers?": "🚀",
		"shaders?": "🛋️",
		"shared?": "📦",
		"src": "📜",
		"storybooks?": "📓",
		"settings?": "⚙️",
		"styles?": "🎨",
		"svg": "📐",
		"scripts?": "📜",
		"tasks?": "☑️",
		"television": "📺",
		"tests?": "🧪",
		"templates?": "🎭",
		"themes?": "🎨",
		"tools?": "⛏️",
		"trash": "🗑️",
		"ui": "🎨",
		"updates?": "⌚",
		"uploads?": "📤",
		"utils?": "🛠️",
		"texts?": "📝",
		"te?mp": "❄️",
		"textures?": "🎨",
		"uploads?": "📤",
		"util": "🛠",
		"venv": "🐍",
		"vscode": "🆚",
		"versions?": "📆",
		"workflows?":"🤖"


	}

	# Search for a specific icon by regex
	for key, value in icons_regex.items():
		if re.search('^'+key+'$', folder_name, re.IGNORECASE):
			return value

	# Default icon
	return "📁"

def get_mime_type(file_path, max_size=10 * 1024 * 1024, force_magic=False, use_magika=False):
	"""
	Get MIME type of a file. Uses file extension for large files and `magic` or `magika` for smaller files.

	Args:
		file_path (str): Path to the file.
		max_size (int): File size threshold for deep MIME detection (default: 10MB).
		force_magic (bool): Force deep MIME detection even for large files.
		use_magika (bool): Use `magika` instead of `magic`.

	Returns:
		str: MIME type of the file.
	"""
	try:
		# First, try detecting MIME type using file extension
		mime = mimetypes.guess_type(file_path)[0]
		if mime and not force_magic:
			return mime  # If detected and deep search is not forced, return immediately

		file_size = os.path.getsize(file_path)
		if file_size > max_size and not force_magic:
			return mime or "application/octet-stream"  # Use extension-based guess if too large

		# Use deep detection if file is small or forced
		if use_magika and "magika" in sys.modules:
			return Magika().identify_path(Path(file_path)).output.mime_type

		if "magic" in sys.modules:
			return magic.from_file(file_path, mime=True)

	except Exception as e:
		sys.stdout.write("\n")
		logging.warning(f"{colored_warn} MIME detection failed for {file_path}: {e}")
		error_logs.append({"name": file_path, "type": str(type(e).__name__), "desc": str(e)})
		return "unknown"

	return mime or "unknown"



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
	global progress, sum_size, magic_scanned
	with progress_lock:
		progress += total_files
		progress_bar.update(total_files)
		try:
			magic_percent = (magic_scanned/progress*100) if progress > 0 else 0
		except ZeroDivisionError:
			magic_percent = 0
		progress_bar.set_description(f"🕷️ | {'🔮 Magika' if use_magika else '🪄 Magic'}: {magic_scanned} [{magic_percent:.1f} %] | 📏 Total: {humanize.naturalsize(sum_size, binary=True)}")


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
			sys.stdout.write("\n")
			if logger.isEnabledFor(logging.DEBUG):
				traceback.print_exc(file=sys.stdout)
			logger.debug(e)
			if "PermissionError" in type(e).__name__:
				logger.warning(f"{colored_no_entry} Permission denied: '{GREY}{path}{RESET}'")
			elif "OSError" in type(e).__name__:
				logger.warning(f"🚫 Access error: '{GREY}{path}{RESET}'")
			elif "FileNotFoundError" in type(e).__name__:
				logger.warning(f"❔ File not found: '{GREY}{path}{RESET}'")
			elif "IsADirectoryError" in type(e).__name__: # Skip junctions
					logger.warning(f"🛤️ Junction skipped: '{GREY}{path}{RESET}'")
			elif "NotADirectoryError" in type(e).__name__:
				logger.warning(f"🚧 Not a directory: '{GREY}{path}{RESET}'")
			elif "FileExistsError" in type(e).__name__: # Skip symbolic links
				logger.warning(f"🔗 Symbolic link skipped: '{GREY}{path}{RESET}'")
			else:
				logger.warning(f"{colored_x} Error: '{GREY}{path}{RESET}' due to {e}")

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
					mime_type = get_mime_type(entry_path, magic_max_size, force_magic, use_magika)
				except Exception as e:
					error_logs.append({"name": path, "type": str(type(e).__name__), "desc": str(e)})
					if args.verbose:
						traceback.print_exc(file=sys.stdout)
					logger.warning(f"{colored_x} Error: '{GREY}{entry_path}{RESET}' due to {e}")
					mime_type = f"{type(e).__name__}"
				file_stat = entry.stat()
				file_size = file_stat.st_size
				sum_size += file_size
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
				scanned_files += 1
				total_size += file_size
			elif entry.is_dir(follow_symlinks=False):
				future = executor.submit(get_folder_structure_threaded, entry_path, progress_bar, error_logs, no_attributes, max_workers, magic_max_size, force_magic, use_magika)
				future_results.append((future, entry_name, entry_path))  # Store folder name & path safely
				scanned_folders += 1

		# Update progress
		update_progress(scanned_files, use_magika)

		for future, folder_name, folder_path in future_results:
			try:
				children, child_size, child_files, child_folders, denied_folders = future.result()
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
				sys.stdout.write("\n")
				if args.verbose:
					traceback.print_exc(file=sys.stdout)
				logger.debug(e)
				if "PermissionError" in type(e).__name__:
					logger.warning(f"{colored_no_entry} Permission denied: '{GREY}{path}{RESET}'")
				elif "OSError" in type(e).__name__:
					logger.warning(f"🚫 Access error: '{GREY}{path}{RESET}'")
				elif "FileNotFoundError" in type(e).__name__:
					logger.warning(f"❔ File not found: '{GREY}{path}{RESET}'")
				elif "IsADirectoryError" in type(e).__name__: # Skip junctions
					logger.warning(f"🛤️ Junction skipped: '{GREY}{path}{RESET}'")
				elif "NotADirectoryError" in type(e).__name__:
					logger.warning(f"🚧 Not a directory: '{GREY}{path}{RESET}'")
				elif "FileExistsError" in type(e).__name__: # Skip symbolic links
					logger.warning(f"🔗 Symbolic link skipped: '{GREY}{path}{RESET}'")
				else:
					logger.warning(f"{colored_x} Error: '{GREY}{path}{RESET}' due to {e}")

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

def get_folder_structure(path, progress_bar=None, error_logs=None, no_attributes=False, magic_max_size = 1 * 1024 * 1024, force_magic=False, use_magika=False, scanned_files=None, scanned_folders=None, magic_scanned=None, denied_folders=None):
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
	global sum_size
	if scanned_files == None:
		scanned_files = 0
	if scanned_folders == None:
		scanned_folders = 0
	if magic_scanned == None:
		magic_scanned = 0
	if denied_folders == None:
		denied_folders = 0

	entries = list(os.scandir(path))
	for entry in entries:
		progress_bar.update(1)
		try:
			magic_percent = magic_scanned/scanned_files*100
		except ZeroDivisionError:
			magic_percent = 0
		dyn_tqdm.set_description(f"🕵️ | {'🔮 Magika' if use_magika else '🪄 Magic'}: {magic_scanned} [{magic_percent:.1f} %] | 📏 Total: {humanize.naturalsize(sum_size, binary=True)} ")

		attributes = get_file_attributes(entry.path) if not no_attributes else None
		'''if entry.is_junction(): # path is a junction
			entry_stat = entry.stat(follow_symlinks=False)
			tree.append({
				"name": entry.name, # Junction name
				"path": entry.path,
				"type": "junction", # whether it is 'folder' or 'file'
				"attr": get_file_attributes(entry.path), # junction attributes
				"size": 0, # junction size in bytes
				"mtime": entry_stat.st_mtime, # junction modification time
				"ctime": entry_stat.st_ctime, # junction creation time
				"atime": entry_stat.st_atime, # junction access time
			})'''

		if entry.is_symlink(): # path is a symbolic link
			entry_stat = entry.stat(follow_symlinks=False)
			tree.append({
				"name": entry.name, # Symbolic link name
				"path": entry.path,
				"type": "symlink", # whether it is 'folder' or 'file'
				"target": os.readlink(entry.path),
				"attr": attributes, # symbolic link attributes
				"size": 0, # symbolic link size in bytes
				"mtime": entry_stat.st_mtime, # symbolic link modification time
				"ctime": entry_stat.st_ctime, # symbolic link creation time
				"atime": entry_stat.st_atime, # symbolic link access time
			})
		elif entry.is_dir(follow_symlinks=False): # path is a directory
			try:
				scanned_folders += 1
				children, child_size, child_files, child_folders, denied_folders = get_folder_structure(entry.path, progress_bar, magic_max_size=magic_max_size, force_magic=force_magic, use_magika=use_magika, scanned_files=scanned_files, scanned_folders=scanned_folders, magic_scanned=magic_scanned, denied_folders=denied_folders)
				total_size += child_size
				entry_stat = entry.stat(follow_symlinks=False)
				tree.append({
					"name": entry.name, # Folder name
					"path": entry.path,
					"type": "folder", # whether it is 'folder' or 'file'
					"size": child_size, # folder size in bytes
					"attr": attributes, # folder attributes
					"mtime": entry_stat.st_mtime, # folder modification time
					"ctime": entry_stat.st_ctime, # folder creation time
					"atime": entry_stat.st_atime, # folder access time
					"files": child_files, # number of files
					"folders": child_folders, # number of subfolders
					"access_denied": False, # whether access is denied
					"children": children, # folder structure
				})
			except Exception as e:
				error_logs.append({"name": path, "type":str(type(e).__name__), "desc": str(e)})
				sys.stdout.write("\n")
				if logger.isEnabledFor(logging.DEBUG):
					traceback.print_exc(file=sys.stdout)
				logger.debug(e)
				if "PermissionError" in type(e).__name__:
					logger.warning(f"{colored_no_entry} Permission denied: '{GREY}{path}{RESET}'")
				elif "OSError" in type(e).__name__:
					logger.warning(f"{colored_no_entry} Access error: '{GREY}{path}{RESET}'")
				elif "FileNotFoundError" in type(e).__name__:
					logger.warning(f"❔ File not found: '{GREY}{path}{RESET}'")
				elif "IsADirectoryError" in type(e).__name__: # Skip junctions
					logger.warning(f"🛤️ Junction skipped: '{GREY}{path}{RESET}'")
				elif "NotADirectoryError" in type(e).__name__:
					logger.warning(f"🚧 Not a directory: '{GREY}{path}{RESET}'")
				elif "FileExistsError" in type(e).__name__: # Skip symbolic links
					logger.warning(f"🔗 Symbolic link skipped: '{GREY}{path}{RESET}'")
				else:
					logger.warning(f"{colored_x} Error: '{GREY}{path}{RESET}' due to {e}")
				entry_stat = entry.stat(follow_symlinks=False)
				tree.append({
					"name": entry.name, # Folder name
					"path": entry.path,
					"type": "folder", # whether it is 'folder' or 'file'
					"size": 0, # folder size in bytes
					"attr": attributes, # folder attributes
					"mtime": entry_stat.st_mtime, # folder modification time
					"ctime": entry_stat.st_ctime, # folder creation time
					"atime": entry_stat.st_atime, # folder access time
					"files": 0, # number of files
					"folders": 0, # number of subfolders
					"access_denied": type(e).__name__, # whether access is denied
					"children": [], # folder structure
				})
				pass  # Skip folders where permission is denied


		elif entry.is_file(follow_symlinks=False): # path is a file
			try:
				mime_type = get_mime_type(entry.path, magic_max_size, force_magic, use_magika)
			except Exception as e:
				error_logs.append({"name": path, "type": str(type(e).__name__), "desc": str(e)})
				if args.verbose:
					traceback.print_exc(file=sys.stdout)
				logger.warning(f"{colored_x} Error: '{GREY}{path}{RESET}' due to {e}")
				mime_type = str(type(e).__name__)
			scanned_files += 1
			file_size = entry.stat().st_size
			total_size += file_size
			# mime_type, _ = mimetyp	es.guess_type(entry.path)
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
			total_size += file_size
			sum_size += file_size
	return tree, total_size, scanned_files, scanned_folders, denied_folders


def get_json_size(data):
	"""Efficiently calculates JSON size by writing it to a temporary file."""
	with tempfile.NamedTemporaryFile(delete=True, mode="w", encoding="utf-8") as temp:
		json.dump(data, temp)  # Stream JSON to file
		temp.flush()  # Ensure data is written
		return os.path.getsize(temp.name)  # Get file size

# Version 3
def compress_json_stream(data, output_file, chunk_size=8192, message="🗜️ Compressing JSON..."):
	"""Compress JSON data efficiently using streaming (avoiding memory overhead)."""
	if not isinstance(chunk_size, int):
		raise TypeError(f"Expected 'chunk_size' to be an integer, but got {type(chunk_size).__name__}")
	
	temp_dir = tempfile.gettempdir()  # Use temp directory
	temp_file = os.path.join(temp_dir, os.path.basename(output_file) + ".tmp.bz2")  # Temporary file path
	print("🧮 Calculating original size...")
	original_size = get_json_size(data)  # Get original size in bytes
	try:
		with bz2.BZ2File(temp_file, 'wb', compresslevel=9) as f_out:
			with tqdm(desc=message, total=original_size, unit="B", unit_scale=True) as dyn_tqdm:
				for chunk in json_iter_encode(data, chunk_size):
					f_out.write(chunk.encode('utf-8'))  # Write chunk
					dyn_tqdm.update(len(chunk))  # Update progress
		compressed_size = os.path.getsize(temp_file)  # Get compressed size in bytes
		shutil.move(temp_file, output_file)  # Move to final location if successful
		print(f"✅ Compression successful! File saved at: {output_file}")

	except Exception as e:
		if logger.isEnabledFor(logging.DEBUG):
			traceback.print_exc(file=sys.stdout)
		print(f"❌ Compression failed: {e}")
		if os.path.exists(temp_file):
			os.remove(temp_file)  # Cleanup temp file if an error occurs
		return original_size, 0
	return original_size, compressed_size

def json_iter_encode(data, chunk_size=8192):
	"""Yield JSON data in small chunks instead of loading the full JSON into memory."""
	encoder = json.JSONEncoder(separators=(',', ':'))  # Compact JSON formatting
	buffer = ""

	for chunk in encoder.iterencode(data):
		buffer += str(chunk)  # Ensure `chunk` is always a string
		while len(buffer) >= chunk_size:
			yield buffer[:chunk_size]  # Yield fixed-size chunks
			buffer = buffer[chunk_size:]  # Keep the remaining part

	if buffer:  # Yield any remaining data
		yield buffer

def edit_get_config(config_file, key, value=None, mode="edit"):
	""" Edit or get a value from the config file. """
	if mode not in ["edit", "get"]:
		raise ValueError(f"Invalid mode: {mode}")
	config = configparser.ConfigParser()
	config.read(config_file)
	if not config.has_section("tree_util"):
		config.add_section("tree_util")
	
	if mode == "edit":
		if value is None:
			raise ValueError("Value is required for 'edit' mode")
		else:
			config["tree_util"][key] = value
			config.set("tree_util", key, value)
			with open(config_file, "w") as conf:
				config.write(conf)
	elif mode == "get":
		return config.get("tree_util", key)

def speed_tier_emoji(speed):
	""" Returns an emoji based on the speed value. """
	speed = float(speed)
	if speed > 30000.0:
		return '⚡'
	elif speed > 20000.0:
		return '💥'
	elif speed > 10000.0:
		return '☄️'
	elif speed > 5000.0:
		return '🚀'
	elif speed > 2500.0:
		return '🔥'
	elif speed > 1000.0:
		return '🌡️'
	elif speed > 500.0:
		return '❄️'
	elif speed > 100.0:
		return '⛄'
	else:
		return '😴'
def save_json_tree(path_to_scan, output_file="folder_structure.json.bz2", simulate=False, no_attributes=False, magic_max_size=1 * 1024 * 1024, use_threads=False, force_magic=False, no_estimates=False, use_magika=False, max_threads=4):

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
	global last_opened_json, config_file
	start_time = time.time()
	absolute_path = os.path.abspath(path_to_scan)
	edit_get_config(config_file, key="last_scan_dir", value=absolute_path, mode="edit")
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
		search_rate = 0
		avg_dir = 0
		dirs_count = 0
		dyn_tqdm_walk = tqdm(os.walk(base_directory),desc="🐍 Calculate total items...", unit=" dirs", smoothing=1.0)
		with ThreadPoolExecutor() as executor:
			# Get a list of subdirectories and files
			timeStart_walk = time.time()
			for dirpath, _, _ in dyn_tqdm_walk:
				dirs_count += 1
				dyn_tqdm_walk.set_description(f"🐍 | 📊 {avg_dir:.1f} files/dir | 📃 {total_items} files | {speed_tier_emoji(search_rate)} {search_rate} files/s")
				future = executor.submit(count_items_in_directory, dirpath)
				total_items += future.result()  # Wait for result and add to total
				try:
					search_rate = f"{(total_items / (time.time() - timeStart_walk)):.2f}"
					avg_dir = total_items / dirs_count
				except ZeroDivisionError:
					search_rate = 0
					avg_dir = 0

		return total_items

	if not no_estimates:
		if use_threads:
			print("🐍 Calculate total items...")
			total_items = count_items_concurrently(path_to_scan)
		else:
			print("🥷 Calculating total items...")
			dyn_tqdm_walk = tqdm(os.walk(path_to_scan),desc="🥷 Calculate total items...", unit=" dirs", smoothing=1.0)
			total_items = []
			dirs_count = 0
			files_count = 0
			search_rate = 0
			avg_dir = 0
			timeStart_walk = time.time()
			for _, _, files in dyn_tqdm_walk:
				dirs_count += 1
				dyn_tqdm_walk.set_description(f"🥷 | 📊 {avg_dir:.1f} files/dir | 📃 {files_count} files | {speed_tier_emoji(search_rate)} {search_rate} files/s")
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
			title_console(f"🕸️ Scanning... - {program_name}")
			print("🕷️ Scanning files...")
			print(f"🧵 Using {max_threads if max_threads > 1 else 'a' if max_threads > 0 else 'no' if max_threads > -1 else max_threads} thread{plural(max_threads)}... (Progress bar may not work properly)")
			global progress, progress_lock, progress_bar
			progress_lock = threading.Lock()
			progress = 0
			with tqdm(total=total_items, desc="🕷️ Scanning files...", unit=" files") as progress_bar:
				structure, total_size, scanned_files, scanned_folders, denied_folders = get_folder_structure_threaded(path_to_scan, progress_bar=progress_bar, error_logs=error_logs, no_attributes=no_attributes, magic_max_size=magic_max_size, force_magic=force_magic, use_magika=use_magika, max_workers=max_threads)
		else:
			title_console(f"📈 Scanning... - {program_name}")
			print("🕵️ Scanning files...")
			dyn_tqdm = tqdm(total=total_items,  unit=" files", smoothing=1.0)
			with dyn_tqdm as progress_bar:
				structure, total_size, scanned_files, scanned_folders, denied_folders = get_folder_structure(path_to_scan, progress_bar=progress_bar, error_logs=error_logs, no_attributes=no_attributes, magic_max_size=magic_max_size, force_magic=force_magic, use_magika=use_magika)
	except KeyboardInterrupt:
		print(f"{colored_stop} Aborted.")
		exit(0)
	end_time = time.time()
	elapsed_seconds = end_time - start_time
	search_rate = f"{(scanned_files / elapsed_seconds):.2f}"
	print(f"\n📋 Results\n")
	print(f" 📄 Total Files: {humanize.intcomma(scanned_files)} | 📂 Total Folders: {humanize.intcomma(scanned_folders)} | 📏 Total Size: {humanize.naturalsize(total_size, binary=True)}")
	print(f" ⏱️ Time Taken: {format_duration(elapsed_seconds)} | {speed_tier_emoji(search_rate)} Search Rate:  {search_rate} files/s\n")

	title_console(f"📝 Enter a note - {program_name}")
	if not args.simulate and timed_choice("📝 Enter a note for the report? ", 10, False, "⏭️ Skipped. You can edit the note later."):
			# not a command, so input prompts is pilcrow
			try:
				user_note = input("¶ ").strip()
			except KeyboardInterrupt:
				user_note = ""
	else:
		user_note = ""

	try:
		partition = get_partition_from_path(absolute_path).fstype
	except Exception as p:
		error_logs.append({"name":"partition", "type":str(type(p).__name__), "desc": str(p)})
		partition = str(type(p).__name__)

	data = { # metadata
		"report_info": {
			"user_note": user_note,
			"error_logs": error_logs,
			"original_path": absolute_path,
			"start_time": start_time,
			"end_time": end_time,
			"partition": partition,
			"total_size": total_size,
			"volume_serial": get_volume_serial_number(absolute_path),
			"volume_label": get_volume_label(absolute_path),
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
			"machine_arch": platform.architecture(),
			"cpu_name": platform.processor(),
			"disk_usage": shutil.disk_usage(path_to_scan),
			"root_mtime": os.path.getmtime(path_to_scan),
			"root_ctime": os.path.getctime(path_to_scan),
			"root_atime": os.path.getatime(path_to_scan),
			"root_attr": get_file_attributes(path_to_scan),
			"threaded": use_threads,
			"max_threads": max_threads,
			"python_version": platform.python_version(),
			"python_implementation": platform.python_implementation(),
			"python_build": platform.python_build(),
			"python_compiler": platform.python_compiler(),
			"python_revision": platform.python_revision(),
		},
		"structure": structure,
	}

	'''def compress_large_json(data, output_file):
		size_total = 0
		with bz2.BZ2File(output_file, 'wb', compresslevel=9) as f_out:
			lines = json.dumps(data).split("\n")
			dyn_tqdm = tqdm(lines, desc="🗜️ Compressing JSON...", unit=" lines")
			for chunk in dyn_tqdm:
				size_total += len(chunk.encode('utf-8'))
				f_out.write(chunk.encode('utf-8'))
				dyn_tqdm.set_description(f"🗜️ Compressing JSON... | {humanize.naturalsize(size_total)} complete")'''

	if simulate:
		print(f"⏭️ Skipping writing file...")
	else:
		print("\n🗜️ Compressing JSON...")
		title_console(f"🗜️ Compressing JSON... - {program_name}")
		# spinner = Spinner()
		# spinner.start() # small spinner animation, but works well
		try:
			original_size, compressed_size = compress_json_stream(data, output_file)
		except KeyboardInterrupt:
			print(f"{colored_stop} Interrupted by user.")
		finally:
			# spinner.stop()
			print(f"📦 JSON has compressed by {round(compressed_size / original_size * 100, 2)} % | {humanize.naturalsize(original_size, binary=True)} ({humanize.intcomma(original_size)} bytes) -> {humanize.naturalsize(compressed_size, binary=True)} ({humanize.intcomma(compressed_size)} bytes) ")
		
	return elapsed_seconds # return time taken

_counter = itertools.count()

def get_top_n_largest(node, n, heap=None, mode="files"):
	"""Get the top n largest files or folders in a directory tree efficiently using a heap."""
	if mode not in {"files", "folders"}:
		raise ValueError(f"Invalid mode: {mode}")

	if heap is None:
		heap = []

	for item in node:
		if mode == "files" and item["type"] != "folder":
			# Use next(_counter) as a tie-breaker
			heapq.heappush(heap, (item["size"], item["path"], next(_counter), item))
		elif mode == "folders" and item["type"] == "folder":
			heapq.heappush(heap, (item["size"], item["path"], next(_counter), item))

		# Keep the heap limited to `n` largest elements.
		if len(heap) > n:
			heapq.heappop(heap)

		# Recursively process children if it's a folder.
		if item["type"] == "folder":
			get_top_n_largest(item["children"], n, heap, mode)

	# Return the n largest items by slicing out the original item stored in index 3.
	return [x[3] for x in heapq.nlargest(n, heap, key=lambda x: (x[0], x[1]))]
	
def get_top_n_recent_files(node, n, heap=None, files=None, mode="new", key="mtime"):
	"""Get the top n largest files in a directory tree efficiently."""
	if heap is None:
		heap = []

	for item in node:
		if item["type"] in {"file", "symlink", "junction"}:
			# Use (size, path, item) to ensure uniqueness and avoid comparison issues
			heapq.heappush(heap, (item["mtime"], item["path"], item))
			if len(heap) > n:
				heapq.heappop(heap)  # Remove the smallest file to keep only top `n`
		elif item["type"] == "folder":
			get_top_n_recent_files(item["children"], n, heap)

	return [x[2] for x in sorted(heap, key=lambda x: x[0], reverse=True)]

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

def search_files(node, query, regex=False, results=None):
	""" Search for files in a directory tree."""
	if results == None:
		results = []
	for item in node:
		if regex: # case-insensitive
			if re.search(query, item["name"], re.IGNORECASE):
				results.append(item)
		else: # case-sensitive
			if query.lower() in item["name"].lower():
				results.append(item)
		if item["type"] == "folder": # recursive
			search_files(item["children"], query, regex, results)
	return results

def search_duplicates(node, seen_files=None, duplicates=None):
	"""Efficiently search for duplicate files by name and size."""
	if seen_files is None:
		seen_files = defaultdict(list)  # Simplifies duplicate tracking
	if duplicates is None:
		duplicates = []

	for item in node:
		if item["type"] == "file":
			key = (item["name"], item["size"])  # Consider both name and size

			if seen_files[key]:  # If key already exists, it's a duplicate
				if len(seen_files[key]) == 1:  # Ensure original is stored only once
					duplicates.append(seen_files[key][0])
				duplicates.append(item)
			
			seen_files[key].append(item)  # Store the file reference

		elif item["type"] == "folder":
			search_duplicates(item["children"], seen_files, duplicates)

	return duplicates  # Avoid sorting unless necessary
def get_most_common_types(node, mode="freq", searchfor="ext", results=None, total_size=None, total_files=None):
	""" Get the top frequent extensions or mime types and sizes in a directory tree."""
	if results is None:
		results = defaultdict(lambda: [0, 0])  # [frequency, size]
	if total_size is None:
		total_size = sum(item["size"] for item in node if item["type"] == "file")
	if total_files is None:
		total_files = sum(1 for item in node if item["type"] == "file")

	for item in node:
		if item["type"] == "file":
			if searchfor == "ext":
				types = os.path.splitext(item["name"])[1].lower()
			elif searchfor == "mime":
				types = item["mime"]
			size = item["size"]
			results[types][0] += 1  # increment frequency
			results[types][1] += size  # add size
		elif item["type"] == "folder":
			get_most_common_types(item["children"], mode, searchfor, results, total_size, total_files)

	# Convert mime types to a dictionary of tuples and add percentage info
	results = {types: (freq, size, size / total_size, freq / total_files) for types, (freq, size) in results.items()}

	# Sort by frequency or size
	if mode == "name":
		return sorted(results.items(), key=lambda x: x[0])
	elif mode == "size":
		return sorted(results.items(), key=lambda x: x[1][1], reverse=True)
	elif mode == "freq":
		return sorted(results.items(), key=lambda x: x[1][0], reverse=True)
	else:
		return sorted(results.items(), key=lambda x: x[1][0], reverse=True)


def find_garbage_files(node, results=None):
	""" Search for garbage files in a directory tree.

	Garbage files are files that are zero bytes in size, or have names that
	match certain patterns. The patterns are based on common temporary or
	backup file names, as well as files that are commonly created by
	operating systems.

	Parameters
	----------
	node : list
		A directory tree node, as returned by `os_tree`.
	results : list, optional
		A list of garbage files found so far. If not provided, a new list
		is created.

	Returns
	-------
	list
		A list of garbage files found in the directory tree.

	Examples
	--------
	>>> import os_tree
	>>> root = os_tree.os_tree(".")
	>>> garbage = find_garbage_files(root)
	>>> print(garbage)
	[{'name': '.DS_Store', 'type': 'file', 'size': 0}, {'name': 'foo.bak', 'type': 'file', 'size': 0}]
	"""

	# Blacklist
	garbage_patterns = r'.*\.(te?mp|log|bak|old|chk|dmp)$|^~.*|Thumbs.db|^\.DS_Store$'

	# Whitelist
	important_pattern = r'.*\.(sys|dll|ini|dat|cfg|lnk|ocx|drv)$'
	folder_whitelist = ['$recycle.bin']#, 'system volume information', 'programdata', 'program files', 'program files (x86)', 'windows', 'system32', 'syswow64', 'winsxs']

	if results == None:
		results = []
	for item in node:
		# If matches blacklist (case-insensitive), or filesize = 0
		if (item["type"] == "file" and re.search(garbage_patterns, item["name"], re.IGNORECASE)) or (item["type"] == "file" and item["size"] == 0):
			# If matches whitelist, do not add to results
			if re.match(important_pattern, item["name"]):
				pass
			else:
				results.append(item)
		if item["type"] == "folder" and item["name"].lower() not in folder_whitelist: # recursive
			find_garbage_files(item["children"], results)
	return results


def set_nth_list(lst, index, value):
	""" Set the value at the specified index in a list, expanding it if necessary."""
	if index >= len(lst):
		lst.extend([None] * (index - len(lst) + 1))  # Expand list with None
	lst[index] = value  # Now it's safe to assign

def convert_markdown_with_external_css(md_text):
	""" Convert markdown text to HTML with external CSS."""
	body = markdown.markdown(md_text, extensions=['tables'])
	style = """table {\n	border-collapse: collapse;\n	width: 100%;\n	will-change: transform;\n}\n
th, td {\n	border: 1px solid black;\n	padding: 8px;\n	text-align: left;\n}\n
th {\n	background-color: #f2f2f2;\n}"""
	styled_html = f"""<!DOCTYPE html>\n<meta charset="utf-8">\n<html>\n<head>\n<style>\n{style}\n</style>\n</head>\n<body>\n{body}\n</body>\n</html>"""
	return styled_html

def repl_str_for_path(path, replace_spaces=True):
	""" Replace characters that cannot be used in a path."""
	path = path.replace(" ", "_") if replace_spaces else path
	return re.sub(r'[<>:"/\\|?*]', '_', path)

# Old functions
def generate_dir_tree(node, level=0):
	"""Generate a directory tree structure."""
	lines = []
	for item in node:
		if item["type"] == "folder":
			lines.append("  " * level + "+ " + item["name"])
			lines.extend(generate_dir_tree(item["children"], level + 1))
		else:
			lines.append("  " * level + "- " + item["name"])

	return lines

# New functions
def generate_tree(node, draw_type="ascii", prefix='', title='', lines=None, show_files=False, show_emojis=False):
	""" Generate a colored string representation of a directory tree."""
	
	# Define tree drawing styles
	valid_styles = {
		"ascii": {"line": "+---", "lastline": r"\---", "vertical": "|   "},
		"box": {"line": "├───", "lastline": "└───", "vertical": "│   "}
	}
	blank = "    "
	
	if draw_type not in valid_styles:
		raise ValueError(f"Invalid draw_type: {draw_type}. Use one of {list(valid_styles.keys())}")

	# Initialize lines
	if lines is None:
		lines = []
		if title:
			lines.append(f"{title}")  # Make the title bold

	style = valid_styles[draw_type]

	# **NEW FIX**: Filter out files if `show_files=False`
	filtered_node = [item for item in node if item["type"] == "folder" or show_files]
	total_entries = len(filtered_node)

	for index, item in enumerate(filtered_node):
		is_last = index == total_entries - 1
		connector = style["lastline"] if is_last else style["line"]
		if show_emojis:
			if item["type"] == "folder":
				connector = f"{connector}{get_folder_icon(item['name'])}"
			elif item["type"] == "file":
				connector = f"{connector}{get_file_icon(item['name'], item['mime'])}"
		if item["type"] == "folder":
			lines.append(prefix + connector + item["name"])
			new_prefix = prefix + (blank if is_last else f"{style['vertical']}")
			generate_tree(item['children'], draw_type=draw_type, prefix=new_prefix, lines=lines, show_files=show_files, show_emojis=show_emojis)
		elif item["type"] == "file" and show_files:
			lines.append(prefix + connector + item["name"])

	return lines


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

def decompress_bz2_to_json(file_path, chunk_size=1024 * 1024):
	"""Decompresses a .bz2 file containing JSON data and returns JSON data,
	original JSON size, and compressed JSON size, using minimal memory.
	
	Args:
		file_path (str): Path to the .bz2 compressed file.
		chunk_size (int, optional): Size of chunks to read. Default is 1MB.
	
	Returns:
		tuple: (json_data, original_size, compressed_size)
	"""
	compressed_size = os.path.getsize(file_path)
	decompressor = bz2.BZ2Decompressor()
	
	json_buffer = io.StringIO()  # Efficient memory usage
	original_size = 0

	with open(file_path, 'rb') as f:
		for chunk in iter(lambda: f.read(chunk_size), b''):
			decompressed_chunk = decompressor.decompress(chunk)
			original_size += len(decompressed_chunk)
			json_buffer.write(decompressed_chunk.decode('utf-8'))

	json_buffer.seek(0)  # Reset pointer before loading JSON
	json_data = json.load(json_buffer)  # Stream directly to JSON

	return json_data, original_size, compressed_size

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

	title_console(f"⏳ Loading JSON... - {program_name}")

	spinner = Spinner(char="emoji_moon2")
	spinner.start() # small spinner animation, but works well
	try:
		'''if "orjson" in sys.modules:
			logger.debug("using orjson")
			with bz2.open(json_file, "rb") as f:  # Open in binary mode
				data = orjson.loads(f.read())
				f.close()
		else:
			with open(json_file, 'rb') as f_in:
				data = json.loads(bz2.decompress(f_in.read()).decode('utf-8'))
				# close file
				f_in.close()'''

		data, original_size, compressed_size = decompress_bz2_to_json(json_file)
		print("\n🧐 Parsing...")


		structure = data["structure"] # The most important part of the data


		edit_get_config(config_file, key="last_opened_json", value=json_file, mode="edit")
	except KeyboardInterrupt:
			print(f"{colored_stop} Interrupted by user.")
	finally:
		spinner.stop()

	# set last opened json
	

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

		global original_path, disk_total, total_size, report_data
		# Keep compatibility
		if "report_info" in data:
			report_data = data["report_info"]
		else:
			report_data = data
		

		disk_total = report_data.get('disk_usage')[0]
		disk_free = report_data.get('disk_usage')[2]
		disk_used = report_data.get('disk_usage')[1]
		disk_free_percentage = disk_free / disk_total * 100
		disk_used_percentage = disk_used / disk_total * 100
		partition_filesystem = report_data.get('partition')
		original_path = report_data.get("original_path").replace("\\", "/")
		elapsed_seconds = report_data.get('end_time') - report_data.get('start_time')
		total_size = report_data.get('total_size')
		search_speed = report_data.get('scanned_files') / elapsed_seconds
		try:
			average_size = report_data.get('total_size') / report_data.get('scanned_files')
		except ZeroDivisionError:
			average_size = 0


		# Generate Report
		global report_info
		report_info = []
		report_info.append(f"\n	📋 Report Info for '{json_file}'\n")
		report_info.append(f" Item			Value")
		report_info.append(f" ----			-----")
		report_info.append(f" 📅 Datetime:		{seconds_to_datetime(report_data.get('start_time'))} - {seconds_to_datetime(report_data.get('end_time'))}	[{humanize.naturaltime(time.time() - report_data.get('end_time'))}]")
		report_info.append(f" ⏱️ Elapsed Time:	{format_duration(elapsed_seconds)}	({elapsed_seconds:.2f} second{plural(round(elapsed_seconds,1))})")
		report_info.append(f" 📑 Report Size:	{humanize.naturalsize(original_size, binary=True)}	({humanize.intcomma(original_size)} byte{plural(original_size)})")
		report_info.append(f" 🗜️ Compressed Size:	{humanize.naturalsize(compressed_size, binary=True)}	({humanize.intcomma(compressed_size)} byte{plural(compressed_size)})	[{compressed_size / original_size * 100:.2f} %]\n")
		report_info.append(f" 🖥️ Computer Name:	{report_data.get('computer_name')}")
		report_info.append(f" 🛰️ System Name:	{report_data.get('system_name')} {report_data.get('system_ver')} {report_data.get('machine_arch')[0]}")
		report_info.append(f" 🏗️ Machine Type:	{report_data.get('machine_type')}\n")
		report_info.append(f" 📍 Original Path:	{original_path}")
		report_info.append(f" 🗃️ Disk Filesystem:	{partition_filesystem}")
		report_info.append(f" 🏷️ Volume Label:	{report_data.get('volume_label')}")
		report_info.append(f" 🔢 Volume Serial:	{report_data.get('volume_serial')}")
		report_info.append(f" 💽 Disk Total:		{humanize.naturalsize(disk_total, binary=True)}	({humanize.intcomma(disk_total)} byte{plural(disk_total)})")
		report_info.append(f" 🈵 Disk Used:		{humanize.naturalsize(disk_used, binary=True)}	({humanize.intcomma(disk_used)} byte{plural(disk_used)})	[{disk_used_percentage:.2f} %]")
		report_info.append(f" 🈳 Disk Free:		{humanize.naturalsize(disk_free, binary=True)}	({humanize.intcomma(disk_free)} byte{plural(disk_free)})	[{disk_free_percentage:.2f} %]\n")
		report_info.append(f" 🪄 Magic max size:	{humanize.naturalsize(report_data.get('magic_max_size', 0), binary=True)}	({humanize.intcomma(report_data.get('magic_max_size'))} byte{plural(report_data.get('magic_max_size'))}) {'[Forced]' if report_data.get('force_magic') else ''}")
		report_info.append(f" 🔮 Magika used:	{report_data.get('use_magika')}")
		try:
			report_info.append(f" 🕵️ Magic scanned:	{humanize.intcomma(report_data.get('magic_scanned'))} file{plural(report_data.get('magic_scanned'))}	[{report_data.get('magic_scanned') / report_data.get('scanned_files') * 100:.2f} %]\n")
		except Exception as z:
			report_info.append(f" 🕵️ Magic scanned:	{humanize.intcomma(report_data.get('magic_scanned'))} file{plural(report_data.get('magic_scanned'))}	[{type(z).__name__} %]\n")
		report_info.append(f" 📊 Scanned Items:	\033[1m{humanize.intcomma(report_data.get('scanned_folders'))}{RESET} folder{plural(report_data.get('scanned_folders'))},	\033[1m{humanize.intcomma(report_data.get('scanned_files'))}{RESET} file{plural(report_data.get('scanned_files'))}")
		report_info.append(f" 📦 Scanned Size:	\033[1m{humanize.naturalsize(report_data.get('total_size'), binary=True)}{RESET} ({humanize.intcomma(report_data.get('total_size'))} byte{plural(report_data.get('total_size'))})")
		report_info.append(f" 🈲 Denied Folders:	{humanize.intcomma(report_data.get('denied_folders'))} folder{plural(report_data.get('denied_folders'))}\n")
		report_info.append(f" ➗ Average Size:	\033[1m{humanize.naturalsize(average_size, binary=True)}{RESET} ({decimal_bytes_to_bits(average_size, True)})" )
		try:
			report_info.append(f" 🗃️ Average files/dir:	{round(report_data.get('scanned_files') / report_data.get('scanned_folders'), 1) } file{plural(report_data.get('scanned_files') / report_data.get('scanned_folders'))}")
		except ZeroDivisionError:
			report_info.append(f" 🗃️ Average files/dir:	0.0 file")
		#report_info.append(f" 🎯 Search Depth:	\033[1m{search_depth}{RESET} level{plural(search_depth)}")
		report_info.append(f" {speed_tier_emoji(search_speed)} Search Speed:	\033[1m{search_speed:.2f}{RESET} files/s\n")
		report_info.append(f" 🧵 Threaded:		{report_data.get('threaded')}")
		report_info.append(f" 📝 User Note:		{report_data.get('user_note')}")
		report_info = ("\n").join(report_info)
		# print(report_info, "\n")

		global error_report
		if report_data["error_logs"]:
			error_report = []
			for idx, error in enumerate(report_data["error_logs"], start=1):
				log = error.get('desc')
				if log == None:
					log = error.get('error')
				if error.get('type') == 'PermissionError':
					error_report.append(f"{idx}.	{colored_no_entry} {log}")
				elif error.get('type') == 'OSError':
					error_report.append(f"{idx}.	{colored_prohibited} {log}")
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
					error_report.append(f"{idx}.	✨ {log}")
				elif error.get('type') == 'NameError':
					error_report.append(f"{idx}.	📛 {log}")
				elif error.get('type') == 'FileNotFoundError':
					error_report.append(f"{idx}.	❔ {log}")
				elif error.get('type') == 'SyntaxError':
					error_report.append(f"{idx}.	🔤 {log}")
				elif error.get('type') == 'MagicException':
					error_report.append(f"{idx}.	🪄 {log}")
				else:
					error_report.append(f"{idx}.	{colored_x} {log}")
			error_report = "\n".join(error_report)
		else:
			error_report = f" {colored_check} No errors found."

	generate_report(data)

	def preview_file(file_path, lines=10): # if lines <= 0, show all
		""" Preview a file """
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
		"name": get_deepest_folder(original_path),
		"type": "folder",
		"path": original_path,
		"size": report_data.get("total_size"),
		"attr": report_data.get("root_attr"),
		"mtime": report_data.get("root_mtime"),
		"ctime": report_data.get("root_ctime"),
		"atime": report_data.get("root_atime"),
		"files": report_data.get("scanned_files"),
		"folders": report_data.get("scanned_folders"),
		"access_denied": False
	}]
	def navigate(node, path="/", selected=None, emoji="🌳", column="size", header=None, sort_action=None):
		"""Navigate through a directory tree."""
		depth = len(path.split("/")) - 2
		title_console(f"{emoji} {shorten_string(path.split('/')[-2] if not path == '/' else path, 50, '…', omit_position='end')} - {program_name}")


		omitted_files = 0
		limit_length = 5000
		# If there are too many files, ask (y/n) if load only top 10000 files
		if len(node) > limit_length:
			print(f"\n	{colored_warn} Too many files: {humanize.intcomma(len(node))}.")
			print(f"	Do you want to load only the top {humanize.intcomma(limit_length)} files? ({UNDERLINE}y{RESET}es/{UNDERLINE}n{RESET}o) default: no")
			ask_load = input()
			if not ask_load.lower() == "n" or ask_load.lower() == "no":
				node = node[:limit_length]
				omitted_files = len(node) - limit_length


		# Function to print the current directory
		def print_top_bar(path="/", file="", additional=""):# Get terminal width
			""" Print the current directory + Set title. """
			logger.debug(f"📂 Dir: {GREY}{depth_dir_info}{RESET}\n🪜 Depth: {depth}")
			# return (f"	📂 Current Directory: {path}\n" + "-" * shutil.get_terminal_size().columns + "\n")
			breadcrumbs_arrow = ' > '
			backslash = '\\'
			return (f"	{emoji}{shorten_string(path+file+additional,shutil.get_terminal_size().columns * 1 / 2, '…').replace('/', breadcrumbs_arrow).replace(backslash, breadcrumbs_arrow)}\n" + "-" * shutil.get_terminal_size().columns + "\n")

		def print_dir(path="/", depth=0, column="size", header=None):
			""" Print a directory."""
			now = time.time()
			print(print_top_bar(path))
			title_console(f"{emoji} {shorten_string(path.split('/')[-2] if not path == '/' else path, 50, '…', omit_position='end')} - {program_name}")
			dir_count = 0
			file_count = 0
			print_list = []
			if header != None:
				print_list.append(header)
			if column == 'path':
				print_list.append(f"#	   Size 	Path")
				print_list.append(f"-	   ----		----")
			else:
				print_list.append(f"#	   {column.title()}		Name")
				print_list.append(f"-	   {'-'*len(column)}		----")
			if column in ["mtime", "ctime", "atime"]:
				print_list.append(f"[0]	🔙  {BOLD}{humanize.naturaltime(now - depth_dir_info[depth][column])}	\033[1m../{RESET}")
			elif column in ["size"]:
				print_list.append(f"[0]	🔙  {BOLD}{humanize.naturalsize(depth_dir_info[depth][column], binary=True)}	\033[1m../{RESET}")
			elif column in ["path"]:
				print_list.append(f"[0]	🔙  {BOLD}{humanize.naturalsize(depth_dir_info[depth]['size'], binary=True)}	\033[1m../{RESET}")
			if depth_dir_info[depth]["access_denied"]:
				print_list.append(f"\n	{colored_no_entry} Access denied: {depth_dir_info[depth]['access_denied']}")

			# Change by column
			for i, item in enumerate(node, start=1):
				# If the file is hidden, show in grey
				if item["name"].startswith(".") or item["attr"].count("Hidden") > 0:
					grey_start = GREY
					grey_end = RESET
				else:
					grey_start = ""
					grey_end = ""
				now = time.time()
				size_display = humanize.naturalsize(item['size'], binary=True)
				name_display = shorten_string(item['name'], shutil.get_terminal_size().columns * 1 / 2, '…', omit_position='middle')
				path_display = shorten_string(item['path'], shutil.get_terminal_size().columns * 1 / 2, '…', omit_position='middle')
				mtime_display = humanize.naturaltime(now - item['mtime'])
				ctime_display = humanize.naturaltime(now - item['ctime'])
				atime_display = humanize.naturaltime(now - item['atime'])

				if item["type"] == "folder":
					icon_display = get_folder_icon(item['name'])
					grey_start = grey_start + BOLD
					grey_end = RESET if not grey_end else grey_end
				elif item["type"] == "symlink":
					icon_display = "🌀"
				else:
					icon_display = get_file_icon(item['name'], item['mime'])

				if column == "size":
					print_list.append(f"{grey_start}[{i}]	{icon_display} {size_display}	{name_display}{grey_end}")
				elif column == "mtime":
					print_list.append(f"{grey_start}[{i}]	{icon_display} {mtime_display}	{name_display}{grey_end}")
				elif column == "ctime":
					print_list.append(f"{grey_start}[{i}]	{icon_display} {ctime_display}	{name_display}{grey_end}")
				elif column == "atime":
					print_list.append(f"{grey_start}[{i}]	{icon_display} {atime_display}	{name_display}{grey_end}")
				elif column == "path":
					print_list.append(f"{grey_start}[{i}]	{icon_display} {size_display}	{path_display}{grey_end}")
				else: # default
					print_list.append(f"{grey_start}[{i}]	{icon_display} {size_display}	{name_display}{grey_end}")

				if item["type"] == "folder":
					dir_count += 1
				else:
					file_count += 1
			print_list.append(f"\n	📁 Directories: {humanize.intcomma(dir_count)} | 📃 Files: {humanize.intcomma(file_count)}")
			return print_list
		def print_file_info(selected):
			""" Print information about a file."""
			try:
				title_console(f"{get_file_icon(selected.get('name'), selected.get('mime'))} {shorten_string(selected.get('name'), 50, '…', omit_position='end')} - {program_name}")
				now = time.time()
				logger.debug(f"📃 Selected file: {GREY}{selected}{RESET}")
				print(print_top_bar(path, selected.get('name')))
				print(f"{get_file_icon(selected.get('name'), selected.get('mime'))} File Information:\n")
				print(f" 📛 Name:	{selected.get('name')}\n")
				print(f" 👣 Location:	{os.path.dirname(selected.get('path'))}")
				print(f" 🗂️ MIME Type:	{selected.get('mime')}\n")
				print(f" 📏 Size:	{humanize.naturalsize(selected.get('size'), binary=True)}	({humanize.intcomma(selected.get('size'))} byte{'s' if selected.get('size') != 1 else ''})")
				print(f" 📅 Created:	{seconds_to_datetime(selected.get('ctime', 0))}	[{humanize.naturaltime(now - selected.get('ctime', 0))}]")
				print(f" 📝 Modified:	{seconds_to_datetime(selected.get('mtime', 0))}	[{humanize.naturaltime(now - selected.get('mtime', 0))}]")
				print(f" 👀 Accessed:	{seconds_to_datetime(selected.get('atime', 0))}	[{humanize.naturaltime(now - selected.get('atime', 0))}]\n")
				print(f" 🔮 Attributes:	{', '.join(selected.get('attr'))}\n")
			except KeyError as e:
				logger.warning(f"{colored_warn} Unknown key: {GREY}{e}{RESET}")

		def print_dir_info(dir_info):
			""" Print information about a directory."""
			try:
				title_console(f"{get_folder_icon(dir_info['name'])} {shorten_string(dir_info['name'], 50, '…', omit_position='end')} - {program_name}")
				now = time.time()
				print(print_top_bar(path))
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

				print(f" 🔮 Attributes:		{', '.join(dir_info.get('attr'))}\n")

			except KeyError as e:
				logger.warning(f"{colored_warn} Unknown key: {GREY}{e}{RESET}")

		def print_link_info(link_info):
			""" Print information about a symlink."""
			try:
				emoji_link = '🌀' if selected.get('type') == 'symlink' else '🛤️'
				title_console(f"{emoji_link} {shorten_string(selected.get('name'), 50, '…', omit_position='end')} - {program_name}")
				now = time.time()
				print(print_top_bar(path))
				print(f"{emoji_link} File Information:\n")
				print(f" 📛 Name:	{selected.get('name')}\n")
				print(f" 👣 Location:	{os.path.dirname(selected.get('path'))}")
				print(f" 🎯 Target:	{link_info.get('target')}\n")
				print(f" 📏 Size:	{humanize.naturalsize(selected.get('size'), binary=True)}	({humanize.intcomma(selected.get('size'))} byte{'s' if selected.get('size') != 1 else ''})")
				print(f" 📅 Created:	{seconds_to_datetime(selected.get('ctime'))}	[{humanize.naturaltime(now - link_info.get('ctime', 0))}]")
				print(f" 📝 Modified:	{seconds_to_datetime(selected.get('mtime'))}	[{humanize.naturaltime(now - link_info.get('mtime', 0))}]")
				print(f" 👀 Accessed:	{seconds_to_datetime(selected.get('atime'))}	[{humanize.naturaltime(now - link_info.get('atime', 0))}]\n")
				print(f" 🔮 Attributes:	{', '.join(selected.get('attr'))}\n")
			except KeyError as e:
				logger.warning(f"{colored_warn} Unknown key: {GREY}{e}{RESET}")


		def open_file(choice, node):
			""" Open a file."""
			global error_message
			if choice.isdigit() and 0 <= int(choice) < len(node) + 1:
				run_path = node[int(choice) - 1]["path"].replace('/', '\\') if int(choice) != 0 else os.path.dirname(node[int(choice) - 1]["path"])
				cmd = ["start", '""', f'"{run_path}"'] if os.name == "nt" else ['xdg-open', f'"{node[int(choice) - 1]["path"]}"']
				title_console(f"🚀 Opening {shorten_string(node[int(choice) - 1]['name'], 50, '…', omit_position='end')} - {program_name}")
				print(f'🚀 Opening selected file with ... `{GREY}{" ".join(cmd)}{RESET}`')
				# run other file
				spinner = Spinner(char='emoji_globe')
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
			""" Edit report user note."""
			title_console(f"📝 Edit Notes - {program_name}")
			print(print_top_bar(path))
			print(report_info, "\n")

			print("\n	📝 Edit Notes (CTRL+C to discard)\n")

			edit_user_note = input("\n¶ ").strip()
			if not edit_user_note == "" or not data["user_note"] == edit_user_note:
				if "report_info" in data:
					data.update({"rerport_info": {"user_note": edit_user_note}})
				else:
					data["user_note"] = edit_user_note

				title_console(f"🗜️ Compressing JSON... - {program_name}")

				try:
					# compressed_data = bz2.compress(json.dumps(data, indent=4).encode('utf-8'))
					# with open(json_file, 'wb') as f_out:
					# 	f_out.write(compressed_data)
					compress_json_stream(data, json_file, message="🗜️ Updating JSON...")
				except KeyboardInterrupt:
					print(f"{colored_stop} Interrupted by user.")
					return
				finally:
					generate_report(data)
					pause()

		def types_results(results, key, search_type="ext"):
			""" Print MIME/extension statistics."""
			while True:
				clear_screen()
				if search_type == "ext":
					title_console(f"📎 Extensions - {program_name}")
					logger.debug(f"📎 Result: {GREY}{results}{RESET}")
					print(print_top_bar(path))
					print(f"\n	📎 Most Common File Extensions - Sorted by {valid_type_keys_desc[valid_type_keys.index(key)]}\n")
					print("#	   Ext.	Count	% Count	Size	% size")
					print("-	   ----	-----	-------	----	------")
					for i, item in enumerate(results, start=1):
						print(f"[{i}]	{get_file_icon('random'+item[0], mimetypes.guess_type('random'+item[0])[0])} {item[0]}	{item[1][0]}	{item[1][3] * 100:.2f} %	{humanize.naturalsize(item[1][1], binary=True)}	{item[1][2] * 100:.2f} %")
					print("\n📌 '/ext /x <key>' to sort, '..' or '/back' to go back\n")
				elif search_type == "mime":
					title_console(f"📎 MIME Types - {program_name}")
					logger.debug(f"📎 Result: {GREY}{results}{RESET}")
					print(print_top_bar(path))
					print(f"\n	📎 Most Common MIME Types - Sorted by {valid_type_keys_desc[valid_type_keys.index(key)]}\n")
					print("#	   MIME		Count	% Count	Size	% size")
					print("-	   ----		-----	-------	----	------")
					for i, item in enumerate(results, start=1):
						print(f"[{i}]	{get_file_icon('', item[0])} {item[0]}		{item[1][0]}	{item[1][3] * 100:.2f} %	{humanize.naturalsize(item[1][1], binary=True)}	{item[1][2] * 100:.2f} %")
					print("\n📌 '/mime /m <key>' to sort, '..' or '/back' to go back\n")
				global error_message
				if not error_message == "":
					print(error_message)
					error_message = ""
				try:
					choice = input(">>> ").strip().lower()
				except KeyboardInterrupt:
					return

				if choice == ".." or choice == "/back" or choice == "/b":
					break
				elif choice == "/exit" or choice == "/quit" or choice == "/q":
					print(f"{colored_stop} Exiting...")
					exit(0)
				# Sort by specific key
				elif choice == "/ext" or choice == "/x" or choice == "/mime" or choice == "/m":
					error_message = (f"{colored_bulb} Usage: /ext [{', '.join(valid_type_keys)}]")
				elif choice.startswith("/ext ") or choice.startswith("/x ") or choice.startswith("/mime ") or choice.startswith("/m "):
					_, k = choice.split(" ", 1)
					if k in valid_type_keys:
						key = k # accepted key
						if key == "freq":
							results = sorted(results, key=lambda x: x[1][0], reverse=True)
						elif key == "size":
							results = sorted(results, key=lambda x: x[1][1], reverse=True)
						elif key == "name":
							results = sorted(results, key=lambda x: x[0], reverse=True)
					else:
						error_message = (f"{colored_warn} Error: Invalid sorting key: {key}")
				elif choice == "/exit" or choice == "/quit" or choice == "/q":
					print(f"{colored_stop} Exiting...")
					exit(0)
				# Number choice, show detailed info about extension, pause
				elif choice.isdigit() and 1 <= int(choice) < len(results) + 1:
					clear_screen()
					extension = results[int(choice) - 1][0]
					if search_type == "ext":
						icon = get_file_icon("random"+extension, mimetypes.guess_type("random"+extension)[0])
						ext_mime_type = f"	[{mimetypes.guess_type('random'+extension)[0]}]"
						ext_mime_type = ext_mime_type if ext_mime_type != None else ""
					elif search_type == "mime":
						icon = get_file_icon("", extension)
						ext_mime_type = ""
					print(print_top_bar(path, additional=extension))
					title_console(f"{icon} {extension} - {program_name}")
					print(f"\n{icon} {'Extension' if search_type == 'ext' else 'MIME Type'}: {extension}{ext_mime_type}\n")
					print(f" 🖇️ Count:	{humanize.intcomma(results[int(choice) - 1][1][0])}")
					print(f" 📏 Size:	{humanize.naturalsize(results[int(choice) - 1][1][1], binary=True)}	({humanize.intcomma(results[int(choice) - 1][1][1])} byte{plural(results[int(choice) - 1][1][1])})")
					print(f" 🛒 Percentage of total frequency:	{results[int(choice) - 1][1][3] * 100:.4f} %")
					print(f" 📐 Percentage of total size:	{results[int(choice) - 1][1][2] * 100:.4f} %")
					print(f" ⚖️ Average size:	{humanize.naturalsize(results[int(choice) - 1][1][1] / results[int(choice) - 1][1][0], binary=True)}	({decimal_bytes_to_bits(results[int(choice) - 1][1][1] / results[int(choice) - 1][1][0],True)})")
					print("\n📌 '/ext /x <key>' to sort, '..' or '/back' to go back\n")
					try:
						pause()
					except KeyboardInterrupt:
						return

		# Sort by name by default
		# node = sorted(node, key=lambda x: x["name"])
		# If sort action, sort entries
		if sort_action:
			node = sorted(node, key=lambda x: x[sort_action], reverse=True)

		selected = None

		valid_sort_keys = ["name", "path", "size", "mime", "ctime", "mtime", "atime", "attr"]
		valid_sort_keys_desc = ["Name", "File Path", "File Size", "MIME Type", "Created Time", "Modified Time", "Accessed Time", "Attributes"]
		valid_type_keys = ["name", "freq", "size"]
		valid_type_keys_desc = ["Name", "Frequency", "Size"]

		while True:
			global error_message
			clear_screen()

			# To append path, use navigate(node, path=path + <name>) function


			print("\n".join(print_dir(path, depth, column)))

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
			if choice == ".." or choice == "/back" or choice == "0":
				if depth == 0:
					exit_or_not = input_or_exit(f"🚪 Are you sure you want to exit? ({UNDERLINE}y{RESET}es/{UNDERLINE}n{RESET}o)", exit_message=f"{colored_stop} Exiting...").lower().strip()
					if exit_or_not == "y" or exit_or_not == "yes":
						depth_dir_info.pop()
						return
				else:
					# print(f"🔙 Going back..." if not depth==0 else print(f"{colored_stop} Exiting..."))
					depth_dir_info.pop()
					return

			elif choice == "/help" or choice == "/h" or choice == "/?":
				clear_screen()
				title_console(f"💡 Help - {program_name}")
				print(print_top_bar(path))
				print("\n💡 Command List\n")
				print(" [NUMBER]	🪜 Navigates to the specified file or directory ")
				print(" CTRL + C	🛑 Returns to the previous directory or exits the program if you are in the root directory.\n")
				print(" /exit /quit /q CTRL + Z\n		🚪 Quits this program")
				print(" /help /h /?	💡 Displays this help message\n")
				print(" .. /back	🔙 Returns to the previous directory")
				print(" /dir /d	📂 Displays the properties of the current directory")
				print(" /del NUMBER 	🚮 Deletes the selected file\n")
				print(" /dup /u	🪞 Displays duplicate files in the current directory")
				print(" /empty /ed	🫙 Displays empty directories in the current directory")
				print(" /error /e	🚨 Displays error message logs from the snapshot report")
				print(" /ext /x (%s)\n" % ", ".join(valid_type_keys), "		📎 Displays the most common file extensions in scanned files. (default key = freq)\n")
				print(" /garbage /g	🗑️ Displays garbage files in the current directory")
				print(" /info /i	📋 Displays snapshot report information")
				print(" /note /n	📝 Edits and saves the user note of the report")
				print(" /mime /m (%s)\n" % ", ".join(valid_type_keys), "		📦 Displays the most common MIME types in scanned files. (default key = freq)")
				print(" /peek /p NUMBER (LINES)\n		👀 Previews file for specified lines (default lines = 20, set 0 to show all data)")
				print(" /recent /r (COUNT)\n		🕰️ Displays the most recently modified files in the current directory")
				print(" /regex /re REGEX\n		🧩 Searches for files or folders using a regular expression")
				print(" /search /find /f STRING\n 		🔎 Searches for files or folders by name")
				print(" /sort /s [%s]\n" % ", ".join(valid_sort_keys), "		📊 Sorts the current directory by a specific key")
				print(" /run /o (NUMBER)\n		🚀 Opens/runs file in system default program")
				print(" /top /t (COUNT)🥇 Displays the top largest file sizes in scanned files. (default count = 10)")
				print(" /topf /tf (COUNT)\n		🏆 Displays the top largest folders in scanned files. (default count = 10)")
				print(" /tree /r -f -e -a\n	 	🌲 Displays the directory tree of the current directory (-f: show files, -a: show in ascii, -e: show emoji icon)")
				print(" /type /y	🎨 Displays file types in the current directory")
				print("\n🛠️ Debug Commands\n")
				print(" /verbose /v	🎚️ Displays verbose output for debugging")
				print(" /@@@@		💀 Warning: Raises an exception for testing purposes\n")
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
				title_console(f"📋 Report info - {program_name}")
				if "report_info" in data:
					logger.debug(f"📋 Report: {GREY}{report_data}{RESET}")
				print(print_top_bar(path))
				print(report_info, "\n\n")
				if total_size > disk_total:
					print("* Note: The scanned size may be bigger than the total disk size. This is because of on-demand cloud storage services.\n")
				pause(exit_message=f"{colored_stop} Exiting...")
			# verbose output
			elif choice == "/verbose" or choice == "/v":
				if logger.getEffectiveLevel() == logging.DEBUG:
					logger.setLevel(logging.INFO)
					error_message = (f"🎚️ Verbosity set to INFO")
				else:
					logger.setLevel(logging.DEBUG)
					error_message = (f"🎚️ Verbosity set to DEBUG")
			elif choice == "/error" or choice == "/e":
				clear_screen()
				title_console(f"🚨 Error logs - {program_name}")
				logger.debug(f"🚨 Error: {GREY}{report_data['error_logs']}{RESET}")
				print(print_top_bar(path))
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
				error_message = (f"{colored_bulb} Usage: /ext [{', '.join(valid_type_keys)}]")
				print("📎 Finding most common file extensions...")
				key = "freq" # default
				spinner = Spinner(char="emoji_clock")
				spinner.start()
				try:
					results = get_most_common_types(node, key, "ext", None, total_size=depth_dir_info[depth].get("size"), total_files=depth_dir_info[depth].get("files"))
				except KeyboardInterrupt:
					print(f"{colored_stop} Exiting...")
					return
				finally:
					spinner.stop()

				if results:
					types_results(results, key, "ext")
				else:
					error_message = (f"{colored_warn} Error: Extensions not found")
			elif choice.startswith("/ext ") or choice.startswith("/x "):
				_, key = choice.split(" ", 1)
				if key in valid_type_keys:
					print("📎 Finding most common file extensions...")
					spinner = Spinner(char="emoji_clock")
					spinner.start()
					try:
						results = get_most_common_types(node, key, None, total_size=data.get("total_size"), total_files=data.get("scanned_files"))
					except KeyboardInterrupt:
						print(f"{colored_stop} Exiting...")
						return
					finally:
						spinner.stop()

					if results:
						types_results(results, key, "ext")
				else:
					error_message = (f"{colored_warn} Error: Invalid sorting key: {key}")
			# Display the most common file mime types
			elif choice == "/mime" or choice == "/m":
				error_message = (f"{colored_bulb} Usage: /mime [{', '.join(valid_type_keys)}]")
				print("📎 Finding most common file mime types...")
				key = "freq" # default
				spinner = Spinner(char="emoji_clock")
				spinner.start()
				try:
					results = get_most_common_types(node, key, "mime", None, total_size=depth_dir_info[depth].get("size"), total_files=depth_dir_info[depth].get("files"))
				except KeyboardInterrupt:
					print(f"{colored_stop} Exiting...")
					return
				finally:
					spinner.stop()

				if results:
					types_results(results, key, "mime")
				else:
					error_message = (f"{colored_warn} Error: MIME types not found")
			elif choice.startswith("/mime ") or choice.startswith("/m "):
				_, key = choice.split(" ", 1)
				if key in valid_type_keys:
					print("📎 Finding most common file MIME types...")
					spinner = Spinner(char="emoji_clock")
					spinner.start()
					try:
						results = get_most_common_types(node, key, None, total_size=data.get("total_size"), total_files=data.get("scanned_files"))
					except KeyboardInterrupt:
						print(f"{colored_stop} Exiting...")
						return
					finally:
						spinner.stop()

					if results:
						types_results(results, key, "mime")
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
					selected = node[int(n) - 1]
					if selected["type"] == "file":# and selected.get("mime", "").startswith("text")
						if not "text" in selected.get("mime", ""):
							print(f"{colored_warn} Selected file is not recognized as a text file. ({GREY}{selected['mime']}{RESET})")
							print(f"Proceeding may cause your terminal to break. Proceed? ({UNDERLINE}y{RESET}es/{UNDERLINE}n{RESET}o)\n")
							try:
								ask_peek = input(">>> ").lower().strip()
							except KeyboardInterrupt:
								ask_peek = None
							if not ask_peek == "y" or ask_peek == "yes":
								continue
						clear_screen()
						title_console(f"👀 Previewing {shorten_string(selected['name'], 50, '…', omit_position='end')} - {program_name}")
						print(print_top_bar(path))
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
			# Find garbage files
			elif choice == "/garbage" or choice == "/g":
				print("🗑️ Finding garbage files...")
				spinner = Spinner(char="emoji_clock")
				spinner.start()
				try:
					results = find_garbage_files(node)
				except KeyboardInterrupt:
					print(f"{colored_stop} Exiting...")
					return
				finally:
					spinner.stop()

				if results:
					set_nth_list(depth_dir_info, depth+1,
					{
						"name": "Searched Garbage Files",
						"path": "<search:garbage>",
						"type": "folder",
						"size": (sum([f["size"] for f in results]) if results else 0),
						"attr": [],
						"ctime": 0, # undefined
						"mtime": 0, # undefined
						"atime": 0, # undefined
						"files": sum(1 if f["type"] == "file" else 0 for f in results),
						"folders": sum(1 if f["type"] == "folder" else 0 for f in results),
						"access_denied": False
					}
					)

					navigate(results, path + "[garbage files]/", emoji="🗑️", column="path")
				else:
					error_message = (f"{colored_check} No garbage files found.")
			# Delete a file with confirmation
			elif choice == "/del":
				error_message = (f"{colored_bulb} Usage: /del NUMBER")
			elif choice.startswith("/del "):
				_, n = choice.split(" ", 2)
				if n.isdigit() and 0 <= int(n) < len(node):
					selected = node[int(n) - 1]
					if selected["type"] == "file":
						#ask
						ask_delete = False
						try:
							ask_delete = timed_choice(f"🚮 Are you sure you want to delete: '{GREY}{selected['path']}{RESET}'? (Timeout in 5s)", timeout=5, default=False, timeout_message="\nTimed out! Not deleting.")
						except KeyboardInterrupt:
							return
						if ask_delete:
							spinner = Spinner(char='emoji_globe')
							spinner.start()
							try:
								os.remove(selected["path"])
								error_message = (f"🚮 Deleted: {selected['name']}")
							except KeyboardInterrupt:
								spinner.stop()
								print(f"{colored_stop} Exiting...")
								return
							finally:
								spinner.stop()
					else:
						error_message = (f"{colored_warn} Error: Selected item is not a file")
				else:
					error_message = (f"{colored_warn} Error: Invalid file number: {n}")

			# Sort the directory
			elif choice == "/sort" or choice == "/s":
				error_message = (f"{colored_bulb} Usage: /sort [{', '.join(valid_sort_keys)}]")
			elif choice.startswith("/sort ") or choice.startswith("/s "):
				key = choice.split(" ")[1]
				if key not in valid_sort_keys:
					error_message = (f"{colored_warn} Error: Invalid sorting key: {key}")
				else:
					print(f"📊 Sorting list by {valid_sort_keys_desc[valid_sort_keys.index(key)]}...")
					spinner = Spinner(char="emoji_clock")
					spinner.start()
					try:
						node = sorted(node, key=lambda x: x[key], reverse=True)
						column = key
						error_message = f"📊 Sorted list by {valid_sort_keys_desc[valid_sort_keys.index(key)]}"
					except KeyboardInterrupt:
						spinner.stop()
						
						print(f"{colored_stop} Exiting...")
						return
					finally:
						spinner.stop()

			# Search for a file or folder
			elif choice == "/search" or choice == "/find" or choice == "/f":
				error_message = (f"{colored_bulb} Usage: /search STRING")
			elif choice.startswith("/search ") or choice.startswith("/find ") or choice.startswith("/f "):
				_, query = choice.split(" ", 1)
				print("🔎 Searching...")
				try:
					spinner = Spinner(char="emoji_clock")
					spinner.start()
					results = search_files(node, query)
					spinner.stop()
			

					if len(results) > 0:
						set_nth_list(depth_dir_info, depth+1,
						{
							"name": "Searched for: " + query,
							"path": "<search:string>",
							"type": "folder",
							"size": (sum([f["size"] for f in results]) if results else 0),
							"attr": [],
							"ctime": 0,
							"mtime": 0,
							"atime": 0,
							"files": sum(1 if f["type"] == "file" else 0 for f in results),
							"folders": sum(1 if f["type"] == "folder" else 0 for f in results),
							"access_denied": False
						}
						)
						navigate(results, path + f"[Search: {query}]/", emoji="🔎", header=f"	🔎 Search Results for '{GREY}{query}{RESET}'\n")
					else:
						error_message = (f"{colored_exclamation} No results found for '{GREY}{query}{RESET}'")
				# Search for a file or folder using a regular expression
				except KeyboardInterrupt:
					spinner.stop()
					print(f"{colored_stop} Exiting...")
					return
				except Exception as e:
					spinner.stop()
					error_message = (f"{colored_exclamation} [{type(e).__name__}]: {e}")

			elif choice == "/regex" or choice == "/re":
				error_message = (f"{colored_bulb} Usage: /regex REGEX")
			elif choice.startswith("/regex ") or choice.startswith("/re "):
				_, regex = choice.split(" ", 1)
				regex = " ".join(regex.split())
				print("🧩 Searching...")
				try:
					spinner = Spinner(char="emoji_clock")
					spinner.start()
					results = search_files(node, regex, True)
					spinner.stop()
	
					if len(results) > 0:
						set_nth_list(depth_dir_info, depth+1,
						{
							"name": "Regex: " + regex,
							"path": "<search:regex>",
							"type": "folder",
							"size": (sum([f["size"] for f in results]) if results else 0),
							"attr": [],
							"ctime": 0,
							"mtime": 0,
							"atime": 0,
							"files": sum(1 if f["type"] == "file" else 0 for f in results),
							"folders": sum(1 if f["type"] == "folder" else 0 for f in results),
							"access_denied": False
						}
						)
						navigate(results, path + f"[Regex: {regex}]/", header=f"	🧩 Search Results for Regex: `{GREY}{regex}{RESET}`\n", emoji="🧩")
					else:
						error_message = (f"{colored_exclamation} No results found for '{GREY}{regex}{RESET}'")
				except KeyboardInterrupt:
					spinner.stop()
					print(f"{colored_stop} Exiting...")
					return
				except Exception as e:
					spinner.stop()
					error_message = (f"{colored_exclamation} [{type(e).__name__}]: {e}")


			# Show empty directories
			elif choice == "/empty" or choice == "/ed":
				title_console(f"🫙 Empty Folders - {program_name}")

				print("🫙 Searching Empty Folders...")
				try:
					spinner = Spinner(char="emoji_clock")
					spinner.start()
					results = search_empty_folders(node)
					spinner.stop()
					if len(results) > 0:
						set_nth_list(depth_dir_info, depth+1,
						{
							"name": "Empty directories",
							"path": "<search:empty_dirs>",
							"type": "folder",
							"size": (sum([f["size"] for f in results]) if results else 0),
							"attr": [],
							"ctime": 0,
							"mtime": 0,
							"atime": 0,
							"files": sum(1 if f["type"] == "file" else 0 for f in results),
							"folders": sum(1 if f["type"] == "folder" else 0 for f in results),
							"access_denied": False
						}
						)
						navigate(results, path + "[Empty directories]/", header="	🫙 Empty directories\n", emoji="🫙")
					else:
						error_message = (f"{colored_check} No empty directories found.")
				except KeyboardInterrupt:
					spinner.stop()
					print(f"{colored_stop} Exiting...")
					return
				except Exception as e:
					spinner.stop()
					error_message = (f"{colored_exclamation} [{type(e).__name__}]: {e}")
			# Show duplicate files
			elif choice == "/dup" or choice == "/u":
				title_console(f"🪞 Duplicate Files - {program_name}")

				print("🪞 Searching Duplicates...")
				try:
					spinner = Spinner(char="emoji_clock")
					spinner.start()
					results = search_duplicates(node)
					spinner.stop()

					if len(results) > 0:
						set_nth_list(depth_dir_info, depth+1,
						{
							"name": "Duplicate Files",
							"path": "<search:empty_files>",
							"type": "folder",
							"size": (sum([f["size"] for f in results]) if results else 0),
							"attr": [],
							"ctime": 0,
							"mtime": 0,
							"atime": 0,
							"files": sum(1 if f["type"] == "file" else 0 for f in results),
							"folders": sum(1 if f["type"] == "folder" else 0 for f in results),
							"access_denied": False
						}
						)
						navigate(results, path + "[Duplicate Files]/", header="	🪞 Duplicate Files\n", emoji="🪞", column="path")
					else:
						error_message = (f"{colored_check} No duplicate files found.")
				except KeyboardInterrupt:
					spinner.stop()
					print(f"{colored_stop} Exiting...")
					return
				except Exception as e:
					spinner.stop()
					error_message = (f"{colored_exclamation} [{type(e).__name__}]: {e}")

			elif choice == "/tree" or choice == "/r" or choice.startswith("/tree ") or choice.startswith("/r "):
				if choice.startswith("/tree ") or choice.startswith("/r "):
					options = choice.split(" ")
					if "-f" in options:
						show_files = "true"
					else:
						show_files = "false"
					if "-a" in options:
						draw_type = "ascii"
					else:
						draw_type = "box"
					if "-e" in options:
						show_emojis = "true"
					else:
						show_emojis = "false"
				else:
					show_files = "false"
					draw_type = "box"
					show_emojis = "false"
				if show_files in ["true", "false"] and draw_type in ["ascii", "box"] and show_emojis in ["true", "false"]:
					show_files = True if show_files == "true" else False
					show_emojis = True if show_emojis == "true" else False
					clear_screen()
					try:
						print("🌲 Generating tree view...")
						spinner = Spinner(char="emoji_clock")
						spinner.start()
						tree_view = ("\n".join(generate_tree(node, draw_type=draw_type, title=depth_dir_info[depth]['name'], show_files=show_files, show_emojis=show_emojis)))
						spinner.stop()
						clear_screen()
						print(tree_view)
					except KeyboardInterrupt:
						print(f"{colored_stop} Exiting...")	
					print(f"\n🌲 Would you like to save tree view to .txt file? ({UNDERLINE}y{RESET}es/{UNDERLINE}n{RESET}o)")
					try:
						ask_save = input(">>> ").lower().strip()
					except KeyboardInterrupt:
						ask_save = None
					if ask_save == "y" or ask_save == "yes":
						tree_save_txt = f"tree_view_{seconds_to_datetime(time.time(), True)}.txt"
						with open(tree_save_txt, "w") as f:
							f.write(tree_view)
						error_message = f"🌲 Tree saved to {tree_save_txt}"
				else:
					error_message = (f"{colored_warn} Error: Invalid arguement: {options[1:]}")
			# Show directory info
			elif choice == "/dir" or choice == "/d":
				clear_screen()
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
					title_console(f"🕰️ Recent files - {program_name}")
					print("🕰️ Searching...")
					try:
						spinner = Spinner(char="emoji_clock")
						spinner.start()
						results = get_top_n_recent_files(node, n)
						spinner.stop()
						if len(results) > 0:
							set_nth_list(depth_dir_info, depth+1,
							{
							"name": "Top " + str(n) + " recent files",
							"path": "<search:recent_files>",
							"type": "folder",
							"size": (sum([f["size"] for f in results]) if results else 0),
							"attr": [],
							"ctime": 0,
							"mtime": 0,
							"atime": 0,
							"files": sum(1 if f["type"] == "file" else 0 for f in results),
							"folders": sum(1 if f["type"] == "folder" else 0 for f in results),
							"access_denied": False
						}
						)
							navigate(results, path + f"[Top {n} recent files]/", header=f"	🕒 Recent files ({n})\n", column="mtime", emoji="🕒", sort_action="mtime")
						else:
							error_message = (f"{colored_exclamation} No results found for '{n}'")
					except KeyboardInterrupt:
						spinner.stop()
						print(f"{colored_stop} Exiting...")
						return
					except Exception as e:
						spinner.stop()
						error_message = (f"{colored_exclamation} [{type(e).__name__}]: {e}")

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
					try:
						spinner = Spinner(char="emoji_clock")
						spinner.start()
						results = get_top_n_largest(node, n, mode="folders")
						spinner.stop()

						if len(results) > 0:
							set_nth_list(depth_dir_info, depth+1,
							{
							"name": "Top " + str(n) + " Largest Folders",
							"path": "<search:largest_folders>",
							"size": (sum([f["size"] for f in results]) if results else 0),
							"attr": [],
							"ctime": 0,
							"mtime": 0,
							"atime": 0,
							"files": sum(1 if f["type"] == "file" else 0 for f in results),
							"folders": sum(1 if f["type"] == "folder" else 0 for f in results),
							"access_denied": False
						}
						)
							navigate(results, path + f"[Top {n} Largest Folders]/", header=f"	🏆 Top {n} Largest Folders\n", column="size", emoji="🏆", sort_action="size")
						else:
							error_message = (f"{colored_exclamation} Top {n} folders not found")
					except KeyboardInterrupt:
						spinner.stop()
						print(f"{colored_stop} Exiting...")
						return
					'''except Exception as e:
						spinner.stop()
						error_message = (f"{colored_exclamation} [{type(e).__name__}]: {e}")'''


					
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
					try:
						spinner = Spinner(char="emoji_clock")
						spinner.start()
						results = get_top_n_largest(node, n, mode="files")
						spinner.stop()
						if len(results) > 0:
							selected = results[0]
							set_nth_list(depth_dir_info, depth+1,
							{
							"name": "Top " + str(n) + " Largest Files",
							"path": "<search:largest_files>",
							"type": "folder",
							"size": (sum([f["size"] for f in results]) if results else 0),
							"attr": [],
							"ctime": 0,
							"mtime": 0,
							"atime": 0,
							"files": sum(1 if f["type"] == "file" else 0 for f in results),
							"folders": sum(1 if f["type"] == "folder" else 0 for f in results),
							"access_denied": False
						}
						)
							navigate(results, path + f"[Top {n} Largest Files]/", header=f"	🥇 Top {n} Largest Files\n", column="size", emoji="🥇", sort_action="size")
						else:
							error_message = (f"{colored_exclamation} Top {n} files not found")
					except KeyboardInterrupt:
						spinner.stop()
						print(f"{colored_stop} Exiting...")
						return
					except Exception as e:
						spinner.stop()
						error_message = (f"{colored_exclamation} [{type(e).__name__}]: {e}")
						
			elif choice == "/run" or choice == "/o":
				# open current directory
				cmd = ['start','""', f"\"{depth_dir_info[-1]['path']}\""] if os.name == "nt" else ['xdg-open', f'"{original_path[:-1]}{path}"']
				print(f'🚀 Opening current directory with explorer... `{GREY}{" ".join(cmd)}{RESET}`')
				spinner = Spinner(char="emoji_globe")
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
			elif choice == ("/@@@@"):
				# raise ZeroDivisionError
				error_message = (1/0)
			# Number navigation
			elif choice.isdigit() and 0 <= int(choice) < len(node) + 1:
				selected = node[int(choice) - 1]
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
					navigate(selected["children"], path + selected["name"] + "/", emoji=get_folder_icon(selected["name"]))
				elif selected["type"] in ["file", "junction", "symlink"]:
					clear_screen()
					if selected["type"] in ["junction", "symlink"]:
						print_link_info(selected)
					else:
						print_file_info(selected)
					pause(exit_message=f"{colored_stop} Exiting...")
			elif choice.isnumeric() or choice.isdigit() and (int(choice) < 0 or int(choice) >= len(node)):
				error_message = f"{colored_warn} Invalid choice: {choice}"
			#else:
			#	error_message = f"{colored_warn} Unknown command: {choice}"
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
		>>> naturalsize_to_int("5Gi")0
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
	computername = f"{platform.system()}_{platform.node()}"

	if os.name == "nt":  # Windows
		label = get_volume_label(path[:1])
		return parts[-1] if len(parts) > 1 else label if not label == None else path[:1]  # Drive letter if root
	else:  # Linux/macOS
		label = get_volume_label(path)
		return parts[-1] if len(parts) > 1 else computername

def todo(message):
	"""
	Returns a formatted string with a green-colored reminder message.

	Parameters:
		message (str): The reminder message to be formatted.

	Returns:
		str: A formatted string with the reminder message.
	"""
	return(f"\033[32m📌 [Reminder]\033[0m - {message}\n")

def get_optimal_workers():
	total_memory = psutil.virtual_memory().total
	return max(2, min(10, total_memory // (512 * 1024 * 1024)))  # Example: Adjust dynamically

def main(args):
	global directory,json_file, scan_log_dir, action, threaded, gui_enabled, main_menu_enabled, error_message, open_after_scan, force_magic, use_magika, magic_max_size, max_threads,last_opened_json, last_scan_dir
	magic_max_size = naturalsize_to_int(args.threshold)
	directory = None
	json_file = None
	# Create the scan log directory
	root_log_dir = "./logs"
	scan_log_dir = f"{root_log_dir}/{platform.node()}"
	if not os.path.exists(scan_log_dir):
		try:
			os.mkdir(scan_log_dir)
		except:
			scan_log_dir =  "./logs"
			os.mkdir(scan_log_dir)
	if os.path.exists(config_file):
		last_opened_json = ""
		last_scan_dir = ""
		try:
			last_opened_json = edit_get_config(config_file, "last_opened_json", mode="get")
		except Exception:
			last_opened_json = ""
		try:
			last_scan_dir = edit_get_config(config_file, "last_scan_dir", mode="get")
		except Exception:
			last_scan_dir = ""
	else:
		last_opened_json = ""
		last_scan_dir = ""

	no_attributes = args.no_attributes

	threaded = args.threads
	if args.max_threads:
		max_threads = args.max_threads
	else: #get optimal number of threads
		max_threads = get_optimal_workers()
	gui_enabled = args.gui
	open_after_scan = args.explore
	error_message = ""
	force_magic = args.force_magic
	try:
		use_magika = args.use_magika
	except AttributeError:
		use_magika = False

	def main_menu():
		global action, threaded, directory, gui_enabled, main_menu_enabled, magic_max_size, json_file, error_message, open_after_scan, force_magic, use_magika, max_threads, last_opened_json, last_scan_dir	
		main_menu_enabled = True
		while True:
			if os.path.exists(config_file):
				try:
					last_opened_json = edit_get_config(config_file, "last_opened_json", mode="get")
				except Exception:
					last_opened_json = ""
				try:
					last_scan_dir = edit_get_config(config_file, "last_scan_dir", mode="get")
				except Exception:
					last_scan_dir = ""
			title_console("🌳 Tree Spider: Threaded Edition")
			clear_screen()
			json_file = ''
			directory = ''
			print("\n📍 Enter commands to begin:\n")
			print(" 🖥️ Main commands\n")
			print(f"  📂 Scan a directory:	'{GREY}scan{RESET}', '{GREY}s{RESET}'")
			if last_scan_dir:
				print(f"  ⌚ Scan Again:	'{GREY}again{RESET}', '{GREY}a{RESET}'{'	['+ last_scan_dir+']' if last_scan_dir else ''}")
			print(f"\n  📑 Explore JSON:	'{GREY}browse{RESET}', '{GREY}b{RESET}'")
			if last_opened_json:
				print(f"  🗓️ Last opened JSON:	'{GREY}last{RESET}', '{GREY}l{RESET}'{'	['+ last_opened_json+']' if last_opened_json else ''}")
			print("\n 🔧 Scan Settings\n")
			print(f"  📏 Magic max size [{humanize.naturalsize(magic_max_size, binary=True)}]:	'{GREY}magic{RESET}', '{GREY}m{RESET}'")
			if "magika" in sys.modules:
				print(f"  🔮 Use magika [{use_magika}]:	'{GREY}magika{RESET}', '{GREY}k{RESET}'")
			else:
				print(f"  {GREY}🔮 Use magika [Unavailable]:	'magika', 'k'{RESET}")
			print(f"  🪄 Force magic [{force_magic}]:	'{GREY}force{RESET}', '{GREY}f{RESET}'")
			print(f"  🧵 Threads [{threaded}]:		'{GREY}threads{RESET}', '{GREY}t{RESET}'")
			print(f"  🕸️ Max threads [{max_threads}]:	'{GREY}max{RESET}', '{GREY}x{RESET}'")
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
			elif action == 'again' or action == 'a':
				scan_again()
			elif action == 'last' or action == 'l':
				open_last_opened()
			elif action == "magic" or action == "m":
				title_console("📏 Set Threshold ")
				print("📏 Set MIME threshold:")
				print(f"Current: {humanize.naturalsize(magic_max_size, binary=True)} ({humanize.intcomma(magic_max_size)} byte{plural(magic_max_size)})")

				while True:
					try:
						magic_max_size = naturalsize_to_int(input(">>> "))
						break
					except ValueError:
						error_message = (f"{colored_warn} Invalid input. Please enter a number.")
					except KeyboardInterrupt:
						break
				error_message = (f"📏 New threshold: {humanize.naturalsize(magic_max_size, binary=True)} ({humanize.intcomma(magic_max_size)} byte{plural(magic_max_size)})")

			elif action == "magika" or action == "k":
				if "magika" in sys.modules:
					use_magika = not use_magika
					error_message = (f"🔮 Use magika {'enabled' if use_magika else 'disabled'}")
				else:
					error_message = (f"🔮 To install magika, run `{GREY}pip install magika{RESET}`. Requires Python 3.8 - 3.12. ")
			elif action == "t" or action == "threads":
				threaded = not threaded
				error_message = (f"🧵 Threads {'enabled' if threaded else 'disabled'}")
			elif action == "x" or action == "max":
				title_console("🕸️ Set Max Threads: ")
				print("🕸️ Set Max Threads:")
				print(f"Current: {max_threads}")

				while True:
					try:
						max_threads = int(input(">>> "))
						break
					except ValueError:
						error_message = (f"{colored_warn} Invalid input. Please enter a number.")
					except KeyboardInterrupt:
						break
				error_message = (f"🕸️ New Max Threads: {max_threads}")
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
				print(f"🔄️ Reloading...")
				error_message = (f"✨ Reloaded!")
				exec(open(__file__).read())
			elif action == "exit" or action == "quit" or action == "q" or action == "..":
				print(f"{colored_stop} Exiting...")
				exit()
			elif not action:
				if main_menu_enabled == True:
					main_menu()
				else:
					logger.error(error_message)
					exit(1)

			else:
				error_message = (f"{colored_warn} Invalid action. Please enter 'scan' or 'browse'.")
				if main_menu_enabled == True:
					main_menu()
				else:
					logger.error(error_message)
					exit(1)

	def scan_mode():
		global directory, error_message
		title_console(f"📂 Select Folder - {program_name}")
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
				try:
					directory = input(">>> ")
				except:
					return
			if not directory:
				error_message = (f"{colored_warn} No directory path provided.")
				if main_menu_enabled:
					main_menu()
				else:
					logger.error(error_message)
					exit(1)
			elif not os.path.isdir(directory):
				error_message = (f"{colored_warn} Invalid directory path: '{directory}'")
				directory = ''
				if main_menu_enabled:
					main_menu()
				else:
					logger.error(error_message)
					exit(1)

		if args.output:
			output_file = args.output
		else:
			default_output_file = f"{get_deepest_folder(directory)[:50]}_{seconds_to_datetime(time.time(), True)}.structure.json.bz2"

			if not args.simulate:
				title_console(f"💾 Output File - {program_name}")
				if gui_enabled: # Set save location
					root = Tk()
					root.withdraw()
					root.attributes("-topmost", True)
					print("💾 Select the output file path:")
					output_file = filedialog.asksaveasfilename(title="Select the output file", defaultextension=".json.bz2", initialdir=scan_log_dir, initialfile=default_output_file, filetypes=[("BZip2 JSON File", "*.json.bz2")])
					root.destroy()
					if not output_file:
						print(f"{colored_warn} No output file path provided.")
						if main_menu_enabled:
							main_menu()
						else:
							exit(1)
					print(f" '{output_file}'")
				else:
					print(f"💾 Enter the output file path (leave blank for default name / CTRL+C to cancel): ")
					try:
						output_file = input(">>> ").strip()
					except KeyboardInterrupt:
						return
					if not output_file:
						output_file = scan_log_dir +"/"+ default_output_file
						logger.warning(f"{colored_warn} No output file path provided. Defaulting to '{GREY}{output_file}{RESET}'")
					elif output_file.endswith(".json"):
						output_file += ".bz2"
					elif not output_file.endswith(".json.bz2"):
						output_file += ".json.bz2"

					if os.path.exists(output_file):
						print(f"{colored_warn} Output file already exists: '{output_file}' - overwrite? ({UNDERLINE}y{RESET}es/{UNDERLINE}n{RESET}o)\n")
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

		time_taken = save_json_tree(directory, output_file=output_file, simulate=args.simulate, no_attributes=no_attributes, magic_max_size=magic_max_size, use_threads=threaded, force_magic=force_magic, no_estimates=args.no_estimates, use_magika=use_magika, max_threads=max_threads)
		sys.stdout.write("\n")
		title_console(f"✅ Task Complete - {program_name}")
		if args.simulate:
			logger.info(f"{colored_check} Simulation complete!")
		else:
			logger.info(f"{colored_check} Folder structure saved to '{output_file}'")
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
		title_console(f"📑 Select Report - {program_name}")
		if not json_file:
			if gui_enabled:
				root = Tk()
				root.withdraw()
				root.attributes("-topmost", True)
				print("📑 Select the BZip2 JSON file to browse:")
				json_file = filedialog.askopenfilename(title="Select BZip2 JSON File", filetypes=[("JSON File", "*.json.bz2")],initialdir=scan_log_dir, defaultextension=".json.bz2")
				root.destroy()

				if not json_file or json_file =='':
					error_message = (f"{colored_warn} No JSON file path provided.")
					if main_menu_enabled:
						main_menu()
					else:
						logger.error(error_message)
						exit(1)

			else:


				print (f"\n📂 Scan log directory: {root_log_dir}\n")
				bz2_files = []
				# Get all files with their midified timestamps and sizes
				for file in os.listdir('.'):
					if file.endswith(".json.bz2"):
						bz2_files.append((os.path.join(file), os.path.getmtime(os.path.join(file)), os.path.getsize(os.path.join(file))))
				for root, _, files in os.walk(root_log_dir):
					for file in files:
						if file.endswith(".json.bz2"):
							bz2_files.append((os.path.join(root, file), os.path.getmtime(os.path.join(root, file)), os.path.getsize(os.path.join(root, file))))

				# Sort the files by modified timestamp
				bz2_files.sort(key=lambda x: x[1])

				# Print the file names and size and modified date
				print("\n📑 Select the JSON file to browse:")
				for file, date, size in bz2_files:
					print(f"({humanize.naturalsize(size)})	[{humanize.naturaltime(time.time() - date)}]	{file}")

				print("\n📑 Enter the JSON file path: ")
				try:
					json_file = input(">>> ").strip()
				except KeyboardInterrupt:
					return
				if not json_file or json_file =='':
					error_message = (f"{colored_warn} No JSON file path provided.")
					if main_menu_enabled:
						main_menu()
					else:
						logger.error(error_message)
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
						logger.error(error_message)
						exit(1)
		print(f"\n📑 Loading JSON file: {json_file} ({humanize.naturalsize(os.path.getsize(json_file))})")
		browse_json_tree(json_file)
		if main_menu_enabled:
			main_menu()
		else:
			exit(0)
	def open_last_opened():
		global error_message, json_file
		if os.path.exists(config_file):
			try:
				last_opened_json = edit_get_config(config_file, "last_opened_json", mode="get")
			except Exception:

				last_opened_json = ""

		else:
			last_opened_json = ""

		if not last_opened_json:
			error_message = (f"{colored_warn} Last used JSON file not found: {last_opened_json}")
			if main_menu_enabled:
				main_menu()
			else:
				logger.error(error_message)
				exit(1)
		elif os.path.exists(last_opened_json):
			json_file = last_opened_json
			print(f"\n📑 Open last used JSON file: {json_file} ({humanize.naturalsize(os.path.getsize(json_file))})")
			browse_json_tree(json_file)
		else:
			error_message = (f"{colored_warn} Last used JSON file not found: {last_opened_json}")
			if main_menu_enabled:
				main_menu()
			else:
				logger.error(error_message)
				exit(1)
	def scan_again():
		global error_message,directory
		if os.path.exists(config_file):
			try:
				last_scan_dir = edit_get_config(config_file, "last_scan_dir", mode="get")
			except Exception:
				last_scan_dir = ""
		else:
			last_scan_dir = ""

		if not last_scan_dir:
			error_message = (f"{colored_warn} Last opened directory not found: {last_scan_dir}")
			if main_menu_enabled:
				main_menu()
			else:
				logger.error(error_message)
				exit(1)
		elif os.path.exists(last_scan_dir):
			directory = last_scan_dir
			print(f"\n📂 Scanning directory: {directory}")
			scan_mode()
		else:
			error_message = (f"{colored_warn} Last opened directory not found: {last_scan_dir}")
			if main_menu_enabled:
				main_menu()
			else:
				logger.error(error_message)

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

	title_console(f"🌳 {program_name}")

	config_file = os.path.join(os.path.dirname(__name__), 'tree_util_config.ini')

	parser = argparse.ArgumentParser(description="🌳 {program_name} - A tool to create snapshots of directory structures and explore them.",epilog="Usage: python3 tree_util.py -s /path/to/directory -o /path/to/output.json.bz2")

	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("-b", "--browse", type=str, help="Explore a structured JSON file. Specify the JSON file path.")
	mode.add_argument("-s", "--scan", type=str, help="Scan and create a structured JSON file. Specify the scan directory path.")
	parser.add_argument("-o", "--output", type=str, help="Specify the path for the BZip2 compressed output. If not specified, the output is saved in the current directory with a datetime. can be used with '-s'.")
	parser.add_argument("-t", "--threshold", type=str, default=naturalsize_to_int("1Mi"), help="Specify the threshold in bytes for enabling deep file type scanning (e.g. 50K, 10Mi, 100 etc.). If the file size is greater than the value, the MIME type is first detected by the mimetypes module (which detects by extension), then if the MIME type is unknown or too common (e.g. text/plain), the magic module is used for deep MIME type detection. Set value to 0 to disable deep file type scanning which makes the script faster. can be used with '-s'.")
	parser.add_argument("-g", "--gui", action="store_true", help="Open the GUI file selection to choose a directory (it's easier this way).")
	parser.add_argument("-m", "--simulate", action="store_true", help="Simulate the scan process, rather than actually writing the JSON file. This is useful for testing purposes.")
	parser.add_argument("-e", "--explore", action="store_true", help="Explore a structured JSON file soon after it's created.")
	parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
	parser.add_argument("-th", "--threads", action="store_true", help="Optimize the script by using threads to scan directories.(faster, but may slow down your CPU)")
	parser.add_argument("-x", "--max-threads", type=int, help="Set the maximum number of threads to use. Default is 8.")
	parser.add_argument("-l", "--last", action="store_true", help="Open last opened JSON file.")
	parser.add_argument("-f", "--force-magic", action="store_true", help="Force deep MIME type detection under the threshold. (Disable extension detection, slower).")
	parser.add_argument("-a","--no-attributes", action="store_true", help="Do not include file attributes in the JSON file.")
	parser.add_argument("--no-estimates", action="store_true", help="Do not estimate total files and directories.(faster)")
	parser.add_argument("-k", "--use-magika", action="store_true", help="Use Google Magika for even deeper MIME type detection. (slower, but can detect more types.)")
	parser.add_argument("--skip-note", action="store_true", help="skip note")
	args = parser.parse_args()

	if not "magika" in sys.modules and args.use_magika:
		raise ModuleNotFoundError("Magika is not installed. Install it with: pip install magika")

	if args.scan:
		if not os.path.isdir(args.scan):
			raise NotADirectoryError(f"Path '{args.scan}' is not a directory.")
		if not os.path.exists(args.scan):
			raise FileNotFoundError(f"Path '{args.scan}' does not exist.")
	elif args.browse:
			if not os.path.exists(args.browse):
				raise FileNotFoundError(f"Path '{args.browse}' does not exist.")
			if not os.path.isfile(args.browse):
				raise IsADirectoryError(f"Path '{args.browse}' is not a file.")

	if args.verbose:
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.INFO)
	if args.gui and not "tkinter" in sys.modules:
		gui_enabled = True
	else:
		gui_enabled = False

	if not args.scan and not args.browse and not args.last:
		if len(error_logs) > 0:
			try:
				timeout()
				input()
			except: # On some systems, keyboard module requires root permission
				pause("Press Enter to continue...")
	main(args)
