# DVUSIPTV Releases

Public APK releases for DVUSIPTV.
DVUSIPTV Releases

## External EPG mappings

Edit `epg/mappings.csv` to add or correct a mapping. The columns are:

```text
provider_stream_id,external_xmltv_id,provider_name,source
176012,CinemaxActionPacific.us,USA Cinemax Action West,us
123456,SomeCanadianChannel.ca,USA Example Canada,ca
```

The supported sources are `us`, `ca`, and `gb`, corresponding to `epg-us.xml.gz`, `epg-ca.xml.gz`, and `epg-gb.xml.gz`. The app reads the generated `epg/mappings.json` at runtime, so mapping changes do not require an APK rebuild or version update. A push to `epg/mappings.csv` automatically rebuilds the small per-channel EPG files.

Latest release: v1.3.1

Downloader APK link:
`https://dvinesky.github.io/DVUSIPTV-Releases/DVUSIPTV.apk`

v1.3.1 notes:
- Uses a direct GitHub Pages APK URL for more reliable Fire OS downloading and installation.

v1.3.0 notes:
- Refreshes stale provider and filtered EPG caches before displaying guide data.
- Prevents old cached EPG entries from hiding current programs on Android TV devices.


v1.2.9 notes:
- Updated the Android TV banner to the DVUSIPTV Premium logo.
- Updated the sign-in screen to use the DVUSIPTV Premium logo.

v1.2.8 notes:
- Preserves Favorites during app updates and same-account provider host changes.
- Protects existing Favorites from being replaced by an empty profile snapshot.
- Improves long-press Favorite actions for Nvidia Shield DPAD/Enter input.

v1.2.7 notes:
- Brightened the guide current-time marker for better visibility.
- Uses one canonical application package for updates.

v1.2.6 notes:
- Checks filtered EPG mappings before the slow provider XMLTV refresh.
- Keeps mapped external EPG results as valid guide data.

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
