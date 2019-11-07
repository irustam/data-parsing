# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import signals
from copy import deepcopy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from urllib.parse import urlencode, urljoin
from user_actions import show_insta_actions
from config import graphql_url, variables_base
from insta.items import InstaItemFollows, \
                        InstaItemPosts, \
                        InstaItemComments, \
                        InstaItemLikes


class InstaUsersSpider(scrapy.Spider):
    name = 'insta_users'

    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']

    def __init__(self, login, passwd, query_hash, users, *args, **kwargs):
        self.login = login
        self.passwd = passwd
        self.users = users
        self.follows = {}
        self.posts = {}
        self.comments = {}
        self.likes = {}
        self.query_hash = query_hash
        super().__init__(*args, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(InstaUsersSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self):
        print('finished')
        show_insta_actions()

    def parse(self, response: HtmlResponse):
        csrf_token = self.get_csrf_token(response)
        inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'

        yield scrapy.FormRequest(
            inst_login_link,
            method='POST',
            callback=self.parse_users,
            formdata={'username': self.login, 'password': self.passwd},
            headers={'X-CSRFToken': csrf_token}
        )
        print(csrf_token)

    def parse_users(self, response: HtmlResponse):
        j_body = json.loads(response.body)

        if j_body.get('authenticated'):
            for user in self.users:
                yield response.follow(urljoin(self.start_urls[0], user),
                                      callback=self.parse_user,
                                      cb_kwargs={'user': user}
                                      )
        #print(1)

    def parse_user(self, response: HtmlResponse, user):
        url_type = 'follows'
        scripts_body = response.xpath('//script[@type="text/javascript"]').extract()
        user_id = self.get_user_id(scripts_body)
        user_vars = deepcopy(variables_base.get(url_type))
        user_vars.update({'id': user_id})

        yield response.follow(self.make_graphql_url(user_vars, url_type),
                              callback=self.parse_follows,
                              cb_kwargs={'user_vars': user_vars, 'user': user}
                              )
        print(user_id)

    def parse_follows(self, response: HtmlResponse, user_vars, user):
        """
        Функция получает на вход распарсенный json с данными по подпискам пользователя.
        Также получает никнейм пользователя user и параметры user_vars для парсинга следующей партии подписчиков.
        Отсюда начинаем парсить посты пользователей, на которых подписан user.
        """
        data = json.loads(response.body)
        users_follows = data['data']['user']['edge_follow']['edges']

        if self.follows.get(user):
            self.follows[user]['edges'].extend(users_follows)
        else:
            self.follows[user] = {'edges': users_follows}

        if data['data']['user']['edge_follow']['page_info']['has_next_page']:
            url_type = 'follows'
            user_vars.update({'after': data['data']['user']['edge_follow']['page_info']['end_cursor']})
            next_page = self.make_graphql_url(user_vars, url_type)
            yield response.follow(next_page,
                                  callback=self.parse_follows,
                                  cb_kwargs={'user_vars': user_vars, 'user': user}
                                  )
        else:
            #Здесь отправляем все подписки пользователя в монго
            item = ItemLoader(InstaItemFollows(), response)
            item.add_value('user', user)
            item.add_value('follows', self.follows[user])
            print('send follows to mongo')
            yield item.load_item()

        if len(users_follows):
            for itm in users_follows:
                url_type = 'posts'
                post_vars = deepcopy(variables_base.get(url_type))
                follow_id = itm['node']['id']

                post_vars.update({'id': follow_id})
                next_page = self.make_graphql_url(post_vars, url_type)
                yield response.follow(next_page,
                                      callback=self.parse_user_posts,
                                      cb_kwargs={'post_vars': post_vars, 'follow_id': follow_id}
                                      )
                print(follow_id)

        print(user)

    def parse_user_posts(self, response: HtmlResponse, post_vars, follow_id):
        """
        Функция получает на вход распарсенный json с постами пользователя, на которого подписан user.
        Также получает никнейм пользователя user и параметры post_vars для парсинга следующей партии постов,
        если их меньше 10.
        Отсюда начинаем парсить комменты и лайки на посты пользователей, на которых подписан user.
        """
        data = json.loads(response.body)
        posts = data['data']['user']['edge_owner_to_timeline_media']['edges']

        if self.posts.get(follow_id):
            self.posts[follow_id]['edges'].extend(posts)
        else:
            self.posts[follow_id] = {'edges': posts}

        if len(posts):
            for itm in posts:
                post_shortcode = itm['node']['shortcode']

                if itm['node']['edge_media_to_comment']['count']:
                    url_type = 'comments'
                    comments_vars = deepcopy(variables_base.get(url_type))
                    comments_vars.update({'shortcode': post_shortcode})
                    next_page_comment = self.make_graphql_url(comments_vars, url_type)
                    yield response.follow(next_page_comment,
                                          callback=self.parse_post_comments,
                                          cb_kwargs={'comments_vars': comments_vars, 'post_shortcode': post_shortcode}
                                          )

                if itm['node']['edge_media_preview_like']['count']:
                    url_type = 'likes'
                    likes_vars = deepcopy(variables_base.get(url_type))
                    likes_vars.update({'shortcode': post_shortcode})
                    next_page_like = self.make_graphql_url(likes_vars, url_type)
                    yield response.follow(next_page_like,
                                          callback=self.parse_post_likes,
                                          cb_kwargs={'likes_vars': likes_vars, 'post_shortcode': post_shortcode}
                                          )

                print(post_shortcode)

        if data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page'] and len(posts) < 10:
            url_type = 'posts'
            post_vars.update({'after': data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']})
            next_page = self.make_graphql_url(post_vars, url_type)
            yield response.follow(next_page,
                                  callback=self.parse_user_posts,
                                  cb_kwargs={'post_vars': post_vars, 'follow_id': follow_id}
                                  )
        else:
            #Здесь отправляем все посты в монго
            item = ItemLoader(InstaItemPosts(), response)
            item.add_value('follow_id', follow_id)
            item.add_value('posts', self.posts[follow_id])
            print('send posts to mongo')
            yield item.load_item()

        print(follow_id)

    def parse_post_comments(self, response: HtmlResponse, comments_vars, post_shortcode):
        """
        Функция получает на вход распарсенный json с данными по комментам на пост.
        Также получает никнейм пользователя user и параметры comments_vars для парсинга следующей партии комментов.
        Данные сохраняем в mongoDB.
        """
        data = json.loads(response.body)
        comments = data['data']['shortcode_media']['edge_media_to_parent_comment']['edges']

        if self.comments.get(post_shortcode):
            self.comments[post_shortcode]['edges'].extend(comments)
        else:
            self.comments[post_shortcode] = {'edges': comments}

        if data['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['has_next_page']:
            url_type = 'comments'
            comments_vars.update({'after': data['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']})
            next_page_com = self.make_graphql_url(comments_vars, url_type)
            yield response.follow(next_page_com,
                                  callback=self.parse_post_comments,
                                  cb_kwargs={'comments_vars': comments_vars, 'post_shortcode': post_shortcode}
                                  )
        else:
            #Здесь отправляем все комменты в монго
            item = ItemLoader(InstaItemComments(), response)
            item.add_value('post_shortcode', post_shortcode)
            item.add_value('comments', self.comments[post_shortcode])
            print('send comments to mongo')
            yield item.load_item()

        print(post_shortcode)

    def parse_post_likes(self, response: HtmlResponse, likes_vars, post_shortcode):
        """
        Функция получает на вход распарсенный json с данными по лайкам на пост.
        Также получает никнейм пользователя user и параметры likes_vars для парсинга следующей партии лайков.
        Данные сохраняем в mongoDB.
        """
        data = json.loads(response.body)

        likes = data['data']['shortcode_media']['edge_liked_by']['edges']

        if self.likes.get(post_shortcode):
            self.likes[post_shortcode]['edges'].extend(likes)
        else:
            self.likes[post_shortcode] = {'edges': likes}

        if data['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page']:
            url_type = 'likes'
            likes_vars.update({'after': data['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor']})
            next_page_l = self.make_graphql_url(likes_vars, url_type)
            yield response.follow(next_page_l,
                                  callback=self.parse_post_likes,
                                  cb_kwargs={'likes_vars': likes_vars, 'post_shortcode': post_shortcode}
                                  )
        else:
            # Здесь отправляем все лайки в монго
            item = ItemLoader(InstaItemLikes(), response)
            item.add_value('post_shortcode', post_shortcode)
            item.add_value('likes', self.likes[post_shortcode])
            print('send likes to mongo')
            yield item.load_item()

        print(post_shortcode)

    def get_csrf_token(self, response: HtmlResponse):
        """
        Получаем response на вход, парсим куки и возвращаем CSRF Token
        """
        return dict(response.headers.items())[b'Set-Cookie'][7].decode("utf-8").split(';')[0][10:]

    def get_user_id(self, body):
        """
        Из полученного содержимого списка с javascript кодами выделяет и возвращает id юзера, которого мы парсим
        """
        t_dict = body[3].split(' = ')[1].replace(';</script>', '')
        j_dict = json.loads(t_dict.encode('UTF-8'))
        return j_dict['entry_data']['ProfilePage'][0]['graphql']['user']['id']

    def make_graphql_url(self, user_vars, url_type):
        """
        Получает на вход параметры для урла и возвращает целый graphql урл для парсинга
        """
        return graphql_url + f'query_hash={self.query_hash.get(url_type)}&{urlencode(user_vars)}'
