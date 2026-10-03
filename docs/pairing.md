# Pair the Paintbrush with Apple devices

These instructions match `the_paintbrush_left.keymap`, including its custom iPhone and iPad disconnect keys. The Bluetooth controls are unchanged by the ARTSEY 0.9 port. They also apply to the previous firmware built from this repo's current main branch. An older firmware already on your keyboard may differ.

Your left-handed base layout is:

```text
	S T R A
	O I Y E
```

Use the base-letter names below even while another layer is active. Press chord keys together, within the configured 175 ms combo window.

## Choose a profile

The keyboard has six Bluetooth profiles. Assign a different profile to each device. The following assignments match the profiles targeted by your existing disconnect keys, but they are recommendations, not a record of your current pairings.

| Base key on Bluetooth layer | ZMK profile index | Suggested device |
| --- | --- | --- |
| A | 0 | MacBook Pro |
| R | 1 | Spare |
| T | 2 | Spare |
| E | 3 | Spare |
| Y | 4 | iPhone |
| I | 5 | iPad |

1. Turn on the keyboard.
2. Unplug its USB cable so USB output preference cannot hide Bluetooth typing.
3. Tap A+E+S+O to enter the Bluetooth selection layer.
4. Tap the profile key for the device.
5. Tap A+E+S+O again to leave the Bluetooth layer.

Do not hold the profile key. A tap selects the profile. Selecting an empty profile makes the keyboard available for pairing. Selecting a bonded profile reconnects to its existing device instead.

## Pair for the first time

First select an unused profile with the steps above.

### MacBook Pro

1. Open **System Settings > Bluetooth**.
2. Find **The Paintbrush** under nearby devices.
3. Click **Connect**.
4. Open a text editor and test typing.

On older macOS releases, use **System Preferences > Bluetooth** instead.

### iPad or iPhone

1. Open **Settings > Bluetooth**.
2. Find **The Paintbrush** under **Other Devices**.
3. Tap the keyboard's name.
4. Open Notes and test typing.

## Repair a pairing

Clearing a profile deletes its bond on the keyboard. Clear only the profile for the device you are repairing, not every profile.

1. On the Apple device, forget **The Paintbrush**. On macOS, open the keyboard's Bluetooth details and choose **Forget This Device**. On iPadOS or iOS, tap the information button beside its name, then **Forget This Device**.
2. On the keyboard, enter the Bluetooth layer with A+E+S+O.
3. Tap the profile key for that device.
4. Leave the Bluetooth layer with A+E+S+O.
5. Tap R+T+Y+I together to clear the selected profile.
6. Pair again in the Apple device's Bluetooth settings.

Both sides must forget the old bond. Clearing only the keyboard can leave the host trying to reconnect with obsolete encryption keys.

A normal firmware flash preserves Bluetooth bonds. Re-pairing is usually unnecessary for a keymap-only change. If you change HID features, such as adding mouse support to firmware that did not have it, forget and re-pair to refresh the host's cached HID descriptor.

## Switch devices without pairing again

1. Tap A+E+S+O.
2. Tap A for the recommended Mac profile, Y for iPhone, or I for iPad.
3. Tap A+E+S+O again.

Only the selected profile receives keystrokes. Another device can still show the keyboard as connected.

## Restore the iPhone or iPad on-screen keyboard

Your custom Bluetooth-layer S key disconnects profile 4. Its O key disconnects profile 5. These actions preserve the bonds.

The active profile reconnects immediately if you disconnect it. Select a different profile first.

1. Enter the Bluetooth layer with A+E+S+O.
2. Select another profile, such as A for the Mac.
3. Tap S to disconnect the recommended iPhone profile, or O to disconnect the recommended iPad profile.
4. Leave the Bluetooth layer with A+E+S+O.

If your phone and tablet use different profile numbers, these disconnect keys target the wrong devices. Move their pairings to profiles 4 and 5, or change the two `BT_DISC` definitions in the keymap.

## Check a failed connection

- If the keyboard is missing from the discovery list, select an empty profile or clear the intended profile on both sides.
- If the host says connected but receives no typing, check the selected profile, leave the Bluetooth layer, and unplug USB.
- If the host still rejects the pairing, power-cycle the keyboard after clearing the bond on both sides.
- If the keyboard does not respond to these chords at all, confirm which firmware and handedness are installed. The repo does not identify your exact controller model or the firmware currently on the device.

See the [ZMK Bluetooth behavior documentation at this repo's pinned revision](https://github.com/zmkfirmware/zmk/blob/241ff39556b3685c9344c4c22fd9a655af8eb3ba/docs/docs/keymaps/behaviors/bluetooth.md) for profile persistence and disconnect behavior.
