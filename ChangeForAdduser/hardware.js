import React, { Component } from 'react';
import HwTable from './hardwareTable';
import {Link} from 'react-router-dom';
import {
  LogBtn,
  CenterForm,
  CenterSpace,
} from '../Navbar/NavbarElements';
import {
  Redirect,
} from "react-router-dom";

class Hardware extends React.Component{
  _isMounted = false;
  constructor(props){
    super(props);
    this.state = {
      authorized:true,
      tested:false,
      username:'',
      name:this.props.match.params.userID.toString(),
      proid:this.props.match.params.proID.toString()
    };
}

componentDidMount=()=>{
    let info = {'username':this.props.match.params.userID.toString(),
                'projectid':this.props.match.params.proID.toString()};
    console.log(info)
    fetch("http://127.0.0.1:5000/api/project/authorized",{method:'post',credentials: 'include', headers:{"Content-Type": "application/json"},body:JSON.stringify(info)})
    .then(response => response.json())
    .then(data => {
      console.log(data)
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


   render(){
     if(!this.state.tested){
      // this.refreshAuth()
      return(
        <div></div>
      );
    }
    else if(!this.state.authorized){
      if(this.state.username !== ''){
        return(
        <div>
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

   
    return <div><HwTable name={this.state.name} proid={this.state.proid}/></div>;
   } 
}
}  


 
export default Hardware;