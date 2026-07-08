import os
import sys
import asyncio
import zipfile
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import threading

# Point Playwright directly to a stable local directory before importing it
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(os.getcwd(), ".playwright-browsers")

from playwright.async_api import async_playwright

# --- CONFIGURATION ---
CHANNEL_URL = "https://discord.com/channels/1259167876733206578/1520766594870153226"
MAIN_DISPLAY_NAME = "Delwyn"
MAIN_USERNAME = "clutch_gamer_19"

ACCOUNT_PROFILES = ["Account_Alpha", "Account_Beta"]

ACCOUNT_COOLDOWNS = {
    "Account_Alpha": 16,
    "Account_Beta": 28
}

# --- DUMMY SERVER TO SATISFY RENDER PORT SCANNER ---
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            return # Keep logs clean
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is active.")
            
    print(f"📡 Starting dummy web framework on port {port} to keep Render happy...")
    try:
        with TCPServer(("0.0.0.0", port), QuietHandler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"⚠️ Web framework notification: {e}")

async def manage_account_loop(account_id, context, chat_box, page):
    cooldown_time = ACCOUNT_COOLDOWNS.get(account_id, 15)
    print(f"🤖 [{account_id}] Listening! Cooldown set to {cooldown_time}s. Monitoring chat...")
    
    try:
        messages = page.locator('li[class*="messageListItem"]')
        last_processed_msg = await messages.last.text_content() if await messages.count() > 0 else ""
    except Exception:
        last_processed_msg = ""

    while True:
        try:
            messages = page.locator('li[class*="messageListItem"]')
            if await messages.count() == 0:
                await asyncio.sleep(1)
                continue
                
            last_message = messages.last
            text_content = await last_message.text_content()
            
            is_start_cmd = "!start" in text_content
            is_stop_cmd = "!stop" in text_content
            
            if (is_start_cmd or is_stop_cmd) and text_content != last_processed_msg:
                is_from_me = (MAIN_DISPLAY_NAME.lower() in text_content.lower() or 
                              MAIN_USERNAME.lower() in text_content.lower())
                
                if not is_from_me:
                    last_processed_msg = text_content 
                    print(f"⚠️ [{account_id}] Security Intercept! Unauthorized input dropped.")
                    await chat_box.click()
                    await page.keyboard.type("YOU ARE NOT HIM LIL BRO")
                    await page.keyboard.press("Enter")
                    await asyncio.sleep(0.5)
                    continue
                
                if is_start_cmd and is_from_me:
                    last_processed_msg = text_content 
                    parts = text_content.split("!start")
                    try:
                        loops = int(parts[1].strip().split()[0])
                    except (IndexError, ValueError):
                        loops = 5  
                    
                    total_packs_to_open = loops * 75
                    actual_sequences_sent = 0
                    was_interrupted = False
                    
                    await chat_box.click()
                    await page.keyboard.type(f"🚀 [{account_id}] Started opening packs! Target: {total_packs_to_open} packs.")
                    await page.keyboard.press("Enter")
                    await asyncio.sleep(1.0)
                    
                    for i in range(loops):
                        try:
                            live_messages = page.locator('li[class*="messageListItem"]')
                            if await live_messages.count() > 0:
                                current_last_msg = await live_messages.last.text_content()
                                live_from_me = (MAIN_DISPLAY_NAME.lower() in current_last_msg.lower() or 
                                                MAIN_USERNAME.lower() in current_last_msg.lower())
                                
                                if "!stop" in current_last_msg:
                                    if live_from_me:
                                        was_interrupted = True
                                        break
                                    else:
                                        await chat_box.click()
                                        await page.keyboard.type("YOU ARE NOT HIM LIL BRO")
                                        await page.keyboard.press("Enter")
                                        last_processed_msg = current_last_msg
                                        await asyncio.sleep(0.5)
                        except Exception:
                            pass

                        print(f"[{account_id}] [{i+1}/{loops}] Dispatching slash execution...")
                        await chat_box.click()
                        await page.keyboard.type("/packs")
                        await asyncio.sleep(0.5)
                        await page.keyboard.press("Tab")
                        await asyncio.sleep(0.4)
                        await page.keyboard.type("75")
                        await asyncio.sleep(0.5)
                        await page.keyboard.press("Enter")
                        await asyncio.sleep(0.3)
                        await page.keyboard.press("Enter")
                        
                        actual_sequences_sent += 1
                        
                        try:
                            updated_messages = page.locator('li[class*="messageListItem"]')
                            if await updated_messages.count() > 0:
                                last_processed_msg = await updated_messages.last.text_content()
                        except Exception:
                            pass
                            
                        if i < loops - 1:
                            for _ in range(int(cooldown_time)):
                                try:
