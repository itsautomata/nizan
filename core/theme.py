"""nizan: terminal theme. green HUD aesthetic."""

# ansi codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

GREEN = "\033[32m"
BRIGHT_GREEN = "\033[92m"
DARK_GREEN = "\033[38;5;22m"
WHITE = "\033[97m"
GRAY = "\033[90m"

# agent colors
AGENT_COLORS = {
    "moderator": "\033[38;5;34m",   # medium green
    "advocate": "\033[38;5;46m",    # bright green
    "critic": "\033[38;5;28m",      # dark green
    "judge": f"{BOLD}\033[38;5;48m",  # bold cyan-green
    "new_factor": f"{BOLD}{BRIGHT_GREEN}",
}


def agent(name):
    """color an agent name."""
    color = AGENT_COLORS.get(name, GREEN)
    return f"{color}{BOLD}[{name.upper()}]{RESET}"


def header(text):
    """main header text."""
    return f"{BOLD}{BRIGHT_GREEN}{text}{RESET}"


def label(text):
    """secondary label."""
    return f"{GREEN}{text}{RESET}"


def dim(text):
    """dimmed text for metadata."""
    return f"{DIM}{GRAY}{text}{RESET}"


def status(text):
    """status message (system-like)."""
    return f"{GREEN}{DIM}{text}{RESET}"


def line(char="-", width=60):
    """separator line."""
    return f"{DARK_GREEN}{char * width}{RESET}"


def heavy_line(width=60):
    """heavy separator."""
    return f"{GREEN}{BOLD}{'=' * width}{RESET}"


def prompt(text):
    """input prompt styling."""
    return f"{GREEN}{BOLD}> {RESET}{text}"


def banner():
    """startup banner."""
    b = f"""{BRIGHT_GREEN}{BOLD}
    ╔══════════════════════════════╗
    ║          n i z a n           ║
    ╚══════════════════════════════╝{RESET}
{DIM}{GREEN}    multi-agent decision system{RESET}
"""
    return b
