# Waveshare 3.6inch e-Paper HAT+ Schematic Replication

## Overview

This project is a replication of the **Waveshare 3.6inch e-Paper HAT+** schematics, originally documented in `3.6inch_e-Paper_HAT+_Schematics.pdf`. The goal is to recreate the schematic faithfully in **KiCad** for learning, modification, or custom PCB development purposes.

The original hardware is a 600×400 pixel e-paper display HAT designed for the Raspberry Pi, manufactured by Waveshare.

---

## Source Reference

- **Original schematic:** `3.6inch_e-Paper_HAT+_Schematics.pdf`
- **Manufacturer:** Waveshare
- **Product:** 3.6inch e-Paper HAT+ (600×400 pixels)
- **Interface:** SPI (3-line or 4-line, selectable via BS0/BS1)

---

## Project Structure

```
├── README.md
├── schematic/
│   ├── epaper_hat.kicad_sch       # Main KiCad schematic file
│   └── epaper_hat.kicad_pro       # KiCad project file
├── library/
│   ├── custom_symbols.kicad_sym   # Custom symbols (FPC connector, etc.)
│   └── custom_footprints.pretty/  # Custom footprints if needed
├── bom/
│   └── bom.csv                    # Bill of materials
└── reference/
    └── 3.6inch_e-Paper_HAT+_Schematics.pdf
```

---

## Circuit Blocks

The schematic consists of the following main sections:

### 1. FPC Connector (J1)
- 50-pin, 0.5mm pitch FPC connector
- Connects to the e-paper display panel
- Includes decoupling capacitors on all power pins

### 2. Boost Converter (Top)
- MOSFET: BSS138LT1G (N-channel)
- Inductor: L1 10uH
- Diodes: D1, D2, D3 MBR0530 (Schottky)
- Generates VPH, VGL, VGH rails for the display

### 3. Boost Converter (Bottom)
- MOSFET: SI2301CDS-T1-E3 (P-channel)
- Inductor: L2 10uH
- Diode: D4 MBR0530
- Generates VPC rail

### 4. Power Switch (Q3/Q4)
- Q3: SI2301CDS-T1-E3 (P-channel MOSFET) — main power switch
- Q4: SS8050 (NPN BJT) — gate driver for Q3
- Controlled by PWR signal from Raspberry Pi

### 5. Voltage Regulator (U3)
- RT9193-33PB LDO regulator
- Input: VCC from Raspberry Pi 5V
- Output: 3V3_OUT (3.3V) for display logic

### 6. Level Shifter (U1)
- TXB0108PWR 8-bit bidirectional level shifter
- Translates SPI signals between Raspberry Pi (3.3V) and display logic

### 7. EEPROM (U2)
- CAT24C32 32K I2C EEPROM
- Stores HAT identification data for Raspberry Pi

### 8. Raspberry Pi GPIO Connector (P1)
- Standard 40-pin Raspberry Pi HAT connector
- Carries SPI, I2C, power, and control signals

### 9. SPI Interface Connector (P2)
- 9-pin connector for direct SPI control
- Alternative to Raspberry Pi connection

### 10. BS0/BS1 Jumper (J2)
- Selects SPI interface mode
- 4 modes supported via BS0 and BS1 combination

---

## SPI Mode Selection

| Type | BS1 | BS0 | Mode |
|------|-----|-----|------|
| 1 | 0 | 0 | 4-wire SPI |
| 2 | 0 | 1 | 3-wire SPI |
| 3 | 1 | 0 | Standard 4-wire SPI |
| 4 | 1 | 1 | SPI/Dual SPI/Quad SPI |

---

## TODO

- [ ] **Double check initial schematics** — verify all connections, net labels, and pin mappings against the original PDF before proceeding further
- [ ] **Raspberry Pi circuit integration** — the Pi GPIO connector (P1) and associated signal routing is not yet included in the KiCad schematic
- [ ] **Assign footprints to all components** — every symbol needs a verified footprint before PCB conversion is possible
- [ ] **PCB layout** — no board layout has been started yet; component placement and trace routing still needed
- [ ] **Test on real hardware** — validate the completed board against a physical microprocessor and e-paper display to confirm correct operation
- [ ] **Review unnecessary components** — some components from the original Waveshare driver circuit may not be needed depending on the target use case; evaluate what can be simplified or removed

---

## License

This replication is for educational and personal use only. All original design rights belong to **Waveshare Electronics**.
