
@app.route('/api/project', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def project_table():
    if request.method == 'POST':
        userid = encrypt(request.get_json().get('name', None))
        projects = dbModel.objects(user_id=userid).all()
        projects_acc = []
        try:
            user_info = users.objects(user_encryptid=userid)
            for user in user_info:
                if user.user_access:
                    for acc in user.user_access:
                        proid = acc.acc_proid
                        nameid = acc.acc_userid
                        project_acc = dbModel.objects(
                            project_id=proid).first()
                        if project_acc:
                            if project_acc.user_id != nameid:
                                user.user_access.remove(acc)
                                user.save()
                            else:
                                projects_acc.append(project_acc)
                        else:
                            user.user_access.remove(acc)
                            user.save()
        except:
            flash("no other access added to this user")

        return jsonify([*map(project_serializer, projects)]+[*map(project_serializer, projects_acc)])

