"""Colour palettes (light / dark × accent) and small colour helpers. No Flet imports."""
from __future__ import annotations

# accent name -> (light primary, dark primary)
ACCENTS: dict[str, tuple[str, str]] = {
    "sage": ("#5B8A72", "#86B79F"),
    "sky": ("#4F7FA8", "#86B1D6"),
    "rose": ("#B4607A", "#D993AB"),
    "sand": ("#B07E48", "#D8AE7A"),
    "lavender": ("#7664A8", "#A898D4"),
}
ACCENT_NAMES: dict[str, tuple[str, str]] = {
    "sage": ("سبز", "Sage"),
    "sky": ("آبی", "Sky"),
    "rose": ("گلبهی", "Rose"),
    "sand": ("شنی", "Sand"),
    "lavender": ("یاسی", "Lavender"),
}

_LIGHT = dict(
    bg="#F5F4EF", surface="#FFFFFF", surface2="#EEECE5", border="#E4E1D8",
    text="#22282B", muted="#687074", faint="#9AA1A4", on_accent="#FFFFFF",
    good="#4F8A68", warn="#C99A45", bad="#C2675F", shadow="#18222828", scrim="#66000000",
    island="#1B2326", island_text="#F3F6F4", island_dim="#8C989B", island_line="#2E3A3E",
)
_DARK = dict(
    bg="#111517", surface="#1A2023", surface2="#232B2F", border="#2C3539",
    text="#E9EEEC", muted="#A2ADAA", faint="#6F7B78", on_accent="#0F1A15",
    good="#86B79F", warn="#E2BC76", bad="#E08A82", shadow="#66000000", scrim="#AA000000",
    island="#0A0D0E", island_text="#F3F6F4", island_dim="#7F8B8E", island_line="#2A3236",
)


def _rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")[:6]
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def mix(a: str, b: str, t: float) -> str:
    """Blend colour `a` over `b` with weight t (0..1 of `a`)."""
    (r1, g1, b1), (r2, g2, b2) = _rgb(a), _rgb(b)
    r, g, bl = (round(x * t + y * (1 - t)) for x, y in ((r1, r2), (g1, g2), (b1, b2)))
    return f"#{r:02X}{g:02X}{bl:02X}"


def palette(accent: str, dark: bool) -> dict[str, str]:
    key = accent if accent in ACCENTS else "sage"
    base = dict(_DARK if dark else _LIGHT)
    surface = base["surface"]
    k = 0.22 if dark else 0.14
    pal = dict(base)
    primary = ACCENTS[key][1 if dark else 0]
    pal["accent"] = primary
    pal["accent_soft"] = mix(primary, surface, k)
    pal["accent_strong"] = mix(primary, "#FFFFFF", 0.85) if dark else mix(primary, "#000000", 0.78)
    for name, (lt, dk) in ACCENTS.items():
        fg = dk if dark else lt
        pal[f"t_{name}"] = fg
        pal[f"t_{name}_soft"] = mix(fg, surface, k)
    for tone in ("good", "warn", "bad"):
        pal[f"{tone}_soft"] = mix(pal[tone], surface, k)
    pal["t_good"], pal["t_good_soft"] = pal["good"], pal["good_soft"]
    pal["t_warn"], pal["t_warn_soft"] = pal["warn"], pal["warn_soft"]
    pal["t_bad"], pal["t_bad_soft"] = pal["bad"], pal["bad_soft"]
    pal["t_accent"], pal["t_accent_soft"] = pal["accent"], pal["accent_soft"]
    # hero gradient: the accent drifting towards a calm blue
    blue = ACCENTS["sky"][1 if dark else 0]
    pal["hero_a"] = primary
    pal["hero_b"] = mix(primary, blue, 0.45)
    pal["glass"] = "#2EFFFFFF" if not dark else "#26000000"  # translucent chip on top of the hero
    return pal


def tone(pal: dict[str, str], name: str) -> tuple[str, str]:
    """(foreground, soft background) for a tone name: accent, sage, sky, rose, sand, lavender, good, warn, bad."""
    return pal.get(f"t_{name}", pal["accent"]), pal.get(f"t_{name}_soft", pal["accent_soft"])


def energy_color(score: int | float | None, dark: bool = False) -> str:
    """Calm red → amber → green scale for 1..10."""
    pal = _DARK if dark else _LIGHT
    if score is None:
        return pal["faint"]
    s = max(1.0, min(10.0, float(score)))
    if s <= 5.5:
        return mix(pal["warn"], pal["bad"], (s - 1) / 4.5)
    return mix(pal["good"], pal["warn"], (s - 5.5) / 4.5)
