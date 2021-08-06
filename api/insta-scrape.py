from instascrape import Profile

def parse_post(post):
    post.scrape(headers=headers)
    parse_post = post.to_dict()
    parse_post['dimensions'] = 0 if (('dimensions' in parse_post) or parse_post.dimensions == 'none') else parse_post.dimensions
    parse_post['tagged_users'] = 0 if (('tagged_users' in parse_post) or parse_post.tagged_users == 'none') else parse_post.tagged_users
    parse_post['caption'] = 0 if (('caption' in parse_post) or parse_post.caption == 'none') else parse_post.caption
    parse_post['comments'] = 0 if (('comments' in parse_post) or parse_post.comments == 'none') else parse_post.comments
    parse_post['likes'] = 0 if (('likes' in parse_post) or parse_post.likes == 'none') else parse_post.likes
    return parse_post

# PASTE YOUR SESSIONID HERE
SESSIONID = '40132536170%3Asbz2AcYhi81aPv%3A13'

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
"cookie":f'sessionid={SESSIONID};'}

profile = Profile('gonews_ok')
profile.scrape(headers=headers)
scraped_data = profile.to_dict()
#scraped_data['list_posts'] = list(map(parse_post,profile.get_recent_posts()))

print(profile.get_recent_posts()[0].to_dict())