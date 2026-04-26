import flet as ft

def main(page: ft.Page):
    page.title = "Algoritmos de Reemplazo de Páginas - Simulador"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_height = 900
    page.padding = 30
    
    # Referencias de la interfaz
    val_refs = [ft.Ref[ft.Text]() for _ in range(3)]
    card_refs = [ft.Ref[ft.Container]() for _ in range(3)]
    
    ref_input = ft.TextField(
        label="Secuencia de referencia", 
        hint_text="ej: 1, 3, 0, 3, 5, 6",
        expand=True, 
        border_color="green400"
    )

    grid_row = ft.Row(
        spacing=2, 
        vertical_alignment=ft.CrossAxisAlignment.START,
        scroll=ft.ScrollMode.ALWAYS,
    )
    
    stats_text = ft.Text("Fallos: 0 | Aciertos: 0", size=22, weight="bold", color="amber400")

    def create_frame(i):
        return ft.Container(
            ref=card_refs[i],
            content=ft.Column([
                ft.Text(f"MARCO {i}", size=10, weight="bold"),
                ft.Text("-", ref=val_refs[i], size=30, weight="bold"),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=120, height=120, bgcolor="greenGrey900", border_radius=10,
            border=ft.Border.all(2, "greenGrey800"),
            animate=ft.Animation(400, "bounceOut")
        )

    def simulate(algo_type):
            try:
                pages = [int(x.strip()) for x in ref_input.value.split(",") if x.strip()]
                if not pages: return
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Error sintáctico"))
                page.snack_bar.open = True
                page.update()
                return

            grid_row.controls.clear()
            frames = [None] * 3
            bits = [0] * 3         
            lru_stack = []         
            faults = 0
            hits = 0
            ptr = 0                

            for i, p in enumerate(pages):
                is_hit = False
                hit_idx = -1
                
                if p in frames:
                    is_hit = True
                    hit_idx = frames.index(p)
                    hits += 1
                    if algo_type == "SC": bits[hit_idx] = 1
                    elif algo_type == "LRU":
                        lru_stack.remove(p)
                        lru_stack.append(p)
                else:
                    faults += 1
                    
                    # La lógica del óptimo
                    if algo_type == "Optimal":
                        if None in frames:
                            hit_idx = frames.index(None)
                            frames[hit_idx] = p
                        else:
                            # Determinar las páginas futuras
                            future_pages = pages[i + 1:]
                            farthest_idx = -1
                            victim_idx = -1
                            
                            for f_idx, f_val in enumerate(frames):
                                if f_val not in future_pages:
                                    # pues la victima es la que no se va a usar mas
                                    victim_idx = f_idx
                                    break
                                else:
                                    # si se usa, se mira que tan lejos esta su proximo uso
                                    next_usage = future_pages.index(f_val)
                                    if next_usage > farthest_idx:
                                        farthest_idx = next_usage
                                        victim_idx = f_idx
                            
                            hit_idx = victim_idx
                            frames[hit_idx] = p

                    elif algo_type == "FIFO":
                        hit_idx = ptr
                        frames[ptr] = p
                        ptr = (ptr + 1) % 3
                    
                    elif algo_type == "SC":
                        while True:
                            if bits[ptr] == 0:
                                hit_idx = ptr
                                frames[ptr] = p
                                bits[ptr] = 0
                                ptr = (ptr + 1) % 3
                                break
                            else:
                                bits[ptr] = 0
                                ptr = (ptr + 1) % 3
                    
                    elif algo_type == "LRU":
                        if None in frames:
                            hit_idx = frames.index(None)
                        else:
                            victim = lru_stack.pop(0)
                            hit_idx = frames.index(victim)
                        frames[hit_idx] = p
                        lru_stack.append(p)

                # Construccion de la matriz
                # cabezera de pagina
                col_items = [
                    ft.Container(
                        content=ft.Text(str(p), weight="bold", color="black"),
                        bgcolor="greenAccent700", width=45, height=45, 
                        alignment=ft.Alignment(0, 0),
                        border=ft.Border.all(1, "black38")
                    )
                ]
                
                # columnas de estado
                for f_idx, f_val in enumerate(frames):
                    # Mostrar amarillo los frames que acaban de ser reemplazados solo si es un fallo
                    is_replacement_target = (not is_hit and f_idx == hit_idx)
                    
                    col_items.append(
                        ft.Container(
                            content=ft.Text(str(f_val) if f_val is not None else "", color="black", weight="bold"),
                            bgcolor="amber" if is_replacement_target else "greenAccent400",
                            width=45, height=45, 
                            alignment=ft.Alignment(0, 0),
                            border=ft.Border.all(1, "black38")
                        )
                    )
                
                grid_row.controls.append(ft.Column(col_items, spacing=0))

            # actualizar estadísticas al final
            stats_text.value = f"Resultados: {faults} Fallos | {hits} Aciertos | Eficiencia: {(hits/len(pages))*100:.1f}%"
            
            # Actualizar los marcos de arriba
            for i in range(3):
                val_refs[i].current.value = str(frames[i]) if frames[i] is not None else "-"
                
                card_refs[i].current.border = ft.Border.all(3, "amber400" if frames[i] is not None else "greenGrey800")
            
            page.update()
    page.add(
        ft.Text("Simulador de reemplazo de páginas", size=32, weight="bold", color="green400"),
        ft.Text("Daniel Alejandro Henao, Laura Sofía Cardona", size=16, weight="normal", color="greenGrey400"),
        ft.Row([
            ref_input, 
            ft.FilledButton("Óptimo", icon="play_arrow", on_click=lambda _: simulate("Optimal")), 
            ft.FilledButton("FIFO mejorado", icon="play_arrow", on_click=lambda _: simulate("SC")),
            ft.FilledButton("LRU", icon="play_arrow", on_click=lambda _: simulate("LRU"))
        ]),
        ft.Row([create_frame(i) for i in range(3)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=30, color="transparent"),
        stats_text,
        ft.Text("Matriz de ejecución paso a paso:", size=16, italic=True),
        ft.Container(
            content=grid_row, 
            padding=20, 
            bgcolor="#1a1a1a", 
            border_radius=15, 
            height=300
        )
    )

if __name__ == "__main__":
    ft.run(main)