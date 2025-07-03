$env:PYTHONPATH = "C:\Users\doug\Trae Projects\AImpact"

.\.venv\Scripts\Activate.ps1

curl -v -X POST "https://us-central1-aiplatform.googleapis.com/v1/projects/aimpact-462807/locations/us-central1/reasoningEngines/4948303702294265856:streamQuery?alt=sse" -H "Content-Type: application/json" -H "Authorization: Bearer %GCLOUD_ACCESS_TOKEN%" -d "{\"class_method\": \"stream_query\", \"input\": {\"user_id\": \"test_user\", \"message\": {\"parts\": [{\"text\": \"Hello agent, what can you do?\"}], \"role\": \"user\"}}}"