from playwright.sync_api import Page

from pages.base_page import BasePage


class SignInPage(BasePage):
    """The app's actual landing route ('/') — a Roam sign-in screen."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Sign In To Roam")
        self.email_input = page.locator('[formcontrolname="email"]')
        self.password_input = page.locator('[formcontrolname="password"]')
        self.password_visibility_toggle = page.get_by_role(
            "button", name="Toggle password visibility"
        )
        self.language_select = page.locator('[formcontrolname="language"]')
        self.sign_in_button = page.get_by_role("button", name="Sign In")

    def load(self):
        return self.goto("/")

    def sign_in(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.sign_in_button.click()
        return self
