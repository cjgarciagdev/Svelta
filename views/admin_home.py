import flet as ft
from database.db import get_stats
from config.theme import INCES_BLUE, INCES_TEAL


# ─── Colores para las barras ───────────────────────────────────────────────────
_COLORES_GENERO   = [ft.Colors.BLUE_400, ft.Colors.PINK_400, ft.Colors.PURPLE_400, ft.Colors.CYAN_400]
_COLORES_DISC     = [ft.Colors.ORANGE_400, INCES_TEAL]
_COLORES_TRIM     = [ft.Colors.INDIGO_400, INCES_TEAL, ft.Colors.CYAN_600, ft.Colors.TEAL_400]
_COLORES_PERFILES = [
    ft.Colors.BLUE_500, ft.Colors.TEAL_500, ft.Colors.CYAN_500, ft.Colors.INDIGO_500,
    ft.Colors.PINK_500, ft.Colors.PURPLE_500, ft.Colors.ORANGE_500, ft.Colors.GREEN_500,
]


# ─── Helper para Gráficos de Barras (ProgressBars) ─────────────────────────────
def _build_bar_chart(titulo: str, total: int, datos: list, paleta_colores: list) -> ft.Container:
    """
    Construye una tarjeta con un título y múltiples barras de progreso.
    datos: lista de tuplas (etiqueta, cantidad)
    """
    elementos = [
        ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD, color=INCES_BLUE),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT)
    ]
    
    if not datos or total == 0:
        elementos.append(ft.Text("Sin datos registrados", color=ft.Colors.GREY_500, italic=True))
    else:
        for i, (etiqueta, cantidad) in enumerate(datos):
            # Calcular porcentaje
            porcentaje = (cantidad / total) * 100 if total > 0 else 0
            color = paleta_colores[i % len(paleta_colores)]
            
            # Limitar longitud de la etiqueta si es muy larga
            etiq_texto = str(etiqueta) if etiqueta else "No especificado"
            if len(etiq_texto) > 30:
                etiq_texto = etiq_texto[:27] + "..."
                
            elementos.append(
                ft.Column([
                    ft.Row(
                        [
                            ft.Text(f"{etiq_texto} ({cantidad})", size=14, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{porcentaje:.1f}%", size=14, color=ft.Colors.GREY_600)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.ProgressBar(
                        value=porcentaje / 100,
                        color=color,
                        bgcolor=ft.Colors.GREY_200,
                        height=10,
                        border_radius=5
                    )
                ], spacing=2)
            )
            elementos.append(ft.Container(height=8)) # Espaciado entre barras
            
    return ft.Container(
        bgcolor=ft.Colors.WHITE,
        padding=20,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)),
        content=ft.Column(elementos, alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.AUTO)
    )


# ─── Vista principal del Dashboard ────────────────────────────────────────────
def admin_home_view(page: ft.Page):
    stats = get_stats()
    total_estudiantes = stats.get("total", 0)

    # ── 1. Tarjeta Total ───────────────────────────────────────────────────────
    tarjeta_total = ft.Container(
        bgcolor=INCES_BLUE,
        padding=ft.padding.Padding(left=30, top=25, right=30, bottom=25),
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.BLACK26, offset=ft.Offset(0, 6)),
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Total de Estudiantes Censados", size=16, color=ft.Colors.WHITE70, weight=ft.FontWeight.BOLD),
                        ft.Text(str(total_estudiantes), size=56, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    ],
                    expand=True,
                    spacing=2,
                ),
                ft.Icon(ft.Icons.PEOPLE_ALT, color=ft.Colors.WHITE24, size=90),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # ── 2. Datos Procesados ────────────────────────────────────────────────────
    
    # Géneros (Forzamos a solo Masculino y Femenino, interpretando la data)
    datos_genero_raw = stats.get("generos", [])
    m_count = 0
    f_count = 0
    for g, c in datos_genero_raw:
        g_str = str(g).strip().lower() if g else ""
        
        # Filtros precisos para español
        if "mujer" in g_str or "femenino" in g_str or g_str == "f":
            f_count += c
        elif "hombre" in g_str or "masculino" in g_str or g_str == "m":
            m_count += c
            
    datos_genero = [("Masculino", m_count), ("Femenino", f_count)]
    
    # Discapacidad
    datos_disc = []
    for posee, cantidad in stats.get("discapacidades", []):
        etiqueta = "Con Discapacidad" if posee == 1 else "Sin Discapacidad"
        datos_disc.append((etiqueta, cantidad))
        
    # Trimestres (Forzamos a que siempre existan los 4)
    datos_trim_raw = dict(stats.get("trimestres", []))
    datos_trimestres = [
        ("1er Trimestre", datos_trim_raw.get("1er Trimestre", 0)),
        ("2do Trimestre", datos_trim_raw.get("2do Trimestre", 0)),
        ("3er Trimestre", datos_trim_raw.get("3er Trimestre", 0)),
        ("4to Trimestre", datos_trim_raw.get("4to Trimestre", 0)),
    ]
    
    # Perfiles Totales
    datos_perfiles = [(p, c) for p, c in stats.get("perfiles_todos", []) if c > 0]

    # ── 3. Construir Gráficos ──────────────────────────────────────────────────
    grafico_genero = _build_bar_chart("Distribución por Género", total_estudiantes, datos_genero, _COLORES_GENERO)
    grafico_disc = _build_bar_chart("Condición de Discapacidad", total_estudiantes, datos_disc, _COLORES_DISC)
    grafico_trim = _build_bar_chart("Censados por Trimestre", total_estudiantes, datos_trimestres, _COLORES_TRIM)
    grafico_perfiles = _build_bar_chart("Perfiles Totales Censados", total_estudiantes, datos_perfiles, _COLORES_PERFILES)

    # ── 4. Tarjeta de Perfiles más Demandados (junto a los gráficos)
    lista_perfiles = [ft.Text("Perfiles con Mayor Demanda", size=16, weight=ft.FontWeight.BOLD, color=INCES_BLUE), ft.Divider(height=10, color=ft.Colors.GREY_300)]
    for perfil, cantidad in stats.get("perfiles", []):
        lista_perfiles.append(
            ft.Row([
                ft.Icon(ft.Icons.MENU_BOOK, size=16, color=INCES_TEAL),
                ft.Text(perfil, size=14, weight=ft.FontWeight.W_500, expand=True),
                ft.Container(content=ft.Text(str(cantidad), size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), bgcolor=INCES_BLUE, padding=ft.Padding.symmetric(horizontal=8, vertical=4), border_radius=10)
            ])
        )

    tarjeta_perfiles = ft.Container(
        bgcolor=ft.Colors.WHITE, padding=20, border_radius=15, shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        content=ft.Column(lista_perfiles)
    )

    # ── 5. Layout Final ────────────────────────────────────────────────────────
    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            [
                ft.Text("Dashboard de Estadísticas", size=28, weight=ft.FontWeight.BOLD, color=INCES_BLUE),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),

                # Fila 1 — Total de censados
                ft.Row([ft.Container(content=tarjeta_total, expand=True)]),
                ft.Divider(height=15, color=ft.Colors.TRANSPARENT),

                # Fila 2 — Género, Discapacidad y Trimestres (3 columnas)
                ft.Row(
                    [
                        ft.Container(content=grafico_genero, expand=True, height=260),
                        ft.Container(content=grafico_disc, expand=True, height=260),
                        ft.Container(content=grafico_trim, expand=True, height=260),
                    ],
                    spacing=15,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Divider(height=15, color=ft.Colors.TRANSPARENT),

                # Fila 3 — Perfiles totales (ocupa todo el ancho, altura automática)
                ft.Row(
                    [ft.Container(content=grafico_perfiles, expand=True, height=350)],
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
        ),
    )
