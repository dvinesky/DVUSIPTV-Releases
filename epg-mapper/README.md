# EPG Mapper

Open the mapper at `https://dvinesky.github.io/DVUSIPTV-Releases/epg-mapper/`. The provider channel list, current IPTV-EPG channel index, and existing GitHub mappings load automatically. Select a provider channel, select the matching IPTV-EPG channel ID, choose the EPG source, and select **Add mapping**. Repeat for each channel, then select **Download mappings.csv** and upload the complete file to `epg/mappings.csv` in GitHub.

![Visual EPG mapper instructions](images/epg-mapper-workflow.svg)

The mapper automatically preserves the mappings already stored in GitHub. Do not start with a blank CSV or upload only newly added rows, because that would remove existing mappings. After the CSV is committed, the GitHub Action generates the filtered EPG files automatically. No APK update is required.

The page deliberately does not write to GitHub automatically. A GitHub token should never be placed in a public webpage. Browser access to the remote EPG may also be blocked by CORS; downloading the file first and using the file picker avoids that limitation.
