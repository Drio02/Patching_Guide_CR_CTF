#!/usr/bin/env python3
"""Genera el índice de vulnerabilidades en el README.md.

Recorre vulns/, arma una tabla Markdown y la inserta entre los marcadores
AUTO-INDEX:START / AUTO-INDEX:END del README.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
VULNS_DIR = ROOT / "vulns"
README = ROOT / "README.md"

START = "<!-- AUTO-INDEX:START -->"
END = "<!-- AUTO-INDEX:END -->"


def get_title(overview: Path, fallback: str) -> str:
    """Extrae el primer '# Título' de overview.md, o usa el nombre de carpeta."""
    if not overview.exists():
        return fallback
    for line in overview.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#\s+(.+)", line.strip())
        if match:
            return match.group(1).strip()
    return fallback


def get_languages(samples: Path) -> list[str]:
    """Lista subcarpetas de samples/ (cada una es un lenguaje)."""
    if not samples.is_dir():
        return []
    return sorted(
        d.name for d in samples.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


def build_table() -> str:
    rows = [
        "| Vulnerabilidad | Lenguajes cubiertos | Docs |",
        "|---|---|---|",
    ]
    vulns = sorted(
        d for d in VULNS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith((".", "_"))
    )
    if not vulns:
        return "_Todavía no hay vulnerabilidades documentadas._"

    for vuln in vulns:
        title = get_title(vuln / "overview.md", vuln.name)
        langs = get_languages(vuln / "samples")
        langs_str = ", ".join(langs) if langs else "—"
        rel = vuln.relative_to(ROOT).as_posix()

        # Solo incluir links de archivos que efectivamente existen
        docs_links = []
        if (vuln / "overview.md").exists():
            docs_links.append(f"[Overview]({rel}/overview.md)")
        if (vuln / "parche.md").exists():
            docs_links.append(f"[Parche]({rel}/parche.md)")
        docs_str = " · ".join(docs_links) if docs_links else "—"

        rows.append(f"| {title} | {langs_str} | {docs_str} |")
    return "\n".join(rows)


def main() -> int:
    if not README.exists():
        print("ERROR: no se encontró README.md", file=sys.stderr)
        return 1

    content = README.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(START) + r".*?" + re.escape(END),
        re.DOTALL,
    )
    if not pattern.search(content):
        print(f"ERROR: marcadores {START} / {END} no están en el README.", file=sys.stderr)
        return 1

    table = build_table()
    new_block = f"{START}\n<!-- Esta sección se genera automáticamente. No la edites a mano. -->\n\n{table}\n\n{END}"
    new_content = pattern.sub(new_block, content)

    if new_content == content:
        print("Sin cambios en el índice.")
        return 0

    README.write_text(new_content, encoding="utf-8")
    print(f"Índice actualizado ({len(table.splitlines()) - 2} entradas).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())