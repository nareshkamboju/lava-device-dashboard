# HYD Workers — Connected Devices

Source: `shikra-FTDI-update` branch, parsed from `worker-configs/hyd-worker-*/ser2net.yaml`.

Total devices: 34 across 23 workers.

| Worker | Device (connection) | Banner / Label | TCP Port | USB Serial ID (`/dev/serial/by-id/...`) |
| --- | --- | --- | --- | --- |
| hyd-worker-01 | qcs615-adp-air-02 | QCS615 ADP AIR 02 | 7084 | `usb-FTDI_FT232R_USB_UART_AV0LHIC8-if00-port0` |
| hyd-worker-01 | glymur-hyd-04 | GLYMUR HYD 04 HYD WORKER 01 | 7112 | `usb-FTDI_ALPACA-LITE_MTP_DEBUG_BOARD_FTA7ZBL9-if00-port0` |
| hyd-worker-02 | rb8-ride-hyd-01 | RB8 RIDE HYD 01 | 7084 | `usb-FTDI_Qualcomm_AIR_8775_AI31952ZZ1-if01-port0` |
| hyd-worker-03 | lemans-hyd-01 | LeMans RIDE HYD 01 | 7084 | `usb-FTDI_Qualcomm_AIR_8775_AI319YIQFG-if01-port0` |
| hyd-worker-03 | glymur-hyd-05 | Glymur HYD 05 | 7112 | `usb-FTDI_ALPACA-LITE_MTP_DEBUG_BOARD_FTAL391Q-if00-port0` |
| hyd-worker-04 | hamoa-iot-evk-04-00 | Hamoa IOT EVK 04 IF00 | 7084 | `usb-FTDI_ALPACA-LITE_IDP8380X_HAMOA_FTANAX9S-if00-port0` |
| hyd-worker-04 | hamoa-iot-evk-04-01 | Hamoa IOT EVK 04 IF01 | 7085 | `usb-FTDI_ALPACA-LITE_IDP8380X_HAMOA_FTANAX9S-if01-port0` |
| hyd-worker-05 | rb3g2-hyd-01 | RB3 gen2 HYD 01 | 7081 | `usb-QUALCOMM_Kona_Debug_Board_Kona58NLDZ-if00-port0` |
| hyd-worker-06 | rb3g2-hyd-02 | RB3 gen2 HYD 02 | 7081 | `usb-QUALCOMM_Kona_Debug_Board_Ko3Z82MH-if00-port0` |
| hyd-worker-07 | rb8-hyd-01 | RB8 HYD 01 | 7087 | `usb-FTDI_RIDE_MICRO_4.0_FTAOBFER-if01-port0` |
| hyd-worker-08 | qcs8300-ride-hyd-01 | QCS8300 RIDE HYD 01 | 7087 | `usb-FTDI_Qualcomm_AIR_8775_AI3192TY75-if01-port0` |
| hyd-worker-09 | shikra-hyd-07 | Shikra HYD 07 | 7004 | `usb-Qcom_Shikra-Debug_UART_SHKHYD07-if00-port0` |
| hyd-worker-10 | hamoa-iot-evk-05 | Hamoa IOT EVK 05 | 7084 | `usb-FTDI_ALPACA-LITE_IDP8380X_HAMOA_FTACK5VU-if00-port0` |
| hyd-worker-11 | rb8-hyd-02 | RB8 HYD 02 | 7087 | `usb-WNC_ALPACA-LITE_FOR_RB8_IQ-9075-EVK_NNPMP51W00FF-if01-port0` |
| hyd-worker-12 | shikra-hyd-02 | Shikra HYD 02 | 7004 | `usb-Qcom_Shikra-Debug_UART_SHKHYD05-if00-port0` |
| hyd-worker-14 | qcs615-adp-air-02 | QCS615 ADP AIR 02 | 7084 | `usb-FTDI_FT232R_USB_UART_AV0LHEYH-if00-port0` |
| hyd-worker-14 | qcs8300-ride-hyd-02-0 | QCS8300 RIDE HYD 02 IF00 | 7096 | `usb-FTDI_Qualcomm_AIR_8775_AI318Z4XFK-if00-port0` |
| hyd-worker-14 | qcs8300-ride-hyd-02-1 | QCS8300 RIDE HYD 02 IF01 | 7097 | `usb-FTDI_Qualcomm_AIR_8775_AI318Z4XFK-if01-port0` |
| hyd-worker-14 | qcs8300-ride-hyd-02-2 | QCS8300 RIDE HYD 02 IF02 | 7098 | `usb-FTDI_Qualcomm_AIR_8775_AI318Z4XFK-if02-port0` |
| hyd-worker-14 | qcs8300-ride-hyd-02-3 | QCS8300 RIDE HYD 02 IF03 | 7099 | `usb-FTDI_Qualcomm_AIR_8775_AI318Z4XFK-if03-port0` |
| hyd-worker-15 | shikra-hyd-03 | Shikra HYD 03 | 7004 | `usb-Qcom_Shikra-Debug_UART_SHKHYD06-if00-port0` |
| hyd-worker-16 | shikra-hyd-04 | Shikra HYD 04 | 7004 | `usb-Qcom_Shikra-Debug_UART_SHKHYD04-if00-port0` |
| hyd-worker-17 | rb8-hyd-02 | RB8 HYD 03 | 7087 | `usb-WNC_ALPACA-LITE_FOR_RB8_IQ-9075-EVK_NNPMP51L00D7-if01-port0` |
| hyd-worker-18 | kaanapali-mtp-02 | Kaanapali MTP 02 | 7090 | `usb-FTDI_ALPACA-LITE_MTP8850_FTADO9TN-if00-port0` |
| hyd-worker-18 | pakala-hyd-03 | Pakala HYD 03 | 7091 | `usb-FTDI_ALPACA-LITE_MTP_DEBUG_BOARD_FTAFV3PP-if00-port0` |
| hyd-worker-19 | kaanapali-mtp-03 | Kaanapali MTP 03 | 7090 | `usb-FTDI_ALPACA-LITE_MTP8850_FTASSPVT-if00-port0` |
| hyd-worker-19 | pakala-hyd-02 | Pakala HYD 02 | 7091 | `usb-FTDI_ALPACA-LITE_MTP_DEBUG_BOARD_FT97DREJ-if00-port0` |
| hyd-worker-20 | glymur-hyd-03 | GLYMUR HYD 03 HYD WORKER 20 | 7110 | `usb-FTDI_ALPACA-LITE_MTP_DEBUG_BOARD_FTAEAV7M-if00-port0` |
| hyd-worker-20 | kaanapali-mtp-04 | Kaanapali MTP 04 | 7090 | `usb-FTDI_ALPACA-LITE_MTP8850_FTA7ULL1-if00-port0` |
| hyd-worker-22 | rb4-hyd-03 | RB4 HYD 03 | 7089 | `usb-WNC_ALPACA-LITE_FOR_RB8_IQ-9075-EVK_NP37P51F002D-if01-port0` |
| hyd-worker-23 | rb4-hyd-02 | RB4 HYD 02 | 7088 | `usb-WNC_ALPACA-LITE_FOR_RB8_IQ-9075-EVK_NNNUP45L0065-if01-port0` |
| hyd-worker-24 | rb4-hyd-01 | RB4 HYD 01 | 7087 | `usb-WNC_ALPACA-LITE_FOR_RB8_IQ-9075-EVK_NP37P51F003C-if01-port0` |
| hyd-worker-25 | kaanapali-mtp-07 | Kaanapali MTP 07 | 7090 | `usb-FTDI_ALPACA-LITE_MTP8850_FTADLWH0-if00-port0` |
| hyd-worker-25 | pakala-hyd-04 | Pakala HYD 04 | 7091 | `usb-FTDI_ALPACA-LITE_MTP_DEBUG_BOARD_FT8J3JX7-if00-port0` |