/*
 * TCC Grupo 6 - 2026S2
 * Sistema de Controle de Estoque de Madeiras para um Luthier
 *
 * Firmware ESP32 + DHT22 + LED de status
 * Autor: João Henrique da Silva
 * Data: 2026
 *
 * Pinagem:
 *   DHT22 DATA -> GPIO 4
 *   LED vermelho -> GPIO 2
 */

#include <Arduino.h>
#include <WiFi.h>
#include <DHT.h>
#include "secrets.h"   // ← credenciais vindas do arquivo local

// ===== Protótipos das funções (OBRIGATÓRIO em .cpp) =====
void conectarWiFi();
void lerEnviarDados();

// As constantes WIFI_SSID e WIFI_PASSWORD já vêm do secrets.h

// ===== Configurações do DHT22 =====
#define DHT_PIN   4
#define DHT_TYPE  DHT22
DHT dht(DHT_PIN, DHT_TYPE);

// ===== LED de status =====
#define LED_PIN   2

// ===== Intervalo entre leituras (ms) =====
const unsigned long INTERVALO_LEITURA = 5000;
unsigned long ultimaLeitura = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  Serial.println("=== TCC Grupo 6 - Controle de Estoque de Madeiras ===");
  Serial.println("Iniciando sensor DHT22...");
  dht.begin();

  conectarWiFi();
}

void loop() {
  unsigned long agora = millis();

  if (agora - ultimaLeitura >= INTERVALO_LEITURA) {
    ultimaLeitura = agora;
    lerEnviarDados();
  }

  // Pisca o LED para indicar que o código está rodando
  digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  delay(500);
}

void conectarWiFi() {
  Serial.print("Conectando ao WiFi: ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 20) {
    delay(500);
    Serial.print(".");
    tentativas++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi conectado!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFalha ao conectar ao WiFi. Modo offline ativado.");
  }
}

void lerEnviarDados() {
  float temperatura = dht.readTemperature();
  float umidade = dht.readHumidity();

  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("Erro ao ler o sensor DHT22!");
    return;
  }

  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.print(" °C | Umidade: ");
  Serial.print(umidade);
  Serial.println(" %");

  // Verifica se está fora dos parâmetros (ajustar conforme necessário)
  if (temperatura < 15.0 || temperatura > 30.0 ||
      umidade < 40.0 || umidade > 70.0) {
    Serial.println("⚠️  ALERTA: Condições fora do padrão!");
    // Aqui futuramente: enviar alerta para o backend
  }

  // TODO: enviar dados para o backend via HTTP/MQTT
  // enviarParaBackend(temperatura, umidade);
}