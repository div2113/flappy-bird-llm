import pygame
import numpy as np

# Sample rate — standard audio quality
SAMPLE_RATE = 44100

def make_sound(frequency, duration, volume=0.3,
               wave='sine', fade=True):
    """Generate a sound from scratch using math."""
    frames = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, frames, False)

    # Wave types
    if wave == 'sine':
        wave_data = np.sin(2 * np.pi * frequency * t)
    elif wave == 'square':
        wave_data = np.sign(np.sin(2 * np.pi * frequency * t))
    elif wave == 'sawtooth':
        wave_data = 2 * (t * frequency - np.floor(t * frequency + 0.5))

    # Fade out to avoid clicking
    if fade:
        fade_len = int(frames * 0.3)
        fade_out = np.linspace(1, 0, fade_len)
        wave_data[-fade_len:] *= fade_out

    # Scale to volume
    wave_data = (wave_data * volume * 32767).astype(np.int16)

    # Stereo (duplicate channel)
    stereo = np.column_stack([wave_data, wave_data])
    sound = pygame.sndarray.make_sound(stereo)
    return sound


def make_flap_sound():
    """Quick upward swoosh."""
    frames = int(SAMPLE_RATE * 0.12)
    t = np.linspace(0, 0.12, frames, False)
    # Frequency rises quickly = swoosh feel
    freq = np.linspace(300, 800, frames)
    wave = np.sin(2 * np.pi * freq * t)
    fade = np.linspace(1, 0, frames)
    wave *= fade * 0.4
    wave = (wave * 32767).astype(np.int16)
    stereo = np.column_stack([wave, wave])
    return pygame.sndarray.make_sound(stereo)


def make_score_sound():
    """Happy little ding."""
    s1 = make_sound(880, 0.08, volume=0.25, wave='sine')
    return s1


def make_hit_sound():
    """Thud + crunch."""
    frames = int(SAMPLE_RATE * 0.25)
    t = np.linspace(0, 0.25, frames, False)
    # Low noise thud
    noise = np.random.uniform(-1, 1, frames)
    tone  = np.sin(2 * np.pi * 120 * t)
    wave  = (noise * 0.6 + tone * 0.4)
    fade  = np.linspace(1, 0, frames)
    wave *= fade * 0.5
    wave  = (wave * 32767).astype(np.int16)
    stereo = np.column_stack([wave, wave])
    return pygame.sndarray.make_sound(stereo)


def make_die_sound():
    """Falling whistle — game over feel."""
    frames = int(SAMPLE_RATE * 0.4)
    t = np.linspace(0, 0.4, frames, False)
    # Frequency drops = falling feel
    freq = np.linspace(600, 150, frames)
    wave = np.sin(2 * np.pi * freq * t)
    fade = np.linspace(1, 0, frames)
    wave *= fade * 0.4
    wave = (wave * 32767).astype(np.int16)
    stereo = np.column_stack([wave, wave])
    return pygame.sndarray.make_sound(stereo)


def make_best_sound():
    """Celebration jingle for new high score."""
    notes = [523, 659, 784, 1047]   # C E G C (major chord)
    sounds = []
    for note in notes:
        sounds.append(make_sound(note, 0.1, volume=0.2))
    return sounds


class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16,
                          channels=2, buffer=512)
        print("🔊 Generating sounds...")
        self.flap  = make_flap_sound()
        self.score = make_score_sound()
        self.hit   = make_hit_sound()
        self.die   = make_die_sound()
        self.best  = make_best_sound()
        print("✅ Sounds ready!")

    def play_flap(self):
        self.flap.play()

    def play_score(self):
        self.score.play()

    def play_hit(self):
        self.hit.play()
        pygame.time.delay(80)
        self.die.play()

    def play_best(self):
        # Play celebration notes with small delay between each
        for i, s in enumerate(self.best):
            pygame.time.set_timer(pygame.USEREVENT + i, (i+1) * 120)
            s.play()