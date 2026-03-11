#!/usr/bin/env python3
“””
╔══════════════════════════════════════════════╗
║        PASSWORD GENERATOR  v1.0.0            ║
║    Secure · Smart · Human-Friendly           ║
║      Developed by Tariq H. Almlaki           ║
╚══════════════════════════════════════════════╝
“””

import random
import string
import secrets
import sys
import time
import os
import argparse
import re
from datetime import datetime

# ─── ANSI Colors ───────────────────────────────────────────

class C:
RESET   = “\033[0m”
BOLD    = “\033[1m”
DIM     = “\033[2m”
GREEN   = “\033[92m”
RED     = “\033[91m”
YELLOW  = “\033[93m”
CYAN    = “\033[96m”
BLUE    = “\033[94m”
GRAY    = “\033[90m”
WHITE   = “\033[97m”
MAGENTA = “\033[95m”
ORANGE  = “\033[38;5;214m”
BG_DARK = “\033[48;5;235m”

# ─── Character Sets ────────────────────────────────────────

UPPERCASE  = string.ascii_uppercase
LOWERCASE  = string.ascii_lowercase
DIGITS     = string.digits
SYMBOLS    = “!@#$%^&*()-_=+[]{}|;:,.<>?”
AMBIGUOUS  = “0OIl1”   # chars that look alike

# ─── Word lists for memorable passwords ───────────────────

ADJECTIVES = [
“swift”, “brave”, “calm”, “dark”, “eager”, “fierce”, “grand”,
“happy”, “icy”, “jolly”, “keen”, “lively”, “mighty”, “noble”,
“quiet”, “rapid”, “sharp”, “tough”, “ultra”, “vivid”, “warm”,
“zesty”, “amber”, “bold”, “crisp”, “dusty”, “epic”, “frosty”,
“glowing”, “hidden”, “iron”, “jade”, “lunar”, “mystic”, “neon”,
“ocean”, “polar”, “royal”, “solar”, “titan”, “urban”, “velvet”,
]

NOUNS = [
“wolf”, “tiger”, “eagle”, “storm”, “blade”, “flame”, “frost”,
“hawk”, “lion”, “river”, “rock”, “shadow”, “shield”, “spark”,
“star”, “stone”, “sword”, “thunder”, “wave”, “wind”, “arrow”,
“bear”, “comet”, “dawn”, “drift”, “ember”, “forge”, “glacier”,
“grove”, “haven”, “horizon”, “island”, “jungle”, “knight”,
“lance”, “meteor”, “mountain”, “night”, “orbit”, “peak”,
“phantom”, “quest”, “raven”, “ridge”, “scout”, “vault”,
]

# ─── Banner ────────────────────────────────────────────────

def print_banner():
print(f”””
{C.CYAN}{C.BOLD}
██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗
██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝
{C.RESET}  {C.MAGENTA}G E N E R A T O R{C.RESET}  {C.GRAY}v1.0.0{C.RESET}
{C.GRAY}Developed by {C.RESET}{C.BOLD}{C.WHITE}Tariq H. Almlaki{C.RESET}
“””)

# ─── Strength Meter ────────────────────────────────────────

def evaluate_strength(password):
score = 0
feedback = []

```
length = len(password)
if length >= 8:   score += 1
if length >= 12:  score += 1
if length >= 16:  score += 1
if length >= 20:  score += 1

has_upper  = bool(re.search(r'[A-Z]', password))
has_lower  = bool(re.search(r'[a-z]', password))
has_digit  = bool(re.search(r'\d', password))
has_symbol = bool(re.search(r'[^A-Za-z0-9]', password))

if has_upper:  score += 1
if has_lower:  score += 1
if has_digit:  score += 1
if has_symbol: score += 2

# Entropy bonus
charset_size = 0
if has_upper:  charset_size += 26
if has_lower:  charset_size += 26
if has_digit:  charset_size += 10
if has_symbol: charset_size += 32
entropy = length * (charset_size.bit_length() if charset_size else 0)

if not has_upper:  feedback.append("add uppercase letters")
if not has_lower:  feedback.append("add lowercase letters")
if not has_digit:  feedback.append("add numbers")
if not has_symbol: feedback.append("add symbols")
if length < 12:    feedback.append("make it longer")

if score <= 3:
    level, color, bar_char = "Weak",   C.RED,    "▓"
    bar_count = 1
elif score <= 5:
    level, color, bar_char = "Fair",   C.ORANGE, "▓"
    bar_count = 2
elif score <= 7:
    level, color, bar_char = "Good",   C.YELLOW, "▓"
    bar_count = 3
elif score <= 9:
    level, color, bar_char = "Strong", C.GREEN,  "▓"
    bar_count = 4
else:
    level, color, bar_char = "Fort Knox", C.CYAN, "▓"
    bar_count = 5

return level, color, bar_count, feedback, entropy
```

def print_strength(password):
level, color, bar_count, feedback, entropy = evaluate_strength(password)
bars = f”{color}{‘▓’ * bar_count}{C.GRAY}{‘░’ * (5 - bar_count)}{C.RESET}”
print(f”  Strength   : {bars}  {color}{C.BOLD}{level}{C.RESET}  {C.GRAY}(~{entropy} bits entropy){C.RESET}”)
if feedback:
print(f”  Tips       : {C.GRAY}{’, ’.join(feedback)}{C.RESET}”)

# ─── Colorize Password ─────────────────────────────────────

def colorize(password):
result = “”
for ch in password:
if ch in UPPERCASE:
result += f”{C.CYAN}{C.BOLD}{ch}{C.RESET}”
elif ch in LOWERCASE:
result += f”{C.WHITE}{ch}{C.RESET}”
elif ch in DIGITS:
result += f”{C.YELLOW}{ch}{C.RESET}”
else:
result += f”{C.MAGENTA}{ch}{C.RESET}”
return result

# ─── Typing animation ──────────────────────────────────────

def type_out(text, delay=0.018):
for ch in text:
print(ch, end=””, flush=True)
time.sleep(delay)
print()

# ─── Password Generators ───────────────────────────────────

def gen_random(length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
charset = “”
required = []

```
if use_upper:
    chars = UPPERCASE
    if exclude_ambiguous:
        chars = "".join(c for c in chars if c not in AMBIGUOUS)
    charset += chars
    required.append(secrets.choice(chars))
if use_lower:
    chars = LOWERCASE
    if exclude_ambiguous:
        chars = "".join(c for c in chars if c not in AMBIGUOUS)
    charset += chars
    required.append(secrets.choice(chars))
if use_digits:
    chars = DIGITS
    if exclude_ambiguous:
        chars = "".join(c for c in chars if c not in AMBIGUOUS)
    charset += chars
    required.append(secrets.choice(chars))
if use_symbols:
    charset += SYMBOLS
    required.append(secrets.choice(SYMBOLS))

if not charset:
    charset = LOWERCASE
    required = [secrets.choice(LOWERCASE)]

remaining = [secrets.choice(charset) for _ in range(length - len(required))]
pool = required + remaining
secrets.SystemRandom().shuffle(pool)
return "".join(pool)
```

def gen_memorable(separator=”-”, capitalize=False):
adj  = secrets.choice(ADJECTIVES)
noun = secrets.choice(NOUNS)
num  = secrets.randbelow(9000) + 1000
sym  = secrets.choice(”!@#$”)
if capitalize:
adj  = adj.capitalize()
noun = noun.capitalize()
return f”{adj}{separator}{noun}{separator}{num}{sym}”

def gen_pin(length=6):
return “”.join([str(secrets.randbelow(10)) for _ in range(length)])

def gen_passphrase(words=4, separator=” “):
chosen = [secrets.choice(ADJECTIVES + NOUNS) for _ in range(words)]
return separator.join(chosen)

# ─── Display Result ────────────────────────────────────────

def display_password(label, password, index=None):
prefix = f”  {C.GRAY}[{index}]{C.RESET} “ if index is not None else “  “
colorized = colorize(password)
print(f”{prefix}{colorized}”)

def display_section(title, passwords, show_strength=True):
print(f”\n  {C.BOLD}{C.CYAN}{title}{C.RESET}”)
print(f”  {C.GRAY}{‘─’ * 56}{C.RESET}”)
for i, pw in enumerate(passwords, 1):
display_password(””, pw, index=i)
if show_strength and passwords:
print()
print_strength(passwords[0])

# ─── Copy to clipboard (optional) ─────────────────────────

def try_copy(text):
try:
if sys.platform == “darwin”:
os.system(f”echo ‘{text}’ | pbcopy”)
return True
elif sys.platform == “win32”:
os.system(f”echo {text} | clip”)
return True
elif sys.platform.startswith(“linux”):
os.system(f”echo ‘{text}’ | xclip -selection clipboard 2>/dev/null || “
f”echo ‘{text}’ | xsel –clipboard –input 2>/dev/null”)
return True
except Exception:
pass
return False

# ─── Save to file ──────────────────────────────────────────

def save_passwords(passwords, filename=“passwords.txt”):
ts = datetime.now().strftime(”%Y-%m-%d %H:%M:%S”)
with open(filename, “a”) as f:
f.write(f”\n{‘─’*50}\n”)
f.write(f”Generated: {ts}\n”)
f.write(f”{‘─’*50}\n”)
for pw in passwords:
f.write(pw + “\n”)
print(f”\n  {C.GREEN}✓ Saved to {C.BOLD}{filename}{C.RESET}”)

# ─── Interactive Menu ──────────────────────────────────────

def ask(prompt, default=””):
default_str = f” [{C.GRAY}{default}{C.RESET}]” if default else “”
val = input(f”  {C.CYAN}{prompt}{C.RESET}{default_str}: “).strip()
return val if val else str(default)

def ask_yn(prompt, default=True):
hint = “Y/n” if default else “y/N”
val = input(f”  {C.CYAN}{prompt}{C.RESET} [{C.GRAY}{hint}{C.RESET}]: “).strip().lower()
if not val:
return default
return val in (“y”, “yes”)

def divider():
print(f”  {C.GRAY}{‘─’ * 56}{C.RESET}”)

def interactive():
print_banner()

```
print(f"  {C.BOLD}What kind of password do you need?{C.RESET}\n")
print(f"  {C.WHITE}1{C.RESET}  {C.CYAN}Random{C.RESET}       {C.GRAY}— classic letters, numbers, symbols{C.RESET}")
print(f"  {C.WHITE}2{C.RESET}  {C.CYAN}Memorable{C.RESET}    {C.GRAY}— word+word+number (easy to remember){C.RESET}")
print(f"  {C.WHITE}3{C.RESET}  {C.CYAN}PIN{C.RESET}          {C.GRAY}— numeric PIN code{C.RESET}")
print(f"  {C.WHITE}4{C.RESET}  {C.CYAN}Passphrase{C.RESET}   {C.GRAY}— multiple random words{C.RESET}")
print(f"  {C.WHITE}5{C.RESET}  {C.CYAN}All Types{C.RESET}    {C.GRAY}— generate one of each{C.RESET}")
print()

choice = ask("Your choice", "1")
count_str = ask("How many passwords", "5")
try:
    count = max(1, min(50, int(count_str)))
except ValueError:
    count = 5

all_passwords = []

# ── Random ────────────────────────────────────────────
if choice in ("1", "5"):
    print()
    divider()
    print(f"  {C.BOLD}Random Password Settings{C.RESET}")
    divider()
    length_str = ask("Length", "16")
    try:
        length = max(4, min(128, int(length_str)))
    except ValueError:
        length = 16

    use_upper   = ask_yn("Include UPPERCASE letters", True)
    use_lower   = ask_yn("Include lowercase letters", True)
    use_digits  = ask_yn("Include numbers (0-9)", True)
    use_symbols = ask_yn("Include symbols (!@#...)", True)
    exc_ambig   = ask_yn("Exclude ambiguous chars (0,O,I,l)", False)

    passwords = [
        gen_random(length, use_upper, use_lower, use_digits, use_symbols, exc_ambig)
        for _ in range(count)
    ]
    all_passwords.extend(passwords)
    display_section("Random Passwords", passwords)

# ── Memorable ─────────────────────────────────────────
if choice in ("2", "5"):
    sep = ask("Separator", "-") if choice == "2" else "-"
    cap = ask_yn("Capitalize words", True) if choice == "2" else True
    passwords = [gen_memorable(sep, cap) for _ in range(count)]
    all_passwords.extend(passwords)
    display_section("Memorable Passwords", passwords)

# ── PIN ───────────────────────────────────────────────
if choice in ("3", "5"):
    pin_len_str = ask("PIN length", "6") if choice == "3" else "6"
    try:
        pin_len = max(4, min(12, int(pin_len_str)))
    except ValueError:
        pin_len = 6
    passwords = [gen_pin(pin_len) for _ in range(count)]
    all_passwords.extend(passwords)
    display_section("PIN Codes", passwords, show_strength=False)

# ── Passphrase ────────────────────────────────────────
if choice in ("4", "5"):
    words_str = ask("Number of words", "4") if choice == "4" else "4"
    sep       = ask("Separator", " ") if choice == "4" else " "
    try:
        num_words = max(2, min(10, int(words_str)))
    except ValueError:
        num_words = 4
    passwords = [gen_passphrase(num_words, sep) for _ in range(count)]
    all_passwords.extend(passwords)
    display_section("Passphrases", passwords, show_strength=False)

# ── Actions ───────────────────────────────────────────
print(f"\n  {C.GRAY}{'─' * 56}{C.RESET}")
print(f"  {C.BOLD}What next?{C.RESET}\n")

if ask_yn("Save passwords to file (passwords.txt)", False):
    save_passwords(all_passwords)

if all_passwords and ask_yn("Copy first password to clipboard", True):
    first = all_passwords[0] if all_passwords else ""
    if try_copy(first):
        print(f"  {C.GREEN}✓ Copied!{C.RESET}  {C.GRAY}{first[:6]}{'*' * max(0,len(first)-6)}{C.RESET}")
    else:
        print(f"  {C.YELLOW}⚠ Clipboard not available. Copy manually.{C.RESET}")

if ask_yn("Generate another batch", False):
    print()
    interactive()
    return

print(f"\n  {C.GREEN}✓ Done!{C.RESET}  {C.GRAY}Stay safe out there.{C.RESET}\n")
```

# ─── CLI Mode ─────────────────────────────────────────────

def cli_mode(args):
print_banner()

```
passwords = []

if args.type == "random":
    for _ in range(args.count):
        passwords.append(gen_random(
            args.length,
            not args.no_upper,
            not args.no_lower,
            not args.no_digits,
            not args.no_symbols,
            args.no_ambiguous,
        ))
    display_section(f"Random Passwords (length={args.length})", passwords)

elif args.type == "memorable":
    for _ in range(args.count):
        passwords.append(gen_memorable(args.separator, not args.no_capitalize))
    display_section("Memorable Passwords", passwords)

elif args.type == "pin":
    for _ in range(args.count):
        passwords.append(gen_pin(args.length))
    display_section(f"PIN Codes (length={args.length})", passwords, show_strength=False)

elif args.type == "passphrase":
    for _ in range(args.count):
        passwords.append(gen_passphrase(args.words, args.separator))
    display_section(f"Passphrases ({args.words} words)", passwords, show_strength=False)

if args.save:
    save_passwords(passwords)

if args.copy and passwords:
    try_copy(passwords[0])
    print(f"  {C.GREEN}✓ First password copied to clipboard.{C.RESET}")

print()
```

# ─── Main ──────────────────────────────────────────────────

def main():
parser = argparse.ArgumentParser(
description=“Password Generator — Secure & Human-Friendly”,
formatter_class=argparse.RawDescriptionHelpFormatter,
epilog=”””
Examples:
python password_generator.py                     # interactive mode
python password_generator.py -t random -l 20 -n 5
python password_generator.py -t memorable -n 3
python password_generator.py -t pin -l 6 -n 10
python password_generator.py -t passphrase -w 5 -n 3
python password_generator.py -t random -l 32 –no-symbols –save
“””
)
parser.add_argument(”-t”, “–type”,         choices=[“random”,“memorable”,“pin”,“passphrase”],
help=“Password type”)
parser.add_argument(”-l”, “–length”,       type=int, default=16, help=“Password length (default: 16)”)
parser.add_argument(”-n”, “–count”,        type=int, default=5,  help=“Number of passwords (default: 5)”)
parser.add_argument(”-w”, “–words”,        type=int, default=4,  help=“Words for passphrase (default: 4)”)
parser.add_argument(”-s”, “–separator”,    default=”-”,          help=“Separator char (default: -)”)
parser.add_argument(”–no-upper”,           action=“store_true”,  help=“Exclude uppercase”)
parser.add_argument(”–no-lower”,           action=“store_true”,  help=“Exclude lowercase”)
parser.add_argument(”–no-digits”,          action=“store_true”,  help=“Exclude digits”)
parser.add_argument(”–no-symbols”,         action=“store_true”,  help=“Exclude symbols”)
parser.add_argument(”–no-ambiguous”,       action=“store_true”,  help=“Exclude ambiguous chars”)
parser.add_argument(”–no-capitalize”,      action=“store_true”,  help=“Don’t capitalize memorable words”)
parser.add_argument(”–save”,               action=“store_true”,  help=“Save to passwords.txt”)
parser.add_argument(”–copy”,               action=“store_true”,  help=“Copy first password to clipboard”)

```
args = parser.parse_args()

if args.type:
    cli_mode(args)
else:
    try:
        interactive()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n  {C.YELLOW}Cancelled.{C.RESET}\n")
        sys.exit(0)
```

if **name** == “**main**”:
main()