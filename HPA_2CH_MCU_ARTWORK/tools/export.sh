#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-/tmp/stm32-kicad-config}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/tmp/stm32-kicad-cache}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-/tmp/stm32-kicad-data}"
mkdir -p "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" "$XDG_DATA_HOME" fabrication preview reports
kicad-cli sch erc HPA_2CH.kicad_sch  -o reports/erc.rpt
kicad-cli pcb drc HPA_2CH.kicad_pcb --schematic-parity  -o reports/drc.rpt
kicad-cli pcb drc HPA_2CH.kicad_pcb --schematic-parity --format json  -o reports/drc.json
kicad-cli sch export netlist HPA_2CH.kicad_sch -o reports/HPA_2CH.net
kicad-cli sch export pdf HPA_2CH.kicad_sch -o preview/Schematic.pdf
kicad-cli pcb export gerbers HPA_2CH.kicad_pcb -o fabrication/ -l F.Cu,In1.Cu,In2.Cu,In3.Cu,In4.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,Edge.Cuts --subtract-soldermask
kicad-cli pcb export drill HPA_2CH.kicad_pcb -o fabrication/ --excellon-separate-th --generate-map --map-format pdf
kicad-cli pcb export svg HPA_2CH.kicad_pcb -o preview/PCB_top.svg -l F.Cu,F.SilkS,Edge.Cuts --mode-single --page-size-mode 2 --exclude-drawing-sheet
kicad-cli pcb export svg HPA_2CH.kicad_pcb -o preview/PCB_bottom.svg -l B.Cu,B.SilkS,Edge.Cuts --mode-single --page-size-mode 2 --exclude-drawing-sheet --mirror
kicad-cli pcb export pos HPA_2CH.kicad_pcb -o fabrication/HPA_2CH_CPL.csv --format csv --units mm --side front --smd-only
