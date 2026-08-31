import gzip
import csv
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree.ElementTree import iterparse

SOURCE_URL = "https://iptv-epg.org/files/epg-us.xml.gz"
ROOT = Path(__file__).resolve().parents[1]
MAPPINGS = ROOT / "epg" / "mappings.json"
MAPPINGS_CSV = ROOT / "epg" / "mappings.csv"
OUTPUT = ROOT / "epg" / "channels"
XMLTV_TIME = re.compile(r"^(\d{14})(?:\s*([+-]\d{4}|Z))?.*$")
SOURCES = {
    "us": "https://iptv-epg.org/files/epg-us.xml.gz",
    "ca": "https://iptv-epg.org/files/epg-ca.xml.gz",
    "gb": "https://iptv-epg.org/files/epg-gb.xml.gz",
}


def parse_time(value):
    match = XMLTV_TIME.match((value or "").strip())
    if not match:
        return 0
    local = datetime.strptime(match.group(1), "%Y%m%d%H%M%S")
    offset = match.group(2) or "+0000"
    if offset == "Z":
        tz = timezone.utc
    else:
        sign = 1 if offset[0] == "+" else -1
        minutes = int(offset[1:3]) * 60 + int(offset[3:5])
        tz = timezone(sign * timedelta(minutes=minutes))
    return int(local.replace(tzinfo=tz).timestamp())


def main():
    mappings = {}
    with MAPPINGS_CSV.open(newline="", encoding="utf-8") as mapping_file:
        reader = csv.DictReader(mapping_file)
        required = {"provider_stream_id", "external_xmltv_id", "provider_name", "source"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"mappings.csv must contain columns: {', '.join(sorted(required))}")
        for line_number, row in enumerate(reader, start=2):
            if None in row or any(not (row.get(column) or "").strip() for column in required):
                raise ValueError(f"Invalid mappings.csv row at line {line_number}: expected 4 populated columns")
            stream_id = row["provider_stream_id"].strip()
            if not stream_id.isdigit():
                raise ValueError(f"Invalid provider_stream_id at line {line_number}: {stream_id}")
            mappings[stream_id] = {
                "provider_name": row["provider_name"].strip(),
                "external_xmltv_id": row["external_xmltv_id"].strip(),
                "source": row["source"].strip().lower(),
            }
    MAPPINGS.write_text(
        json.dumps(dict(sorted(mappings.items(), key=lambda item: int(item[0]))), indent=2) + "\n",
        encoding="utf-8",
    )
    now = datetime.now(timezone.utc)
    start_window = int((now - timedelta(hours=12)).timestamp())
    end_window = int((now + timedelta(days=3)).timestamp())
    entries = {stream_id: [] for stream_id in mappings}

    for source_name, source_url in SOURCES.items():
        wanted = {}
        for stream_id, item in mappings.items():
            if item["source"] == source_name:
                wanted.setdefault(item["external_xmltv_id"], []).append(stream_id)
        if not wanted:
            continue
        print(f"Downloading {source_name.upper()} EPG source")
        request = Request(source_url, headers={"User-Agent": "DVUSIPTV-EPG-builder/1.0"})
        with urlopen(request, timeout=180) as response:
            with gzip.GzipFile(fileobj=response) as source:
                for event, element in iterparse(source, events=("end",)):
                    if element.tag == "programme":
                        external_id = element.attrib.get("channel", "")
                        stream_ids = wanted.get(external_id, [])
                        if stream_ids:
                            start = parse_time(element.attrib.get("start"))
                            stop = parse_time(element.attrib.get("stop"))
                            if start > 0 and stop > start and stop >= start_window and start <= end_window:
                                title = element.findtext("title", default="").strip()
                                description = element.findtext("desc", default="").strip()
                                if title:
                                    for stream_id in stream_ids:
                                        entries[stream_id].append({
                                            "id": f"filtered:{stream_id}:{start}",
                                            "epg_id": external_id,
                                            "title": title,
                                            "description": description,
                                            "metadataSource": "external_filtered",
                                            "fetchedAtMillis": int(now.timestamp() * 1000),
                                            "start_timestamp": str(start),
                                            "stop_timestamp": str(stop),
                                        })
                        element.clear()

    OUTPUT.mkdir(parents=True, exist_ok=True)
    for stream_id, programs in entries.items():
        programs.sort(key=lambda item: int(item["start_timestamp"]))
        (OUTPUT / f"{stream_id}.json").write_text(json.dumps(programs, separators=(",", ":")), encoding="utf-8")
        print(f"{stream_id}: {len(programs)} programs")


if __name__ == "__main__":
    main()
