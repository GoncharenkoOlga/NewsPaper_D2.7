#1 Создаем  двух пользователей
from django.contrib.auth.models import User
user=User.objects.create_user('User1', password='User1')
user=User.objects.create_user('User2', password='User2')
user.is_superuser=False
user.is_staff=False
user.save()

#2 Создаем два объекта модели Author связанные с пользователями
from news.models import *
User.objects.all()
#  В выводе получаем: <QuerySet [<User: admin>, <User: User1>, <User: User2>]>
u1 = User.objects.get(username='User1')
Author.objects.create(user=u1, rating='1')
#  В выводе получаем: <Author: Author object (1)>
u1.save()

u2 = User.objects.get(username='User2')
Author.objects.create(user=u2, rating='2')
#  В выводе получаем: <Author: Author object (2)>
u2.save()


#3 Добавляем 4 категории
from news.models import Category
category_1 = Category.objects.create(category_name='Наука')
category_2 = Category.objects.create(category_name='Технологии')
category_3 = Category.objects.create(category_name='Здоровье')
category_4 = Category.objects.create(category_name='Обо всём')


#4 Добавляем 2 статьи и 1 новость
from news.models import *
post_news = Post.objects.create(author=Author.objects.get(pk=1), title='Единый налоговый вычет: как работает новая система?', text='Единый налоговый счёт (ЕНС) — это не новый режим налогообложения, а новый порядок учёта начисленных и уплаченных налогов и взносов. Все налоги перечисляются в бюджет единым налоговым платежом (ЕНП) по одному КБК (код бюджетной классификации).', choice='news')
post_art_1 = Post.objects.create(author=Author.objects.get(pk=1), title='Психологи рассказали как бороться с неосознанной тревогой', text='«Парадоксально, но лучший способ начать бороться с неосознанной тревогой — принять её. Избегание этой проблемы усугубляет ситуацию, позволяя стрессу прочно закрепиться в жизни человека», — поясняет Андриевская. Осознанность помогает снизить интенсивность эмоций. С их принятием работают многие подходы в психотерапии, помогающие распознавать чувства и физические ощущения без самоосуждения.', choice='articles')
post_art_2 = Post.objects.create(author=Author.objects.get(pk=2), title='Не все диеты одинаково полезны', text='Причина избыточного веса не всегда кроется в переедании. Как не навредить себе диетой и эффективно подобрать новый рацион, пишет «Почему болит» со ссылкой на эндокринолога Елену Кученкову-Виноградову.', choice='articles')
post_news_2 = Post.objects.create(author=Author.objects.get(pk=2), title='"Без осуждения""', text='Ozon хочет в рамках эксперимента трудоустроить 500 заключённых с мягким режимом отбывания.', choice='news')

#5 Присвоем им категории (в одной статье сделаем 2 категории).
from news.models import *
category_1 = Category.objects.all()[0]
category_2 = Category.objects.all()[1]
category_3 = Category.objects.all()[2]
category_4 = Category.objects.all()[3]
post_news.category.add(category_4)
post_art_1.category.add(category_3, category_4)
post_art_2.category.add(category_1, category_3)
post_news_2.category.add(category_2, category_4)

#6 Создаем 4 комментария к разным объектам Post
from news.models import Comment
post_news = Post.objects.get(pk=1)
comment_1 = Comment.objects.create(comment_user=User.objects.get(pk=3), comment_post=post_news,comment_text='Опять бред какой то придумали')
post_news = Post.objects.get(pk=4)
comment_2 = Comment.objects.create(comment_user=User.objects.get(pk=1), comment_post=post_news, comment_text='Очень интересно')
post_art_1 = Post.objects.get(pk=2)
comment_3 = Comment.objects.create(comment_user=User.objects.get(pk=1), comment_post=post_art_1, comment_text='Спасибо, очень полезно')
post_art_2 = Post.objects.get(pk=3)
comment_4 = Comment.objects.create(comment_user=User.objects.get(pk=2), comment_post=post_art_2, comment_text='Много нового для себя почерпнула')
post_news_2 = Post.objects.get(pk=4)
comment_5 = Comment.objects.create(comment_user=User.objects.get(pk=2), comment_post=post_news_2, comment_text='Хм, посмотрим, что из этого выйдет)))')


#7 Применем like и dislike к статьям/новостям и комментариям, корректируем их рейтинги
post_news.like()
post_news.like()
post_news.like()
post_art_1.like()
post_art_2.like()
post_art_2.like()
post_news.like()
comment_1.like()
comment_3.dislike()
comment_4.dislike()
post_art_1.like()
post_news_2.dislike()
post_news_2.dislike()
post_news_2.like()
post_art_1.like()

#8 Обновлем рейтинги для авторов статей
author_1 = Author.objects.get(pk=1)
author_1.update_rating()

author_2 = Author.objects.get(pk=2)
author_2.update_rating()

#9 Выводим имя и рейтинг лучшего пользователя (применяя сортировку)
Author.objects.all().order_by('-rating').values('user__username', 'rating').first()
#  В выводе получаем: {'user__username': 'User1', 'rating': 8}

#10 Выводим дату добавления, имя автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках и дизлайках.
best_post = Post.objects.all().order_by('-post_rating').first()
best_post_data = Post.objects.all().order_by('-post_rating').values('posting_time', 'author__user__username', 'post_rating', 'title').first()
best_post_preview = Post.objects.all().order_by('-post_rating').first().preview()
best_post_preview
#  В выводе получаем: '«Парадоксально, но лучший способ начать бороться с неосознанной тревогой — принять её. Избегание этой проблемы усугубляет си...'

#11 Выводим все комментарии (дата, пользователь, рейтинг, текст) к лучшей статье.
comments = Comment.objects.filter(comment_post=best_post).values('comment_date', 'comment_user', 'comment_rating', 'comment_text')
comments
#  В выводе получаю: <QuerySet [{'comment_date': None, 'comment_user': 1, 'comment_rating': -1, 'comment_text': 'Спасибо, очень полезно'}]>