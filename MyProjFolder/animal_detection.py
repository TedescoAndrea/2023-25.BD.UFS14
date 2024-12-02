def detect_animal_sound(sound: str) -> str:
    sound = sound.lower()
    if sound == "miao":
        return "gatto"
    elif sound == "bau":
        return "cane"
    else:
        return "suono non riconosciuto"
