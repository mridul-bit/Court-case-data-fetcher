import asyncio
from playwright.async_api import async_playwright

BASE_URL = "https://delhihighcourt.nic.in/app/"

async def fetch_case_form_data():
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(BASE_URL)

        # Fetch case types
        case_types = await page.eval_on_selector_all(
            "#case_type option",
            "options => options.map(o => o.textContent.trim()).filter(t => t)"
        )

        # Fetch years
        years = await page.eval_on_selector_all(
            "#year option",
            "options => options.map(o => o.textContent.trim()).filter(t => t)"
        )

        # Fetch captcha text
        captcha_text = await page.inner_text("#captcha-code")

        await browser.close()

        return {
            "case_types": case_types,
            "years": years,
            "captcha": captcha_text
        }


async def fetch_case_details(case_type, case_number, filing_year, captcha_text):
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(BASE_URL)

        # Fill form fields
        await page.select_option("#case_type", label=case_type)
        await page.fill("#case_number", case_number)
        await page.select_option("#year", label=filing_year)
        await page.fill("#captchaInput", captcha_text)

        # Submit
        await page.click("#search")
        await page.wait_for_load_state("networkidle")
        #Check for invalid captcha message
        content = await page.content()
        if "invalid captcha" in content.lower():
            # Fetch fresh captcha and form data again
            fresh = await fetch_case_form_data()
            await browser.close()
            return {
                "error": "Invalid CAPTCHA",
                "case_types": fresh["case_types"],
                "years": fresh["years"],
                "captcha": fresh["captcha"],
            }
        # Extract structured data(assuming return data will have these classes)
        parties = await page.eval_on_selector_all(
            ".party-name", "nodes => nodes.map(n => n.textContent.trim())"
        )
        dates = await page.eval_on_selector_all(
            ".date-column", "nodes => nodes.map(n => n.textContent.trim())"
        )
        judgment_links = await page.eval_on_selector_all(
            "a[href$='.pdf']", "nodes => nodes.map(n => n.href)"
        )
        # can only be sure about reposne format having some raw html so storing it/required also in assignment
        raw_html = await page.content()
        await browser.close()

        return {
            "parties": parties,
            "dates": dates,
            "judgments": judgment_links,
            "raw_html": raw_html
        }


##testing>> fetch_case_form_Data will work but fetch_case_deatils wont since we dont no the format of the response coming frokm delhi high court website
if __name__ == "__main__":
    import asyncio

    # Test fetching form data (case types, years, captcha)
    form_data = asyncio.run(fetch_case_form_data())
    print("Form Data:", form_data)

    # Test fetching case details (replace with valid demo inputs)
    case_details = asyncio.run(fetch_case_details("W.P.(C)", "1234", "2023", form_data["captcha"]))
    print("Case Details:", case_details)

