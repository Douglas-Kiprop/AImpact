$env:PYTHONPATH = "C:\Users\doug\Trae Projects\AImpact"

.\.venv\Scripts\Activate.ps1

curl -v -X POST "https://us-central1-aiplatform.googleapis.com/v1/projects/aimpact-462807/locations/us-central1/reasoningEngines/7147520471892754432:streamQuery?alt=sse" -H "Content-Type: application/json" -H "Authorization: Bearer %GCLOUD_ACCESS_TOKEN%" -d "{\"class_method\": \"stream_query\", \"input\": {\"user_id\": \"test_user\", \"message\": {\"parts\": [{\"text\": \"Hello agent, what can you do?\"}], \"role\": \"user\"}}}"

curl -v -X POST "http://127.0.0.1:8080/query-agent" ^
 -H "Content-Type: application/json" ^
 -d "{\"class_method\": \"stream_query\", \"input\": {\"user_id\": \"test_user\", \"message\": {\"parts\": [{\"text\": \"Hello agent, what can you do?\"}], \"role\": \"user\"}}}"

 gcloud run deploy aimpact-backend --source . --region us-central1 --allow-unauthenticated