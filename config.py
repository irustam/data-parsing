INSTA_LOGIN = 'imsciencedev'
INSTA_PASS = 'getalldatatrue1020'

graphql_url = 'https://www.instagram.com/graphql/query/?'
query_hash = {'follows': 'd04b0a864b4b54837c0d870b0e77e076',
              'posts': '2c5d4d8b70cad329c4a6ebe3abb6eedd',
              'comments': '97b41c52301f77ce508f55e66d17620e',
              'likes': 'd5d763b1e2acf209d62d22d184488e57',
              }
variables_base = {'follows': {"include_reel": "true", "fetch_mutual": "false", "first": 100},
                  'posts': {"first": 10},
                  'comments': {"first": 100},
                  'likes': {"include_reel": "true", "first": 100},
                  }
"""
users = ['jlo',
         'penelopecruzoficial',
         'ladygaga',
         'shakira',
         'madonna',
         'leonardodicaprio',
         'jim.jarmusch',
         'selenagomez',
         'therock',
         ]
"""
users = ['imsciencedev',
         ]