import os
import msvcrt  # Используется для отслеживания нажатий клавиш в Windows
import time
from colorama import Fore, Style, init

# Инициализация colorama для работы в Windows
init()

# --- Настройки меню ---
MENU_ITEMS = [
    "Играть",
    "Скины",
    "Настройки",
    "Сюжет",
    "Выход"
]

# --- Цвета и стили ---
COLOR_TITLE = Fore.YELLOW + Style.BRIGHT
COLOR_MOUNTAIN = Fore.WHITE
COLOR_TEXT = Fore.CYAN
COLOR_SELECTED = Fore.YELLOW
RESET_STYLE = Style.RESET_ALL

# --- ASCII-арт в горном стиле ---
MOUNTAIN_ART = f"""
{COLOR_MOUNTAIN}
        /\\
       /  \\
      /    \\
     /      \\
    /        \\
   /__________\\
      ||||||
{RESET_STYLE}
"""

def print_menu(selected_index):
    """Очищает экран и отображает меню."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(MOUNTAIN_ART)
    print(f"{COLOR_TITLE}Добро пожаловать в Горный Раннер!{RESET_STYLE}\n")
    
    for i, item in enumerate(MENU_ITEMS):
        if i == selected_index:
            # Выделяем выбранный пункт
            print(f"{COLOR_SELECTED} > {item}{RESET_STYLE}")
        else:
            print(f"{COLOR_TEXT}   {item}{RESET_STYLE}")
            
    print("\n(Используйте стрелки Вверх/Вниз для навигации, Enter для выбора)")

def main():
    """Основной цикл программы."""
    current_selection = 0
    
    while True:
        print_menu(current_selection)
        
        # Ожидаем нажатия клавиши (только для Windows)
        key = msvcrt.getch()

        if key == b'\xe0':  # Специальные клавиши (стрелки)
            key = msvcrt.getch()
            if key == b'H':  # Стрелка вверх
                current_selection = (current_selection - 1) % len(MENU_ITEMS)
            elif key == b'P':  # Стрелка вниз
                current_selection = (current_selection + 1) % len(MENU_ITEMS)
        
        elif key == b'\r':  # Клавиша Enter
            selected_item = MENU_ITEMS[current_selection]
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Вы выбрали: {COLOR_SELECTED}{selected_item}{RESET_STYLE}\n")

            if selected_item == "Играть":
                print("Загрузка игры...")
                # Здесь будет код для запуска вашей игры
                time.sleep(2)
            elif selected_item == "Выход":
                print("До встречи!")
                break
            else:
                print("Этот раздел находится в разработке.")
                time.sleep(2)

if __name__ == "__main__":
    main()