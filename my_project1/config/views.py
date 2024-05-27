import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from goods.models import Book

def main(request):
    # type(request) == django.core.handlers.wsgi.WSGIRequest
    return HttpResponse("일반 Text 응답 예제입니다.")

def test1(request):
    return HttpResponse('일반 Text 응답 예제1', content_type='text/plain', charset='euc-kr')

def test2(request):
    print(type(request.headers))         # <class 'django.http.request.HttpHeaders'>
    headerDict = dict(request.headers.items())
    for k, v in headerDict.items():
        print(F'KEY : {k}, VALUE : {v}')
    # KEY : Content-Length, VALUE :
    # KEY : Content-Type, VALUE : text/plain
    # KEY : Host, VALUE : 127.0.0.1:8000
    # KEY : Connection, VALUE : keep-alive
    # KEY : Cache-Control, VALUE : max-age=0
    # KEY : Sec-Ch-Ua, VALUE : "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"
    # KEY : Sec-Ch-Ua-Mobile, VALUE : ?0
    # KEY : Sec-Ch-Ua-Platform, VALUE : "Windows"
    # KEY : Upgrade-Insecure-Requests, VALUE : 1
    # KEY : User-Agent, VALUE : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36
    # KEY : Accept, VALUE : text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
    # KEY : Sec-Fetch-Site, VALUE : none
    # KEY : Sec-Fetch-Mode, VALUE : navigate
    # KEY : Sec-Fetch-User, VALUE : ?1
    # KEY : Sec-Fetch-Dest, VALUE : document
    # KEY : Accept-Encoding, VALUE : gzip, deflate, br, zstd
    # KEY : Accept-Language, VALUE : ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
    print(request.method)                # GET
    print(request.build_absolute_uri())  # http://127.0.0.1:8000/testURL1/test2
    print(request.content_type)          # text/plain
    print(request.user.is_authenticated) # False
    return HttpResponse(dir(request).__str__())

def test3(request):
    path = request.path
    method = request.method
    content = '''
<center><h2>Testing Django Request Response</h2>
<p>Request path :  {data1}</p>
<p>Request Method :  {data2}</center>
'''.format(data1=path, data2=method)
    return HttpResponse(content)

# JSON 리턴
def test4(request):
    return JsonResponse([
        {'book_name':'CentOS 리눅스 구축관리 실무', 'author':'정우영', 'pages': 1020, 'price':35000},
        {'book_name':'전문가를 위한 스프링5', 'author':'율리아나 코스미나', 'pages': 1200, 'price':54000},
    ], safe=False) # JsonResponse의 첫 번째 파라미터가 딕셔너리가 아닌 경우 safe=False로 설정

def test5(request):
    return HttpResponse(
        json.dumps([
            {'book_name':'CentOS 리눅스 구축관리 실무', 'author':'정우영', 'pages': 1020, 'price':35000},
            {'book_name':'전문가를 위한 스프링5', 'author':'율리아나 코스미나', 'pages': 1200, 'price':54000}
        ]),
        headers = {
            'Content-Type' : 'application/json',
            # 'Content-Disposition' : 'attachment; filename="hello.json"',
        },
    )

# 템플릿(Templates) 리턴
def menu_list(request):
    return render(request, "Menu_list.html")

def menu_list2(request):
    template = loader.get_template("Menu_list.html")
    return HttpResponse(template.render(request=request))

def book_list(request):
    books = Book.objects.all()
    print('책 전체 목록:', books)
    
    # Template으로 전달해줄 딕셔너리
    context = {
        'books' : books,   # books 키에 QuerySet 객체를 전달한다.
        'books2' : "<br/>".join(['<h4 style="color:red;">'+str(x)+'</h2>' for x in list(books)]),
    }
    return render(request, 'Book_list.html', context)
    
# 검색화면
# http://localhost:8000/search/?keyword=ABC&keyword=DEF&keyword=GHI ✅ 같은 이름의 파라미터 여러개는 request.GET.getlist("keyword") 로 받는다
# http://localhost:8000/search/?keyword=SQL
def book_search(request):
    # [a for a in request.GET.items()] 이렇게 제너레이터로 모든 파라미터를 받아올 수 있다.
    # print(type(request.GET), type(request)) # <class 'django.http.request.QueryDict'> <class 'django.core.handlers.wsgi.WSGIRequest'>
    keyword = request.GET.get("keyword")
    if keyword is not None :
        books = Book.objects.filter(name__contains=keyword) # 칼럼이름__contains : SELECT ... WHERE 칼럼이름 LIKE '%keyword%'
    else :
        books = Book.objects.none() # 비어있는 쿼리셋 <QuerySet []> 를 할당
    # print(books) # <QuerySet [<Book: 이름: 친절한 SQL 튜닝, 저자: 조시형>]>
    context = {
        "books" : books,
    }
    return render(request, "Book_search.html", context)

