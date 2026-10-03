# Paintbrush ARTSEY 0.9 beta

Only the left-handed Paintbrush layout changes. Other boards keep ARDUX. The [ARTSEY site](https://github.com/artseyio/artsey/blob/84404d5188e9a9401322e318de2f68754928215f/docs/index.md) still labels 0.8.1 as current and 0.9 as beta. The beta announcement dates to February 2024, with source corrections through March 2024.

The port follows the latest [0.9 combos](https://github.com/artseyio/qmk-artsey/blob/c9a86ac6bd7f6b68a1be8f7895445a94207005db/Firmware%20Files/Version%200.9.0/Left%20Hand/combos.txt) and [left-hand keys](https://github.com/artseyio/qmk-artsey/blob/c9a86ac6bd7f6b68a1be8f7895445a94207005db/Firmware%20Files/Version%200.9.0/Left%20Hand/key.txt):

- Period moves to A+I, comma to A+Y, and apostrophe to R+Y. Question mark gets S+O. T+I stays `!`, and A+O stays `/`.
- The latest left-hand beta maps Backspace to R+I and forward Delete to R+E. These differ from the right-hand beta.
- Control S+E, Command S+Y, and Option S+I become toggles. Repeat the chord to release it. One-shot Shift remains E+R+T+S, but activates lazily to avoid interfering with latched Shift.
- Latched Shift moves to A+Y+I+O, replacing Caps Lock. All eight keys release latched modifiers and return to base. Pending one-shot Shift retains its normal timeout; the panic macro does not reset ZMK's internal sticky-key state.
- Hold E for punctuation. A/R/T/S produce hash, grave accent, semicolon, and backslash. Y/I/O produce at sign, minus, and equals.
- Hold A for brackets. R/Y produce opening/closing parentheses, T/I produce square brackets, and S/O produce braces.
- Hold O for media. A/R/T/I control play/pause, mute, volume up, and volume down. E is next track; Y is previous track.

Digits, timings, mouse/navigation controls, six Bluetooth profiles, and the custom disconnect keys stay unchanged. Global utility chords and HID keypresses are retained rather than copying QMK's layer restrictions and `SEND_STRING` implementation. Symbol descriptions assume a US host layout. ZMK's modifier-off behavior can log an attempted release when a modifier is already off; it does not turn that modifier on.

## Pair with Apple devices

Use base-letter names for chords. The left-hand rows are `S T R A` and `O I Y E`. Suggested profiles are A/index 0 for Mac, Y/index 4 for iPhone, and I/index 5 for iPad. These are not a record of your existing pairings.

1. Unplug USB. Tap A+E+S+O, tap the device's profile key, then tap A+E+S+O again.
2. For a new pairing, use an empty profile. On Mac, open System Settings > Bluetooth and connect to **The Paintbrush**. On iPad/iPhone, use Settings > Bluetooth.
3. To repair a pairing, first forget the keyboard on the Apple device. Select its profile on the keyboard, then tap R+T+Y+I to clear that profile's bond. Pair again. This deletes only the selected bond.

To restore an iPhone/iPad's on-screen keyboard, select another profile first. While on the Bluetooth layer, S disconnects index 4 and O disconnects index 5 without forgetting them. Disconnecting the active profile causes it to reconnect immediately. Normal firmware flashes preserve bonds. These instructions assume the installed firmware matches this config. See [ZMK's Bluetooth documentation at the pinned revision](https://github.com/zmkfirmware/zmk/blob/241ff39556b3685c9344c4c22fd9a655af8eb3ba/docs/docs/keymaps/behaviors/bluetooth.md).
