/*
 * ============================================================
 * TCC Grupo 6 - 2026S2
 * Sistema de Controle de Estoque de Madeiras para um Luthier
 * ============================================================
 *
 * ARQUIVO DE EXEMPLO
 * ------------------
 * Este arquivo serve como MODELO para as credenciais do ESP32.
 *
 * COMO USAR:
 *   1. Copie este arquivo para "secrets.h" na mesma pasta:
 *        cp secrets.example.h secrets.h
 *   2. Edite "secrets.h" com seus dados reais (WiFi, IP do backend).
 *   3. NUNCA faça commit de "secrets.h" (já está no .gitignore).
 *
 * Em caso de dúvidas, consulte hardware/firmware/README.md
 * ============================================================
 */

#ifndef SECRETS_H
#define SECRETS_H

// ===== Credenciais de WiFi =====
#define WIFI_SSID       "NOME_DA_REDE_WIFI"
#define WIFI_PASSWORD   "SENHA_DO_WIFI"

// ===== Endereço do backend (onde o ESP32 envia os dados) =====
// Exemplo local:  "http://192.168.0.10:5000/api/leituras"
// Exemplo público: "https://tcc-grupo6.exemplo.com/api/leituras"
#define BACKEND_URL     "http://192.168.0.10:5000/api/leituras"

// ===== Token de autenticação (opcional) =====
// Se o backend exigir um token para aceitar requisições
#define API_TOKEN       "cole_o_token_aqui"

#endif  // SECRETS_H