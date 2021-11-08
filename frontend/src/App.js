import React from "react";
import Navbar from './components/Navbar';
import TextField from '@mui/material/TextField';
import { useState } from "react";
import ArrowForwardIosIcon from '@material-ui/icons/ArrowForwardIos';
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos';
import AlternateEmailIcon from '@material-ui/icons/AlternateEmail';
import SecurityIcon from '@material-ui/icons/Security';
import CloudIcon from '@material-ui/icons/Cloud';
import AddBoxIcon from '@material-ui/icons/AddBox';
import StorageIcon from '@material-ui/icons/Storage';
import { IconButton } from '@mui/material';
import {Link} from 'react-router-dom';
import './App.css';
import { CircularProgress } from '@mui/material';
import {
  LogBtn,
  CenterForm,
  CenterSpace,
  Nav,
  VerticalNav,
  TableSpace,
  NavMenu
} from './components/Navbar/NavbarElements';
import {
  BrowserRouter as Router,
  Switch,
  Redirect,
  Route
} from "react-router-dom";

import { ShowProjects } from './projects';
import { CreateProject } from './createProject';
import HwTable from "./hardwareTable";

//If signin is in the path, it will go to the sign in page
//If signup is in the path, it will go to the sign up page
//If the path is blank, it will go to the home screen
export default function App() {
  return (
    <Router>
      {/* <Navbar /> */}
      <div>
        <Switch>
          <Route path="/signin"> 
            <SignIn />
          </Route>
          <Route path="/signup">
            <SignUp />
          </Route>
          <Route path="/project/:userID/:proID" component={Project} />
          <Route path="/project/:userID" component={Project}  />
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}


class Project extends React.Component{
  _isMounted = false;
  constructor(props){
    super(props);
    this.state = {
      counter:0,
      disbaled: false,
      data:[],
      authorized:true,
      spinner:false,
      index:0,
      projects:true,
      datasets:false,
      tested:false
    };
  }

  getData(){
    this.setState({disbaled:true});
    this.setState({spinner:true});
    let info = {'currentEntry':this.state.index};
    fetch("http://127.0.0.1:5000/api/data",{method:'post', headers:{"Content-Type": "application/json"},body:JSON.stringify(info)})
    .then(response => response.json())
    .then(data => {
      // this.setState({data:data}); 
      for(var i = 0; i < data.length; i++){
        this.setState({ data: [...this.state.data, data[i]] })
        this.setState({index:this.state.index+1})
      }
      if(data.length === 0){
        this.setState({disbaled:true});
      }else{
        this.setState({disbaled:false});
      }
      this.setState({spinner:false});
    });
    
  }


  getRows(){
    return this.state.data.map((entry) => <tr key={this.state.counter++}><td>{entry[0]}</td><td>{entry[1]}</td><td><a href={entry[2]}>Click here to download zip</a></td></tr>);
  }

  componentDidMount(){
    this._isMounted = true;
    let info = {'username':this.props.match.params.userID.toString()};
    fetch("http://127.0.0.1:5000/api/authorized",{method:'post',credentials: 'include', headers:{"Content-Type": "application/json"},body:JSON.stringify(info)})
    .then(response => response.json())
    .then(data => {

      if(data.auth === 'rejected' && this._isMounted){
       this.setState({authorized:false})
       this.setState({tested:true})
      }
      if(data.auth === 'access' && this._isMounted){
      this.setState({tested:true})
      }
    });
  }
  componentWillUnmount() {
    this._isMounted = false;
  }

  signOut(){
    fetch("http://127.0.0.1:5000/api/logout",{method:'post',credentials: 'include', headers:{"Content-Type": "application/json"}})
    .then(response => response.json())
    .then(data => {

      if(data.status === 'success' && this._isMounted){
        this.setState({authorized:false})
      }
      
    });
  }

  projectsClicked(){
    this.setState({projects:true});
    this.setState({datasets:false});
    this.props.history.push('/project/'+ this.props.match.params.userID.toString())
  }

  datasetsClicked(){
    this.setState({projects:false});
    this.setState({datasets:true});
    this.props.history.push('/project/'+ this.props.match.params.userID.toString())
  }

  render(){
    if(!this.state.tested){
      return(<div></div>);
    }
    else if(!this.state.authorized && this.state.tested){
      return <Redirect to='/'/>;
    }else{

      if(this.state.projects && this.props.match.params.proID === undefined){

        return (
          <div className="column">
            
            <Nav><NavMenu> <p style={{color:'#ffffff',fontSize:'2.5em'}}>TEAM SOFTWARE</p></NavMenu><NavMenu> <h1 style={{color:'#ffffff'}}>UserID: {this.props.match.params.userID.toString()}</h1></NavMenu></Nav>
            <div className = "row">
            <VerticalNav>
            <ul className = "ListStyle">
             <li className = "block"><button className="items" href="" onClick={(event) => this.projectsClicked()}>Projects</button></li>
             <li className = "block"><button className="items" href="" onClick={(event) => this.datasetsClicked()}>Datasets</button></li>
             <li className = "block"><button className="items" href="" onClick={(event) => this.signOut()}>Logout</button></li>
            </ul>
            </VerticalNav>
           <div style={{width:"100%"}}>
              <h1 style={{textAlign:"center"}}>Your Projects</h1>
              <ProTable info = {this.props.match.params.userID.toString()} />
              </div>
            </div>
          </div>
        
          );

      }else if(this.state.projects && this.props.match.params.proID !== undefined){

        return (
          <div className="column">
            
            <Nav><NavMenu> <p style={{color:'#ffffff',fontSize:'2.5em'}}>TEAM SOFTWARE</p></NavMenu><NavMenu> <h1 style={{color:'#ffffff'}}>UserID: {this.props.match.params.userID.toString()}</h1></NavMenu></Nav>
            <div className = "row">
            <VerticalNav>
            <ul className = "ListStyle">
             <li className = "block"><button className="items" href="" onClick={(event) => this.projectsClicked()}>Projects</button></li>
             <li className = "block"><button className="items" href="" onClick={(event) => this.datasetsClicked()}>Datasets</button></li>
             <li className = "block"><button className="items" href="" onClick={(event) => this.signOut()}>Logout</button></li>
            </ul>
            </VerticalNav>
           <div style={{width:"100%"}}>
              <div><HwTable name={this.props.match.params.userID.toString()} proid={this.props.match.params.proID.toString()}/></div>
              </div>
            </div>
          </div>
        
          );

      }else if(this.state.datasets){

        return (

            <div className="column">
            <Nav><NavMenu> <p style={{color:'#ffffff',fontSize:'2.5em'}}>TEAM SOFTWARE</p></NavMenu><NavMenu> <h1 style={{color:'#ffffff'}}>UserID: {this.props.match.params.userID.toString()}</h1></NavMenu></Nav>
              <div className = "row">
                <VerticalNav>
                <ul className = "ListStyle">
                  <li className = "block"><button className="items" href="" onClick={(event) => this.projectsClicked()}>Projects</button></li>
                  <li className = "block"><button className="items" href="" onClick={(event) => this.datasetsClicked()}>Datasets</button></li>
                  <li className = "block"><button className="items" href="" onClick={(event) => this.signOut()}>Logout</button></li>
                </ul>
                </VerticalNav>
                <div style={{width:"100%"}}>
                <TableSpace>
                  <table>
                  <tbody>
                    {this.state.data.length === 0 ? null:<tr><th>Name</th><th>Description</th><th>Download</th></tr>}
                    {this.state.data.length === 0  ? null:this.getRows()}
                  </tbody>
                  </table>
                </TableSpace>
                <CenterSpace>
                  {this.state.spinner?<CircularProgress />:null}
                </CenterSpace>
                <CenterSpace>
                  <LogBtn style={{backgroundColor:this.state.disbaled?"#808080":"#CC5500"}} disabled={this.state.disbaled} onClick={(event) => this.getData()} type = "submit">Get data</LogBtn>
                </CenterSpace>
                </div>
              </div>
            </div>
        
          );


      }


   }
  }
}

function ProTable({info}){
  const [data, setData]=useState([{}])
  const [error,setError] = useState('');
  const [proname, setProname]=useState('')
  const [prodesc, setProdesc]=useState('')
  const [proid, setProid]=useState('')

  React.useEffect(()=>{
      fetch("http://127.0.0.1:5000/api/project",
        {method:'post',credentials: 'include', headers:{"Content-Type": "application/json"},
        body:JSON.stringify({'name':info.toString()})})
      .then(response => response.json())
      .then(data => {setData(data)
            console.log(data)})
  },[])
  const updateData=()=>{
    fetch("http://127.0.0.1:5000/api/project",
        {method:'post',credentials: 'include', headers:{"Content-Type": "application/json"},
        body:JSON.stringify({'name':info.toString()})})
      .then(response => response.json())
      .then(data => {setData(data)
            console.log(data)})
  }

  const handleDelete=(user,proid)=>{
      fetch('http://127.0.0.1:5000/api/project/delete',{
          method:"POST",
          body:JSON.stringify({
              "userid":user,
              "proid":proid,
          }),
          headers:{
              "Content-type":"application/json; charset=UTF-8",
              "Access-Control-Allow-Headers":"Content-Type",
              "Access-Control-Allow-Credentials":"true"
          }
      }).then(res => res.json())
      .then(data => {
          if (data.error === 'None'){
            updateData()
          }
          else{
            setError(data.error)}
      })
  }
const setName = (value) =>{
    setProname(value)
}
const setDesc = (value) =>{
    setProdesc(value)
}
const setId = (value) =>{
    setProid(value)
}
  const handleSubmit=()=>{
    fetch('http://127.0.0.1:5000/api/project/add',{
    method:"POST",
    body:JSON.stringify({
        "userid":info.toString(),
        "name":proname,
        "desc":prodesc,
        "proid":proid
    }),
    headers:{
        "Content-type":"application/json; charset=UTF-8",
        "Access-Control-Allow-Headers":"Content-Type",
        "Access-Control-Allow-Credentials":"true"
    }
}).then(res => res.json())
.then(data => {
          if (data.error === 'None'){
            updateData()
            setProname('')
            setProdesc('')
            setProid('')
          }
          else{
            setError(data.error)}
   
})
}

  return(
    <div>
      <div className="project_table">
              <ShowProjects pros={data} name={info} onDelete={handleDelete}/>
      </div>
      <br/>
      <div className="project_create">
        <CenterForm>
            <h1>Create a new project:</h1>
            </CenterForm>
            <CreateProject onSubmit={handleSubmit} setName={setName} setDesc={setDesc} setId={setId}/>
      </div>
      <CenterForm>
          {error?<p style={{ color: 'red' }}>{error}</p>:<p> </p>}
      </CenterForm>
    </div>
  )
}


function Home() {

  const [imgNum, setVal] = useState(0); //imgNum is used to keep track of what icon is currently showing
  const timer = React.useRef(null); //timer used for carousel
  const icons = [
  <AlternateEmailIcon className = "large_icon"/>,
  <SecurityIcon className = "large_icon"/>,
  <CloudIcon className = "large_icon"/>,
  <AddBoxIcon className = "large_icon"/>,
  <StorageIcon className = "large_icon"/>
]; //list of all of the icons used

const descriptions = [
<p className = "bigger_text">Create an account or sign in to get started</p>,
<p className = "bigger_text">High level security with advanced encrytpion</p>,
<p className = "bigger_text">App runs on the cloud so you can access from anywhere</p>,
<p className = "bigger_text">Create multiple projects on your account</p>,
<p className = "bigger_text">Your project information is stored securly in our databases</p>
]; //descriptions of each icon

function resetTimeout() {
  if (timer.current) {
    clearTimeout(timer.current); //setting timer back to 0 if it just changed or if an arrow was pressed
  }
}

React.useEffect(() => {
  resetTimeout();
  timer.current = setTimeout(
    () =>
      setVal((prevIndex) => prevIndex === (icons.length-1) ? 0 : prevIndex+1 //taking care of loop
      ),
    3000 //timer time
  );


  return () => {
    resetTimeout();
  };
}, [imgNum]);

const updateVal = (input) => {

  if(input === "add"){
    setVal((prevIndex) => prevIndex === (icons.length-1) ? 0 : prevIndex+1); //taking care of loop
  }
  if(input === "sub"){
    setVal((prevIndex) => prevIndex === 0 ? icons.length-1 : prevIndex-1);// taking care of loop
  }

}


//Showing the current icon first along with the description and then the arrows
//if the arrows are pressed, they pass a value to tell the fuction to add or subtract
//the <centerForm> is a styled component using template literals to center all the conent
  return (
    <div>
      <Navbar />
      <CenterForm>
        {icons[imgNum]}
      </CenterForm>
      <CenterForm>
        {descriptions[imgNum]}
      </CenterForm>
      <CenterForm>
        <IconButton onClick={()=>updateVal("sub")}>
          <ArrowBackIosIcon/>
        </IconButton>
        <IconButton onClick={()=>updateVal("add")}>
          <ArrowForwardIosIcon/>
        </IconButton>
      </CenterForm>
    </div>
  
  );
}

class SignUp extends React.Component{
  //constructor with all of the variables used for this component
  constructor(props){
    super(props);
    this.state = {
    email:"",
    username: "",
    password: "",
    retype:"",
    error:false,
    blank:true,
    authenticated:false,
    suError:false,
    eCode:""
    };
  }
  //updates the email and checks to see if any options are still blank
  //TODO: disable signup button until all filled in
  setEmail(e){
    this.setState({email: e})
    if(e !== "" && this.state.username !== "" && this.state.password !== "" && this.state.retype !== ""){
      this.setState({blank:false});
    }
  }
  setUsername(user){
    this.setState({username: user})
  }
  //updates password and checks to see if the retype password box matches
  setPassword(pass){
    this.setState({password: pass})
    if(this.state.retype === pass){
      this.setState({error: false})
    }else{
      if(this.state.retype !== ""){
        this.setState({error: true})
      }else{
        this.setState({error: false})
      }
    }
  }
  //if passwords dont match, we set error to true to show a red box
  checkPassword(pass){
    this.setState({retype:pass});
    if(this.state.password === pass){
      this.setState({error: false})
    }else{
      if(pass !== ""){
        this.setState({error: true})
      }else{
        this.setState({error: false})
      }
      
    }
  }

  submitClicked(){
    let info = {'username':this.state.username,'password':this.state.password,'email':this.state.email};
    fetch("http://127.0.0.1:5000/api/signup",{method:'post',credentials: 'include',headers:{"Content-Type": "application/json"},body:JSON.stringify(info)}).then(response => response.json()).then(data => {
      if(data.auth === 'done'){
        this.setState({authenticated:true});
      }else{
        this.setState({suError:true});
        this.setState({eCode:data.auth});
      }
      
    });
    
  }

  render(){
    
    //shows title and uses the CenterForm styled component to center everything
    //Text fields from MUI, when something is typed they update the value
    //the retype password text field has the error option in case the passwords dont match
    //buttons at the bottom of the page to finish sign up or go to sign in if they already have an account

    return (
      <div>
        <Navbar />
        
        <CenterForm>
          <h2>Sign Up</h2>
        </CenterForm>
        <CenterForm>
          <TextField onChange = {(event) => this.setEmail(event.target.value)} id="outlined-basic" label="Email" variant="outlined" margin="normal" />
        </CenterForm>
        <CenterForm>
          <TextField onChange = {(event) => this.setUsername(event.target.value)} id="outlined-basic" label="Username" variant="outlined" margin="normal" />
        </CenterForm>
        <CenterForm>
          <TextField type="password" onChange = {(event) => this.setPassword(event.target.value)} id="outlined-basic" label="Password" variant="outlined" margin="normal" />
        </CenterForm>
        <CenterForm>
          <TextField type="password" error={this.state.error} onChange = {(event) => this.checkPassword(event.target.value)} id="outlined-basic" label="Retype Password" variant="outlined" margin="normal" />
        </CenterForm>
        <CenterForm>
        {this.state.suError?<p style={{ color: 'red' }}>{this.state.eCode}</p>:<p> </p>}
      </CenterForm>
        <CenterForm>
          <LogBtn onClick={(event) => this.submitClicked()} type = "submit">Sign Up</LogBtn>
        </CenterForm>

        <CenterForm>
         <p>Click here to sign in:</p>
         </CenterForm>

        <CenterForm>
        <Link to='/signin' >
        <LogBtn>Sign In</LogBtn>
        </Link>
        </CenterForm>
        {this.state.authenticated?<Redirect to={'/project/'+this.state.username}/>:null}
      </div>
    );

  }

}

function SignIn() {
  //creating two variables for username and password and the functions to change their values
  //setting both of their initial values to blank
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [authenticated,setAuth] = useState(false);
  const [error,setError] = useState(false);
  const [errorCode,setErrorCode] = useState("");

  const submitClicked = ()=>{
    
    let info = {'username':username,'password':password};
    console.log(JSON.stringify(info))
    fetch("http://127.0.0.1:5000/api/signin",{method:'post',credentials: 'include',headers:{"Content-Type": "application/json","Access-Control-Allow-Headers":"Content-Type","Access-Control-Allow-Credentials":"true"},body:JSON.stringify(info)}).then(response => response.json())
    .then(data => {
      if(data.auth === 'pass'){
        setAuth(true);
      }else{
        setError(true);
        setErrorCode(data.auth);
      }
      
    });
    
  }

  return (
    <div>
    <Navbar />
      <CenterForm>
        <h2>Welcome!</h2>
      </CenterForm>
      
      <CenterForm>
        <TextField name="username" onChange = {(event) => setUsername(event.target.value)} id="outlined-basic" label="Username" variant="outlined" margin="normal" />
      </CenterForm>
      <CenterForm>
        <TextField type="password" name="password" onChange = {(event) => setPassword(event.target.value)} id="outlined-basic" label="Password" variant="outlined" margin="normal" />
      </CenterForm>
      <CenterForm>
        {error?<p style={{ color: 'red' }}>{errorCode}</p>:<p> </p>}
      </CenterForm>
      <CenterForm>
      <LogBtn onClick={submitClicked} type = "submit">Sign In</LogBtn>
      </CenterForm>

    

      <CenterForm>
      <p>Click here to sign up:</p>
      </CenterForm>

      <CenterForm>
      <Link to='/signup' >
        <LogBtn>Sign Up</LogBtn>
      </Link>
      </CenterForm>
      {authenticated?<Redirect to={'/project/'+username}/>:null}
    </div>
  );
}


