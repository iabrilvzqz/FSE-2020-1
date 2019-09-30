/* 	Materia: Fundamentos de Sistemas Embebidos
	Semestre: 2020-1
	Alumnos: 	Arellano Yeo Nomar Alberto
				Hernández García Luis Angel
				Vázquez Sánchez Ilse Abril

Descripción: Primer examen parcial. Programa para el ESP32 encargado de tomar los datos 
del sensor LM335 haciendo uso del ADC, convertir el voltaje obtenido en grados Kelvin y 
Celsius y, enviarlos por el UART para que la RPi obtena el voltaje en [mV], los grados 
Kelvin y los grados Celsius */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "driver/adc.h"
#include "driver/uart.h"
#include "esp_adc_cal.h"
#include "esp_err.h"


#define DEFAULT_VREF    3300 	
#define NO_OF_SAMPLES   64    //Multisampling

static esp_adc_cal_characteristics_t *adc_chars;
static const adc_channel_t channel = ADC_CHANNEL_6;   //GPIO34 if ADC1, GPIO14 if ADC2
static const adc_atten_t atten = ADC_ATTEN_DB_11;
static const adc_unit_t unit = ADC_UNIT_1;

static void check_efuse(void)
{
	//Check TP is burned into eFuse
	if (esp_adc_cal_check_efuse(ESP_ADC_CAL_VAL_EFUSE_TP) == ESP_OK)
	{
		printf("eFuse Two Point: Supported\n");
	}else 
	{
		printf("eFuse Two Point: NOT supported\n");
	}

	//Check Vref is burned into eFuse
	if (esp_adc_cal_check_efuse(ESP_ADC_CAL_VAL_EFUSE_VREF) == ESP_OK) {
		printf("eFuse Vref: Supported\n");
	} 
	else {
		printf("eFuse Vref: NOT supported\n");
	}
}

static void print_char_val_type(esp_adc_cal_value_t val_type)
{
	if (val_type == ESP_ADC_CAL_VAL_EFUSE_TP) {
		printf("Characterized using Two Point Value\n");
	} else if (val_type == ESP_ADC_CAL_VAL_EFUSE_VREF) {
		printf("Characterized using eFuse Vref\n");
	} else {
		printf("Characterized using Default Vref\n");
	}
}

void app_main(void)
{
	//Check if Two Point or Vref are burned into eFuse
	check_efuse();
  
	// Configure the UART2 controller
	uart_config_t uart_config2 = {
		.baud_rate = 115200,
		.data_bits = UART_DATA_8_BITS,
		.parity    = UART_PARITY_DISABLE,
		.stop_bits = UART_STOP_BITS_1,
		.flow_ctrl = UART_HW_FLOWCTRL_DISABLE
	};

	uart_param_config(UART_NUM_2, &uart_config2);
	uart_set_pin(UART_NUM_2, 17, 16, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
	uart_driver_install(UART_NUM_2, 1024, 0, 0, NULL, 0);

	//Configure ADC
	adc1_config_width(ADC_WIDTH_BIT_12);
	adc1_config_channel_atten(channel, atten);

	//Characterize ADC
	adc_chars = calloc(1, sizeof(esp_adc_cal_characteristics_t));
	esp_adc_cal_value_t val_type = esp_adc_cal_characterize(unit, atten, ADC_WIDTH_BIT_12, DEFAULT_VREF, adc_chars);
	print_char_val_type(val_type);

	char text[30], txtKelvin[12], txtCelsius[12];
	//Continuously sample ADC1
	while (1) {
		uint32_t adc_reading = 0;
		//Multisampling
		for (int i = 0; i < NO_OF_SAMPLES; i++) {
			adc_reading += adc1_get_raw((adc1_channel_t)channel);
		}
		adc_reading /= NO_OF_SAMPLES;
		
		//Convert adc_reading to voltage in mV
		uint32_t voltage = esp_adc_cal_raw_to_voltage(adc_reading, adc_chars);
		printf("Raw: %d\tVoltage: %dmV\n", adc_reading, voltage);

		sprintf(text, "%d", voltage);
		sprintf(txtKelvin, ",%.3f", voltage/10 - 0.0);
		strcat(text, txtKelvin);
		sprintf(txtCelsius, ",%.3f\n", voltage/10 - 273.15);
		strcat(text, txtCelsius);
		
		
		// Sending voltage to UART
    	uart_write_bytes(UART_NUM_2, text, strlen(text));

		vTaskDelay(pdMS_TO_TICKS(1000));
	}
}
