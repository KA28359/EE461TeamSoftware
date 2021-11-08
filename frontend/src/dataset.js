import React from 'react';
import { CircularProgress } from '@mui/material';
import {
  LogBtn,
  CenterSpace
} from './components/Navbar/NavbarElements';

class DataSet extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      counter:0,
      disbaled: false,
      data:[],
      authorized:true,
      spinner:false,
      index:0,
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

    render() { 
        return (
        <div>
            <CenterSpace>
            <table>
                <tbody>
                {this.state.data.length === 0 ? null:<tr><th>Name</th><th>Description</th><th>Download</th></tr>}
                {this.state.data.length === 0  ? null:this.getRows()}
                </tbody>
            </table>
            </CenterSpace>
            <CenterSpace>
                {this.state.spinner?<CircularProgress />:null}
            </CenterSpace>
            <CenterSpace>
                <LogBtn style={{backgroundColor:this.state.disbaled?"#808080":"#CC5500"}} disabled={this.state.disbaled} onClick={(event) => this.getData()} type = "submit">Get data</LogBtn>
            </CenterSpace>
        </div>
        )}
}
 
export default DataSet;