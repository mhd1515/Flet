
import flet as ft
import ast
import operator


def main(page: ft.Page):
    page.title = "ماشین حساب"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    page.padding = 20
    page.window.width = 370
    page.window.height = 680

    expression = ""

    display = ft.Text(
        value="0",
        size=34,
        color="#F8FAFC",
        text_align=ft.TextAlign.RIGHT,
        weight=ft.FontWeight.BOLD,
        selectable=True,
    )

    history = ft.Text(
        value="",
        size=15,
        color="#94A3B8",
        text_align=ft.TextAlign.RIGHT,
    )

    # محاسبه امن عبارت ریاضی بدون eval
    def safe_calculate(expr):
        expr = expr.replace("×", "*").replace("÷", "/")

        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
            ast.Mod: operator.mod,
        }

        def solve(node):
            if isinstance(node, ast.Expression):
                return solve(node.body)

            if isinstance(node, ast.Constant):
                if type(node.value) in (int, float):
                    return node.value
                raise ValueError("عدد نامعتبر")

            if isinstance(node, ast.BinOp):
                op_type = type(node.op)
                if op_type not in allowed_operators:
                    raise ValueError("عملگر نامعتبر")

                left = solve(node.left)
                right = solve(node.right)

                if op_type in (ast.Div, ast.Mod) and right == 0:
                    raise ZeroDivisionError

                return allowed_operators[op_type](left, right)

            if isinstance(node, ast.UnaryOp):
                op_type = type(node.op)
                if op_type not in allowed_operators:
                    raise ValueError("عملگر نامعتبر")
                return allowed_operators[op_type](solve(node.operand))

            raise ValueError("عبارت نامعتبر")

        tree = ast.parse(expr, mode="eval")
        answer = solve(tree)

        if isinstance(answer, float) and answer.is_integer():
            return str(int(answer))

        return str(round(answer, 10))

    def calculate(key):
        nonlocal expression

        if key == "AC":
            expression = ""
            display.value = "0"
            history.value = ""

        elif key == "⌫":
            expression = expression[:-1]
            display.value = expression or "0"

        elif key == "=":
            if not expression:
                return

            try:
                answer = safe_calculate(expression)
                history.value = expression + " ="
                expression = answer
                display.value = answer
            except ZeroDivisionError:
                history.value = "تقسیم بر صفر امکان‌پذیر نیست"
                display.value = "خطا"
                expression = ""
            except Exception:
                history.value = "عبارت واردشده معتبر نیست"
                display.value = "خطا"
                expression = ""

        elif key == "%":
            try:
                if expression:
                    expression = str(float(expression) / 100)
                    display.value = expression
            except ValueError:
                history.value = "ابتدا یک عدد وارد کن"

        elif key in ["+", "-", "×", "÷"]:
            if not expression:
                if key == "-":
                    expression = "-"
            elif expression[-1] in ["+", "-", "×", "÷"]:
                expression = expression[:-1] + key
            else:
                expression += key

            display.value = expression or "0"

        elif key == ".":
            # جلوگیری از وارد کردن چند ممیز در یک عدد
            current_number = expression
            for op in ["+", "-", "×", "÷"]:
                current_number = current_number.split(op)[-1]

            if "." not in current_number:
                expression += "." if expression else "0."
            display.value = expression

        else:
            expression += key
            display.value = expression

        page.update()

    def make_button(label, color="#1E293B", text_color="#F8FAFC"):
        return ft.Container(
            content=ft.Text(
                label,
                size=22,
                color=text_color,
                weight=ft.FontWeight.W_500,
            ),
            bgcolor=color,
            border_radius=16,
            alignment=ft.Alignment.CENTER,
            height=60,
            expand=1,
            ink=True,
            on_click=lambda e, k=label: calculate(k),
        )

    def make_row(labels):
        controls = []

        for label in labels:
            if label in ["AC", "⌫", "%"]:
                controls.append(
                    make_button(label, "#334155", "#38BDF8")
                )
            elif label in ["÷", "×", "-", "+"]:
                controls.append(
                    make_button(label, "#0369A1")
                )
            elif label == "=":
                controls.append(
                    make_button(label, "#22C55E", "#052E16")
                )
            else:
                controls.append(make_button(label))

        return ft.Row(
            controls=controls,
            spacing=10,
            expand=True,
        )

    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "CALCULATOR",
                            size=14,
                            color="#38BDF8",
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Container(expand=True),
                        ft.Text("✦", size=24, color="#38BDF8"),
                    ],
                ),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=history,
                                alignment=ft.Alignment.CENTER_RIGHT,
                            ),
                            ft.Container(height=12),
                            ft.Container(
                                content=display,
                                alignment=ft.Alignment.CENTER_RIGHT,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                    bgcolor="#1E293B",
                    border_radius=22,
                    padding=20,
                    height=140,
                    alignment=ft.Alignment.CENTER_RIGHT,
                ),
                ft.Container(height=5),
                make_row(["AC", "⌫", "%", "÷"]),
                make_row(["7", "8", "9", "×"]),
                make_row(["4", "5", "6", "-"]),
                make_row(["1", "2", "3", "+"]),
                make_row(["0", ".", "=", "AC"]),
            ],
            spacing=12,
            expand=True,
        )
    )


ft.run(main, view=ft.AppView.WEB_BROWSER)

