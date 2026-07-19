from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    """Example page object. Replace with concession-manager-web's actual landing page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.main_heading = page.get_by_role("heading", level=1)

    def load(self):
        return self.goto("/")
