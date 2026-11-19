# HPA 2CH — 최초 회로도/PCB 초안 D0

**완성품·제조·통전용이 아닌 미배선 초안입니다.** KiCad에서 HPA_2CH.kicad_pro를 열면 됩니다.

- 실제 부품177개,하위 회로도8개,Net 연결 및 실제 풋프린트 배치 포함.
- 200×160mm,6개 구리층. 모든 회로도 파일을 함께 보관하십시오.
- STM32F405ZGT6 전원/Reset/Boot/Crystal/SWD,팬10채널 MOSFET PWM·Tacho,RF Driver/PA2채널,RF 샘플 검출4채널 및 NTC 회로를 포함합니다.
- FPGA 칩은 배치하지 않았습니다. MAX10 예약 영역과 외부 FPGA 연결 헤더만 있습니다.
- 통합 PA 전원 변환기와 방향성 Coupler는 미구현입니다. RF Bias/Drain은 외부 입력으로 표현했습니다.
- RF Matching·Bias·열·임피던스 검증 전입니다. RF passives의 TUNE 값은 확정 부품값이 아닙니다.
- 0R DNP 전원 링크를 임의 실장하거나 전원을 인가하지 마십시오. 제조사 회로 대조와 보호회로 보완이 필요합니다.
- PCB는 부품 배치/Net 할당 초안이며 미배선입니다. 내부 GND Zone도 미충전 상태입니다.
- KiCad9.0.2 CLI에서 파일 파싱/회로 ERC를 확인했습니다. KiCad10 실행 검증은 미수행입니다.
- reports/erc.json 및 drc.json은 실제 검사 결과입니다. 미배선으로 DRC 합격본이 아닙니다.

BOM_DRAFT.csv의 Function 열은 기능 식별자입니다. 각 실제 Reference와 DNP를 확인할 수 있습니다.
RF 라이브러리 핀을 사용했으나 제조사 PDF·S2P·Reference layout 대조가 끝난 것은 아닙니다. 출력5W 목표는 시뮬레이션/측정으로 확인되지 않았습니다.

Gerber는 의도적으로 제공하지 않습니다. 초기 편집용 소스입니다.

하드웨어 인터록·전원 시퀀스·과전류 보호·MCU 펌웨어·FPGA RTL은 이 최초 초안에 구현되지 않았습니다.
함께 포함된 심벌/풋프린트는 프로젝트 상대 경로를 사용합니다.
