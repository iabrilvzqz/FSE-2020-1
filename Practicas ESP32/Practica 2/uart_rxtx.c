/*	Fundamentos de Sistemas Embebidos
	PRACTICA 2 ESP32 UART

	Nombres:
		Arellano Yeo Nomar Alberto
		Hernández García Luis Angel
		Vázquez Sánchez Ilse Abril
*/
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_log.h"
#include "driver/uart.h"
#include "string.h"
#include "driver/gpio.h"


#define led 23
#define boton 4

static const int RX_BUF_SIZE = 1024;

void init(void) {
	const uart_config_t uart_config = {
		.baud_rate = 115200,
		.data_bits = UART_DATA_8_BITS,
		.parity = UART_PARITY_DISABLE,
		.stop_bits = UART_STOP_BITS_1,
		.flow_ctrl = UART_HW_FLOWCTRL_DISABLE
	};
	// Usamos el UART 0
	uart_param_config(UART_NUM_0, &uart_config);
	// Nose usa un buffer para enviar los datos
	uart_driver_install(UART_NUM_0, RX_BUF_SIZE * 2, 0, 0, NULL, 0);

	 gpio_pad_select_gpio(led);
	/* Configurando el GPIO como pin de salida */
	gpio_set_direction(led, GPIO_MODE_OUTPUT);
}

int sendData(const char* logName, const char* data)
{
	const int len = strlen(data);
	const int txBytes = uart_write_bytes(UART_NUM_0, data, len);
	ESP_LOGI(logName, "Wrote %d bytes", txBytes);
	return txBytes;
}

static void tx_task(void *arg)
{
	static const char *TX_TASK_TAG = "TX_TASK";
	esp_log_level_set(TX_TASK_TAG, ESP_LOG_INFO);
	while (1) {
		if (gpio_get_level(boton) == 1) {
			sendData(TX_TASK_TAG, "Boton oprimido");
		} else {
			sendData(TX_TASK_TAG, "Boton no oprimido");
		}
		vTaskDelay(1000 / portTICK_PERIOD_MS);
	}
}

static void rx_task(void *arg)
{
	static const char *RX_TASK_TAG = "RX_TASK";
	esp_log_level_set(RX_TASK_TAG, ESP_LOG_INFO);
	uint8_t* data = (uint8_t*) malloc(RX_BUF_SIZE+1);
	while (1) {
		const int rxBytes = uart_read_bytes(UART_NUM_0, data, RX_BUF_SIZE, 1000 / portTICK_RATE_MS);
		if(rxBytes > 0) {
			data[rxBytes] = 0;
			ESP_LOGI(RX_TASK_TAG, "Read %d bytes: '%s'", rxBytes, data);
			ESP_LOG_BUFFER_HEXDUMP(RX_TASK_TAG, data, rxBytes, ESP_LOG_INFO);
			if(strcmp("a", (char*)data) == 0){
				gpio_set_level(led, 1);
			} else if(strcmp("b", (char*)data) == 0) {
				gpio_set_level(led, 0);
			}
		}
	}
	free(data);
}

void app_main(void)
{
	init();
	xTaskCreate(rx_task, "uart_rx_task", 1024*2, NULL, configMAX_PRIORITIES, NULL);
	xTaskCreate(tx_task, "uart_tx_task", 1024*2, NULL, configMAX_PRIORITIES-1, NULL);
}
