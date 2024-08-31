import tkinter as tk
from tkinter import Canvas, Entry, Label, messagebox, StringVar, OptionMenu, Button, Frame, Scrollbar, Text
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector
import requests
from datetime import datetime
from tkintermapview import TkinterMapView
import logging
import re
import webbrowser

# Configuração do logger para rastreamento e depuração
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

"""classe é responsável por todas as operações de banco de dados """
class Database: 
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        """Estabelece a conexão com o banco de dados MySQL  ."""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='admin',
                database='agroforecast_db'
            )
            if connection.is_connected():
                logging.info("Conexão ao MySQL bem-sucedida.")
                return connection
        except mysql.connector.Error as e:
            logging.error(f"Erro ao conectar ao MySQL: {e}")
            messagebox.showerror("Erro", f"Não foi possível conectar ao banco de dados: {e}")
            return None

    def insert_day_forecast(self, cidade, data, descricao, temperatura, temp_max, temp_min, sensacao_termica, precipitacao, umidade, qualidade_ar, co, no, no2, o3, so2, pm2_5, pm10, nh3, indice_uv, velocidade_vento, visibilidade, nebulosidade, nascer_sol, por_sol):
        """Insere uma previsão do dia na tabela previsao_dia."""
        try:
            cursor = self.connection.cursor()
            insert_query = """INSERT INTO previsao_dia (cidade, data, descricao, temperatura, temp_max, temp_min, sensacao_termica, precipitacao, umidade, qualidade_ar, co, no, no2, o3, so2, pm2_5, pm10, nh3, indice_uv, velocidade_vento, visibilidade, nebulosidade, nascer_sol, por_sol) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (cidade, data, descricao, temperatura, temp_max, temp_min, sensacao_termica, precipitacao, umidade, qualidade_ar, co, no, no2, o3, so2, pm2_5, pm10, nh3, indice_uv, velocidade_vento, visibilidade, nebulosidade, nascer_sol, por_sol))
            self.connection.commit()
            logging.info("Previsão do dia inserida com sucesso.")
        except mysql.connector.Error as e:
            logging.error(f"Erro ao inserir previsão do dia: {e}")
            messagebox.showerror("Erro", f"Não foi possível inserir a previsão do dia: {e}")

    def insert_hourly_forecast(self, cidade, data_hora, temperatura, sensacao_termica, temp_min, temp_max, pressao, umidade, descricao, nuvens, velocidade_vento, direcao_vento, chuva, visibilidade):
        """Insere uma previsão futura na tabela previsoes_futuras."""
        try:
            cursor = self.connection.cursor()
            insert_query = """INSERT INTO previsoes_futuras (cidade, data_hora, temperatura, sensacao_termica, temp_min, temp_max, pressao, umidade, descricao, nuvens, velocidade_vento, direcao_vento, chuva, visibilidade) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (cidade, data_hora, temperatura, sensacao_termica, temp_min, temp_max, pressao, umidade, descricao, nuvens, velocidade_vento, direcao_vento, chuva, visibilidade))
            self.connection.commit()
            logging.info("Previsão futura inserida com sucesso.")
        except mysql.connector.Error as e:
            logging.error(f"Erro ao inserir previsão futura: {e}")
            messagebox.showerror("Erro", f"Não foi possível inserir a previsão futura: {e}")

    def insert_user(self, nome_completo, email, senha, genero, data_nascimento, celular, nacionalidade, cultura_agricola):
        """Insere um novo usuário na tabela usuarios."""
        try:
            cursor = self.connection.cursor()
            insert_query = """INSERT INTO usuarios (nome_completo, email, senha, genero, data_nascimento, celular, nacionalidade, cultura_agricola) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (nome_completo, email, senha, genero, data_nascimento, celular, nacionalidade, cultura_agricola))
            self.connection.commit()
            logging.info("Usuário inserido com sucesso.")
        except mysql.connector.Error as e:
            logging.error(f"Erro ao inserir usuário: {e}")
            messagebox.showerror("Erro", f"Não foi possível cadastrar o usuário: {e}")

    def authenticate_user(self, email, senha):
        """Autentica o usuário baseado no email e senha."""
        try:
            cursor = self.connection.cursor()
            select_query = """SELECT * FROM usuarios WHERE email=%s AND senha=%s"""
            cursor.execute(select_query, (email, senha))
            result = cursor.fetchone()
            return result is not None
        except mysql.connector.Error as e:
            logging.error(f"Erro ao autenticar usuário: {e}")
            return False

    def fetch_day_forecast(self):
        """Busca todas as previsões do dia no banco de dados."""
        try:
            cursor = self.connection.cursor()
            select_query = """SELECT * FROM previsao_dia"""
            cursor.execute(select_query)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            logging.error(f"Erro ao buscar previsões do dia: {e}")
            messagebox.showerror("Erro", "Não foi possível buscar as previsões do dia.")
            return []

    def fetch_hourly_forecast(self):
        """Busca todas as previsões futuras no banco de dados."""
        try:
            cursor = self.connection.cursor()
            select_query = """SELECT * FROM previsoes_futuras"""
            cursor.execute(select_query)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            logging.error(f"Erro ao buscar previsões futuras: {e}")
            messagebox.showerror("Erro", "Não foi possível buscar as previsões futuras.")
            return []

    def delete_day_forecast(self, forecast_id):
        """Deleta uma previsão do dia baseada no ID."""
        try:
            cursor = self.connection.cursor()
            delete_query = """DELETE FROM previsao_dia WHERE id = %s"""
            cursor.execute(delete_query, (forecast_id,))
            self.connection.commit()
            logging.info("Previsão do dia deletada com sucesso.")
        except mysql.connector.Error as e:
            logging.error(f"Erro ao deletar previsão do dia: {e}")
            messagebox.showerror("Erro", f"Não foi possível deletar a previsão do dia: {e}")

    def delete_hourly_forecast(self, forecast_id):
        """Deleta uma previsão futura baseada no ID."""
        try:
            cursor = self.connection.cursor()
            delete_query = """DELETE FROM previsoes_futuras WHERE id = %s"""
            cursor.execute(delete_query, (forecast_id,))
            self.connection.commit()
            logging.info("Previsão futura deletada com sucesso.")
        except mysql.connector.Error as e:
            logging.error(f"Erro ao deletar previsão futura: {e}")
            messagebox.showerror("Erro", f"Não foi possível deletar a previsão futura: {e}")

    def fetch_user_profile(self, email):
        """Busca os dados do perfil do usuário baseado no email."""
        try:
            cursor = self.connection.cursor()
            select_query = """SELECT nome_completo, email, senha, genero, data_nascimento, celular, nacionalidade, cultura_agricola FROM usuarios WHERE email=%s"""
            cursor.execute(select_query, (email,))
            return cursor.fetchone()
        except mysql.connector.Error as e:
            logging.error(f"Erro ao buscar dados do perfil: {e}")
            return None

'''classe é responsável pela interface gráfica e lógica de interação do usuário'''
class AgroforecastApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()  # Instancia a classe Database
        self.root.title("Agroforecast Login")
        self.root.geometry("350x600")

        self.canvas = Canvas(self.root, width=350, height=600)
        self.canvas.pack()

        self.create_gradient('#0000FF', '#00FF00')  # Cria um fundo com gradiente de cor
        self.load_logo()  # Carrega o logo da aplicação
        self.create_entries()  # Cria campos de entrada para email e senha
        self.create_buttons()  # Cria botões de login e redes sociais
        self.create_links()  # Cria links para recuperação de senha e cadastro

        self.dark_mode = False  # Inicializa o modo escuro como desativado
        self.day_forecast_window = None  # Inicializa a referência da janela de previsão do dia
        self.hourly_forecast_window = None  # Inicializa a referência da janela de previsão futura

    def create_gradient(self, color1, color2):
        """Cria um fundo com gradiente de cor."""
        width, height = 350, 600
        image = tk.PhotoImage(width=width, height=height)
        self.canvas.create_image(0, 0, image=image, anchor='nw')

        # Calcula a diferença entre as cores
        r1, g1, b1 = [x >> 8 for x in self.canvas.winfo_rgb(color1)]
        r2, g2, b2 = [x >> 8 for x in self.canvas.winfo_rgb(color2)]
        r_ratio = float(r2 - r1) / height
        g_ratio = float(g2 - g1) / height
        b_ratio = float(b2 - b1) / height

        # Cria o gradiente linha por linha
        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f'#{nr:02x}{ng:02x}{nb:02x}'
            image.put(color, to=(0, i, width, i + 1))

        self.gradient_image = image

    def load_logo(self):
        """Carrega e exibe o logo da aplicação."""
        try:
            original_logo = tk.PhotoImage(file="logo.png")
            scaled_logo = original_logo.subsample(2, 2)
            self.canvas.create_image(175, 100, image=scaled_logo, anchor='center')
            self.logo_image = scaled_logo
        except Exception as e:
            logging.error(f"Erro ao carregar o logo: {e}")
            messagebox.showerror("Erro", "Erro ao carregar o logo.")

    def create_entries(self):
        """Cria os campos de entrada para email e senha."""
        self.email_entry = Entry(self.root, width=30, font=('Arial', 12))
        self.email_entry.insert(0, 'Email')
        self.email_entry.bind("<FocusIn>", lambda event: self.clear_entry(event, self.email_entry, 'Email'))
        self.email_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.email_entry, 'Email'))
        self.canvas.create_window(175, 260, window=self.email_entry)

        self.password_entry = Entry(self.root, show='', width=30, font=('Arial', 12))
        self.password_entry.insert(0, 'Senha')
        self.password_entry.bind("<FocusIn>", lambda event: self.clear_entry(event, self.password_entry, 'Senha'))
        self.password_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.password_entry, 'Senha'))
        self.canvas.create_window(175, 310, window=self.password_entry)

    def create_buttons(self):
        """Cria os botões para login e login via redes sociais."""
        self.create_rounded_button(x=115, y=330, width=120, height=40, radius=20, text="ENTRAR", command=self.login)
        self.create_rounded_button(x=50, y=440, width=120, height=40, radius=20, text="FACEBOOK", command=lambda: webbrowser.open("https://www.facebook.com"), fill_color="#3b5998")
        self.create_rounded_button(x=190, y=440, width=120, height=40, radius=20, text="X", command=lambda: webbrowser.open("https://www.x.com"), fill_color="#000000")

    def create_links(self):
        """Cria links para recuperação de senha e cadastro."""
        forgot_password = Label(self.root, text="Esqueceu a senha?", fg="black", cursor="hand2")
        self.canvas.create_window(175, 390, window=forgot_password)

        signup_text = Label(self.root, text="Não tem conta? Inscrever-se", fg="blue", cursor="hand2")
        signup_text.bind("<Button-1>", self.show_signup)
        self.canvas.create_window(175, 500, window=signup_text)

    def create_rounded_button(self, x, y, width, height, radius, text, command, fill_color="#008000", text_color="white"):
        """Cria um botão arredondado."""
        def on_click(event):
            command()

        self.canvas.create_arc(x, y, x + 2 * radius, y + 2 * radius, start=90, extent=180, fill=fill_color, outline=fill_color)
        self.canvas.create_arc(x + width - 2 * radius, y, x + width, y + 2 * radius, start=0, extent=90, fill=fill_color, outline=fill_color)
        self.canvas.create_arc(x, y + height - 2 * radius, x + 2 * radius, y + height, start=180, extent=90, fill=fill_color, outline=fill_color)
        self.canvas.create_arc(x + width - 2 * radius, y + height - 2 * radius, x + width, y + height, start=270, extent=90, fill=fill_color, outline=fill_color)
        self.canvas.create_rectangle(x + radius, y, x + width - radius, y + height, fill=fill_color, outline=fill_color)
        self.canvas.create_rectangle(x, y + radius, x + width, y + height - radius, fill=fill_color, outline=fill_color)
        self.canvas.create_text(x + width / 2, y + height / 2, text=text, fill=text_color, font=('Arial', 12), anchor='center')

        button_id = self.canvas.create_rectangle(x, y, x + width, y + height, outline='', fill='', tags=("button",))
        self.canvas.tag_bind(button_id, "<ButtonPress-1>", on_click)

    def clear_entry(self, event, entry, default_text):
        """Limpa o texto de entrada padrão quando o campo recebe foco."""
        if entry.get() == default_text:
            entry.delete(0, tk.END)
            if entry == self.password_entry:
                entry.config(show='*')

    def add_placeholder(self, event, entry, default_text):
        """Adiciona texto de entrada padrão quando o campo perde foco."""
        if entry.get() == '':
            entry.insert(0, default_text)
            if entry == self.password_entry:
                entry.config(show='')

    def validate_email(self, email):
        """Valida o formato do email."""
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return re.match(email_regex, email) is not None

    def login(self):
        """Realiza o login do usuário e exibe as abas de previsão do tempo."""
        email = self.email_entry.get()
        senha = self.password_entry.get()

        if email == '' or email == 'Email':
            messagebox.showerror("Erro", "Por favor, insira o email.")
            logging.warning("Tentativa de login sem email.")
        elif senha == '' or senha == 'Senha':
            messagebox.showerror("Erro", "Por favor, insira a senha.")
            logging.warning("Tentativa de login sem senha.")
        elif not self.validate_email(email):
            messagebox.showerror("Erro", "Por favor, insira um email válido.")
            logging.warning(f"Tentativa de login com email inválido: {email}")
        else:
            logging.info(f"Tentativa de login com Email: {email}")
            # Autentica o usuário no banco de dados
            if self.db.authenticate_user(email, senha):
                messagebox.showinfo("Sucesso", "Login bem-sucedido!")
                self.user_email = email  # Armazena o email do usuário logado
                self.show_forecast_tabs()
            else:
                messagebox.showerror("Erro", "Email ou senha incorretos.")
                logging.warning("Tentativa de login com email ou senha incorretos.")

    def show_forecast_tabs(self):
        """Exibe as abas de previsão do tempo após o login."""
        self.canvas.pack_forget()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')

        self.location_frame = ttk.Frame(self.notebook)
        self.day_forecast_frame = ttk.Frame(self.notebook)
        self.hourly_forecast_frame = ttk.Frame(self.notebook)
        self.chatbot_frame = ttk.Frame(self.notebook)  # Nova aba para o chatbot
        self.alerts_frame = ttk.Frame(self.notebook)  # Nova aba para alertas meteorológicos
        self.profile_frame = ttk.Frame(self.notebook)  # Nova aba para o perfil do usuário

        self.notebook.add(self.location_frame, text='Localização')
        self.notebook.add(self.day_forecast_frame, text='Previsão do Dia')
        self.notebook.add(self.hourly_forecast_frame, text='Previsões Futuras')
        self.notebook.add(self.chatbot_frame, text='Chatbot')  # Adiciona a nova aba ao notebook
        self.notebook.add(self.alerts_frame, text='Alertas')  # Adiciona a nova aba ao notebook
        self.notebook.add(self.profile_frame, text='Perfil')  # Adiciona a nova aba ao notebook

        self.create_location_tab()
        self.create_day_forecast_tab()
        self.create_hourly_forecast_tab()
        self.create_chatbot_tab()  # Cria a nova aba do chatbot
        self.create_alerts_tab()  # Cria a nova aba de alertas meteorológicos
        self.create_profile_tab()  # Cria a nova aba do perfil do usuário

        # Adiciona o botão de logout
        self.logout_button = ttk.Button(self.root, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

    def logout(self):
        """Realiza o logout do usuário e retorna à tela de login."""
        for widget in self.root.winfo_children():
            widget.destroy()  # Remove todos os widgets da janela principal
        self.__init__(self.root)  # Recria a tela de login

    def create_location_tab(self):
        """Cria a aba de localização para entrada da cidade e exibição do mapa."""
        location_label = Label(self.location_frame, text="Localização", font=("Arial", 16))
        location_label.pack(pady=10)

        self.city_entry = Entry(self.location_frame, width=30, font=('Arial', 12))
        self.city_entry.insert(0, 'Digite a cidade')
        self.city_entry.bind("<FocusIn>", lambda event: self.clear_entry(event, self.city_entry, 'Digite a cidade'))
        self.city_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.city_entry, 'Digite a cidade'))
        self.city_entry.pack(pady=10)

        self.generate_button = ttk.Button(self.location_frame, text="Gerar", command=self.generate_forecast)
        self.generate_button.pack(pady=10)

        self.location_info = Label(self.location_frame, text="", font=("Arial", 12))
        self.location_info.pack()

        self.map_widget = TkinterMapView(self.location_frame, width=350, height=300, corner_radius=0)
        self.map_widget.pack(pady=10)

        # Adicionando o botão de modo escuro
        self.dark_mode_button = ttk.Button(self.location_frame, text="Modo Escuro", command=self.toggle_dark_mode)
        self.dark_mode_button.pack(pady=10)

        # Frame para colocar os botões lado a lado
        self.button_frame = Frame(self.location_frame)
        self.button_frame.pack(pady=10)

        self.view_day_forecast_button = ttk.Button(self.button_frame, text="Ver Previsão do Dia", command=self.view_day_forecast)
        self.view_day_forecast_button.pack(side='left', padx=5)

        self.view_hourly_forecast_button = ttk.Button(self.button_frame, text="Ver Previsões Futuras", command=self.view_hourly_forecast)
        self.view_hourly_forecast_button.pack(side='left', padx=5)

    def generate_forecast(self):
        """Gera a previsão do tempo para a cidade fornecida."""
        self.city = self.city_entry.get()
        if self.city == '' or self.city == 'Digite a cidade':
            messagebox.showerror("Erro", "Por favor, insira o nome da cidade.")
        else:
            try:
                api_key = 'dfc79743c3c285e1152a9b0262a1bc5f'  # Chave da API OpenWeatherMap
                weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={api_key}&lang=pt&units=metric')
                weather_response.raise_for_status()  # Verifica se a resposta foi bem-sucedida
                weather_data = weather_response.json()

                # Extraindo dados da resposta da API
                main = weather_data['main']
                weather = weather_data['weather'][0]
                wind = weather_data['wind']
                sys = weather_data['sys']
                clouds = weather_data['clouds']
                rain = weather_data.get('rain', {})

                # Processando dados extraídos
                temp_max = main['temp_max']
                temp_min = main['temp_min']
                precipitacao = rain.get('1h', 0)  # Precipitação na última hora
                umidade = main['humidity']
                qualidade_ar = 'N/A'  # Inicialmente como não disponível
                indice_uv = 'N/A'  # Não disponível diretamente
                velocidade_vento = wind['speed']
                sensacao_termica = main['feels_like']
                nascer_sol = datetime.fromtimestamp(sys['sunrise']).strftime('%H:%M')
                por_sol = datetime.fromtimestamp(sys['sunset']).strftime('%H:%M')
                descricao = weather['description']
                visibilidade = weather_data['visibility']
                nebulosidade = clouds['all']
                current_date = datetime.now().strftime('%Y-%m-%d')

                # Chamada à API de poluição do ar
                lat = weather_data['coord']['lat']
                lon = weather_data['coord']['lon']
                air_pollution_response = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}')
                air_pollution_response.raise_for_status()
                air_pollution_data = air_pollution_response.json()

                # Extraindo dados da resposta da API de poluição do ar
                air_quality_index = air_pollution_data['list'][0]['main']['aqi']
                pollutants = air_pollution_data['list'][0]['components']
                qualidade_ar = self.get_air_quality_description(air_quality_index)

                # Componentes de poluição do ar
                co = pollutants.get('co', 'N/A')
                no = pollutants.get('no', 'N/A')
                no2 = pollutants.get('no2', 'N/A')
                o3 = pollutants.get('o3', 'N/A')
                so2 = pollutants.get('so2', 'N/A')
                pm2_5 = pollutants.get('pm2_5', 'N/A')
                pm10 = pollutants.get('pm10', 'N/A')
                nh3 = pollutants.get('nh3', 'N/A')

                # Salvar dados no banco de dados
                self.db.insert_day_forecast(self.city, current_date, descricao, main['temp'], temp_max, temp_min, sensacao_termica, precipitacao, umidade, qualidade_ar, co, no, no2, o3, so2, pm2_5, pm10, nh3, indice_uv, velocidade_vento, visibilidade, nebulosidade, nascer_sol, por_sol)

                # Atualize a aba de localização
                self.location_info.config(text=f"{self.city}\nMáx: {temp_max}°C  Mín: {temp_min}°C")

                # Atualize a aba de previsão do dia
                for widget in self.day_forecast_frame.winfo_children():
                    widget.destroy()
                Label(self.day_forecast_frame, text="Previsão do Dia", font=("Arial", 16)).pack(pady=10)
                Label(self.day_forecast_frame, text=f"Descrição: {descricao}").pack()
                Label(self.day_forecast_frame, text=f"Temperatura: {main['temp']}°C").pack()
                Label(self.day_forecast_frame, text=f"Màx: {temp_max}°C, Mín: {temp_min}°C").pack()
                Label(self.day_forecast_frame, text=f"Sensação térmica: {sensacao_termica}°C").pack()
                Label(self.day_forecast_frame, text=f"Precipitação: {precipitacao} mm").pack()
                Label(self.day_forecast_frame, text=f"Umidade: {umidade}%").pack()
                Label(self.day_forecast_frame, text=f"Qualidade do ar: {qualidade_ar}").pack()
                Label(self.day_forecast_frame, text=f"CO: {co} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"NO: {no} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"NO2: {no2} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"O3: {o3} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"SO2: {so2} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"PM2.5: {pm2_5} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"PM10: {pm10} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"NH3: {nh3} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"Índice UV: {indice_uv}").pack()
                Label(self.day_forecast_frame, text=f"Velocidade do vento: {velocidade_vento} m/s").pack()
                Label(self.day_forecast_frame, text=f"Visibilidade: {visibilidade} m").pack()
                Label(self.day_forecast_frame, text=f"Nebulosidade: {nebulosidade}%").pack()
                Label(self.day_forecast_frame, text=f"Nascer do sol: {nascer_sol}").pack()
                Label(self.day_forecast_frame, text=f"Pôr do sol: {por_sol}").pack()

                # Atualize o mapa interativo
                self.map_widget.set_position(lat, lon)
                self.map_widget.set_marker(lat, lon, text=self.city)
            except requests.exceptions.RequestException as e:
                logging.error(f"Erro na requisição de previsão do tempo: {e}")
                messagebox.showerror("Erro", f"Erro ao obter dados de previsão do tempo: {e}")
            except mysql.connector.Error as e:
                logging.error(f"Erro ao salvar dados no banco de dados: {e}")
                messagebox.showerror("Erro", f"Erro ao salvar dados no banco de dados: {e}")
            except Exception as e:
                logging.error(f"Erro ao processar os dados de previsão do tempo: {e}")
                messagebox.showerror("Erro", f"Erro ao processar dados: {e}")

    def get_air_quality_description(self, index):
        """Retorna a descrição da qualidade do ar com base no índice fornecido."""
        if index == 1:
            return "Bom"
        elif index == 2:
            return "Justo"
        elif index == 3:
            return "Moderado"
        elif index == 4:
            return "Pobre"
        elif index == 5:
            return "Muito Pobre"
        else:
            return "Desconhecido"

    def view_day_forecast(self):
        """Exibe as previsões do dia salvas no banco de dados."""
        day_forecasts = self.db.fetch_day_forecast()
        if not day_forecasts:
            messagebox.showinfo("Informação", "Nenhuma previsão do dia encontrada.")
            return

        if self.day_forecast_window:
            self.day_forecast_window.destroy()

        self.day_forecast_window = tk.Toplevel(self.root)
        self.day_forecast_window.title("Previsões do Dia")
        self.day_forecast_window.geometry("600x400")

        # Cria um canvas e um frame de scroll
        canvas = Canvas(self.day_forecast_window)
        scroll_y = Scrollbar(self.day_forecast_window, orient="vertical", command=canvas.yview)

        # Cria um frame que será adicionado ao canvas
        scroll_frame = Frame(canvas)
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Adiciona o frame ao canvas
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        for forecast in day_forecasts:
            frame = Frame(scroll_frame)
            frame.pack(fill='x', padx=10, pady=5)
            
            forecast_text = (
                f"Cidade: {forecast[1]}\n"
                f"Data: {forecast[2]}\n"
                f"Descrição: {forecast[3]}\n"
                f"Temperatura: {forecast[4]}°C\n"
                f"Máxima: {forecast[5]}°C\n"
                f"Mínima: {forecast[6]}°C\n"
                f"Sensação Térmica: {forecast[7]}°C\n"
                f"Precipitação: {forecast[8]} mm\n"
                f"Umidade: {forecast[9]}%\n"
                f"Qualidade do Ar: {forecast[10]}\n"
                f"CO: {forecast[11]} μg/m³\n"
                f"NO: {forecast[12]} μg/m³\n"
                f"NO2: {forecast[13]} μg/m³\n"
                f"O3: {forecast[14]} μg/m³\n"
                f"SO2: {forecast[15]} μg/m³\n"
                f"PM2.5: {forecast[16]} μg/m³\n"
                f"PM10: {forecast[17]} μg/m³\n"
                f"NH3: {forecast[18]} μg/m³\n"
                f"Índice UV: {forecast[19]}\n"
                f"Velocidade do Vento: {forecast[20]} m/s\n"
                f"Visibilidade: {forecast[21]} m\n"
                f"Nebulosidade: {forecast[22]}%\n"
                f"Nascer do Sol: {forecast[23]}\n"
                f"Pôr do Sol: {forecast[24]}\n"
            )

            Label(frame, text=forecast_text, justify='left').pack(side='left', expand=True, fill='x')
            Button(frame, text="Excluir", command=lambda f_id=forecast[0]: self.delete_day_forecast(f_id)).pack(side='right')

    def delete_day_forecast(self, forecast_id):
        """Deleta a previsão do dia selecionada."""
        self.db.delete_day_forecast(forecast_id)
        messagebox.showinfo("Informação", "Previsão do dia deletada com sucesso.")
        day_forecasts = self.db.fetch_day_forecast()
        if not day_forecasts:
            self.day_forecast_window.destroy()
        else:
            self.view_day_forecast()

    def view_hourly_forecast(self):
        """Exibe as previsões futuras salvas no banco de dados."""
        hourly_forecasts = self.db.fetch_hourly_forecast()
        if not hourly_forecasts:
            messagebox.showinfo("Informação", "Nenhuma previsão futura encontrada.")
            return

        if self.hourly_forecast_window:
            self.hourly_forecast_window.destroy()

        self.hourly_forecast_window = tk.Toplevel(self.root)
        self.hourly_forecast_window.title("Previsões Futuras")
        self.hourly_forecast_window.geometry("600x400")

        # Cria um canvas e um frame de scroll
        canvas = Canvas(self.hourly_forecast_window)
        scroll_y = Scrollbar(self.hourly_forecast_window, orient="vertical", command=canvas.yview)

        # Cria um frame que será adicionado ao canvas
        scroll_frame = Frame(canvas)
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Adiciona o frame ao canvas
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        for forecast in hourly_forecasts:
            frame = Frame(scroll_frame)
            frame.pack(fill='x', padx=10, pady=5)
            
            forecast_text = (
                f"Cidade: {forecast[1]}\n"
                f"Data/Hora: {forecast[2]}\n"
                f"Temperatura: {forecast[3]}°C\n"
                f"Sensação Térmica: {forecast[4]}°C\n"
                f"Temperatura Mínima: {forecast[5]}°C\n"
                f"Temperatura Máxima: {forecast[6]}°C\n"
                f"Pressão: {forecast[7]} hPa\n"
                f"Umidade: {forecast[8]}%\n"
                f"Descrição: {forecast[9]}\n"
                f"Nuvens: {forecast[10]}%\n"
                f"Velocidade do Vento: {forecast[11]} m/s\n"
                f"Direção do Vento: {forecast[12]}°\n"
                f"Chuva: {forecast[13]} mm\n"
                f"Visibilidade: {forecast[14]} m\n"
            )

            Label(frame, text=forecast_text, justify='left').pack(side='left', expand=True, fill='x')
            Button(frame, text="Excluir", command=lambda f_id=forecast[0]: self.delete_hourly_forecast(f_id)).pack(side='right')

    def delete_hourly_forecast(self, forecast_id):
        """Deleta a previsão futura selecionada."""
        self.db.delete_hourly_forecast(forecast_id)
        messagebox.showinfo("Informação", "Previsão futura deletada com sucesso.")
        hourly_forecasts = self.db.fetch_hourly_forecast()
        if not hourly_forecasts:
            self.hourly_forecast_window.destroy()
        else:
            self.view_hourly_forecast()

    def create_day_forecast_tab(self):
        """Cria a aba de previsão do dia."""
        Label(self.day_forecast_frame, text="Previsão do Dia", font=("Arial", 16)).pack(pady=10)

    def create_hourly_forecast_tab(self):
        """Cria a aba de previsões Futuras."""
        Label(self.hourly_forecast_frame, text="Previsões Futuras", font=("Arial", 16)).pack(pady=10)

        self.cnt_entry = Entry(self.hourly_forecast_frame, width=30, font=('Arial', 12))
        self.cnt_entry.insert(0, 'Número de previsões horárias')
        self.cnt_entry.bind("<FocusIn>", lambda event: self.clear_entry(event, self.cnt_entry, 'Número de previsões horárias'))
        self.cnt_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.cnt_entry, 'Número de previsões horárias'))
        self.cnt_entry.pack(pady=10)

        self.hourly_generate_button = ttk.Button(self.hourly_forecast_frame, text="Gerar", command=self.generate_hourly_forecast)
        self.hourly_generate_button.pack(pady=10)

        self.hourly_forecast_info = Text(self.hourly_forecast_frame, wrap='word', width=40, height=20, font=("Arial", 12), state='disabled')
        self.hourly_forecast_info.pack(pady=10)

    def generate_hourly_forecast(self):
        """Gera as previsões futuras para a cidade fornecida."""
        cnt = self.cnt_entry.get()
        if not hasattr(self, 'city') or self.city == '' or self.city == 'Digite a cidade':
            messagebox.showerror("Erro", "Por favor, insira o nome da cidade na aba de Localização.")
        elif cnt == '' or cnt == 'Número de previsões horárias':
            messagebox.showerror("Erro", "Por favor, insira o número de previsões horárias.")
        else:
            try:
                cnt = int(cnt)  # Converte cnt para inteiro
                api_key = 'dfc79743c3c285e1152a9b0262a1bc5f'  # Chave da API OpenWeatherMap
                geocode_url = f"https://api.openweathermap.org/geo/1.0/direct?q={self.city}&appid={api_key}"
                geocode_requisicao = requests.get(geocode_url)
                geocode_requisicao.raise_for_status()
                geocode_dic = geocode_requisicao.json()

                if len(geocode_dic) > 0:
                    lat = geocode_dic[0]['lat']
                    lon = geocode_dic[0]['lon']
                    
                    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&cnt={cnt}&units=metric&lang=pt_br"
                    forecast_requisicao = requests.get(forecast_url)
                    forecast_requisicao.raise_for_status()
                    forecast_dic = forecast_requisicao.json()
                    
                    forecast_text = ""
                    for previsao in forecast_dic['list']:
                        dt = datetime.utcfromtimestamp(previsao['dt']).strftime('%Y-%m-%d %H:%M:%S')
                        temperatura = previsao['main']['temp']
                        sensacao_termica = previsao['main']['feels_like']
                        temp_min = previsao['main']['temp_min']
                        temp_max = previsao['main']['temp_max']
                        pressao = previsao['main']['pressure']
                        umidade = previsao['main']['humidity']
                        descricao = previsao['weather'][0]['description']
                        nuvens = previsao['clouds']['all']
                        velocidade_vento = previsao['wind']['speed']
                        direcao_vento = previsao['wind']['deg']
                        chuva = previsao.get('rain', {}).get('3h', 0)
                        visibilidade = previsao.get('visibility', 10000)
                        
                        # Salvar dados no banco de dados
                        self.db.insert_hourly_forecast(self.city, dt, temperatura, sensacao_termica, temp_min, temp_max, pressao, umidade, descricao, nuvens, velocidade_vento, direcao_vento, chuva, visibilidade)
                        
                        forecast_text += (f"Data/Hora: {dt}\n"
                                          f"Temperatura: {temperatura}°C\n"
                                          f"Sensação térmica: {sensacao_termica}°C\n"
                                          f"Temperatura mínima: {temp_min}°C\n"
                                          f"Temperatura máxima: {temp_max}°C\n"
                                          f"Pressão: {pressao} hPa\n"
                                          f"Umidade: {umidade}%\n"
                                          f"Descrição: {descricao}\n"
                                          f"Nuvens: {nuvens}%\n"
                                          f"Velocidade do vento: {velocidade_vento} m/s\n"
                                          f"Direção do vento: {direcao_vento}°\n"
                                          f"Chuva (últimas 3 horas): {chuva} mm\n"
                                          f"Visibilidade: {visibilidade} metros\n"
                                          + "-" * 40 + "\n")

                    self.hourly_forecast_info.config(state='normal')
                    self.hourly_forecast_info.delete('1.0', tk.END)
                    self.hourly_forecast_info.insert(tk.END, forecast_text)
                    self.hourly_forecast_info.config(state='disabled')
                else:
                    messagebox.showerror("Erro", "Cidade não encontrada. Por favor, tente novamente.")
            except ValueError:
                logging.error("Erro ao converter número de previsões horárias para inteiro.")
                messagebox.showerror("Erro", "Por favor, insira um número válido para o número de previsões horárias.")
            except requests.exceptions.RequestException as e:
                logging.error(f"Erro na requisição de previsões futuras: {e}")
                messagebox.showerror("Erro", f"Erro ao obter dados de previsões futuras: {e}")
            except mysql.connector.Error as e:
                logging.error(f"Erro ao salvar dados no banco de dados: {e}")
                messagebox.showerror("Erro", f"Erro ao salvar dados no banco de dados: {e}")
            except Exception as e:
                logging.error(f"Erro ao processar os dados de previsões futuras: {e}")
                messagebox.showerror("Erro", f"Erro ao processar dados: {e}")

    def create_chatbot_tab(self):
        """Cria a aba do chatbot para interação com os usuários."""
        Label(self.chatbot_frame, text="Chatbot para Agricultores", font=("Arial", 16)).pack(pady=10)

        self.chat_input = Entry(self.chatbot_frame, width=50, font=('Arial', 12))
        self.chat_input.insert(0, 'Digite sua pergunta...')
        self.chat_input.bind("<FocusIn>", lambda event: self.clear_entry(event, self.chat_input, 'Digite sua pergunta...'))
        self.chat_input.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.chat_input, 'Digite sua pergunta...'))
        self.chat_input.bind("<Return>", lambda event: self.process_question())
        self.chat_input.pack(pady=10)

        self.chat_output = Text(self.chatbot_frame, wrap='word', width=40, height=15, font=("Arial", 12), state='disabled', bg="#f0f0f0")
        self.chat_output.pack(pady=10)

        self.send_button = ttk.Button(self.chatbot_frame, text="Enviar", command=self.process_question)
        self.send_button.pack(pady=10)

    def process_question(self):
        """Processa a pergunta do usuário e retorna a resposta."""
        question = self.chat_input.get()
        if question == '' or question == 'Digite sua pergunta...':
            messagebox.showerror("Erro", "Por favor, insira uma pergunta.")
        else:
            answer = self.get_chatbot_response(question)
            self.chat_output.config(state='normal')
            self.chat_output.insert(tk.END, f"Pergunta: {question}\nResposta: {answer}\n{'-' * 40}\n")
            self.chat_output.config(state='disabled')

    def get_chatbot_response(self, question):
        """Retorna uma resposta predefinida com base na pergunta fornecida."""
        predefined_qa = {
            "Qual a previsão de chuva para hoje?": "A previsão indica chuva leve no final da tarde, acumulando cerca de 5 mm.",
            "Como estará a umidade do solo amanhã?": "A umidade do solo estará alta devido às chuvas previstas para esta noite.",
            "Qual a melhor hora para irrigar as plantações amanhã?": "A melhor hora para irrigar será pela manhã, antes das 10h, para evitar a evaporação excessiva.",
            "Haverá geada nos próximos dias?": "Não há previsão de geada nos próximos cinco dias.",
            "Qual a temperatura mínima esperada para esta semana?": "A temperatura mínima esperada é de 12°C na quarta-feira.",
            "Qual a previsão de ventos fortes para hoje?": "Haverá ventos fortes à tarde, com rajadas de até 30 km/h.",
            "Quando será o próximo período de seca?": "Um período de seca é esperado para começar em duas semanas, durando cerca de cinco dias.",
            "Qual a previsão de temperatura para o próximo fim de semana?": "A temperatura deve variar entre 18°C e 25°C no próximo fim de semana.",
            "Haverá tempestades amanhã?": "Sim, tempestades são esperadas para amanhã à noite, com risco de granizo.",
            "Qual o índice de radiação UV para hoje?": "O índice de radiação UV será alto hoje, alcançando um valor de 8 ao meio-dia.",
            "Como estará a visibilidade para pulverização de defensivos amanhã?": "A visibilidade estará boa pela manhã, com condições adequadas para pulverização.",
            "Quando será o próximo período de clima seco?": "O próximo período de clima seco começará daqui a três dias e durará cerca de uma semana.",
            "Haverá risco de inundações esta semana?": "Não há risco de inundações previsto para esta semana.",
            "Qual a previsão de temperatura máxima para hoje?": "A temperatura máxima esperada para hoje é de 28°C.",
            "Qual a quantidade esperada de chuva para os próximos três dias?": "A previsão é de 15 mm de chuva acumulada nos próximos três dias.",
            "Haverá mudanças bruscas de temperatura nos próximos dias?": "Sim, haverá uma queda de temperatura de cerca de 10°C na próxima sexta-feira.",
            "Qual a previsão de umidade relativa do ar para amanhã?": "A umidade relativa do ar estará em torno de 70% pela manhã.",
            "Qual o melhor dia para colher trigo nesta semana?": "Sexta-feira será o melhor dia, com previsão de tempo seco e temperaturas amenas.",
            "Haverá neblina nos próximos dias?": "Sim, neblina densa é esperada na madrugada de quinta-feira.",
            "Qual a previsão de raios UV para o fim de semana?": "Os índices de UV estarão moderados no fim de semana, variando entre 4 e 6.",
            "Quando é o melhor horário para aplicar fertilizantes?": "O melhor horário para aplicação será no início da manhã, antes das 9h.",
            "Haverá condições favoráveis para a ocorrência de pragas esta semana?": "Sim, o clima úmido previsto pode favorecer a ocorrência de pragas.",
            "Qual a previsão de ventos para os próximos três dias?": "Ventos moderados, com velocidade média de 15 km/h, são esperados nos próximos três dias.",
            "Haverá nevasca nos próximos dias?": "Não há previsão de nevasca para os próximos dias.",
            "Qual a previsão de temperatura durante a noite para esta semana?": "As temperaturas noturnas variarão entre 15°C e 20°C durante esta semana."
        }
        return predefined_qa.get(question, f"Desculpe, não tenho uma resposta para '{question}'.")

    def toggle_dark_mode(self):
        """Alterna entre os modos claro e escuro."""
        if hasattr(self, 'dark_mode') and self.dark_mode:
            # Modo claro
            self.apply_light_mode()
            self.dark_mode = False
        else:
            # Modo escuro
            self.apply_dark_mode()
            self.dark_mode = True

    def apply_dark_mode(self):
        """Aplica o modo escuro à interface."""
        # Alterar cores dos widgets para o modo escuro
        style = ttk.Style()
        style.configure('TFrame', background='#333333')
        style.configure('TLabel', background='#333333', foreground='#FFFFFF')
        style.configure('TEntry', fieldbackground='#333333', foreground='#FFFFFF', insertcolor='#FFFFFF')
        style.configure('TButton', background='#333333', foreground='#FFFFFF')

        self.root.configure(bg="#333333")
        self.location_frame.configure(style='TFrame')
        self.day_forecast_frame.configure(style='TFrame')
        self.hourly_forecast_frame.configure(style='TFrame')
        self.chatbot_frame.configure(style='TFrame')
        self.alerts_frame.configure(style='TFrame')

        # Alterar cores dos rótulos e entradas
        for widget in self.location_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#333333", fg="#FFFFFF")
            elif isinstance(widget, Entry):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")

        for widget in self.day_forecast_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#333333", fg="#FFFFFF")
            elif isinstance(widget, Entry):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")

        for widget in self.hourly_forecast_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#333333", fg="#FFFFFF")
            elif isinstance(widget, Entry):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")
            elif isinstance(widget, Text):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")

        for widget in self.chatbot_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#333333", fg="#FFFFFF")
            elif isinstance(widget, Entry):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")
            elif isinstance(widget, Text):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")

        for widget in self.alerts_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#333333", fg="#FFFFFF")
            elif isinstance(widget, Entry):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")
            elif isinstance(widget, Text):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")

    def apply_light_mode(self):
        """Aplica o modo claro à interface."""
        # Reverter para as cores do modo claro
        style = ttk.Style()
        style.configure('TFrame', background='#FFFFFF')
        style.configure('TLabel', background='#FFFFFF', foreground='#000000')
        style.configure('TEntry', fieldbackground='#FFFFFF', foreground='#000000', insertcolor='#000000')
        style.configure('TButton', background='#FFFFFF', foreground='#000000')

        self.root.configure(bg="#FFFFFF")
        self.location_frame.configure(style='TFrame')
        self.day_forecast_frame.configure(style='TFrame')
        self.hourly_forecast_frame.configure(style='TFrame')
        self.chatbot_frame.configure(style='TFrame')
        self.alerts_frame.configure(style='TFrame')

        # Reverter cores dos rótulos e entradas
        for widget in self.location_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#FFFFFF", fg="#000000")
            elif isinstance(widget, Entry):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")

        for widget in self.day_forecast_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#FFFFFF", fg="#000000")
            elif isinstance(widget, Entry):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")

        for widget in self.hourly_forecast_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#FFFFFF", fg="#000000")
            elif isinstance(widget, Entry):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
            elif isinstance(widget, Text):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")

        for widget in self.chatbot_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#FFFFFF", fg="#000000")
            elif isinstance(widget, Entry):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
            elif isinstance(widget, Text):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")

        for widget in self.alerts_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#FFFFFF", fg="#000000")
            elif isinstance(widget, Entry):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
            elif isinstance(widget, Text):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")

    def create_alerts_tab(self):
        """Cria a aba de alertas meteorológicos."""
        tk.Label(self.alerts_frame, text="Alertas", font=("Arial", 16)).pack(pady=10)
        self.alerts_text = tk.Text(self.alerts_frame, wrap='word', width=40, height=20, font=('Arial', 12))
        self.alerts_text.pack(pady=10)

        self.fetch_alerts_button = ttk.Button(self.alerts_frame, text="Atualizar Alertas", command=self.fetch_alerts)
        self.fetch_alerts_button.pack(pady=10)

    def fetch_alerts(self):
        url = "http://api.openweathermap.org/data/2.5/alerts"  # Substitua pelo URL real
        headers = {'Content-Type': 'application/json'}
        data = {
            'appid': 'dfc79743c3c285e1152a9b0262a1bc5f'  # Adicione a chave da API, se necessário
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()

            if response.status_code == 200:
                alert = response_data.get('alert', {})
                description = alert.get('description', [{}])[0]

                self.alerts_text.delete(1.0, tk.END)  # Limpa o texto anterior

                self.alerts_text.insert(tk.END, f"ID do Alerta: {alert.get('id', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Tipo de Mensagem: {response_data.get('msg_type', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Categorias: {', '.join(response_data.get('categories', []))}\n")
                self.alerts_text.insert(tk.END, f"Urgência: {response_data.get('urgency', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Severidade: {response_data.get('severity', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Certeza: {response_data.get('certainty', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Início: {datetime.fromtimestamp(response_data.get('start', 0)).strftime('%d/%m/%Y %H:%M:%S')}\n")
                self.alerts_text.insert(tk.END, f"Fim: {datetime.fromtimestamp(response_data.get('end', 0)).strftime('%d/%m/%Y %H:%M:%S')}\n")
                self.alerts_text.insert(tk.END, f"Remetente: {response_data.get('sender', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Língua: {description.get('language', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Evento: {description.get('event', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Título: {description.get('headline', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Descrição: {description.get('description', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Instruções: {description.get('instruction', 'N/A')}\n")
            else:
                messagebox.showerror("Erro", "Falha ao obter alertas meteorológicos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter dados: {e}")

    def create_profile_tab(self):
        """Cria a aba de perfil do usuário para visualização e edição dos dados."""
        Label(self.profile_frame, text="Perfil do Usuário", font=("Arial", 16)).pack(pady=10)

        Label(self.profile_frame, text="Nome Completo").pack()
        self.full_name_entry = Entry(self.profile_frame, width=30)
        self.full_name_entry.pack()

        Label(self.profile_frame, text="Email").pack()
        self.email_entry_profile = Entry(self.profile_frame, width=30)
        self.email_entry_profile.pack()

        Label(self.profile_frame, text="Senha").pack()
        self.password_entry_profile = Entry(self.profile_frame, show='*', width=30)
        self.password_entry_profile.pack()

        Label(self.profile_frame, text="Gênero").pack()
        self.gender_var_profile = StringVar(self.profile_frame)
        self.gender_var_profile.set("Masculino")  # valor padrão
        gender_options = ["Masculino", "Feminino", "Outro"]
        self.gender_menu_profile = OptionMenu(self.profile_frame, self.gender_var_profile, *gender_options)
        self.gender_menu_profile.pack()

        Label(self.profile_frame, text="Data de Nascimento").pack()
        self.birthdate_entry_profile = DateEntry(self.profile_frame, width=30, date_pattern='y-mm-dd')
        self.birthdate_entry_profile.pack()

        Label(self.profile_frame, text="Celular").pack()
        self.phone_entry_profile = Entry(self.profile_frame, width=30)
        self.phone_entry_profile.pack()

        Label(self.profile_frame, text="Nacionalidade").pack()
        self.nationality_entry_profile = Entry(self.profile_frame, width=30)
        self.nationality_entry_profile.pack()

        Label(self.profile_frame, text="Cultura Agrícola").pack()
        self.agricultural_culture_entry_profile = Entry(self.profile_frame, width=30)
        self.agricultural_culture_entry_profile.pack()

        self.save_profile_button = ttk.Button(self.profile_frame, text="Salvar Alterações", command=self.update_user_profile)
        self.save_profile_button.pack(pady=10)

        self.load_user_profile()  # Carrega o perfil do usuário ao abrir a aba

    def load_user_profile(self):
        """Carrega os dados do perfil do usuário."""
        user_data = self.db.fetch_user_profile(self.user_email)
        if user_data:
            self.full_name_entry.insert(0, user_data[0])
            self.email_entry_profile.insert(0, user_data[1])
            self.password_entry_profile.insert(0, user_data[2])
            self.gender_var_profile.set(user_data[3])
            self.birthdate_entry_profile.set_date(user_data[4])
            self.phone_entry_profile.insert(0, user_data[5])
            self.nationality_entry_profile.insert(0, user_data[6])
            self.agricultural_culture_entry_profile.insert(0, user_data[7])
        else:
            messagebox.showerror("Erro", "Não foi possível carregar os dados do perfil.")

    def update_user_profile(self):
        """Atualiza os dados do perfil do usuário."""
        nome_completo = self.full_name_entry.get()
        email = self.email_entry_profile.get()
        senha = self.password_entry_profile.get()
        genero = self.gender_var_profile.get()
        data_nascimento = self.birthdate_entry_profile.get_date()
        celular = self.phone_entry_profile.get()
        nacionalidade = self.nationality_entry_profile.get()
        cultura_agricola = self.agricultural_culture_entry_profile.get()

        if not (nome_completo and email and senha and genero and data_nascimento and celular and nacionalidade and cultura_agricola):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        try:
            cursor = self.db.connection.cursor()
            update_query = """UPDATE usuarios SET nome_completo=%s, senha=%s, genero=%s, data_nascimento=%s, celular=%s, nacionalidade=%s, cultura_agricola=%s WHERE email=%s"""
            cursor.execute(update_query, (nome_completo, senha, genero, data_nascimento, celular, nacionalidade, cultura_agricola, email))
            self.db.connection.commit()
            messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso.")
        except mysql.connector.Error as e:
            logging.error(f"Erro ao atualizar perfil: {e}")
            messagebox.showerror("Erro", f"Erro ao atualizar perfil: {e}")

    def show_signup(self, event=None):
        """Exibe a janela de cadastro."""
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Cadastro de Usuário")
        signup_window.geometry("400x550")

        Label(signup_window, text="Cadastro de Usuário", font=("Arial", 16)).pack(pady=10)

        # Campos de entrada para cadastro
        Label(signup_window, text="Nome Completo").pack()
        full_name_entry = Entry(signup_window, width=30)
        full_name_entry.pack()

        Label(signup_window, text="Email").pack()
        email_entry = Entry(signup_window, width=30)
        email_entry.pack()

        Label(signup_window, text="Senha").pack()
        password_entry = Entry(signup_window, show='*', width=30)
        password_entry.pack()

        Label(signup_window, text="Gênero").pack()
        gender_var = StringVar(signup_window)
        gender_var.set("Masculino")  # valor padrão
        gender_options = ["Masculino", "Feminino", "Outro"]
        gender_menu = OptionMenu(signup_window, gender_var, *gender_options)
        gender_menu.pack()

        Label(signup_window, text="Data de Nascimento").pack()
        birthdate_entry = DateEntry(signup_window, width=30, date_pattern='y-mm-dd')
        birthdate_entry.pack()

        Label(signup_window, text="Celular").pack()
        phone_entry = Entry(signup_window, width=30)
        phone_entry.pack()

        Label(signup_window, text="Nacionalidade").pack()
        nationality_entry = Entry(signup_window, width=30)
        nationality_entry.pack()

        Label(signup_window, text="Cultura Agrícola").pack()
        agricultural_culture_entry = Entry(signup_window, width=30)
        agricultural_culture_entry.pack()

        def save_user():
            """Salva os dados do usuário no banco de dados."""
            nome_completo = full_name_entry.get()
            email = email_entry.get()
            senha = password_entry.get()
            genero = gender_var.get()
            data_nascimento = birthdate_entry.get_date()
            celular = phone_entry.get()
            nacionalidade = nationality_entry.get()
            cultura_agricola = agricultural_culture_entry.get()

            if not (nome_completo and email and senha and genero and data_nascimento and celular and nacionalidade and cultura_agricola):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
                return

            self.db.insert_user(nome_completo, email, senha, genero, data_nascimento, celular, nacionalidade, cultura_agricola)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso.")
            signup_window.destroy()

        Button(signup_window, text="Salvar", command=save_user).pack(pady=10)

class SplashScreen:
    def __init__(self, splash_root):
        """Inicializa a tela de splash."""
        self.splash_root = splash_root
        self.splash_root.title("Agroforecast")

        splash_canvas = Canvas(self.splash_root, width=350, height=600, bg='#0000FF')
        splash_canvas.pack()

        splash_logo = tk.PhotoImage(file="logo.png")
        scaled_splash_logo = splash_logo.subsample(2, 2)
        splash_canvas.create_image(175, 300, image=scaled_splash_logo, anchor='center')
        self.splash_logo_image = scaled_splash_logo

        self.splash_root.after(3000, self.show_login)

    def show_login(self):
        """Fecha a tela de splash e exibe a tela de login."""
        self.splash_root.destroy()
        root = tk.Tk()
        root.geometry("350x600")
        app = AgroforecastApp(root)
        root.mainloop()

if __name__ == "__main__":
    splash_root = tk.Tk()
    SplashScreen(splash_root)
    splash_root.mainloop()
