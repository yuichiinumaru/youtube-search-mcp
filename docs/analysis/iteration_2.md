# Analysis of Iteration 2: Analytics

## Findings
- `youtube-comment-suite` is written in Java and focuses on a desktop GUI for managing comments. It's not directly compatible with our Python server, but the *logic* (grouping, filtering by keyword, date) is relevant.
- `youtube-content-management-mcp` (which I didn't successfully dump but saw the file list earlier) seems to have tools for `get_channel_metrics`.

## Implementation Strategy
1.  **Sentiment Analysis**: Use `TextBlob` (simple, no API key needed) to analyze comment text.
2.  **Metrics**:
    - Video: Engagement Ratio (Like/View), Comment Ratio.
    - Channel: Average views per video (if fetchable), Subscriber engagement.
3.  **Comments**:
    - Need a new API method `get_video_comments` in `api.py`.
    - Need a `SentimentAnalyzer` in `src/services/analytics.py`.

## New Dependency
- `textblob`

## Tools
- `get_video_analytics(video_id)`: Returns metadata + calculated metrics + sentiment summary of top comments.
- `get_channel_analytics(channel_id)`: Returns metadata + calculated metrics.
