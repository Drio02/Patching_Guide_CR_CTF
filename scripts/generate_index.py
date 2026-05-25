#!/usr/bin/env python3
"""Genera el índice de vulnerabilidades en el README.md.

Detecta overview.md y parche.md sin importar la capitalización. Con --normalize
renombra esos archivos a minúsculas para mantener consistencia en el repo.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VULNS_DIR = ROOT / "vulns"
README = ROOT / "README.md"

START = "<!-- AUTO-INDEX:START -->"
END = "<!-- AUTO-INDEX:END -->"

DOC_FILES = ("overview.md", "parche.md")


def find_ci(directory: Path, target_name: str) -> Path | None:
    """Busca un archivo en directory ignorando mayúsculas/minúsculas."""
    if not directory.is_dir():
        return None
    target_lower = target_name.lower()
    for entry in directory.iterdir():
        if entry.is_file() and entry.name.lower() == target_lower:
            return entry
    return None


def normalize_filename(path: Path) -> Path:
    """Renombra el archivo a minúsculas si no lo está. Retorna el path final."""
    if path.name == path.name.lower():
        return path
    new_path = path.with_name(path.name.lower())
    if new_path.exists() and new_path.resolve() != path.resolve():
        print(
            f"  ⚠ Conflicto: ya existe {new_path.name}, no se renombra {path.name}",
            file=sys.stderr,
        )
        return path
    # Rename en dos pasos: necesario en filesystems case-insensitive
    tmp = path.with_name(f".__tmp__{path.name}")
    path.rename(tmp)
    tmp.rename(new_path)
    print(f"  ✓ Renombrado: {path.relative_to(ROOT)} → {new_path.name}")
    return new_path


def get_title(overview: Path | None, fallback: str) -> str:
    """Extrae el primer '# Título' del overview, o usa el fallback."""
    if overview is None or not overview.exists():
        return fallback
    for line in overview.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#\s+(.+)", line.strip())
        if match:
            return match.group(1).strip()
    return fallback


def get_languages(samples: Path) -> list[str]:
    if not samples.is_dir():
        return []
    return sorted(
        d.name for d in samples.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


def build_table(normalize: bool = False) -> str:
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
        # Buscar cada doc sin importar capitalización; normalizar si se pidió
        docs: dict[str, Path | None] = {}
        for fname in DOC_FILES:
            found = find_ci(vuln, fname)
            if found and normalize:
                found = normalize_filename(found)
            docs[fname] = found

        title = get_title(docs["overview.md"], vuln.name)
        langs = get_languages(vuln / "samples")
        if langs:
            langs_str = ", ".join(f"[{lang}]({rel}/samples/{lang}/)" for lang in langs)
        else:
            langs_str = "—"
        rel = vuln.relative_to(ROOT).as_posix()

        docs_links = []
        if docs["overview.md"]:
            docs_links.append(f"[Overview]({rel}/{docs['overview.md'].name})")
        if docs["parche.md"]:
            docs_links.append(f"[Parche]({rel}/{docs['parche.md'].name})")
        docs_str = " · ".join(docs_links) if docs_links else "—"

        rows.append(f"| {title} | {langs_str} | {docs_str} |")
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--normalize",
        action="store_true",
        help="Renombra overview.md y parche.md a minúsculas si tienen otra capitalización.",
    )
    args = parser.parse_args()

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

    table = build_table(normalize=args.normalize)
    new_block = (
        f"{START}\n"
        f"<!-- Esta sección se genera automáticamente. No la edites a mano. -->\n\n"
        f"{table}\n\n"
        f"{END}"
    )
    new_content = pattern.sub(new_block, content)

    if new_content == content:
        print("Sin cambios en el índice.")
        return 0

    README.write_text(new_content, encoding="utf-8")
    print(f"Índice actualizado ({len(table.splitlines()) - 2} entradas).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())