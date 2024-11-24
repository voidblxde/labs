import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from stl import mesh
import numpy as np

# Загрузка STL-файла
stl_path = "./Sphere.STL"
stl_model = mesh.Mesh.from_file(stl_path)

vectors = stl_model.vectors  # Треугольники модели


def shift_to_center(triangles):
    """Центрирование объекта относительно начала координат."""
    min_p = np.min(triangles, axis=(0, 1))
    max_p = np.max(triangles, axis=(0, 1))
    center = (min_p + max_p) / 2
    return triangles - center


def compute_filled_section(triangles, plane_normal, plane_point):
    """
    Вычисление пересечений треугольников с плоскостью.
    Возвращает список вершин для замкнутого полигона.
    """
    intersections = []

    for triangle in triangles:
        points = []
        for i in range(3):
            p1 = triangle[i]
            p2 = triangle[(i + 1) % 3]

            d1 = np.dot(plane_normal, p1 - plane_point)
            d2 = np.dot(plane_normal, p2 - plane_point)

            if d1 * d2 < 0:  # Точки по разные стороны плоскости
                t = d1 / (d1 - d2)
                intersection = p1 + t * (p2 - p1)
                points.append(intersection)

        if len(points) == 2:
            intersections.extend(points)

    if len(intersections) < 3:
        return []  # Недостаточно точек для полигона

    # Преобразуем intersections в numpy массив
    intersections = np.array(intersections)

    # Упорядочивание точек пересечения по углу вокруг центра тяжести
    center = np.mean(intersections, axis=0)
    angles = np.arctan2(intersections[:, 1] - center[1], intersections[:, 0] - center[0])
    sorted_points = intersections[np.argsort(angles)]

    return sorted_points


def save_intersections_to_file(vertices, filename="sections.txt"):
    """Сохранение координат сечения в текстовый файл."""
    with open(filename, "w") as file:
        for vertex in vertices:
            file.write(f"{vertex[0]} {vertex[1]} {vertex[2]}\n")


def draw_stl(triangles):
    """Отрисовка STL модели в режиме wireframe."""
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_TRIANGLES)
    glColor3f(5.0, 5.0, 5.0)
    for triangle in triangles:
        for vertex in triangle:
            glVertex3fv(vertex)
    glEnd()


def draw_filled_section(vertices):
    """Отрисовка заполненного сечения."""
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glBegin(GL_POLYGON)
    glColor3f(1.0, 0.4, 0.4)
    for vertex in vertices:
        glVertex3fv(vertex)
    glEnd()


# Центрируем модель
triangles = shift_to_center(vectors)

# Определяем плоскость
plane_normal = np.array([0, 0, 1])  # Нормаль плоскости
plane_point = np.array([0, 0, 0])  # Точка на плоскости

# Вычисляем заполненное сечение
filled_section = compute_filled_section(triangles, plane_normal, plane_point)

# Сохраняем координаты сечения
save_intersections_to_file(filled_section)

# Настройка OpenGL
pygame.init()
FPS = 30
clock = pygame.time.Clock()

display = pygame.display.set_mode((1200, 800), DOUBLEBUF | OPENGL, 24)
gluPerspective(45, 1, 1, 500)
glClearColor(0.5, 0.5, 0.5, 1.0)
glTranslate(0, 0, -5)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                glRotatef(event.rel[0], 0, 1, 0)
                glRotatef(event.rel[1], 1, 0, 0)

        if event.type == pygame.MOUSEWHEEL:
            scale = event.y / 10 + 1
            glScalef(scale, scale, scale)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Отрисовка STL модели и заполненного сечения
    draw_stl(triangles)
    draw_filled_section(filled_section)

    pygame.display.flip()
    pygame.display.set_caption(str(clock.get_fps()))
    clock.tick(FPS)

pygame.quit()