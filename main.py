import os
import sys
import subprocess
import asyncio
import zipfile

# --- AUTOMATIC DEPENDENCY INSTALLER ---
try:
    from playwright.async_api import async_playwright
except ModuleNotFoundError:
    print("Installing missing components... Please wait a moment.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    print("Installation complete!\n")
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
                                await asyncio.sleep(1)
                            
                            if was_interrupted:
                                break
                    
                    packs_actually_opened = actual_sequences_sent * 75
                    await chat_box.click()
                    if was_interrupted:
                        await page.keyboard.type(f"🛑 [{account_id}] Paused! Operations cut at {packs_actually_opened} packs.")
                    else:
                        await page.keyboard.type(f"✅ [{account_id}] Complete! Finished handling all {packs_actually_opened} packs.")
                    await page.keyboard.press("Enter")
                    
        except Exception:
            pass
        await asyncio.sleep(1.0)

async def run_bot():
    # --- AUTO UNZIP FOR RENDER CLOUD RUNNER ---
    for profile in ACCOUNT_PROFILES:
        zip_path = f"{profile}.zip"
        if os.path.exists(zip_path) and not os.path.exists(profile):
            print(f"📦 Extracting cloud session files for {profile}...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(os.getcwd())
            print(f"✅ Extraction completed for {profile}.")

    async with async_playwright() as p:
        tasks = []
        
        for profile in ACCOUNT_PROFILES:
            user_data_dir = os.path.join(os.getcwd(), profile)
            print(f"Loading persistent data path for: {user_data_dir}")
            
            context = await p.chromium.launch_persistent_context(
                user_data_dir,
                headless=True,  
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-extensions",
                    "--no-sandbox",
                    "--disable-setuid-sandbox"
                ]
            )
            
            page = context.pages[0] if context.pages else await context.new_page()
            print(f"Connecting browser stream for {profile} to Discord server...")
            await page.goto(CHANNEL_URL)
            
            await asyncio.sleep(5)
            
            chat_box = page.locator('div[role="textbox"]')
            tasks.append(manage_account_loop(profile, context, chat_box, page))
            
        print("\nAll 2 cloud worker sequences started. Concurrent channel monitoring engaged!")
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(run_bot())
