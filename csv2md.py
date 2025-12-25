#!/usr/bin/env python3
import argparse
import csv
import html

def to_md_table(rows, headers):
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        cells = []
        for h in headers:
            v = r.get(h, "")
            v = v.replace("\n", " ").replace("\r", " ")
            v = v.replace("|", "\\|")
            cells.append(v)
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)

def to_details_codeblock(title, text, lang="text"):
    return f"""<details>
<summary>{html.escape(title)}</summary>

```{lang}
{text}
```

</details>"""

def main():
    ap = argparse.ArgumentParser(description="Convert CSV to Markdown-friendly output.")
    ap.add_argument("csv_path")
    ap.add_argument("--head", type=int, default=999999)
    ap.add_argument("--mode", choices=["table", "table+details_csv", "details_csv"], default="table+details_csv")
    ap.add_argument("--encoding", default="utf-8")
    args = ap.parse_args()

    with open(args.csv_path, "r", encoding=args.encoding, newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        all_rows = list(reader)

    with open(args.csv_path, "r", encoding=args.encoding, newline="") as f:
        csv_text = f.read().rstrip("\n")

    head_rows = all_rows[:args.head]
    parts = []

    if args.mode in ("table", "table+details_csv"):
        parts.append(to_md_table(head_rows, headers))
        if len(all_rows) > args.head:
            parts.append(f"\n\n> 表示は先頭 {args.head} 行のみ（全 {len(all_rows)} 行）。\n")

    if args.mode in ("details_csv", "table+details_csv"):
        parts.append(to_details_codeblock(f"全データ（CSV）を表示（{len(all_rows)} 行）", csv_text, "csv"))

    print("\n".join(parts))

if __name__ == "__main__":
    main()
