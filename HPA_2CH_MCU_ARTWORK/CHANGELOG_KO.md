# D1 MCU ARTWORK 변경 이력

- 기존 HPA_2CH_DRAFT는 보존.
- MAX10 예약 영역과 외부 FPGA SPI/GPIO 헤더 제거. STM32 직접 RF 제어용 6핀 J5 적용.
- 5V 입력 단자를 Phoenix 5.08mm로 변경. PA 벌크 커패시터 풋프린트를 1210으로 변경.
- 6층 배선, GND/전원 Zone 충전, PA 방열 비아 및 MCU 전원/신호 탈출 비아 추가.
- ERC/DRC/연결 및 회로도 일치 최종 검사 0건.
- 제조 출력은 검토용. RF 특성/바이어스/보호/방열 및 실물 동작 미검증.
