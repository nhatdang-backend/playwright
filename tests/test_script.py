import re
from playwright.sync_api import Page, expect
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
import asyncio

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.indianvisa.org.in/contact-us")

        await page.get_by_role("textbox", name="Full name").fill("Nguyen Van Test")
        await page.get_by_role("textbox", name="Phone Number").fill("901234567")
        await page.wait_for_timeout(2000)

        await page.get_by_role("textbox", name="Content").fill("Content under 100 characters")
        await page.get_by_role("textbox", name="Email").fill("nhatdang@mobcec.com")
        await page.get_by_role("textbox", name="Subject").fill("SANDBOX_Contact Us #GX006451224")
        await page.get_by_role("combobox").select_option("Complaint")

        submit_btn = page.get_by_role("button", name="SUBMIT")
        await submit_btn.click()

        await page.wait_for_timeout(6000)
        
        
        await page.goto("https://mail.google.com/mail/u/0/#inbox")
        await page.wait_for_timeout(2000)

        email_input = page.get_by_role("textbox", name="Email or phone")
        await email_input.fill("nhatdang@mobcec.com")
        await page.keyboard.press('Enter')

        password_input = page.get_by_role("textbox", name="Enter your password")
        await password_input.fill("cndprokutevip1")
        await page.keyboard.press('Enter')

        await page.get_by_role("textbox", name="Search mail").fill("SANDBOX_Contact Us #GX006451224")
        await page.wait_for_timeout(2000)
        await page.keyboard.press('Enter')

        await page.wait_for_timeout(1000)
        result = await page.get_by_role("button", name="Show more messages").text_content()
        await print("result:", result)
        

asyncio.run(run())