# Firmware ESP32 + DHT22

## Componentes
- ESP32 (placa de desenvolvimento)
- Sensor DHT22 (temperatura e umidade)
- LED vermelho (indicador de status)

## Pinagem
| Componente | Pino ESP32 |
|---|---|
| DHT22 DATA | GPIO 4 |
| DHT22 VCC  | 3.3V |
| DHT22 GND  | GND |
| LED +      | GPIO 2 (com resistor 220Ω) |
| LED -      | GND |

## Bibliotecas necessárias (Arduino IDE)
- `DHT sensor library` (Adafruit)
- `Adafruit Unified Sensor`

## Como gravar
1. Abra `esp32_dht22.ino` na Arduino IDE
2. Selecione a placa **ESP32 Dev Module**
3. Configure WiFi no código
4. Compile e faça o upload