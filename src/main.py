import flet as ft
from random import choice

def main(page: ft.Page):
    page.title = "Random Choice Picker"
    
    # Create controls
    choices_input = ft.TextField(
        label="Enter choices separated by commas",
        expand=True,
        min_lines=3,
        max_lines=5,
        on_submit=lambda _: add_choices()
    )
    choices_list = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    result_text = ft.Text(size=20, weight=ft.FontWeight.BOLD)
    
    def delete_choice(choice_row):
        choices_list.controls.remove(choice_row)
        if not choices_list.controls:
            result_text.value = ""  # Clear result if all choices are deleted
        page.update()
    
    def add_choices():
        if not choices_input.value:
            return
            
        # Clear previous choices
        choices_list.controls.clear()
        result_text.value = ""
        
        # Split and add new choices
        choices = [choice.strip() for choice in choices_input.value.split(",") if choice.strip()]
        for choice_text in choices:
            # Create a delete button for this choice
            delete_btn = ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_color="red400",
                tooltip="Delete choice",
                on_click=lambda _, row=None: delete_choice(row)
            )
            
            # Create a row with the choice text and delete button
            choice_row = ft.Row(
                controls=[
                    ft.Text(choice_text, expand=True),
                    delete_btn
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            
            # Set the row reference for the delete button's callback
            delete_btn.on_click = lambda _, row=choice_row: delete_choice(row)
            
            choices_list.controls.append(choice_row)
        
        # Clear the input field
        choices_input.value = ""
        page.update()
    
    def pick_random():
        if not choices_list.controls:
            result_text.value = "Please add some choices first!"
        else:
            chosen_row = choice(choices_list.controls)
            chosen_text = chosen_row.controls[0].value  # Get text from the first control in the row
            result_text.value = f"Selected: {chosen_text}"
        page.update()
    
    # Create buttons
    add_button = ft.ElevatedButton("Add Choices", on_click=lambda _: add_choices())
    pick_button = ft.ElevatedButton(
        "Pick Random Choice",
        on_click=lambda _: pick_random(),
        icon=ft.Icons.CASINO
    )
    
    # Layout
    page.add(
        ft.Row([choices_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        choices_list,
        ft.Row([pick_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([result_text], alignment=ft.MainAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    # For development, use ft.app(main)
    # ft.app(main)
    # For web deployment, use ft.app(main, view=ft.AppView.WEB_BROWSER)
    ft.app(main, view=ft.AppView.WEB_BROWSER)
