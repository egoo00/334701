import pygame
import sys
import random
import math # Импортируем модуль math для математических функций

# --- Инициализация Pygame ---
pygame.init()
pygame.mixer.init() # NEW ENTRY

# --- Настройки окна ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Горный Раннер")

# --- Генерация звезд (делаем один раз при запуске) ---
STARS = [(random.randint(0, SCREEN_WIDTH), random.randint(0, int(SCREEN_HEIGHT * 0.7)), random.randint(1, 2)) for _ in range(150)]

# --- Цвета ---
COLOR_TITLE = (255, 215, 0)      # Золотой
COLOR_TEXT = (200, 200, 255)     # Светло-лавандовый
COLOR_SELECTED = (255, 255, 255) # Белый

# --- Шрифты ---
try:
    title_font = pygame.font.SysFont('Corbel', 72, bold=True)
    item_font = pygame.font.SysFont('Corbel', 50, bold=True)
    text_font = pygame.font.SysFont('Corbel', 28, bold=False) # ШРИФТ ДЛЯ ТЕКСТА
except:
    title_font = pygame.font.Font(None, 80)
    item_font = pygame.font.Font(None, 60)
    text_font = pygame.font.Font(None, 36)

# --- Состояние игры и меню ---
music_on = True
current_menu = 'main' # 'main', 'settings', 'authors', 'license'

# Загрузка и запуск музыки # NEW ENTRY
try:
    pygame.mixer.music.load(r'c:\Users\Belan\Downloads\Nature_Sounds_Rasslablyayushhie_instrumentalnye_zvuki_prirody_Ansambl_zvukov_prirody_Priroda_KHoroshie_zvuki_dlya_uma_i_tela_Optimalnyjj_Relaks_Proekt_-_Veter_v_Gorakh_dlya_Relaksa_79626999.mp3')
    pygame.mixer.music.play(-1) # -1 означает зацикливание
    if not music_on:
        pygame.mixer.music.pause()
except pygame.error as e:
    print(f"Ошибка загрузки или воспроизведения музыки: {e}")
    music_on = False

# Загрузка фоновых изображений для глав -- ПЕРЕПИСАНО
CHAPTER_BACKGROUNDS = []
CHAPTER_PLACEHOLDERS = [ # Запасные цвета, если картинки не загрузятся
    (40, 40, 80), (60, 40, 60), (40, 60, 40),
    (60, 50, 30), (30, 50, 60), (50, 30, 50)
]
try:
    image_paths = [
        r'c:\Users\Belan\Downloads\i.webp',
        r'c:\Users\Belan\Downloads\i (1).webp',
        r'c:\Users\Belan\Downloads\i (2).webp',
        r'c:\Users\Belan\Downloads\i (3).webp',
        r'c:\Users\Belan\Downloads\i (4).webp',
        r'c:\Users\Belan\Downloads\i (5).webp'
    ]
    for path in image_paths:
        img = pygame.image.load(path)
        CHAPTER_BACKGROUNDS.append(pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT)))
    if len(CHAPTER_BACKGROUNDS) != len(image_paths):
        print("ВНИМАНИЕ: Не все изображения глав были загружены. Будут использованы цветные заглушки.")
        CHAPTER_BACKGROUNDS = [] # Используем заглушки, если хотя бы одно изображение не загрузилось
except pygame.error as e:
    print(f"Ошибка загрузки фоновых изображений: {e}. Будут использованы цветные заглушки.")
    CHAPTER_BACKGROUNDS = []

# --- Данные для всех меню и экранов ---
MENU_DATA = {
    'main': {
        'title': "Горный Раннер",
        'items': ["Играть", "Скины", "Настройки", "Сюжет", "Выход"],
        'selected_index': 0
    },
    'settings': {
        'title': "Настройки",
        'items': ["Музыка: Вкл", "Авторы", "Лицензионное соглашение", "Назад"],
        'selected_index': 0
    },
    'authors': {
        'title': "Авторы",
        'lines': [
            "Идея и разработка: [Ваше Имя]",
            "",
            "Графика: Процедурная генерация",
            "Музыка: [Будет добавлена]",
            "",
            "Нажмите ESC для возврата"
        ]
    },
    'license': {
        'title': "Лицензия",
        'lines': [
            "Этот проект является демонстрационным.",
            "Все права на идею и код защищены.",
            "",
            "Копирование и распространение без разрешения запрещено.",
            "",
            "Нажмите ESC для возврата"
        ]
    },
    'skins': {
        'title': "Скины",
        'skins_list': [
            {'name': 'Стандартный', 'color': (100, 100, 255)}, # Синий
            {'name': 'Красный', 'color': (255, 100, 100)},    # Красный
            {'name': 'Зеленый', 'color': (100, 255, 100)}     # Зеленый
        ],
        'selected_skin_index': 0
    },
    # ДАННЫЕ ГЛАВ -- ПЕРЕПИСАНЫ
    'chapter_select': {
        'title': "Выбор Главы",
        'current_chapter_index': 0,
        'mode': 'chapter',  # 'chapter' или 'level'
        'selected_level_index': 0,
        'chapters': [
            # Генерируем 6 глав, первая открыта, остальные закрыты
            {'name': f'Глава {i+1}', 'locked': i > 0, 'levels': [{'number': j+1, 'completed': False} for j in range(6)]}
            for i in range(6)
        ]
    }
}

# --- Цвета для пейзажа (Фотореалистичная палитра) ---
COLOR_SKY_TOP = (15, 20, 40)         # Глубокий ночной синий
COLOR_SKY_BOTTOM = (40, 30, 70)      # Фиолетовый на горизонте
COLOR_SEA = (10, 15, 35)             # Очень темное море
COLOR_MOUNTAIN_FAR = (35, 40, 65)    # Дальние горы в тумане
COLOR_MOUNTAIN_NEAR = (25, 30, 55)   # Ближние горы
COLOR_SUN_CENTER = (255, 255, 230)   # Центр солнца/луны
COLOR_SUN_GLOW = (230, 210, 180)   # Мягкое свечение
COLOR_HAZE = (100, 90, 120)          # Цвет дымки/тумана

def draw_background():
    """Рисует фотореалистичный фон с туманом, звездами и текстурами."""
    horizon = int(SCREEN_HEIGHT * 0.7)

    # Градиент неба
    for y in range(horizon):
        ratio = y / horizon
        r = int(COLOR_SKY_TOP[0] * (1 - ratio) + COLOR_SKY_BOTTOM[0] * ratio)
        g = int(COLOR_SKY_TOP[1] * (1 - ratio) + COLOR_SKY_BOTTOM[1] * ratio)
        b = int(COLOR_SKY_TOP[2] * (1 - ratio) + COLOR_SKY_BOTTOM[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # Звезды
    for x, y, size in STARS:
        pygame.draw.circle(screen, (255, 255, 255, random.randint(100, 200)), (x, y), size)

    # Море
    pygame.draw.rect(screen, COLOR_SEA, (0, horizon, SCREEN_WIDTH, SCREEN_HEIGHT - horizon))

    # Солнце/Луна со свечением
    sun_pos = (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.25)
    glow_surface = pygame.Surface((140, 140), pygame.SRCALPHA)
    pygame.draw.circle(glow_surface, (*COLOR_SUN_GLOW, 50), (70, 70), 70)
    pygame.draw.circle(glow_surface, (*COLOR_SUN_GLOW, 80), (70, 70), 50)
    screen.blit(glow_surface, (sun_pos[0] - 70, sun_pos[1] - 70))
    pygame.draw.circle(screen, COLOR_SUN_CENTER, sun_pos, 30)

    # Атмосферная дымка/туман на горизонте
    haze_surface = pygame.Surface((SCREEN_WIDTH, 120), pygame.SRCALPHA)
    haze_surface.fill((*COLOR_HAZE, 30)) # Полупрозрачный слой
    screen.blit(haze_surface, (0, horizon - 80))

    # Дальние горы
    far_mountains_poly = [
        (0, horizon), (SCREEN_WIDTH * 0.1, horizon - 80), (SCREEN_WIDTH * 0.2, horizon - 60),
        (SCREEN_WIDTH * 0.35, horizon - 90), (SCREEN_WIDTH * 0.5, horizon - 100),
        (SCREEN_WIDTH * 0.6, horizon - 70), (SCREEN_WIDTH * 0.8, horizon - 85), (SCREEN_WIDTH, horizon)
    ]
    pygame.draw.polygon(screen, COLOR_MOUNTAIN_FAR, far_mountains_poly)

    # Ближние горы
    near_mountains_poly = [
        (0, SCREEN_HEIGHT), (0, horizon + 20), (SCREEN_WIDTH * 0.15, horizon - 40),
        (SCREEN_WIDTH * 0.3, horizon + 15), (SCREEN_WIDTH * 0.5, horizon - 50),
        (SCREEN_WIDTH * 0.75, horizon + 20), (SCREEN_WIDTH * 0.85, horizon - 30),
        (SCREEN_WIDTH, horizon + 40), (SCREEN_WIDTH, SCREEN_HEIGHT)
    ]
    pygame.draw.polygon(screen, COLOR_MOUNTAIN_NEAR, near_mountains_poly)

    # Текстура "шума" на ближних горах для детализации
    for _ in range(50): # Уменьшено количество точек с 200 до 50
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(horizon - 50, SCREEN_HEIGHT)
        # Проверяем, находится ли точка внутри полигона ближних гор (упрощенная проверка)
        if y > horizon + (-0.2 * x + 20): # Очень грубая проверка, но быстрая
            # Замедление мерцания: используем более статичный альфа-канал
            pygame.draw.circle(screen, (*(255,255,255), 10), (x, y), 1) # Увеличена прозрачность (альфа с 2 до 10) для более мягкого эффекта

    # Улучшенное отражение на воде с имитацией волн и отражением звезд
    reflection_y_start = horizon + 5
    num_reflection_lines = 30 # Увеличено количество линий для более детального отражения
    wave_amplitude = 10 # Увеличена амплитуда волны
    wave_frequency = 0.005 # Замедлена частота волны
    time_offset = pygame.time.get_ticks() * wave_frequency

    # Отражение солнца/луны
    for i in range(num_reflection_lines):
        y = reflection_y_start + i * 3
        width = 80 - i * 2.5
        alpha = max(0, 120 - i * 4) # Более плавное затухание
        if width > 0 and alpha > 0:
            wave_offset = int(wave_amplitude * math.sin(time_offset + i * 0.3))
            color = (*COLOR_SUN_GLOW, alpha)
            reflection_surface = pygame.Surface((width, 4), pygame.SRCALPHA)
            pygame.draw.ellipse(reflection_surface, color, (0, 0, width, 4))
            screen.blit(reflection_surface, (sun_pos[0] - width / 2 + random.randint(-5, 5) + wave_offset, y))

    # Отражение звезд
    for x, y, size in STARS:
        if y < horizon: # Отражаем только звезды выше горизонта
            reflection_y = horizon + (horizon - y) # Симметричное отражение
            # Добавляем небольшое искажение для имитации волн
            wave_offset_star = int(wave_amplitude * 0.5 * math.sin(time_offset + x * 0.01))
            alpha_star = max(0, 150 - int((reflection_y - horizon) * 2)) # Затухание отражения
            if alpha_star > 0:
                pygame.draw.circle(screen, (*(255, 255, 255), alpha_star), (x + wave_offset_star, reflection_y), size)

def draw_menu(menu_key, skip_item_index=-1):
    """Рисует все элементы указанного меню на экране."""
    menu = MENU_DATA[menu_key]
    title_text = menu['title']
    items = menu['items']
    selected_index = menu['selected_index']
    draw_background()
    title_surface = title_font.render(title_text, True, COLOR_TITLE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
    screen.blit(title_surface, title_rect)
    for i, item in enumerate(items):
        if i == skip_item_index:
            continue
        is_selected = (i == selected_index)
        shadow_color = (20, 20, 20)
        grad_top_color = (220, 220, 255)
        grad_bottom_color = (150, 150, 220)
        item_rect = item_font.render(item, True, (0,0,0)).get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + i * 60))
        if is_selected:
            grad_top_color = (255, 255, 255)
            grad_bottom_color = (255, 215, 0)
            item_rect.x += 15
        item_surface = item_font.render(item, True, (255,255,255))
        gradient_surface = pygame.Surface(item_surface.get_size(), pygame.SRCALPHA)
        width, height = item_surface.get_size()
        for y in range(height):
            ratio = y / height
            r = int(grad_top_color[0] * (1 - ratio) + grad_bottom_color[0] * ratio)
            g = int(grad_top_color[1] * (1 - ratio) + grad_bottom_color[1] * ratio)
            b = int(grad_top_color[2] * (1 - ratio) + grad_bottom_color[2] * ratio)
            pygame.draw.line(gradient_surface, (r, g, b), (0, y), (width, y))
        gradient_surface.blit(item_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        shadow_surface = item_font.render(item, True, shadow_color)
        shadow_rect = shadow_surface.get_rect(center=item_rect.center).move(5, 5)
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(gradient_surface, item_rect)

def draw_text_screen(menu_key):
    """Рисует простой экран с заголовком и текстом."""
    menu = MENU_DATA[menu_key]
    title_text = menu['title']
    lines = menu['lines']
    draw_background()
    title_surface = title_font.render(title_text, True, COLOR_TITLE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
    screen.blit(title_surface, title_rect)
    for i, line in enumerate(lines):
        line_surface = text_font.render(line, True, COLOR_TEXT)
        line_rect = line_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.2 + i * 40))
        screen.blit(line_surface, line_rect)

def draw_skins_screen():
    """Рисует экран выбора скинов с подиумом и текущим скином."""
    draw_background()
    menu = MENU_DATA['skins']
    title_text = menu['title']
    skins_list = menu['skins_list']
    selected_skin_index = menu['selected_skin_index']
    current_skin = skins_list[selected_skin_index]

    # Заголовок
    title_surface = title_font.render(title_text, True, COLOR_TITLE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
    screen.blit(title_surface, title_rect)

    # Подиум (простая геометрическая фигура)
    podium_color = (150, 150, 150) # Серый
    podium_width = 200
    podium_height = 80
    podium_x = (SCREEN_WIDTH - podium_width) / 2
    podium_y = SCREEN_HEIGHT - 150
    pygame.draw.rect(screen, podium_color, (podium_x, podium_y, podium_width, podium_height))
    pygame.draw.rect(screen, (100, 100, 100), (podium_x, podium_y, podium_width, podium_height), 5) # Граница

    # Отрисовка текущего скина (простой квадрат)
    skin_size = 100
    skin_x = SCREEN_WIDTH / 2 - skin_size / 2
    skin_y = podium_y - skin_size + 10 # Немного выше подиума
    pygame.draw.rect(screen, current_skin['color'], (skin_x, skin_y, skin_size, skin_size))
    pygame.draw.rect(screen, (20, 20, 20), (skin_x, skin_y, skin_size, skin_size), 3) # Граница скина

    # Название скина
    skin_name_surface = item_font.render(current_skin['name'], True, COLOR_TEXT)
    skin_name_rect = skin_name_surface.get_rect(center=(SCREEN_WIDTH / 2, podium_y + podium_height + 30))
    screen.blit(skin_name_surface, skin_name_rect)

    # Стрелки для переключения скинов
    arrow_color = COLOR_SELECTED
    arrow_size = 20
    # Левая стрелка
    pygame.draw.polygon(screen, arrow_color, [
        (podium_x - 50, podium_y + podium_height / 2),
        (podium_x - 30, podium_y + podium_height / 2 - arrow_size),
        (podium_x - 30, podium_y + podium_height / 2 + arrow_size)
    ])
    # Правая стрелка
    pygame.draw.polygon(screen, arrow_color, [
        (podium_x + podium_width + 50, podium_y + podium_height / 2),
        (podium_x + podium_width + 30, podium_y + podium_height / 2 - arrow_size),
        (podium_x + podium_width + 30, podium_y + podium_height / 2 + arrow_size)
    ])

def draw_chapter_select_screen(): # NEW ENTRY
    """Рисует экран выбора глав и уровней.""" # NEW ENTRY
    menu = MENU_DATA['chapter_select']
    chapter_index = menu['current_chapter_index']
    chapter = menu['chapters'][chapter_index]
    mode = menu.get('mode', 'chapter')
    selected_level_index = menu.get('selected_level_index', 0)

    # Фон, специфичный для главы
    if CHAPTER_BACKGROUNDS:
        screen.blit(CHAPTER_BACKGROUNDS[chapter_index], (0, 0))
    else:
        screen.fill(CHAPTER_PLACEHOLDERS[chapter_index % len(CHAPTER_PLACEHOLDERS)])

    # Заголовок (название главы)
    title_surface = title_font.render(chapter['name'], True, COLOR_TITLE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
    screen.blit(title_surface, title_rect)

    # Стрелки для навигации глав
    if mode == 'chapter':
        arrow_color = COLOR_SELECTED
        arrow_size = 30
        pygame.draw.polygon(screen, arrow_color, [
            (50, SCREEN_HEIGHT / 2),
            (80, SCREEN_HEIGHT / 2 - arrow_size),
            (80, SCREEN_HEIGHT / 2 + arrow_size)
        ])
        pygame.draw.polygon(screen, arrow_color, [
            (SCREEN_WIDTH - 50, SCREEN_HEIGHT / 2),
            (SCREEN_WIDTH - 80, SCREEN_HEIGHT / 2 - arrow_size),
            (SCREEN_WIDTH - 80, SCREEN_HEIGHT / 2 + arrow_size)
        ])

        # Отображаем превью соседних глав
        num_chapters = len(menu['chapters'])
        prev_chapter_index = (chapter_index - 1) % num_chapters
        next_chapter_index = (chapter_index + 1) % num_chapters
        
        thumb_size = (200, 112)
        
        # Превью предыдущей главы
        if CHAPTER_BACKGROUNDS:
            prev_thumb = pygame.transform.scale(CHAPTER_BACKGROUNDS[prev_chapter_index], thumb_size)
        else:
            prev_thumb = pygame.Surface(thumb_size)
            prev_thumb.fill(CHAPTER_PLACEHOLDERS[prev_chapter_index % len(CHAPTER_PLACEHOLDERS)])
        prev_thumb_rect = prev_thumb.get_rect(center=(150, SCREEN_HEIGHT / 2))
        screen.blit(prev_thumb, prev_thumb_rect)
        dark = pygame.Surface(thumb_size, pygame.SRCALPHA)
        dark.fill((0,0,0,100))
        screen.blit(dark, prev_thumb_rect)
        pygame.draw.rect(screen, COLOR_SELECTED, prev_thumb_rect, 3)

        # Превью следующей главы
        if CHAPTER_BACKGROUNDS:
            next_thumb = pygame.transform.scale(CHAPTER_BACKGROUNDS[next_chapter_index], thumb_size)
        else:
            next_thumb = pygame.Surface(thumb_size)
            next_thumb.fill(CHAPTER_PLACEHOLDERS[next_chapter_index % len(CHAPTER_PLACEHOLDERS)])
        next_thumb_rect = next_thumb.get_rect(center=(SCREEN_WIDTH - 150, SCREEN_HEIGHT / 2))
        screen.blit(next_thumb, next_thumb_rect)
        dark2 = pygame.Surface(thumb_size, pygame.SRCALPHA)
        dark2.fill((0,0,0,100))
        screen.blit(dark2, next_thumb_rect)
        pygame.draw.rect(screen, COLOR_SELECTED, next_thumb_rect, 3)

    if chapter['locked']:
        # Иконка замка
        lock_font = pygame.font.SysFont('Arial', 200)
        lock_surface = lock_font.render('🔒', True, COLOR_TITLE)
        lock_rect = lock_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(lock_surface, lock_rect)
    else:
        # Отображение уровней
        level_size = 80
        level_padding = 20
        grid_cols = 3
        grid_rows = 2
        start_x = (SCREEN_WIDTH - (grid_cols * (level_size + level_padding) - level_padding)) / 2
        start_y = (SCREEN_HEIGHT - (grid_rows * (level_size + level_padding) - level_padding)) / 2 + 50

        for i, level in enumerate(chapter['levels']):
            row = i // grid_cols
            col = i % grid_cols
            x = start_x + col * (level_size + level_padding)
            y = start_y + row * (level_size + level_padding)
            level_rect = pygame.Rect(x, y, level_size, level_size)
            # Подсветка выбранного уровня
            if mode == 'level' and i == selected_level_index:
                pygame.draw.rect(screen, (255, 220, 100), level_rect, border_radius=18)
            pygame.draw.rect(screen, (200, 200, 200), level_rect, border_radius=15)
            pygame.draw.rect(screen, (100, 100, 100), level_rect, 5, border_radius=15)
            level_font = pygame.font.SysFont('Corbel', 50, bold=True)
            level_text = level_font.render(str(level['number']), True, (50, 50, 50))
            text_rect = level_text.get_rect(center=level_rect.center)
            screen.blit(level_text, text_rect)

def run_selection_animation(menu_key, index):
    """Запускает анимацию 'расплытия' для выбранного пункта меню."""
    clock = pygame.time.Clock()
    menu = MENU_DATA[menu_key]
    item_text = menu['items'][index]
    item_surface_for_size = item_font.render(item_text, True, (0,0,0))
    item_rect = item_surface_for_size.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + index * 60))
    item_rect.x += 15
    grad_top_color = (255, 255, 255)
    grad_bottom_color = (255, 215, 0)
    item_surface_mask = item_font.render(item_text, True, (255, 255, 255))
    gradient_surface = pygame.Surface(item_surface_mask.get_size(), pygame.SRCALPHA)
    width, height = item_surface_mask.get_size()
    for y in range(height):
        ratio = y / height
        r = int(grad_top_color[0] * (1 - ratio) + grad_bottom_color[0] * ratio)
        g = int(grad_top_color[1] * (1 - ratio) + grad_bottom_color[1] * ratio)
        b = int(grad_top_color[2] * (1 - ratio) + grad_bottom_color[2] * ratio)
        pygame.draw.line(gradient_surface, (r, g, b), (0, y), (width, y))
    gradient_surface.blit(item_surface_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    for i in range(25):
        draw_menu(menu_key, skip_item_index=index)
        blur_offset = i * 0.6
        alpha = max(0, 255 - i * 11)
        temp_surface = gradient_surface.copy()
        temp_surface.set_alpha(alpha)
        screen.blit(temp_surface, item_rect.move(-blur_offset, -blur_offset))
        screen.blit(temp_surface, item_rect.move(blur_offset, -blur_offset))
        screen.blit(temp_surface, item_rect.move(-blur_offset, blur_offset))
        screen.blit(temp_surface, item_rect.move(blur_offset, blur_offset))
        pygame.display.flip()
        clock.tick(60)

def draw_gameplay_screen(state):
    """Рисует стартовую сцену: скин на воде между двух скал."""
    # Фон — вода
    screen.fill((30, 40, 80))
    # Левая скала
    pygame.draw.rect(screen, (60, 60, 60), (0, 0, 80, SCREEN_HEIGHT))
    # Правая скала
    pygame.draw.rect(screen, (60, 60, 60), (SCREEN_WIDTH-80, 0, 80, SCREEN_HEIGHT))
    # Вода с анимацией волн
    water_rect = pygame.Rect(80, SCREEN_HEIGHT//2, SCREEN_WIDTH-160, SCREEN_HEIGHT//2)
    
    # Создаем поверхность для воды
    water_surface = pygame.Surface((water_rect.width, water_rect.height), pygame.SRCALPHA)
    
    # Параметры волн
    wave_amplitude = 8
    wave_frequency = 0.02
    time_offset = pygame.time.get_ticks() * wave_frequency

    # Рисуем волны
    for x in range(water_rect.width):
        y_offset = int(wave_amplitude * math.sin(time_offset + x * 0.03))
        color_value = 180 + y_offset * 4 # Меняем цвет в зависимости от высоты волны
        pygame.draw.line(water_surface, (40, 80, color_value), (x, y_offset), (x, water_rect.height))

    screen.blit(water_surface, (water_rect.x, water_rect.y))

    # Скин (квадратик)
    skin = MENU_DATA['skins']['skins_list'][state['skin_index']]
    skin_size = 60
    skin_x = SCREEN_WIDTH//2 - skin_size//2
    skin_y = SCREEN_HEIGHT//2 + 40
    pygame.draw.rect(screen, skin['color'], (skin_x, skin_y, skin_size, skin_size), border_radius=10)
    pygame.draw.rect(screen, (20, 20, 20), (skin_x, skin_y, skin_size, skin_size), 3, border_radius=10)

# --- Основной цикл игры ---
running = True
clock = pygame.time.Clock()
while running:
    # 1. Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Логика для меню с выбором (главное и настройки)
            if current_menu in ['main', 'settings']:
                active_menu_data = MENU_DATA[current_menu]
                if event.key == pygame.K_UP:
                    active_menu_data['selected_index'] = (active_menu_data['selected_index'] - 1) % len(active_menu_data['items'])
                elif event.key == pygame.K_DOWN:
                    active_menu_data['selected_index'] = (active_menu_data['selected_index'] + 1) % len(active_menu_data['items'])
                elif event.key == pygame.K_RETURN:
                    selected_index = active_menu_data['selected_index']
                    selected_item = active_menu_data['items'][selected_index]
                    run_selection_animation(current_menu, selected_index)

                    if current_menu == 'main':
                        if selected_item == "Играть": 
                            current_menu = 'chapter_select'
                            MENU_DATA['chapter_select']['mode'] = 'chapter' # Сброс режима при входе
                        elif selected_item == "Скины": current_menu = 'skins'
                        elif selected_item == "Настройки": current_menu = 'settings'
                        elif selected_item == "Выход": running = False
                        else: print(f"Выбран пункт: {selected_item}")
                    
                    elif current_menu == 'settings':
                        if selected_item.startswith("Музыка"):
                            music_on = not music_on
                            MENU_DATA['settings']['items'][0] = f"Музыка: {'Вкл' if music_on else 'Выкл'}"
                            if music_on: # NEW ENTRY
                                pygame.mixer.music.unpause() # NEW ENTRY
                            else: # NEW ENTRY
                                pygame.mixer.music.pause() # NEW ENTRY
                        elif selected_item == "Авторы": current_menu = 'authors'
                        elif selected_item == "Лицензионное соглашение": current_menu = 'license'
                        elif selected_item == "Назад": current_menu = 'main'

            # Общая логика для всех экранов -- ПЕРЕПИСАНО
            if event.key == pygame.K_ESCAPE:
                if current_menu in ['authors', 'license']:
                    current_menu = 'settings'
                elif current_menu in ['settings', 'skins']:
                    current_menu = 'main'
                elif current_menu == 'chapter_select':
                    # Если в режиме выбора уровня, вернуться к выбору глав
                    if MENU_DATA['chapter_select']['mode'] == 'level':
                        MENU_DATA['chapter_select']['mode'] = 'chapter'
                    # Если в режиме выбора глав, вернуться в главное меню
                    else:
                        current_menu = 'main'
                elif current_menu == 'gameplay':
                    # Вернуться к выбору уровня
                    current_menu = 'chapter_select'
                    MENU_DATA['chapter_select']['mode'] = 'level'
                else: # Из главного меню - выход
                    running = False

            # Логика для меню скинов
            if current_menu == 'skins':
                skins_data = MENU_DATA['skins']
                if event.key == pygame.K_LEFT:
                    skins_data['selected_skin_index'] = (skins_data['selected_skin_index'] - 1) % len(skins_data['skins_list'])
                elif event.key == pygame.K_RIGHT:
                    skins_data['selected_skin_index'] = (skins_data['selected_skin_index'] + 1) % len(skins_data['skins_list'])

            # Логика для меню выбора глав и уровней -- УПРОЩЕНО
            if current_menu == 'chapter_select':
                chapter_data = MENU_DATA['chapter_select']
                chapter = chapter_data['chapters'][chapter_data['current_chapter_index']]
                mode = chapter_data['mode'] # Больше не используем .get()

                if mode == 'chapter':
                    if event.key == pygame.K_LEFT:
                        chapter_data['current_chapter_index'] = (chapter_data['current_chapter_index'] - 1) % len(chapter_data['chapters'])
                    elif event.key == pygame.K_RIGHT:
                        chapter_data['current_chapter_index'] = (chapter_data['current_chapter_index'] + 1) % len(chapter_data['chapters'])
                    elif event.key == pygame.K_RETURN and not chapter['locked']:
                        chapter_data['mode'] = 'level'
                        chapter_data['selected_level_index'] = 0
                elif mode == 'level':
                    num_levels = len(chapter['levels'])
                    if event.key == pygame.K_LEFT:
                        chapter_data['selected_level_index'] = (chapter_data['selected_level_index'] - 1) % num_levels
                    elif event.key == pygame.K_RIGHT:
                        chapter_data['selected_level_index'] = (chapter_data['selected_level_index'] + 1) % num_levels
                    elif event.key == pygame.K_UP:
                        chapter_data['selected_level_index'] = (chapter_data['selected_level_index'] - 3) % num_levels
                    elif event.key == pygame.K_DOWN:
                        chapter_data['selected_level_index'] = (chapter_data['selected_level_index'] + 3) % num_levels
                    elif event.key == pygame.K_RETURN:
                        # Переход в игровой режим
                        current_menu = 'gameplay'
                        gameplay_state = {
                            'chapter_index': chapter_data['current_chapter_index'],
                            'level_index': chapter_data['selected_level_index'],
                            'skin_index': MENU_DATA['skins']['selected_skin_index']
                        }
                    # elif event.key == pygame.K_ESCAPE: # Эта логика теперь в общем обработчике
                    #     chapter_data['mode'] = 'chapter'

    # 2. Отрисовка в зависимости от состояния
    if current_menu in ['main', 'settings']:
        draw_menu(current_menu)
    elif current_menu in ['authors', 'license']:
        draw_text_screen(current_menu)
    elif current_menu == 'skins':
        draw_skins_screen()
    elif current_menu == 'chapter_select':
        draw_chapter_select_screen()
    elif current_menu == 'gameplay':
        draw_gameplay_screen(gameplay_state)

    # 3. Обновление экрана
    pygame.display.flip()
    clock.tick(60)

# --- Завершение работы ---
pygame.quit()
sys.exit()