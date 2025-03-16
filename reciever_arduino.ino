#include <ESP8266WiFi.h>
#include <espnow.h>

// Structure to hold the received data
typedef struct test_struct {
  int busCount;
  int carCount;
  int autoRickshawCount;
  int motorcycleCount;
} test_struct;

test_struct objectCounts;

// Callback function to handle received data
void OnDataRecv(uint8_t *mac, uint8_t *incomingData, uint8_t len) {
  memcpy(&objectCounts, incomingData, sizeof(objectCounts));
  Serial.print("Bytes received: ");
  Serial.println(len);
  Serial.print("Bus Count: ");
  Serial.println(objectCounts.busCount);
  Serial.print("Car Count: ");
  Serial.println(objectCounts.carCount);
  Serial.print("Auto Rickshaw Count: ");
  Serial.println(objectCounts.autoRickshawCount);
  Serial.print("Motorcycle Count: ");
  Serial.println(objectCounts.motorcycleCount);
  Serial.println();
}

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);

  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Initialize ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Register the receive callback function
  esp_now_set_self_role(ESP_NOW_ROLE_SLAVE);
  esp_now_register_recv_cb(OnDataRecv);
}

void loop() {
  // The receiver continuously listens for incoming data
}
