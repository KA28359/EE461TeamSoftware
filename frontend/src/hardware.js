import React from 'react';
import HwTable from './hardwareTable';
class Hardware extends React.Component{
  _isMounted = false;
  constructor(props){
    super(props);
    this.state = {
      name:this.props.match.params.userID.toString(),
      proid:this.props.match.params.proID.toString()
    };
}

   render(){
    return <div><HwTable name={this.state.name} proid={this.state.proid}/></div>;
   } 
}  


 
export default Hardware;