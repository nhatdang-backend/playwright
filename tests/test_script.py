import re
from playwright.sync_api import Page, expect
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
import asyncio
from datetime import datetime
import pytest
import pycron

async def accessToSite():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page    = await context.new_page()
        
        await page.goto("https://www.indianvisa.org.in/contact-us")
        expect(page).to_have_url(re.compile(".*contact-us"))
        
        checkFullName = await page.get_by_role("textbox", name="Full name").fill("Nguyen Van Test")
        expect(checkFullName).to_have_value("Nguyen Van Test")

        checkEmail    = await page.get_by_role("textbox", name="Email").fill("nhatdang@mobcec.com")
        expect(checkEmail).to_have_value("nhatdang@mobcec")

        checkPhone    = await page.get_by_role("textbox", name="Phone Number").fill("901234567")
        expect(checkPhone).to_have_value("901234567")

        checkContent  = await page.get_by_role("textbox", name="Content").fill("Content under 100 characters")
        expect(checkContent).to_have_value("Content under 100 characters")

        checkSubject  = await page.get_by_role("textbox", name="Subject").fill("SANDBOX_Contact Us #GX006451224")
        expect(checkSubject).to_have_value("SANDBOX_Contact Us #GX006451224")

        checkComboBox = await page.get_by_role("combobox").select_option("Complaint")
        expect(checkComboBox).to_equal(["Complaint"])

        submit_btn = await page.get_by_role("button", name="SUBMIT").click()
        content = page.content()
        if "We have received your request and our team will get back to you shortly. You can check your email for further updates." in content:
            expect(True).to_be(True)

async def testConfirmEmail():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://mail.google.com/mail/u/0/#inbox")
        await page.wait_for_timeout(2000)

        email_input = page.get_by_role("textbox", name="Email or phone")
        await email_input.fill("nhatdang@mobcec.com")
        await page.keyboard.press('Enter')

        password_input = page.get_by_role("textbox", name="Enter your password")
        await password_input.fill("cndprokutevip1")
        await page.keyboard.press('Enter')

        await page.get_by_role("textbox", name="Search mail").fill("SANDBOX_Contact Us #GX006451224")
        await page.keyboard.press('Enter')

        await page.wait_for_timeout(1000)
        result = await page.get_by_role("button", name="Show more messages").text_content()
        expect(result).to_contain("1 of")
        await page.close()

async def test_run():
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
        expect(result).to_contain("1 of")
        await page.close()

#asyncio.run(run())

async def scheduler():
    while True:
        if pycron.is_now("*/1 * * * *"):  # every 1 minutes
            asyncio.create_task(test_run())   # don’t block loop
            await asyncio.sleep(60)       # prevent duplicate run in same minute

        await asyncio.sleep(1)
asyncio.run(scheduler())