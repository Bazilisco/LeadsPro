import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from extractor.browser import iniciar_navegador
from extractor.manager import executar_extracao_em_massa
from extractor.exporter import exportar_csv, exportar_excel, exportar_json  # ← sem PDF
import threading
from PIL import Image, ImageTk  # Requer Pillow instalado
import time  # NOVO

class ApplicationGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LEADSPRO")
        self.geometry("1000x600")
        self.configure(bg="#1e1e1e")
        self.navegador = None
        self.extracao_ativa = False
        self.total_estabelecimentos = 0

        # NOVO - métricas HUD
        self._items_ok = tk.IntVar(value=0)
        self._items_err = tk.IntVar(value=0)
        self._start_ts = None
        self._elapsed_var = tk.StringVar(value="00:00")
        self._rate_var = tk.StringVar(value="0,0/min")

        self.style = ttk.Style(self)
        self._configurar_tema_escuro()

        self.create_widgets()
        self._iniciar_timer_hud()  # NOVO
        self._configurar_atalhos()  # NOVO
        self.show_terms_dialog()

    def _configurar_tema_escuro(self):
        self.style.theme_use("default")
        self.style.configure("TFrame", background="#1e1e1e")
        self.style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
        self.style.configure("TButton", background="#3c3c3c", foreground="#ffffff", padding=(10, 6))  # NOVO padding
        self.style.map("TButton", background=[("active", "#505050")])
        self.style.configure("Treeview", background="#2e2e2e", fieldbackground="#2e2e2e", foreground="#ffffff", rowheight=24)  # NOVO rowheight
        self.style.configure("Treeview.Heading", background="#3c3c3c", foreground="#ffffff")
        self.style.configure("TNotebook", background="#1e1e1e")
        self.style.configure("TNotebook.Tab", background="#2e2e2e", foreground="#ffffff")
        self.style.map("TNotebook.Tab", background=[("selected", "#3c3c3c")], foreground=[("selected", "#ffffff")])
        self.style.configure("Horizontal.TProgressbar", troughcolor="#3c3c3c", background="#0078D7", bordercolor="#1e1e1e")

    def show_terms_dialog(self):
        termo = (
            "TERMO DE RESPONSABILIDADE\n\n"
            "Esta aplicação extrai dados públicos do Google Maps para fins informativos.\n"
            "Ao utilizar este software, você declara estar ciente e de acordo com os seguintes pontos:\n\n"
            "1. Respeitar os Termos de Serviço do Google;\n"
            "2. Utilizar os dados exclusivamente para fins pessoais ou internos da sua empresa;\n"
            "3. Não distribuir, vender ou compartilhar os dados coletados;\n"
            "4. Assumir total responsabilidade pelo uso das informações extraídas.\n\n"
            "O desenvolvedor não se responsabiliza por qualquer uso indevido desta ferramenta."
        )
        resultado = messagebox.askokcancel("Termos de Uso", termo)
        if not resultado:
            self.destroy()

    def create_widgets(self):
        # Cabeçalho com logo e título lado a lado
        header = ttk.Frame(self)
        header.pack(pady=(15, 5))

        try:
            logo_img = Image.open("assets/logo.png")
            logo_img = logo_img.resize((35, 35), Image.ANTIALIAS)
            self.logo_tk = ImageTk.PhotoImage(logo_img)
            self.logo_label = tk.Label(header, image=self.logo_tk, bg="#1e1e1e")
            self.logo_label.pack(side=tk.LEFT, padx=(0, 10))
        except Exception as e:
            print(f"[ERRO] Logo não carregada: {e}")

        titulo = ttk.Label(header, text="LEADSPRO", font=("Helvetica", 20, "bold"))
        titulo.pack(side=tk.LEFT)

        # Botões principais
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=(10, 5))

        self.btn_start_browser = ttk.Button(btn_frame, text="Iniciar Navegador", command=self.abrir_navegador)
        self.btn_start_browser.grid(row=0, column=0, padx=5)

        self.btn_start_extract = ttk.Button(btn_frame, text="Iniciar Extração", command=self.iniciar_extracao)
        self.btn_start_extract.grid(row=0, column=1, padx=5)

        self.btn_stop_extract = ttk.Button(btn_frame, text="Parar Extração", command=self.parar_extracao)
        self.btn_stop_extract.grid(row=0, column=2, padx=5)

        # Barra de progresso
        self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate", length=500)
        self.progress.pack(pady=(5, 10))

        # Abas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.result_frame = ttk.Frame(self.notebook)
        self.log_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.result_frame, text="Resultados")
        self.notebook.add(self.log_frame, text="Logs")

        # Tabela de Resultados
        columns = ("Nome", "Endereço", "Telefone", "Site", "Email")
        self.columns = columns  # NOVO - referência para copiar/ordenar
        self.tree = ttk.Treeview(self.result_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self._sort_by(c, False))  # NOVO - ordenar
            self.tree.column(col, width=200, stretch=False)  # NOVO - evita "pula-pula"
        self.tree.pack(expand=True, fill='both')

        # Área de logs
        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, bg="#2e2e2e", fg="#ffffff", insertbackground="white")
        self.log_text.pack(expand=True, fill='both')

        # Rodapé com botões de exportação
        footer = ttk.Frame(self)
        footer.pack(pady=10)

        self.btn_export_csv = ttk.Button(footer, text="Exportar CSV", command=lambda: exportar_csv(self.tree))
        self.btn_export_xlsx = ttk.Button(footer, text="Exportar Excel", command=lambda: exportar_excel(self.tree))
        self.btn_export_json = ttk.Button(footer, text="Exportar JSON", command=lambda: exportar_json(self.tree))

        self.btn_export_csv.grid(row=0, column=0, padx=5)
        self.btn_export_xlsx.grid(row=0, column=1, padx=5)
        self.btn_export_json.grid(row=0, column=2, padx=5)

        # NOVO - export só habilita quando tem dado
        for b in (self.btn_export_csv, self.btn_export_xlsx, self.btn_export_json):  # ← sem PDF
            b.configure(state="disabled")

        # NOVO - HUD / Status Bar
        hud = ttk.Frame(self)
        hud.pack(fill="x", side="bottom", padx=8, pady=(0, 6))

        ttk.Label(hud, text="Coletados:").pack(side="left")
        ttk.Label(hud, textvariable=self._items_ok).pack(side="left", padx=(2, 10))

        ttk.Label(hud, text="Erros:").pack(side="left")
        ttk.Label(hud, textvariable=self._items_err, foreground="#ffb4ab").pack(side="left", padx=(2, 10))

        ttk.Label(hud, text="Tempo:").pack(side="left")
        ttk.Label(hud, textvariable=self._elapsed_var).pack(side="left", padx=(2, 10))

        ttk.Label(hud, text="Velocidade:").pack(side="left")
        ttk.Label(hud, textvariable=self._rate_var).pack(side="left", padx=(2, 10))

    # NOVO - timer HUD
    def _iniciar_timer_hud(self):
        def _tick():
            if self._start_ts is not None:
                sec = int(time.time() - self._start_ts)
                mm, ss = divmod(sec, 60)
                self._elapsed_var.set(f"{mm:02d}:{ss:02d}")
                ok = self._items_ok.get()
                if sec > 0:
                    rate = (ok / sec) * 60.0
                    self._rate_var.set(f"{rate:.1f}/min")
            self.after(1000, _tick)
        self.after(1000, _tick)

    # NOVO - atalhos de teclado
    def _configurar_atalhos(self):
        self.bind("<Control-i>", lambda e: self.abrir_navegador())
        self.bind("<Control-e>", lambda e: self.iniciar_extracao())
        self.bind("<Control-s>", lambda e: self._exportar_atalho())
        self.bind("<Control-c>", lambda e: self.copy_selected_to_clipboard())

    def _exportar_atalho(self):
        # prioridade CSV no atalho
        if self.btn_export_csv["state"] == "normal":
            exportar_csv(self.tree)

    def abrir_navegador(self):
        self._append_log("[INFO] Iniciando navegador...\n")
        self.navegador = iniciar_navegador()
        if self.navegador:
            self._append_log("[OK] Navegador aberto com sucesso!\n")
        else:
            self._append_log("[ERRO] Falha ao iniciar o navegador.\n")

    def iniciar_extracao(self):
        if not self.navegador:
            messagebox.showwarning("Atenção", "Você precisa iniciar o navegador primeiro.")
            return

        # reset visual + métricas
        self.extracao_ativa = True
        self._items_ok.set(0)
        self._items_err.set(0)
        self._start_ts = time.time()

        self.tree.delete(*self.tree.get_children())
        self.progress['value'] = 0
        self._append_log("[INFO] Iniciando extração em nova thread...\n")
        thread = threading.Thread(target=self.executar_extracao, daemon=True)
        thread.start()

    def parar_extracao(self):
        self.extracao_ativa = False
        self._append_log("[INFO] Extração será interrompida.\n")

    def executar_extracao(self):
        estabelecimentos = []

        # callbacks thread-safe: atualizam GUI via .after
        def callback_resultado(dados):
            if not self.extracao_ativa:
                return
            def _ui():
                self.tree.insert("", "end", values=(
                    dados.get("nome", ""),
                    dados.get("endereco", ""),
                    dados.get("telefone", ""),
                    dados.get("site", ""),
                    dados.get("email", "")
                ))
                self._items_ok.set(self._items_ok.get() + 1)  # HUD
                self._apply_zebra()
                # habilita export (sem PDF)
                for b in (self.btn_export_csv, self.btn_export_xlsx, self.btn_export_json):
                    if str(b["state"]) != "normal":
                        b.configure(state="normal")
            self.after(0, _ui)

        def callback_log(texto):
            def _ui():
                self._append_log(texto)
                # Atualiza progresso com base na etapa "Visitando:"
                if texto.startswith("Visitando:") and self.total_estabelecimentos > 0:
                    partes = texto.split("(")
                    if len(partes) > 1 and "/" in partes[1]:
                        progresso = partes[1].split(")")[0]
                        atual, total = progresso.split("/")
                        try:
                            atual_i = int(atual.strip())
                            total_i = int(total.strip())
                            if total_i > 0:
                                self.progress['value'] = (atual_i / total_i) * 100
                        except Exception:
                            pass
                # erro?
                if texto.lower().startswith("[erro]"):
                    self._items_err.set(self._items_err.get() + 1)
            self.after(0, _ui)

        def extraindo():
            executar_extracao_em_massa(
                navegador=self.navegador,
                atualizar_resultado_callback=callback_resultado,
                atualizar_log_callback=callback_log
            )
            # fim
            def _ui_end():
                self.progress['value'] = 100
                self.extracao_ativa = False
                self._start_ts = None  # congela cronômetro
                self._append_log("[OK] Extração finalizada.\n")
            self.after(0, _ui_end)

        # Antes de extrair, contamos os estabelecimentos
        from extractor.scraper import rolar_resultados, coletar_estabelecimentos
        callback_log("[INFO] Carregando estabelecimentos...\n")
        try:
            rolar_resultados(self.navegador, callback_log)
            estabelecimentos.extend(coletar_estabelecimentos(self.navegador))
        except Exception as e:
            callback_log(f"[ERRO] Falha ao carregar estabelecimentos: {e}\n")
        self.total_estabelecimentos = len(estabelecimentos)
        if self.total_estabelecimentos > 0:
            self.after(0, lambda: self._append_log(f"[OK] {self.total_estabelecimentos} estabelecimentos listados.\n"))
        else:
            self.after(0, lambda: self._append_log("[ALERTA] Nenhum estabelecimento listado. Faça a busca no Maps e tente novamente.\n"))

        extraindo()

    def _append_log(self, texto: str):
        self.log_text.insert(tk.END, texto)
        self.log_text.see(tk.END)

    # NOVO - zebra striping e ordenação
    def _apply_zebra(self):
        for idx, iid in enumerate(self.tree.get_children()):
            self.tree.item(iid, tags=("odd" if idx % 2 else "even",))
        self.tree.tag_configure("odd", background="#2a2a2a")
        self.tree.tag_configure("even", background="#2e2e2e")

    def _sort_by(self, col, descending):
        # coleta
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        # número ou string
        def _key(v):
            try:
                return float(str(v[0]).replace(",", "."))
            except:
                return str(v[0]).lower()
        data.sort(key=_key, reverse=descending)
        for index, (_, k) in enumerate(data):
            self.tree.move(k, "", index)
        # alterna sentido no próximo clique
        self.tree.heading(col, command=lambda c=col: self._sort_by(c, not descending))
        self._apply_zebra()

    # NOVO - copiar seleção para a área de transferência
    def copy_selected_to_clipboard(self):
        items = self.tree.selection()
        if not items:
            return
        cols = self.columns
        lines = [";".join(cols)]
        for iid in items:
            values = [str(self.tree.set(iid, c)) for c in cols]
            lines.append(";".join(values))
        text = "\n".join(lines)
        self.clipboard_clear()
        self.clipboard_append(text)
        self._append_log("[OK] Linhas copiadas para a área de transferência (CSV com ;).\n")

    def on_closing(self):
        if self.extracao_ativa:
            if not messagebox.askyesno("Fechar", "Uma extração está em andamento. Deseja realmente sair?"):
                return
        if self.navegador:
            try:
                self.navegador.quit()
            except Exception:
                pass
        self.destroy()

# Execução direta
if __name__ == "__main__":
    app = ApplicationGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
