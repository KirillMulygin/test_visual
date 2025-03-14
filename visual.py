import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Ваши данные
mapping_resources = {0: 0, 1: 'Энергетические', 2: 'Материальные', 3: 'Информационные', 4: 'Финансовые', 5: 'Трудовые'}
mapping_processes = {0: 0, 
                     1: 'Обеспечение Дворца спорта энергетическими ресурсами',
                     2: 'Обеспечение Дворца спорта материальными ресурсами',
                     3: 'Обеспечение Дворца спорта информационными ресурсами',
                     4: 'Обеспечение Дворца спорта финансовыми ресурсами',
                     5: 'Обеспечение Дворца спорта трудовыми ресурсами'}
mapping_functions = {0: 0,
                     1: 'Планирование',
                     2: 'Организация',
                     3: 'Регулирование',
                     4: 'Стимулирование',
                     5: 'Контроль',
                     6: 'Учет',
                     7: 'Анализ'}

# Генерируем координаты точек внутри куба
x_vals = np.arange(0, 6, 1)
y_vals = np.arange(0, 6, 1)
z_vals = np.arange(0, 8, 1)  

# Список точек внутри куба
grid_points = [(x, y, z) for x in x_vals for y in y_vals for z in z_vals]

# Разбираем координаты точек по осям
x_points, y_points, z_points = zip(*grid_points)

# Функция для создания ТОЛЬКО ортогональных соединений (без диагоналей)
def create_grid_edges(points):
    edges = []
    num_points = len(points)
    
    for i in range(num_points):
        x, y, z = points[i]

        # Проверяем соседей только вдоль осей X, Y, Z
        for j in range(i + 1, num_points):
            x2, y2, z2 = points[j]
            
            # Разрешаем соединения ТОЛЬКО если различается ТОЛЬКО одна координата
            dx, dy, dz = abs(x - x2), abs(y - y2), abs(z - z2)
            if (dx == 0 and dy == 0 and dz > 0) or \
               (dx == 0 and dz == 0 and dy > 0) or \
               (dy == 0 and dz == 0 and dx > 0):
                edges.append((i, j))

    return edges

# Генерируем правильные рёбра (без диагональных соединений)
edges = create_grid_edges(grid_points)

# Линии для отображения сетки
lines = []
for edge in edges:
    lines.append(go.Scatter3d(
        x=[x_points[edge[0]], x_points[edge[1]]],
        y=[y_points[edge[0]], y_points[edge[1]]],
        z=[z_points[edge[0]], z_points[edge[1]]],
        mode='lines',
        line=dict(color='green', width=2),
        showlegend=False,
        hoverinfo="skip"
    ))

# Точки для всех координат куба
points = go.Scatter3d(
    x=x_points,
    y=y_points,
    z=z_points,
    mode='markers',
    marker=dict(size=4, color='red'),
    showlegend=False,
    hovertemplate="Ресурсы: %{customdata[0]}<br>Процессы: %{customdata[1]}<br>Функции управления: %{customdata[2]}<extra></extra>",
    customdata=[[mapping_resources.get(x, "Неизвестно"), mapping_processes.get(y, "Неизвестно"), mapping_functions.get(z, "Неизвестно")] for x, y, z in zip(x_points, y_points, z_points)]
)

# Создание 3D-графика
fig = go.Figure(data=lines + [points])

fig.update_layout(
    scene=dict(
        xaxis_title="X - Ресурсы",
        yaxis_title="Y - Процессы",
        zaxis_title="Z - Функции управления"
    ),
    title='Модель функциональной структуры управления имуществом',
    width=800, height=800
)

# Отображаем график в Streamlit
st.title('Модель функциональной структуры управления имуществом')
st.plotly_chart(fig)