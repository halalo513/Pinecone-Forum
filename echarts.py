from pyecharts import options as opts
from pyecharts.charts import Bar, WordCloud
from flask import g
import datetime, jieba

# 统计过去七天内发布的所有文章及对应的评论数，利用pyecharts绘制柱状图
def Answers_Bar_Chart():
    time_now=datetime.datetime.now()
    x_data=[]
    bar_y_data=[]
    for question in g.user.questions:
        if question.create_time>=time_now-datetime.timedelta(days=7):
            x_data.append(question.title)
            bar_y_data.append(len(question.answers))
    bar = (
        Bar()
        .add_xaxis(
            x_data
        )
        .add_yaxis("评论数", bar_y_data)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            title_opts=opts.TitleOpts(title="网友回答提问统计", subtitle="统计过去七天"),
        )
    )
    return bar

# 利用jieba对用户发布的所有文章进行分词统计，采用pyecharts绘制词云图
def WordCloud_Chart():
    questions=g.user.questions
    titles=[question.title for question in questions]
    contents=[question.content for question in questions]
    titles=' '.join(titles)
    contents=' '.join(contents)
    text=titles+contents
    words=jieba.lcut(text)
    counts={}
    for word in words:
        if len(word)==1 or len(word.strip())==0:
            continue
        else:
            counts[word]=counts.get(word, 0)+1
    count_words=[(key, value) for key, value in counts.items()]
    wordcloud = (
        WordCloud()
        .add("", count_words, word_size_range=[20, 100], shape='star')
        .set_global_opts(title_opts=opts.TitleOpts(title="提问词频统计", pos_left='center'))
    )
    return wordcloud



