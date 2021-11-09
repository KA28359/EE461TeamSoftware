
################################################################################################
########################## three parts slightly modified in app.py #############################

@app.route('/api/authorized', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def get_authorized():
    if "user" not in session:
        flash("Access denied: you need to log in first:")
        return {'auth': 'rejected'}
    elif session["user"] != encrypt(request.get_json().get('username', None)):
        flash("Access denied: you're not allowed to proceed that website")
        info = session["user"]
        return {'auth': 'rejected',
                'username': decrypt(info)}
    else:
        return {'auth': 'access'}


@app.route('/api/project/authorized', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def get_authorized_with_pro():
    if "user" not in session:
        flash("Access denied: you need to log in first:")
        return {'auth': 'rejected'}
    else:
        this_user = session["user"]
        userid = encrypt(request.get_json().get('username', None))
        if this_user != userid:
            access = False
            project_ID = int(request.get_json().get('projectid', None))
            check = users.objects(user_encryptid=this_user)
            for item in check:
                for check_acc in item.user_access:
                    if check_acc.acc_userid == userid and check_acc.acc_proid == project_ID:
                        access = True
                        return {'auth': 'access'}
            if not access:
                flash("Access denied: you're not allowed to proceed that website")
                return {'auth': 'rejected',
                        'username': decrypt(this_user)}
        else:
            return {'auth': 'access'}


@ app.route('/api/project/hardware/adduser', methods=["GET", "POST"])
def project_adduser():
    if request.method == 'POST':
        error = ''
        userid = encrypt(request.get_json().get('name', None))
        project_ID = int(request.get_json().get('proid', None))
        # project_this = dbModel.objects(project_id=project_ID)
        add_user = encrypt(request.get_json().get('usertoadd', None))
        user = users.objects(user_encryptid=add_user).first()
        if user:
            try:
                new_acc = addAccess(acc_userid=userid,
                                    acc_proid=project_ID)
                user.user_access.append(new_acc)
                user.save()
                error = ("user added")
                return {'error': error}
            except:
                return{'error': 'failed: unknown error'}
        else:
            error = "invalid user name"
            return {'error': error}






################################################################################################
###########################changement in Class <Project> in app.js ##############################
######################### just the ssession part and the render part ############################




class Project extends React.Component{
  _isMounted = false;
  refreased = false;
  constructor(props){
    super(props);
    this.state = {
      counter:0,
      disbaled: false,
      data:[],
      authorized:true,
      spinner:false,
      index:0,
      tested:false,
      name:this.props.match.params.userID.toString(),
      username:''
    };
  }

  refreshAuth=()=>{
    if(!this.state.tested && !this.refreased){
      this.refreased=true
      this.componentDidMount()  
  }}

  componentDidMount=()=>{
    let info = {'username':this.props.match.params.userID.toString()};
    fetch("http://127.0.0.1:5000/api/authorized",{method:'post',credentials: 'include', headers:{"Content-Type": "application/json"},body:JSON.stringify(info)})
    .then(response => response.json())
    .then(data => {
      this._isMounted=true
      if(data.auth === 'rejected' && this._isMounted){
       const path=(data.username===undefined)? '' : data.username
       this.setState({username:path})
       this.setState({authorized:false,tested:true})
       this.refreased=false
       
      }
      if(data.auth === 'access' && this._isMounted){
      this.setState({authorized:true,tested:true})
      }
    });
  }
  componentWillUnmount() {
    this._isMounted = false;
  }



...



render(){
    if(!this.state.tested){
      this.refreshAuth()
      return(
        <div></div>
      );
    }
    else if(!this.state.authorized){
      if(this.state.username !== ''){
        return(
        <div>
          <Nav><NavMenu> <p style={{color:'#ffffff',fontSize:'2.5em'}}>TEAM SOFTWARE</p></NavMenu><NavMenu> <h1 style={{color:'#ffffff'}}>UserID: {this.props.match.params.userID.toString()}</h1><LogBtn style={{backgroundColor:"#ffffff",color:"#000000",marginLeft:'24px'}}  onClick={(event) => this.signOut()} type = "submit">Sign Out</LogBtn></NavMenu></Nav>
          <CenterSpace>
            <div style={{ color: 'red', textAlign:"center"}} >
            <p>Access denied:</p>
            <p>if you're trying to use another account, you need to logout first</p>
            </div>
          </CenterSpace>
          <CenterSpace>
            <Link to={'/project/'+this.state.username} onClick={()=>this.setState({tested:false})} >Go back</Link>
          </CenterSpace>
        </div>
      );
      }
      else{
        return <Redirect to='/'/>
      }
    }else{

   
  return (...)
  
  
  
  
  #######################################################################
  ######### you may need to modify the calling of <HwTable> part ########
  ###### because I added a class <Hardware> to call it instead ##########
  #######################################################################
