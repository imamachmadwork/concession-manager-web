from playwright.sync_api import Page


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
