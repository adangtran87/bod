import validators

import flet as ft


class ShopItem(ft.UserControl):
    def __init__(self, item: str, amount: int = 5):
        super().__init__()
        self.image = None
        self.text = None
        if validators.url(item):
            self.image = item
        else:
            self.text = item
        self.amount = amount

    def build(self):
        if self.image:
            item = ft.Image(
                src=self.image,
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            )
        elif self.text:
            item = ft.Container(
                padding=10,
                width=140,
                height=140,
                content=ft.Text(self.text, text_align=ft.MainAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                bgcolor=ft.colors.LIGHT_BLUE_ACCENT_200,
            )
        else:
            item = ft.Image(
                src="https://picsum.photos/150/150?0",
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            )

        column_content = []
        column_content.append(item)
        column_content.append(
            ft.Row(
                [
                    ft.FilledTonalButton(
                        self.amount, icon="attach_money", icon_color="AMBER_200"
                    ),
                    ft.FilledButton("Buy"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )

        card = ft.Card(
            content=ft.Container(
                padding=10,
                width=200,
                height=220,
                content=ft.Column(
                    column_content,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            )
        )

        return card


class ShopPanel(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.grid = ft.GridView(
            expand=1,
            runs_count=1,
            max_extent=300,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )

    def build(self):
        for i in range(0, 60):
            if i % 2 == 0:
                self.grid.controls.append(
                    ShopItem(item=f"https://picsum.photos/150/150?{i}")
                )
            else:
                self.grid.controls.append(ShopItem(item=f"{i}"))

        return ft.Container(
            margin=10,
            padding=10,
            content=self.grid,
        )
