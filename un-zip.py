import rich
import pypdf
import pyzipper
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from rich import print

def banner():
    print(r"""

[bold green]   ╔═════════════════════════════════════════════════╗[/bold green]
[bold green]   ║                                                 ║[/bold green]
[bold green]   ║   [bold blue]  ███[bold cyan]████╗ [/bold cyan]██████╗   █████╗  ███╗   ███╗      [/bold blue]║[/bold green]
[bold green]   ║   [bold cyan]  ██╔════╝ [bold blue]██╔══██[/bold blue]╗ ██╔══██╗ ████╗ ████║      [/bold cyan]║[/bold green]
[bold green]   ║   [/bold green]  ███[bold cyan]████╗ ██████╔[/bold cyan]╝ ███████║ ██╔████╔██║      [bold green]║[/bold green]
[bold green]   ║   [/bold green]  ╚════██║ ██╔[bold blue]═══╝  ██╔══██║ ██║╚█[/bold blue]█╔╝██║   [bold green]   ║[/bold green]
[bold green]   ║   [bold cyan]  █████[bold blue]██║ ██║      ██║ [/bold blue] ██║ ██║ ╚═╝ ██║     [/bold cyan] ║[/bold green]
[bold green]   ║   [/bold green] [bold blue] ╚══════╝[/bold blue] ╚═╝      ╚═╝  ╚═╝ ╚═╝     ╚═╝     [bold green] ║[/bold green]
[bold green]   ║                                                 ║[/bold green]
[bold green]   ╚═════════════════════════════════════════════════╝[/bold green]
[bold red]             ╔═════════════════════════════╗[/bold red]
[bold red]             ║ [bold green] ZIP Password Finder Tool  [/bold green] ║[/bold red]
[bold red]             ╚═════════════════════════════╝[/bold red]

    """)

def check_pdf_password(args):
    pdf_path, password = args
    try:
        reader = pypdf.PdfReader(pdf_path)
        if reader.decrypt(password):
            return password
    except Exception:
        pass
    return None

def check_zip_password(args):
    zip_path, password = args
    try:
        # استخدام pyzipper لدعم ZipCrypto و AES بمختلف أنواعه
        with pyzipper.AESZipFile(zip_path) as zf:
            zf.extractall(pwd=password.encode('utf-8'))
            return password
    except Exception:
        pass
    return None

def main():
    if len(sys.argv) < 4:
        banner()
        print("[bold red] [+] [bold Magenta]Usage:[bold blue] python un-zip.py [/bold blue]<zip|pdf>[/bold red] <target_file> [/bold Magenta]<wordlist.txt> ]")
        sys.exit(1)

    file_type = sys.argv[1].lower()
    target_file = sys.argv[2]
    words_file = sys.argv[3]

    print(f"[bold green][*] [bold red]Loading wordlist into memory...")
    try:
        with open(words_file, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[bold red][!] Error: File '{words_file}' not found.")
        return

    print(f"[bold red][*] [bold yellow]Total passwords:[/bold yellow] {len(passwords):,}")
    print(f"[bold red][*] [bold blue]Starting multi-threaded attack on all CPU cores...")

    # بدء حساب الوقت هنا
    start_time = time.time()

    tasks = [(target_file, pwd) for pwd in passwords]
    worker_func = check_pdf_password if file_type == "pdf" else check_zip_password

    found_password = None
    with ProcessPoolExecutor() as executor:
        for result in executor.map(worker_func, tasks, chunksize=100):
            if result:
                found_password = result
                executor.shutdown(wait=False, cancel_futures=True)
                break

    # إنهاء حساب الوقت وحساب الفرق
    end_time = time.time()
    elapsed_time = end_time - start_time

    if found_password:
        print(f"\n[bold red][+] [bold green]SUCCESS: Password found -> {found_password}")
        print(f"[bold red][*] [bold cyan]Time Elapsed: {elapsed_time:.2f} seconds")
        with open("result.txt", "w") as res:
            res.write(f"Target: {target_file}\nPassword: {found_password}\nTime Elapsed: {elapsed_time:.2f} seconds\n")
    else:
        print("\n[bold green][-][bold red] FAILED: Password not found in wordlist.")
        print(f"[bold red][*][bold blue] Time Elapsed: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()

