from playwright.sync_api import Page

from pages.base_page import BasePage


class SignInPage(BasePage):
    """The app's actual landing route ('/') — a Roam sign-in screen.

    No data-qa-id/data-testid hooks exist in the app yet (verified by a full
    DOM attribute scan on 2026-07-19). Every locator below is QA-ID-first
    with a CSS/role fallback via get_by_qa_id(), so it keeps working today
    and switches to the real attribute automatically once added — see
    docs/qa-id-convention.md for the proposed IDs and naming convention.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.get_by_qa_id(
            "sign-in-heading", fallback=page.get_by_role("heading", name="Sign In To Roam")
        )
        self.email_input = self.get_by_qa_id(
            "sign-in-email-input", fallback=page.locator('[formcontrolname="email"]')
        )
        self.password_input = self.get_by_qa_id(
            "sign-in-password-input", fallback=page.locator('[formcontrolname="password"]')
        )
        self.password_visibility_toggle = self.get_by_qa_id(
            "sign-in-password-visibility-toggle",
            fallback=page.get_by_role("button", name="Toggle password visibility"),
        )
        self.language_select = self.get_by_qa_id(
            "sign-in-language-select", fallback=page.locator('[formcontrolname="language"]')
        )
        self.sign_in_button = self.get_by_qa_id(
            "sign-in-submit-button", fallback=page.get_by_role("button", name="Sign In")
        )

    def load(self):
        return self.goto("/")

    def sign_in(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.sign_in_button.click()
        return self
