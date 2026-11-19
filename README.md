# HPA 2CH — MCU only ARTWORK review

- [Download KiCad schematic + routed PCB + outputs ZIP](HPA_2CH_MCU_ARTWORK_Review.zip)
- [Download Gerber + NC Drill review ZIP](HPA_2CH_MCU_Gerber_Review.zip)
- [Open KiCad project](HPA_2CH_MCU_ARTWORK/HPA_2CH.kicad_pro)
- [PCB top preview](HPA_2CH_MCU_ARTWORK/preview/PCB_top.png)
- [Schematic PDF](HPA_2CH_MCU_ARTWORK/preview/Schematic.pdf)
- [Read limitations and fabrication requirements](HPA_2CH_MCU_ARTWORK/README_KO.md)

MAX10 reserved area/interface removed; STM32 direct control. 200×160mm, 6 layers. KiCad 9.0.2 final checks: ERC 0, DRC 0, unrouted 0, schematic parity issues 0. **Engineering review only: RF matching, PA bias, hardware protection and thermal performance are unvalidated. External PA supplies/couplers required. Not a fabrication or power-up release.**

---

# HPA 2CH initial draft

- [Download all KiCad draft files](HPA_2CH_Initial_Draft.zip)
- [Open project source](HPA_2CH_DRAFT/HPA_2CH.kicad_pro)
- [Root schematic](HPA_2CH_DRAFT/HPA_2CH.kicad_sch)
- [PCB placement](HPA_2CH_DRAFT/HPA_2CH.kicad_pcb)
- [Schematic PDF](HPA_2CH_DRAFT/preview/HPA_2CH_Schematic.pdf)

**Initial placement draft, UNROUTED, not for fabrication or power-up.** FPGA device, integrated PA supplies and directional couplers are not implemented. RF matching/bias/thermal design is unverified. See the draft README and actual ERC/DRC results.

---

# STM32 LED10 PCB

## Latest: 100 × 100 mm — Rev.B

- [Complete 100mm design ZIP](STM32_LED10_100_RevB_Design_Review.zip): KiCad, BOM, firmware, schematic PDF, previews, verification reports and change history.
- [100mm Gerber and drill ZIP](STM32_LED10_100_RevB_Gerber_Drill_Review.zip).
- [100mm PCB artwork preview](STM32_LED10_100_RevB_PCB_top.png).

PCB resized from 200×200mm to 100×100mm through component relocation and fresh routing. Component pad/drill sizes, circuit connectivity and firmware behavior are unchanged. Two copper layers retained. ERC/DRC: zero violations, zero unconnected pads, zero schematic parity issues; 38 connectivity/geometry checks and 6 sequencer logic tests passed.

## Preserved: 200 × 200 mm — Rev.A

- [Original 200mm design ZIP](STM32_LED10_Design.zip).
- [Original 200mm Gerber and drill ZIP](STM32_LED10_Gerber.zip).

## Download

Open the desired ZIP on GitHub and select **Download raw file**, or use **Code → Download ZIP** for the whole repository. Use the files marked **100mm / Rev.B** for the latest size.

**Engineering review drafts; not approved for manufacture.** Official manufacturer PDF electrical/package/stability review remains pending; no physical prototype or hardware test has been performed. See the included README and reports before fabrication.
