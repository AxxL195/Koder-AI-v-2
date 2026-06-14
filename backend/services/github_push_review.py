import httpx

async def push_review(ai_review:str, installation_token:str, repo_name: str, pr_number: int,head_SHA):
    headers = {
        'Authorization' : f'Bearer {installation_token}',
        'Accept' : 'application/vnd.github+json'
    }

    owner, repo = repo_name.split('/')

    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews'

    comments= []

    for issue in ai_review['issues']:
        comments.append({
            'path': issue['file_path'],
            'line' : issue['line_number'],
            'body' : f"**{issue['severity'].upper()} — {issue['category']}**\n\n{issue['comment']}"
        })

    has_critical = False

    for i in ai_review['issues']:
        if i['severity'] == 'critical':
            has_critical = True
            break

    event= 'REQUEST_CHANGES' if has_critical else 'COMMENT'

    body = {
        'commit_id': head_SHA,
        'body': f"## 🤖 AI Code Review\n\n{ai_review['summary']}",
        'event': event,
        'comments': comments
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.post(
            url,
            headers = headers,
            json=body
        )

        if response.status_code != 200:
            raise Exception(f'Failed to post review: {response.status_code} {response.text}')

        else:
            print('Review posted to GitHub ✓')
        
    
    