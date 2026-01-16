import subprocess
import time
import os
import sys
import threading
import psutil
import socket
from colorama import init, Fore, Style

# Khởi tạo colorama
init(autoreset=True)

class Metrics:
    def __init__(self):
        self.fetch_count = 0
        self.start_time = time.time()
        self.tunnel_url = "Đang lấy URL..."
        self.lock = threading.Lock()

    def increment_fetch(self):
        with self.lock:
            self.fetch_count += 1
    
    def set_url(self, url):
        with self.lock:
            self.tunnel_url = url

metrics = Metrics()

# ASCII ART cực chất
ASCII_ART = f"""
{Fore.CYAN}{Style.BRIGHT}
  _    _ _    _ __  __          _   _   ____ _____ ____  
 | |  | | |  | |  \/  |   /\   | \ | | |  _ \_   _/ __ \ 
 | |__| | |  | | \  / |  /  \  |  \| | | |_) || || |  | |
 |  __  | |  | | |\/| | / /\ \ | . ` | |  _ < | || |  | |
 | |  | | |__| | |  | |/ ____ \| |\  | | |_) || || |__| |
 |_|  |_|\____/|_|  |_/_/    \_\_| \_| |____/_____\____/ 
                                                         
  {Fore.MAGENTA}>> Human Biology Management System - Ultra Fast Deployer <<
"""

def is_port_open(port):
    """Kiểm tra port cực nhanh dùng socket"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.1)
        return s.connect_ex(('127.0.0.1', port)) == 0

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
    # Sử dụng tệp tin không chặn để đọc log nhanh hơn
    for line in iter(proc.stdout.readline, ''):
        line = line.strip()
        if not line: continue
        
        # Nhận diện URL từ Localtunnel
        if "your url is:" in line:
            url = line.split("your url is:")[1].strip()
            metrics.set_url(url)
            continue 

        if any(kw in line for kw in ["GET", "POST", "OPTIONS", "PATCH", "DELETE"]):
            metrics.increment_fetch()
            
        # Xóa dòng status hiện tại trước khi in log mới
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        sys.stdout.flush()
        print(f"{color}[{prefix}]{Style.RESET_ALL} {line}")
    proc.stdout.close()

def run_services():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, 'src', 'backend')
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ASCII_ART)
    print(f"{Fore.CYAN}{Style.BRIGHT}🚀 Khởi động phiên bản v3.1 | OS: {os.name.upper()}")

    processes = []
    is_windows = os.name == 'nt'

    try:
        # 1. Khởi động Backend (Tối ưu đa luồng)
        if is_windows:
            print(f"{Fore.YELLOW}⚡ [WIN] Đang kích hoạt Waitress (Production + 8 Threads)...")
            # Thêm --threads=8 để xử lý song song cực nhanh
            cmd = ['waitress-serve', '--port=5000', '--threads=8', '--call', 'app:create_app']
        else:
            print(f"{Fore.YELLOW}⚡ [LINUX] Đang kích hoạt Gunicorn (4 Workers/Pebble)...")
            cmd = ['gunicorn', '--bind', '0.0.0.0:5000', '--workers', '4', '--worker-class', 'gevent', 'app:create_app()']

        backend_proc = subprocess.Popen(
            cmd, cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
            text=True, bufsize=1, universal_newlines=True
        )
        processes.append(backend_proc)
        threading.Thread(target=monitor_output, args=(backend_proc, "API", Fore.GREEN), daemon=True).start()

        # 🚀 TỐI ƯU: Không dùng time.sleep(3), kiểm tra port liên tục để start LT ngay khi API sẵn sàng
        print(f"{Fore.WHITE}⏳ Chờ API sẵn sàng...", end="", flush=True)
        retries = 0
        while not is_port_open(5000) and retries < 100:
            time.sleep(0.1)
            retries += 1
        print(f" {Fore.GREEN}SẴN SÀNG!")

        # 2. Khởi động Localtunnel (Force Subdomain humain)
        print(f"{Fore.YELLOW}🌐 Đang kết nối tới Localtunnel với subdomain 'humain'...")
        
        def start_tunnel():
            while True:
                lt_proc = subprocess.Popen(
                    ['lt', '--port', '5000', '--subdomain', 'humainbio'],
                    shell=True if is_windows else False,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                    text=True, bufsize=1, universal_newlines=True
                )
                
                # Đợi một chút để lấy URL từ output
                line = lt_proc.stdout.readline()
                if "your url is:" in line:
                    url = line.split("your url is:")[1].strip()
                    if "humainbio.loca.lt" in url:
                        print(f" {Fore.GREEN}ĐÃ LẤY ĐƯỢC DOMAIN CHUẨN!")
                        metrics.set_url(url)
                        processes.append(lt_proc)
                        threading.Thread(target=monitor_output, args=(lt_proc, "NET", Fore.BLUE), daemon=True).start()
                        break
                    else:
                        print(f"{Fore.RED}⚠️ Server cấp sai domain ({url}). Đang thử lại...", end="\r")
                        if is_windows:
                            subprocess.call(['taskkill', '/F', '/T', '/PID', str(lt_proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        else:
                            lt_proc.terminate()
                        time.sleep(2) # Đợi 2s trước khi thử lại

        threading.Thread(target=start_tunnel, daemon=True).start()

        print(f"\n{Fore.GREEN}✅ HỆ THỐNG ĐÃ ONLINE!")
        print(f"{Fore.WHITE}🔗 http://localhost:5000")
        print(f"{Fore.WHITE}🌍 https://humain.loca.lt\n")

        # Dashboard Loop
        while True:
            if backend_proc.poll() is not None:
                print(f"\n{Fore.RED}❌ Lỗi: Backend đột tử!")
                break
            
            ram = get_ram_usage()
            uptime = int(time.time() - metrics.start_time)
            
            # Dashboard hiển thị URL động
            sys.stdout.write(f"\r{Fore.MAGENTA}✨ {Fore.CYAN}{metrics.tunnel_url} {Fore.MAGENTA}| RAM {ram:5.1f}MB | REQS {metrics.fetch_count:4} | UP {uptime:4}s")
            sys.stdout.flush()
            time.sleep(0.5)

    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}🛑 Đang thu hồi tài nguyên...")
    finally:
        for proc in processes:
            try:
                if is_windows:
                    subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except: pass
        print(f"{Fore.GREEN}👋 Xong!")

if __name__ == "__main__":
    if os.name != 'nt': import signal
    run_services()
