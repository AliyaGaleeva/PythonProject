from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.generic import TemplateView

# Create your views here.
from django.http import HttpResponse, Http404
from django.views import generic

from polls.make_short import make_short_address
from polls.forms import IndexForm
import pandas as pd

def index(request):
    '''
    метод отображения стартовой страницы
    :param request: запрос
    :return: стартовая страница
    '''
    return render(request, "index.html")


def all_addresses(request):
    '''
    метод для отображения всех ссылок
    :param request: запрос
    :return: страница со списком всех адресов в таблице
    '''
    urls = pd.read_csv("data.csv", sep=",")
    html_urls = pd.DataFrame(urls).to_html(header="all addresses", index=False, border=2)
    #return render(request, "allAddresses.html")
    return HttpResponse(html_urls)


def give_short(request):
    '''
    метод для получения короткой ссылки
    :param request: запрос
    :return: страницу с коротким адресом
    '''
    long_str = request.POST.get("long_url")
    short_str = make_short_address(long_str, "data.csv")
    return HttpResponse("<h2>Your short address: {0}</h2>".format(short_str))

def delete(request, link):
    """метод для удаление ссылок
    :param request: запрос
    :param link: ссылка, которую надо удалить
    :return: переход на страницу со списком ссылок
    """
    res = pd.read_csv("data.csv", sep=",")
    res = res.set_index('long_addresses')
    # проверить есть ли такая ссылка
    if link in res.index:
        res.drop([link], inplace=True)
    res.to_csv("data.csv")
    return redirect("all")


def redir(request, link):
    """метод для переадресации перехода
    :param request: запрос
    :param link: хеш исходной ссылки
    :return: исходная страница или страниуа ошибки
    """
    res = pd.read_csv("data.csv", sep=",")
    res = res.set_index('short_addresses')
    # проверить есть ли такая ссылка
    if link in res.index:
        long_link = res.loc[link].long_addresses
        return redirect(long_link)
    else:
        return HttpResponse("<h2>This address does not exist, try again</h2>")
