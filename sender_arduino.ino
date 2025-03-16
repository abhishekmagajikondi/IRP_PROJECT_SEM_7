#include <espnow.h>
#include <ESP8266WiFi.h>

// REPLACE WITH YOUR RECEIVER'S MAC ADDRESS
uint8_t broadcastAddress1[] = {0x40, 0x91, 0x51, 0x58, 0xA3, 0x21};

// Structure to hold the counts
typedef struct test_struct {
  int busCount;
  int carCount;
  int autoRickshawCount;
  int motorcycleCount;
} test_struct;

test_struct objectCounts;

void OnDataSent(uint8_t *mac_addr, uint8_t sendStatus) {
  Serial.print("Packet to: ");
  char macStr[18];
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.print(macStr);
  Serial.print(" send status:\t");
  Serial.println(sendStatus == 0 ? "Delivery Success" : "Delivery Fail");
}

void setup() {
  Serial.begin(115200);

  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Initialize ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);
  esp_now_register_send_cb(OnDataSent);

  // Register the receiver peer
  esp_now_add_peer(broadcastAddress1, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);
}

void loop() {
  if (Serial.available() > 0) {
    String receivedData = Serial.readStringUntil('\n');
    int counts[4];
    sscanf(receivedData.c_str(), "%d,%d,%d,%d", &counts[0], &counts[1], &counts[2], &counts[3]);

    objectCounts.busCount = counts[0];
    objectCounts.carCount = counts[1];
    objectCounts.autoRickshawCount = counts[2];
    objectCounts.motorcycleCount = counts[3];

    uint8_t result = esp_now_send(broadcastAddress1, (uint8_t *)&objectCounts, sizeof(test_struct));

    if (result == 0) {
      Serial.println("Data sent successfully");
    } else {
      Serial.println("Error sending the data");
    }
  }
}
