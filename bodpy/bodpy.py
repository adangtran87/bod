import nfcutils
import flet as ft


def main(page: ft.Page):
    page.title = "Bank of Dad"
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.add(nfcutils.ButtonGetNfcId())


if __name__ == "__main__":
    ft.app(target=main)
