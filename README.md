# DVUSIPTV Releases

Public APK releases for DVUSIPTV.
DVUSIPTV Releases

Latest release: v1.2.5

v1.2.5 notes:
- Added filtered external EPG lookup by provider stream ID.
- Added off-device EPG filtering workflow so low-memory devices do not download the full source XMLTV feed.

v1.2.4 notes:
- Restored West Coast external EPG fallback on low-memory devices.
- Uses targeted, disk-backed XMLTV parsing to avoid the previous guide crash.

v1.2.3 notes:
- Prevented external XMLTV parsing on low-memory devices to avoid guide crashes.
- Low-memory devices continue using provider and API guide data.

v1.2.2 notes:
- Improved EPG fallback matching for channels with missing provider EPG IDs.
- Added support for channel-name variants such as AMC West and regional East/West feeds.
- Added West Coast schedule offset handling when only an East/base listing is available.
- Prevented duplicate external guide downloads and removed the oversized feed that could cause device memory pressure.
