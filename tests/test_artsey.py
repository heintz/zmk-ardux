#!/usr/bin/env python3
"""Build and exercise the real keymap with ZMK's native mock scanner."""

import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def exercise(hand, beta, app, regression=False):
    letters = "ARTSEYIO" if hand == "right" else "STRAOIYE"
    positions = {key: divmod(i, 4) for i, key in enumerate(letters)}
    events = []
    expected = []

    def chord(keys, code=None, page=7, hold=20, mods=0):
        for key in keys:
            row, col = positions[key]
            events.append(f"ZMK_MOCK_PRESS({row},{col},5)")
        for i, key in enumerate(keys):
            row, col = positions[key]
            delay = 250 if i == len(keys) - 1 else hold if i == 0 else 5
            events.append(f"ZMK_MOCK_RELEASE({row},{col},{delay})")
        if code is not None:
            expected.extend([(page, code, True, mods), (page, code, False, mods)])

    def toggle(keys, code, pressed):
        chord(keys)
        expected.append((7, code, pressed, 0))

    if beta:
        # Press the changed punctuation chords, not the behavior labels.
        for keys, code, mods in [("AI", 0x37, 0), ("AY", 0x36, 0), ("RY", 0x34, 0),
                                 ("SO", 0x38, 2), ("TI", 0x1E, 2), ("AO", 0x38, 0)]:
            chord(keys, code, mods=mods)

        # Command stays held across two Tabs, then the same chord releases it.
        toggle("SY", 0xE3, True)
        chord("ARTO", 0x2B)
        chord("ARTO", 0x2B)
        toggle("SY", 0xE3, False)
        toggle("SE", 0xE0, True)
        chord("A", 0x04)
        chord("R", 0x15)
        toggle("SE", 0xE0, False)
        toggle("SI", 0xE2, True)
        chord("ARTO", 0x2B)
        chord("ARTO", 0x2B)
        toggle("SI", 0xE2, False)
        toggle("AYIO", 0xE1, True)
        chord("A", 0x04)
        chord("R", 0x15)
        toggle("AYIO", 0xE1, False)

        # The one-shot Shift chord remains distinct from latched Shift.
        toggle("ERTS", 0xE1, True)
        chord("A", 0x04)
        # Sticky Shift releases after its target key's release.
        expected.append((7, 0xE1, False, 0))
        chord("R", 0x15)

        # Hold E for punctuation, A for paired brackets, O for media.
        for anchor, keys in [
            ("E", [("A", 7, 0x20), ("R", 7, 0x35), ("T", 7, 0x33),
                   ("S", 7, 0x31), ("Y", 7, 0x1F), ("I", 7, 0x2D), ("O", 7, 0x2E)]),
            ("A", [("R", 7, 0x26), ("Y", 7, 0x27), ("T", 7, 0x2F),
                   ("I", 7, 0x30), ("S", 7, 0x2F), ("O", 7, 0x30)]),
            ("O", [("A", 12, 0xCD), ("R", 12, 0xE2), ("T", 12, 0xE9),
                   ("E", 12, 0xB6 if hand == "right" else 0xB5),
                   ("Y", 12, 0xB5 if hand == "right" else 0xB6), ("I", 12, 0xEA)]),
        ]:
            row, col = positions[anchor]
            events.append(f"ZMK_MOCK_PRESS({row},{col},250)")
            for key, page, code in keys:
                mods = 2 if (anchor, key) in {("E", "A"), ("E", "Y"),
                                             ("A", "R"), ("A", "Y"), ("A", "S"), ("A", "O")} else 0
                chord(key, code, page, mods=mods)
            events.append(f"ZMK_MOCK_RELEASE({row},{col},250)")

        # Panic must release all latched modifiers and leave navigation.
        for keys, code in [("SE", 0xE0), ("SY", 0xE3), ("SI", 0xE2), ("AYIO", 0xE1)]:
            toggle(keys, code, True)
        chord("REI")
        chord("ARTSEYIO")
        expected.extend([(7, code, False, 0) for code in [0xE0, 0xE3, 0xE2, 0xE1]])
        chord("A", 0x04)
        chord("R", 0x15)
        if regression:
            # Arm one-shot Shift, then latch Shift before its timeout.
            # The latch must survive the one-shot timer expiring.
            chord("ERTS")
            chord("AYIO", hold=6000)
            expected.append((7, 0xE1, True, 0))
            chord("R", 0x15)
            toggle("AYIO", 0xE1, False)
    else:
        # An unopted-in board keeps ARDUX punctuation and Caps Lock.
        for keys, code in [("AY", 0x37), ("AI", 0x36), ("AYI", 0x34), ("AYIO", 0x39)]:
            chord(keys, code)

    shield = ROOT / f"config/boards/shields/the_paintbrush/the_paintbrush_{hand}.keymap"
    with tempfile.TemporaryDirectory(prefix=f"artsey-{hand}-") as tmp:
        config = pathlib.Path(tmp)
        (config / "native_posix_64.keymap").write_text(
            ("#define ARTSEY_09 1\n" if beta else "")
            + f'#include "{shield}"\n'
            + "#include <dt-bindings/zmk/kscan_mock.h>\n"
            # Bluetooth is not simulated. Replace only its behavior with a no-op.
            + "&bt { compatible = \"zmk,behavior-macro-two-param\"; bindings = <&none>; };\n"
            + "&kscan { columns = <4>; events = <\n"
            + "\n".join(events) + "\n>; };\n"
        )
        (config / "native_posix_64.conf").write_text(
            "CONFIG_ZMK_COMBO_MAX_COMBOS_PER_KEY=24\n"
            "CONFIG_ZMK_COMBO_MAX_KEYS_PER_COMBO=8\n"
            "CONFIG_ZMK_COMBO_MAX_PRESSED_COMBOS=8\n"
            "CONFIG_ZMK_POINTING=y\n"
        )
        build = config / "build"
        subprocess.run(["west", "build", "-s", str(app), "-d", str(build),
                        "-b", "native_posix_64", "--", f"-DZMK_CONFIG={config}",
                        "-DCONFIG_ASSERT=y"], check=True)
        output = subprocess.check_output([str(build / "zephyr/zmk.exe")], text=True)
        # Keep the complete runtime evidence in the CI artifact.
        log = ROOT / f"test-{hand}-{'beta' if beta else 'legacy'}.log"
        log.write_text(output)
        actual = [(int(page, 16), int(code, 16), state == "pressed", int(mods, 16))
                  for state, page, code, mods in re.findall(
                      r"hid_listener_keycode_(pressed|released): usage_page 0x([0-9A-Fa-f]+) keycode 0x([0-9A-Fa-f]+) implicit_mods 0x([0-9A-Fa-f]+)", output)]
        if regression:
            reports = []
            pressed = None
            for line in output.splitlines():
                match = re.search(r"hid_listener_keycode_pressed: usage_page 0x07 keycode 0x([0-9A-Fa-f]+)", line)
                if match:
                    pressed = int(match[1], 16)
                mask = re.search(r"Modifiers set to 0x([0-9A-Fa-f]+)", line)
                if mask and pressed is not None:
                    reports.append((pressed, int(mask[1], 16)))
                    pressed = None
            last_r = [mask for key, mask in reports if key == 0x15][-1]
            if last_r != 2:
                raise AssertionError(f"One-shot Shift canceled the Shift latch: R report modifiers expected 0x02, got 0x{last_r:02x}")
        if actual != expected:
            raise AssertionError(f"{hand} beta={beta}\nexpected: {expected}\nactual:   {actual}\nFull log: {log}")
        if beta:
            modifiers = re.findall(r"Modifiers set to 0x([0-9A-Fa-f]+)", output)
            if not modifiers or int(modifiers[-1], 16) != 0:
                raise AssertionError("Panic left a modifier pressed")
        print(f"PASS: {hand} {'0.9 beta' if beta else 'legacy'}, {len(actual)} HID events")


if __name__ == "__main__":
    app = pathlib.Path(sys.argv[1]).resolve()
    exercise("left", True, app)
    exercise("right", False, app)
    exercise("left", True, app, regression=True)
