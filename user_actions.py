from pymongo import MongoClient
from config import mongo_url, db_name, collections


def show_insta_actions():
    client = MongoClient(mongo_url)
    mg_db = client[db_name]

    collection_follows = mg_db[collections['follows']]
    collection_posts = mg_db[collections['posts']]
    collection_comments = mg_db[collections['comments']]
    collection_likes = mg_db[collections['likes']]
    users = collection_follows.find()

    for user in users:
        user_nick = user.get('user')[0]

        follows = user.get('follows')[0].get('edges')
        if len(follows):
            for f_itm in follows:
                follow_id = f_itm.get('node').get('id')
                posts_res = collection_posts.find({'follow_id': follow_id})

                for posts_doc in posts_res:
                    posts = posts_doc.get('posts')[0].get('edges')
                    if len(posts):
                        for p_itm in posts:
                            p_shortcode = p_itm.get('node').get('shortcode')
                            comments_res = collection_comments.find(
                                {'post_shortcode': p_shortcode, 'comments.edges.node.username': user_nick})
                            likes_res = collection_likes.find(
                                {'post_shortcode': p_shortcode, 'likes.edges.node.username': user_nick})

                            for c_itm in comments_res:
                                comments = c_itm.get('comments')[0].get('edges')
                                for comment in comments:
                                    if comment.get('node').get('username') == user_nick:
                                        print(f'{user_nick} в посте с shortcode={p_shortcode} пользователя {follow_id} \
оставил коментарий: {comment.get("node").get("username")}')

                            for l_itm in likes_res:
                                likes = l_itm.get('likes')[0].get('edges')
                                for like in likes:
                                    if like.get('node').get('username') == user_nick:
                                        print(f'{user_nick} в посте с shortcode={p_shortcode} пользователя {follow_id} \
поставил лайк')