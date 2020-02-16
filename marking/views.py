from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from marking import models
from django.views.decorators.csrf import csrf_exempt
from datetime import date

@login_required
def index(request):
    return render(request, 'index.html')
@csrf_exempt
@login_required
def mark(request):

    if int(date.today().month) == 1:
        last_month = 12
        last_year = date.today().year -1
    else:
        last_month = int(date.today().month) - 1
        last_year = date.today().year
    last_date = str(last_year) + str(last_month)
    if request.method == 'GET':
        v1 = models.UserProfile.objects.all()
    elif request.method == 'POST':
        req_user_id = request.POST.get('req_user_id')
        print(req_user_id)
        req_user = models.UserProfile.objects.filter(id=req_user_id)
        # req_user = models.IsMark.objects.filter(id=req_user_id)
        if len(req_user) is not 0:
            req_user = req_user[0]

            if req_user.is_mark_name.is_grade is False:
                last_id = models.UserProfile.objects.all().last()  # get person total

                # now_month = str(n_year) + str(n_month)
                for id in range(1, last_id.id+1):
                    td_id = "id_" + str(id)
                    td_score = "score_" + str(id)
                    td_user_id = request.POST.get(td_id)
                    td_score = int(request.POST.get(td_score))

                    mark_obj = models.Mark.objects.filter(name_id=td_user_id,month=last_date)
                    # print(len(mark_obj))
                    if len(mark_obj) is not 0:
                        update_obj = models.Mark.objects.filter(name_id=td_user_id,month=last_date)[0]

                        print(type(update_obj.score),type(td_score))
                        update_score = update_obj.score + td_score
                        update_score_num = update_obj.score_num + 1
                        mark_id = update_obj.id
                        update_ave_score = str("%.2f" % (update_score/update_score_num))
                        models.Mark.objects.filter(id=mark_id).update(score=update_score,
                                                                      score_num=update_score_num,
                                                                      ave_score=update_ave_score)
                    else:
                        models.Mark.objects.create(name_id=td_user_id,
                                                   score=td_score,month=last_date,score_num=1,ave_score=td_score)
                # user_id = models.UserProfile.objects.filter(id=req_user_id)
                # req_user.is_mark_name.is_grade
                # models.UserProfile.objects.filter(id=req_user_id).update(is_grade=True)
                models.IsMark.objects.filter(name=req_user).update(is_grade=True)

            else:
                print("request.user.name:",req_user.name,'已经评分过了')
        return redirect('/mark/')
    return render(request, 'mark.html',{'v1': v1, 'y1': last_year, 'm1': last_month})


@csrf_exempt
@login_required
def history_mark(request):
    if request.method == 'GET':
        if int(date.today().month) == 1:
            last_month = 12
            last_year = date.today().year -1
        else:
            last_month = int(date.today().month) - 1
            last_year = date.today().year

        last_date = str(last_year) + str(last_month)
        v2 = models.Mark.objects.filter(month=last_date)
        # return render(request, 'history_mark.html',{'v2': v2, 'y1': last_year, 'm1': last_month})
    elif request.method == 'POST':
        last_year = request.POST.get("y_score")
        last_month = request.POST.get("m_score")
        filter_date = str(last_year) + str(last_month)
        v2 = models.Mark.objects.filter(month=filter_date)

    return render(request, 'history_mark.html',{'v2': v2, 'y1': last_year, 'm1': last_month})

def acc_login(request):
    errors = {}
    print(request.method)
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        user = authenticate(email=username,password=password)
        print(user)
        if user:
            login(request,user)
            return redirect(request.GET.get("next", "/"))
        else:
            errors['msg'] = "Wrong username or password!"
    return render(request, 'login.html', {'errors':errors})

