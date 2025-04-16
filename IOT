#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>  // untuk HTTPS (Ubidots)

// Pin sensor & buzzer
#define TRIG_PIN 2
#define ECHO_PIN 15
#define BUZZER_PIN 4

// WiFi credentials
const char* ssid = "awok awok";         
const char* password = "[yntkts]";      

// Ubidots config
const char* token = "BBUS-P4twvDDkjPFuAZVSnnzuwAU4XxP0E4";
const char* device_label = "esp32";
const char* variable_label = "ultrasonik";

// Flask config
const char* flask_host = "http://192.168.110.151:5000"; // Ganti dengan IP server Flask kamu

// Fungsi hitung jarak
float getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  return duration * 0.034 / 2;
}

// Kirim ke Ubidots
void sendToUbidots(float distance) {
  WiFiClientSecure client;
  client.setInsecure(); // Abaikan SSL (untuk testing)

  HTTPClient https;
  String url = String("https://industrial.api.ubidots.com/api/v1.6/devices/") + device_label;

  Serial.println("[HTTP] Connecting to Ubidots...");
  if (https.begin(client, url)) {
    https.addHeader("Content-Type", "application/json");
    https.addHeader("X-Auth-Token", token);

    String payload = "{\"" + String(variable_label) + "\":" + String(distance) + "}";
    int httpCode = https.POST(payload);

    if (httpCode > 0) {
      Serial.print("[HTTP] Ubidots Response code: ");
      Serial.println(httpCode);
    } else {
      Serial.print("[HTTP] Ubidots POST failed: ");
      Serial.println(https.errorToString(httpCode).c_str());
    }

    https.end();
  } else {
    Serial.println("[HTTP] Unable to connect to Ubidots");
  }
}

// Kirim ke Flask lokal
void sendToFlask(float distance) {
  HTTPClient http;
  String url = String(flask_host) + "/receive"; // endpoint Flask

  Serial.println("[HTTP] Connecting to Flask...");
  if (http.begin(url)) {
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"distance\":" + String(distance) + "}";
    int httpCode = http.POST(payload);

    if (httpCode > 0) {
      Serial.print("[HTTP] Flask Response code: ");
      Serial.println(httpCode);
    } else {
      Serial.print("[HTTP] Flask POST failed: ");
      Serial.println(http.errorToString(httpCode).c_str());
    }

    http.end();
  } else {
    Serial.println("[HTTP] Unable to connect to Flask");
  }
}

// Setup awal
void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 20) {
    delay(500);
    Serial.print(".");
    retries++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nGagal konek WiFi!");
    Serial.print("WiFi status: ");
    Serial.println(WiFi.status());
  }
}

// Loop utama
void loop() {
  float distance = getDistance();
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Zona berdasarkan jarak
  if (distance <= 15) {
    Serial.println("Status: BAHAYA!");
    digitalWrite(BUZZER_PIN, HIGH);
  } else if (distance <= 30) {
    Serial.println("Status: SEDANG");
    digitalWrite(BUZZER_PIN, LOW);
  } else {
    Serial.println("Status: AMAN");
    digitalWrite(BUZZER_PIN, LOW);
  }

  sendToUbidots(distance);
  sendToFlask(distance);

  delay(2000); // jeda antar pengiriman data
}
