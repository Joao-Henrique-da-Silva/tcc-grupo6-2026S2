# Sistema de Controle de Estoque de Madeiras para um Luthier

Projeto de TCC do curso de **Engenharia de Computação** da **Universidade Virtual do Estado de São Paulo (UNIVESP)** — Turma 2026S2.

O projeto propõe um **sistema IoT** para monitoramento e rastreabilidade das condições de armazenamento de madeiras utilizadas na luthieria, integrando sensores ambientais, identificação por QR Code, banco de dados histórico, geração de alertas e funcionamento offline.

---

## 👥 Integrantes

| Nome | RA |
|---|---|
| Arthur Rogério Ferreira | 2207985 |
| Daniel Francisco Sobrinho | 2202929 |
| Fernando Pires Barbosa | 2232308 |
| Gisele Vieira de Amorim | 2207864 |
| João Henrique da Silva | 2106952 |
| Marco Aurélio de Freitas Rodrigues | 23205488 |
| Wandery Aparecido Ramos | 2100353 |

**Orientador(a):** _(a definir)_

---

## 🎯 Objetivos

### Objetivo geral
Desenvolver e avaliar um sistema IoT para monitoramento e rastreabilidade das condições de armazenamento de madeiras utilizadas na luthieria.

### Objetivos específicos
- [ ] Levantar requisitos e realizar revisão da literatura
- [ ] Projetar e implementar hardware e software
- [ ] Monitorar temperatura e umidade
- [ ] Identificar madeiras por QR Code
- [ ] Armazenar dados e históricos
- [ ] Gerar alertas para condições fora dos parâmetros
- [ ] Permitir funcionamento temporário offline
- [ ] Avaliar a variação de massa das madeiras
- [ ] Realizar testes para validar o sistema

---

## 🧱 Estrutura do Repositório

```
tcc-grupo6-2026S2/
├── docs/                  # Documentação, projeto de pesquisa, requisitos
├── hardware/
│   ├── esquemas/          # Diagramas de circuito, imagens
│   └── firmware/          # Código do ESP32 (Arduino/C++)
│       ├── esp32_dht22.ino
│       ├── secrets.example.h
│       └── README.md
├── software/
│   ├── backend/           # API / servidor (recebe dados do ESP32)
│   ├── frontend/          # Interface web / dashboard
│   └── database/          # Schema do banco de dados
├── qrcode/                # Geração e leitura de QR Codes
├── testes/                # Testes de integração e validação
├── .gitignore
└── README.md
```

---

## 🛠️ Tecnologias Utilizadas

### Hardware
- **ESP32** — microcontrolador com WiFi integrado
- **DHT22** — sensor de temperatura e umidade
- **LED vermelho** — indicador de status do firmware
- **Leitor de QR Code USB** — identificação das madeiras

### Software
- **Arduino IDE / PlatformIO** — desenvolvimento do firmware
- **Python (Flask)** — backend / API REST _(a confirmar)_
- **SQLite / PostgreSQL** — banco de dados _(a confirmar)_
- **HTML/CSS/JS** — frontend / dashboard _(a confirmar)_

---

## 🚀 Como Começar

### 1. Clonar o repositório

```bash
git clone git@github.com:Marco-Univesp/tcc-grupo6-2026S2.git
cd tcc-grupo6-2026S2
```

### 2. Configurar identidade local (apenas neste repositório)

```bash
git config --local user.name "Seu Nome"
git config --local user.email "seu_numero@aluno.univesp.br"
```

### 3. Firmware (ESP32)

Consulte as instruções detalhadas em [`hardware/firmware/README.md`](hardware/firmware/README.md).

**Resumo:**
1. Copie `secrets.example.h` para `secrets.h`
2. Preencha o SSID e a senha do WiFi
3. Abra `esp32_dht22.ino` na Arduino IDE
4. Selecione a placa **ESP32 Dev Module**
5. Compile e faça upload

### 4. Backend (a definir)

```bash
cd software/backend
# (instruções serão adicionadas quando o backend estiver pronto)
```

---

## 🌿 Fluxo de Trabalho no Git

**Nunca trabalhe direto na `main`.** Use branches por tarefa:

```bash
# 1. Sincronizar com o repositório principal
git checkout main
git fetch upstream
git merge upstream/main

# 2. Criar branch da tarefa
git checkout -b feature/nome-da-tarefa

# 3. Trabalhar, salvar e commitar
git add .
git commit -m "feat: descrição do que foi feito"

# 4. Enviar para o fork
git push origin feature/nome-da-tarefa

# 5. Abrir Pull Request no GitHub (fork → main do upstream)
```

### Convenção de commits (Conventional Commits)
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `refactor:` refatoração
- `test:` testes
- `chore:` tarefas de manutenção

---

## 📅 Cronograma

| Período | Etapa | Responsáveis |
|---|---|---|
| 1ª quinzena de agosto | Levantamento de requisitos | Todos |
| 2ª quinzena de agosto | Validação de requisitos | Todos |
| 1ª quinzena de setembro | Prototipagem (software + hardware) | Fernando, Wandery, João Henrique |
| 2ª quinzena de setembro | Módulos principais + integração | Fernando, Wandery, João Henrique |
| 1ª quinzena de outubro | Refinamento + compra de componentes | Todos |
| 2ª quinzena de outubro | Integração e testes preliminares | Fernando, Wandery, João Henrique |
| 1ª quinzena de novembro | Testes funcionais | Todos |
| 2ª quinzena de novembro | Apresentação final | Todos |

---

## 📚 Referências

_(a serem adicionadas conforme a norma ABNT)_

- GLASS, Samuel V.; ZELINKA, Samuel L. **Moisture relations and physical properties of wood.** In: ROSS, Robert J. (ed.). Wood handbook: wood as an engineering material. Madison, WI: USDA, 2010.
- SILVA, José Carlos da; OLIVEIRA, Marcos Vinícius. **Automação e controle de processos industriais com Arduino e sensores IoT.** São Paulo: Érica, 2024.
- TURBAN, Efraim; VOLONINO, Linda. **Tecnologia da informação para gestão.** 10. ed. Rio de Janeiro: LTC, 2021.

_(lista completa no PDF do projeto de pesquisa)_

---

## 📄 Licença

Projeto acadêmico desenvolvido para fins educacionais na UNIVESP — 2026S2.