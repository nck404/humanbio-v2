import subprocess
import time
import os
import sys
import threading
import psutil
from colorama import init, Fore, Style

# Khởi tạo colorama cho Windows/Linux
init(autoreset=True)

# ASCII ART
ASCII_ART = f"""
{Fore.CYAN}{Style.BRIGHT}
  _    _ _    _ __  __          _   _   ____ _____ ____  
 | |  | | |  | |  \/  |   /\   | \ | | |  _ \_   _/ __ \ 
 | |__| | |  | | \  / |  /  \  |  \| | | |_) || || |  | |
 |  __  | |  | | |\/| | / /\ \ | . ` | |  _ < | || |  | |
 | |  | | |__| | |  | |/ ____ \| |\  | | |_) || || |__| |
 |_|  |_|\____/|_|  |_/_/    \_\_| \_| |____/_____\____/ 
                                                         
  {Fore.MAGENTA}>> Human Biology Management System - Cross-Platform Deployer <<
  {Fore.YELLOW}System detected: {os.name.upper()}
"""

class Metrics:
    def __init__(self):
        self.fetch_count = 0
        self.start_time = time.time()
        self.lock = threading.Lock()

    def increment_fetch(self):
        with self.lock:
            self.fetch_count += 1

metrics = Metrics()

def get_ram_usage():
    try:
        process = psutil.Process(os.getpid())
        total_mem = process.memory_info().rss
        for child in process.children(recursive=True):
            try:
                total_mem += child.memory_info().rss
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return total_mem / (1024 * 1024)
    except:
        return 0

def monitor_output(proc, prefix, color):
    for line in iter(proc.stdout.readline, ''):
        line = line.strip()
        if not line: continue
        if any(keyword in line for keyword in ["GET", "POST", "OPTIONS", "PATCH", "DELETE"]):
            metrics.increment_fetch()
        print(f"{color}[{prefix}]{Style.RESET_ALL} {line}")
    proc.stdout.close()

def run_services():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, 'src', 'backend')
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ASCII_ART)

    processes = []
    is_windows = os.name == 'nt'

    try:
        # 1. Khởi động Backend
        if is_windows:
            print(f"{Fore.YELLOW}🚀 [WINDOWS] Khởi động với Waitress (Production Mode)...")
            cmd = ['waitress-serve', '--port=5000', '--call', 'app:create_app']
        else:
            print(f"{Fore.YELLOW}🚀 [LINUX/UNIX] Khởi động với Gunicorn (Production Mode)...")
            # Cài đặt gunicorn nếu chạy trên linux
            cmd = ['gunicorn', '--bind', '0.0.0.0:5000', '--workers', '4', 'app:create_app()']

        backend_proc = subprocess.Popen(
            cmd,
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        processes.append(backend_proc)
        threading.Thread(target=monitor_output, args=(backend_proc, "BACKEND", Fore.GREEN), daemon=True).start()

        time.sleep(3)

        # 2. Khởi động Localtunnel
        print(f"{Fore.YELLOW}🌐 Đang khởi động Localtunnel (Subdomain: humain)...")
        lt_proc = subprocess.Popen(
            ['lt', '--port', '5000', '--subdomain', 'humain'],
            shell=True if is_windows else False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        processes.append(lt_proc)
        threading.Thread(target=monitor_output, args=(lt_proc, "TUNNEL ", Fore.BLUE), daemon=True).start()

        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.GREEN}✅ HỆ THỐNG ĐÃ SẴN SÀNG HOẠT ĐỘNG!")
        print(f"{Fore.WHITE}🔗 Local:   http://localhost:5000")
        print(f"{Fore.WHITE}🌍 Public:  https://humain.loca.lt")
        print(f"{Fore.CYAN}{'='*60}\n")

        while True:
            if backend_proc.poll() is not None:
                print(f"\n{Fore.RED}❌ Lỗi: Backend đã dừng!")
                break
            
            uptime = int(time.time() - metrics.start_time)
            ram = get_ram_usage()
            dashboard = f"\r{Fore.MAGENTA}📊 STATUS: {Fore.WHITE}OS: {os.name.upper()} | RAM: {ram:.1f} MB | FETCHES: {metrics.fetch_count} | UPTIME: {uptime}s {Style.RESET_ALL}"
            sys.stdout.write(dashboard)
            sys.stdout.flush()
            time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}🛑 Đang đóng tất cả dịch vụ...")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Lỗi hệ thống: {e}")
    finally:
        for proc in processes:
            try:
                if is_windows:
                    subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except:
                pass
        print(f"{Fore.GREEN}👋 Tạm biệt!")

if __name__ == "__main__":
    if os.name != 'nt':
        import signal
    run_services()
