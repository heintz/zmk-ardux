# ARTSEY 0.9 beta port

This repository follows ARDUX, not current ARTSEY. The left-handed Paintbrush now opts into the ARTSEY 0.9 beta layout with `#define ARTSEY_09 1` before including `ardux.dtsi`. Other shields retain their existing ARDUX layouts. Remove that definition to restore the previous Paintbrush layout.

The option supports standard eight-key layouts in either hand. It rejects `ARDUX_BIG` and `ARDUX_COLEMAK`, whose extensions are outside this port. It retains this repository's layer IDs, hold-tap and combo timings, number-layer extras, mouse support, Bluetooth profiles, and Paintbrush disconnect bindings.

## Sources and status

ARTSEY's website still labels 0.8.1 as current and 0.9.0 as beta. The beta announcement is dated February 29, 2024. The latest layout and QMK corrections in the source repositories are dated March 5, 2024. These are not a newly released stable version.

The port uses the following sources:

- [ARTSEY announcement and diagrams](https://github.com/artseyio/artsey/blob/84404d5188e9a9401322e318de2f68754928215f/docs/index.md).
- [0.9 right-hand combo definitions](https://github.com/artseyio/qmk-artsey/blob/c9a86ac6bd7f6b68a1be8f7895445a94207005db/Firmware%20Files/Version%200.9.0/Right%20Hand/combos.txt).
- [0.9 right-hand keys](https://github.com/artseyio/qmk-artsey/blob/c9a86ac6bd7f6b68a1be8f7895445a94207005db/Firmware%20Files/Version%200.9.0/Right%20Hand/key.txt).
- [0.9 left-hand keys](https://github.com/artseyio/qmk-artsey/blob/c9a86ac6bd7f6b68a1be8f7895445a94207005db/Firmware%20Files/Version%200.9.0/Left%20Hand/key.txt).
- [0.8.1 QMK combo definitions](https://github.com/artseyio/qmk-artsey/blob/c9a86ac6bd7f6b68a1be8f7895445a94207005db/Firmware%20Files/Version%200.8.1/Right%20Hand/combos.txt).

The ARTSEY website's YAML and generated Markdown still describe 0.8.1. The archived `artseyio/zmk-artsey` predates the beta. Neither supplies a ready-made ZMK 0.9 update. Current ARDUX upstream changes are separate from this ARTSEY port.

## Changes relative to this config

Chords below use the letters printed on the base layer, regardless of handedness.

| Action | Existing config | ARTSEY 0.9 beta |
| --- | --- | --- |
| Period | A+Y | A+I |
| Comma | A+I | A+Y |
| Apostrophe | A+Y+I | R+Y |
| Question mark | Hold E, then Y | S+O |
| Control | One-shot S+E | Toggle S+E |
| Command | One-shot S+Y | Toggle S+Y |
| Option | One-shot S+I | Toggle S+I |
| Latched Shift | R+Y | A+Y+I+O |
| Caps Lock | A+Y+I+O | Removed in favor of latched Shift |
| Panic | None | All eight keys release latched modifiers and return to base |

Period and comma were already assigned to A+I and A+Y in the newer QMK 0.8.1 source. Swapping them here corrects this repository's older ZMK mapping as well as aligning it with 0.9.

The one-shot Shift chord E+R+T+S remains unchanged. Letters, Enter, Backspace, Delete, Tab, Escape, Space, the digit layout, and the navigation and mouse activation chords remain unchanged.

Holding E still opens punctuation. In base-letter coordinates, A becomes `#`, R becomes grave accent, S becomes backslash, and Y becomes `@`. T stays semicolon, I stays minus, and O stays equals. `!` remains T+I, and `/` remains A+O.

Holding A still opens brackets. R and Y now produce opening and closing parentheses. T and I produce opening and closing square brackets. S and O produce opening and closing braces. The left-handed bracket arrangement follows the latest left-hand QMK source, rather than mirroring the older ARDUX arrangement.

Holding O opens the beta media layer. A is play/pause, R is mute, T is volume up, and I is volume down. On the left-handed layout, E is next track and Y is previous track. On the right-handed layout, E is previous track and Y is next track. This handedness difference follows upstream's latest key definitions. Insert, Print Screen, and the custom-layer right Shift are no longer on that layer.

## ZMK behavior choices

QMK 0.9 implements Control, GUI, Alt, and latched Shift with modifier toggles, not one-shot modifiers. This port uses ZMK `&kt`. Tap a modifier chord again to release it. For Command-Tab, tap S+Y, tap Tab as often as needed, then tap S+Y again.

The eight-key panic macro uses ZMK key-toggle behaviors in `off` mode and `&to 0`. It releases the four left modifiers used by the beta chords. It does not toggle them blindly, reset the MCU, clear Bluetooth bonds, or send Caps Lock. ZMK can log an attempted release of a modifier that was already off. This has no effect on the HID state. Pending one-shot Shift can still expire on its normal timeout. Unlike a reboot, this macro does not reset every behavior's internal state.

The existing global availability of utility and modifier chords is retained, including in the Bluetooth layer. QMK's implementation limits some chords to base, navigation, and mouse. Retaining global availability avoids removing this config's existing shortcuts.

QMK uses `SEND_STRING` for many outputs. This port retains ZMK HID keypresses so modifiers and host keyboard layouts behave as they do elsewhere in this config. Symbol descriptions assume a US host keyboard layout.

## Verification

The Build workflow compiles the repository's firmware matrix. Branch and PR builds no longer publish releases labeled as `main` firmware.

The Test ARTSEY workflow builds and runs actual ZMK keymaps with its native mock scanner. It checks the changed punctuation, modifier toggles across repeated keypresses, one-shot Shift, held punctuation, brackets, media keys, panic, and unchanged legacy right-hand mappings. It compares emitted HID keycode events and implicit modifiers against literal expected results. Bluetooth is replaced with a no-op in the native test only. Real firmware builds retain the actual Bluetooth behavior.

To run the behavioral checks in a Linux ZMK development workspace with this manifest's pinned dependencies, run:

```sh
	python3 tests/test_artsey.py /path/to/zmk/app
```

Native tests do not verify radio pairing, OLED output, or physical combo timing. Before flashing, identify the controller fitted to your Paintbrush. Then test typing, Command-Tab, latched Shift, panic, and each device connection on the hardware. Do not choose a firmware artifact based only on the shield name.

See [Pair the Paintbrush with Apple devices](pairing.md) for the unchanged Bluetooth controls.
