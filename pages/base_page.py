from playwright.sync_api import Locator, Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, path: str = "/"):
        self.page.goto(path)
        return self

    def title(self) -> str:
        return self.page.title()

    def url(self) -> str:
        return self.page.url

    def get_by_qa_id(self, qa_id: str, fallback: Locator | None = None) -> Locator:
        """Locate an element by its QA ID, checking both `data-qa-id` and
        `data-testid` — naming is inconsistent across the app today, so both
        are recognized rather than picking one and breaking on the other.
        See docs/qa-id-convention.md for the naming convention and rollout
        plan.

        `fallback` (a CSS/role/etc. locator) is used while an element has no
        QA ID attribute yet: `.or_()` matches whichever of the two actually
        exists in the DOM, so a page object keeps working right up until the
        real attribute lands, and then switches over with no test change.
        """
        locator = self.page.locator(f'[data-qa-id="{qa_id}"], [data-testid="{qa_id}"]')
        return locator.or_(fallback) if fallback is not None else locator
