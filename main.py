import flet as ft

def main(page: ft.Page):
    page.title = "Algoritmos de Reemplazo de Páginas - Simulador"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_height = 900
    page.padding = 30
    
    # Input para cantidad de marcos (Default 3)
    frame_count_input = ft.TextField(
        label="N° Marcos", 
        value="3", 
        width=100, 
        text_align=ft.TextAlign.CENTER,
        border_color="green400"
    )

    # Contenedor para los marcos superiores (se llenará dinámicamente)
    frames_ui_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    
    # Referencias dinámicas
    val_refs = []
    card_refs = []
    
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
        v_ref = ft.Ref[ft.Text]()
        c_ref = ft.Ref[ft.Container]()
        val_refs.append(v_ref)
        card_refs.append(c_ref)
        
        return ft.Container(
            ref=c_ref,
            content=ft.Column([
                ft.Text(f"MARCO {i}", size=10, weight="bold"),
                ft.Text("-", ref=v_ref, size=30, weight="bold"),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=120, height=120, bgcolor="greenGrey900", border_radius=10,
            border=ft.Border.all(2, "greenGrey800"),
            animate=ft.Animation(400, "bounceOut")
        )

    def simulate(algo_type):
            try:
                num_frames = int(frame_count_input.value)
                pages = [int(x.strip()) for x in ref_input.value.split(",") if x.strip()]
                if not pages: return
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Error en los datos de entrada"))
                page.snack_bar.open = True
                page.update()
                return

            # Limpiar y regenerar marcos superiores
            val_refs.clear()
            card_refs.clear()
            frames_ui_row.controls = [create_frame(i) for i in range(num_frames)]
            
            grid_row.controls.clear()
            frames = [None] * num_frames
            bits = [0] * num_frames         
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
                    
                    if algo_type == "Optimal":
                        if None in frames:
                            hit_idx = frames.index(None)
                            frames[hit_idx] = p
                        else:
                            future_pages = pages[i + 1:]
                            farthest_idx = -1
                            victim_idx = -1
                            
                            for f_idx, f_val in enumerate(frames):
                                if f_val not in future_pages:
                                    victim_idx = f_idx
                                    break
                                else:
                                    next_usage = future_pages.index(f_val)
                                    if next_usage > farthest_idx:
                                        farthest_idx = next_usage
                                        victim_idx = f_idx
                            
                            hit_idx = victim_idx
                            frames[hit_idx] = p

                    elif algo_type == "FIFO":
                        hit_idx = ptr
                        frames[ptr] = p
                        ptr = (ptr + 1) % num_frames
                    
                    elif algo_type == "SC":
                        while True:
                            if bits[ptr] == 0:
                                hit_idx = ptr
                                frames[ptr] = p
                                bits[ptr] = 0
                                ptr = (ptr + 1) % num_frames
                                break
                            else:
                                bits[ptr] = 0
                                ptr = (ptr + 1) % num_frames
                    
                    elif algo_type == "LRU":
                        if None in frames:
                            hit_idx = frames.index(None)
                        else:
                            victim = lru_stack.pop(0)
                            hit_idx = frames.index(victim)
                        frames[hit_idx] = p
                        lru_stack.append(p)

                col_items = [
                    ft.Container(
                        content=ft.Text(str(p), weight="bold", color="black"),
                        bgcolor="greenAccent700", width=45, height=45, 
                        alignment=ft.Alignment(0, 0),
                        border=ft.Border.all(1, "black38")
                    )
                ]
                
                for f_idx, f_val in enumerate(frames):
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

            stats_text.value = f"Resultados: {faults} Fallos | {hits} Aciertos | Eficiencia: {(hits/len(pages))*100:.1f}%"
            
            for i in range(num_frames):
                val_refs[i].current.value = str(frames[i]) if frames[i] is not None else "-"
                card_refs[i].current.border = ft.Border.all(3, "amber400" if frames[i] is not None else "greenGrey800")
            
            page.update()

    # Inicializar marcos superiores por defecto
    frames_ui_row.controls = [create_frame(i) for i in range(3)]

    page.add(
        ft.Text("Simulador de reemplazo de páginas", size=32, weight="bold", color="green400"),
        ft.Text("Daniel Alejandro Henao, Laura Sofía Cardona", size=16, weight="normal", color="greenGrey400"),
        ft.Row([
            ref_input, 
            frame_count_input,
            ft.FilledButton("Óptimo", icon="play_arrow", on_click=lambda _: simulate("Optimal")), 
            ft.FilledButton("FIFO", icon="play_arrow", on_click=lambda _: simulate("FIFO")),
            ft.FilledButton("FIFO mejorado", icon="play_arrow", on_click=lambda _: simulate("SC")),
            ft.FilledButton("LRU", icon="play_arrow", on_click=lambda _: simulate("LRU"))
        ]),
        frames_ui_row,
        ft.Divider(height=30, color="transparent"),
        stats_text,
        ft.Text("Matriz de ejecución paso a paso:", size=16, italic=True),
        ft.Container(
            content=grid_row, 
            padding=20, 
            bgcolor="#1a1a1a", 
            border_radius=15, 
            height=350 # Ajustado un poco para marcos dinámicos
        )
    )

if __name__ == "__main__":
    ft.run(main)