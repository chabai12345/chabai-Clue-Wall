"""
侦探看板 · Detective Board — 桌面版
将 Web 应用包装为无边框置顶窗口，支持全局热键唤出。
"""
import ctypes
import ctypes.wintypes
import os
import sys
import threading
import webview

# ── 配置 ────────────────────────────────────────
HOTKEY_MOD = (0x0002 | 0x0004)       # Ctrl + Shift
HOTKEY_VK = 0x44                      # D
HOTKEY_ID = 1
HOTKEY_LABEL = "Ctrl+Shift+D"
SERVER_PORT = 8000
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

# ── 全局状态 ────────────────────────────────────
_window = None
_is_visible = True


# ── 路径处理（兼容 PyInstaller） ────────────────

def get_data_dir() -> str:
    """可写数据目录：打包后位于 %APPDATA%，不会因重建丢失。"""
    if getattr(sys, 'frozen', False):
        return os.path.join(os.environ['APPDATA'], '线索墙')
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def get_static_dir() -> str:
    """静态文件目录：打包后从 _MEIPASS 读取。"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'static')
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')


# ── FastAPI 后台服务器 ───────────────────────────

def start_server():
    """在后台线程运行 FastAPI。"""
    import uvicorn
    # 将路径注入环境变量，让 main.py 读取
    os.environ['DETECTIVE_BOARD_DATA'] = get_data_dir()
    os.environ['DETECTIVE_BOARD_STATIC'] = get_static_dir()
    from main import app
    uvicorn.run(app, host='127.0.0.1', port=SERVER_PORT, log_level='warning')


# ── 全局热键（Windows API） ─────────────────────

def hotkey_listener():
    """Windows 消息循环监听全局热键。"""
    user32 = ctypes.windll.user32
    if not user32.RegisterHotKey(None, HOTKEY_ID, HOTKEY_MOD, HOTKEY_VK):
        return  # 热键注册失败，静默跳过

    msg = ctypes.wintypes.MSG()
    try:
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0):
            if msg.message == 0x0312:          # WM_HOTKEY
                if msg.wParam == HOTKEY_ID:
                    toggle_visibility()
            else:
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
    finally:
        user32.UnregisterHotKey(None, HOTKEY_ID)


def toggle_visibility():
    """切换窗口显示 / 隐藏。"""
    global _is_visible
    if _window is None:
        return
    try:
        if _is_visible:
            _window.hide()
            _is_visible = False
        else:
            _window.show()
            _window.restore()
            _is_visible = True
    except Exception:
        pass


# ── JS API 桥 ───────────────────────────────────

class Api:
    """暴露给前端 JS 的方法。"""

    @staticmethod
    def minimize():
        if _window:
            _window.minimize()

    @staticmethod
    def exit_app():
        if _window:
            _window.destroy()
        os._exit(0)

    @staticmethod
    def get_app_info():
        return {
            'desktop': True,
            'hotkey': HOTKEY_LABEL,
            'version': '1.0.0',
        }


# ── 入口 ────────────────────────────────────────

if __name__ == '__main__':
    # 启动后端服务器
    threading.Thread(target=start_server, daemon=True).start()

    # 注册全局热键
    threading.Thread(target=hotkey_listener, daemon=True).start()

    api = Api()

    _window = webview.create_window(
        '线索墙',
        f'http://127.0.0.1:{SERVER_PORT}',
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        resizable=True,
        js_api=api,
    )

    webview.start(private_mode=False, debug=False)
