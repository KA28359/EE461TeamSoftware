import React, { Component } from 'react';
import '../../App.css';
import { CircularProgress } from '@mui/material';
import {
  LogBtn,
  CenterForm,
  CenterSpace,
  Nav,
  NavMenu
} from '../Navbar/NavbarElements';
import {
  BrowserRouter as Router,
  Switch,
  Redirect,
  Route,
  Link
} from "react-router-dom";
import Hardware from './hardware';
import DataSet from './dataset';
import'./resource.css'
import HwTable from './hardwareTable';

export default class ResourcePage extends React.Component{
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
      tested:false,
      name:this.props.match.params.userID.toString(),
      proid:this.props.match.params.proID.toString()
    };
  }

  // componentDidMount(){
  //   this._isMounted = true;
  //   let info = {'username':this.state.name,
  //               'projectid':this.state.proid};
  //   fetch("http://127.0.0.1:5000/api/project/authorized",{method:'post',credentials: 'include', headers:{"Content-Type": "application/json"},body:JSON.stringify(info)})
  //   .then(response => response.json())
  //   .then(data => {

  //     if(data.auth === 'rejected' && this._isMounted){
  //      this.setState({authorized:false})
  //      this.setState({tested:true})
  //     }
  //     if(data.auth === 'access' && this._isMounted){
  //     this.setState({tested:true})
  //     }
  //   });
  // }
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

  render(){
    // if(!this.state.tested){
    //   return(<div></div>);
    // }
    // else 
    // if(!this.state.authorized && this.state.tested){
    //   return <Redirect to='/'/>;
    // }else{

   
  return (
    <Router>
    <div>
      <Nav><NavMenu> <p style={{color:'#ffffff',fontSize:'2.5em'}}>TEAM SOFTWARE</p></NavMenu>
           <NavMenu> <h1 style={{color:'#ffffff'}}>UserID: {this.props.match.params.userID.toString()}</h1>
                     <Link className="nav-link" to={"/project/"+this.state.name+"/"+this.state.proid+"/dataset"}>DataSets</Link>
                     <Link className="nav-link" to={"/project/"+this.state.name+"/"+this.state.proid+"/hardware"}>Hardwares</Link>
                     <Link className="nav-link" to={"/project/"+this.state.name}>My projects</Link>
                     <LogBtn style={{backgroundColor:"#ffffff",color:"#000000",marginLeft:'24px'}}  onClick={(event) => this.signOut()} type = "submit">Sign Out</LogBtn>
           </NavMenu>
      </Nav>
      <Switch>
          <Route path="/project/:userID/:proID/dataSet"  component={DataSet}  />
          <Route path="/project/:userID/:proID/hardware"  component={Hardware}  />
      </Switch>  
    </div>
    </Router>
  
    );
   }
  }
  // function Hardware(){
  //   return <div><HwTable name={this.props.match.params.userID.toString()} 
  //                        proid={this.props.match.params.proID.toString()}/></div>
  // }
//}
