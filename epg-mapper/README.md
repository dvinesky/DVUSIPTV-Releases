# EPG Mapper

Open `index.html` in Chrome, or publish the `epg-mapper` folder with GitHub Pages. Load `simple_channel_list.txt`, then load the current IPTV-EPG `.xml.gz` file or use the URL field. Select a provider channel; four-letter station call signs such as `WJRT` are detected automatically and used to filter and rank the IPTV-EPG matches. Select the matching IPTV-EPG channel ID, then select **Add mapping**. The **Download mappings.csv** button creates a file ready to review and commit.

The page deliberately does not write to GitHub automatically. A GitHub token should never be placed in a public webpage. Browser access to the remote EPG may also be blocked by CORS; downloading the file first and using the file picker avoids that limitation.
