import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Глобальные переменные для хранения координат и цветов точек
static_points = []
static_colors = []

# Инициализация окна
def init_window(title):
    if not glfw.init():
        return None
    window = glfw.create_window(640, 480, title, None, None)
    if not window:
        glfw.terminate()
        return None
    glfw.make_context_current(window)
    return window

# Настройка перспективы
def setup_scene():
    glClearColor(0.5, 0.5, 0.75, 1.0)  # Цвет фона
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Очистка буферов
    glEnable(GL_DEPTH_TEST)  # Включаем тест глубины
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 640 / 480, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Функция для рисования куба
def draw_cube(angle_x, angle_y):
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -7.0)  # Перемещаем куб
    glRotatef(angle_x, 1.0, 0.0, 0.0)  # Вращение вокруг оси X
    glRotatef(angle_y, 0.0, 1.0, 0.0)  # Вращение вокруг оси Y
    glBegin(GL_QUADS)

    # Верхняя грань
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)

    # Нижняя грань
    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)

    # Передняя грань
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    # Задняя грань
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)

    # Левая грань
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)

    # Правая грань
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glEnd()

# Инициализация статичных точек
def init_static_points(num_points=500):
    global static_points, static_colors
    static_points = [(np.random.uniform(-1, 1), np.random.uniform(-1, 1), np.random.uniform(-1, 1)) for _ in range(num_points)]
    static_colors = [(np.random.rand(), np.random.rand(), np.random.rand()) for _ in range(num_points)]

# Функция для рисования вращающегося массива точек
def draw_points(angle_x, angle_y):
    global static_points, static_colors
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)  # Перемещаем массив точек
    glRotatef(angle_x, 1.0, 0.0, 0.0)  # Вращение вокруг оси X
    glRotatef(angle_y, 0.0, 1.0, 0.0)  # Вращение вокруг оси Y
    glPointSize(5)
    glBegin(GL_POINTS)
    for point, color in zip(static_points, static_colors):
        glColor3f(*color)
        glVertex3f(*point)
    glEnd()

# Функция для рисования сферы
def draw_sphere(angle_x, angle_y):
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -6.0)
    glRotatef(angle_x, 1.0, 0.0, 0.0)
    glRotatef(angle_y, 0.0, 1.0, 0.0)

    # Настройка освещения
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    light_position = [5.0, 5.0, 5.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glPushMatrix()
    glScalef(1.0, 0.7, 1.0)  # Приплюснуть сферу по оси Y

    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    glColor3f(0.0, 0.7, 1.0)
    gluSphere(quadric, 1, 64, 64)

    glPopMatrix()

    glDisable(GL_LIGHTING)


# Функция для рисования сцены со сферой на кубе
def draw_sphere_and_cube(angle_x, angle_y):
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -20.0)  # Отодвинем сцену немного дальше
    glRotatef(angle_x, 1.0, 0.0, 0.0)
    glRotatef(angle_y, 0.0, 1.0, 0.0)

    # Рисуем куб
    glPushMatrix()
    glScalef(2.0, 2.0, 2.0)  # Увеличим размер куба
    glBegin(GL_QUADS)
    # Верхняя грань
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    # Нижняя грань
    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    # Передняя грань
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    # Задняя грань
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    # Левая грань
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    # Правая грань
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glEnd()
    glPopMatrix()

    # Рисуем сферу
    glPushMatrix()
    glTranslatef(0.0, 6.0, 0.0)  # Поднимаем сферу над кубом
    quadric = gluNewQuadric()
    glColor3f(0.0, 0.7, 1.0)
    gluSphere(quadric, 2.5, 32, 32)  # Увеличиваем радиус сферы до 2.5
    glPopMatrix()


# Главная функция для рисования каждой фигуры в отдельном окне
def main():
    windows = []

    # Инициализация окон для каждой фигуры
    windows.append(init_window("Cube"))
    windows.append(init_window("Points"))
    windows.append(init_window("Sphere"))
    windows.append(init_window("Sphere and Cube"))

    if None in windows:
        return

    # Инициализация статичных точек
    init_static_points()

    # Начальные углы поворота
    angle_x = 0.0
    angle_y = 0.0

    # Переменные для отслеживания состояния мыши
    is_mouse_pressed = False
    last_mouse_pos = (0, 0)

    # Функция для обработки мыши
    def mouse_button_callback(window, button, action, mods):
        nonlocal is_mouse_pressed, last_mouse_pos
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                is_mouse_pressed = True
                last_mouse_pos = glfw.get_cursor_pos(window)
            elif action == glfw.RELEASE:
                is_mouse_pressed = False

    # Функция для отслеживания перемещений мыши
    def cursor_position_callback(window, xpos, ypos):
        nonlocal angle_x, angle_y, last_mouse_pos
        if is_mouse_pressed:
            dx = xpos - last_mouse_pos[0]
            dy = ypos - last_mouse_pos[1]
            angle_x += dy * 0.5  # Изменение угла по X
            angle_y += dx * 0.5  # Изменение угла по Y
            last_mouse_pos = (xpos, ypos)

    # Устанавливаем обработчики событий для каждого окна
    for window in windows:
        glfw.set_mouse_button_callback(window, mouse_button_callback)
        glfw.set_cursor_pos_callback(window, cursor_position_callback)

    while not any([glfw.window_should_close(window) for window in windows]):
        # Рисуем куб
        glfw.make_context_current(windows[0])
        setup_scene()
        draw_cube(angle_x, angle_y)
        glfw.swap_buffers(windows[0])

        # Рисуем вращающийся массив точек
        glfw.make_context_current(windows[1])
        setup_scene()
        draw_points(angle_x, angle_y)
        glfw.swap_buffers(windows[1])

        # Рисуем сферу
        glfw.make_context_current(windows[2])
        setup_scene()
        draw_sphere(angle_x, angle_y)
        glfw.swap_buffers(windows[2])

        # Рисуем сферу и куб вместе
        glfw.make_context_current(windows[3])
        setup_scene()
        draw_sphere_and_cube(angle_x, angle_y)
        glfw.swap_buffers(windows[3])

        glfw.poll_events()

    for window in windows:
        glfw.destroy_window(window)

    glfw.terminate()


if __name__ == "__main__":
    main()