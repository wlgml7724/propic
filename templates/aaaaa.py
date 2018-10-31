
def save_user_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            users = User.objects.all()

            data['html_user_list'] = render_to_string('propicker/setting.html', {
                'users': users
            })
    
        else:
            print("dafs")
            data['form_is_valid'] = False
    context = {'form': form}
    data['userhtml_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

    

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)    
    if request.method == 'POST':
        form = UserForm(request.POST, instance = user)      

    else:
        form = UserForm(instance = user)

    return save_user_form(request, form, 'propicker/user_update.html')

def save_profile_form(request, form, template_name):
    print("\n\nprofile_form저장")
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            propickers = Propicker.objects.all()
            print('저장', form.save()) # 1-> true
            data['html_propicker_list'] = render_to_string('mypic/mypic_all.html', {'propickers': propickers})
            # print('데이터', data['html_propicker_list'])
        else:
            print("유효성 실패")
            data['form_is_valid'] = False
    context = {'form': form}
    data['propickerhtml_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

    

def profile_update(request, pk):
    print("\n\nprofile_update시작")
    # propicker 가져온다. 
    propicker = get_object_or_404(
        Propicker, 
        pk=pk
    )
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance = propicker)      

    else:
        form = ProfileForm(instance = propicker)

    return save_profile_form(request, form, 'propicker/profile_update.html')

