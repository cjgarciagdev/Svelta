import flet as ft
from database.db import get_stats
from config.theme import INCES_BLUE, INCES_TEAL

def admin_home_view(page: ft.Page):
    stats = get_stats()
    
    # 1. Tarjeta Total
    tarjeta_total = ft.Container(
        bgcolor=INCES_BLUE, padding=25, border_radius=15,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(0, 5)),
        content=ft.Column([
            ft.Text("Total de Estudiantes Censados", size=16, color=ft.Colors.WHITE70, weight=ft.FontWeight.BOLD),
            ft.Text(str(stats["total"]), size=48, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            ft.Icon(ft.Icons.PEOPLE_ALT, color=ft.Colors.WHITE30, size=50)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    # 2. Gráfico de Género (Barras Visuales Compatibles)
    secciones_genero = [ft.Text("Distribución por Género", size=16, weight=ft.FontWeight.BOLD, color=INCES_BLUE), ft.Divider(height=10, color=ft.Colors.TRANSPARENT)]
    colores_genero = [ft.Colors.BLUE_400, ft.Colors.PINK_400, ft.Colors.PURPLE_400]
    
    for i, (genero, cantidad) in enumerate(stats["generos"]):
        porcentaje = (cantidad / stats["total"]) * 100 if stats["total"] > 0 else 0
        secciones_genero.append(
            ft.Column([
                ft.Row([ft.Text(f"{genero} ({cantidad})", size=14, weight=ft.FontWeight.BOLD), ft.Text(f"{porcentaje:.1f}%", size=14, color=ft.Colors.GREY_600)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.ProgressBar(value=porcentaje/100, color=colores_genero[i % len(colores_genero)], bgcolor=ft.Colors.GREY_200, height=10)
            ])
        )
    
    grafico_genero = ft.Container(
        bgcolor=ft.Colors.WHITE, padding=20, border_radius=15, shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        content=ft.Column(secciones_genero, alignment=ft.MainAxisAlignment.CENTER)
    )

    # 3. Gráfico de Discapacidad (Barras Visuales Compatibles)
    barras_discapacidad = [ft.Text("Condición de Discapacidad", size=16, weight=ft.FontWeight.BOLD, color=INCES_BLUE), ft.Divider(height=10, color=ft.Colors.TRANSPARENT)]
    for i, (posee, cantidad) in enumerate(stats["discapacidades"]):
        etiqueta = "Con Discapacidad" if posee == 1 else "Sin Discapacidad"
        color = ft.Colors.ORANGE_400 if posee == 1 else INCES_TEAL
        porcentaje = (cantidad / stats["total"]) * 100 if stats["total"] > 0 else 0
        barras_discapacidad.append(
            ft.Column([
                ft.Row([ft.Text(f"{etiqueta} ({cantidad})", size=14, weight=ft.FontWeight.BOLD), ft.Text(f"{porcentaje:.1f}%", size=14, color=ft.Colors.GREY_600)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.ProgressBar(value=porcentaje/100, color=color, bgcolor=ft.Colors.GREY_200, height=10)
            ])
        )
        
    grafico_discapacidad = ft.Container(
        bgcolor=ft.Colors.WHITE, padding=20, border_radius=15, shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        content=ft.Column(barras_discapacidad, alignment=ft.MainAxisAlignment.CENTER)
    )

    # 4. Tarjeta de Cursos más Demandados
    lista_cursos = [ft.Text("Cursos con Mayor Demanda", size=16, weight=ft.FontWeight.BOLD, color=INCES_BLUE), ft.Divider(height=10, color=ft.Colors.GREY_300)]
    for curso, cantidad in stats.get("cursos", []):
        lista_cursos.append(
            ft.Row([
                ft.Icon(ft.Icons.MENU_BOOK, size=16, color=INCES_TEAL),
                ft.Text(curso, size=14, weight=ft.FontWeight.W_500, expand=True),
                ft.Container(content=ft.Text(str(cantidad), size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), bgcolor=INCES_BLUE, padding=ft.padding.symmetric(horizontal=8, vertical=4), border_radius=10)
            ])
        )

    tarjeta_cursos = ft.Container(
        bgcolor=ft.Colors.WHITE, padding=20, border_radius=15, shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        content=ft.Column(lista_cursos)
    )

    return ft.Container(
        expand=True, padding=20,
        content=ft.Column([
            ft.Text("Dashboard de Estadísticas", size=28, weight=ft.FontWeight.BOLD, color=INCES_BLUE),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Row([ft.Container(content=tarjeta_total, expand=True)]),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Row([
                ft.Container(content=grafico_genero, expand=True, height=300),
                ft.Container(content=grafico_discapacidad, expand=True, height=300),
                ft.Container(content=tarjeta_cursos, expand=True, height=300)
            ])
        ], scroll=ft.ScrollMode.AUTO)
    )
