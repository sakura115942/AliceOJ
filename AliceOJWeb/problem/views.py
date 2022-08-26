from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


import os
import json
import markdown

from .models import Problem, Solution, Answer
from user.models import User, UserData
from user.wrapper import login_require
from .complier import Complier
from .judger import Judger
# Create your views here.


def problem_list(request):
    menu = 'problem'
    problems = Problem.objects.all()
    p = Paginator(problems, 10)
    if p.num_pages <= 1:
        page_data = ''
    else:
        page = int(request.GET.get('page', 1))
        problems = p.page(page)
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:
            right = page_range[page:page + 2]
            print(total_pages)
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page == total_pages:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            right = page_range[page:page + 2]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        page_data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
        }

    return render(
        request, 'problemList.html', {
            'menu': menu,
            'problemList': problems,
            'pageData': page_data,
        })


def problem_detail(request, id):

    problem = Problem.objects.get(id=id)
    problem.description = markdown.markdown(problem.description,
                                            extensions=[
                                                'markdown.extensions.extra',
                                                'markdown.extensions.codehilite',
                                                'markdown.extensions.toc',
                                            ])
    answers = problem.answer_set.order_by('-judger_time')[:10]
    return render(request, 'problemDetail.html', {'problem': problem, 'answers':answers})

BASE_PATH = 'temp/'
BASE_DIR = settings.BASE_DIR

@csrf_exempt
@login_require
def problem_submit(request):
    referer = request.META['HTTP_REFERER']
    code = request.POST.get('code', None)
    if code is None:
        return redirect(referer)

    user_id = request.session['user_id']
    problem_id = referer.split('/')[-2]

    user = User.objects.get(id=user_id)
    problem = Problem.objects.get(id=problem_id)

    exe_path = BASE_DIR + '/temp/exe_%s_%s' % (user_id, problem_id)
    source_path = BASE_DIR + '/temp/source_%s_%s.c' % (user_id, problem_id)

    input_path = BASE_DIR + '/temp/input_%s.txt' % (problem_id)    # 题目输入
    answer_path = BASE_DIR + '/temp/answer_%s.txt' % (problem_id)  # 题目答案
    output_path = BASE_DIR + '/temp/output_%s_%s.txt' % (user_id, problem_id)  # 用户程序输出
    
    with open(source_path, 'w') as f:
        f.write(code)

    # 将输入和预期的输出写入到文件以供测评
    if not os.path.exists(input_path):
        input_msg = problem.solution.input
        with open(input_path, 'w') as f:
            f.write(input_msg)

    if not os.path.exists(answer_path):
        answer_msg = problem.solution.output
        with open(answer_path, 'w') as f:
            f.write(answer_msg)

    if not os.path.exists(output_path):
        with open(output_path, 'w'):
            pass

    answer = Answer()
    answer.problem = problem
    answer.user = user
    answer.state = False

    # 编译无误情况下，返回0
    res = Complier.complie(source_path, exe_path)
    if res != 0:
        answer.message = res
        answer.save()
        return redirect(referer)
    
    config = {
        'input_path': input_path,
        'output_path': output_path,
        'answer_path': answer_path,
        'cpu_time_limit': problem.solution.cpu_time_limit,
        'real_time_limit': problem.solution.real_time_limit,
        'memory_limit': problem.solution.memory_limit,
    }

    result = Judger.judge(exe_path, config)
    state = result.get('state', None)
    print(result)
    if (state is None) or (not state):
        pass
    else:
        user_data = UserData.objects.get(user=user)
        user_data.score += problem.score
        user_data.accepted_count += 1
        user_data.save()
    
    answer.cpu_time = result['cpu_time']
    answer.real_time = result['real_time']
    answer.use_memory = result['use_memory']
    answer.message = result['msg']
    answer.state = state
    answer.save()
   
    return redirect(referer)
