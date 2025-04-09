from pathlib import Path
import os
import platform

def get_download_folder():
    system = platform.system()
    home = Path.home()

    if system == "Windows":
        # 通常 Windows 的下載路徑
        download = home / "Downloads"
    elif system == "Darwin":
        # macOS 的下載路徑
        download = home / "Downloads"
    elif system == "Linux":
        # Linux 有時候會存在 XDG_DOWNLOAD_DIR 設定
        try:
            import subprocess
            result = subprocess.run(['xdg-user-dir', 'DOWNLOAD'], capture_output=True, text=True)
            download = Path(result.stdout.strip())
        except Exception:
            download = home / "Downloads"
    else:
        # fallback
        download = home / "Downloads"

    return download

# 使用範例
download_path = get_download_folder()
print(f"下載資料夾位置是：{download_path}")
